"""멀티TF CLV(Close Location Value) 정렬 추세추종 스캘프 — 백테스트 엔진.

엔트리: 15m 봉 i 종가 확정 시점에
        CLV_15m[i](자기 자신) AND CLV_1h(그 시각까지 닫힌 가장 최근 1h봉, merge_asof backward)
        AND CLV_4h(동일하게 4h봉) 이 방향 정렬 + 거래량 필터 → i+1봉 시가 체결(shift(1)).
        1h/4h 는 "봉이 닫혀 값이 확정된 시각"(open_time+봉길이) 기준 causal 매핑이라
        naive 매핑(그 시각을 포함하는 상위봉 구간 통째로 매핑)과 달리 미확정봉을 참조하지 않는다.
방향: 롱 CLV_15m>=th15L AND CLV_1h>=th1hL AND CLV_4h>=th4hL(vol_ok), 숏은 대칭(<=).
청산: (1) 고정 SL = entry ∓ ATR(15m,14)[i]×atr_stop_mult (스칼라, 방향 무관 — 반전에서도 그대로
          대칭 재배치되므로 "자연스러운 극값 재계산" 문제 자체가 발생하지 않음).
      (2) ATR(15m,14) 트레일링×atr_trail_mult — 직전까지 닫힌 봉들의 극값 기준.
      (3) 15m CLV 반대극단 조기청산: **원신호 방향(orig_direction) 기준** — 이 청산은 SL/트레일링류의
          리스크관리 메커니즘이 아니라 스펙이 명시한 '조건 청산'(서사적 테제 무효화)이라, CLAUDE.md
          확립 규칙("SL은 표준 대칭재배치, 서사적 테제 무효화는 원신호 기준")과 mtfcvd repro 선례를
          따른다. 최종방향(반전 포함) 기준으로 두면 반전모드가 진입 직후 구조적으로 퇴화할 위험이 있음.
      (4) 시간청산: max_hold_bars 경과.
      동봉 동시성립 시 SL > 트레일링 > CLV반전청산 > 시간청산 순 우선.
전 성과는 R-배수(risk_dist=ATR15[i]×atr_stop_mult)로 계산 — 계좌소진/사이징 아티팩트 원천 차단.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
from crypto_trader.signals import indicators as ind  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE


@dataclass
class RunConfig:
    clv15_th_long: float = 0.75
    clv15_th_short: float = 0.25
    clv1h_th_long: float = 0.65
    clv1h_th_short: float = 0.35
    clv4h_th_long: float = 0.60
    clv4h_th_short: float = 0.40
    vol_mult: float = 1.2
    vol_lookback: int = 20
    atr_stop_mult: float = 1.0
    atr_trail_mult: float = 2.0
    max_hold_bars: int = 32
    signal_mode: str = "all3"       # "all3"(base) | "15m_only" | "two_tf"(15m+1h) | "no_gate"
    direction_mode: str = "normal"  # "normal" | "reverse"
    cost_on: bool = True
    disable_clv_flip_exit: bool = False  # 반전모드 제3의대안: CLV반전 조기청산 완전 비활성


@dataclass
class Signals:
    h15: pd.DataFrame
    clv15: np.ndarray
    clv1h_at15: np.ndarray
    clv4h_at15: np.ndarray
    vol_ok: np.ndarray
    atr15: np.ndarray
    nan_frac_1h: float
    nan_frac_4h: float


def build_signals(symbol: str, cfg: RunConfig) -> Signals | None:
    h15 = common.load_klines(symbol, "15m")
    h1 = common.load_klines(symbol, "1h")
    h4 = common.load_klines(symbol, "4h")
    if h15.empty or h1.empty or h4.empty:
        return None

    clv15 = common.clv(h15)
    clv1h = common.clv(h1)
    clv4h = common.clv(h4)

    close15 = (h15.index + pd.Timedelta(minutes=15)).astype("datetime64[ns, UTC]")
    clv1h_at15 = common.map_asof_backward(pd.DatetimeIndex(close15), clv1h, 3600)
    clv4h_at15 = common.map_asof_backward(pd.DatetimeIndex(close15), clv4h, 4 * 3600)

    lb = cfg.vol_lookback
    vol_mean_prev = h15["volume"].shift(1).rolling(lb, min_periods=lb).mean()
    vol_ok = (h15["volume"] >= cfg.vol_mult * vol_mean_prev).to_numpy()

    atr15 = ind.atr(h15, 14).to_numpy(float)

    nan_frac_1h = float(np.isnan(clv1h_at15).mean())
    nan_frac_4h = float(np.isnan(clv4h_at15).mean())

    return Signals(h15=h15, clv15=clv15.to_numpy(float), clv1h_at15=clv1h_at15,
                   clv4h_at15=clv4h_at15, vol_ok=vol_ok, atr15=atr15,
                   nan_frac_1h=nan_frac_1h, nan_frac_4h=nan_frac_4h)


@dataclass
class TradeRec:
    symbol: str
    direction: str
    orig_direction: str
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float
    risk_dist: float
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    reason: str = ""
    holding_bars: int = 0
    r_gross: float = 0.0
    r_net: float = 0.0


def _fill(price: float, direction: str, closing: bool, apply_slip: bool) -> float:
    if not apply_slip:
        return price
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * SLIPPAGE)


def _orig_dir_at(sig: Signals, i: int, cfg: RunConfig) -> str | None:
    """이번 봉 i 종가 기준 원신호 방향(정렬조건 판정, signal_mode 별 분기)."""
    c15, c1h, c4h, vok = sig.clv15[i], sig.clv1h_at15[i], sig.clv4h_at15[i], sig.vol_ok[i]
    if not vok:
        return None
    mode = cfg.signal_mode
    if mode == "no_gate":
        h15 = sig.h15
        o, c = h15["open"].iloc[i], h15["close"].iloc[i]
        if c > o:
            return "long"
        if c < o:
            return "short"
        return None
    if not np.isfinite(c15):
        return None
    long_ok = c15 >= cfg.clv15_th_long
    short_ok = c15 <= cfg.clv15_th_short
    if mode == "15m_only":
        pass
    elif mode == "two_tf":
        if not np.isfinite(c1h):
            return None
        long_ok = long_ok and (c1h >= cfg.clv1h_th_long)
        short_ok = short_ok and (c1h <= cfg.clv1h_th_short)
    elif mode == "all3":
        if not (np.isfinite(c1h) and np.isfinite(c4h)):
            return None
        long_ok = long_ok and (c1h >= cfg.clv1h_th_long) and (c4h >= cfg.clv4h_th_long)
        short_ok = short_ok and (c1h <= cfg.clv1h_th_short) and (c4h <= cfg.clv4h_th_short)
    else:
        raise ValueError(mode)
    if long_ok and not short_ok:
        return "long"
    if short_ok and not long_ok:
        return "short"
    return None


def run_symbol(symbol: str, sig: Signals, cfg: RunConfig) -> list[TradeRec]:
    h15 = sig.h15
    n = len(h15)
    open_ = h15["open"].to_numpy(float)
    high = h15["high"].to_numpy(float)
    low = h15["low"].to_numpy(float)
    close = h15["close"].to_numpy(float)
    idx = h15.index

    trades: list[TradeRec] = []
    trade: TradeRec | None = None
    pending: dict | None = None
    extreme = 0.0

    for i in range(n):
        # 0) 대기 체결
        if pending is not None and trade is None:
            direction = pending["direction"]
            fill_px = _fill(open_[i], direction, closing=False, apply_slip=cfg.cost_on)
            risk_dist = pending["risk_dist"]
            if risk_dist > 0 and np.isfinite(risk_dist) and fill_px > 0:
                stop_price = fill_px - risk_dist if direction == "long" else fill_px + risk_dist
                trade = TradeRec(symbol=symbol, direction=direction,
                                 orig_direction=pending["orig_direction"],
                                 entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                 stop_price=stop_price, risk_dist=risk_dist)
                extreme = fill_px
            pending = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            is_long = trade.direction == "long"
            exit_px = None
            reason = ""
            # 1a) 고정 SL
            if is_long and l <= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"
            elif (not is_long) and h >= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"
            # 1b) ATR 트레일링(직전까지 닫힌 봉 기준 극값 + 직전봉 ATR)
            if exit_px is None:
                atr_v = sig.atr15[i - 1] if i > 0 else np.nan
                if np.isfinite(atr_v):
                    if is_long:
                        level = extreme - cfg.atr_trail_mult * atr_v
                        if l <= level:
                            exit_px, reason = level, "atr_trail"
                    else:
                        level = extreme + cfg.atr_trail_mult * atr_v
                        if h >= level:
                            exit_px, reason = level, "atr_trail"
            # 1c) CLV 반대극단 조기청산(원신호 방향 기준)
            if exit_px is None and not cfg.disable_clv_flip_exit:
                c15 = sig.clv15[i]
                if np.isfinite(c15):
                    if trade.orig_direction == "long" and c15 <= cfg.clv15_th_short:
                        exit_px, reason = c, "clv_flip"
                    elif trade.orig_direction == "short" and c15 >= cfg.clv15_th_long:
                        exit_px, reason = c, "clv_flip"
            # 1d) 시간청산
            if exit_px is None and (i - trade.entry_idx) >= cfg.max_hold_bars:
                exit_px, reason = c, "time_exit"

            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True, apply_slip=cfg.cost_on)
                dirn = 1.0 if is_long else -1.0
                raw = dirn * (fill_px - trade.entry_price)
                r_gross = raw / trade.risk_dist
                fee_cost = TAKER_FEE * (trade.entry_price + fill_px) if cfg.cost_on else 0.0
                r_net = (raw - fee_cost) / trade.risk_dist
                trade.exit_idx = i; trade.exit_time = idx[i]; trade.exit_price = fill_px
                trade.reason = reason; trade.holding_bars = i - trade.entry_idx
                trade.r_gross = r_gross; trade.r_net = r_net
                trades.append(trade)
                trade = None
            else:
                extreme = max(extreme, h) if is_long else min(extreme, l)

        # 2) 신규 진입 판정(이번 bar 종가 기준) -> 다음 bar 시가 체결
        if trade is None and pending is None and i + 1 < n:
            orig_dir = _orig_dir_at(sig, i, cfg)
            if orig_dir is not None:
                exec_dir = orig_dir
                if cfg.direction_mode == "reverse":
                    exec_dir = "short" if orig_dir == "long" else "long"
                risk_dist = sig.atr15[i] * cfg.atr_stop_mult if np.isfinite(sig.atr15[i]) else np.nan
                if np.isfinite(risk_dist) and risk_dist > 0:
                    pending = {"direction": exec_dir, "orig_direction": orig_dir,
                              "risk_dist": risk_dist}

    return trades


def load_all_signals(symbols=common.SYMBOLS, cfg: RunConfig = RunConfig()) -> dict[str, Signals]:
    out = {}
    for s in symbols:
        sig = build_signals(s, cfg)
        if sig is not None:
            out[s] = sig
    return out


def run_all(symbols_sig: dict[str, Signals], cfg: RunConfig) -> dict[str, list[TradeRec]]:
    return {sym: run_symbol(sym, sig, cfg) for sym, sig in symbols_sig.items()}
