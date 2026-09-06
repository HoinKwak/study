"""신호 사전계산·캐시(sigs.pkl)."""
import pickle
import time

import common

t0 = time.time()
sigs = {}
for s in common.SYMBOLS:
    t1 = time.time()
    sig = common.build_signals(s)
    if sig is not None:
        sigs[s] = sig
        print(f"  {s}: n={len(sig.df15m)} 범위 {sig.df15m.index.min()}~{sig.df15m.index.max()} "
             f"({time.time()-t1:.1f}s)")
common.SP.mkdir(parents=True, exist_ok=True)
with open(f"{common.SP}/sigs.pkl", "wb") as f:
    pickle.dump(sigs, f)
print(f"완료 ({time.time()-t0:.1f}s) — 심볼: {list(sigs.keys())}")
