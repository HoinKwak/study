"""파라미터 스윕: window / z_th / price_filter / atr_tp_mult / atr_sl_mult / time_exit_bars.
signal_source=resid, dir_mode=A(최선 변형) 고정, net(fee_on) 기준."""
import pickle
import sys
import time

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiresid")
import common
import engine
import stats_utils as su

AXES = [
    ("window", [40, 50, 60, 75, 90]),
    ("z_th", [2.5, 2.75, 3.0, 3.25, 3.5]),
    ("price_filter", [0.2, 0.25, 0.3, 0.4, 0.5]),
    ("atr_tp_mult", [1.5, 2.0, 2.5, 3.0]),
    ("atr_sl_mult", [0.75, 1.0, 1.25, 1.5]),
    ("time_exit_bars", [12, 24, 36, 48]),
]

results = []
base_sigs_cache = {}
for axis_name, values in AXES:
    for v in values:
        t0 = time.time()
        sig_kw = {}
        cfg_kw = {}
        if axis_name == "window":
            sig_kw["window"] = v
            cfg_kw["window"] = v
        else:
            cfg_kw[axis_name] = v
        sig_key = sig_kw.get("window", 60)
        if sig_key not in base_sigs_cache:
            base_sigs_cache[sig_key] = engine.load_all_signals(window=sig_key)
        sigs = base_sigs_cache[sig_key]
        cfg = engine.RunConfig(signal_source="resid", dir_mode="A", **cfg_kw)
        trades = engine.run_all(sigs, cfg)
        all_trades = [t for lst in trades.values() for t in lst]
        df = su.trades_df(all_trades)
        is_df, oos_df, full_df = su.split_is_oos(df)
        d = su.summary(oos_df, f"{axis_name}={v}")
        d["is_pf"] = su.pf_r(is_df)
        d["is_n"] = len(is_df)
        d["axis"] = axis_name
        d["value"] = v
        results.append(d)
        print(f"{axis_name:16s}={str(v):8s} OOS n={d['n']:4d} PF(R)={d['pf_r']:.3f} t={d['t']:+.3f} "
             f"p={d['p']:.4f} || IS n={d['is_n']:4d} PF(R)={d['is_pf']:.3f}  ({time.time()-t0:.1f}s)")

with open(f"{common.SP}/results_sweep.pkl", "wb") as f:
    pickle.dump(results, f)
print("done")
