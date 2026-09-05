"""부트스트랩 검정: 대조군 우열(표본수 맞춘 부트스트랩) + base⊆pool 중복률 + 독립 Welch +
부호 무작위화(승률 고정 대안 포함)."""
from __future__ import annotations

import pickle

import numpy as np

import common
import stats_utils as su
from scipy import stats as sstats


def overlap_frac(a_df, b_df) -> float:
    key_a = set(zip(a_df["symbol"], a_df["entry_time"]))
    key_b = set(zip(b_df["symbol"], b_df["entry_time"]))
    if not key_a:
        return float("nan")
    return len(key_a & key_b) / len(key_a)


def winrate_fixed_shuffle(r: np.ndarray, win_rate: float, n_rep: int = 200, seed: int = 55) -> dict:
    """승률 고정 대안 부호 무작위화: |r| 크기는 실제 거래에서 그대로 쓰되, 부호를 '실제 승률'
    확률로 다시 뽑는다(50/50 암묵귀무가설 함정 회피 — 과거 삼백병 건 교훈 반영)."""
    rng = np.random.default_rng(seed)
    n = len(r)
    absr = np.abs(r)
    means = np.empty(n_rep)
    for i in range(n_rep):
        sign = rng.random(n) < win_rate
        sim = np.where(sign, absr, -absr)
        means[i] = sim.mean()
    actual = r.mean()
    pctile = float((means <= actual).mean() * 100)
    return dict(pctile=pctile, actual_mean=float(actual), n=n, win_rate=win_rate)


def main():
    with open(common.SP / "trades_all.pkl", "rb") as f:
        d = pickle.load(f)

    base = d["base"]; gross = d["gross"]; none = d["none"]; atrp = d["atrp"]
    regime_rev = d["regime_rev"]

    _, oos_base, _ = su.split_is_oos(base)
    _, oos_gross, _ = su.split_is_oos(gross)
    _, oos_none, _ = su.split_is_oos(none)
    _, oos_atrp, _ = su.split_is_oos(atrp)
    _, oos_regime_rev, _ = su.split_is_oos(regime_rev)

    r_base = oos_base["r"].to_numpy()
    r_gross = oos_gross["r"].to_numpy()
    r_none = oos_none["r"].to_numpy()
    r_atrp = oos_atrp["r"].to_numpy()
    r_regime_rev = oos_regime_rev["r"].to_numpy()

    print("===== base⊆pool 중복률 =====")
    print("base vs none  overlap(base 기준):", overlap_frac(oos_base, oos_none))
    print("base vs atrp  overlap(base 기준):", overlap_frac(oos_base, oos_atrp))
    print("base vs regime_rev overlap(base 기준):", overlap_frac(oos_base, oos_regime_rev))

    print("\n===== 표본수 맞춘 부트스트랩(pool→base 크기로 리샘플, base가 그 분포에서 백분위) =====")
    b_vs_none = su.bootstrap_matched_n_diff(r_none, r_base, n_boot=5000)
    print("base vs none  :", b_vs_none)
    b_vs_atrp = su.bootstrap_matched_n_diff(r_atrp, r_base, n_boot=5000)
    print("base vs atrp  :", b_vs_atrp)
    b_vs_regime_rev = su.bootstrap_matched_n_diff(r_regime_rev, r_base, n_boot=5000)
    print("base vs regime_rev(대조군③, base가 이 분포에서 몇 %ile인지):", b_vs_regime_rev)

    print("\n===== 독립 Welch(base vs regime_rev, 중복 제거 잔여표본) =====")
    print(su.independent_pair_diff(oos_base, oos_regime_rev))
    print("독립 Welch(base vs atrp, 중복 제거 잔여표본):")
    print(su.independent_pair_diff(oos_base, oos_atrp))

    print("\n===== 직접 Welch(base vs regime_rev, 전체표본) =====")
    t, p = sstats.ttest_ind(r_base, r_regime_rev, equal_var=False)
    print(f"t={t:.3f} p={p:.4f} mean_base={r_base.mean():.4f} mean_regime_rev={r_regime_rev.mean():.4f}")

    print("\n===== 부호 무작위화(50/50, net·gross) =====")
    print("net :", su.sign_shuffle_test(r_base, n_rep=200))
    print("gross:", su.sign_shuffle_test(r_gross, n_rep=200))

    print("\n===== 승률 고정 대안 부호 무작위화(net·gross) =====")
    wr_net = (r_base > 0).mean()
    wr_gross = (r_gross > 0).mean()
    print(f"net  win_rate={wr_net:.4f} :", winrate_fixed_shuffle(r_base, wr_net))
    print(f"gross win_rate={wr_gross:.4f} :", winrate_fixed_shuffle(r_gross, wr_gross))


if __name__ == "__main__":
    main()
