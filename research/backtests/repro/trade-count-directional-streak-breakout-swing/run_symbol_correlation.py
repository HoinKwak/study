"""종목 간 신호 상관: 평시 vs 위기국면(BTC 절대 일간수익률 상위 5%) 꼬리 상관.
+ 같은 캘린더일/5일 롤링 윈도우 동시진입 클러스터 점검."""
import pickle
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import common
import engine
import stats_utils as su

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

for short_mode in ["streak_down", "streak_up_alt"]:
    print(f"\n############ short_mode={short_mode} ############")
    cfg = engine.RunConfig(mode="gated", short_mode=short_mode)
    trades = engine.run_all(sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    d = su.trades_df(all_trades)
    d["cal_day"] = d["entry_time"].dt.floor("D")

    btc = common.load_klines_4h("BTCUSDT")
    btc_daily = btc["close"].resample("1D").last()
    btc_ret = btc_daily.pct_change()

    all_days = pd.date_range(common.IS_START.floor("D"), common.OOS_END.floor("D"), freq="D", tz="UTC")
    ind = pd.DataFrame(0, index=all_days, columns=common.SYMBOLS)
    for sym in common.SYMBOLS:
        days = d.loc[d.symbol == sym, "cal_day"].unique()
        ind.loc[ind.index.isin(days), sym] = 1

    corr_full = ind.corr()
    btc_ret_aligned = btc_ret.reindex(all_days)
    thr = btc_ret_aligned.abs().quantile(0.95)
    crisis_days = btc_ret_aligned[btc_ret_aligned.abs() >= thr].index
    ind_crisis = ind.loc[ind.index.isin(crisis_days)]
    corr_crisis = ind_crisis.corr()

    def offdiag_mean(m):
        vals = m.values[np.triu_indices_from(m.values, k=1)]
        return np.nanmean(vals)

    print(f"위기일수(BTC |일간수익률| 상위5%) = {len(crisis_days)}, 임계 |ret|>={thr:.4f}")
    print(f"평시 오프대각 평균상관 = {offdiag_mean(corr_full):.4f}")
    print(f"위기국면 오프대각 평균상관 = {offdiag_mean(corr_crisis):.4f}")
    same_day_all = ind.sum(axis=1)
    same_day_crisis = ind.loc[ind.index.isin(crisis_days)].sum(axis=1)
    print(f"평시 일별 동시발생종목수 평균 = {same_day_all.mean():.4f}")
    print(f"위기일 일별 동시발생종목수 평균 = {same_day_crisis.mean():.4f}")
    print("최대 동시발생종목수(전체기간):", int(same_day_all.max()))
    top_days = same_day_all.sort_values(ascending=False).head(5)
    print("동시발생 상위 5일:")
    print(top_days)
