from __future__ import annotations
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common

TFS = ["5m", "15m", "1h"]


def _job(sym, tf, y, m):
    return sym, tf, y, m, common.fetch_month(sym, tf, y, m) is not None


if __name__ == "__main__":
    months = common._month_range(common.IS_START, common.OOS_END)
    jobs = [(sym, tf, y, m) for tf in TFS for sym in common.SYMBOLS for y, m in months]
    print(f"total jobs: {len(jobs)}")
    t0 = time.time()
    ok, miss = 0, 0
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = [ex.submit(_job, *j) for j in jobs]
        for i, f in enumerate(as_completed(futs)):
            sym, tf, y, m, got = f.result()
            if got:
                ok += 1
            else:
                miss += 1
                print(f"MISS {sym} {tf} {y}-{m:02d}")
            if (i + 1) % 100 == 0:
                print(f"{i+1}/{len(jobs)} done, {time.time()-t0:.1f}s", flush=True)
    print(f"DONE ok={ok} miss={miss} total_time={time.time()-t0:.1f}s")
