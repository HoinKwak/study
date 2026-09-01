"""통계 유틸 — PF(R), t검정, 부트스트랩(재현 가능 시드).

hash(str) 내장 시드 사용 금지 — hashlib 기반 결정적 시드만 사용.
"""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd
from scipy import stats


def seed_from_str(s: str) -> int:
    return int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)


def pf_r(r: np.ndarray) -> float:
    r = np.asarray(r, dtype=float)
    r = r[np.isfinite(r)]
    if len(r) == 0:
        return float("nan")
    gains = r[r > 0].sum()
    losses = -r[r < 0].sum()
    if losses <= 0:
        return float("inf") if gains > 0 else float("nan")
    return gains / losses


def summarize(r: np.ndarray, label: str = "") -> dict:
    r = np.asarray(r, dtype=float)
    r = r[np.isfinite(r)]
    n = len(r)
    if n == 0:
        return {"label": label, "n": 0}
    mean = r.mean()
    sd = r.std(ddof=1) if n > 1 else float("nan")
    se = sd / np.sqrt(n) if n > 1 else float("nan")
    t = mean / se if se and se > 0 else float("nan")
    p = 2 * (1 - stats.t.cdf(abs(t), df=n - 1)) if n > 1 and np.isfinite(t) else float("nan")
    win = (r > 0).mean()
    return {
        "label": label, "n": n, "pf_r": pf_r(r), "mean_r": mean, "sd_r": sd, "t": t, "p": p,
        "win_rate": win, "sum_r": r.sum(),
    }


def declustered_daily(df: pd.DataFrame, time_col: str = "entry_time", r_col: str = "r_multiple"
                      ) -> np.ndarray:
    """캘린더일 단위 de-clustering: 같은 날 여러 트레이드는 평균 R로 축약."""
    if df.empty:
        return np.array([])
    d = df.copy()
    d["cal_day"] = pd.to_datetime(d[time_col]).dt.tz_convert("UTC").dt.date
    g = d.groupby("cal_day")[r_col].mean()
    return g.to_numpy(float)


def bootstrap_diff_matched_n(sample_a: np.ndarray, sample_b: np.ndarray, n_match: int,
                             n_iter: int = 200, seed: int = 0) -> dict:
    """sample_b(대조군 풀)에서 n_match개를 복원추출해 sample_a(mean)와 비교하는 백분위 검정.

    반환: a_mean 이 b 리샘플 분포에서 몇 백분위인지(낮을수록 a가 열세).
    """
    rng = np.random.default_rng(seed)
    a = np.asarray(sample_a, dtype=float)
    a = a[np.isfinite(a)]
    b = np.asarray(sample_b, dtype=float)
    b = b[np.isfinite(b)]
    if len(a) == 0 or len(b) == 0:
        return {"a_mean": float("nan"), "percentile": float("nan"), "b_means": []}
    a_mean = a.mean()
    b_means = np.array([rng.choice(b, size=n_match, replace=True).mean() for _ in range(n_iter)])
    pct = float((b_means < a_mean).mean() * 100)
    return {"a_mean": a_mean, "percentile": pct, "b_means_mean": b_means.mean(),
           "b_means_std": b_means.std()}


def welch_t(a: np.ndarray, b: np.ndarray) -> dict:
    a = np.asarray(a, dtype=float)
    a = a[np.isfinite(a)]
    b = np.asarray(b, dtype=float)
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return {"t": float("nan"), "p": float("nan"), "na": len(a), "nb": len(b)}
    t, p = stats.ttest_ind(a, b, equal_var=False)
    return {"t": float(t), "p": float(p), "na": len(a), "nb": len(b),
           "mean_a": a.mean(), "mean_b": b.mean()}
