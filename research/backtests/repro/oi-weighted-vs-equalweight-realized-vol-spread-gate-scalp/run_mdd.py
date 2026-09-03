"""R-배수 누적합 기준 MDD(최대낙폭, R단위) — IS/OOS/FULL, net."""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).parent / "results_main.pkl"


def mdd_r(df, col="net_R"):
    if df.empty:
        return float("nan")
    cum = df.sort_values("entry_time")[col].cumsum()
    peak = cum.cummax()
    dd = cum - peak
    return float(dd.min())


def main():
    with open(RESULTS, "rb") as f:
        R = pickle.load(f)["results"]
    for name in ["gated", "ungated", "btc_solo", "ew_solo", "reverse"]:
        for label in ["is_df", "oos_df", "full_df"]:
            df = R[name][label]
            print(f"{name:12s} {label:8s} n={len(df):5d} MDD(R)={mdd_r(df):+.2f}")


if __name__ == "__main__":
    main()
