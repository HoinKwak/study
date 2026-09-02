"""수익률 1차 자기상관 부호전환 레짐스위치 스캘프 — 백테스트 엔진.

레짐(1h, rho=lag-1 자기상관 rolling N=60): rho<=-rho_th -> MR(평균회귀), rho>=+rho_th -> MOM(추세추종),
그 사이는 중립(무거래). 레짐값은 1h 봉 확정시각(open_time+1h)에 확정되어 그 다음 1h 동안 15m 그리드에
고정 매핑(merge_asof backward, 룩어헤드 없음).

MR 트리거(15m): 직전 k봉 누적가격변화 >= +ext_mult*ATR15 -> 숏(과확장 페이드), <= -ext_mult*ATR15 -> 롱.
MOM 트리거(15m): 20봉 Donchian(직전 봉까지, self-reference 배제) 상단 돌파+거래량조건 -> 롱, 하단 -> 숏.

신호는 봉 i 종가 확정 시점에 판정 -> 봉 i+1 시가에 체결(shift(1), 룩어헤드 없음).

청산(서브모드별로 완전히 다름, 진입 시점 서브모드 고정 — 레짐이 바뀌어도 보유 포지션은 진입시
로직 그대로 청산):
  MR: EMA20 복귀(TP) / 과확장극값 바깥 sl_mult*ATR(SL) / mr_max_hold 시간청산.
  MOM: ATR 트레일링(TP) / 신호봉 반대극값(SL) / mom_max_hold 시간청산.
  같은 봉에서 여러 조건 동시 성립 시 SL > TP(revert/trail) > 시간청산 순 우선.

리스크거리(risk_dist)는 신호봉 종가(close[i])를 진입가 근사로 써서 신호 확정 시점에 1회 계산하고,
실제 체결가(fill_price) 기준으로 대칭 재배치한다(entry -+ risk_dist) — 반전모드에서 "그 방향의
자연스러운 극값"을 다시 계산하지 않고 원신호 기준 거리를 그대로 씀(CLAUDE.md 신규규칙 준수).
전 성과는 이 risk_dist 기준 R-배수로 계산(계좌소진/사이징 아티팩트 원천 차단).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
import indicators as racsr_ind  # noqa: E402
from crypto_trader.signals import indicators as ind  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE

N_1H = 60          # rho 롤링윈도(1h봉)


@dataclass
class RunConfig:
    rho_th: float = 0.15
    k: int = 3
    ext_mult: float = 1.5
    donchian_n: int = 20
    vol_mult: float = 1.5
    sl_mult: float = 1.0
    trail_mult: float = 1.5
    mr_max_hold: int = 8         # 15m봉 = 2h
    mom_max_hold: int = 16       # 15m봉 = 4h
    signal_mode: str = "gated"   # "gated"|"mr_only_ungated"|"mom_only_ungated"|"no_gate_both"
    direction_mode: str = "normal"  # "normal"|"reverse"
    cost_on: bool = True         # False=gross(수수료0·슬리피지0)
    disable_mr_tp: bool = False  # 3안: 반전모드 퇴화 점검용 — MR EMA복귀 TP 비활성(SL/시간청산만)


@dataclass
class Signals:
    h15: pd.DataFrame
    regime15: np.ndarray     # -1=MR, +1=MOM, 0=중립/미확정
    rho15: np.ndarray        # 진단용 원값
    atr15: np.ndarray
    ema20: np.ndarray
    mr_long_trig: np.ndarray
    mr_short_trig: np.ndarray
    mr_extreme_low: np.ndarray   # 직전 k봉(현재봉 포함) 최저 저가 -> 롱 SL 앵커
    mr_extreme_high: np.ndarray  # 직전 k봉(현재봉 포함) 최고 고가 -> 숏 SL 앵커
    mom_breakout_up: np.ndarray
    mom_breakout_down: np.ndarray
    mom_vol_ok: np.ndarray
    rho1h: pd.Series         # 진단용(1h grid)


def build_signals(symbol: str, cfg: RunConfig) -> Signals | None:
    h15 = common.load_klines(symbol, "15m")
    h1 = common.load_klines(symbol, "1h")
    if h15.empty or h1.empty:
        return None

    r1h = racsr_ind.log_returns(h1["close"])
    rho1h = racsr_ind.rolling_lag1_autocorr(r1h, N_1H)

    regime1h = pd.Series(0, index=h1.index, dtype=int)
    regime1h[rho1h <= -cfg.rho_th] = -1
    regime1h[rho1h >= cfg.rho_th] = 1

    close15_avail = (h15.index + pd.Timedelta(hours=1)).astype("datetime64[ns, UTC]")
    # 1h 봉이 확정된 시각(open_time+1h)에 그 값이 사용 가능 -> 15m 그리드에 backward asof
    regime15 = common.map_asof_backward(pd.DatetimeIndex(h15.index), regime1h.astype(float), 3600)
    regime15 = np.nan_to_num(regime15, nan=0.0).astype(int)
    rho15 = common.map_asof_backward(pd.DatetimeIndex(h15.index), rho1h, 3600)

    atr15 = ind.atr(h15, 14).to_numpy(float)
    ema20 = ind.ema(h15["close"], 20).to_numpy(float)

    close = h15["close"].to_numpy(float)
    k = cfg.k
    cum_ret_k = close - np.concatenate([np.full(k, np.nan), close[:-k]]) if k < len(close) else \
        np.full(len(close), np.nan)
    mr_short_trig = cum_ret_k >= cfg.ext_mult * atr15
    mr_long_trig = cum_ret_k <= -cfg.ext_mult * atr15

    low_roll = h15["low"].rolling(k, min_periods=k).min().to_numpy(float)
    high_roll = h15["high"].rolling(k, min_periods=k).max().to_numpy(float)

    lb = cfg.donchian_n
    high_prev_max = h15["high"].shift(1).rolling(lb, min_periods=lb).max().to_numpy(float)
    low_prev_min = h15["low"].shift(1).rolling(lb, min_periods=lb).min().to_numpy(float)
    mom_breakout_up = (close > high_prev_max)
    mom_breakout_down = (close < low_prev_min)
    vol = h15["volume"].to_numpy(float)
    vol_ma_prev = h15["volume"].shift(1).rolling(lb, min_periods=lb).mean().to_numpy(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        vol_ratio = vol / vol_ma_prev
    mom_vol_ok = vol_ratio >= cfg.vol_mult

    return Signals(h15=h15, regime15=regime15, rho15=rho15, atr15=atr15, ema20=ema20,
                   mr_long_trig=mr_long_trig, mr_short_trig=mr_short_trig,
                   mr_extreme_low=low_roll, mr_extreme_high=high_roll,
                   mom_breakout_up=mom_breakout_up.astype(bool),
                   mom_breakout_down=mom_breakout_down.astype(bool),
                   mom_vol_ok=np.nan_to_num(mom_vol_ok, nan=False).astype(bool),
                   rho1h=rho1h)


@dataclass
class TradeRec:
    symbol: str
    mode: str            # "MR"|"MOM"
    direction: str        # 최종(실행) 방향
    orig_direction: str
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float
    risk_dist: float
    regime_at_entry: int
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    reason: str = ""
    holding_bars: int = 0
    r_gross: float = 0.0
    r_net: float = 0.0


def _fill(price: float, direction: str, closing: bool, apply_cost: bool) -> float:
    if not apply_cost:
        return price
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * SLIPPAGE)


def _detect_trigger(sig: Signals, i: int, mode: str):
    """(submode, orig_direction) 반환, 없으면 None. mode 는 RunConfig.signal_mode."""
    reg = sig.regime15[i]

    def mr_check():
        if sig.mr_short_trig[i]:
            return "MR", "short"
        if sig.mr_long_trig[i]:
            return "MR", "long"
        return None

    def mom_check():
        if not sig.mom_vol_ok[i]:
            return None
        if sig.mom_breakout_up[i]:
            return "MOM", "long"
        if sig.mom_breakout_down[i]:
            return "MOM", "short"
        return None

    if mode == "gated":
        if reg == -1:
            return mr_check()
        if reg == 1:
            return mom_check()
        return None
    if mode == "mr_only_ungated":
        return mr_check()
    if mode == "mom_only_ungated":
        return mom_check()
    if mode == "no_gate_both":
        r = mom_check()
        if r is not None:
            return r
        return mr_check()
    raise ValueError(mode)


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
    extreme = 0.0  # MOM 트레일링용 극값 추적

    for i in range(n):
        # 0) 대기 체결
        if pending is not None and trade is None:
            direction = pending["direction"]
            fill_px = _fill(open_[i], direction, closing=False, apply_cost=cfg.cost_on)
            risk_dist = pending["risk_dist"]
            if risk_dist > 0 and np.isfinite(risk_dist) and fill_px > 0:
                stop_price = fill_px - risk_dist if direction == "long" else fill_px + risk_dist
                trade = TradeRec(symbol=symbol, mode=pending["mode"], direction=direction,
                                 orig_direction=pending["orig_direction"],
                                 entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                 stop_price=stop_price, risk_dist=risk_dist,
                                 regime_at_entry=pending["regime_at_entry"])
                extreme = fill_px
            pending = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            is_long = trade.direction == "long"
            exit_px = None
            reason = ""
            # 1a) 고정 SL (최우선)
            if is_long and l <= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"
            elif (not is_long) and h >= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"

            if exit_px is None and trade.mode == "MR":
                if not cfg.disable_mr_tp:
                    e20 = sig.ema20[i]
                    if np.isfinite(e20):
                        if is_long and h >= e20:
                            exit_px, reason = e20, "mr_ema_revert"
                        elif (not is_long) and l <= e20:
                            exit_px, reason = e20, "mr_ema_revert"
                if exit_px is None and (i - trade.entry_idx) >= cfg.mr_max_hold:
                    exit_px, reason = c, "time_exit"
            elif exit_px is None and trade.mode == "MOM":
                atr_v = sig.atr15[i - 1] if i > 0 else np.nan
                if np.isfinite(atr_v):
                    if is_long:
                        level = extreme - cfg.trail_mult * atr_v
                        if l <= level:
                            exit_px, reason = level, "atr_trail"
                    else:
                        level = extreme + cfg.trail_mult * atr_v
                        if h >= level:
                            exit_px, reason = level, "atr_trail"
                if exit_px is None and (i - trade.entry_idx) >= cfg.mom_max_hold:
                    exit_px, reason = c, "time_exit"

            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True, apply_cost=cfg.cost_on)
                dirn = 1.0 if is_long else -1.0
                raw = dirn * (fill_px - trade.entry_price)
                r_gross_cost = raw / trade.risk_dist
                if cfg.cost_on:
                    fee_cost = TAKER_FEE * (trade.entry_price + fill_px)
                    r_net = (raw - fee_cost) / trade.risk_dist
                else:
                    r_net = r_gross_cost
                trade.exit_idx = i; trade.exit_time = idx[i]; trade.exit_price = fill_px
                trade.reason = reason; trade.holding_bars = i - trade.entry_idx
                trade.r_gross = r_gross_cost; trade.r_net = r_net
                trades.append(trade)
                trade = None
            else:
                if trade.mode == "MOM":
                    extreme = max(extreme, h) if is_long else min(extreme, l)

        # 2) 신규 진입 판정(이번 bar 종가 기준) -> 다음 bar 시가 체결
        if trade is None and pending is None and i + 1 < n:
            det = _detect_trigger(sig, i, cfg.signal_mode)
            if det is not None:
                submode, orig_dir = det
                if submode == "MR":
                    if orig_dir == "short":
                        stop_level = sig.mr_extreme_high[i] + cfg.sl_mult * sig.atr15[i]
                    else:
                        stop_level = sig.mr_extreme_low[i] - cfg.sl_mult * sig.atr15[i]
                else:  # MOM
                    stop_level = low[i] if orig_dir == "long" else high[i]
                risk_dist = abs(close[i] - stop_level)
                if np.isfinite(risk_dist) and risk_dist > 0:
                    exec_dir = orig_dir
                    if cfg.direction_mode == "reverse":
                        exec_dir = "short" if orig_dir == "long" else "long"
                    pending = {"direction": exec_dir, "orig_direction": orig_dir,
                              "mode": submode, "signal_idx": i, "risk_dist": risk_dist,
                              "regime_at_entry": int(sig.regime15[i])}

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
