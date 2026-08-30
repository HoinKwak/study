"""크로스섹셔널 프리미엄인덱스 스퀴즈 순위 로테이션 — 체결 엔진.

신호(1d, squeeze_pctile+donchian breakout) -> 진입확인(4h 첫 봉) -> 청산(4h 바 시뮬레이션).
전부 R-배수로 산출(costs 포함/미포함 병기).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from common import (SYMBOLS, atr14, build_daily_frame, load_symbol,
                     IS_START, IS_END, OOS_START, OOS_END)

ROUND_TRIP_COST = 0.0014  # 왕복 수수료+슬리피지


@dataclass
class Trade:
    symbol: str
    reg_date: pd.Timestamp
    trigger_date: pd.Timestamp
    entry_time: pd.Timestamp
    entry_price: float
    direction: int  # 1=long, -1=short
    atr_entry: float
    risk_distance: float
    exit_time: pd.Timestamp
    exit_price: float
    exit_reason: str
    hold_bars: int
    gross_R: float = field(init=False)

    def __post_init__(self):
        raw = (self.exit_price - self.entry_price) / self.risk_distance * self.direction
        self.gross_R = raw

    @property
    def net_R(self) -> float:
        cost_R = ROUND_TRIP_COST * self.entry_price / self.risk_distance
        return self.gross_R - cost_R


def load_all(squeeze_window: int = 60, donchian_len: int = 15) -> dict:
    """symbol -> {daily: DataFrame, price_4h: DataFrame, atr4h: Series}"""
    out = {}
    for sym in SYMBOLS:
        data = load_symbol(sym)
        daily = build_daily_frame(sym, data, squeeze_window=squeeze_window,
                                   donchian_len=donchian_len)
        price_4h = data["price_4h"]
        atr = atr14(price_4h)
        out[sym] = {"daily": daily, "price_4h": price_4h, "atr4h": atr}
    return out


def cross_sectional_calendar(universe: dict) -> pd.DatetimeIndex:
    """전 종목 공통 거래일(교집합) — Monday 등록 기준일."""
    idx = None
    for sym, d in universe.items():
        di = d["daily"].index
        idx = di if idx is None else idx.intersection(di)
    return idx.sort_values()


def register_candidates(universe: dict, calendar: pd.DatetimeIndex,
                         squeeze_entry_pctile: float, top_k: int,
                         rank_mode: str = "topk", shuffle_seed: int | None = None
                         ) -> list[tuple[str, pd.Timestamp]]:
    """매주 월요일, 압축 후보(symbol, reg_date) 등록.

    rank_mode: 'topk'(하위 top_k만) / 'no_rank'(임계 통과 전원) / 'shuffle'(주별 횡단면
    셔플 후 top_k — 셔플은 그 주 7종목의 squeeze_pctile 값을 종목 라벨과 재배정).
    """
    mondays = calendar[calendar.dayofweek == 0]
    rng = np.random.default_rng(shuffle_seed) if shuffle_seed is not None else None
    candidates = []
    for t in mondays:
        row = {}
        for sym, d in universe.items():
            daily = d["daily"]
            if t in daily.index:
                v = daily.loc[t, "squeeze_pctile"]
                if pd.notna(v):
                    row[sym] = v
        if not row:
            continue
        syms = list(row.keys())
        vals = np.array([row[s] for s in syms])
        if rank_mode == "shuffle":
            vals = rng.permutation(vals)
            row = dict(zip(syms, vals))
        eligible = [s for s in syms if row[s] <= squeeze_entry_pctile]
        if not eligible:
            continue
        if rank_mode == "no_rank":
            chosen = eligible
        else:
            chosen = sorted(eligible, key=lambda s: row[s])[:top_k]
        for s in chosen:
            candidates.append((s, t))
    return candidates


def find_triggers(universe: dict, candidates: list[tuple[str, pd.Timestamp]],
                   trigger_window: int, squeeze_exit_pctile: float
                   ) -> list[tuple[str, pd.Timestamp, pd.Timestamp]]:
    """(symbol, reg_date) -> 첫 해소일(trigger_date) 탐색. 못 찾으면 제외.

    ⚠️ 자체발견 버그(수정됨): 한 종목이 연속된 여러 월요일에 계속 압축상태(<=entry_pctile)로
    남아있으면 매주 별도 등록되고, 그 등록들의 trigger_window 가 겹쳐 **같은 trigger_date**를
    중복으로 찾아내 동일 실체 트레이드가 2회 계상되는 문제가 있었다(2026-06-03 DOGE/ADA에서
    발견 — reg_date 2026-05-25 과 06-01 두 등록이 모두 06-02 트리거를 찾아 완전히 동일한
    entry/exit/PnL 트레이드가 2건 생성됨). (symbol, trigger_date) 기준 중복 제거로 수정
    (동일 실체 이벤트는 1트레이드로만 계상 — 최초 등록분을 채택).
    """
    out = []
    for sym, reg_date in candidates:
        daily = universe[sym]["daily"]
        idx = daily.index
        pos = idx.searchsorted(reg_date)
        # reg_date 다음날부터 trigger_window 거래일 이내
        window_idx = idx[pos + 1: pos + 1 + trigger_window]
        for t in window_idx:
            v = daily.loc[t, "squeeze_pctile"]
            if pd.notna(v) and v >= squeeze_exit_pctile:
                out.append((sym, reg_date, t))
                break
    seen: set[tuple] = set()
    deduped = []
    for sym, reg_date, t in out:
        key = (sym, t)
        if key in seen:
            continue
        seen.add(key)
        deduped.append((sym, reg_date, t))
    return deduped


def signal_direction(universe: dict, triggers: list[tuple[str, pd.Timestamp, pd.Timestamp]]
                      ) -> list[tuple[str, pd.Timestamp, pd.Timestamp, int]]:
    """트리거일 종가 vs donchian 채널로 롱/숏/보류 판정."""
    out = []
    for sym, reg_date, trig_date in triggers:
        daily = universe[sym]["daily"]
        row = daily.loc[trig_date]
        dh, dl, c = row["donchian_high"], row["donchian_low"], row["price_close"]
        if pd.isna(dh) or pd.isna(dl):
            continue
        if c > dh:
            out.append((sym, reg_date, trig_date, 1))
        elif c < dl:
            out.append((sym, reg_date, trig_date, -1))
        # else: 보류
    return out


def simulate_trade(universe: dict, sym: str, trig_date: pd.Timestamp, direction: int,
                    reg_date: pd.Timestamp, atr_sl_mult: float, atr_trail_mult: float,
                    max_hold_days: int, invalidation_bars: int = 5,
                    reverse: bool = False, disable_invalidation: bool = False,
                    ) -> Trade | None:
    """단일 트레이드 4h 바 시뮬레이션."""
    price_4h = universe[sym]["price_4h"]
    atr = universe[sym]["atr4h"]
    daily = universe[sym]["daily"]

    # 진입 시각: trig_date(1d bar) 종료 = trig_date+1일 00:00 UTC 의 첫 4h 봉
    entry_time = trig_date + pd.Timedelta(days=1)
    if entry_time not in price_4h.index:
        # 가장 가까운 다음 4h 봉으로 폴백
        pos = price_4h.index.searchsorted(entry_time)
        if pos >= len(price_4h.index):
            return None
        entry_time = price_4h.index[pos]

    epos = price_4h.index.get_loc(entry_time)
    if epos == 0:
        return None
    # ATR: 진입 직전 확정봉 값(shift(1) 관례)
    atr_entry = atr.iloc[epos - 1]
    if pd.isna(atr_entry) or atr_entry <= 0:
        return None
    entry_price = price_4h["open"].iloc[epos]

    trade_dir = -direction if reverse else direction
    risk_distance = atr_entry * atr_sl_mult  # 원신호 기준 1회 계산(반전 시에도 동일값 재사용)
    if trade_dir == 1:
        init_sl = entry_price - risk_distance
    else:
        init_sl = entry_price + risk_distance

    # 원신호 기준 채널(무효화용) — 반전 시에도 원신호 방향 그대로 사용(대칭 재배치는 진입가/SL만)
    dh = daily.loc[trig_date, "donchian_high"]
    dl = daily.loc[trig_date, "donchian_low"]
    # 무효화 레벨: 반전 모드에서는 최종(반전된) 방향 기준으로 재해석 — direction(원신호) 기준 채널을
    # trade_dir 기준으로 재배치(원신호 채널 대신 대칭 반사가 아니라, 무효화는 '브레이크아웃 실패'
    # 서사이므로 최종 방향 기준으로 뒤집는다: 반전 롱이면 반전 롱의 무효화 레벨=dl(반전 전 숏의
    # 채널), 반전 숏이면 dh).
    if trade_dir == 1:
        invalidation_level = dl if reverse else dh
    else:
        invalidation_level = dh if reverse else dl

    max_hold_bars = max_hold_days * 6  # 4h 봉 하루 6개

    extreme = price_4h["high"].iloc[epos] if trade_dir == 1 else price_4h["low"].iloc[epos]
    n = len(price_4h)
    for k in range(1, max_hold_bars + 1):
        pos = epos + k
        if pos >= n:
            # 데이터 끝 도달 — 마지막 봉 종가로 강제청산
            last = n - 1
            return Trade(sym, reg_date, trig_date, entry_time, entry_price, trade_dir,
                         atr_entry, risk_distance, price_4h.index[last],
                         price_4h["close"].iloc[last], "data_end", k)
        bar = price_4h.iloc[pos]
        # 챈들리어(트레일링) + 초기SL 결합: 롱은 max(SL, chandelier), 숏은 min(SL, chandelier)
        if trade_dir == 1:
            chand = extreme - atr_entry * atr_trail_mult
            eff_stop = max(init_sl, chand)
            if bar["low"] <= eff_stop:
                return Trade(sym, reg_date, trig_date, entry_time, entry_price, trade_dir,
                             atr_entry, risk_distance, price_4h.index[pos], eff_stop,
                             "stop", k)
        else:
            chand = extreme + atr_entry * atr_trail_mult
            eff_stop = min(init_sl, chand)
            if bar["high"] >= eff_stop:
                return Trade(sym, reg_date, trig_date, entry_time, entry_price, trade_dir,
                             atr_entry, risk_distance, price_4h.index[pos], eff_stop,
                             "stop", k)
        # 브레이크아웃 무효화(최초 invalidation_bars 봉 이내, 종가 기준)
        if not disable_invalidation and k <= invalidation_bars and pd.notna(invalidation_level):
            if trade_dir == 1 and bar["close"] < invalidation_level:
                return Trade(sym, reg_date, trig_date, entry_time, entry_price, trade_dir,
                             atr_entry, risk_distance, price_4h.index[pos], bar["close"],
                             "invalidation", k)
            if trade_dir == -1 and bar["close"] > invalidation_level:
                return Trade(sym, reg_date, trig_date, entry_time, entry_price, trade_dir,
                             atr_entry, risk_distance, price_4h.index[pos], bar["close"],
                             "invalidation", k)
        # 시간청산
        if k == max_hold_bars:
            return Trade(sym, reg_date, trig_date, entry_time, entry_price, trade_dir,
                         atr_entry, risk_distance, price_4h.index[pos], bar["close"],
                         "time", k)
        # 트레일 익스트림 갱신(다음 봉 판단용, 현재 봉 포함)
        if trade_dir == 1:
            extreme = max(extreme, bar["high"])
        else:
            extreme = min(extreme, bar["low"])
    return None


def run_variant(universe: dict, squeeze_entry_pctile: float = 0.20,
                 squeeze_exit_pctile: float = 0.70, trigger_window: int = 10,
                 top_k: int = 2, donchian_len: int = 15, atr_sl_mult: float = 1.5,
                 atr_trail_mult: float = 3.0, max_hold_days: int = 15,
                 rank_mode: str = "topk", shuffle_seed: int | None = None,
                 reverse: bool = False, disable_invalidation: bool = False,
                 invalidation_bars: int = 5) -> list[Trade]:
    calendar = cross_sectional_calendar(universe)
    cands = register_candidates(universe, calendar, squeeze_entry_pctile, top_k,
                                 rank_mode=rank_mode, shuffle_seed=shuffle_seed)
    triggers = find_triggers(universe, cands, trigger_window, squeeze_exit_pctile)
    signals = signal_direction(universe, triggers)
    trades = []
    for sym, reg_date, trig_date, direction in signals:
        tr = simulate_trade(universe, sym, trig_date, direction, reg_date,
                             atr_sl_mult, atr_trail_mult, max_hold_days,
                             invalidation_bars=invalidation_bars,
                             reverse=reverse, disable_invalidation=disable_invalidation)
        if tr is not None:
            trades.append(tr)
    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame(columns=["symbol", "reg_date", "trigger_date", "entry_time",
                                      "exit_time", "direction", "exit_reason", "hold_bars",
                                      "gross_R", "net_R"])
    rows = []
    for t in trades:
        rows.append({
            "symbol": t.symbol, "reg_date": t.reg_date, "trigger_date": t.trigger_date,
            "entry_time": t.entry_time, "exit_time": t.exit_time, "direction": t.direction,
            "exit_reason": t.exit_reason, "hold_bars": t.hold_bars,
            "gross_R": t.gross_R, "net_R": t.net_R,
        })
    df = pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
    return df


def split_is_oos(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    is_df = df[(df["entry_time"] >= IS_START) & (df["entry_time"] <= IS_END)]
    oos_df = df[(df["entry_time"] >= OOS_START) & (df["entry_time"] <= OOS_END)]
    full_df = df[(df["entry_time"] >= IS_START) & (df["entry_time"] <= OOS_END)]
    return is_df, oos_df, full_df


def pf_r(series: pd.Series) -> float:
    pos = series[series > 0].sum()
    neg = -series[series < 0].sum()
    if neg == 0:
        return float("inf") if pos > 0 else float("nan")
    return pos / neg


def t_stat(series: pd.Series) -> float:
    n = len(series)
    if n < 2:
        return float("nan")
    return series.mean() / (series.std(ddof=1) / np.sqrt(n))
