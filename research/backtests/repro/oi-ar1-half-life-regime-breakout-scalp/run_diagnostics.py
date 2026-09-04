"""필수 진단 일괄 실행 — de-clustering/LOO/top-N/셔플/부트스트랩(gross 포함), 반전·대조군 비교."""
import pickle
import sys

import numpy as np
import pandas as pd
from scipy import stats as sstats

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiar1hl")
import common
import engine
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

phi_net = results[("phi_hi", True)]
phi_gross = results[("phi_hi", False)]
none_net = results[("none", True)]
none_gross = results[("none", False)]
oiz_net = results[("oiz_hi", True)]
philo_net = results[("phi_lo", True)]
rev_net = results[("reverse", True)]

_, phi_oos, _ = su.split_is_oos(phi_net)
_, phi_oos_g, _ = su.split_is_oos(phi_gross)
_, none_oos, _ = su.split_is_oos(none_net)
_, none_oos_g, _ = su.split_is_oos(none_gross)
_, oiz_oos, _ = su.split_is_oos(oiz_net)
_, philo_oos, _ = su.split_is_oos(philo_net)
_, rev_oos, _ = su.split_is_oos(rev_net)

print("### 핵심 대조군① 게이트 없는 순수 Donchian — OOS net 부트스트랩 우월성(phi_hi vs none) ###")
bd = su.bootstrap_diff_test(phi_oos["r"].to_numpy(), none_oos["r"].to_numpy())
print(bd, "  (p_a_better 가 클수록 게이트 없는 대조군이 phi_hi 보다 열등하지 않다는 뜻)")

print("\n### base(phi_hi)⊆pool(none) 중복도 — 겹치지 않는 잔여표본 독립검정 ###")
ip = su.independent_pair_diff(phi_oos, none_oos)
print(ip)

print("\n### 표본수 맞춘 부트스트랩(스펙 사전폐기조건 b) — none 표본에서 phi_hi n 만큼 리샘플, "
     "phi_hi mean(R) 이 그 분포에서 몇 백분위인지 ###")
mn = su.bootstrap_matched_n_diff(none_oos["r"].to_numpy(), phi_oos["r"].to_numpy())
print(mn, "  (50 백분위 근방이면 게이트가 무가치, p 값은 min(pctile,100-pctile)/100*2 로 근사)")

print("\n### 핵심 대조군② OI z-score 게이트(동어반복/부가가치 점검, phi_hi vs oiz_hi) — OOS net ###")
bd2 = su.bootstrap_diff_test(phi_oos["r"].to_numpy(), oiz_oos["r"].to_numpy())
print(bd2)
print(su.print_summary(su.summary(oiz_oos, "oiz_hi/net OOS")))

print("\n### 핵심 대조군③ phi 낮은 레짐(가설 방향성 점검, phi_hi vs phi_lo) — OOS net ###")
print(su.print_summary(su.summary(philo_oos, "phi_lo/net OOS")))

print("\n### 핵심 대조군④ 방향반전 — OOS net (phi_hi vs reverse) ###")
print(su.print_summary(su.summary(rev_oos, "reverse/net OOS")))
bd4 = su.bootstrap_diff_test(phi_oos["r"].to_numpy(), rev_oos["r"].to_numpy())
print(bd4)
print("  reverse reason 분포:", rev_oos["reason"].value_counts().to_dict())
print(f"  reverse zero_hold_frac={(rev_oos['holding_bars']==0).mean()*100:.2f}%  "
     f"mean_hold={rev_oos['holding_bars'].mean():.2f}봉  (정방향 대비 비교)")
print(f"  정방향(phi_hi) zero_hold_frac={(phi_oos['holding_bars']==0).mean()*100:.2f}%  "
     f"mean_hold={phi_oos['holding_bars'].mean():.2f}봉")

print("\n\n### de-clustering (phi_hi/net, OOS) — 캘린더일 단위 ###")
dc = su.decluster_calendar_day(phi_oos)
if len(dc) >= 2:
    t, p = sstats.ttest_1samp(dc["r"], 0.0)
else:
    t, p = np.nan, np.nan
print(f"  명목 n={len(phi_oos)} -> 고유 캘린더일 n={len(dc)}  PF(R)={su.pf_r(dc):.3f} "
     f"mean(R)={dc['r'].mean():+.4f} t={t:+.3f} p={p:.4f}")

print("\n### de-clustering (phi_hi/net, OOS) — 3~5일 롤링 윈도우 ###")
for wd in [3, 4, 5]:
    dr = su.decluster_rolling_days(phi_oos, window_days=wd)
    if len(dr) >= 2:
        t, p = sstats.ttest_1samp(dr["r"], 0.0)
    else:
        t, p = np.nan, np.nan
    print(f"  window={wd}d -> 고유클러스터 n={len(dr)}  PF(R)={su.pf_r(dr):.3f} "
         f"mean(R)={dr['r'].mean():+.4f} t={t:+.3f} p={p:.4f}")

