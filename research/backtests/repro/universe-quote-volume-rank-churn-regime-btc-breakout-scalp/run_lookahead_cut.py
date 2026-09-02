"""룩어헤드 절단 테스트: 특정 시점 이후 데이터를 잘라내고 재계산해도, 절단점보다 충분히
이전(안전마진) 시점의 신호(churn_pctile·게이트·BTC 브레이크아웃)가 원본과 완전히 일치하는지 확인."""
from __future__ import annotations

import pandas as pd

import common

CUT_AT = pd.Timestamp("2024-03-15", tz="UTC")   # 임의의 중간 절단점
SAFETY_MARGIN_HOURS = 24 * 5   # 절단점 5일 전까지만 비교(경계효과 배제)


def main():
    regime_full = common.build_regime_1h(symbols=common.EXT_SYMBOLS)
    btc_full = common.build_btc_signals()
    aligned_full = common.align_regime_to_15m(btc_full.df15, regime_full)

    # --- 1h 데이터 절단(regime) ---
    common.load_klines_1h.cache_clear()
    orig_load = common._load_klines

    def cut_load(symbol, tf, subdir):
        df = orig_load(symbol, tf, subdir)
        return df[df.index <= CUT_AT]

    common._load_klines = cut_load
    regime_cut = common.build_regime_1h(symbols=common.EXT_SYMBOLS)
    common._load_klines = orig_load
    common.load_klines_1h.cache_clear()

    cutoff_compare = CUT_AT - pd.Timedelta(hours=SAFETY_MARGIN_HOURS)
    a = regime_full.loc[:cutoff_compare, ["rank_churn", "churn_pctile"]].dropna()
    b = regime_cut.loc[:cutoff_compare, ["rank_churn", "churn_pctile"]].dropna()
    common_idx = a.index.intersection(b.index)
    diff = (a.loc[common_idx] - b.loc[common_idx]).abs()
    print(f"1h 레짐: 비교 시점수={len(common_idx)}, 최대 절대오차 rank_churn="
         f"{diff['rank_churn'].max():.10f}, churn_pctile={diff['churn_pctile'].max():.10f}")
    assert diff.max().max() < 1e-9, "룩어헤드 의심: 절단 전 시점의 레짐값이 달라짐"

    # --- 15m 데이터 절단(BTC Donchian/ATR) ---
    common.load_klines_15m.cache_clear()

    def cut_load_15m(symbol, tf, subdir):
        df = orig_load(symbol, tf, subdir)
        return df[df.index <= CUT_AT]

    common._load_klines = cut_load_15m
    btc_cut = common.build_btc_signals()
    common._load_klines = orig_load
    common.load_klines_15m.cache_clear()

    idx_common = btc_full.df15.index[btc_full.df15.index <= cutoff_compare]
    idx_common = idx_common.intersection(btc_cut.df15.index)
    dh_full = pd.Series(btc_full.don_hi, index=btc_full.df15.index).reindex(idx_common)
    dh_cut = pd.Series(btc_cut.don_hi, index=btc_cut.df15.index).reindex(idx_common)
    dl_full = pd.Series(btc_full.don_lo, index=btc_full.df15.index).reindex(idx_common)
    dl_cut = pd.Series(btc_cut.don_lo, index=btc_cut.df15.index).reindex(idx_common)
    atr_full = btc_full.atr14.reindex(idx_common)
    atr_cut = btc_cut.atr14.reindex(idx_common)
    max_dh = (dh_full - dh_cut).abs().max()
    max_dl = (dl_full - dl_cut).abs().max()
    max_atr = (atr_full - atr_cut).abs().max()
    print(f"15m BTC 지표: 비교 시점수={len(idx_common)}, 최대오차 don_hi={max_dh:.10f} "
         f"don_lo={max_dl:.10f} atr14={max_atr:.10f}")
    assert max_dh < 1e-6 and max_dl < 1e-6 and max_atr < 1e-6, "룩어헤드 의심: BTC 지표 절단 전 값 변경"

    print("\n룩어헤드 절단 테스트 통과: 절단점 이전 신호가 원본과 완전 일치.")


if __name__ == "__main__":
    main()
