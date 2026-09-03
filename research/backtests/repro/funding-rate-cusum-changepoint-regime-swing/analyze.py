"""메인 분석 러너 — 기본 변형(base) IS/OOS/FULL 통계 + 무비용 진단 + 반전/게이트없음 대조군."""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

from common import IS_START, IS_END, OOS_START, OOS_END, pf_r, t_stat, win_rate
from engine import load_all, run_variant, trades_to_df


def summarize(df: pd.DataFrame, rcol: str = "net_R") -> dict:
    if len(df) == 0:
        return {"n": 0}
    r = df[rcol]
    return {"n": int(len(df)), "pf": pf_r(r), "t": t_stat(r), "mean_R": float(r.mean()),
            "win_rate": win_rate(r), "sum_R": float(r.sum())}


def split(df: pd.DataFrame, tcol: str = "entry_time"):
    if len(df) == 0:
        return df, df, df
    t = df[tcol]
    is_df = df[(t >= IS_START) & (t <= IS_END)]
    oos_df = df[(t >= OOS_START) & (t <= OOS_END)]
    full_df = df[(t >= IS_START) & (t <= OOS_END)]
    return is_df, oos_df, full_df


def main() -> None:
    univ = load_all()

    # === 기본 변형 ===
    trades = run_variant(univ)
    df = trades_to_df(trades)
    is_df, oos_df, full_df = split(df)
    assert len(is_df) + len(oos_df) == len(full_df), "IS+OOS != FULL"

    result = {
        "base_net": {
            "IS": summarize(is_df, "net_R"), "OOS": summarize(oos_df, "net_R"),
            "FULL": summarize(full_df, "net_R"),
        },
        "base_gross": {
            "IS": summarize(is_df, "gross_R"), "OOS": summarize(oos_df, "gross_R"),
            "FULL": summarize(full_df, "gross_R"),
        },
    }

    # === 무비용 진단(gross_R 이미 fee=0/slip=0 이므로 별도 시뮬 불필요 — R 정의 자체가 gross) ===
    # (net_R = gross_R - cost_R 이므로 gross_R 은 곧 fee=0·slippage=0 시뮬과 동일)

    # === 대조군: 게이트없음(EMA 방향필터 제거) ===
    trades_nogate = run_variant(univ, no_ema_gate=True)
    df_nogate = trades_to_df(trades_nogate)
    _, oos_nogate, full_nogate = split(df_nogate)
    result["nogate_net"] = {"OOS": summarize(oos_nogate, "net_R"),
                            "FULL": summarize(full_nogate, "net_R")}
    result["nogate_gross"] = {"OOS": summarize(oos_nogate, "gross_R"),
                              "FULL": summarize(full_nogate, "gross_R")}

    # === 반전 대조군(방향 뒤집기, 반대체인지포인트 무효화는 원신호 기준 유지) ===
    trades_rev = run_variant(univ, reverse=True)
    df_rev = trades_to_df(trades_rev)
    _, oos_rev, full_rev = split(df_rev)
    result["reverse_net"] = {"OOS": summarize(oos_rev, "net_R"), "FULL": summarize(full_rev, "net_R")}

    # === 반전 대조군, 제3의 대안(반전모드에서 반대체인지포인트 무효화 청산 완전 비활성) ===
    trades_rev2 = run_variant(univ, reverse=True, disable_reversal_exit=True)
    df_rev2 = trades_to_df(trades_rev2)
    _, oos_rev2, full_rev2 = split(df_rev2)
    result["reverse_noinvalidation_net"] = {"OOS": summarize(oos_rev2, "net_R"),
                                            "FULL": summarize(full_rev2, "net_R")}

    # === 청산사유/보유기간 분포 (zero_hold_frac 트리비얼 — 직접 분포로 대체) ===
    for name, d in [("base", full_df), ("reverse", full_rev)]:
        if len(d):
            result[f"{name}_exit_reason"] = d["exit_reason"].value_counts().to_dict()
            result[f"{name}_hold_bars_desc"] = d["hold_bars"].describe().to_dict()

    with open("out_summary.json", "w") as f:
        json.dump(result, f, indent=2, default=str)

    df.to_csv("out_base_trades.csv", index=False)
    df_rev.to_csv("out_reverse_trades.csv", index=False)
    df_nogate.to_csv("out_nogate_trades.csv", index=False)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
