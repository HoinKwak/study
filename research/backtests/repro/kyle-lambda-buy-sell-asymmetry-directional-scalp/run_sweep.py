"""파라미터 스윕: gap_hi/lo_pctile·sv_trigger_pctile·atr_trail_mult·atr_stop_mult·max_hold_bars
(신호 재계산 불필요) + lambda_window·gap_pctile_window·min_samples(신호 재계산 필요, common.with_params)."""
import pickle
import time

import common
import engine
import stats_utils as su

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

variants = []
for th in (70, 75, 80, 85, 90):
    variants.append(("gap_hi_pctile", th, dict(gap_hi_pctile=float(th),
                                               gap_lo_pctile=float(100 - th))))
for th in (80, 85, 88, 90, 92):
    variants.append(("sv_trigger_pctile", th, dict(sv_trigger_pctile=float(th))))
for m in (1.4, 1.6, 1.8, 2.0, 2.4):
    variants.append(("atr_trail_mult", m, dict(atr_trail_mult=m)))
for m in (1.0, 1.2, 1.4, 1.6):
    variants.append(("atr_stop_mult", m, dict(atr_stop_mult=m)))
for hh in (8, 12, 16, 20, 24):
    variants.append(("max_hold_bars", hh, dict(max_hold_bars=hh)))

rows = []
t0 = time.time()
for name, val, kw in variants:
    cfg = engine.RunConfig(gate="base", fee_on=True, **kw)
    trades = engine.run_all(sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    _, oos_df, _ = su.split_is_oos(df)
    s = su.summary(oos_df, f"{name}={val}")
    rows.append(s)
    print(su.print_summary(s))
print(f"\n총 {len(variants)}변형(청산·게이트 임계), {time.time()-t0:.1f}s")

print("\n=== lambda_window 스윕(신호 재계산 필요) ===")
for w_days in (2, 3, 4, 5):
    w = w_days * common.BARS_PER_DAY_15M
    use_sigs = {s: common.with_params(sig, s, lambda_window=w) for s, sig in sigs.items()}
    cfg = engine.RunConfig(gate="base", fee_on=True)
    trades = engine.run_all(use_sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    _, oos_df, _ = su.split_is_oos(df)
    s = su.summary(oos_df, f"lambda_window={w_days}d")
    print(su.print_summary(s))

print("\n=== gap_pctile_window 스윕(신호 재계산 필요) ===")
for gw_days in (15, 20, 25, 30):
    gw = gw_days * common.BARS_PER_DAY_15M
    use_sigs = {s: common.with_params(sig, s, gap_pctile_window=gw) for s, sig in sigs.items()}
    cfg = engine.RunConfig(gate="base", fee_on=True)
    trades = engine.run_all(use_sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    _, oos_df, _ = su.split_is_oos(df)
    s = su.summary(oos_df, f"gap_pctile_window={gw_days}d")
    print(su.print_summary(s))

print("\n=== min_samples_per_side 스윕(신호 재계산 필요) ===")
for ms in (30, 50, 80, 120):
    use_sigs = {s: common.with_params(sig, s, min_samples=ms) for s, sig in sigs.items()}
    cfg = engine.RunConfig(gate="base", fee_on=True)
    trades = engine.run_all(use_sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    _, oos_df, _ = su.split_is_oos(df)
    s = su.summary(oos_df, f"min_samples={ms}")
    print(su.print_summary(s))
