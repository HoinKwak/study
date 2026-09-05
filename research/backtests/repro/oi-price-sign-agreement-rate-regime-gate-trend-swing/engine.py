"""가격-OI 변화 부호일치율(Co-Sign Agreement Rate) 게이트 + BTC EMA20/50 추세추종 — 백테스트 엔진.

전부 4h(스펙 진입규칙·파라미터 절이 EMA20/50도 4h로 명시 — 헤더의 "1d(EMA20/50 추세확인)"과
불일치하나 문자 그대로의 진입규칙·파라미터를 우선해 4h로 구현, 리포트 §0에 명시).

신호(4h, BTC EMA20/50 크로스 + agree_pctile 게이트):
  - 4h 봉 t 종가 확정 시점에: EMA20(t) 가 EMA50(t)를 상향/하향 크로스(t-1 대비 부호 전환).
  - 게이트: 크로스 확정봉 t 자신의 agree_pctile(t) >= hi_th (같은 봉 — 룩어헤드 아님, agree_pctile(t)는
    봉 t 종가로 확정되는 ΔOI(t)·ΔPrice(t)까지만 사용).
  - 체결: 크로스 확정봉(t) **다음 4h 봉(t+1)의 시가**에 진입.
  - ATR(20,4h) 은 진입 시점 직전 완결 봉(entry_i-1 = t) 값 사용.
  - 청산: 고정 SL(ATR×2.5, 대칭재배치) **또는** 반대방향 EMA20/50 크로스(최종 direction 변수 기준) —
    시간청산·트레일 없음(스펙 "시간/조건 청산: 없음" 그대로).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "OISIGN_REPO_SRC", "/home/user/study/.claude/worktrees/agent-a64cdc714957bee50/src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE

GATE_MODES = ["base", "none", "lowagree", "corr", "swap", "reverse"]


@dataclass
class TradeRec:
    direction: str          # "long"/"short" (최종 방향 — reverse 모드에서 뒤집힌 값)
    raw_direction: str      # EMA 크로스 원신호 방향(reverse 모드 전)
    gate: str
    signal_idx: int         # 크로스 확정봉(t) 인덱스
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    fixed_stop: float
    quantity: float
    risk_amount: float
    gate_metric_at_signal: float
    fee_entry: float = 0.0
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    fee_exit: float = 0.0
    pnl: float = 0.0
    r_multiple: float = 0.0
    reason: str = ""
    holding_bars: int = 0


def _fill(price: float, direction: str, closing: bool, fee_on: bool) -> float:
    if not fee_on:
        return price
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * SLIPPAGE)


def _fee(notional: float, fee_on: bool) -> float:
    if not fee_on:
        return 0.0
    return abs(notional) * TAKER_FEE


@dataclass
class RunConfig:
    hi_th: float = common.HI_TH
    atr_stop_mult: float = common.ATR_STOP_MULT
    gate: str = "base"     # base|none|lowagree|corr|swap|reverse
    fee_on: bool = True
    starting_equity: float = 10_000.0


def _ema_cross_events(ema_fast: np.ndarray, ema_slow: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """golden_at[k]: EMA_fast가 EMA_slow를 k에서 상향돌파 확정(k>=1). death_at[k]: 하향돌파 확정."""
    n = len(ema_fast)
    golden_at = np.zeros(n, dtype=bool)
    death_at = np.zeros(n, dtype=bool)
    prev_above = ema_fast[:-1] > ema_slow[:-1]
    curr_above = ema_fast[1:] > ema_slow[1:]
    valid = (np.isfinite(ema_fast[:-1]) & np.isfinite(ema_slow[:-1]) &
             np.isfinite(ema_fast[1:]) & np.isfinite(ema_slow[1:]))
    golden_at[1:] = valid & (~prev_above) & curr_above
    death_at[1:] = valid & prev_above & (~curr_above)
    return golden_at, death_at


def run_btc(sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager) -> list[TradeRec]:
    symbol = "BTCUSDT"
    df4h = sig.df4h
    n4h = len(df4h)

    o4 = df4h["open"].to_numpy(float)
    h4 = df4h["high"].to_numpy(float)
    l4 = df4h["low"].to_numpy(float)
    c4 = df4h["close"].to_numpy(float)
    atr20 = sig.atr20.to_numpy(float)

    ema_f = sig.ema_fast.to_numpy(float)
    ema_s = sig.ema_slow.to_numpy(float)
    golden_at, death_at = _ema_cross_events(ema_f, ema_s)

    agree_pctile = sig.agree_pctile.to_numpy(float)
    corr_pctile = sig.corr_pctile.to_numpy(float)
    agree_vol_pctile = sig.agree_vol_pctile.to_numpy(float)

    lo_th = 100.0 - cfg.hi_th

    events = ([(t, "long") for t in np.where(golden_at)[0]] +
              [(t, "short") for t in np.where(death_at)[0]])
    events.sort()

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    lev = settings.leverage_for("BTC/USDT")
    next_available_4h = -1

    for t, raw_direction in events:
        if cfg.gate == "base":
            gm = agree_pctile[t]
            ok = np.isfinite(gm) and gm >= cfg.hi_th
        elif cfg.gate == "none":
            gm = agree_pctile[t]
            ok = True
        elif cfg.gate == "lowagree":
            gm = agree_pctile[t]
            ok = np.isfinite(gm) and gm <= lo_th
        elif cfg.gate == "corr":
            gm = corr_pctile[t]
            ok = np.isfinite(gm) and gm >= cfg.hi_th
        elif cfg.gate == "swap":
            gm = agree_vol_pctile[t]
            ok = np.isfinite(gm) and gm >= cfg.hi_th
        elif cfg.gate == "reverse":
            gm = agree_pctile[t]
            ok = np.isfinite(gm) and gm >= cfg.hi_th
        else:
            raise ValueError(cfg.gate)
        if not ok:
            continue

        direction = raw_direction
        if cfg.gate == "reverse":
            direction = "short" if raw_direction == "long" else "long"

        entry_i = t + 1
        if entry_i <= next_available_4h:
            continue  # 동시 포지션 금지(직전 트레이드 미청산)
        if entry_i >= n4h - 1:
            continue

        entry_raw = o4[entry_i]
        atr_v = atr20[entry_i - 1] if entry_i - 1 >= 0 else np.nan
        if not (np.isfinite(atr_v) and atr_v > 0 and entry_raw > 0):
            continue

        sl_dist = cfg.atr_stop_mult * atr_v
        fill_px = _fill(entry_raw, direction, closing=False, fee_on=cfg.fee_on)
        if direction == "long":
            fixed_stop = fill_px - sl_dist
            dirn = Direction.LONG
        else:
            fixed_stop = fill_px + sl_dist
            dirn = Direction.SHORT

        plan = risk.build_plan_with_stop(symbol, dirn, fill_px, fixed_stop, fill_px, equity,
                                         leverage=lev)
        if plan is None or plan.quantity <= 0:
            continue

        fee_entry = _fee(fill_px * plan.quantity, cfg.fee_on)
        trade = TradeRec(direction=direction, raw_direction=raw_direction, gate=cfg.gate,
                         signal_idx=t, entry_idx=entry_i, entry_time=df4h.index[entry_i],
                         entry_price=fill_px, fixed_stop=fixed_stop, quantity=plan.quantity,
                         risk_amount=plan.risk_amount,
                         gate_metric_at_signal=float(gm) if np.isfinite(gm) else float("nan"),
                         fee_entry=fee_entry)
        equity -= fee_entry

        is_long = direction == "long"
        # 반대방향 EMA 크로스 이벤트 — 최종 direction 기준(리스크 원칙 §6 준수)
        opp_event = death_at if is_long else golden_at

        exit_i = None; exit_px = None; reason = ""
        j = entry_i
        while j < n4h:
            h, l, cl = h4[j], l4[j], c4[j]
            stop_level = trade.fixed_stop
            hit = (l <= stop_level) if is_long else (h >= stop_level)
            if hit:
                exit_i = j; exit_px = stop_level; reason = "stop"; break
            if opp_event[j]:
                exit_i = j; exit_px = cl; reason = "ema_reverse"; break
            j += 1
        if exit_i is None:
            exit_i = n4h - 1; exit_px = c4[exit_i]; reason = "data_end"

        fill_exit = _fill(exit_px, direction, closing=True, fee_on=cfg.fee_on)
        fee_exit = _fee(fill_exit * trade.quantity, cfg.fee_on)
        raw = ((fill_exit - trade.entry_price) if is_long
              else (trade.entry_price - fill_exit)) * trade.quantity
        pnl = raw - fee_entry - fee_exit   # ⚠️진입 수수료도 pnl에 반영(두 라운드 연속 나온 버그 회피)
        trade.exit_idx = exit_i; trade.exit_time = df4h.index[exit_i]; trade.exit_price = fill_exit
        trade.pnl = pnl; trade.fee_exit = fee_exit; trade.reason = reason
        trade.holding_bars = exit_i - entry_i
        trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
        equity += pnl
        trades.append(trade)
        next_available_4h = exit_i

    return trades


def run_config(sig: common.Signals, cfg: RunConfig) -> list[TradeRec]:
    settings = get_settings()
    risk = RiskManager(settings)
    return run_btc(sig, cfg, settings, risk)
