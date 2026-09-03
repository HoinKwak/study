"""BTC 15m Donchian(20) 브레이크아웃 + 1h 스프레드(OI가중 vs 등가중 실현변동성) z-score 게이트
— 신호/체결 엔진. 전부 R-배수로 산출(gross/net 병기), 진입은 shift(1)(신호봉 다음봉 시가).

청산: 손절 고정(진입가 ∓ATR(15m,14)×1.0, 방향 무관 대칭) → 트레일링(신고가/신저가∓ATR×1.4,
SL 보다 유리해지면 교체, 이번봉 갱신 후 다음봉부터 유효) → max_hold=10봉 시간청산.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

import common as C

ROUNDTRIP_COST = C.ROUNDTRIP_COST


@dataclass
class Trade:
    signal_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry_price: float
    raw_direction: int      # 원신호 방향(브레이크아웃 방향): +1=롱(상단돌파) -1=숏(하단이탈)
    trade_direction: int    # 실제 체결 방향(반전판은 -raw_direction)
    atr_entry: float
    risk_distance: float    # ATR(15m,14)×stop_mult — 방향 무관 대칭(원신호/반전 동일값)
    gate_state: str
    exit_time: pd.Timestamp
    exit_price: float
    exit_reason: str
    hold_bars: int
    gross_R: float = field(init=False)

    def __post_init__(self):
        self.gross_R = (self.exit_price - self.entry_price) / self.risk_distance * self.trade_direction

    @property
    def net_R(self) -> float:
        cost_R = ROUNDTRIP_COST * self.entry_price / self.risk_distance
        return self.gross_R - cost_R


def find_signals(df15: pd.DataFrame, don_hi: np.ndarray, don_lo: np.ndarray,
                  gate_1h_aligned: pd.Series | None, mode: str,
                  rng: np.random.Generator | None = None,
                  random_probs: dict | None = None) -> list[tuple[pd.Timestamp, int, str]]:
    """(signal_time, raw_direction, gate_state) 리스트. mode 에 따라 게이트 적용 방식이 다름.

    mode:
      - "ungated": 게이트 없음, 브레이크아웃이면 항상 발화(양방향).
      - "gated"/"btc_solo"/"ew_solo"/"reverse": gate_1h_aligned 값(short_only/long_only/neutral)에
        따라 방향별로 스킵. NaN(워밍업)이면 스킵.
      - "random_gate": 같은 시점별 gate_state 를 무작위(관측 3분류 비율 유지, rng 로 매 bar 독립
        추첨)로 재생성해 실제 spread_z 타이밍과 무관한 placebo 게이트로 사용.
    """
    close = df15["close"].to_numpy(float)
    idx = df15.index
    out = []
    if mode == "random_gate":
        states = ["short_only", "long_only", "neutral"]
        p = [random_probs["short_only"], random_probs["long_only"], random_probs["neutral"]]
        gate_arr = rng.choice(states, size=len(idx), p=p)
    elif mode == "ungated":
        gate_arr = None
    else:
        gate_arr = gate_1h_aligned.reindex(idx).to_numpy(dtype=object)

    for i in range(len(idx)):
        if not np.isfinite(don_hi[i]) or not np.isfinite(don_lo[i]):
            continue
        c = close[i]
        long_break = c > don_hi[i]
        short_break = c < don_lo[i]
        if not (long_break or short_break):
            continue

        if mode == "ungated":
            state = "neutral"
        else:
            state = gate_arr[i]
            if state is None or (isinstance(state, float) and np.isnan(state)):
                continue

        sig_long = long_break and (state in ("neutral", "long_only"))
        sig_short = short_break and (state in ("neutral", "short_only"))
        if sig_long:
            out.append((idx[i], 1, state))
        elif sig_short:
            out.append((idx[i], -1, state))
    return out


def simulate_trade(df15: pd.DataFrame, atr14: pd.Series, signal_time: pd.Timestamp,
                    raw_direction: int, gate_state: str, reverse: bool = False,
                    atr_trail_mult: float = C.ATR_TRAIL_MULT, atr_stop_mult: float = C.ATR_STOP_MULT,
                    max_hold: int = C.MAX_HOLD) -> Trade | None:
    if signal_time not in df15.index:
        return None
    spos = df15.index.get_loc(signal_time)
    epos = spos + 1
    if epos >= len(df15):
        return None

    atr_entry = float(atr14.iloc[spos])
    if not np.isfinite(atr_entry) or atr_entry <= 0:
        return None

    entry_time = df15.index[epos]
    entry_price = float(df15["open"].iloc[epos])

    # 리스크 거리: ATR(15m,14)×stop_mult — 방향과 무관하게 항상 같은 크기(대칭). 원신호/반전
    # 어느 쪽에서도 재계산 없이 동일값 재사용(대칭 재배치 요건 자동 충족).
    risk_distance = atr_entry * atr_stop_mult
    if risk_distance <= 0:
        return None

    trade_dir = -raw_direction if reverse else raw_direction
    stop_price = entry_price - trade_dir * risk_distance

    high = df15["high"].to_numpy(float)
    low = df15["low"].to_numpy(float)
    close = df15["close"].to_numpy(float)
    n = len(df15)

    running_ext = df15["high"].iloc[epos] if trade_dir == 1 else df15["low"].iloc[epos]

    for k in range(1, max_hold + 1):
        pos = epos + k
        if pos >= n:
            last = n - 1
            return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                        atr_entry, risk_distance, gate_state, df15.index[last],
                        float(close[last]), "data_end", k)
        h, l = high[pos], low[pos]
        if trade_dir == 1:
            if l <= stop_price:
                return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                            atr_entry, risk_distance, gate_state, df15.index[pos],
                            stop_price, "stop_or_trail", k)
            running_ext = max(running_ext, h)
            trail_cand = running_ext - atr_trail_mult * atr_entry
            stop_price = max(stop_price, trail_cand)
        else:
            if h >= stop_price:
                return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                            atr_entry, risk_distance, gate_state, df15.index[pos],
                            stop_price, "stop_or_trail", k)
            running_ext = min(running_ext, l)
            trail_cand = running_ext + atr_trail_mult * atr_entry
            stop_price = min(stop_price, trail_cand)
        if k == max_hold:
            return Trade(signal_time, entry_time, entry_price, raw_direction, trade_dir,
                        atr_entry, risk_distance, gate_state, df15.index[pos],
                        float(close[pos]), "time", k)
    return None


def run_variant(df15: pd.DataFrame, don_hi: np.ndarray, don_lo: np.ndarray, atr14: pd.Series,
                 gate_1h_aligned: pd.Series | None, mode: str, reverse: bool = False,
                 atr_trail_mult: float = C.ATR_TRAIL_MULT, atr_stop_mult: float = C.ATR_STOP_MULT,
                 max_hold: int = C.MAX_HOLD, rng: np.random.Generator | None = None,
                 random_probs: dict | None = None,
                 signals: list | None = None) -> list[Trade]:
    if signals is None:
        signals = find_signals(df15, don_hi, don_lo, gate_1h_aligned, mode, rng, random_probs)
    trades = []
    for signal_time, raw_direction, gate_state in signals:
        tr = simulate_trade(df15, atr14, signal_time, raw_direction, gate_state, reverse=reverse,
                            atr_trail_mult=atr_trail_mult, atr_stop_mult=atr_stop_mult,
                            max_hold=max_hold)
        if tr is not None:
            trades.append(tr)
    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame(columns=["signal_time", "entry_time", "exit_time", "raw_direction",
                                     "trade_direction", "gate_state", "exit_reason", "hold_bars",
                                     "gross_R", "net_R"])
    rows = []
    for t in trades:
        rows.append({
            "signal_time": t.signal_time, "entry_time": t.entry_time, "exit_time": t.exit_time,
            "raw_direction": t.raw_direction, "trade_direction": t.trade_direction,
            "gate_state": t.gate_state, "exit_reason": t.exit_reason, "hold_bars": t.hold_bars,
            "gross_R": t.gross_R, "net_R": t.net_R,
        })
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
