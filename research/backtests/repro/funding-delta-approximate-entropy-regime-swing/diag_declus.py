"""De-clustering — 캘린더일 단위 + 3~5일 롤링 클러스터. gross/net 둘 다."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import pf_r, t_stat, split_is_oos
from events import build_universe
from engine import run_variant, trades_to_df


def calendar_day_groups(df: pd.DataFrame, col: str) -> pd.Series:
    g = df.groupby(df["entry_time"].dt.date)[col].mean()
    return g


def rolling_cluster_ids(entry_times: pd.Series, days: int) -> np.ndarray:
    ids = np.zeros(len(entry_times), dtype=int)
    cluster_start = None
    cur_id = -1
    for i, t in enumerate(entry_times):
        if cluster_start is None or (t - cluster_start).days >= days:
            cur_id += 1
            cluster_start = t
        ids[i] = cur_id
    return ids


def rolling_cluster_groups(df: pd.DataFrame, col: str, days: int) -> pd.Series:
    d = df.sort_values("entry_time").reset_index(drop=True)
    d["cid"] = rolling_cluster_ids(d["entry_time"], days)
    return d.groupby("cid")[col].mean()


def summarize(df: pd.DataFrame, label: str) -> dict:
    out = {}
    for col in ["gross_R", "net_R"]:
        cal = calendar_day_groups(df, col)
        r3 = rolling_cluster_groups(df, col, 3)
        r5 = rolling_cluster_groups(df, col, 5)
        out[col] = {
            "trade_level": {"n": len(df), "pf": pf_r(df[col]), "t": t_stat(df[col])},
            "calendar_day": {"n": len(cal), "pf": pf_r(cal), "t": t_stat(cal)},
            "roll3d": {"n": len(r3), "pf": pf_r(r3), "t": t_stat(r3)},
            "roll5d": {"n": len(r5), "pf": pf_r(r5), "t": t_stat(r5)},
        }
    return {label: out}


def main() -> dict:
    uni = build_universe()
    trades = trades_to_df(run_variant(uni))
    is_df, oos_df, full_df = split_is_oos(trades)
    result = {}
    result.update(summarize(oos_df, "OOS"))
    result.update(summarize(is_df, "IS"))
    result.update(summarize(full_df, "FULL"))
    print(json.dumps(result, indent=2, default=float))
    return result


if __name__ == "__main__":
    main()
