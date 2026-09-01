"""2차 진단: de-clustering, no-gate 대조군, 반전 대조군, LOO, 파라미터 스윕, 종목간 상관,
손실클러스터 대칭점검, pooled(무조건부 가속) 대조군."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import common
import engine
import stats_utils as su


def split(df):
    et = pd.to_datetime(df["entry_time"])
    is_ = df[et <= common.IS_END]
    oos = df[(et >= common.OOS_START) & (et <= common.OOS_END)]
    return is_, oos


fa = common.build_funding_accel("BTCUSDT", window=60)
alts = engine.load_all_alts()

print("########## [1] de-clustering (캘린더일, gated 채택안, net) ##########")
main = pd.read_csv(common.SP / "trades_main.csv", parse_dates=["entry_time", "exit_time"])
main_gross = pd.read_csv(common.SP / "trades_main_gross.csv", parse_dates=["entry_time", "exit_time"])
_, oos_main = split(main)
_, oos_gross = split(main_gross)

dc_net = su.declustered_daily(oos_main)
dc_gross = su.declustered_daily(oos_gross)
print("net  일단위 de-clustered:", su.summarize(dc_net, "OOS net decluster"))
print("gross일단위 de-clustered:", su.summarize(dc_gross, "OOS gross decluster"))
print("고유일수:", len(dc_net), " / 명목 트레이드수:", len(oos_main))

print("\n########## [2] 종목 간 신호 동시성(같은 캘린더일 진입) ##########")
oos_main["cal_day"] = pd.to_datetime(oos_main["entry_time"]).dt.tz_convert("UTC").dt.date
per_day_syms = oos_main.groupby("cal_day")["symbol"].nunique()
print("OOS 고유일수:", oos_main["cal_day"].nunique())
print("일별 동시진입 종목수 분포:\n", per_day_syms.value_counts().sort_index())
print("6종목 전부 동시진입인 일수:", (per_day_syms == 6).sum())
print("3종목+ 동시진입인 일수:", (per_day_syms >= 3).sum())

# 위기국면(BTC 극단변동) vs 평시 상관 비교: BTC 1일 절대수익률 상위 10% 날짜를 위기일로 정의
btc15 = common.load_klines("BTCUSDT", "15m")
btc_daily = btc15["close"].resample("1D").last()
btc_ret = btc_daily.pct_change().abs()
crisis_days = set(btc_ret[btc_ret >= btc_ret.quantile(0.90)].index.date)
oos_main["is_crisis"] = oos_main["cal_day"].isin(crisis_days)
crisis_share = oos_main["is_crisis"].mean()
print(f"\nOOS 트레이드 중 BTC 위기일(상위10% |일변동|)과 겹치는 비율: {crisis_share*100:.1f}%")
# 위기일 vs 평시일 동시진입 종목수 평균
crisis_days_grp = per_day_syms[per_day_syms.index.isin(crisis_days)]
calm_days_grp = per_day_syms[~per_day_syms.index.isin(crisis_days)]
print("위기일 평균 동시진입종목수:", crisis_days_grp.mean() if len(crisis_days_grp) else float("nan"),
     " n_days=", len(crisis_days_grp))
print("평시일 평균 동시진입종목수:", calm_days_grp.mean() if len(calm_days_grp) else float("nan"),
     " n_days=", len(calm_days_grp))

print("\n########## [3] 게이트 없는 대조군 (스펙 폐기조건 c) ##########")
cfg_gate = engine.RunConfig()
cfg_nogate = engine.RunConfig(no_gate=True)
events = common.find_accel_events(fa, accel_z_threshold=1.5)
res_nogate = engine.run_all(alts, events, cfg_nogate)
all_ng = [engine.trades_to_df(t) for t in res_nogate.values()]
full_ng = pd.concat(all_ng, ignore_index=True) if all_ng else pd.DataFrame()
full_ng.to_csv(common.SP / "trades_nogate.csv", index=False)
is_ng, oos_ng = split(full_ng)
print("no-gate 전체 n:", len(full_ng))
print("no-gate OOS:", su.summarize(oos_ng["r_multiple"].to_numpy(), "no-gate OOS"))
print("gated   OOS:", su.summarize(oos_main["r_multiple"].to_numpy(), "gated OOS"))

# 표본수 맞춘 부트스트랩: gated(n=787)이 no-gate 풀(대조군)에서 몇 백분위인지
overlap_conf_times = set(zip(main["symbol"], main["confirm_time"])) if "confirm_time" in main else set()
ng_conf_times = set(zip(full_ng["symbol"], full_ng["confirm_time"]))
gated_conf_times = set(zip(main["symbol"], main["confirm_time"]))
overlap_n = len(gated_conf_times & ng_conf_times)
print(f"\ngated ⊆ no-gate 겹침: {overlap_n}/{len(gated_conf_times)} = "
     f"{overlap_n/max(len(gated_conf_times),1)*100:.1f}% (gated 기준)")
print(f"no-gate 풀 대비 겹침 비율: {overlap_n/max(len(ng_conf_times),1)*100:.1f}% (no-gate 기준)")

bs = su.bootstrap_diff_matched_n(oos_main["r_multiple"].to_numpy(), oos_ng["r_multiple"].to_numpy(),
                                 n_match=len(oos_main), n_iter=200,
                                 seed=su.seed_from_str("bfll_gate_vs_nogate"))
print("gated(OOS) 평균 R이 no-gate 리샘플 분포에서의 백분위:", bs["percentile"],
     " gated mean:", bs["a_mean"], " no-gate resample mean:", bs["b_means_mean"])

# 비중첩 표본만의 독립 Welch
gated_only_mask = ~oos_main.set_index(["symbol", "confirm_time"]).index.isin(
    pd.MultiIndex.from_tuples(ng_conf_times))
oos_main_idx = oos_main.set_index(["symbol", "confirm_time"], drop=False)
gated_nonoverlap = oos_main_idx[~oos_main_idx.index.isin(pd.MultiIndex.from_tuples(ng_conf_times))]
ng_only = full_ng.set_index(["symbol", "confirm_time"], drop=False)
ng_only_oos = split(ng_only)[1]
ng_nonoverlap = ng_only_oos[~ng_only_oos.index.isin(pd.MultiIndex.from_tuples(gated_conf_times))]
print("비중첩 gated n:", len(gated_nonoverlap), " 비중첩 no-gate n:", len(ng_nonoverlap))
w = su.welch_t(gated_nonoverlap["r_multiple"].to_numpy(), ng_nonoverlap["r_multiple"].to_numpy())
print("비중첩 독립 Welch t검정(gated vs no-gate):", w)

print("\n########## [4] pooled(무조건부 가속, z=0) 대조군 ##########")
events_z0 = common.find_accel_events(fa, accel_z_threshold=0.0)
print("z=0(무조건부) 트리거 이벤트 수:", len(events_z0), " (z>=1.5 대비:", len(events), ")")
res_z0 = engine.run_all(alts, events_z0, cfg_gate)
all_z0 = [engine.trades_to_df(t) for t in res_z0.values()]
full_z0 = pd.concat(all_z0, ignore_index=True) if all_z0 else pd.DataFrame()
full_z0.to_csv(common.SP / "trades_z0.csv", index=False)
is_z0, oos_z0 = split(full_z0)
print("pooled(z=0) OOS:", su.summarize(oos_z0["r_multiple"].to_numpy(), "pooled OOS"))
print("gated(z=1.5) OOS:", su.summarize(oos_main["r_multiple"].to_numpy(), "gated OOS"))
bs2 = su.bootstrap_diff_matched_n(oos_main["r_multiple"].to_numpy(), oos_z0["r_multiple"].to_numpy(),
                                  n_match=len(oos_main), n_iter=200,
                                  seed=su.seed_from_str("bfll_gate_vs_pooled"))
print("gated 평균 R이 pooled 리샘플 분포에서의 백분위:", bs2["percentile"])

print("\n########## [5] 반전 대조군 ##########")
cfg_rev = engine.RunConfig(reverse=True)
res_rev = engine.run_all(alts, events, cfg_rev)
all_rev = [engine.trades_to_df(t) for t in res_rev.values()]
full_rev = pd.concat(all_rev, ignore_index=True) if all_rev else pd.DataFrame()
full_rev.to_csv(common.SP / "trades_reverse.csv", index=False)
_, oos_rev = split(full_rev)
print("반전 OOS:", su.summarize(oos_rev["r_multiple"].to_numpy(), "reverse OOS"))
print("정방향 OOS:", su.summarize(oos_main["r_multiple"].to_numpy(), "forward OOS"))
print("반전 청산사유 분포:\n", full_rev["exit_reason"].value_counts())
print("반전 holding_bars 분포: mean=", full_rev["holding_bars"].mean(),
     " median=", full_rev["holding_bars"].median(),
     " zero_hold_frac=", (full_rev["holding_bars"] == 0).mean())
print("정방향 holding_bars 분포: mean=", main["holding_bars"].mean(),
     " median=", main["holding_bars"].median(),
     " zero_hold_frac=", (main["holding_bars"] == 0).mean())

print("\n########## [6] LOO(종목별 제외) OOS ##########")
for sym in common.ALT_SYMBOLS:
    sub = oos_main[oos_main["symbol"] != sym]
    print(f"  {sym} 제외:", su.summarize(sub["r_multiple"].to_numpy(), f"LOO-{sym}"))

print("\n########## [7] top-N 제거(최대 승리 트레이드) ##########")
r = oos_main["r_multiple"].to_numpy()
order = np.argsort(-r)
for topn in [1, 3, 5, 10, 20]:
    if topn >= len(r):
        continue
    rest = np.delete(r, order[:topn])
    print(f"  top-{topn} 제거:", su.summarize(rest, f"top{topn}removed"))

print("\n########## [8] 손실 클러스터 대칭점검(최악 트레이드 제거) ##########")
order_loss = np.argsort(r)   # 오름차순(가장 손실 큰 것부터)
for topn in [1, 3, 5, 10, 20]:
    if topn >= len(r):
        continue
    rest = np.delete(r, order_loss[:topn])
    print(f"  최악 {topn}건 제거:", su.summarize(rest, f"worst{topn}removed"))

print("\n########## [9] 5일 롤링 클러스터 점검 ##########")
oos_main_sorted = oos_main.sort_values("entry_time").reset_index(drop=True)
oos_main_sorted["entry_time"] = pd.to_datetime(oos_main_sorted["entry_time"])
oos_main_sorted["block5"] = (oos_main_sorted["entry_time"] - oos_main_sorted["entry_time"].min()
                             ).dt.days // 5
block_sum = oos_main_sorted.groupby("block5")["r_multiple"].sum().sort_values(ascending=False)
total_sum = oos_main_sorted["r_multiple"].sum()
print("총 OOS 순 R:", total_sum)
print("최대 기여 5일 블록 top5:\n", block_sum.head(5))
top3_blocks_share = block_sum.head(3).sum() / total_sum if total_sum != 0 else float("nan")
print("상위 3개 5일블록이 차지하는 비율:", top3_blocks_share)
