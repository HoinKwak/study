"""메인 실행: base(net/gross) + 대조군(c)(d) + 반전 + de-clustering + 셔플 + 스윕 + LOO + top-N.
결과를 pickle 로 캐시(results_main.pkl)해 이후 리뷰/재분석에서 재사용."""
import pickle
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd

import common
import engine
import stats_utils as su

t0 = time.time()
print("시그널 빌드 중...")
sig_all = engine.load_all_signals()
for s, sig in sig_all.items():
    print(f"  {s}: h1={len(sig.h1)} h4={len(sig.h4)} d1={len(sig.d1)}")

configs = {
    "base": engine.RunConfig(),
    "base_gross": engine.RunConfig(cost_on=False),
    "ctrl_c_h1only": engine.RunConfig(signal_mode="h1_only"),
    "ctrl_c_h1only_gross": engine.RunConfig(signal_mode="h1_only", cost_on=False),
    "ctrl_d_h4d1": engine.RunConfig(signal_mode="h4_d1_only"),
    "ctrl_d_h4d1_gross": engine.RunConfig(signal_mode="h4_d1_only", cost_on=False),
    "reverse": engine.RunConfig(direction_mode="reverse"),
    "reverse_gross": engine.RunConfig(direction_mode="reverse", cost_on=False),
    "reverse_nochand": engine.RunConfig(direction_mode="reverse", disable_chandelier=True),
}

results = {}
for name, cfg in configs.items():
    trades = engine.run_all(sig_all, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    results[name] = df
    print(f"{name}: n_total={len(df)}")

with open(common.SP / "results_main.pkl", "wb") as f:
    pickle.dump(results, f)

print(f"\n완료 {time.time()-t0:.1f}s")

print("\n=== base(net) IS/OOS/FULL ===")
is_df, oos_df, full_df = su.split_is_oos(results["base"])
print(su.fmt(su.summary(is_df, "IS")))
print(su.fmt(su.summary(oos_df, "OOS")))
print(su.fmt(su.summary(full_df, "FULL")))
print("IS+OOS 정합:", len(is_df) + len(oos_df) == len(full_df), len(is_df), len(oos_df), len(full_df))

print("\n=== base(gross) IS/OOS/FULL ===")
is_g, oos_g, full_g = su.split_is_oos(results["base_gross"])
print(su.fmt(su.summary(is_g, "IS-gross")))
print(su.fmt(su.summary(oos_g, "OOS-gross")))
print(su.fmt(su.summary(full_g, "FULL-gross")))

print("\n=== 종목별 OOS(net) ===")
for sym in common.SYMBOLS:
    d = oos_df[oos_df["symbol"] == sym]
    print(su.fmt(su.summary(d, sym)))

print("\n=== 대조군 (c) 1h 단독 게이트 ===")
is_c, oos_c, full_c = su.split_is_oos(results["ctrl_c_h1only"])
print(su.fmt(su.summary(is_c, "IS-c(h1only)")))
print(su.fmt(su.summary(oos_c, "OOS-c(h1only)")))
_isg, oosg_c, _fg = su.split_is_oos(results["ctrl_c_h1only_gross"])
print(su.fmt(su.summary(oosg_c, "OOS-c(h1only)-gross")))

print("\n=== 대조군 (d) 4h+1d(1h 제거) ===")
is_d, oos_d, full_d = su.split_is_oos(results["ctrl_d_h4d1"])
print(su.fmt(su.summary(is_d, "IS-d(h4d1)")))
print(su.fmt(su.summary(oos_d, "OOS-d(h4d1)")))
_isg2, oosg_d, _fg2 = su.split_is_oos(results["ctrl_d_h4d1_gross"])
print(su.fmt(su.summary(oosg_d, "OOS-d(h4d1)-gross")))

print("\n=== 반전 대조군 ===")
is_r, oos_r, full_r = su.split_is_oos(results["reverse"])
print(su.fmt(su.summary(is_r, "IS-reverse")))
print(su.fmt(su.summary(oos_r, "OOS-reverse")))
is_rg, oos_rg, full_rg = su.split_is_oos(results["reverse_gross"])
print(su.fmt(su.summary(oos_rg, "OOS-reverse-gross")))
is_rn, oos_rn, full_rn = su.split_is_oos(results["reverse_nochand"])
print(su.fmt(su.summary(oos_rn, "OOS-reverse-nochand(3rd alt)")))

print("\n반전 청산사유 분포(OOS):")
print(oos_r["reason"].value_counts())
print("반전 보유봉수 분포(OOS): mean=%.2f median=%.1f, 1봉이내청산비율=%.1f%%" % (
    oos_r["holding_bars"].mean(), oos_r["holding_bars"].median(),
    (oos_r["holding_bars"] <= 1).mean() * 100))
print("정방향 청산사유 분포(OOS):")
print(oos_df["reason"].value_counts())
print("정방향 보유봉수 분포(OOS): mean=%.2f median=%.1f, 1봉이내청산비율=%.1f%%" % (
    oos_df["holding_bars"].mean(), oos_df["holding_bars"].median(),
    (oos_df["holding_bars"] <= 1).mean() * 100))

print("\n=== de-clustering (base net, OOS) ===")
print(su.fmt(su.summary(oos_df, "원본(OOS)")))
cal = su.decluster_calendar_day(oos_df)
print(su.fmt(su.summary(cal, "캘린더일")))
for w in [3, 4, 5]:
    roll = su.decluster_rolling_days(oos_df, window_days=w)
    print(su.fmt(su.summary(roll, f"{w}일롤링")))

print("\n=== de-clustering (base gross, OOS) — gross t 도 동일 de-clustering 적용 ===")
print(su.fmt(su.summary(oos_g, "원본(OOS-gross)")))
cal_g = su.decluster_calendar_day(oos_g)
print(su.fmt(su.summary(cal_g, "캘린더일-gross")))
for w in [3, 4, 5]:
    roll_g = su.decluster_rolling_days(oos_g, window_days=w)
    print(su.fmt(su.summary(roll_g, f"{w}일롤링-gross")))

print("\n=== 동시진입일 비율(OOS, 7종목) ===")
d = oos_df.copy()
d["cal_day"] = d["entry_time"].dt.floor("D")
sym_per_day = d.groupby("cal_day")["symbol"].nunique()
print("고유일수:", len(sym_per_day), "명목건수:", len(d))
print("일별 동시종목수 분포:\n", sym_per_day.value_counts().sort_index())

print("\n=== 5일 롤링 최대 클러스터 기여도(OOS, base net) ===")
roll5 = su.decluster_rolling_days(oos_df, window_days=5)
roll5_sorted = roll5.assign(contrib=lambda x: x["r"] * x["n"]).sort_values("contrib", ascending=False)
total_sum_r = oos_df["r"].sum()
print("총 클러스터수:", len(roll5), "총 R합:", round(total_sum_r, 2))
print(roll5_sorted.head(5)[["entry_time", "n", "r", "contrib"]])
top3_contrib = roll5_sorted.head(3)["contrib"].sum()
print(f"top-3 클러스터 기여 비율: {top3_contrib/total_sum_r*100:.1f}%")

print(f"\n총 소요 {time.time()-t0:.1f}s")
