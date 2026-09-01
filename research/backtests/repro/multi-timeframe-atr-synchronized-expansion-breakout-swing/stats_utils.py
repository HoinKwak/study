"""통계 진단 유틸 — PF(R), t검정, 부트스트랩, de-clustering, 셔플. (기존 oi-bipower repro 패턴을 계승)"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sstats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine


def trades_df(trades: list[engine.TradeRec], rcol: str = "r_net") -> pd.DataFrame:
    rows = []
    for t in trades:
        rows.append(dict(symbol=t.symbol, direction=t.direction, orig_direction=t.orig_direction,
                         entry_time=t.entry_time, exit_time=t.exit_time, entry_idx=t.entry_idx,
                         exit_idx=t.exit_idx, r_gross=t.r_gross, r_net=t.r_net, reason=t.reason,
                         holding_bars=t.holding_bars))
    cols = ["symbol", "direction", "orig_direction", "entry_time", "exit_time", "entry_idx",
            "exit_idx", "r_gross", "r_net", "reason", "holding_bars"]
    if not rows:
        d = pd.DataFrame(columns=cols)
    else:
        d = pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
    d["r"] = d[rcol] if len(d) else pd.Series(dtype=float)
    return d


def split_is_oos(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    is_df = df[(df["entry_time"] >= common.IS_START) & (df["entry_time"] <= common.IS_END)]
    oos_df = df[(df["entry_time"] >= common.OOS_START) & (df["entry_time"] <= common.OOS_END)]
    full_df = df[(df["entry_time"] >= common.IS_START) & (df["entry_time"] <= common.OOS_END)]
    return is_df, oos_df, full_df


def pf_r(df: pd.DataFrame) -> float:
    if df.empty:
        return float("nan")
    wins = df.loc[df["r"] > 0, "r"].sum()
    losses = -df.loc[df["r"] < 0, "r"].sum()
    return wins / losses if losses > 0 else float("inf")


def t_stat(df: pd.DataFrame) -> tuple[float, float, int]:
    r = df["r"].dropna().to_numpy()
    n = len(r)
    if n < 2:
        return float("nan"), float("nan"), n
    t, p = sstats.ttest_1samp(r, 0.0)
    return float(t), float(p), n


def summary(df: pd.DataFrame, label: str) -> dict:
    t, p, n = t_stat(df)
    win_rate = (df["r"] > 0).mean() * 100 if len(df) else float("nan")
    return dict(label=label, n=n, pf_r=pf_r(df),
               mean_r=df["r"].mean() if len(df) else float("nan"),
               t=t, p=p, win_rate=win_rate, sum_r=df["r"].sum() if len(df) else 0.0)


def fmt(d: dict) -> str:
    return (f"{d['label']:30s} n={d['n']:5d} PF(R)={d['pf_r']:.3f} mean(R)={d['mean_r']:+.4f} "
           f"t={d['t']:+.3f} p={d['p']:.4f} win%={d['win_rate']:.1f}")


# --------------------------------------------------------- de-clustering

def decluster_calendar_day(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    d = df.copy()
    d["cal_day"] = d["entry_time"].dt.floor("D")
    agg = d.groupby("cal_day").agg(r=("r", "mean"), n=("r", "size")).reset_index()
    agg["entry_time"] = agg["cal_day"]
    return agg


def decluster_rolling_days(df: pd.DataFrame, window_days: int = 4) -> pd.DataFrame:
    """전 종목 통합 entry_time 기준 그리디 순차 병합(직전 대표시각으로부터 window_days 이내면 동일
    클러스터). 여러 종목이 같은 매크로 사건에 동시 반응해 며칠씩 어긋나며 몰리는 패턴을 잡기 위함."""
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
    agg = d.groupby("cluster").agg(r=("r", "mean"), n=("r", "size"),
                                   entry_time=("entry_time", "first")).reset_index(drop=True)
    return agg


# --------------------------------------------------------- 부트스트랩

def bootstrap_matched_n_diff(pool_r: np.ndarray, base_r: np.ndarray, n_boot: int = 5000,
                             seed: int = 7) -> dict:
    """표본수 맞춘 부트스트랩: pool 에서 base 와 같은 크기로 리샘플링해 mean(R) 분포 생성,
    base 의 실측 mean(R) 이 그 분포에서 차지하는 백분위."""
    rng = np.random.default_rng(seed)
    n = len(base_r)
    if n == 0 or len(pool_r) == 0:
        return dict(pctile=float("nan"), base_mean=float("nan"), pool_dist_mean=float("nan"), n=n)
    means = np.empty(n_boot)
    for i in range(n_boot):
        s = rng.choice(pool_r, size=n, replace=True)
        means[i] = s.mean()
    base_mean = base_r.mean()
    pctile = float((means <= base_mean).mean() * 100)
    return dict(pctile=pctile, base_mean=float(base_mean), pool_dist_mean=float(means.mean()),
               n=n, n_boot=n_boot)


def bootstrap_diff_indep(r_a: np.ndarray, r_b: np.ndarray, n_boot: int = 5000, seed: int = 11
                         ) -> dict:
    """두 독립표본 평균 R 차이의 부트스트랩(표본수 각자 유지). p_a_le_b = P(mean(A_boot)<=mean(B_boot))."""
    rng = np.random.default_rng(seed)
    na, nb = len(r_a), len(r_b)
    if na == 0 or nb == 0:
        return dict(p_a_le_b=float("nan"))
    cnt = 0
    for _ in range(n_boot):
        sa = rng.choice(r_a, size=na, replace=True)
        sb = rng.choice(r_b, size=nb, replace=True)
        if sa.mean() <= sb.mean():
            cnt += 1
    return dict(mean_a=float(r_a.mean()), mean_b=float(r_b.mean()), p_a_le_b=cnt / n_boot,
               n_boot=n_boot)


# --------------------------------------------------------- 셔플(부호 무작위화)

def sign_shuffle_test(df: pd.DataFrame, n_shuffle: int = 100, seed: int = 3) -> dict:
    """표본수 불변, 각 트레이드의 방향(부호)만 50/50 무작위 재배정해 100회 재계산한 mean(R) 분포에서
    실제 mean(R) 의 백분위를 구한다. R 계산은 이미 방향 반영된 값이므로, '부호 무작위화'는
    각 트레이드의 raw 손익 크기(|R|)는 유지한 채 방향성 정보가 실제로 도움이 됐는지를 검정한다
    (즉 |R_i| 는 고정하고 부호만 50/50 무작위 배정)."""
    if df.empty:
        return dict(pctile=float("nan"))
    r = df["r"].to_numpy()
    abs_r = np.abs(r)
    rng = np.random.default_rng(seed)
    means = np.empty(n_shuffle)
    for i in range(n_shuffle):
        signs = rng.choice([-1.0, 1.0], size=len(r))
        means[i] = (abs_r * signs).mean()
    real_mean = r.mean()
    pctile = float((means <= real_mean).mean() * 100)
    return dict(pctile=pctile, real_mean=float(real_mean), shuffle_mean=float(means.mean()),
               n_shuffle=n_shuffle)
