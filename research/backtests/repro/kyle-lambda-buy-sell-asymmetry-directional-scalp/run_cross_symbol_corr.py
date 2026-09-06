"""종목 간 신호 상관(평시 vs 위기국면) — 스펙 §종목 간 신호 상관 사전 예상 검증."""
import pickle

import numpy as np
import pandas as pd

import common
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)
with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

df = results[("base", True)]
_, oos_df, _ = su.split_is_oos(df)

btc = sigs["BTCUSDT"].df15m["close"]
daily_close = btc.resample("1D").last()
daily_ret = daily_close.pct_change().abs()
thresh = daily_ret.quantile(0.95)
crisis_days = set(daily_ret[daily_ret >= thresh].index.floor("D"))

oos_df = oos_df.copy()
oos_df["cal_day"] = oos_df["entry_time"].dt.floor("D")

all_days = pd.date_range(common.OOS_START.floor("D"), common.OOS_END.floor("D"), freq="D", tz="UTC")
ind = pd.DataFrame(index=all_days)
for sym in common.SYMBOLS:
    days_with_entry = set(oos_df.loc[oos_df["symbol"] == sym, "cal_day"])
    ind[sym] = [1 if d in days_with_entry else 0 for d in all_days]

is_crisis = pd.Series([d in crisis_days for d in all_days], index=all_days)

corr_all = ind.corr()
corr_normal = ind[~is_crisis].corr()
corr_crisis = ind[is_crisis].corr()


def avg_offdiag(c):
    n = len(c)
    return (c.to_numpy().sum() - n) / (n * n - n)


print(f"평시일수={int((~is_crisis).sum())} 위기일수={int(is_crisis.sum())}")
print(f"진입-일 지시자 평균 종목간 상관: 전체={avg_offdiag(corr_all):.4f} "
     f"평시={avg_offdiag(corr_normal):.4f} 위기={avg_offdiag(corr_crisis):.4f}")
