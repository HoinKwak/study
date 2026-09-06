"""대조군 비교: 게이트없음(none)·반대방향(tvr_hi)·신호원교체(rv_lo, RV스퀴즈) — 표본수 맞춘
부트스트랩 + base⊆pool 중첩률 + 중첩없는 독립 Welch. 부호 무작위화·승률고정 셔플(net/gross 둘 다)."""
import pickle

import numpy as np

import common
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

base_net = su.split_is_oos(results[("tvr_lo", True)])[1]
base_gross = su.split_is_oos(results[("tvr_lo", False)])[1]

print("=== base(tvr_lo) OOS 개요 === net n=%d gross n=%d" % (len(base_net), len(base_gross)))

for other_gate, label in [("none", "게이트없음(순수 Donchian)"), ("tvr_hi", "게이트 반대방향(tvr_std_pctile>=70)"),
                          ("rv_lo", "신호원교체(RV 스퀴즈, rv15_pctile<=30)")]:
    other_net = su.split_is_oos(results[(other_gate, True)])[1]
    other_gross = su.split_is_oos(results[(other_gate, False)])[1]
    print(f"\n--- base(tvr_lo) vs {other_gate}[{label}] ---")

    # base⊆pool 중첩률(net 트레이드 기준, symbol+entry_time)
    key_base = set(zip(base_net["symbol"], base_net["entry_time"]))
    key_other = set(zip(other_net["symbol"], other_net["entry_time"]))
    overlap = key_base & key_other
    print(f" base n={len(key_base)} other n={len(key_other)} 중첩={len(overlap)} "
         f"(base의 {len(overlap)/len(key_base)*100:.1f}% 가 other 에도 존재)")

    for tag, b, o in [("net", base_net, other_net), ("gross", base_gross, other_gross)]:
        # 표본수 맞춘 부트스트랩: other 를 pool 로 base 크기만큼 리샘플
        bm = su.bootstrap_matched_n_diff(o["r"].to_numpy(), b["r"].to_numpy())
        print(f"  [{tag}] 표본수맞춘부트스트랩: base mean(R)={bm['base_mean']:+.4f} "
             f"vs pool(={other_gate}) 리샘플분포 mean={bm['pool_dist_mean']:+.4f} "
             f"→ base 가 그 분포에서 {bm['pctile']:.1f} 백분위")
        ind = su.independent_pair_diff(b, o)
        print(f"  [{tag}] 중첩제거 독립 Welch: overlap={ind['overlap_n']}"
             f"({ind['overlap_frac_a']*100:.1f}% of base) a_only={ind['a_only_n']} "
             f"b_only={ind['b_only_n']} t={ind['welch_t']:+.3f} p={ind['welch_p']:.4f}")

print("\n=== 부호 무작위화(100회) & 승률고정 셔플 — base(tvr_lo) OOS ===")
for tag, d in [("net", base_net), ("gross", base_gross)]:
    r = d["r"].to_numpy()
    ss = su.sign_shuffle_test(r, n_rep=100)
    wf = su.winrate_fixed_shuffle_test(r, n_rep=100)
    print(f" [{tag}] n={len(r)} 부호무작위화: 실제mean={ss['actual_mean']:+.4f} "
         f"백분위={ss['pctile']:.1f}  |  승률고정: 실제mean={wf['actual_mean']:+.4f} "
         f"승률={wf['win_rate']*100:.1f}% 백분위={wf['pctile']:.1f}")

# --- 원신호와의 신호 중첩률(reverse) — 반전 대조군 요건: "동일 신호집합" 여부 명시 ---
rev_net = su.split_is_oos(results[("reverse", True)])[1]
key_base_all = set(zip(base_net["symbol"], base_net["entry_time"]))
key_rev = set(zip(rev_net["symbol"], rev_net["entry_time"]))
overlap_rev = key_base_all & key_rev
print(f"\n=== base(tvr_lo) vs reverse 신호 중첩률(OOS) ===")
print(f" base n={len(key_base_all)} reverse n={len(key_rev)} 중첩={len(overlap_rev)} "
     f"(base의 {len(overlap_rev)/len(key_base_all)*100:.1f}%, reverse의 "
     f"{len(overlap_rev)/len(key_rev)*100:.1f}%)")
print(f" base전용={len(key_base_all - key_rev)}건 reverse전용={len(key_rev - key_base_all)}건")
