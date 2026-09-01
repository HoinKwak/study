"""동어반복(tautology) 점검 — 잔차z vs OI순수z 상관(전체구간 + 트리거시점 한정) + 종목간 신호상관."""
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiresid")
import common
import engine

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

cfg = engine.RunConfig()
print("=== 잔차z vs OI순수z 상관 (전체구간, pairwise pandas.corr) ===")
overall_corrs = {}
for sym, sig in sigs.items():
    z_resid = pd.Series(sig.z_resid, index=sig.df.index)
    z_oi = pd.Series(sig.z_oi, index=sig.df.index)
    c = z_resid.corr(z_oi)
    overall_corrs[sym] = c
    print(f"  {sym:10s} corr={c:.4f}  n_valid={z_resid.notna().sum()}")

print("\n=== 트리거 시점 한정 상관 (|z_resid|>=z_th 발화 시점만) ===")
trig_corrs = {}
for sym, sig in sigs.items():
    z_resid = pd.Series(sig.z_resid, index=sig.df.index)
    z_oi = pd.Series(sig.z_oi, index=sig.df.index)
    dp = sig.d_price_pct
    trig_mask = (z_resid.abs() >= cfg.z_th) & (dp.abs() < cfg.price_filter)
    n_trig = trig_mask.sum()
    if n_trig >= 5:
        c = z_resid[trig_mask].corr(z_oi[trig_mask])
    else:
        c = float("nan")
    trig_corrs[sym] = c
    print(f"  {sym:10s} n_trig={n_trig:4d} corr(z_resid,z_oi | trigger)={c:.4f}")

print("\n=== 트리거 시점 한정 상관 (|z_oi|>=z_th 발화 시점만, 대칭 확인) ===")
for sym, sig in sigs.items():
    z_resid = pd.Series(sig.z_resid, index=sig.df.index)
    z_oi = pd.Series(sig.z_oi, index=sig.df.index)
    dp = sig.d_price_pct
    trig_mask = (z_oi.abs() >= cfg.z_th) & (dp.abs() < cfg.price_filter)
    n_trig = trig_mask.sum()
    if n_trig >= 5:
        c = z_resid[trig_mask].corr(z_oi[trig_mask])
    else:
        c = float("nan")
    print(f"  {sym:10s} n_trig={n_trig:4d} corr(z_resid,z_oi | trigger)={c:.4f}")

print("\n=== 트리거 집합 자체의 중첩도(잔차 트리거 vs OI-z 트리거, 같은 bar·같은 방향) ===")
for sym, sig in sigs.items():
    z_resid = pd.Series(sig.z_resid, index=sig.df.index)
    z_oi = pd.Series(sig.z_oi, index=sig.df.index)
    dp = sig.d_price_pct
    resid_trig = (z_resid.abs() >= cfg.z_th) & (dp.abs() < cfg.price_filter)
    oi_trig = (z_oi.abs() >= cfg.z_th) & (dp.abs() < cfg.price_filter)
    both = resid_trig & oi_trig
    same_sign = both & (np.sign(z_resid) == np.sign(z_oi))
    union_n = (resid_trig | oi_trig).sum()
    jaccard = both.sum() / union_n if union_n > 0 else float("nan")
    print(f"  {sym:10s} resid_trig={resid_trig.sum():4d} oi_trig={oi_trig.sum():4d} "
         f"both={both.sum():4d} both_same_sign={same_sign.sum():4d} jaccard={jaccard:.4f}")

with open(f"{common.SP}/corr_results.pkl", "wb") as f:
    pickle.dump(dict(overall=overall_corrs, trigger=trig_corrs), f)
print("\n저장: corr_results.pkl")
