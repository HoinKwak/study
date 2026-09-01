"""멀티 타임프레임 ATR% 동시확장 동조 브레이크아웃 — 백테스트 엔진.

엔트리: 4h 봉 i 종가 확정 시점에 삼중 동조 rising-edge 판정(룩어헤드 없음, p1h/p4h/p1d 는 전부
common.build_signals 에서 asof-backward 매핑돼 미래 참조 불가) -> bar i+1 시가에 체결(shift(1)).
방향: 신호봉(i) 자신의 마감 방향(양봉=롱/음봉=숏).
청산: (1) 고정 SL = 진입가 ∓ ATR22(4h, 신호봉 시점)×1.5 (평생 고정)
      (2) 챈들리어 트레일(ATR22(4h)×3.5) — 진입 이후 매 봉마다 '직전까지 닫힌 봉들의 극값'
          기준으로 레벨을 계산해 이번 봉 인트라바 이탈시 청산, 그 후 이번 봉 극값을 반영해 래칫.
      (3) 시간청산: 보유 15봉(4h) 경과 시 강제 종가청산.
      같은 봉에서 SL/챈들리어 동시 이탈이면 SL 우선(하우스 컨벤션).
모든 성과는 R-배수(고정 리스크 가정, 진입가-SL 거리를 1R)로 계산 — 계좌소진/사이징 아티팩트 원천 차단.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE


@dataclass
class TradeRec:
    symbol: str
    direction: str          # 최종 체결 방향("long"/"short")
    orig_direction: str     # 원신호 방향(반전모드에서만 direction 과 다름)
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float       # 고정 SL
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


@dataclass
class RunConfig:
    pct_th: float = 60.0
    lookback_1h: int = 168
    lookback_4h: int = 42
    lookback_1d: int = 20
    atr_mult_sl: float = 1.5
    atr_mult_tp: float = 3.5   # 챈들리어 트레일 배수
    time_exit_bars: int = 15
    signal_mode: str = "triple"   # "triple" | "h1_only"(대조군c) | "h4_d1_only"(대조군d)
    direction_mode: str = "normal"  # "normal" | "reverse"
    cost_on: bool = True            # False -> gross(fee=0, slippage=0) 진단
    disable_chandelier: bool = False  # 반전모드 3안: 챈들리어 청산 완전 비활성(SL+시간청산만)


def _signal_mask(sig: common.Signals, cfg: RunConfig) -> np.ndarray:
    th = cfg.pct_th
    p1h, p4h, p1d = sig.p1h_at4h, sig.p4h_at4h, sig.p1d_at4h
    if cfg.signal_mode == "triple":
        return (p1h >= th) & (p4h >= th) & (p1d >= th)
    if cfg.signal_mode == "h1_only":
        return (p1h >= th)
    if cfg.signal_mode == "h4_d1_only":
        return (p4h >= th) & (p1d >= th)
    raise ValueError(cfg.signal_mode)


def run_symbol(symbol: str, sig: common.Signals, cfg: RunConfig) -> list[TradeRec]:
    h4 = sig.h4
    n = len(h4)
    close = h4["close"].to_numpy(float)
    high = h4["high"].to_numpy(float)
    low = h4["low"].to_numpy(float)
    open_ = h4["open"].to_numpy(float)
    idx = h4.index

    mask = _signal_mask(sig, cfg)
    valid = np.isfinite(sig.p1h_at4h) & np.isfinite(sig.p4h_at4h) & np.isfinite(sig.p1d_at4h)
    mask = mask & valid
    rising = mask & ~np.concatenate([[False], mask[:-1]])

    atr_sl_arr = sig.atr22_4h_signal      # 신호봉(i) 시점 ATR22 -> 고정 SL 계산
    atr_trail_arr = sig.atr22_4h_trail    # bar j 체크에 쓸 ATR22 = atr22[j-1](직전까지 닫힌 값)

    trades: list[TradeRec] = []
    trade: TradeRec | None = None
    pending: dict | None = None
    extreme = 0.0  # 챈들리어 러닝 극값(직전까지 닫힌 봉 기준)

    for i in range(0, n):
        # 0) 대기 체결
        if pending is not None and trade is None:
            sidx = pending["signal_idx"]
            entry_raw = open_[i]
            direction = pending["direction"]
            fill_px = _fill(entry_raw, direction, closing=False, apply_slip=cfg.cost_on)
            atr_v = atr_sl_arr[sidx]
            stop_dist = cfg.atr_mult_sl * atr_v
            if stop_dist > 0 and np.isfinite(stop_dist) and fill_px > 0:
                stop_price = fill_px - stop_dist if direction == "long" else fill_px + stop_dist
                trade = TradeRec(symbol=symbol, direction=direction,
                                 orig_direction=pending["orig_direction"],
                                 entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                 stop_price=stop_price)
                extreme = fill_px
            pending = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            exit_px = None
            reason = ""
            is_long = trade.direction == "long"
            # 1a) 고정 SL
            if is_long and l <= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"
            elif (not is_long) and h >= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"
            # 1b) 챈들리어 트레일(직전까지 닫힌 봉의 극값 + 직전 ATR22 로 이번 봉 레벨 계산)
            if exit_px is None and not cfg.disable_chandelier:
                atr_v = atr_trail_arr[i]
                if np.isfinite(atr_v):
                    if is_long:
                        level = extreme - cfg.atr_mult_tp * atr_v
                        if l <= level:
                            exit_px, reason = level, "chandelier"
                    else:
                        level = extreme + cfg.atr_mult_tp * atr_v
                        if h >= level:
                            exit_px, reason = level, "chandelier"
            # 1c) 시간청산
            if exit_px is None and (i - trade.entry_idx) >= cfg.time_exit_bars:
                exit_px, reason = c, "time_exit"

            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True, apply_slip=cfg.cost_on)
                dirn = 1.0 if is_long else -1.0
                raw = dirn * (fill_px - trade.entry_price)
                risk_dist = abs(trade.entry_price - trade.stop_price)
                r_gross = raw / risk_dist if risk_dist > 0 else 0.0
                fee_cost = TAKER_FEE * (trade.entry_price + fill_px) if cfg.cost_on else 0.0
                r_net = (raw - fee_cost) / risk_dist if risk_dist > 0 else 0.0
                trade.exit_idx = i; trade.exit_time = idx[i]; trade.exit_price = fill_px
                trade.reason = reason; trade.holding_bars = i - trade.entry_idx
                trade.r_gross = r_gross; trade.r_net = r_net
                trades.append(trade)
                trade = None
            else:
                # 챈들리어 극값 래칫(이번 봉 자신의 고/저를 이번 봉 종가확정 시점에 반영 ->
                # 다음 봉 레벨 계산에만 쓰임, 이번 봉 판정엔 미반영이라 룩어헤드 아님)
                extreme = max(extreme, h) if is_long else min(extreme, l)

        # 2) 신규 진입 판정(이번 bar 종가 기준 rising-edge) -> 다음 bar 시가 체결
        if trade is None and pending is None and i + 1 < n and rising[i]:
            o_i, c_i = open_[i], close[i]
            if c_i > o_i:
                orig_dir = "long"
            elif c_i < o_i:
                orig_dir = "short"
            else:
                orig_dir = None
            if orig_dir is not None:
                exec_dir = orig_dir
                if cfg.direction_mode == "reverse":
                    exec_dir = "short" if orig_dir == "long" else "long"
                pending = {"direction": exec_dir, "orig_direction": orig_dir, "signal_idx": i}

    return trades


def load_all_signals(symbols=common.SYMBOLS, **kw) -> dict[str, common.Signals]:
    out = {}
    for s in symbols:
        sig = common.build_signals(s, **kw)
        if sig is not None:
            out[s] = sig
    return out


def run_all(symbols_sig: dict[str, common.Signals], cfg: RunConfig) -> dict[str, list[TradeRec]]:
    return {sym: run_symbol(sym, sig, cfg) for sym, sig in symbols_sig.items()}
