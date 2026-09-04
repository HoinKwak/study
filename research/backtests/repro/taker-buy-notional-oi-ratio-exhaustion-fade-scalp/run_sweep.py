"""파라미터 스윕 — z_th, body_th, atr_stop_mult, atr_trail_mult, rr_target, max_hold_bars,
ema_slope_th_pct(엔진 파라미터, 재신호계산 불필요) + z_window(신호 재계산 필요)."""
import pickle

import common
import engine
import stats_utils as su

with open(common.SP / "sigs_200.pkl", "rb") as f:
    sigs = pickle.load(f)

print("### 파라미터 스윕(엔진 파라미터, mode=oi_buy_sell, reverse=False) — IS/OOS PF(R), t ###")
variants = []
for z_th in [2.5, 3.0, 3.5]:
    variants.append(dict(z_th=z_th))
for body_th in [0.30, 0.40, 0.50]:
    variants.append(dict(body_th=body_th))
for atr_stop_mult in [0.7, 1.0, 1.3]:
    variants.append(dict(atr_stop_mult=atr_stop_mult))
for atr_trail_mult in [1.2, 1.5, 2.0]:
    variants.append(dict(atr_trail_mult=atr_trail_mult))
for rr in [1.0, 1.3, 1.8]:
    variants.append(dict(rr_target=rr))
for mh in [6, 10, 16]:
    variants.append(dict(max_hold_bars=mh))
for slope_th in [0.0, 0.003, 0.008]:
    variants.append(dict(ema_slope_th_pct=slope_th))
variants.append(dict(use_1h_confirm=False))

rows = []
for v in variants:
    cfg = engine.RunConfig(mode="oi_buy_sell", reverse=False, fee_on=True, **v)
    trades = engine.run_all(sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    is_df, oos_df, full_df = su.split_is_oos(df)
    s_is = su.summary(is_df, "IS")
    s_oos = su.summary(oos_df, "OOS")
    rows.append(dict(variant=str(v), is_n=s_is["n"], is_pf=s_is["pf_r"], is_t=s_is["t"],
                     oos_n=s_oos["n"], oos_pf=s_oos["pf_r"], oos_t=s_oos["t"]))
    print(f"{str(v):30s} IS n={s_is['n']:5d} PF={s_is['pf_r']:.3f} t={s_is['t']:+.2f}  |  "
         f"OOS n={s_oos['n']:5d} PF={s_oos['pf_r']:.3f} t={s_oos['t']:+.2f}")

with open(common.SP / "sweep_results.pkl", "wb") as f:
    pickle.dump(rows, f)

print("\n### z_window 스윕(신호 재계산 필요) ###")
for zw in [120, 150, 200, 250, 300]:
    sigs_v = {s: common.build_signals(s, z_window=zw) for s in common.SYMBOLS}
    cfg = engine.RunConfig(mode="oi_buy_sell", reverse=False, fee_on=True)
    trades = engine.run_all(sigs_v, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    is_df, oos_df, full_df = su.split_is_oos(df)
    s_is = su.summary(is_df, "IS")
    s_oos = su.summary(oos_df, "OOS")
    print(f"z_window={zw:3d}  IS n={s_is['n']:5d} PF={s_is['pf_r']:.3f} t={s_is['t']:+.2f}  |  "
         f"OOS n={s_oos['n']:5d} PF={s_oos['pf_r']:.3f} t={s_oos['t']:+.2f}")
