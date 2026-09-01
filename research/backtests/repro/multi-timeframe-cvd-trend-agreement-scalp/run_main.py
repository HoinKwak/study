"""메인 실행: base(net/gross) + 대조군 3종 + 반전(3안 포함) + 3안, IS/OOS/FULL, 종목별, 동시진입일."""
from __future__ import annotations
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su


def build_all_signals():
    cfg0 = engine.RunConfig()
    sigs = {}
    for sym in common.SYMBOLS:
        sigs[sym] = engine.build_signals(sym, cfg0)
    return sigs


def run_variant(sigs, cfg, label):
    trades_all = []
    for sym, sig in sigs.items():
        trades_all.extend(engine.run_symbol(sym, sig, cfg))
    df = su.trades_df(trades_all, rcol=("r_net" if cfg.cost_on else "r_gross"))
    is_df, oos_df, full_df = su.split_is_oos(df)
    print(f"\n--- {label} ---")
    print(su.fmt(su.summary(is_df, f"{label} IS")))
    print(su.fmt(su.summary(oos_df, f"{label} OOS")))
    print(su.fmt(su.summary(full_df, f"{label} FULL")))
    print(f"  IS+OOS==FULL check: {len(is_df)}+{len(oos_df)}={len(is_df)+len(oos_df)} vs FULL={len(full_df)}")
    return df, is_df, oos_df, full_df


if __name__ == "__main__":
    t0 = time.time()
    sigs = build_all_signals()
    print(f"signals built for {len(sigs)} symbols in {time.time()-t0:.1f}s")

    results = {}

    # base net
    cfg_base = engine.RunConfig(signal_mode="both", direction_mode="normal", cost_on=True)
    results["base_net"] = run_variant(sigs, cfg_base, "base(net, both-gate)")

    # base gross(무비용)
    cfg_gross = engine.RunConfig(signal_mode="both", direction_mode="normal", cost_on=False)
    results["base_gross"] = run_variant(sigs, cfg_gross, "base(gross, fee=0/slip=0)")

    # 대조군 ①CVD_1h 단독
    cfg_c1 = engine.RunConfig(signal_mode="h1_only", direction_mode="normal", cost_on=True)
    results["ctrl1_h1only"] = run_variant(sigs, cfg_c1, "ctrl1(CVD_1h 단독게이트, net)")

    # 대조군 ②CVD_5m 단독
    cfg_c2 = engine.RunConfig(signal_mode="h5_only", direction_mode="normal", cost_on=True)
    results["ctrl2_h5only"] = run_variant(sigs, cfg_c2, "ctrl2(CVD_5m 단독게이트, net)")

    # 대조군 ③게이트 없음
    cfg_c3 = engine.RunConfig(signal_mode="none", direction_mode="normal", cost_on=True)
    results["ctrl3_nogate"] = run_variant(sigs, cfg_c3, "ctrl3(게이트없음, net)")

    # 반전
    cfg_rev = engine.RunConfig(signal_mode="both", direction_mode="reverse", cost_on=True)
    results["reverse_net"] = run_variant(sigs, cfg_rev, "reverse(both-gate, net)")

    cfg_rev_gross = engine.RunConfig(signal_mode="both", direction_mode="reverse", cost_on=False)
    results["reverse_gross"] = run_variant(sigs, cfg_rev_gross, "reverse(both-gate, gross)")

    # 3안: 테제무효화 청산 완전 비활성(반전모드)
    cfg_rev_noinval = engine.RunConfig(signal_mode="both", direction_mode="reverse", cost_on=True,
                                       disable_thesis_exit=True)
    results["reverse_noinval"] = run_variant(sigs, cfg_rev_noinval, "reverse(테제무효화 비활성, net)")

    # 종목별 OOS(net, base)
    print("\n=== 종목별 OOS(net, base) ===")
    for sym, sig in sigs.items():
        trades = engine.run_symbol(sym, sig, cfg_base)
        df = su.trades_df(trades, rcol="r_net")
        _, oos_df, _ = su.split_is_oos(df)
        print(su.fmt(su.summary(oos_df, sym)))

    # 청산사유·보유기간 분포(정방향 vs 반전, OOS)
    print("\n=== 청산사유·보유기간 분포(OOS) ===")
    for lbl, key in [("정방향", "base_net"), ("반전", "reverse_net")]:
        _, oos_df, _ = results[key][1], results[key][2], results[key][3]
        reasons = oos_df.groupby("reason").size()
        mean_hold = oos_df["holding_bars"].mean()
        zero_hold = (oos_df["holding_bars"] == 0).mean() * 100
        print(f"{lbl}: n={len(oos_df)} reasons={dict(reasons)} mean_hold_bars={mean_hold:.2f} "
              f"0봉청산율={zero_hold:.1f}%")

    print(f"\nTOTAL TIME {time.time()-t0:.1f}s")
