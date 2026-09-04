"""통계 진단 유틸 — PF(R), t검정, 부트스트랩, de-clustering. (oi-price-regression 선례 재사용/개작)"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sstats

import common
import engine


def trades_df(trades: list[engine.TradeRec]) -> pd.DataFrame:
    rows = []
    for t in trades:
        rows.append(dict(symbol=t.symbol, direction=t.direction, origin_side=t.origin_side,
                         signal_source=t.signal_source, reverse=t.reverse,
                         entry_time=t.entry_time, exit_time=t.exit_time,
                         entry_idx=t.entry_idx, exit_idx=t.exit_idx, pnl=t.pnl, r=t.r_multiple,
                         reason=t.reason, holding_bars=t.holding_bars, risk_amount=t.risk_amount,
                         z_at_signal=t.z_at_signal))
    if not rows:
        return pd.DataFrame(columns=["symbol", "direction", "origin_side", "signal_source",
                                     "reverse", "entry_time", "exit_time", "entry_idx", "exit_idx",
                                     "pnl", "r", "reason", "holding_bars", "risk_amount",
                                     "z_at_signal"])
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
    r = df["r"].dropna().to_numpy()
    n = len(r)
    if n < 2:
        return float("nan"), float("nan"), n
    t, p = sstats.ttest_1samp(r, 0.0)
    return float(t), float(p), n


def max_drawdown_r(df: pd.DataFrame) -> float:
    """R-배수 누적합 기준 MDD(자기자본 등가중, 복리 미반영)."""
    if df.empty:
        return float("nan")
    d = df.sort_values("entry_time")
    cum = d["r"].cumsum()
    peak = cum.cummax()
    dd = cum - peak
    return float(dd.min())


def summary(df: pd.DataFrame, label: str) -> dict:
    t, p, n = t_stat(df)
    win_rate = (df["r"] > 0).mean() * 100 if len(df) else float("nan")
    return dict(label=label, n=n, pf_r=pf_r(df), mean_r=df["r"].mean() if len(df) else float("nan"),
               t=t, p=p, win_rate=win_rate, sum_r=df["r"].sum() if len(df) else 0.0,
               mdd_r=max_drawdown_r(df))


def print_summary(d: dict) -> str:
    return (f"{d['label']:34s} n={d['n']:5d} PF(R)={d['pf_r']:.3f} mean(R)={d['mean_r']:+.4f} "
           f"t={d['t']:+.3f} p={d['p']:.4f} win%={d['win_rate']:.1f} MDD(R)={d['mdd_r']:.2f}")


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
    """3~5일 롤링 윈도우 de-clustering: 같은 종목 여부 무관하게, 진입시각이 window_days 이내로
    이어지는 트레이드를 하나의 클러스터로 묶어 클러스터 평균 R 을 표본으로 삼는다."""
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


def sign_shuffle_test(r: np.ndarray, n_rep: int = 100, seed: int = 123) -> dict:
    rng = np.random.default_rng(seed)
    n = len(r)
    if n == 0:
        return dict(pctile=float("nan"), actual_mean=float("nan"))
    means = np.empty(n_rep)
    for i in range(n_rep):
        flip = rng.integers(0, 2, size=n) * 2 - 1
        means[i] = (r * flip).mean()
    actual = r.mean()
    pctile = float((means <= actual).mean() * 100)
    return dict(pctile=pctile, actual_mean=float(actual), shuffle_mean=float(means.mean()),
               shuffle_std=float(means.std()), n_rep=n_rep, n=n)
