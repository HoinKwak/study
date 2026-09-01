"""1차 진단: BTC 펀딩가속 트리거 빈도 + confirm_window 내 알트 confirm 결합확률."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import common

fa = common.build_funding_accel("BTCUSDT", window=60)
print("funding prints:", len(fa.df), fa.df.index.min(), fa.df.index.max())
print("funding interval median (h):", fa.df.index.to_series().diff().median())

ev = common.find_accel_events(fa, accel_z_threshold=1.5)
print("total accel events (z>=1.5):", len(ev))
ev["is_is"] = ev["trigger_time"] <= common.IS_END
ev["is_oos"] = (ev["trigger_time"] >= common.OOS_START) & (ev["trigger_time"] <= common.OOS_END)
print("IS events:", ev["is_is"].sum(), "OOS events:", ev["is_oos"].sum())
print("direction value counts:", ev["direction"].value_counts().to_dict())

# alt confirm 결합확률 체크 (BTCUSDT 제외 6개 알트, confirm_window=8h)
alts = {s: common.build_alt_signals(s) for s in common.ALT_SYMBOLS}
for s, a in alts.items():
    if a is None:
        print(s, "NO DATA")

confirm_window = pd.Timedelta(hours=8)


def check_confirm(alt: common.AltSignals, trigger_time: pd.Timestamp, direction: int):
    df = alt.df
    win_end = trigger_time + confirm_window
    mask = (df.index >= trigger_time) & (df.index < win_end)
    sub = df[mask]
    if sub.empty:
        return None
    idxpos = df.index.get_indexer(sub.index)
    du = alt.don_upper.to_numpy()[idxpos]
    dl = alt.don_lower.to_numpy()[idxpos]
    va = alt.vol_avg.to_numpy()[idxpos]
    close = sub["close"].to_numpy()
    qv = sub["quote_volume"].to_numpy()
    if direction > 0:
        cond = (close > du) & (qv >= 1.3 * va)
    else:
        cond = (close < dl) & (qv >= 1.3 * va)
    valid = np.isfinite(du) & np.isfinite(va) & cond
    if not valid.any():
        return None
    first = np.argmax(valid)
    return sub.index[first]


results = {s: 0 for s in common.ALT_SYMBOLS}
totals = {s: 0 for s in common.ALT_SYMBOLS}
for _, row in ev.iterrows():
    tt, d = row["trigger_time"], row["direction"]
    for s, a in alts.items():
        if a is None:
            continue
        totals[s] += 1
        r = check_confirm(a, tt, d)
        if r is not None:
            results[s] += 1

print("\nconfirm hit-rate per alt (of", len(ev), "triggers):")
for s in common.ALT_SYMBOLS:
    n = results[s]
    print(f"  {s}: {n}/{totals[s]} = {n/max(totals[s],1)*100:.1f}%")

print("\ntotal potential trades (sum over alts):", sum(results.values()))
