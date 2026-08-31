"""프리미엄인덱스 꼬리비율(wick ratio) 소진 반전 — 체결 엔진.

신호(4h premiumIndexKlines wick_asym 연속카운트 + premium 부호 + 1d EMA20 이격) ->
진입(다음 4h 봉 시가, shift(1)) -> 청산(ATR 트레일링/SL/시간/프리미엄 제로크로스, 4h 바 시뮬레이션).
전부 R-배수로 산출(gross/net 병기).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from common import ROUND_TRIP_COST, SYMBOLS, atr14, ema20_1d, load_symbol, wick_asym


@dataclass
class Trade:
    symbol: str
    signal_time: pd.Timestamp   # 신호 확정 4h 봉(t) 시각
    entry_time: pd.Timestamp    # 진입 4h 봉(t+1) 시각
    entry_price: float
    direction: int   # 1=long, -1=short
    atr_entry: float
    risk_distance: float
    exit_time: pd.Timestamp
    exit_price: float
    exit_reason: str
    hold_bars: int
    consec: int          # 진입시점 consec_upper/lower 값
    prem_close_sig: float
    ext_pct_sig: float
    gross_R: float = field(init=False)

    def __post_init__(self):
        raw = (self.exit_price - self.entry_price) / self.risk_distance * self.direction
        self.gross_R = raw

    @property
    def net_R(self) -> float:
        cost_R = ROUND_TRIP_COST * self.entry_price / self.risk_distance
        return self.gross_R - cost_R


def build_frame(symbol: str, wick_th: float = 0.4, lookback_bars: int = 6,
                 min_count: int = 4, ext_th: float = 0.05) -> dict:
    """symbol -> {prem4h(신호용 컬럼 포함), price4h, atr4h, ema20_1d}"""
    data = load_symbol(symbol)
    prem = data["prem_4h"].copy()
    price = data["price_4h"]
    price1d = data["price_1d"]

    idx = prem.index.intersection(price.index)
    prem = prem.loc[idx]
    price_aligned = price.loc[idx]

    wa = wick_asym(prem)
    prem["wick_asym"] = wa
    is_upper = (wa >= wick_th).astype(float)
    is_lower = (wa <= -wick_th).astype(float)
    # 최근 lookback_bars(현재봉 포함) 중 개수 — rolling sum
    prem["consec_upper"] = is_upper.rolling(lookback_bars, min_periods=lookback_bars).sum()
    prem["consec_lower"] = is_lower.rolling(lookback_bars, min_periods=lookback_bars).sum()
    prem["premium_close"] = prem["close"]

    # 1d EMA20 -> 4h 로 인과적(lookahead 없는) 정렬: 4h 봉 t 시각에는 "그 이전에 완결된"
    # 일봉만 참조 가능. 일봉 index(0시 UTC)는 (index+1day) 시점에야 완결.
    ema_1d = ema20_1d(price1d)
    daily_closed_at = price1d.index + pd.DateOffset(days=1)  # ms/us 함정 회피(DateOffset)
    order = np.argsort(daily_closed_at.values)
    closed_sorted = daily_closed_at.values[order]
    ema_sorted = ema_1d.values[order]
    pos = np.searchsorted(closed_sorted, price_aligned.index.values, side="right") - 1
    ema_aligned = np.where(pos >= 0, ema_sorted[np.clip(pos, 0, None)], np.nan)
    prem["ema20_1d"] = ema_aligned
    prem["price_close"] = price_aligned["close"]
    prem["ext_pct"] = (price_aligned["close"] - ema_aligned) / ema_aligned

    atr = atr14(price)
    return {"prem": prem, "price": price, "atr": atr, "min_count": min_count,
            "wick_th": wick_th, "lookback_bars": lookback_bars, "ext_th": ext_th}


def find_signals(frame: dict) -> list[tuple[pd.Timestamp, int, int, float, float]]:
    """(signal_time, direction, consec, prem_close, ext_pct) 리스트. direction: 1=롱, -1=숏."""
    prem = frame["prem"]
    min_count = frame["min_count"]
    ext_th = frame["ext_th"]
    out = []
    cu = prem["consec_upper"].to_numpy()
    cl = prem["consec_lower"].to_numpy()
    pc = prem["premium_close"].to_numpy()
    ext = prem["ext_pct"].to_numpy()
    idx = prem.index
    n = len(prem)
    for i in range(n):
        if not np.isfinite(cu[i]) or not np.isfinite(ext[i]):
            continue
        if cu[i] >= min_count and pc[i] > 0 and ext[i] >= ext_th:
            out.append((idx[i], -1, int(cu[i]), float(pc[i]), float(ext[i])))
        elif cl[i] >= min_count and pc[i] < 0 and ext[i] <= -ext_th:
            out.append((idx[i], 1, int(cl[i]), float(pc[i]), float(ext[i])))
    return out


def simulate_trade(frame: dict, signal_time: pd.Timestamp, direction: int,
                    consec: int, prem_close_sig: float, ext_pct_sig: float,
                    atr_sl_mult: float, atr_trail_mult: float, max_hold_bars: int,
                    reverse: bool = False) -> Trade | None:
    price = frame["price"]
    atr = frame["atr"]
    prem = frame["prem"]

    if signal_time not in price.index:
        return None
    spos = price.index.get_loc(signal_time)
    epos = spos + 1  # shift(1) 진입: 다음 4h 봉 시가
    if epos >= len(price.index):
        return None
    entry_time = price.index[epos]
    entry_price = price["open"].iloc[epos]

    # ATR: 신호 확정봉(t) 값 사용(그 시점까지 확정된 정보, shift 불필요 — t는 이미 닫힌 봉)
    atr_entry = atr.iloc[spos]
    if pd.isna(atr_entry) or atr_entry <= 0:
        return None

    trade_dir = -direction if reverse else direction
    risk_distance = atr_entry * atr_sl_mult  # 원신호 기준 1회 계산(반전 시에도 동일값 재사용)
    if trade_dir == 1:
        init_sl = entry_price - risk_distance
    else:
        init_sl = entry_price + risk_distance

    n = len(price)
    extreme = price["high"].iloc[epos] if trade_dir == 1 else price["low"].iloc[epos]
    for k in range(1, max_hold_bars + 1):
        pos = epos + k  # k=1 -> 진입봉(entry_time) 다음 봉부터 SL/TP 판정
        if pos >= n:
            last = n - 1
            return Trade(frame_symbol(frame), signal_time, entry_time, entry_price, trade_dir,
                         atr_entry, risk_distance, price.index[last], price["close"].iloc[last],
                         "data_end", k, consec, prem_close_sig, ext_pct_sig)
        bar = price.iloc[pos]
        # 챈들리어 트레일링 + 초기 SL 결합
        if trade_dir == 1:
            chand = extreme - atr_entry * atr_trail_mult
            eff_stop = max(init_sl, chand)
            if bar["low"] <= eff_stop:
                return Trade(frame_symbol(frame), signal_time, entry_time, entry_price, trade_dir,
                             atr_entry, risk_distance, price.index[pos], eff_stop,
                             "stop", k, consec, prem_close_sig, ext_pct_sig)
        else:
            chand = extreme + atr_entry * atr_trail_mult
            eff_stop = min(init_sl, chand)
            if bar["high"] >= eff_stop:
                return Trade(frame_symbol(frame), signal_time, entry_time, entry_price, trade_dir,
                             atr_entry, risk_distance, price.index[pos], eff_stop,
                             "stop", k, consec, prem_close_sig, ext_pct_sig)
        # 프리미엄인덱스 종가 0선 반대통과 익절(원신호 방향 기준 — 서사적 청산조건, 반전시에도
        # 원신호 방향 부호 그대로 사용: '프리미엄이 원래 신호가 예상한 방향으로 정상화'되면 청산)
        if bar.name in prem.index:
            pc_now = prem.loc[bar.name, "premium_close"]
            if pd.notna(pc_now):
                if direction == -1 and pc_now < 0:   # 원신호 숏: 프리미엄이 콘탱고->백워데이션
                    return Trade(frame_symbol(frame), signal_time, entry_time, entry_price,
                                 trade_dir, atr_entry, risk_distance, price.index[pos],
                                 bar["close"], "premium_zerocross", k, consec, prem_close_sig,
                                 ext_pct_sig)
                if direction == 1 and pc_now > 0:    # 원신호 롱: 프리미엄이 백워데이션->콘탱고
                    return Trade(frame_symbol(frame), signal_time, entry_time, entry_price,
                                 trade_dir, atr_entry, risk_distance, price.index[pos],
                                 bar["close"], "premium_zerocross", k, consec, prem_close_sig,
                                 ext_pct_sig)
        if k == max_hold_bars:
            return Trade(frame_symbol(frame), signal_time, entry_time, entry_price, trade_dir,
                         atr_entry, risk_distance, price.index[pos], bar["close"],
                         "time", k, consec, prem_close_sig, ext_pct_sig)
        if trade_dir == 1:
            extreme = max(extreme, bar["high"])
        else:
            extreme = min(extreme, bar["low"])
    return None


_SYM_MAP: dict[int, str] = {}


def frame_symbol(frame: dict) -> str:
    return frame.get("_symbol", "?")


def load_all(wick_th: float = 0.4, lookback_bars: int = 6, min_count: int = 4,
             ext_th: float = 0.05) -> dict:
    out = {}
    for sym in SYMBOLS:
        fr = build_frame(sym, wick_th=wick_th, lookback_bars=lookback_bars,
                          min_count=min_count, ext_th=ext_th)
        fr["_symbol"] = sym
        out[sym] = fr
    return out


def run_variant(universe: dict, atr_sl_mult: float = 1.4, atr_trail_mult: float = 2.2,
                 max_hold_bars: int = 30, reverse: bool = False,
                 gate: str = "full") -> list[Trade]:
    """gate: 'full'(전체조건) / 'no_gate'(consec 조건만, premium 부호+ext 필터 제거) /
    'no_ext'(ext 필터만 제거) / 'no_premium_sign'(premium 부호만 제거)."""
    trades = []
    for sym, frame in universe.items():
        if gate == "full":
            signals = find_signals(frame)
        else:
            signals = find_signals_gated(frame, gate)
        for signal_time, direction, consec, prem_c, ext_p in signals:
            tr = simulate_trade(frame, signal_time, direction, consec, prem_c, ext_p,
                                 atr_sl_mult, atr_trail_mult, max_hold_bars, reverse=reverse)
            if tr is not None:
                trades.append(tr)
    return trades


def find_signals_gated(frame: dict, gate: str) -> list[tuple[pd.Timestamp, int, int, float, float]]:
    prem = frame["prem"]
    min_count = frame["min_count"]
    ext_th = frame["ext_th"]
    out = []
    cu = prem["consec_upper"].to_numpy()
    cl = prem["consec_lower"].to_numpy()
    pc = prem["premium_close"].to_numpy()
    ext = prem["ext_pct"].to_numpy()
    idx = prem.index
    n = len(prem)
    for i in range(n):
        if not np.isfinite(cu[i]) or not np.isfinite(ext[i]):
            continue
        short_ok = cu[i] >= min_count
        long_ok = cl[i] >= min_count
        if gate == "no_ext":
            short_ok = short_ok and pc[i] > 0
            long_ok = long_ok and pc[i] < 0
        elif gate == "no_premium_sign":
            short_ok = short_ok and ext[i] >= ext_th
            long_ok = long_ok and ext[i] <= -ext_th
        elif gate == "no_gate":
            pass  # consec 조건만
        if short_ok and not long_ok:
            out.append((idx[i], -1, int(cu[i]), float(pc[i]), float(ext[i])))
        elif long_ok and not short_ok:
            out.append((idx[i], 1, int(cl[i]), float(pc[i]), float(ext[i])))
    return out


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame(columns=["symbol", "signal_time", "entry_time", "exit_time",
                                      "direction", "exit_reason", "hold_bars", "consec",
                                      "gross_R", "net_R"])
    rows = []
    for t in trades:
        rows.append({
            "symbol": t.symbol, "signal_time": t.signal_time, "entry_time": t.entry_time,
            "exit_time": t.exit_time, "direction": t.direction, "exit_reason": t.exit_reason,
            "hold_bars": t.hold_bars, "consec": t.consec, "prem_close_sig": t.prem_close_sig,
            "ext_pct_sig": t.ext_pct_sig, "gross_R": t.gross_R, "net_R": t.net_R,
        })
    df = pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
    return df


def split_is_oos(df: pd.DataFrame, is_start, is_end, oos_start, oos_end
                  ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    is_df = df[(df["entry_time"] >= is_start) & (df["entry_time"] <= is_end)]
    oos_df = df[(df["entry_time"] >= oos_start) & (df["entry_time"] <= oos_end)]
    full_df = df[(df["entry_time"] >= is_start) & (df["entry_time"] <= oos_end)]
    return is_df, oos_df, full_df
