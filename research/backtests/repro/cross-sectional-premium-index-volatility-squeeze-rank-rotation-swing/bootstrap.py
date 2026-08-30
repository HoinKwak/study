"""표본수 맞춘 부트스트랩 검정: base vs no_rank(중복독립화 포함), base vs shuffle."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from scipy import stats

from engine import pf_r


def welch_test(a: pd.Series, b: pd.Series) -> tuple[float, float]:
    t, p = stats.ttest_ind(a, b, equal_var=False)
    return float(t), float(p)


def bootstrap_pf_ci(series: pd.Series, n_boot: int = 2000, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    vals = series.values
    n = len(vals)
    pfs = []
    for _ in range(n_boot):
        sample = vals[rng.integers(0, n, n)]
        pos = sample[sample > 0].sum()
        neg = -sample[sample < 0].sum()
        if neg > 0:
            pfs.append(pos / neg)
    pfs = np.array(pfs)
    return float(np.percentile(pfs, 2.5)), float(np.percentile(pfs, 97.5))


def main() -> None:
    base = pd.read_csv("out_base_trades.csv", parse_dates=["entry_time"])
    nr = pd.read_csv("out_norank_trades.csv", parse_dates=["entry_time"])

    from common import OOS_START, OOS_END
    base_oos = base[(base["entry_time"] >= OOS_START) & (base["entry_time"] <= OOS_END)]
    nr_oos = nr[(nr["entry_time"] >= OOS_START) & (nr["entry_time"] <= OOS_END)]

    out = {}

    # base ⊆ pool 확인: base 트레이드가 no_rank 풀에 (symbol, entry_time) 기준 존재하는지
    key_base = set(zip(base_oos["symbol"], base_oos["entry_time"]))
    key_nr = set(zip(nr_oos["symbol"], nr_oos["entry_time"]))
    overlap = key_base & key_nr
    out["base_oos_n"] = len(base_oos)
    out["norank_oos_n"] = len(nr_oos)
    out["overlap_n"] = len(overlap)
    out["overlap_frac_of_base"] = len(overlap) / len(base_oos) if len(base_oos) else float("nan")
    print(f"base OOS n={len(base_oos)}, no_rank OOS n={len(nr_oos)}, "
          f"중복(base⊆pool) n={len(overlap)} ({out['overlap_frac_of_base']*100:.1f}%)")

    # 전체 비교 Welch (base vs no_rank, net_R)
    t1, p1 = welch_test(base_oos["net_R"], nr_oos["net_R"])
    out["welch_base_vs_norank_full"] = {"t": t1, "p": p1}
    print(f"Welch(base vs no_rank, 전체): t={t1:.3f} p={p1:.4f}")

    # 중복 제거 독립표본: no_rank 에서 base와 겹치는 트레이드 제외한 잔여만
    nr_oos_key = list(zip(nr_oos["symbol"], nr_oos["entry_time"]))
    nr_indep = nr_oos[[k not in key_base for k in nr_oos_key]]
    if len(nr_indep) >= 2:
        t2, p2 = welch_test(base_oos["net_R"], nr_indep["net_R"])
        out["welch_base_vs_norank_independent_residual"] = {"t": t2, "p": p2, "n_residual": len(nr_indep)}
        print(f"Welch(base vs no_rank 잔여-독립, n={len(nr_indep)}): t={t2:.3f} p={p2:.4f}")
    else:
        out["welch_base_vs_norank_independent_residual"] = None
        print(f"no_rank 잔여 독립표본 부족(n={len(nr_indep)}) — 검정 생략")

    # 표본수 맞춘 부트스트랩(base n 크기로 no_rank 에서 반복추출, PF 분포 비교)
    rng = np.random.default_rng(42)
    n_base = len(base_oos)
    base_pf = pf_r(base_oos["net_R"])
    nr_vals = nr_oos["net_R"].values
    boot_pfs = []
    for _ in range(2000):
        if n_base > len(nr_vals):
            break
        sample = rng.choice(nr_vals, size=n_base, replace=False)
        pos = sample[sample > 0].sum()
        neg = -sample[sample < 0].sum()
        if neg > 0:
            boot_pfs.append(pos / neg)
    if boot_pfs:
        boot_pfs = np.array(boot_pfs)
        pct = (boot_pfs < base_pf).mean() * 100
        out["base_pf"] = float(base_pf)
        out["norank_matched_boot_pf_mean"] = float(boot_pfs.mean())
        out["base_percentile_vs_norank_matched_boot"] = float(pct)
        print(f"표본수맞춘 부트스트랩(no_rank, n={n_base}): PF 평균={boot_pfs.mean():.3f}, "
              f"base(PF={base_pf:.3f}) 백분위={pct:.1f}")

    with open("out_bootstrap.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\n저장: out_bootstrap.json")


if __name__ == "__main__":
    main()
