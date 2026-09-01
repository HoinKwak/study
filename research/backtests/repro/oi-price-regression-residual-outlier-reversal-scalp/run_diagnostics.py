"""사전 폐기조건 (b)(d) 및 나머지 필수 진단 일괄 실행 — de-clustering/LOO/top-N/shuffle/부트스트랩."""
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiresid")
import common
import engine
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

resid_a_net = results[("resid", "A", True)]
resid_a_gross = results[("resid", "A", False)]
oiz_a_net = results[("oi_zscore", "A", True)]
oiz_a_gross = results[("oi_zscore", "A", False)]

_, resid_a_oos, _ = su.split_is_oos(resid_a_net)
_, oiz_a_oos, _ = su.split_is_oos(oiz_a_net)
_, resid_a_oos_g, _ = su.split_is_oos(resid_a_gross)
_, oiz_a_oos_g, _ = su.split_is_oos(oiz_a_gross)

print("### (d) 핵심대조군(oi_zscore) 대비 우월성 부트스트랩 — OOS net R ###")
bd = su.bootstrap_diff_test(resid_a_oos["r"].to_numpy(), oiz_a_oos["r"].to_numpy())
print(bd, "  (p_a_better 가 클수록 resid 가 oi_zscore 보다 우수하지 않다는 뜻)")

print("\n### (d) 표본수 맞춘 부트스트랩 (pool=resid, base=oi_zscore 크기로) ###")
mn = su.bootstrap_matched_n_diff(resid_a_oos["r"].to_numpy(), oiz_a_oos["r"].to_numpy())
print(mn)

print("\n### base⊆pool 중복 검정력 이슈 대응 — 겹치지 않는 잔여표본 독립검정 ###")
ip = su.independent_pair_diff(resid_a_oos, oiz_a_oos)
print(ip)

print("\n### gross 도 동일 비교(비용 이전부터 우위 있는지) ###")
bd_g = su.bootstrap_diff_test(resid_a_oos_g["r"].to_numpy(), oiz_a_oos_g["r"].to_numpy())
print(bd_g)

print("\n\n### de-clustering (resid/A/net, OOS) — 캘린더일 단위 ###")
dc = su.decluster_calendar_day(resid_a_oos)
t, p = (np.nan, np.nan)
from scipy import stats as sstats
if len(dc) >= 2:
    t, p = sstats.ttest_1samp(dc["r"], 0.0)
print(f"  명목 n={len(resid_a_oos)} -> 고유 캘린더일 n={len(dc)}  PF(R)={su.pf_r(dc):.3f} "
     f"mean(R)={dc['r'].mean():+.4f} t={t:+.3f} p={p:.4f}")

print("\n### de-clustering (resid/A/net, OOS) — 3~5일 롤링 윈도우 ###")
for wd in [3, 4, 5]:
    dr = su.decluster_rolling_days(resid_a_oos, window_days=wd)
    if len(dr) >= 2:
        t, p = sstats.ttest_1samp(dr["r"], 0.0)
    else:
        t, p = np.nan, np.nan
    print(f"  window={wd}d -> 고유클러스터 n={len(dr)}  PF(R)={su.pf_r(dr):.3f} "
         f"mean(R)={dr['r'].mean():+.4f} t={t:+.3f} p={p:.4f}")

print("\n### de-clustering — gross(fee=0) 도 동일 처리 ###")
dcg = su.decluster_calendar_day(resid_a_oos_g)
if len(dcg) >= 2:
    t, p = sstats.ttest_1samp(dcg["r"], 0.0)
else:
    t, p = np.nan, np.nan
print(f"  gross 캘린더일 n={len(dcg)} PF(R)={su.pf_r(dcg):.3f} mean(R)={dcg['r'].mean():+.4f} "
     f"t={t:+.3f} p={p:.4f}")

print("\n\n### LOO(symbol) — resid/A/net, OOS ###")
for sym in common.SYMBOLS:
    sub = resid_a_oos[resid_a_oos["symbol"] != sym]
    print(f"  {sym} 제외 n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} mean(R)={sub['r'].mean():+.4f}")

print("\n### top-N 트레이드 제거 — resid/A/net, OOS ###")
srt = resid_a_oos.sort_values("r", ascending=False)
for topn in [1, 3, 5, 10, 20]:
    sub = srt.iloc[topn:]
    print(f"  top-{topn:2d} 제거 n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} sum(R)={sub['r'].sum():+.2f}"
         f"  (top-{topn} 합={srt.iloc[:topn]['r'].sum():+.2f}, 전체합={resid_a_oos['r'].sum():+.2f})")

print("\n\n### 부호 무작위화 셔플 100회 — resid/A/net, OOS ###")
sh = su.sign_shuffle_test(resid_a_oos["r"].to_numpy(), n_rep=100)
print(sh)

print("\n### 캘린더일 de-clustered 표본에도 셔플 적용 ###")
sh_dc = su.sign_shuffle_test(dc["r"].to_numpy(), n_rep=100)
print(sh_dc)
