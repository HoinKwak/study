"""부트스트랩 대조군 비교·de-clustering·순열검정·top-N 제거·청산사유/보유기간 분포 — results_main.pkl 재사용."""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np

import stats_utils as su

RESULTS = Path(__file__).parent / "results_main.pkl"


def load():
    with open(RESULTS, "rb") as f:
        return pickle.load(f)["results"]


def main():
    R = load()

    print("=== 1) 게이트 대조군 부트스트랩(표본수 맞춤, OOS, net) ===")
    gated_oos = R["gated"]["oos_df"]["net_R"].to_numpy()
    for ctrl in ["ungated", "btc_solo", "ew_solo", "random_gate"]:
        pool = R[ctrl]["oos_df"]["net_R"].to_numpy()
        res = su.bootstrap_matched_n_diff(pool, gated_oos)
        print(f"  gated vs {ctrl:12s}: base(gated) mean={res['base_mean']:+.4f} "
             f"pool_dist_mean={res['pool_dist_mean']:+.4f} gated의 pool분포 내 백분위={res['pctile']:.1f}"
             f" (n={res['n']})")
        diff = su.bootstrap_diff_test(gated_oos, pool)
        print(f"    직접비교: mean(gated)={diff['mean_a']:+.4f} mean({ctrl})={diff['mean_b']:+.4f} "
             f"diff={diff['diff']:+.4f} P(gated<=대조군)={diff['p_a_better']:.4f}")

    print("\n=== 1b) 반전 대조군 vs 정방향(OOS, net, 표본수 동일 n) ===")
    rev_oos = R["reverse"]["oos_df"]["net_R"].to_numpy()
    diff = su.bootstrap_diff_test(gated_oos, rev_oos)
    print(f"  mean(정방향)={diff['mean_a']:+.4f} mean(반전)={diff['mean_b']:+.4f} diff={diff['diff']:+.4f} "
         f"P(정방향<=반전)={diff['p_a_better']:.4f}")

    print("\n=== 2) de-clustering(gated, OOS) ===")
    for costcol in ["net_R", "gross_R"]:
        print(f"  [{costcol}]")
        df = R["gated"]["oos_df"]
        cal = su.decluster_calendar_day(df, col=costcol)
        roll = su.decluster_rolling_days(df, window_days=4, col=costcol)
        for label, d in [("원본(트레이드 단위)", df), ("캘린더일", cal), ("3~5일 롤링(4일)", roll)]:
            s = su.summary(d, label, col=costcol)
            print("   ", su.print_summary(s))

    print("\n=== 3) 순열검정(gated, OOS, net, n_perm=100) ===")
    r = R["gated"]["oos_df"]["net_R"].dropna().to_numpy()
    sr = su.sign_randomization_test(r, n_perm=100)
    wr = su.win_rate_fixed_permutation_test(r, n_perm=100)
    print(f"  부호 무작위화: obs_mean={sr['obs_mean']:+.4f} 백분위={sr['pctile']:.1f} (n_perm={sr['n_perm']})")
    print(f"  승률고정 순열(승률={wr['win_rate']:.3f}<50%): obs_mean={wr['obs_mean']:+.4f} "
         f"백분위={wr['pctile']:.1f} (n_perm={wr['n_perm']})")

    print("\n=== 4) top-N 제거(gated, OOS, net) ===")
    d2 = R["gated"]["oos_df"].sort_values("net_R", ascending=False).reset_index(drop=True)
    for topn in [1, 5, 10, 20, 50]:
        trimmed = d2.iloc[topn:]
        s = su.summary(trimmed, f"top-{topn} 제거", col="net_R")
        print(" ", su.print_summary(s))

    print("\n=== 5) 청산사유·보유기간 분포(gated vs reverse, OOS) — zero_hold_frac 트리비얼 지표 대신 직접 확인 ===")
    for name in ["gated", "reverse"]:
        df = R[name]["oos_df"]
        print(f"  [{name}] n={len(df)}")
        print("   exit_reason:", df["exit_reason"].value_counts(normalize=True).round(3).to_dict())
        print("   hold_bars stats: mean=%.2f median=%.1f  hold==1 비율=%.3f" % (
            df["hold_bars"].mean(), df["hold_bars"].median(), (df["hold_bars"] == 1).mean()))

    print("\n=== 6) gate_state 별 성과 분해(gated, OOS, net) ===")
    df = R["gated"]["oos_df"]
    for state, g in df.groupby("gate_state"):
        s = su.summary(g, f"gate={state}", col="net_R")
        print(" ", su.print_summary(s))


if __name__ == "__main__":
    main()
