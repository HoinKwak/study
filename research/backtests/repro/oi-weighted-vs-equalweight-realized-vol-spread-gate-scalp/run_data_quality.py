"""데이터 품질 진단: create_time 정시정렬·지터, metrics 0-fill/ffill 비율, klines-metrics 병합
NaN 비율, 종목별 결측 구간(특히 2022-06~12)."""
from __future__ import annotations

import pandas as pd

import common as C


def main():
    print("=== metrics create_time 정시 정렬 여부(지터 확인) ===")
    m5 = C.load_metrics_5m(C.BTC)
    minutes = m5.index.minute
    seconds = m5.index.second
    off_grid = ((minutes % 5 != 0) | (seconds != 0)).sum()
    print(f"  BTC 5분 그리드[:00/:05/...] 밖 타임스탬프 수: {off_grid} / {len(m5)}")

    print("\n=== 종목별 0-fill(<=0, 결측 처리됨) 비율 + ffill 비율(1h 집계 후) ===")
    udata = C.build_universe_data()
    for sym in C.SYMBOLS:
        m5s = C.load_metrics_5m(sym)
        zero_frac = (m5s["sum_open_interest_value"].isna()).mean() if not m5s.empty else float("nan")
        oi1h = C.oi_value_1h_from_5m(m5s)
        ffill_frac = oi1h["oi_raw_nan"].mean() if not oi1h.empty else float("nan")
        print(f"  {sym:10s} 5분 0-fill/결측 비율={zero_frac*100:.3f}%  1h ffill 비율={ffill_frac*100:.3f}%")

    print("\n=== 2022-06~12 구간 결측 집중 여부(과거 count_toptrader 결측 이력과 비교) ===")
    for sym in C.SYMBOLS:
        m5s = C.load_metrics_5m(sym)
        sub = m5s.loc["2022-06-01":"2022-12-31"]
        na_frac = sub["sum_open_interest_value"].isna().mean() if len(sub) else float("nan")
        print(f"  {sym:10s} 2022-06~12 sum_open_interest_value 결측률={na_frac*100:.2f}% (n={len(sub)})")

    print("\n=== klines(1h)-metrics 병합 NaN 비율(rv, oi_value 각각 + join 후 rv_ow) ===")
    for sym in C.SYMBOLS:
        rv_na = udata.rv[sym].isna().mean() if sym in udata.rv.columns else float("nan")
        oi_na = udata.oi_value[sym].isna().mean() if sym in udata.oi_value.columns else float("nan")
        print(f"  {sym:10s} rv NaN비율={rv_na*100:.2f}%  oi_value NaN비율={oi_na*100:.2f}%")

    gate, spread_df = __import__("gates").build_gate_oiweighted(udata=udata)
    print(f"\n  spread_z 전체 NaN 비율={spread_df['spread_z'].isna().mean()*100:.2f}% "
         f"(워밍업 90h + 구간 결측 포함, n={len(spread_df)})")


if __name__ == "__main__":
    main()
