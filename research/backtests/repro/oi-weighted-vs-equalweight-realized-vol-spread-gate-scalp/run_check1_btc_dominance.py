"""1단계 최우선 점검: BTC OI 비중 + OI가중 RV vs BTC 단독 RV 상관(레벨·spread_z, 전체구간·트리거시점).
사전 폐기조건 (a): 상관>=0.9 면 재포장으로 폐기."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as C


def main():
    udata = C.build_universe_data()
    print("=== 종목별 OI 명목가치 데이터 커버리지(1h bar 수) ===")
    for sym in C.SYMBOLS:
        col = udata.oi_value[sym] if sym in udata.oi_value.columns else pd.Series(dtype=float)
        print(f"  {sym:10s} n_notna={col.notna().sum():6d} / n_total={len(col):6d}")

    spread_df = C.compute_spread(udata)
    print("\n=== BTC OI 비중(btc_oi_weight) 분포 ===")
    bw = spread_df["btc_oi_weight"].dropna()
    print(f"  n={len(bw)}  mean={bw.mean():.4f}  median={bw.median():.4f}  "
         f"min={bw.min():.4f}  max={bw.max():.4f}")
    print("  연도별 평균:")
    for yr, g in bw.groupby(bw.index.year):
        print(f"    {yr}: mean={g.mean():.4f} n={len(g)}")

    # BTC 단독 실현변동성(레벨) — 이미 udata.rv[BTC]
    btc_rv = udata.rv[C.BTC]

    merged = spread_df.join(btc_rv.rename("btc_rv"), how="inner").dropna(
        subset=["rv_ow", "btc_rv"])
    print(f"\n=== 레벨 상관(pandas.corr, pairwise, n={len(merged)}) ===")
    print("  rv_ow vs btc_rv          :", merged["rv_ow"].corr(merged["btc_rv"]))
    print("  rv_ew vs btc_rv          :", merged["rv_ew"].corr(merged["btc_rv"]))

    # spread_z 기준 상관은 스칼라 하나뿐이라 "vs btc_rv" 대신 btc_rv 의 zscore 화한 것과 비교하거나
    # 게이트로 쓰이는 spread_z 자체가 btc_rv 의 z-score 와 얼마나 같은지를 봐야 정확한 질문이 된다.
    # (btc-solo-vol 게이트 대조군에서 쓸 것과 동일한 방식으로 btc_rv 의 z-score 를 만든다.)
    btc_rv_z = (btc_rv - btc_rv.rolling(C.SPREAD_Z_WINDOW).mean()) / \
        btc_rv.rolling(C.SPREAD_Z_WINDOW).std(ddof=0)
    merged2 = spread_df.join(btc_rv_z.rename("btc_rv_z"), how="inner").dropna(
        subset=["spread_z", "btc_rv_z"])
    print(f"\n=== z-score 상관(spread_z vs btc_rv_z, 게이트로 실제 쓰이는 변수 기준, n={len(merged2)}) ===")
    print("  spread_z vs btc_rv_z     :", merged2["spread_z"].corr(merged2["btc_rv_z"]))

    # 트리거 시점 한정(게이트가 실제로 short_only/long_only 로 발화한 시점만)
    gate = C.gate_from_spread_z(spread_df["spread_z"])
    trig_mask = gate.isin(["short_only", "long_only"])
    trig_idx = spread_df.index[trig_mask]
    trig = merged2.reindex(trig_idx).dropna(subset=["spread_z", "btc_rv_z"])
    print(f"\n=== 트리거 시점 한정 z-score 상관(n={len(trig)}) ===")
    if len(trig) > 2:
        print("  spread_z vs btc_rv_z     :", trig["spread_z"].corr(trig["btc_rv_z"]))
    else:
        print("  표본 부족")

    trig_lvl = merged.reindex(trig_idx).dropna(subset=["rv_ow", "btc_rv"])
    print(f"\n=== 트리거 시점 한정 레벨 상관(n={len(trig_lvl)}) ===")
    if len(trig_lvl) > 2:
        print("  rv_ow vs btc_rv          :", trig_lvl["rv_ow"].corr(trig_lvl["btc_rv"]))
    else:
        print("  표본 부족")

    print("\n=== gate 분포 ===")
    print(gate.value_counts(dropna=False))


if __name__ == "__main__":
    main()