print("\n### de-clustering — gross(fee=0) 도 동일 처리(캘린더일 + 3~5일 롤링) ###")
dcg = su.decluster_calendar_day(phi_oos_g)
if len(dcg) >= 2:
    t, p = sstats.ttest_1samp(dcg["r"], 0.0)
else:
    t, p = np.nan, np.nan
print(f"  gross 캘린더일 n={len(dcg)} PF(R)={su.pf_r(dcg):.3f} mean(R)={dcg['r'].mean():+.4f} "
     f"t={t:+.3f} p={p:.4f}")
for wd in [3, 4, 5]:
    drg = su.decluster_rolling_days(phi_oos_g, window_days=wd)
    if len(drg) >= 2:
        t, p = sstats.ttest_1samp(drg["r"], 0.0)
    else:
        t, p = np.nan, np.nan
    print(f"  gross window={wd}d -> 고유클러스터 n={len(drg)}  PF(R)={su.pf_r(drg):.3f} "
         f"mean(R)={drg['r'].mean():+.4f} t={t:+.3f} p={p:.4f}")

print("\n\n### LOO(symbol) — phi_hi/net, OOS ###")
for sym in common.SYMBOLS:
    sub = phi_oos[phi_oos["symbol"] != sym]
    t, p = (sstats.ttest_1samp(sub["r"], 0.0) if len(sub) >= 2 else (np.nan, np.nan))
    print(f"  {sym} 제외 n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} mean(R)={sub['r'].mean():+.4f} t={t:+.3f}")

print("\n### 종목별 개별 OOS(phi_hi/net) ###")
for sym in common.SYMBOLS:
    sub = phi_oos[phi_oos["symbol"] == sym]
    t, p = (sstats.ttest_1samp(sub["r"], 0.0) if len(sub) >= 2 else (np.nan, np.nan))
    print(f"  {sym:10s} n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} mean(R)={sub['r'].mean():+.4f} t={t:+.3f}")

print("\n### top-N 트레이드 제거 — phi_hi/net, OOS ###")
srt = phi_oos.sort_values("r", ascending=False)
for topn in [1, 3, 5, 10, 20]:
    sub = srt.iloc[topn:]
    print(f"  top-{topn:2d} 제거 n={len(sub):4d} PF(R)={su.pf_r(sub):.3f} sum(R)={sub['r'].sum():+.2f}"
         f"  (top-{topn} 합={srt.iloc[:topn]['r'].sum():+.2f}, 전체합={phi_oos['r'].sum():+.2f})")

print("\n\n### 부호 무작위화(방향/게이트 부가가치) 셔플 100회 — phi_hi/net, OOS ###")
sh = su.sign_shuffle_test(phi_oos["r"].to_numpy(), n_rep=100)
print(sh)

print("\n### 캘린더일 de-clustered 표본에도 셔플 적용 ###")
sh_dc = su.sign_shuffle_test(dc["r"].to_numpy(), n_rep=100)
print(sh_dc)

print("\n### gross 부호 무작위화(100회) — phi_hi/gross, OOS (비용 이전 방향정보 자체 점검) ###")
sh_g = su.sign_shuffle_test(phi_oos_g["r"].to_numpy(), n_rep=100)
print(sh_g)

print("\n\n### 종목 간 신호 상관 — 동시진입일 비율(캘린더일 + 3~5일 롤링) ###")
d = phi_oos.copy()
d["cal_day"] = d["entry_time"].dt.floor("D")
per_day_syms = d.groupby("cal_day")["symbol"].nunique()
print("  캘린더일당 진입종목수 분포:", per_day_syms.value_counts().sort_index().to_dict())
print(f"  동시(2종목+) 진입일 비율: {(per_day_syms>=2).mean()*100:.1f}%  "
     f"(7종목 전부 동시): {(per_day_syms>=7).mean()*100:.2f}%")
for wd in [3, 4, 5]:
    dr = phi_oos.sort_values("entry_time").copy()
    cluster_id = []
    cur_id = 0; last_time = None
    for t in dr["entry_time"]:
        if last_time is None or (t - last_time) > pd.Timedelta(days=wd):
            cur_id += 1
        cluster_id.append(cur_id); last_time = t
    dr["cluster"] = cluster_id
    nsym = dr.groupby("cluster")["symbol"].nunique()
    print(f"  {wd}일 롤링클러스터 {len(nsym)}개, 2종목+ 비율={((nsym>=2).mean()*100):.1f}%, "
         f"최대 종목수={nsym.max()}")
