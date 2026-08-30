from __future__ import annotations
import sys, time
sys.path.insert(0, "research/impl")
from subbarcv_common import load_klines_qv, SYMBOLS, IS_START, OOS_END

TFS = ["5m", "15m", "1h"]

if __name__ == "__main__":
    t0 = time.time()
    for tf in TFS:
        for sym in SYMBOLS:
            t1 = time.time()
            df = load_klines_qv(sym, tf, IS_START, OOS_END)
            print(f"{sym} {tf}: {len(df)} rows [{df.index.min()} ~ {df.index.max()}] "
                  f"({time.time()-t1:.1f}s)", flush=True)
    print(f"TOTAL {time.time()-t0:.1f}s")
