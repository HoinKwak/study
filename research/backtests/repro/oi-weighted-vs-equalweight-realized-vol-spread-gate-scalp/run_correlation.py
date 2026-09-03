"""동어반복 점검 + 결합확률 실측 + 종목간 신호상관(평균/위기국면)."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as C
import engine
import gates


def main():
    udata = C.build_universe_data()
    gate, spread_df = gates.build_gate_oiweighted(udata=udata)
    btc = C.build_btc_signals()

    print("=== 결합확률 실측(최종 진입조건 전체: 게이트 AND Donchian(20) 브레이크아웃) ===")
    aligned = C.align_1h_to_15m(btc.df15, gate.to_frame("gate"))["gate"]
    n_bars = int(btc.don_hi[np.isfinite(btc.don_hi)].shape[0])
    close = btc.df15["close"].to_numpy(float)
    long_break = close > btc.don_hi
    short_break = close < btc.don_lo
    breakout_any = np.nan_to_num(long_break.astype(float)) + np.nan_to_num(short_break.astype(float))
    breakout_rate = np.nanmean((long_break | short_break).astype(float))
    print(f"  BTC 15m 전체 워밍업 이후 봉수(유효 don_hi)≈{n_bars}")
    print(f"  브레이크아웃(양방향) 자체 발생률: {breakout_rate*100:.2f}% (독립 게이트 가정 없이)")

    signals_gated = engine.find_signals(btc.df15, btc.don_hi, btc.don_lo, aligned, "gated")
    signals_ungated = engine.find_signals(btc.df15, btc.don_hi, btc.don_lo, None, "ungated")
    n_years = (C.OOS_END - C.IS_START).days / 365.25
    print(f"  게이트+브레이크아웃 결합 신호수(전체구간)={len(signals_gated)} "
         f"(연환산 {len(signals_gated)/n_years:.0f}건/년, 스펙 예상 100~250건/년의 "
         f"{len(signals_gated)/n_years/175:.1f}배, 175=예상 중앙값)")
    print(f"  브레이크아웃 단독(게이트 없음) 신호수(전체구간)={len(signals_ungated)} "
         f"(연환산 {len(signals_ungated)/n_years:.0f}건/년)")
    print(f"  게이트 필터링 비율: {(1 - len(signals_gated)/len(signals_ungated))*100:.1f}% 감소")

    print("\n=== 동어반복 점검: OI가중 스프레드(spread_z) vs 기존 지표 상관 ===")
    btc1h = C.load_klines_1h(C.BTC)
    atr_pct = (btc1h["high"] - btc1h["low"]) / btc1h["close"]
    merged = spread_df.join(atr_pct.rename("btc_range_pct"), how="inner").dropna(
        subset=["spread_z", "btc_range_pct"])
    print("  spread_z vs BTC 1h range%(ATR 근사)  :", merged["spread_z"].corr(merged["btc_range_pct"]))

    print("\n=== 종목 간 신호(1h realized vol) 상관 — 평균 vs 위기국면(BTC |수익률| 상위 5%) ===")
    rv = udata.rv[C.SYMBOLS].dropna(how="any")
    corr_avg = rv.corr()
    print("  평균 구간 상관행렬(pandas.corr):")
    print(corr_avg.round(3))

    btc_ret = np.log(btc1h["close"] / btc1h["close"].shift(1)).abs()
    thresh = btc_ret.quantile(0.95)
    crisis_idx = btc_ret[btc_ret >= thresh].index
    rv_crisis = rv.reindex(rv.index.intersection(crisis_idx)).dropna(how="any")
    corr_crisis = rv_crisis.corr()
    print(f"\n  위기국면(BTC|logret|상위5%, n={len(rv_crisis)}) 상관행렬:")
    print(corr_crisis.round(3))

    off_diag_avg = corr_avg.to_numpy()[~np.eye(7, dtype=bool)]
    off_diag_crisis = corr_crisis.to_numpy()[~np.eye(7, dtype=bool)]
    print(f"\n  평균 오프대각 상관 평균={off_diag_avg.mean():.3f}  위기국면 오프대각 상관 평균="
         f"{off_diag_crisis.mean():.3f}")


if __name__ == "__main__":
    main()
