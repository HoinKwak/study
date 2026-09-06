"""파라미터 스윕 — apen_lo_pctile·pullback_lookback·atr_trail_mult·apen_window 핵심 4개.
각 변형에 대해 OOS 거래단위 PF/t 뿐 아니라 5일 롤링 de-cluster PF/t·top-3 클러스터 순익비중까지
병기(트레이드단위 수치만 보면 의사반복에 속을 위험 — 본 리포트 §5.2 교훈 그대로 적용)."""
from __future__ import annotations

import json

import pandas as pd

from common import pf_r, t_stat, split_is_oos
from diag_declus import rolling_cluster_groups, rolling_cluster_ids
from events import build_universe
from engine import run_variant, trades_to_df


def eval_variant(uni, **kwargs) -> dict:
    pullback_lookback = kwargs.pop("pullback_lookback", 5)
    trades = trades_to_df(run_variant(uni, pullback_lookback=pullback_lookback, **kwargs))
    if len(trades) == 0:
        return {"n": 0}
    _, oos, _ = split_is_oos(trades)
    if len(oos) == 0:
        return {"n": 0}
    r5 = rolling_cluster_groups(oos, "net_R", 5)
    d = oos.sort_values("entry_time").reset_index(drop=True)
    d["cid"] = rolling_cluster_ids(d["entry_time"], 5)
    csum = d.groupby("cid")["net_R"].sum().sort_values(ascending=False)
    top3_share = 100.0 * csum.iloc[:3].sum() / d["net_R"].sum() if d["net_R"].sum() != 0 else float("nan")
    return {
        "n": len(oos), "pf_net_trade": pf_r(oos["net_R"]), "t_net_trade": t_stat(oos["net_R"]),
        "n_clusters5d": len(r5), "pf_net_roll5d": pf_r(r5), "t_net_roll5d": t_stat(r5),
        "top3_share_pct": top3_share,
    }


def main() -> dict:
    uni_default = build_universe()
    results = {"baseline": eval_variant(uni_default)}

    for lo in [20, 40]:
        u = build_universe(apen_lo_pctile=lo)
        results[f"apen_lo_pctile={lo}"] = eval_variant(u)

    for pb in [3, 8]:
        results[f"pullback_lookback={pb}"] = eval_variant(uni_default, pullback_lookback=pb)

    for tm in [1.8, 3.2]:
        results[f"atr_trail_mult={tm}"] = eval_variant(uni_default, atr_trail_mult=tm)

    for win in [20, 45]:
        u = build_universe(apen_window=win)
        results[f"apen_window={win}"] = eval_variant(u)

    print(json.dumps(results, indent=2, default=float))
    return results


if __name__ == "__main__":
    main()
