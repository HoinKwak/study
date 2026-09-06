"""대조군 비교(스펙 사전 폐기조건 (f) 포함): base vs symlambda(대조군①)·taker_z(대조군②)·none —
표본수 맞춘 부트스트랩 + base⊆pool 중첩률 + 중첩없는 독립 Welch. 부호 무작위화·승률고정 셔플.
hypothesis_orig/reverse 신호 중첩률(구조적으로 100% 동일 — 아래에서 실측 확인)."""
import pickle

import numpy as np

import common
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

base_net = su.split_is_oos(results[("base", True)])[1]
base_gross = su.split_is_oos(results[("base", False)])[1]

print("=== base OOS 개요 === net n=%d gross n=%d" % (len(base_net), len(base_gross)))

for other_gate, label in [("symlambda", "대조군①(대칭λ 레짐, 딥/씬마켓)"),
                          ("taker_z", "대조군②(taker_buy_ratio 레벨 게이트, 동어반복 확인)"),
                          ("none", "게이트 완전제거(트리거+sv3부호만)")]:
    other_net = su.split_is_oos(results[(other_gate, True)])[1]
    other_gross = su.split_is_oos(results[(other_gate, False)])[1]
    print(f"\n--- base vs {other_gate}[{label}] ---")

    key_base = set(zip(base_net["symbol"], base_net["entry_time"]))
    key_other = set(zip(other_net["symbol"], other_net["entry_time"]))
    overlap = key_base & key_other
    print(f" base n={len(key_base)} other n={len(key_other)} 중첩={len(overlap)} "
         f"(base의 {len(overlap)/len(key_base)*100:.1f}% 가 other 에도 존재)")

    for tag, b, o in [("net", base_net, other_net), ("gross", base_gross, other_gross)]:
        bm = su.bootstrap_matched_n_diff(o["r"].to_numpy(), b["r"].to_numpy())
        print(f"  [{tag}] 표본수맞춘부트스트랩: base mean(R)={bm['base_mean']:+.4f} "
             f"vs pool(={other_gate}) 리샘플분포 mean={bm['pool_dist_mean']:+.4f} "
             f"→ base 가 그 분포에서 {bm['pctile']:.1f} 백분위"
             f"  [(f) 폐기조건: p>0.10 즉 10~90백분위면 무가치]")
        ind = su.independent_pair_diff(b, o)
        print(f"  [{tag}] 중첩제거 독립 Welch: overlap={ind['overlap_n']}"
             f"({ind['overlap_frac_a']*100:.1f}% of base) a_only={ind['a_only_n']} "
             f"b_only={ind['b_only_n']} t={ind['welch_t']:+.3f} p={ind['welch_p']:.4f}")

print("\n=== 부호 무작위화(100회) & 승률고정 셔플 — base OOS ===")
for tag, d in [("net", base_net), ("gross", base_gross)]:
    r = d["r"].to_numpy()
    ss = su.sign_shuffle_test(r, n_rep=100)
    wf = su.winrate_fixed_shuffle_test(r, n_rep=100)
    print(f" [{tag}] n={len(r)} 부호무작위화: 실제mean={ss['actual_mean']:+.4f} "
         f"백분위={ss['pctile']:.1f}  |  승률고정: 실제mean={wf['actual_mean']:+.4f} "
         f"승률={wf['win_rate']*100:.1f}% 백분위={wf['pctile']:.1f}")

# --- 반전 대조군: reverse == hypothesis_orig 신호 중첩률(구조상 100% 동일 여부 실측) ---
rev_net = su.split_is_oos(results[("reverse", True)])[1]
hyp_net = su.split_is_oos(results[("hypothesis_orig", True)])[1]
key_rev = set(zip(rev_net["symbol"], rev_net["entry_time"]))
key_hyp = set(zip(hyp_net["symbol"], hyp_net["entry_time"]))
key_base_all = set(zip(base_net["symbol"], base_net["entry_time"]))
overlap_rev_hyp = key_rev & key_hyp
overlap_rev_base = key_rev & key_base_all
print(f"\n=== 반전 대조군(reverse) 신호 중첩률 ===")
print(f" reverse n={len(key_rev)} hypothesis_orig n={len(key_hyp)} 중첩={len(overlap_rev_hyp)} "
     f"({len(overlap_rev_hyp)/len(key_rev)*100:.1f}% of reverse) — "
     f"⚠️base 는 hypothesis_orig 의 방향반전으로 '확정'됐으므로 reverse(=base 반전)와 "
     f"hypothesis_orig 는 진입시점 신호집합이 구조적으로 완전 동일할 것으로 예상(방향만 다름).")
print(f" reverse ∩ base(원신호) = {len(overlap_rev_base)}건 ({len(overlap_rev_base)/len(key_base_all)*100:.1f}% of base) "
     f"— reverse 는 base 와 '진입시점'은 동일(방향만 반대)이어야 정상.")
