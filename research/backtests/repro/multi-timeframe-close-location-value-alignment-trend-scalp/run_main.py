"""메인 실행: base(net/gross) + 대조군4종(15m단독/두TF/게이트없음/IBS단독) + 반전(+3안), IS/OOS/FULL,
종목별, 청산사유·보유기간 분포(정방향/반전)."""
from __future__ import annotations
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import ibs_ctrl
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


def run_ibs_variant(label, direction_mode="normal", cost_on=True):
    icfg = ibs_ctrl.IbsConfig(direction_mode=direction_mode, cost_on=cost_on)
    trades_all = []
    for sym in common.SYMBOLS:
        sig = ibs_ctrl.build_signals(sym)
        if sig is None:
            continue
        trades_all.extend(ibs_ctrl.run_symbol(sym, sig, icfg))
    df = su.trades_df(trades_all, rcol=("r_net" if cost_on else "r_gross"))
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

    cfg_base = engine.RunConfig(signal_mode="all3", direction_mode="normal", cost_on=True)
    results["base_net"] = run_variant(sigs, cfg_base, "base(net, 15m/1h/4h 정렬)")

    cfg_gross = engine.RunConfig(signal_mode="all3", direction_mode="normal", cost_on=False)
    results["base_gross"] = run_variant(sigs, cfg_gross, "base(gross, fee=0/slip=0)")

    cfg_c1 = engine.RunConfig(signal_mode="15m_only", direction_mode="normal", cost_on=True)
    results["ctrl_15m_only"] = run_variant(sigs, cfg_c1, "ctrl(단일TF 15m만, net)")

    cfg_c2 = engine.RunConfig(signal_mode="two_tf", direction_mode="normal", cost_on=True)
    results["ctrl_two_tf"] = run_variant(sigs, cfg_c2, "ctrl(두TF 15m+1h만, net)")

    cfg_c3 = engine.RunConfig(signal_mode="no_gate", direction_mode="normal", cost_on=True)
    results["ctrl_no_gate"] = run_variant(sigs, cfg_c3, "ctrl(게이트없음=거래량+캔들색, net)")

    results["ibs_alone"] = run_ibs_variant("ctrl(IBS단독 15m 평균회귀, net)")
    results["ibs_alone_gross"] = run_ibs_variant("ctrl(IBS단독 gross)", cost_on=False)

    cfg_rev = engine.RunConfig(signal_mode="all3", direction_mode="reverse", cost_on=True)
    results["reverse_net"] = run_variant(sigs, cfg_rev, "reverse(15m/1h/4h 정렬, net)")

    cfg_rev_gross = engine.RunConfig(signal_mode="all3", direction_mode="reverse", cost_on=False)
    results["reverse_gross"] = run_variant(sigs, cfg_rev_gross, "reverse(gross)")

    cfg_rev_noflip = engine.RunConfig(signal_mode="all3", direction_mode="reverse", cost_on=True,
                                      disable_clv_flip_exit=True)
    results["reverse_noflip"] = run_variant(sigs, cfg_rev_noflip, "reverse(CLV반전청산 비활성, net)")

    print("\n=== 종목별 OOS(net, base) ===")
    for sym, sig in sigs.items():
        trades = engine.run_symbol(sym, sig, cfg_base)
        df = su.trades_df(trades, rcol="r_net")
        _, oos_df, _ = su.split_is_oos(df)
        print(su.fmt(su.summary(oos_df, sym)))

    print("\n=== 청산사유·보유기간 분포(OOS, 정방향 vs 반전 vs 반전+CLV반전청산비활성) ===")
    for lbl, key in [("정방향", "base_net"), ("반전", "reverse_net"), ("반전+비활성", "reverse_noflip")]:
        _, oos_df, _ = results[key][1], results[key][2], results[key][3]
        reasons = oos_df.groupby("reason").size()
        mean_hold = oos_df["holding_bars"].mean()
        zero_hold = (oos_df["holding_bars"] == 0).mean() * 100
        print(f"{lbl}: n={len(oos_df)} reasons={dict(reasons)} mean_hold_bars={mean_hold:.2f} "
              f"0봉청산율={zero_hold:.1f}%")

    print(f"\nTOTAL TIME {time.time()-t0:.1f}s")
