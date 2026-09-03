"""de-clustering — 캘린더일 단위 + 3~5일 롤링 윈도우, gross·net 둘 다."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import pf_r, t_stat


def calendar_day_declus(df: pd.DataFrame, rcol: str) -> pd.Series:
    """같은 캘린더일에 여러 종목이 동시진입하면 그 날의 평균 R 하나로 축약."""
    d = df.copy()
    d["day"] = d["entry_time"].dt.floor("D")
    return d.groupby("day")[rcol].mean()


def rolling_window_declus(df: pd.DataFrame, rcol: str, window_days: int) -> pd.Series:
    """entry_time 오름차순으로 훑으며 window_days 이내 재진입은 하나의 클러스터로 묶어 평균."""
    d = df.sort_values("entry_time").reset_index(drop=True)
    clusters = []
    cur_cluster = [0]
    for i in range(1, len(d)):
        if (d["entry_time"].iloc[i] - d["entry_time"].iloc[cur_cluster[0]]).days < window_days:
            cur_cluster.append(i)
        else:
            clusters.append(cur_cluster)
            cur_cluster = [i]
    if cur_cluster:
        clusters.append(cur_cluster)
    means = [d[rcol].iloc[c].mean() for c in clusters]
    return pd.Series(means)


def summarize(series: pd.Series) -> dict:
    if len(series) < 2:
        return {"n": len(series), "pf": float("nan"), "t": float("nan")}
    return {"n": int(len(series)), "pf": pf_r(series), "t": t_stat(series),
            "mean": float(series.mean())}


def main() -> None:
    df = pd.read_csv("out_base_trades.csv", parse_dates=["entry_time", "exit_time", "event_time"])
    oos = df[(df["entry_time"] >= "2024-07-01") & (df["entry_time"] <= "2026-06-30 23:59:59")]

    out = {}
    for rcol in ["net_R", "gross_R"]:
        cal = calendar_day_declus(oos, rcol)
        r3 = rolling_window_declus(oos, rcol, 3)
        r5 = rolling_window_declus(oos, rcol, 5)
        out[rcol] = {
            "trade_level": summarize(oos[rcol]),
            "calendar_day": summarize(cal),
            "rolling_3day": summarize(r3),
            "rolling_5day": summarize(r5),
        }

    with open("out_diag_declus.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
