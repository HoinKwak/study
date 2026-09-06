"""§클러스터/기여도 분해 — top-N(최고 승리) 제거·worst-N(최악 손실) 제거 대칭 점검."""
from __future__ import annotations

import json
import pandas as pd

from common import pf_r, t_stat, IS_START, OOS_START, OOS_END


def main():
    df = pd.read_csv("out_trades_base.csv", parse_dates=["entry_time"])
    oos = df[(df["entry_time"] >= OOS_START) & (df["entry_time"] <= OOS_END)].sort_values("net_R")
    out = {"n_oos": len(oos)}
    for topn in [1, 2, 3]:
        best_removed = oos.iloc[:-topn] if topn < len(oos) else oos.iloc[0:0]
        worst_removed = oos.iloc[topn:] if topn < len(oos) else oos.iloc[0:0]
        out[f"remove_top{topn}_best"] = {
            "n": len(best_removed), "net_pf": pf_r(best_removed["net_R"]),
            "net_t": t_stat(best_removed["net_R"])}
        out[f"remove_worst{topn}"] = {
            "n": len(worst_removed), "net_pf": pf_r(worst_removed["net_R"]),
            "net_t": t_stat(worst_removed["net_R"])}
    print(json.dumps(out, indent=2, default=str))
    with open("out_diag_topn.json", "w") as f:
        json.dump(out, f, indent=2, default=str)


if __name__ == "__main__":
    main()
