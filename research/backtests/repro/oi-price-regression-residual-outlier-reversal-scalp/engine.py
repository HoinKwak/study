"""OI-가격 회귀잔차 아웃라이어 반전 스캘프 — 백테스트 엔진.

엔트리: 신호는 bar i 종가 확정 시점에 판정(룩어헤드 없음, z_resid/z_oi 는 window 이내 데이터만 사용해
       bar i 를 포함하되 미래 bar 는 전혀 참조하지 않음) → bar i+1 시가에 체결(shift(1) 진입).
청산: 고정 SL(진입가 ∓ ATR14×atr_sl_mult, 불변) + ATR 트레일링(신고가/신저가 ∓ ATR14×atr_tp_mult,
     "직전 봉까지" 확정된 run_ext 기준으로만 갱신 — 룩어헤드 방지, worker.py 의 실 트레일링 로직과
     동일 관례) 중 더 유리한(타이트한) 쪽이 유효 스톱. 시간청산 24h(time_exit_bars).
     이 스펙의 청산은 순수 가격 기반(ATR)이라 서사/레짐 무효화 조건이 없음 — "반전 대조군 청산이
     원신호 방향을 참조하는 버그" 클래스가 구조적으로 발생할 수 없다(방향에 의존하는 조기청산 분기
     자체가 없음, 부호만 대칭 반전).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "OIRESID_REPO_SRC", str(Path(__file__).resolve().parents[4] / "src")))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE


@dataclass
class TradeRec:
    symbol: str
    direction: str          # 체결 방향("long"/"short")
    signal_source: str      # "resid" | "oi_zscore"
    dir_mode: str            # "A"(z>0->short) | "B"(z>0->long)
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    fixed_stop: float
    quantity: float
    risk_amount: float
    z_at_signal: float
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
    window: int = 60
    z_th: float = 3.0
    price_filter: float = 0.3      # |Δprice%| < 이 값
    atr_tp_mult: float = 2.0       # 트레일링 폭
    atr_sl_mult: float = 1.0       # 고정 SL 폭
    time_exit_bars: int = 24       # 1h 봉 = 24개 = 24시간
    signal_source: str = "resid"   # "resid"(채택안) | "oi_zscore"(핵심 대조군)
    dir_mode: str = "A"            # "A": z>0(OI 과잉증가)->숏 / z<0->롱  (반전 테제)
                                    # "B": 반대(추종 테제)
    fee_on: bool = True
    starting_equity: float = 10_000.0
    warmup: int | None = None


def run_symbol(symbol: str, sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager
               ) -> list[TradeRec]:
    df = sig.df
    n = len(df)
    close = df["close"].to_numpy(float)
    high = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    open_ = df["open"].to_numpy(float)
    atr = sig.atr14.to_numpy(float)
    dprice = sig.d_price_pct.to_numpy(float)
    z = sig.z_resid if cfg.signal_source == "resid" else sig.z_oi
    idx = df.index

    warmup = cfg.warmup if cfg.warmup is not None else (cfg.window * 2 + 20)
    warmup = min(warmup, n - 2)

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    trade: TradeRec | None = None
    run_ext: float | None = None   # 트레일링 기준 극값(직전 봉까지 확정)
    pending: dict | None = None
    lev = settings.leverage_for(symbol[:-4] + "/USDT")

    for i in range(max(0, warmup), n):
        # 0) 대기 중인 진입 체결(이번 bar 시가)
        if pending is not None and trade is None:
            sidx = pending["signal_idx"]
            direction = pending["direction"]
            entry_raw = open_[i]
            fill_px = _fill(entry_raw, direction, closing=False) if cfg.fee_on else entry_raw
            atr_v = atr[sidx]
            sl_dist = cfg.atr_sl_mult * atr_v
            if sl_dist > 0 and np.isfinite(sl_dist) and fill_px > 0:
                if direction == "long":
                    fixed_stop = fill_px - sl_dist
                    dirn = Direction.LONG
                else:
                    fixed_stop = fill_px + sl_dist
                    dirn = Direction.SHORT
                # take_profit 은 트레일링이라 고정값이 없음 — build_plan_with_stop 시그니처상
                # take_profit 인자가 필요하므로 SL 반대편에 아주 먼 값(사실상 미사용)을 채워
                # 리스크(수량) 산정에는 영향 없게 한다(risk_amount 는 entry~fixed_stop 거리만 사용).
                far_tp = fill_px + sl_dist * 100 if direction == "long" else fill_px - sl_dist * 100
                plan = risk.build_plan_with_stop(symbol, dirn, fill_px, fixed_stop, far_tp, equity,
                                                 leverage=lev)
                if plan is not None and plan.quantity > 0:
                    fee0 = _fee(fill_px * plan.quantity) if cfg.fee_on else 0.0
                    trade = TradeRec(symbol=symbol, direction=direction,
                                     signal_source=cfg.signal_source, dir_mode=cfg.dir_mode,
                                     entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                     fixed_stop=fixed_stop, quantity=plan.quantity,
                                     risk_amount=plan.risk_amount, z_at_signal=pending["z"],
                                     fees=fee0)
                    equity -= fee0
                    run_ext = fill_px
            pending = None

        # 1) 보유 중 청산 판정 — 트레일 레벨은 "직전 bar 까지" 확정된 run_ext 기준(룩어헤드 방지)
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            atr_v = atr[i]
            is_long = trade.direction == "long"
            if is_long:
                trail_level = (run_ext - cfg.atr_tp_mult * atr_v) if np.isfinite(atr_v) else -np.inf
                eff_stop = max(trade.fixed_stop, trail_level)
            else:
                trail_level = (run_ext + cfg.atr_tp_mult * atr_v) if np.isfinite(atr_v) else np.inf
                eff_stop = min(trade.fixed_stop, trail_level)

            exit_px = None; reason = ""
            if is_long and l <= eff_stop:
                exit_px, reason = eff_stop, ("stop_loss" if eff_stop <= trade.fixed_stop + 1e-9
                                             else "trailing_stop")
            elif (not is_long) and h >= eff_stop:
                exit_px, reason = eff_stop, ("stop_loss" if eff_stop >= trade.fixed_stop - 1e-9
                                             else "trailing_stop")
            if exit_px is None and (i - trade.entry_idx) >= cfg.time_exit_bars:
                exit_px, reason = c, "time_exit"

            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True) if cfg.fee_on else exit_px
                fee1 = _fee(fill_px * trade.quantity) if cfg.fee_on else 0.0
                raw = ((fill_px - trade.entry_price) if is_long
                       else (trade.entry_price - fill_px)) * trade.quantity
                pnl = raw - fee1
                trade.exit_idx = i; trade.exit_time = idx[i]; trade.exit_price = fill_px
                trade.pnl = pnl; trade.fees += fee1; trade.reason = reason
                trade.holding_bars = i - trade.entry_idx
                trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
                equity += pnl
                trades.append(trade)
                trade = None
                run_ext = None
            else:
                # 청산 안 됐으면 이번 bar 의 h/l 로 run_ext 갱신(다음 bar 트레일 기준)
                run_ext = max(run_ext, h) if is_long else min(run_ext, l)

        # 2) 신규 진입 신호 판정(이번 bar 종가 기준, 체결은 다음 bar 시가)
        if trade is None and pending is None and i + 1 < n:
            zi = z[i]
            dp = dprice[i]
            if np.isfinite(zi) and np.isfinite(dp) and abs(zi) >= cfg.z_th and abs(dp) < cfg.price_filter:
                if cfg.dir_mode == "A":
                    direction = "short" if zi > 0 else "long"
                else:
                    direction = "long" if zi > 0 else "short"
                pending = {"direction": direction, "signal_idx": i, "z": zi}

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
