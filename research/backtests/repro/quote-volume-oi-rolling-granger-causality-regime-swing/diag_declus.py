"""de-clustering: 캘린더일 단위 + 3~5일 롤링 재집계(gross·net 둘 다)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import pf_r, t_stat, split_is_oos

HERE = Path(__file__).resolve().parent


def calendar_day_declus(df: pd.DataFrame, col: str) -> dict:
    if len(df) == 0:
        return {"n_days": 0}
    d = df.copy()
    d["day"] = d["entry_time"].dt.floor("D")
    daily = d.groupby("day")[col].sum()
    return {"n_days": int(len(daily)), "pf": pf_r(daily), "t": t_stat(daily)}


def rolling_block_declus(df: pd.DataFrame, col: str, block_days: int) -> dict:
    if len(df) == 0:
        return {"n_blocks": 0}
    d = df.sort_values("entry_time").copy()
    t0 = d["entry_time"].iloc[0]
    block_id = ((d["entry_time"] - t0) / pd.Timedelta(days=block_days)).astype(int)
    grouped = d.groupby(block_id)[col].sum()
    return {"n_blocks": int(len(grouped)), "pf": pf_r(grouped), "t": t_stat(grouped)}


def main():
    df = pd.read_csv(HERE / "out_trades_base.csv", parse_dates=["entry_time"])
    is_df, oos_df, full_df = split_is_oos(df)
    out = {}
    for name, sub in [("IS", is_df), ("OOS", oos_df), ("FULL", full_df)]:
        out[name] = {}
        for col in ("gross_R", "net_R"):
            out[name][col] = {
                "trade_unit": {"n": int(len(sub)), "pf": pf_r(sub[col]) if len(sub) else float("nan"),
                              "t": t_stat(sub[col]) if len(sub) else float("nan")},
                "calendar_day": calendar_day_declus(sub, col),
                "rolling_3d": rolling_block_declus(sub, col, 3),
                "rolling_5d": rolling_block_declus(sub, col, 5),
            }
    print(json.dumps(out, indent=2, default=str))
    (HERE / "out_diag_declus.json").write_text(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
