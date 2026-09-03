"""통계 진단 유틸 — PF(R), t검정, 부트스트랩, de-clustering, 승률고정 순열검정.
(기존 universe-quote-volume-rank-churn-regime-btc-breakout-scalp/stats_utils.py 와 동일 로직,
컬럼명(net_R/gross_R)만 이 리포트의 engine.trades_to_df 출력에 맞춤)"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sstats

import common


def split_is_oos(df: pd.DataFrame, time_col: str = "entry_time"
                  ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    is_df = df[(df[time_col] >= common.IS_START) & (df[time_col] <= common.IS_END)]
    oos_df = df[(df[time_col] >= common.OOS_START) & (df[time_col] <= common.OOS_END)]
    full_df = df[(df[time_col] >= common.IS_START) & (df[time_col] <= common.OOS_END)]
    return is_df, oos_df, full_df


def pf_r(df: pd.DataFrame, col: str = "net_R") -> float:
    if df.empty:
        return float("nan")
    wins = df.loc[df[col] > 0, col].sum()
    losses = -df.loc[df[col] < 0, col].sum()
    return wins / losses if losses > 0 else float("inf")


def t_stat(df: pd.DataFrame, col: str = "net_R") -> tuple[float, float, int]:
    r = df[col].dropna().to_numpy()
    n = len(r)
    if n < 2:
        return float("nan"), float("nan"), n
    t, p = sstats.ttest_1samp(r, 0.0)
    return float(t), float(p), n


def summary(df: pd.DataFrame, label: str, col: str = "net_R") -> dict:
    t, p, n = t_stat(df, col)
    win_rate = (df[col] > 0).mean() * 100 if len(df) else float("nan")
    return dict(label=label, n=n, pf_r=pf_r(df, col),
               mean_r=df[col].mean() if len(df) else float("nan"),
               t=t, p=p, win_rate=win_rate, sum_r=df[col].sum() if len(df) else 0.0)


def print_summary(d: dict) -> str:
    return (f"{d['label']:34s} n={d['n']:5d} PF(R)={d['pf_r']:.3f} mean(R)={d['mean_r']:+.4f} "
           f"t={d['t']:+.3f} p={d['p']:.4f} win%={d['win_rate']:.1f}")


# --------------------------------------------------------- de-clustering

def decluster_calendar_day(df: pd.DataFrame, col: str = "net_R") -> pd.DataFrame:
    if df.empty:
        return df
    d = df.copy()
    d["cal_day"] = d["entry_time"].dt.floor("D")
    agg = d.groupby("cal_day").agg(**{col: (col, "mean")}, n=(col, "size")).reset_index()
    agg["entry_time"] = agg["cal_day"]
    return agg


def decluster_rolling_days(df: pd.DataFrame, window_days: int = 4, col: str = "net_R") -> pd.DataFrame:
    if df.empty:
        return df
    d = df.sort_values("entry_time").reset_index(drop=True)
    cluster_id = []
    cur_id = 0
    last_time = None
    for t in d["entry_time"]:
        if last_time is None or (t - last_time) > pd.Timedelta(days=window_days):
            cur_id += 1
        cluster_id.append(cur_id)
        last_time = t
    d["cluster"] = cluster_id
    agg = d.groupby("cluster").agg(**{col: (col, "mean")}, n=(col, "size"),
                                   entry_time=("entry_time", "first")).reset_index(drop=True)
    return agg


# --------------------------------------------------------- 부트스트랩

def bootstrap_diff_test(r_a: np.ndarray, r_b: np.ndarray, n_boot: int = 5000, seed: int = 42) -> dict:
    rng = np.random.default_rng(seed)
    na, nb = len(r_a), len(r_b)
    if na == 0 or nb == 0:
        return dict(mean_a=float("nan"), mean_b=float("nan"), diff=float("nan"), p_a_better=float("nan"))
    diffs = np.empty(n_boot)
    for i in range(n_boot):
        sa = rng.choice(r_a, size=na, replace=True)
        sb = rng.choice(r_b, size=nb, replace=True)
        diffs[i] = sa.mean() - sb.mean()
    obs_diff = r_a.mean() - r_b.mean()
    p_not_better = float((diffs <= 0).mean())
    return dict(mean_a=float(r_a.mean()), mean_b=float(r_b.mean()), diff=float(obs_diff),
               p_a_better=p_not_better, n_boot=n_boot)


def bootstrap_matched_n_diff(pool_r: np.ndarray, base_r: np.ndarray, n_boot: int = 5000,
                             seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    n = len(base_r)
    if n == 0 or len(pool_r) == 0:
        return dict(pctile=float("nan"), base_mean=float("nan"), pool_dist_mean=float("nan"))
    means = np.empty(n_boot)
    for i in range(n_boot):
        s = rng.choice(pool_r, size=n, replace=True)
        means[i] = s.mean()
    base_mean = base_r.mean()
    pctile = float((means <= base_mean).mean() * 100)
    return dict(pctile=pctile, base_mean=float(base_mean), pool_dist_mean=float(means.mean()),
               n=n, n_boot=n_boot)


def welch_independent(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    if len(a) < 2 or len(b) < 2:
        return float("nan"), float("nan")
    t, p = sstats.ttest_ind(a, b, equal_var=False)
    return float(t), float(p)


# --------------------------------------------------------- 순열검정

def sign_randomization_test(r: np.ndarray, n_perm: int = 100, seed: int = 11) -> dict:
    rng = np.random.default_rng(seed)
    n = len(r)
    obs = r.mean()
    signs = rng.choice([-1.0, 1.0], size=(n_perm, n))
    perm_means = (np.abs(r)[None, :] * signs).mean(axis=1)
    pctile = float((perm_means <= obs).mean() * 100)
    return dict(obs_mean=float(obs), pctile=pctile, n_perm=n_perm)


def win_rate_fixed_permutation_test(r: np.ndarray, n_perm: int = 100, seed: int = 13) -> dict:
    rng = np.random.default_rng(seed)
    n = len(r)
    win_count = int((r > 0).sum())
    pool = np.abs(r)
    obs = r.mean()
    perm_means = np.empty(n_perm)
    idx = np.arange(n)
    for i in range(n_perm):
        rng.shuffle(idx)
        win_idx = idx[:win_count]
        perm_sum = 2.0 * pool[win_idx].sum() - pool.sum()
        perm_means[i] = perm_sum / n
    pctile = float((perm_means <= obs).mean() * 100)
    return dict(obs_mean=float(obs), pctile=pctile, n_perm=n_perm, win_rate=float(win_count / n))
