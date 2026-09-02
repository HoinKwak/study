"""자기상관·재포장 점검용 지표 — rho(lag-1 자기상관), Hurst(R/S), 분산비율(VR), ROC, 실현변동성.

전부 순수 numpy/pandas, 룩어헤드 없이 t 시점까지의 과거값만 사용(rolling, shift 기반).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view


def log_returns(close: pd.Series) -> pd.Series:
    return np.log(close / close.shift(1))


def rolling_lag1_autocorr(r: pd.Series, window: int) -> pd.Series:
    """rho(t) = 롤링 window 개의 r(t)와 r(t-1) 간 Pearson 상관계수."""
    return r.rolling(window).corr(r.shift(1))


def rolling_variance_ratio2(r: pd.Series, window: int) -> pd.Series:
    """Lo-MacKinlay 분산비율 VR(2) = Var(2기간 중첩수익률)/(2*Var(1기간 수익률)), 롤링 window."""
    var1 = r.rolling(window).var()
    r2 = r + r.shift(1)
    var2 = r2.rolling(window).var()
    return var2 / (2.0 * var1)


def rolling_hurst_rs(r: pd.Series, window: int = 60,
                     lags: tuple[int, ...] = (10, 12, 15, 20, 30, 60)) -> pd.Series:
    """롤링 R/S(Rescaled Range) 방식 Hurst 지수. window 를 lags 각각의 부분윈도로 나눠
    R/S(m) 평균을 구하고 log(R/S) vs log(m) 회귀 기울기 = H.

    lags 는 window 의 약수만 사용(재현 가능한 등분할). numpy stride-trick 으로 전 구간을
    한 번에 벡터화 계산(파이썬 루프로 봉마다 도는 것보다 수백 배 빠름).
    """
    lags = tuple(m for m in lags if window % m == 0 and m >= 4)
    vals = r.to_numpy(dtype=float)
    n = len(vals)
    out = np.full(n, np.nan)
    if n < window:
        return pd.Series(out, index=r.index)
    # windows[i] = vals[i-window+1 : i+1]  (i>=window-1)
    windows = sliding_window_view(vals, window)  # shape (n-window+1, window)
    valid_row = ~np.isnan(windows).any(axis=1)

    log_m = np.log(np.array(lags, dtype=float))
    rs_means = np.full((windows.shape[0], len(lags)), np.nan)
    for li, m in enumerate(lags):
        nchunk = window // m
        w = windows[:, : nchunk * m].reshape(windows.shape[0], nchunk, m)
        mean_c = w.mean(axis=2, keepdims=True)
        dev = w - mean_c
        cumdev = np.cumsum(dev, axis=2)
        R = cumdev.max(axis=2) - cumdev.min(axis=2)
        S = w.std(axis=2, ddof=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            RS = np.where(S > 0, R / S, np.nan)
        rs_means[:, li] = np.nanmean(RS, axis=1)

    log_rs = np.log(rs_means)
    x = log_m
    x_mean = x.mean()
    x_dev = x - x_mean
    denom = (x_dev ** 2).sum()
    y_mean = np.nanmean(log_rs, axis=1)
    y_dev = log_rs - y_mean[:, None]
    slope = np.nansum(x_dev[None, :] * y_dev, axis=1) / denom
    slope = np.where(np.isnan(log_rs).any(axis=1), np.nan, slope)
    slope = np.where(valid_row, slope, np.nan)

    out[window - 1:] = slope
    return pd.Series(out, index=r.index)


def rolling_roc(close: pd.Series, window: int) -> pd.Series:
    """단순 모멘텀 대조군: window 기간 수익률."""
    return close / close.shift(window) - 1.0


def rolling_realized_vol(r: pd.Series, window: int) -> pd.Series:
    return r.rolling(window).std()
