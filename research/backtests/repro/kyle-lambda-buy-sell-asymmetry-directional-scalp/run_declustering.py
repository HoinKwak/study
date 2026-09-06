"""de-clustering(캘린더일·3~5일 롤링) — net·gross 둘 다 병행. + 위기국면(BTC 절대수익률 상위 5%)
de-clustering(사전 폐기조건 g)."""
import pickle

import numpy as np
import pandas as pd

import common
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

for fee_on in [True, False]:
    df = results[("base", fee_on)]
    _, oos_df, _ = su.split_is_oos(df)
    label = f"base/{'net' if fee_on else 'gross'}"
    print(f"\n=== {label} OOS de-clustering ===")
    print(" 원본(트레이드 단위):", su.print_summary(su.summary(oos_df, "raw")))
    cal = su.decluster_calendar_day(oos_df)
    print(" 캘린더일:          ", su.print_summary(su.summary(cal, "cal_day")))
    for w in (3, 4, 5):
        roll = su.decluster_rolling_days(oos_df, window_days=w)
        print(f" {w}일 롤링:          ", su.print_summary(su.summary(roll, f"roll{w}d")))

# --- 위기국면(사전 폐기조건 g): BTC 절대수익률 상위 5% de-clustering 후 t<1.5 이면 매크로패닉 의존 ---
print("\n=== 위기국면(BTC 절대 15m 수익률 상위 5%) de-clustering(사전 폐기조건 g) ===")
with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)
btc = sigs["BTCUSDT"].df15m["close"]
daily_close = btc.resample("1D").last()
daily_ret = daily_close.pct_change().abs()
thresh = daily_ret.quantile(0.95)
crisis_days = set(daily_ret[daily_ret >= thresh].index.floor("D"))
print(f" BTC 일간(종가기준) |수익률| 95%ile 임계={thresh*100:.3f}%  위기 캘린더일수(전체이력)={len(crisis_days)}")

df_net = results[("base", True)]
_, oos_net, _ = su.split_is_oos(df_net)
oos_net = oos_net.copy()
oos_net["cal_day"] = oos_net["entry_time"].dt.floor("D")
is_crisis = oos_net["cal_day"].isin(crisis_days)
print(" 위기일 트레이드:  ", su.print_summary(su.summary(oos_net[is_crisis], "crisis")))
print(" 평시일 트레이드:  ", su.print_summary(su.summary(oos_net[~is_crisis], "normal")))
# 캘린더일 de-clustering 후에도 위기일이 여전히 별도로 큰 비중인지 실측
cal = su.decluster_calendar_day(oos_net)
cal["is_crisis"] = cal["entry_time"].isin(crisis_days)
print(" [캘린더일 de-cluster 후] 위기일:", su.print_summary(su.summary(cal[cal["is_crisis"]], "cal_crisis")))
print(" [캘린더일 de-cluster 후] 평시일:", su.print_summary(su.summary(cal[~cal["is_crisis"]], "cal_normal")))
