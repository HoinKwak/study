"""체결 엔진 — 신호(bar i, 닫힌 데이터) -> bar i+1 시가 진입(shift(1)) -> ATR 트레일링(2.5)
+ 고정 SL(1.3×ATR, 진입가 대칭) + apen_pctile>=85(레짐붕괴, 방향무관 스칼라조건) 즉시청산
+ 최대 30봉(4h) 시간청산. 전부 R-배수(risk_distance = ATR_signal_bar × stop_mult, 1회 계산).

⚠️레짐붕괴 청산은 방향 변수를 전혀 참조하지 않는 스칼라 조건(apen_pctile>=85 여부만 봄)이라
반전 대조군에서도 뒤집을 대상이 없다 — GK/RS 스윙 백테스트 선례와 동일 구조(방향 미참조
분기는 반전모드에서도 퇴화가 구조적으로 불가능).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from common import ROUND_TRIP_COST
from events import build_universe, detect_signals


@dataclass
class Trade:
    symbol: str
    signal_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry_price: float
    direction: int
    trade_dir: int
    atr_entry: float
    risk_distance: float
    exit_time: pd.Timestamp
    exit_price: float
    exit_reason: str
    hold_bars: int
    gross_R: float = field(init=False)

    def __post_init__(self):
        self.gross_R = (self.exit_price - self.entry_price) / self.risk_distance * self.trade_dir

    @property
    def net_R(self) -> float:
        cost_R = ROUND_TRIP_COST * self.entry_price / self.risk_distance
        return self.gross_R - cost_R


def simulate_symbol(sym: str, price: pd.DataFrame, atr: pd.Series, breakdown: pd.Series,
                    signals: pd.DataFrame, stop_mult: float = 1.3, atr_trail_mult: float = 2.5,
                    max_hold_bars: int = 30, reverse: bool = False,
                    disable_breakdown_exit: bool = False) -> list[Trade]:
    if len(signals) == 0:
        return []
    idx = price.index
    n = len(idx)
    pos_of = {t: i for i, t in enumerate(idx)}  # O(1) lookup(4h 그리드라 크지 않음)
    breakdown_arr = breakdown.reindex(idx).to_numpy()
    atr_arr = atr.to_numpy()

    trades: list[Trade] = []
    last_exit_time = None
    signals = signals.sort_values("signal_time").reset_index(drop=True)

    for _, sig in signals.iterrows():
        st = sig["signal_time"]
        if st not in pos_of:
            continue
        i = pos_of[st]
        if i + 1 >= n:
            continue
        entry_pos = i + 1
        entry_time = idx[entry_pos]
        if last_exit_time is not None and entry_time <= last_exit_time:
            continue  # 포지션 보유 중이면 스킵(순차 체결, 스윙 저빈도 특성)
        entry_price = float(price["open"].iloc[entry_pos])
        direction = int(sig["direction"])
        trade_dir = -direction if reverse else direction
        atr_entry = float(sig["atr_entry"])
        risk_distance = atr_entry * stop_mult
        if risk_distance <= 0 or not np.isfinite(risk_distance):
            continue
        stop = entry_price - risk_distance if trade_dir == 1 else entry_price + risk_distance
        active_stop = stop
        running_extreme = float(price["high"].iloc[entry_pos]) if trade_dir == 1 else float(
            price["low"].iloc[entry_pos])

        exit_trade = None
        for k in range(0, max_hold_bars):
            pos = entry_pos + k
            if pos >= n:
                last = n - 1
                exit_trade = Trade(sym, st, entry_time, entry_price, direction, trade_dir,
                                    atr_entry, risk_distance, idx[last],
                                    float(price["close"].iloc[last]), "data_end", k)
                break
            ts = idx[pos]
            bar = price.iloc[pos]

            # 1) 레짐붕괴(apen_pctile>=85, 방향무관 스칼라) — 이 봉 시가에 즉시 청산
            #    (진입 당일 봉(k=0)에는 미적용 — 진입 자체가 gate_active 확인 후이므로 자기당착 방지)
            if k > 0 and not disable_breakdown_exit and bool(breakdown_arr[pos]):
                exit_trade = Trade(sym, st, entry_time, entry_price, direction, trade_dir,
                                    atr_entry, risk_distance, ts, float(bar["open"]),
                                    "regime_breakdown", k)
                break

            # 2) ATR 트레일링 + 고정 SL(래칫)
            if k > 0:
                atr_prev = float(atr_arr[pos - 1])
                if trade_dir == 1:
                    trail_stop = running_extreme - atr_trail_mult * atr_prev
                    active_stop = max(active_stop, trail_stop)
                    if bar["low"] <= active_stop:
                        exit_trade = Trade(sym, st, entry_time, entry_price, direction, trade_dir,
                                            atr_entry, risk_distance, ts, active_stop,
                                            "atr_trail_or_sl", k)
                        break
                else:
                    trail_stop = running_extreme + atr_trail_mult * atr_prev
                    active_stop = min(active_stop, trail_stop)
                    if bar["high"] >= active_stop:
                        exit_trade = Trade(sym, st, entry_time, entry_price, direction, trade_dir,
                                            atr_entry, risk_distance, ts, active_stop,
                                            "atr_trail_or_sl", k)
                        break

            # 3) 시간청산
            if k == max_hold_bars - 1:
                exit_trade = Trade(sym, st, entry_time, entry_price, direction, trade_dir,
                                    atr_entry, risk_distance, ts, float(bar["close"]), "time", k)
                break

            if trade_dir == 1:
                running_extreme = max(running_extreme, float(bar["high"]))
            else:
                running_extreme = min(running_extreme, float(bar["low"]))

        if exit_trade is not None:
            trades.append(exit_trade)
            last_exit_time = exit_trade.exit_time

    return trades


def run_variant(uni: dict, pullback_lookback: int = 5, stop_mult: float = 1.3,
                atr_trail_mult: float = 2.5, max_hold_bars: int = 30, reverse: bool = False,
                disable_breakdown_exit: bool = False, no_gate: bool = False,
                gate_override: dict | None = None) -> list[Trade]:
    """no_gate=True 면 게이트 없이 순수 EMA20/50+눌림목만으로 신호(사전폐기조건 (e) 대조군).
    gate_override: {symbol: bool Series} — 대조군 게이트(예: ADX 게이트)로 통째로 교체."""
    trades: list[Trade] = []
    for sym, frame in uni["universe"].items():
        f = dict(frame)
        if no_gate:
            f["gate_active"] = pd.Series(True, index=f["price"].index)
        elif gate_override is not None:
            f["gate_active"] = gate_override[sym].reindex(f["price"].index).fillna(False)
        signals = detect_signals(f, pullback_lookback=pullback_lookback)
        tr = simulate_symbol(sym, f["price"], f["atr"], f["regime_breakdown"], signals,
                             stop_mult=stop_mult, atr_trail_mult=atr_trail_mult,
                             max_hold_bars=max_hold_bars, reverse=reverse,
                             disable_breakdown_exit=disable_breakdown_exit)
        trades.extend(tr)
    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame()
    return pd.DataFrame([{
        "symbol": t.symbol, "signal_time": t.signal_time, "entry_time": t.entry_time,
        "entry_price": t.entry_price, "direction": t.direction, "trade_dir": t.trade_dir,
        "atr_entry": t.atr_entry, "risk_distance": t.risk_distance, "exit_time": t.exit_time,
        "exit_price": t.exit_price, "exit_reason": t.exit_reason, "hold_bars": t.hold_bars,
        "gross_R": t.gross_R, "net_R": t.net_R,
    } for t in trades])
