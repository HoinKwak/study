"""서브캔들(5m) 거래대금 균일성(CV) 기반 1h 신호 계산.

- 5m quote_volume 데이터를 1h 버킷(정시 정렬)으로 그룹핑, 정확히 12개 서브캔들이
  있는 그룹만 사용(부분 그룹 배제 — 스펙 명시 처리).
- 1h 봉의 OHLC 는 5m 데이터를 그대로 집계해 재구성한다(네이티브 1h 를 별도로 받아
  정합을 맞추는 대신, 신호가 참조하는 서브캔들과 완전히 같은 타임라인을 보장 —
  룩어헤드/정합 오류를 원천 차단하는 설계 선택).
- CV = std(quote_vol_12, ddof=0) / mean(quote_vol_12)
- dir = sign(close-open) (0이면 무신호로 취급)
- consist = 서브캔들 중 dir 과 같은 방향(sign(sub_close-sub_open)==dir) 비율
- pctile_cv: 과거 60일(1,440 시간봉) 롤링 백분위 — 현재 바는 제외(과거 window 만 사용,
  룩어헤드 방지). half_hour_qv_accel/scalp 스퀴즈필터와 동일 관례.
- range_atr = |close-open| / ATR(14,1h)
"""
from __future__ import annotations

import numpy as np
import pandas as pd

ROLL_DAYS = 60
ROLL_BARS = ROLL_DAYS * 24  # 1,440 (1h 봉 기준)


def build_hourly_from_5m(df5: pd.DataFrame) -> pd.DataFrame:
    """5m(OHLC+quote_volume) → 1h 서브캔들 그룹(완전한 12개 그룹만) 데이터프레임.

    반환 컬럼: open,high,low,close (1h 집계), cv, dir, consist.
    성능: groupby 를 Python 루프로 순회하지 않고 벡터화 집계로 계산(40만+행에서
    수 초→수십ms). 결과는 루프 버전과 동일(단위테스트로 대조 확인).
    """
    df = df5.copy()
    df["hour"] = df.index.floor("1h")
    g = df.groupby("hour", sort=True)

    counts = g.size()
    complete_hours = counts[counts == 12].index

    o = g["open"].first()
    c = g["close"].last()
    h = g["high"].max()
    l = g["low"].min()
    qv_mean = g["quote_volume"].mean()
    qv_std = g["quote_volume"].std(ddof=0)
    cv = qv_std / qv_mean.replace(0.0, np.nan)

    d = pd.Series(np.sign((c - o).to_numpy()), index=o.index).astype(int)

    # consist: 서브캔들 부호가 그 시간대 dir 과 일치하는 비율
    hour_dir = df["hour"].map(d)
    sub_sign = np.sign(df["close"].to_numpy(float) - df["open"].to_numpy(float))
    match = pd.Series(sub_sign, index=df.index) == hour_dir
    consist = match.groupby(df["hour"]).mean()

    hourly = pd.DataFrame({
        "open": o, "high": h, "low": l, "close": c, "cv": cv, "dir": d, "consist": consist,
    })
    hourly = hourly.loc[hourly.index.isin(complete_hours)].sort_index()
    hourly.loc[hourly["dir"] == 0, "consist"] = np.nan
    hourly.index.name = "hour"
    return hourly


def _atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    h, l, c = df["high"], df["low"], df["close"]
    prev_c = c.shift(1)
    tr = pd.concat([h - l, (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def compute_signal_frame(df5: pd.DataFrame, pctile_cv_th: float = 30.0,
                          consist_th_num: int = 8, consist_th_den: int = 12,
                          range_atr_th: float = 0.5, atr_period: int = 14,
                          roll_bars: int = ROLL_BARS,
                          cv_override: pd.Series | None = None) -> pd.DataFrame:
    """1h 신호 프레임 계산. cv_override 는 셔플 대조군용(cv 컬럼을 종목별로 무작위 치환한 값).

    모든 파생 컬럼은 "신호봉 자신의 정보"까지만 사용(각 바 시점에 확정 가능한 값). pctile_cv 는
    과거 window(현재 바 제외)로 계산해 룩어헤드를 방지.
    """
    hourly = build_hourly_from_5m(df5)
    if cv_override is not None:
        hourly["cv"] = cv_override.reindex(hourly.index).to_numpy()
    hourly["atr"] = _atr(hourly, atr_period)
    hourly["range_atr"] = (hourly["close"] - hourly["open"]).abs() / hourly["atr"]

    cv = hourly["cv"]
    n = len(hourly)
    pctile = np.full(n, np.nan)
    cv_arr = cv.to_numpy(float)
    for i in range(n):
        lo = max(0, i - roll_bars)
        window = cv_arr[lo:i]  # 현재 바(i) 제외, 과거만
        window = window[~np.isnan(window)]
        if len(window) < 100:  # 최소 표본(약 4일) 확보 전엔 무신호
            continue
        cur = cv_arr[i]
        if np.isnan(cur):
            continue
        pctile[i] = (window <= cur).mean() * 100.0
    hourly["pctile_cv"] = pctile

    consist_th = consist_th_num / consist_th_den
    cond_cv = hourly["pctile_cv"] <= pctile_cv_th
    cond_consist = hourly["consist"] >= consist_th - 1e-9
    cond_range = hourly["range_atr"] >= range_atr_th

    combined = cond_cv & cond_consist & cond_range
    hourly["long_trigger"] = combined & (hourly["dir"] == 1)
    hourly["short_trigger"] = combined & (hourly["dir"] == -1)
    return hourly


def donchian_breakout_frame(df15: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """게이트 없음 대조군 — 순수 15m Donchian(20) 브레이크아웃 신호(폐기조건 ①).

    직전 lookback 개 15m 봉(현재봉 제외)의 고가/저가 돌파.
    """
    df = df15.copy()
    prior_high = df["high"].shift(1).rolling(lookback).max()
    prior_low = df["low"].shift(1).rolling(lookback).min()
    df["long_trigger"] = df["close"] > prior_high
    df["short_trigger"] = df["close"] < prior_low
    return df
