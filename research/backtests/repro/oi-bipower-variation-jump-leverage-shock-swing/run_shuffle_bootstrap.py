"""셔플 대조군(부호 무작위화, 100회) + 대조군 우열 부트스트랩(표본수 맞춤 + 독립 Welch)."""
import pickle
import sys

import numpy as np
import pandas as pd
from scipy import stats as sstats

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oibv")
import common
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

base = results["base"]
_is, oos, _full = su.split_is_oos(base)

print("=" * 70)
print("① 부호 무작위화 셔플(100회) — 방향선택이 무작위보다 나은지")
print("=" * 70)
# risk_amount·holding 구조는 그대로 두고 방향만 50/50 재추첨 → PnL 부호를 무작위화한 R 근사:
# |r| 는 유지하고 부호만 무작위 재배정(승패 자체를 다시 굴리는 근사, mean(R) 분포 비교).
rng = np.random.default_rng(123)
abs_r = oos["r"].abs().to_numpy()
actual_mean = oos["r"].mean()
n_boot = 100
shuf_means = np.empty(n_boot)
for b in range(n_boot):
    signs = rng.choice([-1.0, 1.0], size=len(abs_r))
    shuf_means[b] = (abs_r * signs).mean()
pctile = float((shuf_means <= actual_mean).mean() * 100)
print(f"실제 mean(R)={actual_mean:.4f} vs 부호무작위화(100회) 분포 — 백분위={pctile:.1f}")

print("\n② 승률고정 대안 검정(이항검정) — 부호무작위화(50/50 가정)의 과장 여부 점검용")
# 부호무작위화(①)는 승률 50%를 암묵적 귀무가설로 깔아 실제 승률이 50%에서 벗어나면 그
# 자체로 극단 백분위가 나올 수 있다(과거 삼백병삼흑아 라운드에서 지적된 함정) — 승률 자체를
# 그대로 두고 "이 승률이 순수 우연(p=0.5 이항분포)과 구분되는지"만 별도로 본다.
win_rate = (oos["r"] > 0).mean()
n = len(oos)
wins = int((oos["r"] > 0).sum())
binom_p = sstats.binomtest(wins, n, 0.5).pvalue if n > 0 else float("nan")
print(f"승률={win_rate*100:.1f}% (n={n}, 승={wins}) — 이항검정(H0: p=0.5) p={binom_p:.4f}")

print("\n" + "=" * 70)
print("③ 대조군 우열 부트스트랩 — base vs price_swap / base vs reverse")
print("=" * 70)
for other_key, label in [("price_swap", "price_swap(가격기반JR 대조군)"),
                          ("reverse", "reverse(방향반전 대조군)"),
                          ("no_invalidation", "no_invalidation(무효화청산 비활성)")]:
    other = results[other_key]
    _is_o, oos_o, _full_o = su.split_is_oos(other)
    ra = oos["r"].dropna().to_numpy()
    rb = oos_o["r"].dropna().to_numpy()
    if len(ra) < 2 or len(rb) < 2:
        print(f"{label}: 표본부족(base n={len(ra)}, {other_key} n={len(rb)})")
        continue
    bd = su.bootstrap_diff_test(ra, rb, n_boot=5000)
    tw, pw = sstats.ttest_ind(ra, rb, equal_var=False)
    print(f"base(n={len(ra)}, mean={ra.mean():.4f}) vs {label}(n={len(rb)}, mean={rb.mean():.4f}) "
         f"| diff={bd['diff']:+.4f} p_not_better={bd['p_a_better']:.4f} | Welch t={tw:+.3f} p={pw:.4f}")
    # base ⊆ pool 대응: base 를 pool 에서 제외한 순수 독립분(있다면) — price_swap/reverse 는
    # 서로 다른 트레이드 집합(다른 트리거)이라 원천적으로 독립(중복 트레이드 최소).
    # entry_time 기준 중복 정도만 확인.
    overlap = len(set(zip(oos["symbol"], oos["entry_time"])) &
                 set(zip(oos_o["symbol"], oos_o["entry_time"])))
    print(f"  entry_time 기준 중복(overlap): {overlap}건 (base n={len(oos)}, {other_key} n={len(oos_o)})")

print("\n" + "=" * 70)
print("④ 표본수 맞춘 부트스트랩(대조군 풀 대비 base 백분위)")
print("=" * 70)
for other_key, label in [("price_swap", "price_swap"), ("reverse", "reverse")]:
    other = results[other_key]
    _is_o, oos_o, _full_o = su.split_is_oos(other)
    pool_r = oos_o["r"].dropna().to_numpy()
    base_r = oos["r"].dropna().to_numpy()
    if len(pool_r) < 5 or len(base_r) < 2:
        continue
    bm = su.bootstrap_matched_n_diff(pool_r, base_r, n_boot=5000)
    print(f"base(n={bm['n']}) mean={bm['base_mean']:.4f} vs {label}풀 표본수맞춤재추첨분포 "
         f"mean={bm['pool_dist_mean']:.4f} → base 백분위={bm['pctile']:.1f}")
