"""base(agree_pctile 게이트) ⊆ pool(corr/swap 게이트) 부분집합 관계 점검.

§4(대 none)는 논리적으로 항상 100%(필터 부분집합은 무필터의 부분집합이라 자명) — 이 스크립트는
그보다 정보가 되는 비교(서로 다른 지표를 쓰는 corr·swap 게이트와의 중첩)를 계산한다."""
from __future__ import annotations

import common
import engine
import stats_utils as su


def get(sig, gate: str):
    cfg = engine.RunConfig(gate=gate, fee_on=True)
    trades = engine.run_config(sig, cfg)
    return su.trades_df(trades)


def main():
    sig = common.build_signals()
    base = get(sig, "base"); corr = get(sig, "corr"); swap = get(sig, "swap")
    _, base_oos, base_full = su.split_is_oos(base)
    _, corr_oos, corr_full = su.split_is_oos(corr)
    _, swap_oos, swap_full = su.split_is_oos(swap)

    for label, a, b in [("OOS base vs corr", base_oos, corr_oos),
                        ("OOS base vs swap", base_oos, swap_oos),
                        ("FULL base vs corr", base_full, corr_full),
                        ("FULL base vs swap", base_full, swap_full)]:
        ta = set(a["entry_time"]); tb = set(b["entry_time"])
        ov = ta & tb
        print(f"{label}: base n={len(ta)} pool n={len(tb)} overlap={len(ov)} "
             f"frac_of_base={len(ov)/len(ta)*100:.1f}%")

    ind1 = su.independent_pair_diff(base_oos, corr_oos)
    ind2 = su.independent_pair_diff(base_oos, swap_oos)
    print("OOS 독립 Welch base vs corr(비중첩 잔여):", ind1)
    print("OOS 독립 Welch base vs swap(비중첩 잔여):", ind2)


if __name__ == "__main__":
    main()
