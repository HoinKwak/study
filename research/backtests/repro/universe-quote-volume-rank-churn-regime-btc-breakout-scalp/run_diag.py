"""부트스트랩 대조군 비교·de-clustering·순열검정 — results_main.pkl 재사용."""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np

import stats_utils as su

RESULTS = Path(__file__).parent / "results_main.pkl"


def load():
    with open(RESULTS, "rb") as f:
        return pickle.load(f)


def main():
    R = load()

    print("=== 1) 게이트 대조군 부트스트랩(표본수 맞춤, OOS, n35) ===")
    gated_oos = R["n35_gated"]["oos_df"]["r"].to_numpy()
    for ctrl in ["ungated", "random_gate", "gate_top"]:
        pool = R[f"n35_{ctrl}"]["oos_df"]["r"].to_numpy()
        res = su.bootstrap_matched_n_diff(pool, gated_oos)
        print(f"  gated vs {ctrl:12s}: base(gated) mean={res['base_mean']:+.4f} "
             f"pool_dist_mean={res['pool_dist_mean']:+.4f} gated의 pool분포 내 백분위={res['pctile']:.1f}"
             f" (n={res['n']})")
        diff = su.bootstrap_diff_test(gated_oos, pool)
        print(f"    직접비교: mean(gated)={diff['mean_a']:+.4f} mean({ctrl})={diff['mean_b']:+.4f} "
             f"diff={diff['diff']:+.4f} P(gated<=대조군)={diff['p_a_better']:.4f}")

    print("\n=== 2) de-clustering(n35_gated, OOS, net) ===")
    df = R["n35_gated"]["oos_df"]
    cal = su.decluster_calendar_day(df)
    roll = su.decluster_rolling_days(df, window_days=4)
    for label, d in [("원본(트레이드 단위)", df), ("캘린더일", cal), ("3~5일 롤링(4일)", roll)]:
        s = su.summary(d, label)
        print(" ", su.print_summary(s))

    print("\n=== 3) 순열검정(n35_gated, OOS, net) ===")
    r = df["r"].dropna().to_numpy()
    sr = su.sign_randomization_test(r)
    wr = su.win_rate_fixed_permutation_test(r)
    print(f"  부호 무작위화: obs_mean={sr['obs_mean']:+.4f} 백분위={sr['pctile']:.1f} (n_perm={sr['n_perm']})")
    print(f"  승률고정 순열: obs_mean={wr['obs_mean']:+.4f} 백분위={wr['pctile']:.1f} "
         f"win_rate={wr['win_rate']:.3f} (n_perm={wr['n_perm']})")

    print("\n=== 4) top-N 제거(n35_gated, OOS, net) ===")
    d2 = df.sort_values("r", ascending=False).reset_index(drop=True)
    for topn in [1, 3, 5, 10]:
        trimmed = d2.iloc[topn:]
        s = su.summary(trimmed, f"top-{topn} 제거")
        print(" ", su.print_summary(s))


if __name__ == "__main__":
    main()
