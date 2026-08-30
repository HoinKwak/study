"""종목 간 신호 상관: 평시 평균 vs 위기 국면(BTC 절대 일간수익률 상위 5%) 꼬리 상관."""
import pickle
import sys

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiskew")
import numpy as np
import pandas as pd
import common

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)
gated = results["gated"]

# 일별 이진 신호 지표(진입 발생 여부) 심볼별
d = gated.copy()
d["cal_day"] = d["entry_time"].dt.floor("D")

btc = common.load_klines_4h("BTCUSDT")
btc_daily = btc["close"].resample("1D").last()
btc_ret = btc_daily.pct_change()

all_days = pd.date_range(common.IS_START.floor("D"), common.OOS_END.floor("D"), freq="D", tz="UTC")
ind = pd.DataFrame(0, index=all_days, columns=common.SYMBOLS)
for sym in common.SYMBOLS:
    days = d.loc[d.symbol == sym, "cal_day"].unique()
    ind.loc[ind.index.isin(days), sym] = 1

print("=== 평시 전체 상관(일별 이진 신호 발생 여부) ===")
corr_full = ind.corr()
print(corr_full.round(3))

btc_ret_aligned = btc_ret.reindex(all_days)
thr = btc_ret_aligned.abs().quantile(0.95)
crisis_days = btc_ret_aligned[btc_ret_aligned.abs() >= thr].index
print(f"\n위기일수(BTC |일간수익률| 상위5%) = {len(crisis_days)}, 임계 |ret|>={thr:.4f}")

ind_crisis = ind.loc[ind.index.isin(crisis_days)]
print("\n=== 위기 국면(꼬리) 상관 ===")
corr_crisis = ind_crisis.corr()
print(corr_crisis.round(3))

# 오프-대각 평균
def offdiag_mean(m):
    vals = m.values[np.triu_indices_from(m.values, k=1)]
    return np.nanmean(vals)

print(f"\n평시 오프대각 평균상관 = {offdiag_mean(corr_full):.4f}")
print(f"위기국면 오프대각 평균상관 = {offdiag_mean(corr_crisis):.4f}")

# 같은 날 동시발생 종목수 분포 (위기일 vs 평시)
same_day_all = ind.sum(axis=1)
same_day_crisis = ind.loc[ind.index.isin(crisis_days)].sum(axis=1)
print(f"\n평시 일별 동시발생종목수 평균 = {same_day_all.mean():.3f}")
print(f"위기일 일별 동시발생종목수 평균 = {same_day_crisis.mean():.3f}")
