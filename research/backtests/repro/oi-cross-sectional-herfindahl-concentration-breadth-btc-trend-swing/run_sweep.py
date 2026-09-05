from __future__ import annotations
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi")
import common, engine, stats_utils as su

univ = common.build_universe()

print("=== hhi_window 스윕 (lo=-0.75, hi=0.75 고정) ===")
for hw in [30, 45, 60, 75, 90]:
    sig = common.build_signals(univ, hhi_window=hw)
    cfg = engine.RunConfig(gate="hhi", fee_on=True)
    trades = engine.run_config(sig, cfg)
    df = su.trades_df(trades)
    is_df, oos_df, full_df = su.split_is_oos(df)
    print(f"hhi_window={hw:3d}  " + su.print_summary(su.summary(oos_df, "OOS")) +
          f"  | IS " + su.print_summary(su.summary(is_df, "")))

print()
print("=== 임계값(lo_th/hi_th) 스윕 (hhi_window=60 고정) ===")
sig60 = common.build_signals(univ, hhi_window=60)
for th in [0.5, 0.75, 1.0, 1.25, 1.5]:
    cfg = engine.RunConfig(gate="hhi", lo_th=-th, hi_th=th, fee_on=True)
    trades = engine.run_config(sig60, cfg)
    df = su.trades_df(trades)
    is_df, oos_df, full_df = su.split_is_oos(df)
    print(f"th=+-{th:.2f}  " + su.print_summary(su.summary(oos_df, "OOS")) +
          f"  | IS " + su.print_summary(su.summary(is_df, "")))
