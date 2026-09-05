from __future__ import annotations

import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi")

import numpy as np
import pandas as pd

import common
import engine
import stats_utils as su

print("=== 유니버스 구축 ===")
univ = common.build_universe()
print("HHI 완전표본 일수:", univ.hhi.notna().sum(), "/", len(univ.hhi))
print("HHI describe:\n", univ.hhi.describe())

sig = common.build_signals(univ)
print("BTC 1d 봉수:", len(sig.df1d), "BTC 4h 봉수:", len(sig.df4h))
print("hhi_z 유효:", sig.hhi_z.notna().sum())
print("EMA50 유효:", sig.ema50_1d.notna().sum())

for gate in ["none", "hhi", "btcshare", "reverse"]:
    for fee_on in [True, False]:
        cfg = engine.RunConfig(gate=gate, fee_on=fee_on)
        trades = engine.run_config(sig, cfg)
        df = su.trades_df(trades)
        is_df, oos_df, full_df = su.split_is_oos(df)
        label = f"{gate:10s} fee={'on ' if fee_on else 'off'}"
        print(su.print_summary(su.summary(full_df, label + " FULL")))
        print(su.print_summary(su.summary(is_df, label + " IS  ")))
        print(su.print_summary(su.summary(oos_df, label + " OOS ")))
        print(f"  IS+OOS n = {len(is_df)+len(oos_df)}, FULL n = {len(full_df)} (IS+OOS==FULL check)")
