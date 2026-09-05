"""통계 진단 유틸 — PF(R), t검정, 부트스트랩, de-clustering. (oi-hhi 백테스트의 stats_utils.py 구조 재사용)"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sstats

import common
import engine


def trades_df(trades: list[engine.TradeRec]) -> pd.DataFrame:
    rows = []
    for t in trades:
        rows.append(dict(direction=t.direction, raw_direction=t.raw_direction, gate=t.gate,
                         signal_idx=t.signal_idx, entry_time=t.entry_time, exit_time=t.exit_time,
                         entry_idx=t.entry_idx, exit_idx=t.exit_idx, pnl=t.pnl, r=t.r_multiple,
                         reason=t.reason, holding_bars=t.holding_bars, risk_amount=t.risk_amount,
                         gate_metric=t.gate_metric_at_signal, fee_entry=t.fee_entry,
                         fee_exit=t.fee_exit))
    if not rows:
        return pd.DataFrame(columns=["direction", "raw_direction", "gate", "signal_idx",
                                     "entry_time", "exit_time", "entry_idx", "exit_idx", "pnl", "r",
                                     "reason", "holding_bars", "risk_amount", "gate_metric",
                                     "fee_entry", "fee_exit"])
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


def summary(df: pd.DataFrame, label: str) -> dict:
    t, p, n = t_stat(df)
    win_rate = (df["r"] > 0).mean() * 100 if len(df) else float("nan")
    return dict(label=label, n=n, pf_r=pf_r(df), mean_r=df["r"].mean() if len(df) else float("nan"),
               t=t, p=p, win_rate=win_rate, sum_r=df["r"].sum() if len(df) else 0.0)


def print_summary(d: dict) -> str:
    return (f"{d['label']:34s} n={d['n']:5d} PF(R)={d['pf_r']:.3f} mean(R)={d['mean_r']:+.4f} "
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


def independent_pair_diff(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict:
    key_a = set(df_a["entry_time"])
    key_b = set(df_b["entry_time"])
    overlap = key_a & key_b
    overlap_frac_a = len(overlap) / len(key_a) if key_a else float("nan")
    a_only = df_a[~df_a["entry_time"].isin(overlap)]
    b_only = df_b[~df_b["entry_time"].isin(overlap)]
    if len(a_only) >= 2 and len(b_only) >= 2:
        t, p = sstats.ttest_ind(a_only["r"], b_only["r"], equal_var=False)
    else:
        t, p = float("nan"), float("nan")
    return dict(overlap_n=len(overlap), overlap_frac_a=overlap_frac_a,
               a_only_n=len(a_only), b_only_n=len(b_only), welch_t=float(t), welch_p=float(p))


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


def winrate_fixed_shuffle_test(r: np.ndarray, n_rep: int = 100, seed: int = 321) -> dict:
    """승률 고정 대안 검정: 실제 승률로 무작위 이진 성패열을 생성해 승 R풀·패 R풀에서 복원추출."""
    rng = np.random.default_rng(seed)
    n = len(r)
    if n == 0:
        return dict(pctile=float("nan"), actual_mean=float("nan"))
    win_r = r[r > 0]
    loss_r = r[r <= 0]
    p_win = len(win_r) / n
    means = np.empty(n_rep)
    for i in range(n_rep):
        is_win = rng.random(n) < p_win
        sample = np.empty(n)
        n_win = is_win.sum()
        n_loss = n - n_win
        if n_win > 0 and len(win_r) > 0:
            sample[is_win] = rng.choice(win_r, size=n_win, replace=True)
        elif n_win > 0:
            sample[is_win] = 0.0
        if n_loss > 0 and len(loss_r) > 0:
            sample[~is_win] = rng.choice(loss_r, size=n_loss, replace=True)
        elif n_loss > 0:
            sample[~is_win] = 0.0
        means[i] = sample.mean()
    actual = r.mean()
    pctile = float((means <= actual).mean() * 100)
    return dict(pctile=pctile, actual_mean=float(actual), shuffle_mean=float(means.mean()),
               shuffle_std=float(means.std()), n_rep=n_rep, n=n, p_win=p_win)
