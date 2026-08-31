"""체결건수 방향 스트릭 지속 브레이크아웃 — 백테스트 엔진.

엔트리: 신호는 bar i 종가 확정 시점에 판정(룩어헤드 없음) -> bar i+1 시가에 체결(shift(1) 진입).
청산: 스톱(고정SL 진입가∓ATR×1.3 vs ATR×2.5 트레일링 중 유리한(래칫) 값)은 인트라바(고저) 체크,
     스트릭반전 조기청산·시간청산은 판정 시점(그 bar 종가)에 체결.
스톱 체크는 "이전 bar 까지 갱신된" stop_price 를 사용하고, 트레일링 갱신은 그 다음 순서로 이번
bar 의 high/low/ATR 로 이뤄져 다음 bar 부터 반영된다(같은 bar 내 룩어헤드 없음, scalp.py 관용 패턴).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

import os  # noqa: E402
sys.path.insert(0, os.environ.get(
    "TCSTREAK_REPO_SRC", str(Path(__file__).resolve().parents[4] / "src")))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE


@dataclass
class TradeRec:
    symbol: str
    direction: str          # 최종 체결 방향("long"/"short") — reverse 모드에선 원신호와 다를 수 있음
    orig_direction: str     # 원신호 방향(narrative 기준, streak 반전 조기청산 판정에 사용)
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float
    quantity: float
    risk_amount: float
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    pnl: float = 0.0
    fees: float = 0.0
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
    streak_th: int = 5
    donchian_period: int = 20
    ema_period: int = 50
    atr_sl_mult: float = 1.3
    atr_trail_mult: float = 2.5
    max_hold_bars: int = 42
    streak_reversal_bars: int = 3     # 조기청산 트리거: 반대방향 스트릭 >= 이 값
    short_mode: str = "streak_down"   # "streak_down"(기본, 대칭가정) | "streak_up_alt"(비대칭 대안)
    mode: str = "gated"       # "gated" | "ungated"(순수 Donchian+EMA, 스트릭게이트 없음) | "reverse"
    fee_on: bool = True       # False 면 무비용(gross) 진단
    starting_equity: float = 10_000.0
    warmup: int | None = None


def _entry_signal(i: int, close: np.ndarray, don_hi: np.ndarray, don_lo: np.ndarray,
                  ema1d: np.ndarray, streak_up: np.ndarray, streak_down: np.ndarray,
                  cfg: RunConfig) -> tuple[bool, bool]:
    """(sig_long, sig_short) 반환. cfg.mode 에 따라 게이트 유무 분기."""
    c = close[i]
    if not (np.isfinite(don_hi[i]) and np.isfinite(don_lo[i]) and np.isfinite(ema1d[i])):
        return False, False
    long_break = c > don_hi[i]
    short_break = c < don_lo[i]
    ema_up = c > ema1d[i]
    ema_dn = c < ema1d[i]

    if cfg.mode == "ungated":
        sig_long = long_break and ema_up
        sig_short = short_break and ema_dn
        return sig_long, sig_short

    su, sd = streak_up[i], streak_down[i]
    gate_long = np.isfinite(su) and su >= cfg.streak_th
    if cfg.short_mode == "streak_up_alt":
        gate_short = np.isfinite(su) and su >= cfg.streak_th
    else:
        gate_short = np.isfinite(sd) and sd >= cfg.streak_th

    sig_long = gate_long and long_break and ema_up
    sig_short = gate_short and short_break and ema_dn
    return sig_long, sig_short


def run_symbol(symbol: str, sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager
               ) -> list[TradeRec]:
    df = sig.df
    n = len(df)
    close = df["close"].to_numpy(float)
    high = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    open_ = df["open"].to_numpy(float)
    atr = sig.atr14.to_numpy(float)
    don_hi, don_lo = sig.don_hi, sig.don_lo
    ema1d = sig.ema1d.to_numpy(float)
    streak_up, streak_down = sig.streak_up, sig.streak_down
    idx = df.index

    warmup = cfg.warmup if cfg.warmup is not None else max(cfg.donchian_period, 60) + 5
    warmup = min(warmup, n - 2)

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    trade: TradeRec | None = None
    run_ext = 0.0   # 러너 트레일링용 최고(롱)/최저(숏) 값
    pending: dict | None = None
    lev = settings.leverage_for(symbol[:-4] + "/USDT")

    for i in range(max(0, warmup), n):
        # 0) 대기 중인 진입 주문 체결 (이번 bar 시가)
        if pending is not None and trade is None:
            sidx = pending["signal_idx"]
            entry_raw = open_[i]
            direction = pending["direction"]
            fill_px = _fill(entry_raw, direction, closing=False, fee_on=cfg.fee_on)
            atr_v = atr[sidx]
            stop_dist = cfg.atr_sl_mult * atr_v
            if stop_dist > 0 and np.isfinite(stop_dist) and fill_px > 0:
                if direction == "long":
                    stop_price = fill_px - stop_dist
                    dirn = Direction.LONG
                else:
                    stop_price = fill_px + stop_dist
                    dirn = Direction.SHORT
                # take_profit 은 없음(트레일링이 익절 역할) — RiskManager 플랜 계산용으로 스톱
                # 반대편에 넓은 명목 TP 를 하나 넣어 build_plan_with_stop 인터페이스만 충족.
                nominal_tp = fill_px + stop_dist * 100 if direction == "long" else fill_px - stop_dist * 100
                plan = risk.build_plan_with_stop(symbol, dirn, fill_px, stop_price, nominal_tp,
                                                 equity, leverage=lev)
                if plan is not None and plan.quantity > 0:
                    fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
                    trade = TradeRec(symbol=symbol, direction=direction,
                                     orig_direction=pending["orig_direction"],
                                     entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                     stop_price=stop_price,
                                     quantity=plan.quantity, risk_amount=plan.risk_amount,
                                     fees=fee0)
                    equity -= fee0
                    run_ext = fill_px
            pending = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            exit_px = None; reason = ""
            # 1a) 스톱(고정SL/트레일링 래칫 통합) 인트라바 체크 — 이전 bar 까지 갱신된 stop 사용
            if trade.direction == "long":
                if l <= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop"
            else:
                if h >= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop"
            # 1b) 스트릭 반전 조기청산(서사 무효화) — 원신호(orig_direction) 기준
            if exit_px is None:
                su_i, sd_i = streak_up[i], streak_down[i]
                if trade.orig_direction == "long" and np.isfinite(sd_i) and sd_i >= cfg.streak_reversal_bars:
                    exit_px, reason = c, "streak_reversal"
                elif trade.orig_direction == "short" and np.isfinite(su_i) and su_i >= cfg.streak_reversal_bars:
                    exit_px, reason = c, "streak_reversal"
            # 1c) 시간청산
            if exit_px is None and (i - trade.entry_idx) >= cfg.max_hold_bars:
                exit_px, reason = c, "time_exit"

            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True, fee_on=cfg.fee_on)
                fee1 = _fee(fill_px * trade.quantity, cfg.fee_on)
                raw = ((fill_px - trade.entry_price) if trade.direction == "long"
                       else (trade.entry_price - fill_px)) * trade.quantity
                pnl = raw - fee1
                trade.exit_idx = i; trade.exit_time = idx[i]; trade.exit_price = fill_px
                trade.pnl = pnl; trade.fees += fee1; trade.reason = reason
                trade.holding_bars = i - trade.entry_idx
                trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
                equity += pnl
                trades.append(trade)
                trade = None
            else:
                # 1d) 트레일링 갱신(다음 bar 부터 반영) — 스톱은 유리한 방향으로만 래칫
                atr_v = atr[i]
                if trade.direction == "long":
                    run_ext = max(run_ext, h)
                    if np.isfinite(atr_v):
                        trail = run_ext - cfg.atr_trail_mult * atr_v
                        trade.stop_price = max(trade.stop_price, trail)
                else:
                    run_ext = min(run_ext, l) if run_ext > 0 else l
                    if np.isfinite(atr_v):
                        trail = run_ext + cfg.atr_trail_mult * atr_v
                        trade.stop_price = min(trade.stop_price, trail)

        # 2) 신규 진입 신호 판정 (이번 bar 종가 기준, 체결은 다음 bar 시가)
        if trade is None and pending is None and i + 1 < n:
            sig_long, sig_short = _entry_signal(i, close, don_hi, don_lo, ema1d,
                                                streak_up, streak_down, cfg)
            if sig_long or sig_short:
                orig_dir = "long" if sig_long else "short"
                exec_dir = orig_dir
                if cfg.mode == "reverse":
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


def run_all(symbols_sig: dict[str, common.Signals], cfg: RunConfig
            ) -> dict[str, list[TradeRec]]:
    settings = get_settings()
    risk = RiskManager(settings)
    out = {}
    for sym, sig in symbols_sig.items():
        out[sym] = run_symbol(sym, sig, cfg, settings, risk)
    return out
