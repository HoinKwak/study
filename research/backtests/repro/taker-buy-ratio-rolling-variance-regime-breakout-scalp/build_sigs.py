"""신호 사전계산·캐시(sigs.pkl)."""
import pickle
import time

import common
import engine

t0 = time.time()
sigs = engine.load_all_signals()
common.SP.mkdir(parents=True, exist_ok=True)
with open(f"{common.SP}/sigs.pkl", "wb") as f:
    pickle.dump(sigs, f)
print(f"완료 ({time.time()-t0:.1f}s) — 심볼: {list(sigs.keys())}")
for sym, sig in sigs.items():
    df = sig.df15m
    print(f"  {sym}: 15m n={len(df)} 범위 {df.index.min()}~{df.index.max()} "
         f"tvr_raw_nan_frac={sig.tvr_raw_nan.mean()*100:.2f}%")
