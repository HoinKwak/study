"""체결 엔진 — OI CUSUM 체인지포인트(BTC 자체 OI) -> confirm_bars 이내 EMA20/50 방향 확인
-> 다음 4h봉 시가 진입 -> ATR(4h,14) 트레일링(×2.5, 래칫) + 고정 SL(×1.5×ATR진입시, 대칭)
+ 반대 방향 체인지포인트(원시, 원신호 기준) 무효화 + 30봉 시간청산. 전부 R-배수.

direction_map: {"up": 1 또는 -1, "down": 1 또는 -1} — cp_type 별 실제 매매방향(롱=1/숏=-1).
스펙 문언 그대로면 {"up": 1, "down": -1}(추세추종). §1단계 실측(diag_direction.py)에서
하방 체인지포인트 뒤 컨트래리언 롱이 유리하다고 나오면 {"up": 1, "down": 1} 등으로 조정.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from common import ROUND_TRIP_COST
from signals import Signals, build_signals
from events import raw_cp_events, gated_entries


@dataclass
class Trade:
    symbol: str
    cp_time: pd.Timestamp
    cp_type: str
    entry_time: pd.Timestamp
    entry_price: float
    direction: int           # cp_type 로부터 direction_map 으로 배정된 원신호 방향(1=롱,-1=숏)
    trade_dir: int            # 실제 매매 방향(reverse 시 -direction)
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


DEFAULT_DIRECTION_MAP = {"up": 1, "down": -1}  # 스펙 문언 그대로(추세추종)


def simulate_trades(sig: Signals, entries: pd.DataFrame, direction_map: dict,
                     stop_mult: float = 1.5, atr_trail_mult: float = 2.5,
                     max_hold_bars: int = 30, reverse: bool = False,
                     disable_reversal_exit: bool = False,
                     raw_cp: pd.DataFrame | None = None) -> list[Trade]:
    """단일 심볼(BTC), 순차 체결(포지션 보유 중 신규 신호는 무시 — 스윙 저빈도 특성)."""
    if len(entries) == 0:
        return []
    price = sig.df
    atr = sig.atr14
    n = len(price)
    idx = price.index
    close = price["close"].to_numpy()
    high = price["high"].to_numpy()
    low = price["low"].to_numpy()
    openp = price["open"].to_numpy()
    atr_arr = atr.to_numpy()

    if raw_cp is None:
        raw_cp = raw_cp_events(sig)

    trades: list[Trade] = []
    last_exit_time = None
    entries = entries.sort_values("entry_time").reset_index(drop=True)

    for _, e in entries.iterrows():
        entry_time = e["entry_time"]
        if last_exit_time is not None and entry_time <= last_exit_time:
            continue
        entry_bar = int(e["entry_bar"])
        entry_price = float(openp[entry_bar])
        cp_type = e["cp_type"]
        direction = direction_map[cp_type]
        trade_dir = -direction if reverse else direction
        atr_entry = float(e["atr_entry"])
        risk_distance = atr_entry * stop_mult
        if risk_distance <= 0 or not np.isfinite(risk_distance):
            continue

        stop = entry_price - risk_distance if trade_dir == 1 else entry_price + risk_distance

        reversal_time = None
        if not disable_reversal_exit:
            opp_type = "down" if cp_type == "up" else "up"
            opp = raw_cp[(raw_cp["cp_type"] == opp_type) & (raw_cp["cp_time"] > entry_time)]
            if len(opp):
                reversal_time = opp["cp_time"].iloc[0]

        running_extreme = high[entry_bar] if trade_dir == 1 else low[entry_bar]
        active_stop = stop
        exit_trade = None
        for kk in range(1, max_hold_bars + 1):
            pos = entry_bar + kk
            if pos >= n:
                last = n - 1
                exit_trade = Trade(sig.symbol, e["cp_time"], cp_type, entry_time, entry_price,
                                    direction, trade_dir, atr_entry, risk_distance,
                                    idx[last], float(close[last]), "data_end", kk)
                break
            ts = idx[pos]

            if reversal_time is not None and ts == reversal_time:
                exit_trade = Trade(sig.symbol, e["cp_time"], cp_type, entry_time, entry_price,
                                    direction, trade_dir, atr_entry, risk_distance,
                                    ts, float(openp[pos]), "reversal_invalidation", kk)
                break

            atr_prev = float(atr_arr[pos - 1])
            if not np.isfinite(atr_prev) or atr_prev <= 0:
                atr_prev = atr_entry  # 결측 방어(희귀) — 진입시 ATR 로 폴백
            if trade_dir == 1:
                trail_stop = running_extreme - atr_trail_mult * atr_prev
                active_stop = max(active_stop, trail_stop)
                if low[pos] <= active_stop:
                    exit_trade = Trade(sig.symbol, e["cp_time"], cp_type, entry_time, entry_price,
                                        direction, trade_dir, atr_entry, risk_distance,
                                        ts, active_stop, "atr_trail_or_sl", kk)
                    break
            else:
                trail_stop = running_extreme + atr_trail_mult * atr_prev
                active_stop = min(active_stop, trail_stop)
                if high[pos] >= active_stop:
                    exit_trade = Trade(sig.symbol, e["cp_time"], cp_type, entry_time, entry_price,
                                        direction, trade_dir, atr_entry, risk_distance,
                                        ts, active_stop, "atr_trail_or_sl", kk)
                    break

            if kk == max_hold_bars:
                exit_trade = Trade(sig.symbol, e["cp_time"], cp_type, entry_time, entry_price,
                                    direction, trade_dir, atr_entry, risk_distance,
                                    ts, float(close[pos]), "time", kk)
                break

            if trade_dir == 1:
                running_extreme = max(running_extreme, float(high[pos]))
            else:
                running_extreme = min(running_extreme, float(low[pos]))

        if exit_trade is not None:
            trades.append(exit_trade)
            last_exit_time = exit_trade.exit_time

    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame()
    return pd.DataFrame([{
        "symbol": t.symbol, "cp_time": t.cp_time, "cp_type": t.cp_type,
        "entry_time": t.entry_time, "entry_price": t.entry_price,
        "direction": t.direction, "trade_dir": t.trade_dir,
        "atr_entry": t.atr_entry, "risk_distance": t.risk_distance,
        "exit_time": t.exit_time, "exit_price": t.exit_price, "exit_reason": t.exit_reason,
        "hold_bars": t.hold_bars, "gross_R": t.gross_R, "net_R": t.net_R,
    } for t in trades])
