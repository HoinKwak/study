"""유니버스 OI 명목가치 횡단면 HHI 게이트 + BTC EMA50 추세추종 — 백테스트 엔진.

신호(1d, BTC EMA50 크로스 + HHI 레짐 게이트) → 4h 진입/청산:
  - 1d 봉 t 종가 확정 시점에: close(t) 가 EMA50(t)를 상향/하향 크로스(close(t-1) 대비 부호 전환).
  - 게이트: 크로스 발생일 t 의 **직전 확정일(t-1)** hhi_z 기준으로 판정(스펙 "직전 확정 1d" 명시,
    같은 날 롤링윈도우 자체엔 룩어헤드 없으나 스펙 문구를 그대로 따름 — 보수적).
  - 체결: 크로스 확정일(t) **다음날(t+1) 00:00 UTC 의 첫 4h 봉 시가**에 진입.
  - ATR(4h,14) 은 진입 시점 직전 완결 4h 봉(entry_i-1) 값을 사용(entry 봉 자신은 아직 모름).
  - 청산: SL(고정, ATR×2.0)·트레일(ATR×3.0, 러닝 고가/저가 기준) 중 타이트한 쪽 + hhi_z 역전 조기청산
    (1d 갱신 시점에서만 판정, causal) + max_hold=30일(4h×180봉) 시간청산.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "OIHHI_REPO_SRC", "/home/user/study/.claude/worktrees/agent-a25eed216f42f1e6d/src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE
BARS_PER_DAY_4H = 6


@dataclass
class TradeRec:
    direction: str          # "long"/"short"
    gate: str                # "hhi"(기본) | "none"(게이트없음①) | "btcshare"(대조②) | "reverse"(대조③)
    signal_day_idx: int      # 1d 크로스 확정일 인덱스(t)
    entry_idx: int           # 4h 진입 인덱스
    entry_time: pd.Timestamp
    entry_price: float
    fixed_stop: float
    quantity: float
    risk_amount: float
    hhi_z_at_signal: float
    fees: float = 0.0
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
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
    lo_th: float = common.LO_TH
    hi_th: float = common.HI_TH
    ema_len: int = common.EMA_LEN
    atr_stop_mult: float = common.ATR_STOP_MULT
    atr_trail_mult: float = common.ATR_TRAIL_MULT
    max_hold_days: int = common.MAX_HOLD_DAYS
    gate: str = "hhi"           # hhi|none|btcshare|reverse
    fee_on: bool = True
    starting_equity: float = 10_000.0


def _map_1d_idx_to_4h(df1d_index: pd.DatetimeIndex, df4h: pd.DataFrame) -> np.ndarray:
    """1d 봉 인덱스(그날 00:00 UTC) → 그날 24:00 UTC(=다음날 00:00) 이후 첫 4h 봉의 위치.
    searchsorted(side='left') on 4h index for boundary = day + 1d."""
    boundary = df1d_index + pd.Timedelta(days=1)
    idx4h = df4h.index.to_numpy()
    boundary_np = boundary.to_numpy()
    pos = np.searchsorted(idx4h, boundary_np, side="left")
    return pos


def run_btc(sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager) -> list[TradeRec]:
    symbol = "BTCUSDT"
    df1d = sig.df1d
    df4h = sig.df4h
    n1d = len(df1d)
    n4h = len(df4h)

    close1d = df1d["close"].to_numpy(float)
    ema50 = sig.ema50_1d.to_numpy(float)

    hhi_z = sig.hhi_z.to_numpy(float)
    btc_share_z = sig.btc_oi_share_z.to_numpy(float)

    o4 = df4h["open"].to_numpy(float)
    h4 = df4h["high"].to_numpy(float)
    l4 = df4h["low"].to_numpy(float)
    c4 = df4h["close"].to_numpy(float)
    atr4 = sig.atr14_4h.to_numpy(float)

    entry_pos = _map_1d_idx_to_4h(df1d.index, df4h)  # len n1d, 4h 인덱스 위치(다음날 첫 4h봉)

    # 1d 크로스 이벤트: close(t-1) vs ema(t-1), close(t) vs ema(t) 부호 전환
    prev_above = close1d[:-1] > ema50[:-1]
    curr_above = close1d[1:] > ema50[1:]
    valid = np.isfinite(ema50[:-1]) & np.isfinite(ema50[1:]) & np.isfinite(close1d[:-1]) & np.isfinite(close1d[1:])
    golden = valid & (~prev_above) & curr_above
    death = valid & prev_above & (~curr_above)
    # 인덱스 t (1-based within full array, 즉 golden[k] corresponds to day index k+1)
    golden_days = np.where(golden)[0] + 1
    death_days = np.where(death)[0] + 1

    events = [(t, "long") for t in golden_days] + [(t, "short") for t in death_days]
    events.sort()

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    lev = settings.leverage_for("BTC/USDT")
    next_available_4h = -1

    for t, raw_direction in events:
        if t - 1 < 0:
            continue
        # 게이트 판정: "직전 확정일(t-1)"의 hhi_z 기준
        gate_val_hhi = hhi_z[t - 1]
        gate_val_share = btc_share_z[t - 1]

        if cfg.gate == "hhi":
            if not np.isfinite(gate_val_hhi):
                continue
            ok = (gate_val_hhi <= cfg.lo_th) if raw_direction == "long" else (gate_val_hhi >= cfg.hi_th)
            gate_metric = gate_val_hhi
        elif cfg.gate == "none":
            ok = True
            gate_metric = gate_val_hhi
        elif cfg.gate == "btcshare":
            if not np.isfinite(gate_val_share):
                continue
            ok = (gate_val_share <= cfg.lo_th) if raw_direction == "long" else (gate_val_share >= cfg.hi_th)
            gate_metric = gate_val_share
        elif cfg.gate == "reverse":
            # 방향반전: hhi 게이트가 통과시킨 모집단에서 방향만 뒤집는다(母표본 동일 유지).
            if not np.isfinite(gate_val_hhi):
                continue
            ok = (gate_val_hhi <= cfg.lo_th) if raw_direction == "long" else (gate_val_hhi >= cfg.hi_th)
            gate_metric = gate_val_hhi
        else:
            raise ValueError(cfg.gate)
        if not ok:
            continue

        direction = raw_direction
        if cfg.gate == "reverse":
            direction = "short" if raw_direction == "long" else "long"

        entry_i = int(entry_pos[t])
        if entry_i <= next_available_4h:
            continue  # 동시 포지션 금지(직전 트레이드 미청산)
        if entry_i >= n4h - 1:
            continue

        entry_raw = o4[entry_i]
        atr_v = atr4[entry_i - 1] if entry_i - 1 >= 0 else np.nan
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

        fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
        trade = TradeRec(direction=direction, gate=cfg.gate, signal_day_idx=t, entry_idx=entry_i,
                         entry_time=df4h.index[entry_i], entry_price=fill_px, fixed_stop=fixed_stop,
                         quantity=plan.quantity, risk_amount=plan.risk_amount,
                         hhi_z_at_signal=float(gate_metric) if np.isfinite(gate_metric) else float("nan"),
                         fees=fee0)
        equity -= fee0

        is_long = direction == "long"
        exit_i = None; exit_px = None; reason = ""
        running_extreme = entry_raw
        j = entry_i
        max_hold_bars = cfg.max_hold_days * BARS_PER_DAY_4H
        max_j = min(n4h - 1, entry_i + max_hold_bars + 2)

        while j <= max_j:
            holding = j - entry_i
            prev = j - 1
            atr_prev = atr4[prev] if prev >= 0 else np.nan
            trail_level = np.nan
            if np.isfinite(atr_prev) and atr_prev > 0:
                if is_long:
                    trail_level = running_extreme - cfg.atr_trail_mult * atr_prev
                else:
                    trail_level = running_extreme + cfg.atr_trail_mult * atr_prev

            # hhi_z 역전 조기청산: 4h 봉 j 가 속한 1d 날짜(day_of_j)의 "직전 확정일" hhi_z 로 판정
            # (day_of_j 자신은 아직 미확정일 수 있으므로 day_of_j-1 사용 — causal)
            day_of_j = np.searchsorted(df1d.index.asi8, df4h.index.asi8[j], side="right") - 1
            hhi_reversal = False
            if cfg.gate in ("hhi", "reverse") and day_of_j - 1 >= 0:
                hz = hhi_z[day_of_j - 1]
                if np.isfinite(hz):
                    # raw_direction(게이트 판정 방향) 기준 반대 극단 전환 여부
                    if raw_direction == "long" and hz >= cfg.hi_th:
                        hhi_reversal = True
                    elif raw_direction == "short" and hz <= cfg.lo_th:
                        hhi_reversal = True
            elif cfg.gate == "btcshare" and day_of_j - 1 >= 0:
                hz = btc_share_z[day_of_j - 1]
                if np.isfinite(hz):
                    if raw_direction == "long" and hz >= cfg.hi_th:
                        hhi_reversal = True
                    elif raw_direction == "short" and hz <= cfg.lo_th:
                        hhi_reversal = True

            if is_long:
                levels = [trade.fixed_stop]
                if np.isfinite(trail_level):
                    levels.append(trail_level)
                stop_level = max(levels)
            else:
                levels = [trade.fixed_stop]
                if np.isfinite(trail_level):
                    levels.append(trail_level)
                stop_level = min(levels)

            h, l, cl = h4[j], l4[j], c4[j]
            hit = (l <= stop_level) if is_long else (h >= stop_level)
            if hit:
                exit_i = j; exit_px = stop_level; reason = "stop_combined"; break
            if hhi_reversal:
                exit_i = j; exit_px = cl; reason = "hhi_reversal"; break
            if holding >= max_hold_bars:
                exit_i = j; exit_px = cl; reason = "time_exit"; break

            running_extreme = max(running_extreme, h) if is_long else min(running_extreme, l)
            j += 1
        if exit_i is None:
            exit_i = max_j; exit_px = c4[max_j]; reason = "data_end"

        fill_exit = _fill(exit_px, direction, closing=True, fee_on=cfg.fee_on)
        fee1 = _fee(fill_exit * trade.quantity, cfg.fee_on)
        raw = ((fill_exit - trade.entry_price) if is_long
              else (trade.entry_price - fill_exit)) * trade.quantity
        pnl = raw - fee1
        trade.exit_idx = exit_i; trade.exit_time = df4h.index[exit_i]; trade.exit_price = fill_exit
        trade.pnl = pnl; trade.fees += fee1; trade.reason = reason
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
