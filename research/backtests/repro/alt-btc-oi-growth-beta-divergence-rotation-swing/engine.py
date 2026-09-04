"""알트 OI성장률-BTC가격 베타 다이버전스 로테이션 — 백테스트 엔진.

엔트리: 잔차 z-score(4h 그리드에 causal 매핑) + EMA20(4h) 확인, bar i 종가 확정 시점에 판정
       → bar i+1 시가에 체결(shift(1) 진입, 슬리피지 반영).
청산: 고정 SL(진입가 ∓ ATR14(4h)×atr_sl_mult) + 고정 TP(R:R target) + z-reversion(원신호 기준,
     아래 참조) + 시간청산(max_hold_bars) 중 가장 먼저 도달하는 것.
     같은 bar 에 SL/TP 둘 다 닿으면 SL 우선(프레임워크 관례, 보수적).
반전 대조군: 신호 이벤트(타이밍) 는 동일하게 유지하고 체결 방향만 반대로 잡는다(표준 방식).
     SL/TP 는 ATR 기반 스칼라 거리라 진입가 기준 대칭 재배치가 자연스럽게 성립(방향성 극값 참조
     없음 — "반전 대조군 스톱이 방향에 편향된 진입확인봉의 자연스러운 극값을 재사용" 하는 버그
     클래스가 구조적으로 발생할 수 없음). z-reversion 청산은 "서사적 테제 무효화" 조건이라
     (CLAUDE.md 확립 규칙) 최종(반전) 방향이 아니라 **원신호의 z 부호**를 기준으로 판정한다
     — origin_side=="long_raw"(z>=+z_th 로 트리거) 는 항상 "z<=0 이면 무효화", origin_side==
     "short_raw"(z<=-z_th) 는 항상 "z>=0 이면 무효화". 이렇게 하지 않으면(최종 방향 기준 재해석)
     반전 거래가 진입 직후 항상 무효화 조건을 만족하는 퇴화(zero_hold) 가 구조적으로 발생한다
     (z 는 진입 시점에 이미 threshold 를 넘어선 상태이므로).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "ALTOIBETA_REPO_SRC", str(Path(__file__).resolve().parents[4] / "src")))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402


@dataclass
class RunConfig:
    window: int = 60
    ema_period: int = 20
    z_th: float = 2.0
    rr_target: float = 2.0
    atr_sl_mult: float = 2.0
    max_hold_bars: int = 42          # 4h*42 = 1주
    signal_source: str = "resid"     # "resid"(채택안) | "oi_zscore"(베타 무력화 대조군)
    reverse: bool = False            # True 면 신호 이벤트 동일·체결 방향만 반대
    fee_on: bool = True
    taker_fee: float = common.TAKER_FEE
    slippage: float = common.SLIPPAGE
    starting_equity: float = 10_000.0
    warmup: int | None = None        # None 이면 window*7(대략 1d→4h 배율) + ema_period 정도로 자동


@dataclass
class TradeRec:
    symbol: str
    direction: str            # 체결 방향 "long"/"short"
    origin_side: str          # 원신호 부호 "long_raw"(z>=+z_th) | "short_raw"(z<=-z_th)
    signal_source: str
    reverse: bool
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float
    take_profit: float
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


def _fill(price: float, direction: str, slippage: float, closing: bool) -> float:
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * slippage)


def _fee(notional: float, rate: float) -> float:
    return abs(notional) * rate


def run_symbol(symbol: str, bundle: common.Bundle, cfg: RunConfig, settings, risk: RiskManager
              ) -> list[TradeRec]:
    df = bundle.df4h
    n = len(df)
    close = df["close"].to_numpy(float)
    high = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    open_ = df["open"].to_numpy(float)
    atr = bundle.atr14
    ema20 = bundle.ema20
    z = bundle.z_resid if cfg.signal_source == "resid" else bundle.z_oi_raw
    idx = df.index

    warmup = cfg.warmup if cfg.warmup is not None else (cfg.window + cfg.ema_period + 5)
    warmup = min(warmup, n - 2)

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    trade: TradeRec | None = None
    pending: dict | None = None
    lev = settings.leverage_for(symbol[:-4] + "/USDT")

    for i in range(warmup, n):
        # 0) 대기 중인 진입 체결(이번 bar 시가, shift(1))
        if pending is not None and trade is None:
            sidx = pending["signal_idx"]
            direction = pending["direction"]
            entry_raw = open_[i]
            fill_px = (_fill(entry_raw, direction, cfg.slippage, closing=False)
                      if cfg.fee_on else entry_raw)
            atr_v = atr[sidx]
            risk_dist = cfg.atr_sl_mult * atr_v
            if risk_dist > 0 and np.isfinite(risk_dist) and fill_px > 0:
                if direction == "long":
                    stop_price = fill_px - risk_dist
                    take_profit = fill_px + cfg.rr_target * risk_dist
                    dirn = Direction.LONG
                else:
                    stop_price = fill_px + risk_dist
                    take_profit = fill_px - cfg.rr_target * risk_dist
                    dirn = Direction.SHORT
                plan = risk.build_plan_with_stop(symbol, dirn, fill_px, stop_price, take_profit,
                                                 equity, leverage=lev)
                if plan is not None and plan.quantity > 0:
                    fee0 = _fee(fill_px * plan.quantity, cfg.taker_fee) if cfg.fee_on else 0.0
                    trade = TradeRec(symbol=symbol, direction=direction,
                                     origin_side=pending["origin_side"],
                                     signal_source=cfg.signal_source, reverse=cfg.reverse,
                                     entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                     stop_price=stop_price, take_profit=take_profit,
                                     quantity=plan.quantity, risk_amount=plan.risk_amount,
                                     z_at_signal=pending["z"], fees=fee0)
                    equity -= fee0
            pending = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            is_long = trade.direction == "long"
            exit_px = None
            reason = ""
            # 1a) 인트라바 SL/TP (같은 bar 둘 다 닿으면 SL 우선)
            if is_long:
                if l <= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
                elif h >= trade.take_profit:
                    exit_px, reason = trade.take_profit, "take_profit"
            else:
                if h >= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
                elif l <= trade.take_profit:
                    exit_px, reason = trade.take_profit, "take_profit"
            # 1b) z-reversion(원신호 기준) — bar 종가 확정 시점 값 사용
            if exit_px is None:
                zi = z[i]
                if np.isfinite(zi):
                    if trade.origin_side == "long_raw" and zi <= 0.0:
                        exit_px, reason = c, "z_reversion"
                    elif trade.origin_side == "short_raw" and zi >= 0.0:
                        exit_px, reason = c, "z_reversion"
            # 1c) 시간청산
            if exit_px is None and (i - trade.entry_idx) >= cfg.max_hold_bars:
                exit_px, reason = c, "time_exit"

            if exit_px is not None:
                fill_px = (_fill(exit_px, trade.direction, cfg.slippage, closing=True)
                          if cfg.fee_on else exit_px)
                fee1 = _fee(fill_px * trade.quantity, cfg.taker_fee) if cfg.fee_on else 0.0
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

        # 2) 신규 진입 신호 판정(이번 bar 종가 기준, 체결은 다음 bar 시가)
        if trade is None and pending is None and i + 1 < n:
            zi = z[i]
            if np.isfinite(zi) and np.isfinite(ema20[i]):
                long_raw = zi >= cfg.z_th and close[i] > ema20[i]
                short_raw = zi <= -cfg.z_th and close[i] < ema20[i]
                if long_raw or short_raw:
                    origin_side = "long_raw" if long_raw else "short_raw"
                    raw_dir = "long" if long_raw else "short"
                    exec_dir = raw_dir if not cfg.reverse else (
                        "short" if raw_dir == "long" else "long")
                    pending = {"direction": exec_dir, "signal_idx": i, "z": zi,
                              "origin_side": origin_side}

    return trades


def load_all_bundles(symbols=common.ALT_SYMBOLS, **kw) -> dict[str, common.Bundle]:
    out = {}
    for s in symbols:
        b = common.build_bundle(s, **kw)
        if b is not None:
            out[s] = b
    return out


def run_all(bundles: dict[str, common.Bundle], cfg: RunConfig) -> dict[str, list[TradeRec]]:
    settings = get_settings()
    risk = RiskManager(settings)
    out = {}
    for sym, b in bundles.items():
        out[sym] = run_symbol(sym, b, cfg, settings, risk)
    return out
