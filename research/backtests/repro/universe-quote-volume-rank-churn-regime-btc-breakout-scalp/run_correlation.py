"""동어반복 점검: rank_churn 이 기존 지표(24h거래대금 std·HHI·BTC 실현변동성·ATR%)의 재포장이
아님을 상관으로 논증. 전체구간 상관 + 트리거 시점 한정 상관 둘 다 확인(pandas.corr, pairwise)."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common
import engine


def realized_vol_1h(df1h: pd.DataFrame, window: int = 24) -> pd.Series:
    ret = np.log(df1h["close"] / df1h["close"].shift(1))
    return ret.rolling(window).std()


def main():
    regime35 = common.build_regime_1h(symbols=common.EXT_SYMBOLS)
    btc1h = common.load_klines_1h("BTCUSDT")
    rv = realized_vol_1h(btc1h)

    merged = regime35.join(rv.rename("btc_rv24"), how="inner")

    print("=== 전체 구간 상관(pandas.corr, pairwise) ===")
    print("rank_churn vs vol24_std      :", merged["rank_churn"].corr(merged["vol24_std"]))
    print("rank_churn vs hhi            :", merged["rank_churn"].corr(merged["hhi"]))
    print("rank_churn vs btc_rv24       :", merged["rank_churn"].corr(merged["btc_rv24"]))
    print("churn_pctile vs vol24_std    :", merged["churn_pctile"].corr(merged["vol24_std"]))
    print("churn_pctile vs hhi          :", merged["churn_pctile"].corr(merged["hhi"]))
    print("churn_pctile vs btc_rv24     :", merged["churn_pctile"].corr(merged["btc_rv24"]))

    # 트리거 시점 한정: 게이트가 실제로 ON 이었던(즉 브레이크아웃과 결합해 신호가 난) 1h 시점만.
    btc = common.build_btc_signals()
    aligned = common.align_regime_to_15m(btc.df15, regime35)
    cfg = engine.RunConfig(mode="gated")
    trades = engine.run_all(btc, aligned, cfg)
    trig_times = pd.to_datetime([t.entry_time for t in trades]).floor("h")
    trig_1h = merged.reindex(trig_times.unique())
    print(f"\n=== 트리거 시점 한정 상관(n={len(trig_1h)}) ===")
    print("rank_churn vs vol24_std      :", trig_1h["rank_churn"].corr(trig_1h["vol24_std"]))
    print("rank_churn vs hhi            :", trig_1h["rank_churn"].corr(trig_1h["hhi"]))
    print("rank_churn vs btc_rv24       :", trig_1h["rank_churn"].corr(trig_1h["btc_rv24"]))


if __name__ == "__main__":
    main()
