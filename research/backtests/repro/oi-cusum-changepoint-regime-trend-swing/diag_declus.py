"""§de-clustering: 캘린더일 + 3~5일 롤링(BTC 단일종목이라 "동시진입"은 없지만, 스펙 요구대로
같은 날/근접일 다건이 있으면 대표 1건으로 묶어 t 재계산). gross/net 병행."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import pf_r, t_stat


def decluster(df: pd.DataFrame, window_days: int) -> pd.DataFrame:
    """entry_time 기준 window_days 이내로 뭉친 트레이드를 그룹화해 그룹당 net_R 합산(1행)."""
    if len(df) == 0:
        return df
    d = df.sort_values("entry_time").reset_index(drop=True)
    group_id = 0
    groups = [0]
    last_t = d["entry_time"].iloc[0]
    for i in range(1, len(d)):
        t = d["entry_time"].iloc[i]
        if (t - last_t) <= pd.Timedelta(days=window_days):
            groups.append(group_id)
        else:
            group_id += 1
            groups.append(group_id)
        last_t = t
    d["cluster"] = groups
    agg = d.groupby("cluster").agg(net_R=("net_R", "sum"), gross_R=("gross_R", "sum"),
                                    entry_time=("entry_time", "first")).reset_index(drop=True)
    return agg


def main():
    df = pd.read_csv("out_trades_base.csv", parse_dates=["entry_time", "exit_time", "cp_time"])
    from common import IS_START, IS_END, OOS_START, OOS_END
    oos = df[(df["entry_time"] >= OOS_START) & (df["entry_time"] <= OOS_END)]
    full = df[(df["entry_time"] >= IS_START) & (df["entry_time"] <= OOS_END)]

    out = {}
    for name, d in [("oos", oos), ("full", full)]:
        out[name] = {}
        for unit, wd in [("trade", 0), ("calendar_day", 1), ("3day_roll", 3), ("5day_roll", 5)]:
            dd = decluster(d, wd) if wd > 0 else d
            out[name][unit] = {
                "n": len(dd),
                "net_pf": pf_r(dd["net_R"]), "net_t": t_stat(dd["net_R"]),
                "gross_pf": pf_r(dd["gross_R"]), "gross_t": t_stat(dd["gross_R"]),
            }
    print(json.dumps(out, indent=2, default=str))
    with open("out_diag_declus.json", "w") as f:
        json.dump(out, f, indent=2, default=str)


if __name__ == "__main__":
    main()
