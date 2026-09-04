"""동어반복(tautology) 점검: OI변화율-가격수익률 상관(전체+트리거시점) + z(vol_ratio) vs z(oi_vol60 단독)
상관 + 종목간 신호상관(연간 평균 + BTC 절대수익률 상위5% 위기국면 꼬리상관)."""
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oivolratio")
import common
import engine

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

cfg = engine.RunConfig()

print("=== (1) OI변화율 vs 가격수익률 상관 — 전체구간 (스펙 실측 0.288 재확인) ===")
for sym, sig in sigs.items():
    c = sig.oi_ret.corr(sig.px_ret)
    print(f"  {sym:10s} corr(oi_ret,px_ret)={c:.4f}  n_valid={sig.oi_ret.notna().sum()}")

print("\n=== (1b) 트리거 시점 한정 상관 (z>=z_th 발화 시점만) ===")
for sym, sig in sigs.items():
    z = pd.Series(sig.z, index=sig.df1h.index)
    trig = z >= cfg.z_th
    n_trig = trig.sum()
    if n_trig >= 5:
        c = sig.oi_ret[trig].corr(sig.px_ret[trig])
    else:
        c = float("nan")
    print(f"  {sym:10s} n_trig={n_trig:5d} corr(oi_ret,px_ret | trigger)={c:.4f}")

print("\n=== (2) z(vol_ratio) vs z(oi_vol60 단독) 상관 — 비율의 부가가치 점검 ===")
print("    (비율 정규화가 'OI 변동성 그 자체'와 사실상 동일한 정보라면 동어반복에 가까움)")
overall_corrs = {}
trig_corrs = {}
for sym, sig in sigs.items():
    zr = pd.Series(sig.z, index=sig.df1h.index)
    zo = pd.Series(sig.z_oi_only, index=sig.df1h.index)
    c = zr.corr(zo)
    overall_corrs[sym] = c
    trig = zr >= cfg.z_th
    n_trig = trig.sum()
    ct = zr[trig].corr(zo[trig]) if n_trig >= 5 else float("nan")
    trig_corrs[sym] = ct
    print(f"  {sym:10s} corr(z_ratio,z_oi_only) 전체={c:.4f}  트리거시점={ct:.4f}  n_trig={n_trig}")

print("\n=== (3) 종목 간 신호상관 — z(vol_ratio) 쌍상관 (연간 전체) ===")
zdf = pd.DataFrame({sym: pd.Series(sig.z, index=sig.df1h.index) for sym, sig in sigs.items()})
corr_all = zdf.corr()
print(corr_all.round(3).to_string())

print("\n=== (3b) 위기국면 꼬리상관 — BTC 절대 1h 수익률 상위 5% 시점만 ===")
btc_px_ret = sigs["BTCUSDT"].px_ret.reindex(zdf.index)
thresh = btc_px_ret.abs().quantile(0.95)
crisis_mask = btc_px_ret.abs() >= thresh
print(f"  BTC |1h 수익률| >= {thresh:.4%} 시점 n={crisis_mask.sum()} (전체 {len(crisis_mask)}의 {crisis_mask.mean():.2%})")
corr_crisis = zdf[crisis_mask].corr()
print(corr_crisis.round(3).to_string())

with open(f"{common.SP}/corr_results.pkl", "wb") as f:
    pickle.dump(dict(overall=overall_corrs, trigger=trig_corrs, corr_all=corr_all,
                     corr_crisis=corr_crisis), f)
print("\n저장: corr_results.pkl")
