"""BTC 펀딩ΔF ApEn 레짐 + BTC 추세방향 + 동어반복 점검용 대조 지표 일체.

전부 causal(각 시점에 그 시점까지의 정보만 사용) — 룩어헤드 점검은 diag_lookahead.py 에서 별도 확인.
"""
from __future__ import annotations

import bisect

import numpy as np
import pandas as pd

from apen import rolling_apen
from common import load_funding_btc, load_klines_4h, ema_pair, atr14_4h, adx14_4h


def apen_pctile_series(apen: pd.Series, window_days: int = 90) -> pd.Series:
    """트레일링 `window_days`일 창 내에서 apen 값의 백분위(0~100). 자기 자신 포함, causal.

    포인터 기반 O(N log N)(정렬 리스트에 bisect) — pandas rolling().rank(pct=True) 의
    min_periods 함정(다른 스펙에서 이력 18.9% 소실을 낸 바로 그 버그)을 원천 회피하기 위해
    직접 구현한다.
    """
    idx = apen.index
    vals = apen.to_numpy()
    n = len(vals)
    out = np.full(n, np.nan)
    win = pd.Timedelta(days=window_days)
    sorted_vals: list[float] = []
    left = 0
    for i in range(n):
        if not np.isfinite(vals[i]):
            continue
        # 윈도우 시작 포인터 전진(오래된 값 제거)
        cutoff = idx[i] - win
        while left < i:
            if idx[left] >= cutoff:
                break
            if np.isfinite(vals[left]):
                pos = bisect.bisect_left(sorted_vals, vals[left])
                sorted_vals.pop(pos)
            left += 1
        pos_ins = bisect.bisect_left(sorted_vals, vals[i])
        bisect.insort(sorted_vals, vals[i])
        cnt_le = bisect.bisect_right(sorted_vals, vals[i])
        out[i] = 100.0 * cnt_le / len(sorted_vals)
    return pd.Series(out, index=idx)


def build_btc_apen(apen_window: int = 30, apen_m: int = 2, apen_r_mult: float = 0.2,
                    pctile_window_days: int = 90) -> dict:
    funding_8h, excluded_frac = load_funding_btc()
    delta = funding_8h["rate"].diff()
    apen_arr = rolling_apen(delta.to_numpy(), window=apen_window, m=apen_m, r_mult=apen_r_mult)
    apen = pd.Series(apen_arr, index=delta.index)
    apen_pctile = apen_pctile_series(apen, window_days=pctile_window_days)
    return {"funding_8h": funding_8h, "delta": delta, "apen": apen, "apen_pctile": apen_pctile,
            "excluded_frac": excluded_frac}


def build_btc_price_regime(ema_fast: int = 20, ema_slow: int = 50, atr_period: int = 14):
    price = load_klines_4h("BTCUSDT")
    ema = ema_pair(price, ema_fast, ema_slow)
    atr = atr14_4h(price, atr_period)
    adx, plus_di, minus_di = adx14_4h(price, atr_period)
    # 동어반복 점검용 추가 대조지표
    log_ret = np.log(price["close"]).diff()
    rv20 = log_ret.rolling(20).std()  # 실현변동성(20봉)
    ema_slope = (ema["ema_fast"] - ema["ema_slow"]) / price["close"]  # EMA 괴리율(추세강도 프록시)
    return {"price": price, "ema": ema, "atr": atr, "adx": adx, "rv20": rv20,
            "ema_slope": ema_slope}


def map_settlement_to_bars(settlement_series: pd.Series, bar_index: pd.DatetimeIndex) -> pd.Series:
    """정산시각 인덱스의 시리즈를 4h 봉 인덱스에 backward asof 매핑(과거 정산값만 사용, causal)."""
    s = settlement_series.dropna().sort_index()
    if len(s) == 0:
        return pd.Series(np.nan, index=bar_index)
    left = pd.DataFrame({"t": bar_index})
    right = pd.DataFrame({"t": s.index, "v": s.values})
    out = pd.merge_asof(left, right, on="t", direction="backward")
    out = out.set_index("t")["v"]
    out.index.name = None
    return out
