"""전체 결과 요약 — 기본안 IS/OOS/FULL PF·t (거래단위 + de-cluster 병기)."""
from __future__ import annotations

import json

from common import pf_r, t_stat, win_rate, split_is_oos
from diag_declus import calendar_day_groups, rolling_cluster_groups
from events import build_universe
from engine import run_variant, trades_to_df


def block(df) -> dict:
    if len(df) == 0:
        return {"n": 0}
    cal = calendar_day_groups(df, "net_R")
    r5 = rolling_cluster_groups(df, "net_R", 5)
    cal_g = calendar_day_groups(df, "gross_R")
    r5_g = rolling_cluster_groups(df, "gross_R", 5)
    return {
        "n_trades": len(df),
        "net": {"pf_trade": pf_r(df["net_R"]), "t_trade": t_stat(df["net_R"]),
                "pf_cal": pf_r(cal), "t_cal": t_stat(cal), "n_cal": len(cal),
                "pf_roll5d": pf_r(r5), "t_roll5d": t_stat(r5), "n_roll5d": len(r5)},
        "gross": {"pf_trade": pf_r(df["gross_R"]), "t_trade": t_stat(df["gross_R"]),
                  "pf_cal": pf_r(cal_g), "t_cal": t_stat(cal_g),
                  "pf_roll5d": pf_r(r5_g), "t_roll5d": t_stat(r5_g)},
        "win_rate": win_rate(df["net_R"]),
    }


def main() -> dict:
    uni = build_universe()
    trades = trades_to_df(run_variant(uni))
    is_df, oos_df, full_df = split_is_oos(trades)
    out = {"IS": block(is_df), "OOS": block(oos_df), "FULL": block(full_df)}
    print(json.dumps(out, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
