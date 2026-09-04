"""OI 변동성/가격 변동성 비율 극단 페이드 스캘프 — 백테스트 엔진.

신호(1h, z-score) → 15m 진입/청산 매핑:
  - 1h 봉 j 의 종가 시점에 z(j)>=z_th(=2.0) & px_ret_4h_sum(j) 부호로 방향 확정
    (룩어헤드 없음 — z(j) 는 j 시점까지의 데이터만 사용).
  - 체결: 1h 봉 j 의 종가시각 == 다음 시간의 시작 == 15m 그리드에서 그 시각을 연 첫 15m 봉의
    "시가"에 체결(사실상 shift(1) 로 다음 15m 봉에 진입하는 것과 동일한 인과관계, 1h→15m 교차
    타임프레임 매핑).
  - ATR(14,15m) 은 진입 신호 확정 시점(직전 완결 15m 봉)의 값을 사용(entry 봉 자신의 고가/저가는
    아직 모르므로 lookahead 방지).
  - 청산 우선순위(같은 15m 봉 내 동시발생 시 보수적으로 처리):
      1) 봉 시가 시점 z-회귀 확인 청산("직전 완결 1h 봉까지"의 z<=0, causal) — 봉 시가에 청산.
      2) 봉 중 SL 터치(ATR14(15m)×1.2) — SL/TP 동시터치 시 SL 우선.
      3) 봉 중 RR 1.6 고정 목표 터치.
      4) 보유 12봉(15m×12=3h) 경과 시 봉 종가 강제청산.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get("OIVR_REPO_SRC", "/home/user/study/src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE
NS_1H = np.timedelta64(1, "h").astype("timedelta64[ns]").astype("int64")


@dataclass
class TradeRec:
    symbol: str
    direction: str          # "long"/"short"
    dir_mode: str            # "A"(스펙 기본: 4h수익률과 반대로 페이드) | "B"(반전: 4h수익률과 같은 방향 모멘텀)
    trigger_1h_idx: int      # 트리거 1h 봉 인덱스
    entry_idx: int           # 15m 인덱스
    entry_time: pd.Timestamp
    entry_price: float
    fixed_stop: float
    tp_price: float
    quantity: float
    risk_amount: float
    z_at_signal: float
    px_ret_4h_at_signal: float
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
    z_th: float = 2.0
    atr_sl_mult: float = 1.2
    rr_target: float = 1.6
    max_hold_bars: int = 12       # 15m 봉 수 (3시간)
    dir_mode: str = "A"           # "A": 페이드(스펙 기본) | "B": 모멘텀(반전 대조군)
    fee_on: bool = True
    starting_equity: float = 10_000.0
    warmup: int | None = None     # 1h 인덱스 기준 워밍업(None 이면 자동)


def _completed_1h_counts(df1h_index: pd.DatetimeIndex, ts15_ns: np.ndarray) -> np.ndarray:
    """15m 타임스탬프(ns) 각각에 대해 '그 시각까지 완결된 1h 봉 개수'(sleeve_backtester._confirm_slices
    와 동일한 searchsorted 패턴)."""
    ends = df1h_index.asi8 + NS_1H
    return np.searchsorted(ends, ts15_ns, side="right")


def run_symbol(symbol: str, sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager
               ) -> list[TradeRec]:
    df1h = sig.df1h
    df15m = sig.df15m
    n15 = len(df15m)
    n1h = len(df1h)

    z = sig.z
    px4h = sig.px_ret_4h_sum.to_numpy(float)
    atr15 = sig.atr14_15m.to_numpy(float)
    o15 = df15m["open"].to_numpy(float)
    h15 = df15m["high"].to_numpy(float)
    l15 = df15m["low"].to_numpy(float)
    c15 = df15m["close"].to_numpy(float)

    # 15m 각 봉의 '시가 시점까지 완결된 1h 봉 수' — entry 매핑과 z-회귀 청산 판정에 공용.
    counts_open = _completed_1h_counts(df1h.index, df15m.index.asi8)

    # 15m open_time -> iloc 조회용(1h 봉 종가시각과 정확히 일치하는 15m 봉을 찾기 위함)
    ts15_to_iloc = pd.Series(np.arange(n15), index=df15m.index)

    warmup1h = cfg.warmup if cfg.warmup is not None else 150  # vol_window*2+something 여유
    warmup1h = min(warmup1h, n1h - 2)

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    lev = settings.leverage_for(symbol[:-4] + "/USDT")
    next_available_i = -1  # 동시 포지션 금지(항상 flat 일 때만 신규 진입) — 이전 트레이드 청산봉 이후만 허용

    for j in range(max(0, warmup1h), n1h - 1):
        zj = z[j]
        p4 = px4h[j]
        if not (np.isfinite(zj) and np.isfinite(p4)):
            continue
        if not (zj >= cfg.z_th):
            continue
        if p4 == 0:
            continue
        if cfg.dir_mode == "A":
            direction = "long" if p4 < 0 else "short"     # 페이드(스펙 기본)
        else:
            direction = "short" if p4 < 0 else "long"     # 모멘텀(반전 대조군)

        close_ts = df1h.index[j] + pd.Timedelta(hours=1)
        entry_i = ts15_to_iloc.get(close_ts)
        if entry_i is None or entry_i <= 0 or entry_i >= n15 - 1:
            continue  # 15m 데이터 결측(그리드 불일치) — 스킵
        if entry_i <= next_available_i:
            continue  # 이전 트레이드가 아직 보유 중(동시 포지션 금지) — 스킵

        entry_raw = o15[entry_i]
        atr_v = atr15[entry_i - 1]  # 직전 완결 15m 봉까지의 ATR (lookahead 방지)
        if not (np.isfinite(atr_v) and atr_v > 0 and entry_raw > 0):
            continue
        sl_dist = cfg.atr_sl_mult * atr_v
        fill_px = _fill(entry_raw, direction, closing=False, fee_on=cfg.fee_on)
        if direction == "long":
            fixed_stop = fill_px - sl_dist
            tp_price = fill_px + cfg.rr_target * sl_dist
            dirn = Direction.LONG
        else:
            fixed_stop = fill_px + sl_dist
            tp_price = fill_px - cfg.rr_target * sl_dist
            dirn = Direction.SHORT

        plan = risk.build_plan_with_stop(symbol, dirn, fill_px, fixed_stop, tp_price, equity,
                                         leverage=lev)
        if plan is None or plan.quantity <= 0:
            continue

        fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
        trade = TradeRec(symbol=symbol, direction=direction, dir_mode=cfg.dir_mode,
                         trigger_1h_idx=j, entry_idx=entry_i, entry_time=df15m.index[entry_i],
                         entry_price=fill_px, fixed_stop=fixed_stop, tp_price=tp_price,
                         quantity=plan.quantity, risk_amount=plan.risk_amount, z_at_signal=zj,
                         px_ret_4h_at_signal=p4, fees=fee0)
        equity -= fee0

        # ------------------------------------------------ 보유 시뮬레이션(15m)
        is_long = direction == "long"
        exit_i = None; exit_px = None; reason = ""
        i = entry_i
        max_i = min(n15 - 1, entry_i + cfg.max_hold_bars + 2)
        while i <= max_i:
            holding = i - entry_i
            # 1) 봉 시가 시점 z-회귀 확인청산(직전 완결 1h 봉까지의 z, causal)
            if holding >= 1:  # entry 봉 자신은 트리거 z(>=z_th)라 회귀 조건 성립 불가 — 명시적 스킵
                cnt = counts_open[i]
                if cnt >= 1:
                    z_last = z[cnt - 1]
                    if np.isfinite(z_last) and z_last <= 0:
                        exit_i = i; exit_px = o15[i]; reason = "z_reversion"; break
            # 2) 봉 중 SL/TP 터치(entry 봉 포함 — 시가 체결 직후이므로 그 봉의 고가/저가로도
            #    SL/TP 판정 가능, 동시터치 시 SL 우선)
            h, l, c = h15[i], l15[i], c15[i]
            sl_hit = (l <= trade.fixed_stop) if is_long else (h >= trade.fixed_stop)
            tp_hit = (h >= trade.tp_price) if is_long else (l <= trade.tp_price)
            if sl_hit:
                exit_i = i; exit_px = trade.fixed_stop; reason = "stop_loss"; break
            if tp_hit:
                exit_i = i; exit_px = trade.tp_price; reason = "take_profit"; break
            if holding >= cfg.max_hold_bars:
                exit_i = i; exit_px = c; reason = "time_exit"; break
            i += 1
        if exit_i is None:
            # 데이터 끝에 도달(드묾) — 마지막 봉 종가로 강제 청산(회계 정합용, FULL 표본에 포함)
            exit_i = max_i; exit_px = c15[max_i]; reason = "data_end"

        fill_exit = _fill(exit_px, direction, closing=True, fee_on=cfg.fee_on)
        fee1 = _fee(fill_exit * trade.quantity, cfg.fee_on)
        raw = ((fill_exit - trade.entry_price) if is_long
              else (trade.entry_price - fill_exit)) * trade.quantity
        pnl = raw - fee1
        trade.exit_idx = exit_i; trade.exit_time = df15m.index[exit_i]; trade.exit_price = fill_exit
        trade.pnl = pnl; trade.fees += fee1; trade.reason = reason
        trade.holding_bars = exit_i - entry_i
        trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
        equity += pnl
        trades.append(trade)
        next_available_i = exit_i

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
