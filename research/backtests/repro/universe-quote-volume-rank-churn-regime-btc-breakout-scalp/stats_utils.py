"""통계 진단 유틸 — PF(R), t검정, 부트스트랩, de-clustering, 승률고정 순열검정."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sstats

import common
import engine


def trades_df(trades: list[engine.TradeRec]) -> pd.DataFrame:
    rows = []
    for t in trades:
        rows.append(dict(symbol=t.symbol, direction=t.direction, orig_direction=t.orig_direction,
                         entry_time=t.entry_time, exit_time=t.exit_time, entry_idx=t.entry_idx,
                         exit_idx=t.exit_idx, pnl=t.pnl, r=t.r_multiple, reason=t.reason,
                         holding_bars=t.holding_bars, risk_amount=t.risk_amount))
    if not rows:
        return pd.DataFrame(columns=["symbol", "direction", "orig_direction", "entry_time",
                                     "exit_time", "entry_idx", "exit_idx", "pnl", "r", "reason",
                                     "holding_bars", "risk_amount"])
    d = pd.DataFrame(rows)
    return d.sort_values("entry_time").reset_index(drop=True)


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
    """단일표본 t검정: H0: mean(R)=0. 반환 (t, p, n)."""
    r = df["r"].dropna().to_numpy()
    n = len(r)
    if n < 2:
        return float("nan"), float("nan"), n
    t, p = sstats.ttest_1samp(r, 0.0)
    return float(t), float(p), n


def summary(df: pd.DataFrame, label: str) -> dict:
    t, p, n = t_stat(df)
    win_rate = (df["r"] > 0).mean() * 100 if len(df) else float("nan")
    return dict(label=label, n=n, pf_r=pf_r(df), mean_r=df["r"].mean() if len(df) else float("nan"),
               t=t, p=p, win_rate=win_rate, sum_r=df["r"].sum() if len(df) else 0.0)


def print_summary(d: dict) -> str:
    return (f"{d['label']:30s} n={d['n']:5d} PF(R)={d['pf_r']:.3f} mean(R)={d['mean_r']:+.4f} "
           f"t={d['t']:+.3f} p={d['p']:.4f} win%={d['win_rate']:.1f}")


# --------------------------------------------------------- de-clustering

def decluster_calendar_day(df: pd.DataFrame) -> pd.DataFrame:
    """캘린더일 단위 de-clustering: 같은 UTC 날짜에 여러 트레이드 진입 시 하루 대표 1건(평균 R)으로 축약."""
    if df.empty:
        return df
    d = df.copy()
    d["cal_day"] = d["entry_time"].dt.floor("D")
    agg = d.groupby("cal_day").agg(r=("r", "mean"), n=("r", "size")).reset_index()
    agg["entry_time"] = agg["cal_day"]
    return agg


def decluster_rolling_days(df: pd.DataFrame, window_days: int = 4) -> pd.DataFrame:
    """3~5일 롤링 윈도우 de-clustering: entry_time 정렬 후, 이전 대표 트레이드로부터
    window_days 이내 진입한 트레이드를 같은 클러스터로 묶어 평균 R 로 축약(그리디 순차 병합)."""
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

def bootstrap_diff_test(r_a: np.ndarray, r_b: np.ndarray, n_boot: int = 5000, seed: int = 42
                        ) -> dict:
    """두 독립표본(A vs B) 평균 R 차이의 부트스트랩 검정."""
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
    """표본수 맞춘 부트스트랩: pool(대조군, 더 큰 표본)에서 base 와 같은 크기로 반복 리샘플링해
    mean(R) 분포를 만들고, base 의 mean(R) 이 그 분포에서 어느 백분위인지 계산."""
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


# --------------------------------------------------------- 순열검정

def sign_randomization_test(r: np.ndarray, n_perm: int = 2000, seed: int = 11) -> dict:
    """부호 무작위화(50/50): 각 트레이드 R 부호를 독립적으로 뒤집어 mean(R) 귀무분포 생성.
    ⚠️ 승률<50% 인 표본에서는 이 검정의 극단 백분위가 산술적 귀결일 수 있음(암묵적 귀무가설이
    승률 50%) — win_rate_fixed_permutation_test 를 병행할 것."""
    rng = np.random.default_rng(seed)
    n = len(r)
    obs = r.mean()
    signs = rng.choice([-1.0, 1.0], size=(n_perm, n))
    perm_means = (np.abs(r)[None, :] * signs).mean(axis=1)
    pctile = float((perm_means <= obs).mean() * 100)
    return dict(obs_mean=float(obs), pctile=pctile, n_perm=n_perm)


def win_rate_fixed_permutation_test(r: np.ndarray, n_perm: int = 2000, seed: int = 13) -> dict:
    """승률 고정 순열검정: 승리 트레이드 개수(win_count)는 실측 그대로 고정하되, |R| 크기 풀
    (승/패 전체) 에서 어느 트레이드가 '승리'로 배정되는지를 무작위 재배정해 mean(R) 귀무분포를
    만든다. 즉 "이길 때 실제로 더 크게 이기고, 질 때 더 작게 지는가"(승패 크기 비대칭)를
    승률 자체와 분리해 검정 — sign_randomization_test 의 '50% 암묵 귀무가설' 문제를 회피.
    (⚠️ 승/패 그룹 내부에서만 크기를 섞으면 그룹 합이 불변이라 순열이 항상 관측치와 같아지는
    자명한(degenerate) 검정이 된다 — 반드시 전체 |R| 풀에서 승리 슬롯을 재추첨해야 함.)"""
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
