"""파라미터 민감도 스윕: accel_z_threshold, confirm_window, atr_trail_mult."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
import common
import engine
import stats_utils as su

fa = common.build_funding_accel("BTCUSDT", window=60)
alts = engine.load_all_alts()


def split_oos(df):
    et = pd.to_datetime(df["entry_time"])
    return df[(et >= common.OOS_START) & (et <= common.OOS_END)]


rows = []
for az in [1.0, 1.5, 2.0, 2.5]:
    events = common.find_accel_events(fa, accel_z_threshold=az)
    cfg = engine.RunConfig(accel_z_threshold=az)
    res = engine.run_all(alts, events, cfg)
    full = pd.concat([engine.trades_to_df(t) for t in res.values()], ignore_index=True)
    oos = split_oos(full)
    s = su.summarize(oos["r_multiple"].to_numpy(), f"accel_z={az}")
    s["param"] = "accel_z_threshold"
    s["value"] = az
    rows.append(s)
    print(s)

for cw in [8.0, 16.0, 24.0]:
    events = common.find_accel_events(fa, accel_z_threshold=1.5)
    cfg = engine.RunConfig(confirm_window_h=cw)
    res = engine.run_all(alts, events, cfg)
    full = pd.concat([engine.trades_to_df(t) for t in res.values()], ignore_index=True)
    oos = split_oos(full)
    s = su.summarize(oos["r_multiple"].to_numpy(), f"confirm_window={cw}")
    s["param"] = "confirm_window_h"
    s["value"] = cw
    rows.append(s)
    print(s)

events_base = common.find_accel_events(fa, accel_z_threshold=1.5)
for tm in [1.0, 1.2, 1.5, 1.8]:
    cfg = engine.RunConfig(atr_trail_mult=tm)
    res = engine.run_all(alts, events_base, cfg)
    full = pd.concat([engine.trades_to_df(t) for t in res.values()], ignore_index=True)
    oos = split_oos(full)
    s = su.summarize(oos["r_multiple"].to_numpy(), f"atr_trail_mult={tm}")
    s["param"] = "atr_trail_mult"
    s["value"] = tm
    rows.append(s)
    print(s)

for dl in [14, 20, 30]:
    alts_dl = engine.load_all_alts(donchian_lookback=dl)
    cfg = engine.RunConfig()
    res = engine.run_all(alts_dl, events_base, cfg)
    full = pd.concat([engine.trades_to_df(t) for t in res.values()], ignore_index=True)
    oos = split_oos(full)
    s = su.summarize(oos["r_multiple"].to_numpy(), f"donchian_lookback={dl}")
    s["param"] = "donchian_lookback"
    s["value"] = dl
    rows.append(s)
    print(s)

pd.DataFrame(rows).to_csv(common.SP / "sweep_results.csv", index=False)
print("\nPASS 기준(OOS PF(R)>=1.3 AND t>=1.96) 충족 변형 수:",
     sum(1 for r in rows if (r.get("pf_r", 0) or 0) >= 1.3 and (r.get("t", 0) or 0) >= 1.96),
     "/", len(rows))
