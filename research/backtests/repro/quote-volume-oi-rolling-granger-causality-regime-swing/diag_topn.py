"""매크로 클러스터 분해: 상위(top-N) 제거 + ⭐최악(worst-N) 제거까지 대칭으로.
또한 종목간 진입일 상관(평시/꼬리)도 함께 계산."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import pf_r, t_stat, split_is_oos

HERE = Path(__file__).resolve().parent


def topn_removed(sub: pd.DataFrame, col: str, n: int, worst: bool = False) -> dict:
    if len(sub) <= n:
        return {"n_left": max(0, len(sub) - n), "pf": float("nan"), "t": float("nan")}
    s = sub.sort_values(col, ascending=worst)
    left = s.iloc[n:]
    return {"n_left": int(len(left)), "pf": pf_r(left[col]), "t": t_stat(left[col])}


def cross_symbol_corr(df: pd.DataFrame) -> dict:
    if len(df) == 0:
        return {}
    d = df.copy()
    d["day"] = d["entry_time"].dt.floor("D")
    symbols = sorted(d["symbol"].unique())
    if len(symbols) < 2:
        return {"note": "종목 1개뿐이라 상관 계산 불가"}
    all_days = pd.date_range(d["day"].min(), d["day"].max(), freq="D")
    mat = pd.DataFrame(0, index=all_days, columns=symbols)
    for _, r in d.iterrows():
        mat.loc[r["day"], r["symbol"]] = 1
    corr = mat.corr()
    vals = corr.values[np.triu_indices(len(symbols), k=1)]
    same_day = int((mat.sum(axis=1) >= 2).sum())
    return {"avg_pairwise_corr": float(np.nanmean(vals)), "n_days_multi_symbol": same_day,
            "n_unique_days": int(len(mat))}


def main():
    df = pd.read_csv(HERE / "out_trades_base.csv", parse_dates=["entry_time"])
    is_df, oos_df, full_df = split_is_oos(df)
    out = {}
    for name, sub in [("IS", is_df), ("OOS", oos_df), ("FULL", full_df)]:
        out[name] = {}
        for col in ("gross_R", "net_R"):
            out[name][col] = {
                "baseline": {"n": int(len(sub)), "pf": pf_r(sub[col]) if len(sub) else float("nan")},
                "top1_removed": topn_removed(sub, col, 1),
                "top3_removed": topn_removed(sub, col, 3),
                "worst1_removed": topn_removed(sub, col, 1, worst=True),
                "worst3_removed": topn_removed(sub, col, 3, worst=True),
            }
        out[name]["cross_symbol_entry_corr"] = cross_symbol_corr(sub)
    print(json.dumps(out, indent=2, default=str))
    (HERE / "out_diag_topn.json").write_text(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
