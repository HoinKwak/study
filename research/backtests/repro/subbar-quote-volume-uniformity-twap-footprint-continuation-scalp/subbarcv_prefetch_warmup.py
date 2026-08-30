"""웜업 구간(2021-11~2021-12) 5m/15m 데이터 추가 프리페치 — 60일 롤링 백분위 창을
IS_START(2022-01-01)부터 최대한 채우기 위함."""
from __future__ import annotations
import sys, time
sys.path.insert(0, "research/impl")
from subbarcv_common import load_klines_qv, load_klines, SYMBOLS

if __name__ == "__main__":
    t0 = time.time()
    for tf, loader in (("5m", load_klines_qv), ("15m", load_klines)):
        for sym in SYMBOLS:
            t1 = time.time()
            df = loader(sym, tf, "2021-11-01", "2021-12-31")
            print(f"{sym} {tf} warmup: {len(df)} rows [{df.index.min()} ~ {df.index.max()}] "
                  f"({time.time()-t1:.1f}s)", flush=True)
    print(f"TOTAL {time.time()-t0:.1f}s")
