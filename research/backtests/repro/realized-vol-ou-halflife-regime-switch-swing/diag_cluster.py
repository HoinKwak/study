"""매크로 클러스터 분해 — 5일 롤링(고정블록) top-3/worst-3 제거 대칭 점검(양쪽 다).

사전 폐기조건 (e): top-3 제거 시 순손실 전환하면 폐기. 추가로 worst-3 제거도 대칭 점검
(직전 라운드 리뷰어 신규 규칙 — 최악 제거 시 오히려 개선되면 우편향 집중 구조 확증).
"""
from __future__ import annotations

import json
import sys

import pandas as pd

sys.path.insert(0, ".")
from stats_utils import pf, t_stat


def cluster_decompose(trades: pd.DataFrame, r_col: str = "net_R", window_days: int = 5) -> dict:
    if len(trades) == 0:
        return {}
    g = trades.copy().sort_values("entry_time")
    t0 = g["entry_time"].min().normalize()
    block = ((g["entry_time"] - t0).dt.days // window_days)
    g["_block"] = block
    agg = g.groupby("_block")[r_col].sum().sort_values()
    n_clusters = len(agg)
    total_r = agg.sum()

    top3 = agg.sort_values(ascending=False).head(3)
    worst3 = agg.sort_values(ascending=True).head(3)

    remain_top3 = g[~g["_block"].isin(top3.index)]
    remain_worst3 = g[~g["_block"].isin(worst3.index)]

    return {
        "n_clusters": n_clusters,
        "total_R": float(total_r),
        "top3_sum_R": float(top3.sum()),
        "top3_share_of_total": float(top3.sum() / total_r) if total_r != 0 else None,
        "worst3_sum_R": float(worst3.sum()),
        "after_remove_top3": {"n": len(remain_top3), "sum_R": float(remain_top3[r_col].sum()),
                               "PF": pf(remain_top3[r_col]), "t": t_stat(remain_top3[r_col])},
        "after_remove_worst3": {"n": len(remain_worst3), "sum_R": float(remain_worst3[r_col].sum()),
                                 "PF": pf(remain_worst3[r_col]), "t": t_stat(remain_worst3[r_col])},
        "top3_blocks": [str(b) for b in top3.index],
        "worst3_blocks": [str(b) for b in worst3.index],
    }


def main():
    out = {}
    for mode in ["breakout", "fade"]:
        trades = pd.read_csv(f"out_trades_{mode}_base.csv", parse_dates=["entry_time", "exit_time"])
        from common import OOS_START, OOS_END
        oos = trades[(trades["entry_time"] >= OOS_START) & (trades["entry_time"] <= OOS_END)]
        out[mode] = cluster_decompose(oos, "net_R", window_days=5)
        print(mode, "OOS cluster decomposition:")
        print(json.dumps(out[mode], indent=2))
    with open("out_diag_cluster.json", "w") as f:
        json.dump(out, f, indent=2, default=str)


if __name__ == "__main__":
    main()
