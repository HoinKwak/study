import pickle, common
import numpy as np

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

for sym, sig in sigs.items():
    df = sig.df15m
    u = sig.donch_upper.to_numpy(float); lo = sig.donch_lower.to_numpy(float)
    c = df["close"].to_numpy(float)
    zcr_p = sig.zcr_pctile
    valid = np.isfinite(u) & np.isfinite(lo) & np.isfinite(c) & zcr_p.notna().to_numpy()
    long_break = valid & (c > u); short_break = valid & (c < lo)
    both = long_break & short_break
    long_break &= ~both; short_break &= ~both
    break_mask = long_break | short_break
    zcr30 = (zcr_p <= 30.0).to_numpy() & valid
    n_2cond = (break_mask & zcr30).sum()
    n_days = (df.index.max()-df.index.min()).days
    yr = n_days/365.25
    print(sym, "break+zcr30(2조건)/yr:", round(n_2cond/yr,1))
