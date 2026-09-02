"""BTC 웍 리젝션 + 알트 브레드스 확인 — 신호/체결 엔진.

신호(BTC 15m 웍 리젝션 + 같은 15m 봉에서 알트 6종목 중 confirm_n_th개 이상 동일방향 확인) ->
진입(다음 15m 봉 시가, shift(1)) -> 청산(스윙10봉/RR target TP, 웍극값+buffer SL, 8봉 시간청산).
전부 R-배수로 산출(gross/net 병기).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from common import (ALTS, BTC, CLOSE_LOC_TH, CONFIRM_N_TH, MAX_HOLD, ROUND_TRIP_COST,
                     RR_TARGET, SL_BUFFER, SWING_LOOKBACK, WICK_ATR_MULT, WICK_BODY_MULT,
                     load_all, wick_signals)


@dataclass
class Trade:
    signal_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry_price: float
    raw_direction: int      # 원신호 방향(웍의 자연스러운 페이드 방향): +1=롱(하단웍) -1=숏(상단웍)
    trade_direction: int    # 실제 체결 방향(반전판은 -raw_direction)
    atr_entry: float
    risk_distance: float    # 원신호 기준 1회 계산(반전시에도 동일 크기 재사용)
    confirm_n: int
    exit_time: pd.Timestamp
    exit_price: float
    exit_reason: str
    hold_bars: int
    gross_R: float = field(init=False)

    def __post_init__(self):
        self.gross_R = (self.exit_price - self.entry_price) / self.risk_distance * self.trade_direction

    @property
    def net_R(self) -> float:
        cost_R = ROUND_TRIP_COST * self.entry_price / self.risk_distance
        return self.gross_R - cost_R


def build_universe(wick_body_mult: float = WICK_BODY_MULT, wick_atr_mult: float = WICK_ATR_MULT,
                    close_loc_th: float = CLOSE_LOC_TH) -> dict:
    """전체 종목 로드 + (파라미터 스윕용) 웍 신호 재계산."""
    raw = load_all()  # 기본 파라미터로 이미 계산됨
    if (wick_body_mult, wick_atr_mult, close_loc_th) != (WICK_BODY_MULT, WICK_ATR_MULT, CLOSE_LOC_TH):
        out = {}
        for sym, feat in raw.items():
            out[sym] = wick_signals(feat, wick_body_mult, wick_atr_mult, close_loc_th)
        return out
    return raw


def build_confirm_frame(universe: dict) -> pd.DataFrame:
    """BTC 인덱스 기준으로 알트들의 is_upper/is_lower 를 정렬해 confirm_n_upper/lower 계산.

    정렬은 인과적으로 문제없음(같은 15m 봉이 모든 종목 동시 마감, `pandas.join` inner 정렬만 사용
    — 미래 시점 참조 없음). 교집합 인덱스만 사용(결측 종목-시점은 트레이드 생성 대상에서 제외).
    """
    btc = universe[BTC][["open", "high", "low", "close", "atr", "is_upper", "is_lower"]].copy()
    btc.columns = ["open", "high", "low", "close", "atr", "btc_upper", "btc_lower"]

    idx = btc.index
    for alt in ALTS:
        idx = idx.intersection(universe[alt].index)

    frame = btc.loc[idx].copy()
    upper_cnt = pd.Series(0, index=idx)
    lower_cnt = pd.Series(0, index=idx)
    for alt in ALTS:
        a = universe[alt].loc[idx]
        upper_cnt = upper_cnt.add(a["is_upper"].astype(int), fill_value=0)
        lower_cnt = lower_cnt.add(a["is_lower"].astype(int), fill_value=0)
    frame["confirm_n_upper"] = upper_cnt
    frame["confirm_n_lower"] = lower_cnt
    return frame


def find_signals(frame: pd.DataFrame, confirm_n_th: int | None = CONFIRM_N_TH
                  ) -> list[tuple[pd.Timestamp, int, int]]:
    """(signal_time, raw_direction, confirm_n) 리스트.

    confirm_n_th=None 이면 브레드스 게이트 완전 제거(BTC 단독판 대조군①).
    raw_direction: +1=롱(하단 웍, 강세) / -1=숏(상단 웍, 약세).
    """
    out = []
    bu = frame["btc_upper"].to_numpy()
    bl = frame["btc_lower"].to_numpy()
    cu = frame["confirm_n_upper"].to_numpy()
    cl = frame["confirm_n_lower"].to_numpy()
    idx = frame.index
    for i in range(len(frame)):
        if bu[i] and (confirm_n_th is None or cu[i] >= confirm_n_th):
            out.append((idx[i], -1, int(cu[i])))
        elif bl[i] and (confirm_n_th is None or cl[i] >= confirm_n_th):
            out.append((idx[i], 1, int(cl[i])))
    return out


def find_signals_random_subset(frame: pd.DataFrame, universe: dict, subset_size: int,
                                confirm_n_th: int, idx: pd.Index, rng: np.random.Generator
                                ) -> list[tuple[pd.Timestamp, int, int]]:
    """대조군③: 6개 알트 중 무작위 subset_size개만으로 confirm_n 재계산."""
    chosen = rng.choice(ALTS, size=subset_size, replace=False)
    upper_cnt = pd.Series(0, index=idx)
    lower_cnt = pd.Series(0, index=idx)
    for alt in chosen:
        a = universe[alt].loc[idx]
        upper_cnt = upper_cnt.add(a["is_upper"].astype(int), fill_value=0)
        lower_cnt = lower_cnt.add(a["is_lower"].astype(int), fill_value=0)
    out = []
    bu = frame["btc_upper"].to_numpy()
    bl = frame["btc_lower"].to_numpy()
    cu = upper_cnt.to_numpy()
    cl = lower_cnt.to_numpy()
    for i in range(len(frame)):
        if bu[i] and cu[i] >= confirm_n_th:
            out.append((idx[i], -1, int(cu[i])))
        elif bl[i] and cl[i] >= confirm_n_th:
            out.append((idx[i], 1, int(cl[i])))
    return out


def simulate_trade(frame: pd.DataFrame, signal_time: pd.Timestamp, raw_direction: int,
                    confirm_n: int, reverse: bool = False,
                    rr_target: float = RR_TARGET, sl_buffer: float = SL_BUFFER,
                    max_hold: int = MAX_HOLD, swing_lookback: int = SWING_LOOKBACK
                    ) -> Trade | None:
    if signal_time not in frame.index:
        return None
    spos = frame.index.get_loc(signal_time)
    epos = spos + 1
    if epos >= len(frame):
        return None

    atr_entry = frame["atr"].iloc[spos]
    if pd.isna(atr_entry) or atr_entry <= 0:
        return None

    entry_time = frame.index[epos]
    entry_price = float(frame["open"].iloc[epos])

    # 리스크 거리: 원신호(raw_direction) 기준 1회 계산 — 반전판에서도 동일 크기 재사용(대칭 재배치).
    sig_high = float(frame["high"].iloc[spos])
    sig_low = float(frame["low"].iloc[spos])
    if raw_direction == -1:   # 상단 웍(약세) -> 원신호 숏, 원신호 SL = 신호봉 고가 + buffer*ATR
        raw_stop = sig_high + sl_buffer * atr_entry
        risk_distance = raw_stop - entry_price
    else:                      # 하단 웍(강세) -> 원신호 롱, 원신호 SL = 신호봉 저가 - buffer*ATR
        raw_stop = sig_low - sl_buffer * atr_entry
        risk_distance = entry_price - raw_stop
    if risk_distance <= 0:
        return None

    trade_dir = -raw_direction if reverse else raw_direction
    stop_price = entry_price - trade_dir * risk_distance

    # 스윙 타깃(직전 10봉, 신호봉 포함 — 시점상 전부 확정된 정보)
    win_start = max(0, spos - swing_lookback + 1)
    window = frame.iloc[win_start:spos + 1]
    if trade_dir == 1:
        swing_target = float(window["high"].max())
        rr_price = entry_price + rr_target * atr_entry
        tp_price = min(swing_target, rr_price)
    else:
        swing_target = float(window["low"].min())
        rr_price = entry_price - rr_target * atr_entry
        tp_price = max(swing_target, rr_price)

    n = len(frame)
    for k in range(1, max_hold + 1):
        pos = epos + k
        if pos >= n:
            last = n - 1
            return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                         atr_entry, risk_distance, confirm_n, frame.index[last],
                         float(frame["close"].iloc[last]), "data_end", k)
        bar = frame.iloc[pos]
        if trade_dir == 1:
            if bar["low"] <= stop_price:
                return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                             atr_entry, risk_distance, confirm_n, frame.index[pos],
                             stop_price, "stop", k)
            if bar["high"] >= tp_price:
                return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                             atr_entry, risk_distance, confirm_n, frame.index[pos],
                             tp_price, "tp", k)
        else:
            if bar["high"] >= stop_price:
                return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                             atr_entry, risk_distance, confirm_n, frame.index[pos],
                             stop_price, "stop", k)
            if bar["low"] <= tp_price:
                return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                             atr_entry, risk_distance, confirm_n, frame.index[pos],
                             tp_price, "tp", k)
        if k == max_hold:
            return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                         atr_entry, risk_distance, confirm_n, frame.index[pos],
                         float(bar["close"]), "time", k)
    return None


def run_variant(frame: pd.DataFrame, confirm_n_th: int | None = CONFIRM_N_TH,
                 reverse: bool = False, rr_target: float = RR_TARGET,
                 sl_buffer: float = SL_BUFFER, max_hold: int = MAX_HOLD,
                 signals: list | None = None) -> list[Trade]:
    if signals is None:
        signals = find_signals(frame, confirm_n_th)
    trades = []
    for signal_time, raw_direction, confirm_n in signals:
        tr = simulate_trade(frame, signal_time, raw_direction, confirm_n, reverse=reverse,
                             rr_target=rr_target, sl_buffer=sl_buffer, max_hold=max_hold)
        if tr is not None:
            trades.append(tr)
    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame(columns=["signal_time", "entry_time", "exit_time", "raw_direction",
                                      "trade_direction", "confirm_n", "exit_reason", "hold_bars",
                                      "gross_R", "net_R"])
    rows = []
    for t in trades:
        rows.append({
            "signal_time": t.signal_time, "entry_time": t.entry_time, "exit_time": t.exit_time,
            "raw_direction": t.raw_direction, "trade_direction": t.trade_direction,
            "confirm_n": t.confirm_n, "exit_reason": t.exit_reason, "hold_bars": t.hold_bars,
            "gross_R": t.gross_R, "net_R": t.net_R,
        })
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)


def split_is_oos(df: pd.DataFrame, is_start, is_end, oos_start, oos_end
                  ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    is_df = df[(df["entry_time"] >= is_start) & (df["entry_time"] <= is_end)]
    oos_df = df[(df["entry_time"] >= oos_start) & (df["entry_time"] <= oos_end)]
    full_df = df[(df["entry_time"] >= is_start) & (df["entry_time"] <= oos_end)]
    return is_df, oos_df, full_df
