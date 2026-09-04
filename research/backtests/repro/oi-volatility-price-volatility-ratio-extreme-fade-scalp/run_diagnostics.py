"""필수 진단 일괄 실행 — de-clustering/LOO/top-N/shuffle/부트스트랩(gross 포함)."""
import pickle
import sys

import numpy as np
import pandas as pd
from scipy import stats as sstats

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oivolratio")
import common
import engine
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

a_net = results[("A", True)]
a_gross = results[("A", False)]
b_net = results[("B", True)]
b_gross = results[("B", False)]

_, a_oos, _ = su.split_is_oos(a_net)
_, a_oos_g, _ = su.split_is_oos(a_gross)
_, b_oos, _ = su.split_is_oos(b_net)
_, b_oos_g, _ = su.split_is_oos(b_gross)

print("### (반전 대조군 A vs B) OOS net 부트스트랩 우월성 ###")
bd = su.bootstrap_diff_test(a_oos["r"].to_numpy(), b_oos["r"].to_numpy())
print(bd, "  (p_a_better 가 클수록 A(스펙 기본 페이드) 가 B(모멘텀) 보다 우수하지 않다는 뜻)")

print("\n### base(A)⊆pool 중복도 — 겹치지 않는 잔여표본 독립검정 (동일 트리거, 방향만 다름이라 100% 중첩 예상) ###")
ip = su.independent_pair_diff(a_oos, b_oos)
print(ip)

print("\n\n### de-clustering (A/net, OOS) — 캘린더일 단위 ###")
dc = su.decluster_calendar_day(a_oos)
if len(dc) >= 2:
    t, p = sstats.ttest_1samp(dc["r"], 0.0)
else:
    t, p = np.nan, np.nan
print(f"  명목 n={len(a_oos)} -> 고유 캘린더일 n={len(dc)}  PF(R)={su.pf_r(dc):.3f} "
     f"mean(R)={dc['r'].mean():+.4f} t={t:+.3f} p={p:.4f}")

print("\n### de-clustering (A/net, OOS) — 3~5일 롤링 윈도우 ###")
for wd in [3, 4, 5]:
    dr = su.decluster_rolling_days(a_oos, window_days=wd)
    if len(dr) >= 2:
        t, p = sstats.ttest_1samp(dr["r"], 0.0)
    else:
        t, p = np.nan, np.nan
    print(f"  window={wd}d -> 고유클러스터 n={len(dr)}  PF(R)={su.pf_r(dr):.3f} "
         f"mean(R)={dr['r'].mean():+.4f} t={t:+.3f} p={p:.4f}")

print("\n### de-clustering — gross(fee=0) 도 동일 처리(캘린더일) ###")
dcg = su.decluster_calendar_day(a_oos_g)
if len(dcg) >= 2:
    t, p = sstats.ttest_1samp(dcg["r"], 0.0)
else:
    t, p = np.nan, np.nan
print(f"  gross 캘린더일 n={len(dcg)} PF(R)={su.pf_r(dcg):.3f} mean(R)={dcg['r'].mean():+.4f} "
     f"t={t:+.3f} p={p:.4f}")

print("\n\n### LOO(symbol) — A/net, OOS ###")
for sym in common.SYMBOLS:
    sub = a_oos[a_oos["symbol"] != sym]
    t, p = (sstats.ttest_1samp(sub["r"], 0.0) if len(sub) >= 2 else (np.nan, np.nan))
    print(f"  {sym} 제외 n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} mean(R)={sub['r'].mean():+.4f} t={t:+.3f}")

print("\n### 종목별 개별 OOS(A/net) ###")
for sym in common.SYMBOLS:
    sub = a_oos[a_oos["symbol"] == sym]
    t, p = (sstats.ttest_1samp(sub["r"], 0.0) if len(sub) >= 2 else (np.nan, np.nan))
    print(f"  {sym:10s} n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} mean(R)={sub['r'].mean():+.4f} t={t:+.3f}")

print("\n### top-N 트레이드 제거 — A/net, OOS ###")
srt = a_oos.sort_values("r", ascending=False)
for topn in [1, 3, 5, 10, 20]:
    sub = srt.iloc[topn:]
    print(f"  top-{topn:2d} 제거 n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} sum(R)={sub['r'].sum():+.2f}"
         f"  (top-{topn} 합={srt.iloc[:topn]['r'].sum():+.2f}, 전체합={a_oos['r'].sum():+.2f})")

print("\n\n### 부호 무작위화(방향필터 부가가치) 셔플 100회 — A/net, OOS ###")
sh = su.sign_shuffle_test(a_oos["r"].to_numpy(), n_rep=100)
print(sh)

print("\n### 캘린더일 de-clustered 표본에도 셔플 적용 ###")
sh_dc = su.sign_shuffle_test(dc["r"].to_numpy(), n_rep=100)
print(sh_dc)

print("\n### gross 부호 무작위화(100회) — A/gross, OOS (비용 이전 방향정보 자체 점검) ###")
sh_g = su.sign_shuffle_test(a_oos_g["r"].to_numpy(), n_rep=100)
print(sh_g)
