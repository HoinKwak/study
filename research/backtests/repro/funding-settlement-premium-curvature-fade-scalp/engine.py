"""체결 엔진 — 정산이벤트(c_z 극단) -> 진입(정산시각 15m봉 시가, shift(1) 원칙) ->
청산(ATR SL / 1.3R TP / 프리미엄 체크포인트수준 복귀 / 8봉 시간청산). 전부 R-배수 산출.

방향반전(reverse) 대조군: risk_distance 는 원신호 기준 1회 계산해 대칭 재배치(SL/TP 가격
기준 청산은 trade_dir 로 뒤집힘). 단 '프리미엄 체크포인트 수준 복귀' 청산은 서사적(narrative)
청산으로 trade.direction 이 아니라 진입 시점에 1회 캡처한 객관적 시장사실
(entry_side_sign = sign(premium_at_entry - checkpoint_premium))을 기준으로 판정한다
(CLAUDE.md 축적 규칙 — AVWAP재접촉 건 선례와 동일 처리, SL 은 표준 대칭 재배치와 별개).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from common import ROUND_TRIP_COST, SYMBOLS, atr14_15m, load_symbol
from events import build_events


@dataclass
class Trade:
    symbol: str
    t0: pd.Timestamp
    checkpoint_time: pd.Timestamp
    settlement_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry_price: float
    direction: int          # 1=long, -1=short (원신호 방향, reverse 여부와 무관)
    trade_dir: int           # 실제 매매 방향(reverse 시 -direction)
    atr_entry: float
    risk_distance: float
    c: float
    c_z: float
    checkpoint_premium: float
    premium_at_entry: float
    exit_time: pd.Timestamp
    exit_price: float
    exit_reason: str
    hold_bars: int
    gross_R: float = field(init=False)

    def __post_init__(self):
        raw = (self.exit_price - self.entry_price) / self.risk_distance * self.trade_dir
        self.gross_R = raw

    @property
    def net_R(self) -> float:
        cost_R = ROUND_TRIP_COST * self.entry_price / self.risk_distance
        return self.gross_R - cost_R


def build_frame(symbol: str, anchor_offset_hours: int = 0, check_offset_min: int = 60,
                window_min: int = 480, lookback: int = 60) -> dict:
    data = load_symbol(symbol)
    prem_1m = data["prem_1m"]["close"]
    price_15m = data["price_15m"]
    atr = atr14_15m(price_15m)
    # 15m 그리드에 정렬된 프리미엄 종가(그 15m 구간 내 마지막 1분 종가, causal — 미래 미포함)
    premium_15m = prem_1m.resample("15min", label="left", closed="left").last()
    events = build_events(prem_1m, anchor_offset_hours=anchor_offset_hours,
                           check_offset_min=check_offset_min, window_min=window_min,
                           lookback=lookback)
    return {"symbol": symbol, "price_15m": price_15m, "atr": atr,
            "premium_15m": premium_15m, "prem_1m": prem_1m, "events": events}


def find_signals(frame: dict, z_threshold: float = 2.0) -> pd.DataFrame:
    ev = frame["events"]
    ev = ev[ev["c_z"].notna()].copy()
    ev["direction"] = 0
    ev.loc[ev["c_z"] >= z_threshold, "direction"] = -1   # 과열 롱쏠림 -> 숏 페이드
    ev.loc[ev["c_z"] <= -z_threshold, "direction"] = 1   # 과열 숏쏠림 -> 롱 페이드
    return ev[ev["direction"] != 0].reset_index(drop=True)


def simulate_trade(frame: dict, row: pd.Series, atr_sl_mult: float, tp_r_mult: float,
                    max_hold_bars: int, reverse: bool = False) -> Trade | None:
    price = frame["price_15m"]
    atr = frame["atr"]
    premium_15m = frame["premium_15m"]
    prem_1m = frame["prem_1m"]

    settlement_time = row["settlement_time"]
    if settlement_time not in price.index:
        return None
    epos = price.index.get_loc(settlement_time)
    entry_time = settlement_time
    entry_price = float(price["open"].iloc[epos])

    # ATR: 진입 직전 완결봉(entry_time - 15min) 값 사용(causal, 미래 미포함)
    prev_pos = epos - 1
    if prev_pos < 0:
        return None
    atr_entry = float(atr.iloc[prev_pos])
    if not np.isfinite(atr_entry) or atr_entry <= 0:
        return None

    direction = int(row["direction"])
    trade_dir = -direction if reverse else direction
    risk_distance = atr_entry * atr_sl_mult   # 원신호 기준 1회 계산(반전 시에도 재사용)
    if risk_distance <= 0:
        return None

    if trade_dir == 1:
        stop = entry_price - risk_distance
        tp_r = entry_price + tp_r_mult * risk_distance
    else:
        stop = entry_price + risk_distance
        tp_r = entry_price - tp_r_mult * risk_distance

    checkpoint_premium = float(row["checkpoint_premium"])
    premium_at_entry = prem_1m.get(entry_time, np.nan)
    if pd.isna(premium_at_entry):
        return None
    entry_side_sign = float(np.sign(premium_at_entry - checkpoint_premium))

    n = len(price)
    for k in range(1, max_hold_bars + 1):
        pos = epos + k
        if pos >= n:
            last = n - 1
            return Trade(frame["symbol"], row["t0"], row["checkpoint_time"], settlement_time,
                         entry_time, entry_price, direction, trade_dir, atr_entry, risk_distance,
                         float(row["c"]), float(row["c_z"]), checkpoint_premium,
                         premium_at_entry, price.index[last], float(price["close"].iloc[last]),
                         "data_end", k)
        bar = price.iloc[pos]
        ts = price.index[pos]

        # 1) SL 인트라바 우선
        if trade_dir == 1:
            if bar["low"] <= stop:
                return Trade(frame["symbol"], row["t0"], row["checkpoint_time"], settlement_time,
                             entry_time, entry_price, direction, trade_dir, atr_entry,
                             risk_distance, float(row["c"]), float(row["c_z"]),
                             checkpoint_premium, premium_at_entry, ts, stop, "stop_loss", k)
        else:
            if bar["high"] >= stop:
                return Trade(frame["symbol"], row["t0"], row["checkpoint_time"], settlement_time,
                             entry_time, entry_price, direction, trade_dir, atr_entry,
                             risk_distance, float(row["c"]), float(row["c_z"]),
                             checkpoint_premium, premium_at_entry, ts, stop, "stop_loss", k)

        # 2) 1.3R 인트라바 익절
        if trade_dir == 1:
            if bar["high"] >= tp_r:
                return Trade(frame["symbol"], row["t0"], row["checkpoint_time"], settlement_time,
                             entry_time, entry_price, direction, trade_dir, atr_entry,
                             risk_distance, float(row["c"]), float(row["c_z"]),
                             checkpoint_premium, premium_at_entry, ts, tp_r, "take_profit_r", k)
        else:
            if bar["low"] <= tp_r:
                return Trade(frame["symbol"], row["t0"], row["checkpoint_time"], settlement_time,
                             entry_time, entry_price, direction, trade_dir, atr_entry,
                             risk_distance, float(row["c"]), float(row["c_z"]),
                             checkpoint_premium, premium_at_entry, ts, tp_r, "take_profit_r", k)

        # 3) 프리미엄 체크포인트수준 복귀 익절(bar 종가 기준, 서사적 청산 — entry_side_sign 기준)
        pnow = premium_15m.get(ts, np.nan)
        if pd.notna(pnow) and entry_side_sign != 0:
            reverted = ((entry_side_sign > 0 and pnow <= checkpoint_premium)
                        or (entry_side_sign < 0 and pnow >= checkpoint_premium))
            if reverted:
                return Trade(frame["symbol"], row["t0"], row["checkpoint_time"], settlement_time,
                             entry_time, entry_price, direction, trade_dir, atr_entry,
                             risk_distance, float(row["c"]), float(row["c_z"]),
                             checkpoint_premium, premium_at_entry, ts, float(bar["close"]),
                             "premium_reversion", k)

        # 4) 시간청산
        if k == max_hold_bars:
            return Trade(frame["symbol"], row["t0"], row["checkpoint_time"], settlement_time,
                         entry_time, entry_price, direction, trade_dir, atr_entry, risk_distance,
                         float(row["c"]), float(row["c_z"]), checkpoint_premium,
                         premium_at_entry, ts, float(bar["close"]), "time", k)
    return None


def load_all(anchor_offset_hours: int = 0, check_offset_min: int = 60,
             window_min: int = 480, lookback: int = 60) -> dict:
    out = {}
    for sym in SYMBOLS:
        out[sym] = build_frame(sym, anchor_offset_hours=anchor_offset_hours,
                               check_offset_min=check_offset_min, window_min=window_min,
                               lookback=lookback)
    return out


def run_variant(universe: dict, z_threshold: float = 2.0, atr_sl_mult: float = 1.0,
                tp_r_mult: float = 1.3, max_hold_bars: int = 8,
                reverse: bool = False) -> list[Trade]:
    trades = []
    for sym, frame in universe.items():
        signals = find_signals(frame, z_threshold=z_threshold)
        for _, row in signals.iterrows():
            tr = simulate_trade(frame, row, atr_sl_mult, tp_r_mult, max_hold_bars,
                                reverse=reverse)
            if tr is not None:
                trades.append(tr)
    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame()
    return pd.DataFrame([{
        "symbol": t.symbol, "t0": t.t0, "checkpoint_time": t.checkpoint_time,
        "settlement_time": t.settlement_time, "entry_time": t.entry_time,
        "entry_price": t.entry_price, "direction": t.direction, "trade_dir": t.trade_dir,
        "atr_entry": t.atr_entry, "risk_distance": t.risk_distance, "c": t.c, "c_z": t.c_z,
        "checkpoint_premium": t.checkpoint_premium, "premium_at_entry": t.premium_at_entry,
        "exit_time": t.exit_time, "exit_price": t.exit_price, "exit_reason": t.exit_reason,
        "hold_bars": t.hold_bars, "gross_R": t.gross_R, "net_R": t.net_R,
    } for t in trades])
