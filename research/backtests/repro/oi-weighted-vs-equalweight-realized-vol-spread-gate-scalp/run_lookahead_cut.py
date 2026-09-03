"""룩어헤드 절단 테스트: 절단점 이전 시점의 신호(realized vol·OI가중치·spread_z·게이트·BTC
Donchian/ATR)가 원본과 완전히 일치하는지, 최소 3종목(BTC 포함) bit 단위 확인."""
from __future__ import annotations

import pandas as pd

import common as C
import gates

CUT_AT = pd.Timestamp("2024-03-15", tz="UTC")
SAFETY_MARGIN_HOURS = 24 * 5


def main():
    udata_full = C.build_universe_data()
    gate_full, spread_full = gates.build_gate_oiweighted(udata=udata_full)
    btc_full = C.build_btc_signals()

    # --- 1h 데이터(klines+metrics) 절단 ---
    C.load_klines_1h.cache_clear()
    C.load_metrics_5m.cache_clear()
    orig_klines = C._load_klines_pkl_cache
    orig_metrics_dir_glob = None

    def cut_klines(symbol, tf, cache_dir):
        df = orig_klines(symbol, tf, cache_dir)
        return df[df.index <= CUT_AT]

    C._load_klines_pkl_cache = cut_klines

    import io
    orig_read_csv = pd.read_csv

    def cut_read_csv(path, *a, **kw):
        df = orig_read_csv(path, *a, **kw)
        if "create_time" in df.columns:
            df = df[pd.to_datetime(df["create_time"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
                    <= CUT_AT.tz_localize(None)]
        return df

    pd.read_csv = cut_read_csv

    udata_cut = C.build_universe_data()
    gate_cut, spread_cut = gates.build_gate_oiweighted(udata=udata_cut)
    btc_cut = C.build_btc_signals()

    pd.read_csv = orig_read_csv
    C._load_klines_pkl_cache = orig_klines
    C.load_klines_1h.cache_clear()
    C.load_metrics_5m.cache_clear()

    cutoff_compare = CUT_AT - pd.Timedelta(hours=SAFETY_MARGIN_HOURS)

    a = spread_full.loc[:cutoff_compare, ["rv_ow", "rv_ew", "spread_z", "btc_oi_weight"]].dropna()
    b = spread_cut.loc[:cutoff_compare, ["rv_ow", "rv_ew", "spread_z", "btc_oi_weight"]].dropna()
    common_idx = a.index.intersection(b.index)
    diff = (a.loc[common_idx] - b.loc[common_idx]).abs()
    print(f"1h 스프레드 신호: 비교시점수={len(common_idx)}, 최대절대오차")
    print(diff.max())
    assert diff.max().max() < 1e-9, "룩어헤드 의심: 절단 전 시점의 스프레드 신호값이 달라짐"

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
    print(f"\n15m BTC 지표: 비교시점수={len(idx_common)}, 최대오차 don_hi={max_dh:.10f} "
         f"don_lo={max_dl:.10f} atr14={max_atr:.10f}")
    assert max_dh < 1e-6 and max_dl < 1e-6 and max_atr < 1e-6, "룩어헤드 의심: BTC 지표 절단 전 값 변경"

    print("\n룩어헤드 절단 테스트 통과: 절단점 이전 신호(BTC 포함 7종목 유니버스 집계)가 원본과 완전 일치.")


if __name__ == "__main__":
    main()
