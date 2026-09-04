"""파라미터 스윕(개별 파라미터 1개씩 변경, 스펙 명시 범위) + LOO(종목 하나씩 제외)."""
from __future__ import annotations

import pandas as pd

import common
import engine
import stats_utils as su


def oos_summary(bundles, cfg, label):
    trades = engine.run_all(bundles, cfg)
    rows = [su.trades_df(trades.get(s, [])) for s in bundles.keys()]
    pooled = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    _, oos, _ = su.split_is_oos(pooled)
    d = su.summary(oos, label)
    print(" ", su.print_summary(d))
    return d


def main():
    bundles_default = engine.load_all_bundles()   # window=60 기본
    print("=== 파라미터 스윕(OOS, PF(R)·t) ===")

    print("\n-- z_th (1.5 / 2.0[base] / 2.5) --")
    for zt in (1.5, 2.0, 2.5):
        cfg = engine.RunConfig(z_th=zt)
        oos_summary(bundles_default, cfg, f"z_th={zt}")

    print("\n-- ema_period (10 / 20[base] / 30) --  (주의: EMA 는 Bundle 에 사전계산되므로 "
         "종목별로 해당 ema_period 로 재빌드)")
    for ep in (10, 20, 30):
        bundles_ep = engine.load_all_bundles(ema_period=ep)
        cfg = engine.RunConfig(ema_period=ep)
        oos_summary(bundles_ep, cfg, f"ema={ep}")

    print("\n-- atr_sl_mult (1.5 / 2.0[base] / 2.5) --")
    for m in (1.5, 2.0, 2.5):
        cfg = engine.RunConfig(atr_sl_mult=m)
        oos_summary(bundles_default, cfg, f"atr_sl_mult={m}")

    print("\n-- rr_target (1.5 / 2.0[base] / 3.0) --")
    for rr in (1.5, 2.0, 3.0):
        cfg = engine.RunConfig(rr_target=rr)
        oos_summary(bundles_default, cfg, f"rr_target={rr}")

    print("\n-- max_hold_bars (21=3.5d / 42[base]=7d / 84=14d) --")
    for mh in (21, 42, 84):
        cfg = engine.RunConfig(max_hold_bars=mh)
        oos_summary(bundles_default, cfg, f"max_hold={mh}")

    print("\n-- window(beta/z, 40 / 60[base] / 90) --")
    for w in (40, 60, 90):
        bundles_w = engine.load_all_bundles(window=w)
        cfg = engine.RunConfig(window=w)
        oos_summary(bundles_w, cfg, f"window={w}")

    print("\n=== LOO(종목 하나씩 제외, base cfg, OOS 풀링) ===")
    base_cfg = engine.RunConfig()
    for excl in common.ALT_SYMBOLS:
        sub_syms = [s for s in common.ALT_SYMBOLS if s != excl]
        bundles_sub = {s: bundles_default[s] for s in sub_syms}
        oos_summary(bundles_sub, base_cfg, f"LOO(제외 {excl})")


if __name__ == "__main__":
    main()
