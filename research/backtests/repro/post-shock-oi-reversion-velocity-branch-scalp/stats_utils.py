"""통계 진단 유틸 — PF(R), t검정, 부트스트랩, de-clustering."""
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


def pf_r(df: pd.DataFrame, col: str = "r_multiple") -> float:
    if df.empty:
        return float("nan")
    wins = df.loc[df[col] > 0, col].sum()
    losses = -df.loc[df[col] < 0, col].sum()
    return wins / losses if losses > 0 else float("inf")


def t_stat(df: pd.DataFrame, col: str = "r_multiple") -> tuple[float, float, int]:
    r = df[col].dropna().to_numpy()
    n = len(r)
    if n < 2:
        return float("nan"), float("nan"), n
    t, p = sstats.ttest_1samp(r, 0.0)
    return float(t), float(p), n


def summary(df: pd.DataFrame, label: str, col: str = "r_multiple") -> dict:
    t, p, n = t_stat(df, col)
    win_rate = (df[col] > 0).mean() * 100 if len(df) else float("nan")
    return dict(label=label, n=n, pf_r=pf_r(df, col), mean_r=df[col].mean() if len(df) else float("nan"),
               t=t, p=p, win_rate=win_rate, sum_r=df[col].sum() if len(df) else 0.0)


def print_summary(d: dict) -> str:
    return (f"{d['label']:34s} n={d['n']:5d} PF(R)={d['pf_r']:.3f} mean(R)={d['mean_r']:+.4f} "
           f"t={d['t']:+.3f} p={d['p']:.4f} win%={d['win_rate']:.1f}")


# --------------------------------------------------------- de-clustering

def decluster_calendar_day(df: pd.DataFrame, col: str = "r_multiple",
                            time_col: str = "entry_time") -> pd.DataFrame:
    if df.empty:
        return df
    d = df.copy()
    d["cal_day"] = d[time_col].dt.floor("D")
    agg = d.groupby("cal_day").agg(r_multiple=(col, "mean"), n=(col, "size")).reset_index()
    agg["entry_time"] = agg["cal_day"]
    return agg


def decluster_rolling_days(df: pd.DataFrame, window_days: int = 4, col: str = "r_multiple",
                            time_col: str = "entry_time") -> pd.DataFrame:
    if df.empty:
        return df
    d = df.sort_values(time_col).reset_index(drop=True)
    cluster_id = []
    cur_id = 0
    last_time = None
    for t in d[time_col]:
        if last_time is None or (t - last_time) > pd.Timedelta(days=window_days):
            cur_id += 1
        cluster_id.append(cur_id)
        last_time = t
    d["cluster"] = cluster_id
    agg = d.groupby("cluster").agg(r_multiple=(col, "mean"), n=(col, "size"),
                                   entry_time=(time_col, "first")).reset_index(drop=True)
    return agg


# --------------------------------------------------------- 부트스트랩

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


def welch_test(a: np.ndarray, b: np.ndarray) -> dict:
    if len(a) < 2 or len(b) < 2:
        return dict(t=float("nan"), p=float("nan"), na=len(a), nb=len(b))
    t, p = sstats.ttest_ind(a, b, equal_var=False)
    return dict(t=float(t), p=float(p), na=len(a), nb=len(b), mean_a=float(np.mean(a)),
               mean_b=float(np.mean(b)))
