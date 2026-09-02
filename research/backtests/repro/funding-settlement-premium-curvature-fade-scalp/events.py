"""정산 이벤트 구성 — 곡률계수 c(2차 회귀) 벡터화 계산.

매 8h 윈도우(기본 00/08/16 UTC 앵커, anchor_offset_hours 로 이동 가능)마다:
  - 윈도우 시작(t0)부터 check_offset_min 분 전(체크포인트, causal)까지의 1분 프리미엄
    종가 n_bars=window_min-check_offset_min 개에 대해 2차 OLS(quadratic, τ∈[0,1] 정규화)를
    적합해 곡률계수 c 를 구한다.
  - c_z = (c - 과거 lookback 회 c 평균) / 표준편차 (causal, 현재 이벤트 제외 = shift(1)).

같은 길이(n_bars)의 모든 윈도우는 동일한 τ 그리드를 쓰므로, 2차 계수의 최소자승 가중치
벡터를 1회만 구해 전체 이벤트에 대해 행렬곱(사실상 내적)으로 처리 — np.polyfit 대비
수천 배 빠르고 수치적으로 완전히 동일(아래 자체 검증 참조).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _quad_c2_weights(n: int) -> np.ndarray:
    """길이 n 고정 τ 그리드(0..1 균등)에서 2차 OLS 의 τ² 계수(c2)를 y 에 대한 선형결합으로
    표현하는 가중치 벡터(길이 n). c2 = weights @ y."""
    tau = np.linspace(0.0, 1.0, n)
    X = np.column_stack([tau ** 2, tau, np.ones(n)])
    pinv = np.linalg.pinv(X)   # 3 x n
    return pinv[0]             # τ² 계수(c2) 행


def build_events(prem_1m: pd.Series, anchor_offset_hours: int = 0,
                  check_offset_min: int = 60, window_min: int = 480,
                  lookback: int = 60) -> pd.DataFrame:
    """prem_1m: DatetimeIndex(ns, UTC) 1분 프리미엄 종가 Series.
    반환: t0, checkpoint_time, settlement_time, c, c_z, checkpoint_premium 컬럼의 DataFrame
    (이벤트는 t0 오름차순, 60회 warmup 이전 c_z=NaN)."""
    if len(prem_1m) == 0:
        return pd.DataFrame(columns=["t0", "checkpoint_time", "settlement_time",
                                     "c", "c_z", "checkpoint_premium"])
    n_bars = window_min - check_offset_min
    idx0 = prem_1m.index.min().floor("D")
    idx1 = prem_1m.index.max()
    grid = pd.date_range(idx0, idx1 + pd.Timedelta(hours=8), freq="8h", tz="UTC")
    grid = grid + pd.Timedelta(hours=anchor_offset_hours)
    grid = grid[(grid >= idx0) & (grid + pd.Timedelta(minutes=window_min) <= idx1
                                   + pd.Timedelta(minutes=1))]

    values = prem_1m.to_numpy(dtype=float)
    ts_ns = prem_1m.index.values.astype("datetime64[ns]").astype(np.int64)
    minute_ns = np.int64(60_000_000_000)

    w = _quad_c2_weights(n_bars)
    rows = []
    for t0 in grid:
        t0_ns = np.int64(t0.value)
        want_ns = t0_ns + np.arange(n_bars, dtype=np.int64) * minute_ns
        pos = np.searchsorted(ts_ns, want_ns)
        if pos.max(initial=0) >= len(ts_ns):
            continue
        ok = (pos < len(ts_ns)) & (ts_ns[np.clip(pos, 0, len(ts_ns) - 1)] == want_ns)
        if not ok.all():
            continue  # 결측(갭) 윈도우는 스킵
        y = values[pos]
        if not np.all(np.isfinite(y)):
            continue
        c2 = float(w @ y)
        checkpoint_premium = float(y[-1])
        checkpoint_time = t0 + pd.Timedelta(minutes=n_bars)
        settlement_time = t0 + pd.Timedelta(minutes=window_min)
        rows.append((t0, checkpoint_time, settlement_time, c2, checkpoint_premium))

    if not rows:
        return pd.DataFrame(columns=["t0", "checkpoint_time", "settlement_time",
                                     "c", "c_z", "checkpoint_premium"])
    df = pd.DataFrame(rows, columns=["t0", "checkpoint_time", "settlement_time",
                                     "c", "checkpoint_premium"])
    df = df.sort_values("t0").reset_index(drop=True)
    roll_mean = df["c"].shift(1).rolling(lookback, min_periods=lookback).mean()
    roll_std = df["c"].shift(1).rolling(lookback, min_periods=lookback).std(ddof=1)
    df["c_z"] = (df["c"] - roll_mean) / roll_std
    return df


def causal_zscore(series: pd.Series, lookback: int = 60) -> pd.Series:
    """이벤트 시퀀스(시간순 정렬)에 대해 과거 lookback 개(현재 제외, shift(1))로
    평균/표준편차를 구해 z-score. build_events 의 c_z 산출과 동일한 방법."""
    roll_mean = series.shift(1).rolling(lookback, min_periods=lookback).mean()
    roll_std = series.shift(1).rolling(lookback, min_periods=lookback).std(ddof=1)
    return (series - roll_mean) / roll_std


if __name__ == "__main__":
    # 자체검증: _quad_c2_weights 가 np.polyfit(deg=2) 과 동일 결과를 내는지 확인.
    rng = np.random.default_rng(0)
    for n in (60, 120, 420):
        tau = np.linspace(0, 1, n)
        y = rng.normal(size=n) + 3.0 * tau ** 2 - 1.5 * tau
        c2_poly = np.polyfit(tau, y, deg=2)[0]
        c2_w = _quad_c2_weights(n) @ y
        assert abs(c2_poly - c2_w) < 1e-9, (n, c2_poly, c2_w)
    print("quad weight vector matches np.polyfit(deg=2) — OK")
