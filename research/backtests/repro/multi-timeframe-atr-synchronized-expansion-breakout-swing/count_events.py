"""1차 진단: 삼중 동조 rising-edge 이벤트 수(종목별·IS/OOS)를 우선 확인한다."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import numpy as np
import pandas as pd

TH = 60.0

print(f"{'symbol':10s} {'n_full':>7s} {'n_is':>6s} {'n_oos':>6s} {'first':>12s} {'last':>12s}")
total_is = total_oos = 0
for sym in common.SYMBOLS:
    sig = common.build_signals(sym)
    if sig is None:
        print(f"{sym}: no data")
        continue
    h4 = sig.h4
    close4h = (h4.index + pd.Timedelta(hours=4))
    mask = (sig.p1h_at4h >= TH) & (sig.p4h_at4h >= TH) & (sig.p1d_at4h >= TH)
    mask_s = pd.Series(mask, index=h4.index)
    rising = mask_s & ~mask_s.shift(1).fillna(False).astype(bool)
    ev_idx = h4.index[rising.to_numpy()]
    ev_close = ev_idx + pd.Timedelta(hours=4)
    is_mask = (ev_close >= common.IS_START) & (ev_close <= common.IS_END)
    oos_mask = (ev_close >= common.OOS_START) & (ev_close <= common.OOS_END)
    n_is, n_oos = int(is_mask.sum()), int(oos_mask.sum())
    total_is += n_is; total_oos += n_oos
    first = ev_idx.min() if len(ev_idx) else None
    last = ev_idx.max() if len(ev_idx) else None
    print(f"{sym:10s} {len(ev_idx):7d} {n_is:6d} {n_oos:6d} {str(first)[:12]:>12s} {str(last)[:12]:>12s}")

print(f"\nTOTAL IS={total_is} OOS={total_oos}")
