"""ΔOI 왜도 레짐 게이트 + Donchian 추세추종 스윙 — 백테스트 엔진.

엔트리: 신호는 bar i 종가 확정 시점에 판정(룩어헤드 없음) → bar i+1 시가에 체결(shift(1) 진입).
청산: SL/TP 는 인트라바(고저) 체크(손절우선), 시간청산·레짐해소청산은 판정 시점(그 bar 종가)에 체결.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

import os  # noqa: E402
sys.path.insert(0, os.environ.get(
    "OISKEW_REPO_SRC", str(Path(__file__).resolve().parents[4] / "src")))

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
    orig_direction: str     # 원신호 방향(narrative 기준, 레짐해소 청산 판정에 사용)
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float
    take_profit: float
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


def _fill(price: float, direction: str, closing: bool) -> float:
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * SLIPPAGE)


def _fee(notional: float) -> float:
    return abs(notional) * TAKER_FEE


@dataclass
class RunConfig:
    doi_window: int = 60
    pctile_window_days: int = 180
    pctile_hi: float = 70.0
    pctile_lo: float = 30.0
    donchian_period: int = 20
    rr_target: float = 2.5
    atr_sl_mult: float = 2.0
    max_hold_days: int = 5
    mode: str = "gated"       # "gated" | "ungated"(순수 Donchian, 게이트없음 대조군) | "reverse"(방향반전)
    fee_on: bool = True       # False 면 무비용(gross) 진단
    starting_equity: float = 10_000.0
    warmup: int | None = None  # None -> pctile_window_bars + doi_window 사용


def run_symbol(symbol: str, sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager
               ) -> list[TradeRec]:
    df = sig.df
    n = len(df)
    close = df["close"].to_numpy(float)
    high = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    open_ = df["open"].to_numpy(float)
    atr = sig.atr14.to_numpy(float)
    pctile = sig.pctile_skew.to_numpy(float)
    don_hi, don_lo = sig.don_hi, sig.don_lo
    idx = df.index

    max_hold_bars = cfg.max_hold_days * 6   # 4h 봉 = 하루 6개

    pctile_window_bars = cfg.pctile_window_days * 6
    warmup = cfg.warmup if cfg.warmup is not None else (pctile_window_bars + cfg.doi_window + 5)
    warmup = min(warmup, n - 2)

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    trade: TradeRec | None = None
    pending: dict | None = None   # {"direction":..,"orig_direction":..,"signal_idx":i}
    lev = settings.leverage_for(symbol[:-4] + "/USDT")

    for i in range(max(0, warmup), n):
        # 0) 대기 중인 진입 주문 체결 (이번 bar 시가)
        if pending is not None and trade is None:
            sidx = pending["signal_idx"]
            entry_raw = open_[i]
            direction = pending["direction"]
            fill_px = _fill(entry_raw, direction, closing=False) if cfg.fee_on else entry_raw
            atr_v = atr[sidx]
            stop_dist = cfg.atr_sl_mult * atr_v
            if stop_dist > 0 and np.isfinite(stop_dist) and fill_px > 0:
                if direction == "long":
                    stop_price = fill_px - stop_dist
                    tp = fill_px + stop_dist * cfg.rr_target
                    dirn = Direction.LONG
                else:
                    stop_price = fill_px + stop_dist
                    tp = fill_px - stop_dist * cfg.rr_target
                    dirn = Direction.SHORT
                plan = risk.build_plan_with_stop(symbol, dirn, fill_px, stop_price, tp, equity,
                                                 leverage=lev)
                if plan is not None and plan.quantity > 0:
                    fee0 = _fee(fill_px * plan.quantity) if cfg.fee_on else 0.0
                    trade = TradeRec(symbol=symbol, direction=direction,
                                     orig_direction=pending["orig_direction"],
                                     entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                     stop_price=stop_price, take_profit=tp,
                                     quantity=plan.quantity, risk_amount=plan.risk_amount,
                                     fees=fee0)
                    equity -= fee0
            pending = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            exit_px = None; reason = ""
            # 1a) SL/TP 인트라바(손절 우선)
            if trade.direction == "long":
                if l <= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
                elif h >= trade.take_profit:
                    exit_px, reason = trade.take_profit, "take_profit"
            else:
                if h >= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
                elif l <= trade.take_profit:
                    exit_px, reason = trade.take_profit, "take_profit"
            # 1b) 레짐해소(서사무효화) 조기청산 — 원신호(orig_direction) 기준 반대극단 반전
            if exit_px is None and np.isfinite(pctile[i]):
                p = pctile[i]
                if trade.orig_direction == "long" and p <= cfg.pctile_lo:
                    exit_px, reason = c, "regime_invalidation"
                elif trade.orig_direction == "short" and p >= cfg.pctile_hi:
                    exit_px, reason = c, "regime_invalidation"
            # 1c) 시간청산
            if exit_px is None and (i - trade.entry_idx) >= max_hold_bars:
                exit_px, reason = c, "time_exit"
            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True) if cfg.fee_on else exit_px
                fee1 = _fee(fill_px * trade.quantity) if cfg.fee_on else 0.0
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

        # 2) 신규 진입 신호 판정 (이번 bar 종가 기준, 체결은 다음 bar 시가)
        if trade is None and pending is None and i + 1 < n and np.isfinite(don_hi[i]):
            c = close[i]
            long_break = c > don_hi[i]
            short_break = c < don_lo[i]
            p = pctile[i]
            gate_long = np.isfinite(p) and p >= cfg.pctile_hi
            gate_short = np.isfinite(p) and p <= cfg.pctile_lo

            sig_long = sig_short = False
            if cfg.mode == "ungated":
                sig_long, sig_short = long_break, short_break
            else:  # gated / reverse 모두 게이트+브레이크아웃 결합 신호를 트리거로 사용
                sig_long = gate_long and long_break
                sig_short = gate_short and short_break

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
