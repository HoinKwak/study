import pickle
import common
import numpy as np

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)
sig = sigs["BTCUSDT"]
df = sig.df15m
idx = df.index

for name, s in [("zcr", sig.zcr), ("zcr_pctile", sig.zcr_pctile), ("oi_delta", sig.oi_delta)]:
    na = s.isna().to_numpy()
    run_start = None
    runs = []
    for i, v in enumerate(na):
        if v and run_start is None:
            run_start = i
        if not v and run_start is not None:
            runs.append((run_start, i - 1))
            run_start = None
    if run_start is not None:
        runs.append((run_start, len(na) - 1))
    runs2 = [(idx[a], idx[b], b - a + 1) for a, b in runs]
    runs2.sort(key=lambda x: -x[2])
    print(f"--- {name}: total NaN={na.sum()} runs={len(runs2)} ---")
    for r in runs2[:8]:
        print(" ", r)
