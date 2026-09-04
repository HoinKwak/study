"""필수 진단 일괄 실행 — de-clustering(캘린더일+3~5일롤링, net+gross)/LOO/top-N/shuffle."""
import pickle

import numpy as np
from scipy import stats as sstats

import common
import stats_utils as su

with open(common.SP / "results_main.pkl", "rb") as f:
    results = pickle.load(f)

a_net = results[(False, True)]
a_gross = results[(False, False)]

_, a_oos, _ = su.split_is_oos(a_net)
_, a_oos_g, _ = su.split_is_oos(a_gross)

print("### de-clustering (net, OOS) — 캘린더일 단위 ###")
dc = su.decluster_calendar_day(a_oos)
t, p = sstats.ttest_1samp(dc["r"], 0.0) if len(dc) >= 2 else (np.nan, np.nan)
print(f"  명목 n={len(a_oos)} -> 고유 캘린더일 n={len(dc)}  PF(R)={su.pf_r(dc):.3f} "
     f"mean(R)={dc['r'].mean():+.4f} t={t:+.3f} p={p:.4g}")

print("\n### de-clustering (net, OOS) — 3~5일 롤링 윈도우 ###")
for wd in [3, 4, 5]:
    dr = su.decluster_rolling_days(a_oos, window_days=wd)
    t, p = sstats.ttest_1samp(dr["r"], 0.0) if len(dr) >= 2 else (np.nan, np.nan)
    print(f"  window={wd}d -> 고유클러스터 n={len(dr)}  PF(R)={su.pf_r(dr):.3f} "
         f"mean(R)={dr['r'].mean():+.4f} t={t:+.3f} p={p:.4g}")

print("\n### de-clustering — gross(fee=0) 도 동일 처리(캘린더일 + 3~5일 롤링) ###")
dcg = su.decluster_calendar_day(a_oos_g)
t, p = sstats.ttest_1samp(dcg["r"], 0.0) if len(dcg) >= 2 else (np.nan, np.nan)
print(f"  캘린더일 n={len(dcg)} PF(R)={su.pf_r(dcg):.3f} mean(R)={dcg['r'].mean():+.4f} "
     f"t={t:+.3f} p={p:.4g}")
for wd in [3, 4, 5]:
    drg = su.decluster_rolling_days(a_oos_g, window_days=wd)
    t, p = sstats.ttest_1samp(drg["r"], 0.0) if len(drg) >= 2 else (np.nan, np.nan)
    print(f"  window={wd}d(gross) -> n={len(drg)} PF(R)={su.pf_r(drg):.3f} "
         f"mean(R)={drg['r'].mean():+.4f} t={t:+.3f} p={p:.4g}")

print("\n\n### LOO(symbol) — net, OOS ###")
for sym in common.SYMBOLS:
    sub = a_oos[a_oos["symbol"] != sym]
    t, p = (sstats.ttest_1samp(sub["r"], 0.0) if len(sub) >= 2 else (np.nan, np.nan))
    print(f"  {sym} 제외 n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} mean(R)={sub['r'].mean():+.4f} t={t:+.3f}")

print("\n### 종목별 개별 OOS(net) ###")
for sym in common.SYMBOLS:
    sub = a_oos[a_oos["symbol"] == sym]
    t, p = (sstats.ttest_1samp(sub["r"], 0.0) if len(sub) >= 2 else (np.nan, np.nan))
    print(f"  {sym:10s} n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} mean(R)={sub['r'].mean():+.4f} t={t:+.3f}")

print("\n### top-N 트레이드 제거 — net, OOS ###")
srt = a_oos.sort_values("r", ascending=False)
for topn in [1, 3, 5, 10, 20, 50]:
    sub = srt.iloc[topn:]
    print(f"  top-{topn:2d} 제거 n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} sum(R)={sub['r'].sum():+.2f}"
         f"  (top-{topn} 합={srt.iloc[:topn]['r'].sum():+.2f}, 전체합={a_oos['r'].sum():+.2f})")

print("\n\n### 부호 무작위화(방향 부가가치) 셔플 100회 — net, OOS ###")
sh = su.sign_shuffle_test(a_oos["r"].to_numpy(), n_rep=100)
print(sh)

print("\n### gross 부호 무작위화(100회) — 비용 이전 방향정보 자체 점검 ###")
sh_g = su.sign_shuffle_test(a_oos_g["r"].to_numpy(), n_rep=100)
print(sh_g)

print("\n\n### 청산사유 분포(net, OOS) ###")
print(a_oos["reason"].value_counts())
print("\n### holding_bars 분포(net, OOS) ###")
print(a_oos["holding_bars"].describe())
zero_hold_frac = (a_oos["holding_bars"] == 0).mean()
print(f"zero_hold_frac(진입봉 즉시청산) = {zero_hold_frac:.4f}")

print("\n### 방향 분포(net, OOS) ###")
print(a_oos["direction"].value_counts())
