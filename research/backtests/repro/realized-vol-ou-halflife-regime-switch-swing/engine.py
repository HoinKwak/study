"""체결 엔진 — 신호(bar t, 닫힌 데이터) -> bar t+1 시가 진입(shift(1)).

브레이크아웃 모드: ATR(14,4h)×1.8 SL(진입가 대칭) + ATR×2.5 트레일링(래칫) + 20봉 시간청산.
페이드 모드: ATR×1.8 SL(진입가 대칭, 고정) + ATR×1.5 고정 TP(트레일 없음) + dev 0 재돌파(방향
무관 스칼라 조건, 전 봉 종가 확정치 사용 — 룩어헤드 방지) + 20봉 시간청산.

전부 R-배수(risk_distance = ATR_signal_bar × atr_sl(1.8), 1회 계산 후 고정) — 자체발견/자체점검:
진입 수수료가 pnl 에 반영되는지(§엔진 net_R 공식에서 진입+청산 왕복비용을 전부 반영, 두 라운드
연속 진입수수료 누락 버그가 났던 선례 확인용으로 net_R 계산을 명시적으로 여기 남긴다).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from common import ROUND_TRIP_COST


@dataclass
class Trade:
    symbol: str
    mode: str               # "breakout" / "fade"
    signal_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry_price: float
    raw_direction: int      # 원신호 방향(+1/-1)
    trade_dir: int          # 실제 체결 방향(reverse 모드에서 -raw_direction)
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
        # 왕복(진입+청산) 비용을 R-배수 단위로 환산해 gross 에서 차감 — 진입 수수료 반영 확인용.
        cost_R = ROUND_TRIP_COST * self.entry_price / self.risk_distance
        return self.gross_R - cost_R


def simulate_symbol(sym: str, mode: str, price: pd.DataFrame, atr: pd.Series,
                     dev: pd.Series, directions: pd.Series, *,
                     atr_sl: float = 1.8, atr_trail_breakout: float = 2.5,
                     atr_tp_fade: float = 1.5, max_hold_bars: int = 20,
                     reverse: bool = False) -> list[Trade]:
    """directions: 신호봉(t) 인덱스에 값(+1/-1), 그 외 0/NaN. atr,dev,price 는 동일 4h 인덱스."""
    idx = price.index
    n = len(idx)
    pos_of = {t: i for i, t in enumerate(idx)}
    atr_arr = atr.to_numpy(float)
    # dev 는 "직전 확정봉" 값으로 미리 shift(1) 해 전달받는다(호출측 책임) — 룩어헤드 방지.
    dev_arr = dev.to_numpy(float)
    o = price["open"].to_numpy(float)
    h = price["high"].to_numpy(float)
    l = price["low"].to_numpy(float)
    c = price["close"].to_numpy(float)

    sig_times = directions[directions != 0].index
    trades: list[Trade] = []
    last_exit_time = None

    for st in sig_times:
        if st not in pos_of:
            continue
        i = pos_of[st]
        if i + 1 >= n:
            continue
        entry_pos = i + 1
        entry_time = idx[entry_pos]
        if last_exit_time is not None and entry_time <= last_exit_time:
            continue  # 단일 포지션(심볼당), 순차 체결
        raw_direction = int(directions.loc[st])
        trade_dir = -raw_direction if reverse else raw_direction
        atr_entry = float(atr_arr[i])  # 신호봉(t) 자신의 ATR(결정시점 값)
        if not np.isfinite(atr_entry) or atr_entry <= 0:
            continue
        risk_distance = atr_entry * atr_sl
        entry_price = float(o[entry_pos])
        stop = entry_price - risk_distance if trade_dir == 1 else entry_price + risk_distance
        active_stop = stop
        tp_fixed = (entry_price + atr_entry * atr_tp_fade if trade_dir == 1
                    else entry_price - atr_entry * atr_tp_fade)
        running_extreme = h[entry_pos] if trade_dir == 1 else l[entry_pos]

        exit_trade = None
        for k in range(0, max_hold_bars):
            pos = entry_pos + k
            if pos >= n:
                last = n - 1
                exit_trade = Trade(sym, mode, st, entry_time, entry_price, raw_direction,
                                    trade_dir, atr_entry, risk_distance, idx[last],
                                    float(c[last]), "data_end", k)
                break
            ts = idx[pos]
            if k > 0:
                if mode == "fade":
                    # 1) dev 0 재돌파(균형 복귀, 방향무관 스칼라) — 전봉 확정 dev 사용, 이 봉 시가 청산
                    dp = dev_arr[pos - 1]
                    if np.isfinite(dp) and dp <= 0.0:
                        exit_trade = Trade(sym, mode, st, entry_time, entry_price, raw_direction,
                                            trade_dir, atr_entry, risk_distance, ts,
                                            float(o[pos]), "dev_revert", k)
                        break
                    # 2) 고정 SL/TP(트레일 없음) — 보수적으로 SL 먼저 확인
                    if trade_dir == 1:
                        if l[pos] <= stop:
                            exit_trade = Trade(sym, mode, st, entry_time, entry_price,
                                                raw_direction, trade_dir, atr_entry,
                                                risk_distance, ts, stop, "sl", k)
                            break
                        if h[pos] >= tp_fixed:
                            exit_trade = Trade(sym, mode, st, entry_time, entry_price,
                                                raw_direction, trade_dir, atr_entry,
                                                risk_distance, ts, tp_fixed, "tp_fixed", k)
                            break
                    else:
                        if h[pos] >= stop:
                            exit_trade = Trade(sym, mode, st, entry_time, entry_price,
                                                raw_direction, trade_dir, atr_entry,
                                                risk_distance, ts, stop, "sl", k)
                            break
                        if l[pos] <= tp_fixed:
                            exit_trade = Trade(sym, mode, st, entry_time, entry_price,
                                                raw_direction, trade_dir, atr_entry,
                                                risk_distance, ts, tp_fixed, "tp_fixed", k)
                            break
                else:  # breakout: ATR 트레일링(래칫) + SL
                    atr_prev = atr_arr[pos - 1]
                    if trade_dir == 1:
                        trail_stop = running_extreme - atr_trail_breakout * atr_prev
                        active_stop = max(active_stop, trail_stop)
                        if l[pos] <= active_stop:
                            exit_trade = Trade(sym, mode, st, entry_time, entry_price,
                                                raw_direction, trade_dir, atr_entry,
                                                risk_distance, ts, active_stop,
                                                "atr_trail_or_sl", k)
                            break
                    else:
                        trail_stop = running_extreme + atr_trail_breakout * atr_prev
                        active_stop = min(active_stop, trail_stop)
                        if h[pos] >= active_stop:
                            exit_trade = Trade(sym, mode, st, entry_time, entry_price,
                                                raw_direction, trade_dir, atr_entry,
                                                risk_distance, ts, active_stop,
                                                "atr_trail_or_sl", k)
                            break

            if k == max_hold_bars - 1:
                exit_trade = Trade(sym, mode, st, entry_time, entry_price, raw_direction,
                                    trade_dir, atr_entry, risk_distance, ts, float(c[pos]),
                                    "time", k)
                break

            if trade_dir == 1:
                running_extreme = max(running_extreme, h[pos])
            else:
                running_extreme = min(running_extreme, l[pos])

        if exit_trade is not None:
            trades.append(exit_trade)
            last_exit_time = exit_trade.exit_time

    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame(columns=[
            "symbol", "mode", "signal_time", "entry_time", "entry_price", "raw_direction",
            "trade_dir", "atr_entry", "risk_distance", "exit_time", "exit_price",
            "exit_reason", "hold_bars", "gross_R", "net_R"])
    return pd.DataFrame([{
        "symbol": t.symbol, "mode": t.mode, "signal_time": t.signal_time,
        "entry_time": t.entry_time, "entry_price": t.entry_price,
        "raw_direction": t.raw_direction, "trade_dir": t.trade_dir, "atr_entry": t.atr_entry,
        "risk_distance": t.risk_distance, "exit_time": t.exit_time, "exit_price": t.exit_price,
        "exit_reason": t.exit_reason, "hold_bars": t.hold_bars,
        "gross_R": t.gross_R, "net_R": t.net_R,
    } for t in trades])
