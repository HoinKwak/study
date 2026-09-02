"""유니버스 rank_churn 레짐 게이트 + BTC 15m Donchian 브레이크아웃 — 백테스트 엔진.

엔트리: bar i 종가 확정 시점에 판정(레짐은 그 시각까지 알려진 최신 1h 값만 사용, 룩어헤드
없음) → bar i+1 시가에 체결(shift(1) 진입).
청산: SL(신호봉 시가) 인트라바 체크(손절 우선) → ATR 트레일링(신고가/신저가-ATR×mult, 이번봉
갱신 후 다음봉부터 유효) → 레짐 OFF 전환 시 다음봉 시가 청산.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "RANKCHURN_REPO_SRC", str(Path(__file__).resolve().parents[4] / "src")))

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
    orig_direction: str     # 원신호 방향(narrative 기준)
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


def _fill(price: float, direction: str, closing: bool) -> float:
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * SLIPPAGE)


def _fee(notional: float) -> float:
    return abs(notional) * TAKER_FEE


@dataclass
class RunConfig:
    gate_pctile: float = 10.0
    donchian_period: int = 20
    body_atr_mult: float = 1.0
    atr_trail_mult: float = 1.5
    stop_mult: float = 1.0            # SL = 신호봉 시가 기준(라이브 scalp15m과 동일)
    mode: str = "gated"                # "gated" | "ungated"(순수 Donchian) | "reverse"(방향반전)
                                       # | "random_gate"(같은 발화율 랜덤 게이트)
                                       # | "gate_top"(churn 상위 decile 게이트, 게이트 자체 반전)
    fee_on: bool = True
    starting_equity: float = 10_000.0
    seed: int = 0                     # random_gate 시드


def run_btc(sig: common.BtcSignals, gate_aligned: pd.DataFrame, cfg: RunConfig,
           settings, risk: RiskManager) -> list[TradeRec]:
    df = sig.df15
    n = len(df)
    close = df["close"].to_numpy(float)
    high = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    open_ = df["open"].to_numpy(float)
    atr = sig.atr14.to_numpy(float)
    body_ok = (sig.body_frac_atr.to_numpy(float) >= cfg.body_atr_mult)
    don_hi, don_lo = sig.don_hi, sig.don_lo
    idx = df.index
    pctile = gate_aligned["churn_pctile"].reindex(idx).to_numpy(float)

    if cfg.mode == "random_gate":
        # 같은 발화율(gate_pctile 기준 관측 duty cycle)로 무작위 게이트 생성(재현용 seed 고정).
        valid = np.isfinite(pctile)
        duty = float((pctile[valid] <= cfg.gate_pctile).mean()) if valid.any() else 0.0
        rng = np.random.default_rng(cfg.seed)
        gate_on = np.where(valid, rng.random(n) < duty, False)
    elif cfg.mode == "gate_top":
        # 게이트 반전: churn 상위 decile(리더보드가 가장 활발히 재배열되는 구간)일 때만 발화.
        gate_on = np.isfinite(pctile) & (pctile >= (100.0 - cfg.gate_pctile))
    else:
        gate_on = np.isfinite(pctile) & (pctile <= cfg.gate_pctile)

    symbol = common.TRADE_SYMBOL
    lev = settings.leverage_for(symbol[:-4] + "/USDT")
    warmup = 21  # donchian(20)+1 정도만 있으면 충분(레짐 워밍업은 gate_on 자체가 NaN→False 처리)

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    trade: TradeRec | None = None
    running_ext = 0.0     # 트레일링 기준 신고가/신저가(진입 이후)
    pending_entry: dict | None = None
    pending_exit = False  # 레짐 OFF 확정 → 다음봉 시가 청산

    for i in range(warmup, n):
        # 0a) 레짐 OFF 확정 청산(대기중이면 이번 bar 시가 체결)
        if pending_exit and trade is not None:
            exit_raw = open_[i]
            fill_px = _fill(exit_raw, trade.direction, closing=True) if cfg.fee_on else exit_raw
            fee1 = _fee(fill_px * trade.quantity) if cfg.fee_on else 0.0
            raw = ((fill_px - trade.entry_price) if trade.direction == "long"
                   else (trade.entry_price - fill_px)) * trade.quantity
            pnl = raw - fee1
            trade.exit_idx = i; trade.exit_time = idx[i]; trade.exit_price = fill_px
            trade.pnl = pnl; trade.fees += fee1; trade.reason = "gate_off"
            trade.holding_bars = i - trade.entry_idx
            trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
            equity += pnl
            trades.append(trade)
            trade = None
        pending_exit = False

        # 0b) 대기 중인 진입 체결(이번 bar 시가)
        if pending_entry is not None and trade is None:
            sidx = pending_entry["signal_idx"]
            entry_raw = open_[i]
            direction = pending_entry["direction"]
            orig_direction = pending_entry["orig_direction"]
            fill_px = _fill(entry_raw, direction, closing=False) if cfg.fee_on else entry_raw
            sig_open = open_[sidx]
            # SL = 신호봉 시가(라이브 scalp15m과 동일 정의). stop_mult 는 체결가-신호봉시가
            # 거리를 확장하는 배수(기본 1.0 = 신호봉 시가 그대로).
            # ⚠️ 리스크 거리는 반드시 "원신호(orig_direction)" 기준 1회로 계산한다 — 진입 확인봉이
            # 브레이크아웃 방향(원신호 방향)으로 이미 편향돼 있어(예: 롱 브레이크아웃이면
            # fill_px(다음봉 시가) > sig_open 이 구조적으로 성립), reverse 모드에서 실행방향
            # 기준으로 재계산하면 반대부호가 나와 dist 가 1e-9 로 퇴화하는 버그가 생긴다(자체발견,
            # 아래 리포트 §자체발견 버그 참고). 원신호 기준 dist 를 실행방향에 대칭 적용한다.
            if orig_direction == "long":
                dist = max(fill_px - sig_open, 1e-9)
            else:
                dist = max(sig_open - fill_px, 1e-9)
            if direction == "long":
                stop_price = fill_px - cfg.stop_mult * dist
            else:
                stop_price = fill_px + cfg.stop_mult * dist
            dirn = Direction.LONG if direction == "long" else Direction.SHORT
            plan = risk.build_plan_with_stop(symbol, dirn, fill_px, stop_price, fill_px, equity,
                                             leverage=lev)
            if plan is not None and plan.quantity > 0:
                fee0 = _fee(fill_px * plan.quantity) if cfg.fee_on else 0.0
                trade = TradeRec(symbol=symbol, direction=direction,
                                 orig_direction=pending_entry["orig_direction"],
                                 entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                 stop_price=stop_price, quantity=plan.quantity,
                                 risk_amount=plan.risk_amount, fees=fee0)
                equity -= fee0
                running_ext = high[i] if direction == "long" else low[i]
            pending_entry = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l = high[i], low[i]
            exit_px = None; reason = ""
            if trade.direction == "long":
                if l <= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
            else:
                if h >= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
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
            else:
                # 1b) 트레일링 갱신(이번 bar 신고가/신저가 반영, 다음 bar 부터 유효한 스톱)
                atr_v = atr[i]
                if trade.direction == "long":
                    running_ext = max(running_ext, h)
                    if np.isfinite(atr_v) and atr_v > 0:
                        cand = running_ext - cfg.atr_trail_mult * atr_v
                        trade.stop_price = max(trade.stop_price, cand)
                else:
                    running_ext = min(running_ext, l)
                    if np.isfinite(atr_v) and atr_v > 0:
                        cand = running_ext + cfg.atr_trail_mult * atr_v
                        trade.stop_price = min(trade.stop_price, cand)
                # 1c) 레짐 OFF 판정(이번 bar 종가시각 기준 알려진 값) → 다음 bar 시가 청산 예약
                # ungated(순수 Donchian) 대조군은 게이트 개념이 없으므로 이 청산을 적용하지 않음.
                if cfg.mode != "ungated" and not gate_on[i]:
                    pending_exit = True

        # 2) 신규 진입 신호 판정(이번 bar 종가 기준, 체결은 다음 bar 시가)
        if trade is None and pending_entry is None and i + 1 < n and np.isfinite(don_hi[i]):
            c = close[i]
            long_break = c > don_hi[i] and body_ok[i]
            short_break = c < don_lo[i] and body_ok[i]

            if cfg.mode == "ungated":
                sig_long, sig_short = long_break, short_break
            else:  # gated / reverse / random_gate 모두 게이트+브레이크아웃 결합
                sig_long = gate_on[i] and long_break
                sig_short = gate_on[i] and short_break

            if sig_long or sig_short:
                orig_dir = "long" if sig_long else "short"
                exec_dir = orig_dir
                if cfg.mode == "reverse":
                    exec_dir = "short" if orig_dir == "long" else "long"
                pending_entry = {"direction": exec_dir, "orig_direction": orig_dir,
                                 "signal_idx": i}

    return trades


def run_all(sig: common.BtcSignals, gate_aligned: pd.DataFrame, cfg: RunConfig
           ) -> list[TradeRec]:
    settings = get_settings()
    risk = RiskManager(settings)
    return run_btc(sig, gate_aligned, cfg, settings, risk)
