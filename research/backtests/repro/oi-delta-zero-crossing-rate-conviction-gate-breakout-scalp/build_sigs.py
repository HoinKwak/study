"""신호 사전계산·pickle 캐시."""
import pickle
import time

import common
import engine

t0 = time.time()
sigs = engine.load_all_signals()
print(f"신호 빌드 완료 ({time.time()-t0:.1f}s) — 심볼: {list(sigs.keys())}")
with open(f"{common.SP}/sigs.pkl", "wb") as f:
    pickle.dump(sigs, f)
print("저장 완료: sigs.pkl")
for s, sig in sigs.items():
    print(s, sig.df15m.shape, sig.df15m.index.min(), sig.df15m.index.max())
