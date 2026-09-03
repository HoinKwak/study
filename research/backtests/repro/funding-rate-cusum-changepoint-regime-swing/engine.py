"""체결 엔진 — CUSUM 체인지포인트(펀딩레이트) -> EMA20/60 방향 확인 -> 다음 4h봉 시가 진입
-> ATR 트레일링(3.0) + 고정 SL(1.5×ATR, 진입가 대칭) + 반대 체인지포인트 무효화 + 45봉 시간청산.
전부 R-배수로 산출(risk_distance = ATR_entry × stop_mult, 진입 시 1회 계산).

⚠️ 타이밍 정합: 8h 정산(00/08/16 UTC)은 4h 봉 경계와 정확히 일치한다(4h 봉은 0,4,8,...20
UTC에 오픈). CUSUM 이벤트 시각 t 에서 "직전 완결봉"은 open_time=t-4h(close_time=t, 바로
그 순간 완결)이고 EMA/ATR 판정은 그 봉으로 한다. "다음 4h 봉"은 open_time=t 인 바로 그 봉이라
곧바로 그 시가에 체결 가능(지연 없음, 룩어헤드 없음 — 결정에 필요한 정보가 전부 t 시점에
확정돼 있다).

반대 체인지포인트 무효화(반전 대조군 처리): '테제 무효화'류 청산이라 **원신호(direction)
기준**으로 판정한다(trade_dir 아님, CLAUDE.md 축적 규칙과 일치). risk_distance 는 원신호
기준 1회 계산해 반전 시에도 대칭 재배치(SL 은 표준 메커니즘이라 대칭 재배치 유지).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from common import ROUND_TRIP_COST, ema_4h, atr14_4h, load_symbol
from events import detect_events, filter_8h


@dataclass
class Trade:
    symbol: str
    event_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry_price: float
    direction: int          # 원신호 방향 (1=롱, -1=숏), reverse 여부와 무관
    trade_dir: int           # 실제 매매 방향(reverse 시 -direction)
    atr_entry: float
    risk_distance: float
    e_val: float
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


def build_frame(symbol: str, baseline_window: int = 60, cusum_k: float = 0.5,
                cusum_h: float = 4.0, ema_fast: int = 20, ema_slow: int = 60) -> dict:
    data = load_symbol(symbol)
    funding = data["funding"]
    price_4h = data["price_4h"]
    funding_8h, excluded_frac = filter_8h(funding)
    events, diag = detect_events(funding_8h, baseline_window=baseline_window, k=cusum_k, h=cusum_h)
    ema = ema_4h(price_4h, ema_fast, ema_slow)
    atr = atr14_4h(price_4h)
    return {"symbol": symbol, "price_4h": price_4h, "ema": ema, "atr": atr,
            "funding": funding, "funding_8h": funding_8h, "excluded_frac": excluded_frac,
            "events": events, "diag": diag}


def find_signals(frame: dict) -> pd.DataFrame:
    """이벤트에 EMA 방향 게이트를 적용해 진입 후보를 만든다.

    - 직전 완결 4h봉(open_time = event_time - 4h) 의 ema_fast/ema_slow 로 방향 확인.
    - 롱: direction==1(상방 체인지포인트) AND ema_fast>ema_slow(해당 완결봉)
    - 숏: direction==-1 AND ema_fast<ema_slow
    - 진입봉(open_time == event_time)이 가격 데이터에 없으면(데이터 경계) 제외.
    """
    ev = frame["events"]
    if len(ev) == 0:
        return pd.DataFrame()
    price = frame["price_4h"]
    ema = frame["ema"]
    atr = frame["atr"]

    rows = []
    for _, r in ev.iterrows():
        t = r["event_time"]
        prev_open = t - pd.Timedelta(hours=4)
        if prev_open not in price.index or t not in price.index:
            continue
        prev_pos = price.index.get_loc(prev_open)
        ema_fast_v = ema["ema_fast"].iloc[prev_pos]
        ema_slow_v = ema["ema_slow"].iloc[prev_pos]
        atr_v = atr.iloc[prev_pos]
        if not (np.isfinite(ema_fast_v) and np.isfinite(ema_slow_v) and np.isfinite(atr_v)
                and atr_v > 0):
            continue
        direction = int(r["direction"])
        if direction == 1 and not (ema_fast_v > ema_slow_v):
            continue
        if direction == -1 and not (ema_fast_v < ema_slow_v):
            continue
        rows.append({"event_time": t, "direction": direction, "e": float(r["e"]),
                     "atr_entry": float(atr_v)})
    return pd.DataFrame(rows)


def simulate_trades(frame: dict, signals: pd.DataFrame, stop_mult: float = 1.5,
                    atr_trail_mult: float = 3.0, max_hold_bars: int = 45,
                    reverse: bool = False, disable_reversal_exit: bool = False,
                    signal_source: str | None = None) -> list[Trade]:
    """단일 심볼, 순차 체결(포지션 보유 중엔 새 신호 무시 — 스윙 저빈도 특성).

    signal_source: None 이면 frame['events'](CUSUM)를 반전청산 트리거로 쓰고, 다른 값을
    지정하면(신호원 교체 대조군용) 해당 이벤트 프레임을 사용하지 않고 반전청산을 비활성화.
    """
    if len(signals) == 0:
        return []
    price = frame["price_4h"]
    ema = frame["ema"]
    atr = frame["atr"]
    events = frame["events"]  # 반대 체인지포인트 탐색용(항상 원 CUSUM 이벤트 스트림 사용)

    signals = signals.sort_values("event_time").reset_index(drop=True)
    trades: list[Trade] = []
    last_exit_time = None

    for _, sig in signals.iterrows():
        t = sig["event_time"]
        if last_exit_time is not None and t <= last_exit_time:
            continue  # 포지션 보유 중 신호는 건너뜀(다음 신호로)
        if t not in price.index:
            continue
        epos = price.index.get_loc(t)
        entry_time = t
        entry_price = float(price["open"].iloc[epos])
        direction = int(sig["direction"])
        trade_dir = -direction if reverse else direction
        atr_entry = float(sig["atr_entry"])
        risk_distance = atr_entry * stop_mult
        if risk_distance <= 0 or not np.isfinite(risk_distance):
            continue

        if trade_dir == 1:
            stop = entry_price - risk_distance
        else:
            stop = entry_price + risk_distance

        # 반대 체인지포인트(원신호 기준) — entry_time 이후 최초 1건
        reversal_time = None
        if not disable_reversal_exit:
            opp = events[(events["direction"] == -direction) & (events["event_time"] > entry_time)]
            if len(opp):
                reversal_time = opp["event_time"].iloc[0]

        n = len(price)
        running_extreme = float(price["high"].iloc[epos]) if trade_dir == 1 else float(
            price["low"].iloc[epos])
        active_stop = stop  # 래칫: SL 에서 시작해 유리한 쪽으로만 조여든다(역행 완화 없음)
        exit_trade = None
        for k in range(1, max_hold_bars + 1):
            pos = epos + k
            if pos >= n:
                last = n - 1
                exit_trade = Trade(frame["symbol"], t, entry_time, entry_price, direction,
                                    trade_dir, atr_entry, risk_distance, float(sig["e"]),
                                    price.index[last], float(price["close"].iloc[last]),
                                    "data_end", k)
                break
            ts = price.index[pos]
            bar = price.iloc[pos]

            # 1) 반대 체인지포인트 무효화 — 그 봉 시가에서 즉시 청산(봉이 열리는 순간 확정)
            if reversal_time is not None and ts == reversal_time:
                exit_trade = Trade(frame["symbol"], t, entry_time, entry_price, direction,
                                    trade_dir, atr_entry, risk_distance, float(sig["e"]),
                                    ts, float(bar["open"]), "reversal_invalidation", k)
                break

            # 2) ATR 트레일링(전봉 ATR·running_extreme, 래칫으로 SL 대비 역행 없음) + 고정 SL
            atr_prev = float(atr.iloc[pos - 1])
            if trade_dir == 1:
                trail_stop = running_extreme - atr_trail_mult * atr_prev
                active_stop = max(active_stop, trail_stop)
                if bar["low"] <= active_stop:
                    exit_trade = Trade(frame["symbol"], t, entry_time, entry_price, direction,
                                        trade_dir, atr_entry, risk_distance, float(sig["e"]),
                                        ts, active_stop, "atr_trail_or_sl", k)
                    break
            else:
                trail_stop = running_extreme + atr_trail_mult * atr_prev
                active_stop = min(active_stop, trail_stop)
                if bar["high"] >= active_stop:
                    exit_trade = Trade(frame["symbol"], t, entry_time, entry_price, direction,
                                        trade_dir, atr_entry, risk_distance, float(sig["e"]),
                                        ts, active_stop, "atr_trail_or_sl", k)
                    break

            # 3) 시간청산
            if k == max_hold_bars:
                exit_trade = Trade(frame["symbol"], t, entry_time, entry_price, direction,
                                    trade_dir, atr_entry, risk_distance, float(sig["e"]),
                                    ts, float(bar["close"]), "time", k)
                break

            # 다음 루프를 위해 running_extreme 갱신(이번 봉까지 반영, causal — 다음 봉 판정에만 사용)
            if trade_dir == 1:
                running_extreme = max(running_extreme, float(bar["high"]))
            else:
                running_extreme = min(running_extreme, float(bar["low"]))

        if exit_trade is not None:
            trades.append(exit_trade)
            last_exit_time = exit_trade.exit_time

    return trades


def load_all(baseline_window: int = 60, cusum_k: float = 0.5, cusum_h: float = 4.0,
            ema_fast: int = 20, ema_slow: int = 60) -> dict:
    from common import SYMBOLS
    out = {}
    for sym in SYMBOLS:
        out[sym] = build_frame(sym, baseline_window=baseline_window, cusum_k=cusum_k,
                               cusum_h=cusum_h, ema_fast=ema_fast, ema_slow=ema_slow)
    return out


def run_variant(universe: dict, stop_mult: float = 1.5, atr_trail_mult: float = 3.0,
                max_hold_bars: int = 45, reverse: bool = False,
                disable_reversal_exit: bool = False, no_ema_gate: bool = False) -> list[Trade]:
    trades = []
    for sym, frame in universe.items():
        if no_ema_gate:
            ev = frame["events"]
            if len(ev) == 0:
                continue
            price = frame["price_4h"]
            atr = frame["atr"]
            rows = []
            for _, r in ev.iterrows():
                t = r["event_time"]
                prev_open = t - pd.Timedelta(hours=4)
                if prev_open not in price.index or t not in price.index:
                    continue
                prev_pos = price.index.get_loc(prev_open)
                atr_v = atr.iloc[prev_pos]
                if not (np.isfinite(atr_v) and atr_v > 0):
                    continue
                rows.append({"event_time": t, "direction": int(r["direction"]),
                            "e": float(r["e"]), "atr_entry": float(atr_v)})
            signals = pd.DataFrame(rows)
        else:
            signals = find_signals(frame)
        tr = simulate_trades(frame, signals, stop_mult=stop_mult, atr_trail_mult=atr_trail_mult,
                             max_hold_bars=max_hold_bars, reverse=reverse,
                             disable_reversal_exit=disable_reversal_exit)
        trades.extend(tr)
    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame()
    return pd.DataFrame([{
        "symbol": t.symbol, "event_time": t.event_time, "entry_time": t.entry_time,
        "entry_price": t.entry_price, "direction": t.direction, "trade_dir": t.trade_dir,
        "atr_entry": t.atr_entry, "risk_distance": t.risk_distance, "e_val": t.e_val,
        "exit_time": t.exit_time, "exit_price": t.exit_price, "exit_reason": t.exit_reason,
        "hold_bars": t.hold_bars, "gross_R": t.gross_R, "net_R": t.net_R,
    } for t in trades])
