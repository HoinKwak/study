"""파라미터 스윕: zcr_pctile_th·donchian_lb·atr_trail_mult·atr_stop_mult·max_hold_bars.
zcr_window 은 신호 자체를 재계산해야 하므로 common.with_zcr_window() 로 별도 처리."""
import pickle
import time

import common
import engine
import stats_utils as su

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

variants = []
for th in (20, 25, 30, 35, 40):
    variants.append(("zcr_pctile_th", th, dict(zcr_pctile_th=float(th))))
for lb in (10, 15, 20, 25, 30):
    variants.append(("donchian_lb", lb, dict(donchian_lb=lb)))
for m in (1.0, 1.5, 2.0, 2.5):
    variants.append(("atr_trail_mult", m, dict(atr_trail_mult=m)))
for m in (0.8, 1.0, 1.5, 2.0):
    variants.append(("atr_stop_mult", m, dict(atr_stop_mult=m)))
for h in (12, 18, 24, 36, 48):
    variants.append(("max_hold_bars", h, dict(max_hold_bars=h)))

rows = []
t0 = time.time()
for name, val, kw in variants:
    lb = kw.get("donchian_lb")
    use_sigs = sigs
    if lb is not None and lb != common.DONCHIAN_LB:
        use_sigs = {s: common.with_donchian_lb(sig, lb) for s, sig in sigs.items()}
    cfg = engine.RunConfig(gate="zcr_lo", fee_on=True, **kw)
    trades = engine.run_all(use_sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    _, oos_df, _ = su.split_is_oos(df)
    s = su.summary(oos_df, f"{name}={val}")
    rows.append(s)
    print(su.print_summary(s))
print(f"\n총 {len(variants)}변형, {time.time()-t0:.1f}s")

# zcr_window 스윕(신호 재계산)
print("\n=== zcr_window 스윕(신호 재계산 필요) ===")
for w in (12, 18, 24, 36, 48):
    use_sigs = {s: common.with_zcr_window(s, sig, w) for s, sig in sigs.items()}
    max_trans = w - 1
    cfg = engine.RunConfig(gate="zcr_lo", fee_on=True)
    trades = engine.run_all(use_sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    _, oos_df, _ = su.split_is_oos(df)
    s = su.summary(oos_df, f"zcr_window={w}(trans={max_trans})")
    print(su.print_summary(s))
