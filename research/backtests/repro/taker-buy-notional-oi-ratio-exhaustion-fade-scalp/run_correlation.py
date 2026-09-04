"""동어반복(tautology) 점검: z_buy 가 캔들 거래량(volume) z-score·taker_buy_frac(매수비중)의
재포장이 아닌지 (전체구간 + 트리거 시점 한정) + 종목간 신호상관(연간 + 위기국면 꼬리상관)."""
import pickle

import numpy as np
import pandas as pd

import common
import engine

with open(common.SP / "sigs_200.pkl", "rb") as f:
    sigs = pickle.load(f)

cfg = engine.RunConfig()

print("=== (1) z_buy vs z_volume(캔들 거래량 자체 z-score) 상관 — 전체구간 + 트리거시점 ===")
for sym, sig in sigs.items():
    zb = pd.Series(sig.z_buy, index=sig.df15m.index)
    zv = pd.Series(sig.z_volume, index=sig.df15m.index)
    c_all = zb.corr(zv)
    trig = zb >= cfg.z_th
    n_trig = trig.sum()
    c_trig = zb[trig].corr(zv[trig]) if n_trig >= 5 else float("nan")
    print(f"  {sym:10s} corr_all={c_all:.4f}  corr_trigger={c_trig:.4f}  n_trig={n_trig}")

print("\n=== (2) z_buy vs taker_buy_frac(매수비중, 방향성 있는 절대량과 무관한 비율) 상관 ===")
for sym, sig in sigs.items():
    zb = pd.Series(sig.z_buy, index=sig.df15m.index)
    tbf = sig.taker_buy_frac
    c_all = zb.corr(tbf)
    trig = zb >= cfg.z_th
    n_trig = trig.sum()
    c_trig = zb[trig].corr(tbf[trig]) if n_trig >= 5 else float("nan")
    print(f"  {sym:10s} corr_all={c_all:.4f}  corr_trigger={c_trig:.4f}  n_trig={n_trig}")

print("\n=== (3) z_buy vs ΔOI%(oi_pct_change) 상관 — '단순 OI변화율의 재포장' 아닌지 ===")
for sym, sig in sigs.items():
    zb = pd.Series(sig.z_buy, index=sig.df15m.index)
    doi = sig.oi_pct_change
    c_all = zb.corr(doi)
    trig = zb >= cfg.z_th
    n_trig = trig.sum()
    c_trig = zb[trig].corr(doi[trig]) if n_trig >= 5 else float("nan")
    print(f"  {sym:10s} corr_all={c_all:.4f}  corr_trigger={c_trig:.4f}")

print("\n=== (4) z_buy(OI 분모) vs z_vol24h_buy(24h거래대금 분모, 대조군②) 상관 — "
     "'OI 대비'가 부가가치를 내는지(분모 교체만으로 사실상 동일하면 무가치) ===")
for sym, sig in sigs.items():
    zb = pd.Series(sig.z_buy, index=sig.df15m.index)
    zv24 = pd.Series(sig.z_vol24h_buy, index=sig.df15m.index)
    c_all = zb.corr(zv24)
    trig = zb >= cfg.z_th
    n_trig = trig.sum()
    c_trig = zb[trig].corr(zv24[trig]) if n_trig >= 5 else float("nan")
    print(f"  {sym:10s} corr_all={c_all:.4f}  corr_trigger={c_trig:.4f}")

print("\n=== (5) 종목 간 신호상관 — z_buy 쌍상관(연간 전체, pandas.corr pairwise) ===")
zdf = pd.DataFrame({sym: pd.Series(sig.z_buy, index=sig.df15m.index) for sym, sig in sigs.items()})
corr_all = zdf.corr()
print(corr_all.round(3).to_string())

print("\n=== (5b) 위기국면 꼬리상관 — BTC 절대 15m 수익률 상위 5% 시점만 ===")
btc_ret = np.log(sigs["BTCUSDT"].df15m["close"] / sigs["BTCUSDT"].df15m["close"].shift(1))
btc_ret = btc_ret.reindex(zdf.index)
thresh = btc_ret.abs().quantile(0.95)
crisis_mask = btc_ret.abs() >= thresh
print(f"  BTC |15m 수익률| >= {thresh:.4%} 시점 n={crisis_mask.sum()} "
     f"(전체 {len(crisis_mask)}의 {crisis_mask.mean():.2%})")
corr_crisis = zdf[crisis_mask].corr()
print(corr_crisis.round(3).to_string())

with open(common.SP / "corr_results.pkl", "wb") as f:
    pickle.dump(dict(corr_all=corr_all, corr_crisis=corr_crisis), f)
print("\n저장: corr_results.pkl")
