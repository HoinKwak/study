"""매크로 클러스터 분해 — 5일 롤링 클러스터 상위 몇 개가 OOS 순 R(net_R 합)의 몇 %를 차지하는가.
top-1/top-2/top-3 제거 시 PF(R)·t 변화도 함께 본다(스펙 §종목간 신호상관에서 요구한 항목)."""
from __future__ import annotations

import json

import pandas as pd

from common import pf_r, t_stat, split_is_oos
from diag_declus import rolling_cluster_ids
from events import build_universe
from engine import run_variant, trades_to_df


def main() -> dict:
    uni = build_universe()
    trades = trades_to_df(run_variant(uni))
    _, oos_df, _ = split_is_oos(trades)
    d = oos_df.sort_values("entry_time").reset_index(drop=True)
    d["cid"] = rolling_cluster_ids(d["entry_time"], 5)
    cluster_sum = d.groupby("cid")["net_R"].sum().sort_values(ascending=False)
    total_net = d["net_R"].sum()
    total_gross = d["gross_R"].sum()

    top_shares = {}
    for k in [1, 2, 3, 5]:
        top_ids = cluster_sum.index[:k]
        top_sum = cluster_sum.loc[top_ids].sum()
        share_pct = 100.0 * top_sum / total_net if total_net != 0 else float("nan")
        rest = d[~d["cid"].isin(top_ids)]
        top_shares[f"top{k}"] = {
            "share_pct_of_total_net": share_pct,
            "n_clusters_total": int(cluster_sum.shape[0]),
            "rest_n_trades": int(len(rest)),
            "rest_pf_net": pf_r(rest["net_R"]),
            "rest_t_net": t_stat(rest["net_R"]),
            "rest_pf_gross": pf_r(rest["gross_R"]),
            "rest_t_gross": t_stat(rest["gross_R"]),
        }

    # 상위 클러스터의 실제 시점·관여종목·순익 상세
    top_detail = []
    for cid in cluster_sum.index[:3]:
        sub = d[d["cid"] == cid]
        top_detail.append({
            "cid": int(cid), "start": str(sub["entry_time"].min()),
            "end": str(sub["entry_time"].max()), "n_trades": int(len(sub)),
            "symbols": sorted(sub["symbol"].unique().tolist()),
            "net_R_sum": float(sub["net_R"].sum()),
        })

    out = {"total_net_R": float(total_net), "total_gross_R": float(total_gross),
           "n_clusters": int(cluster_sum.shape[0]), "top_shares": top_shares,
           "top_detail": top_detail}
    print(json.dumps(out, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
