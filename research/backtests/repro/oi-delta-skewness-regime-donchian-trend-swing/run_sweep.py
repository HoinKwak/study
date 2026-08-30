"""파라미터 스윕: doi_window / pctile_window_days / pctile_th / donchian_period."""
import pickle
import sys
import time

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiskew")
import common
import engine
import stats_utils as su

AXES = [
    ("doi_window", [30, 45, 60, 90, 120]),
    ("pctile_window_days", [90, 120, 180, 270, 365]),
    ("pctile_th", [(60, 40), (65, 35), (70, 30), (75, 25), (80, 20)]),
    ("donchian_period", [10, 15, 20, 30, 40]),
]

results = []
for axis_name, values in AXES:
    for v in values:
        kw = {}
        cfg_kw = {}
        if axis_name == "pctile_th":
            cfg_kw["pctile_hi"], cfg_kw["pctile_lo"] = v
            label = f"pctile_th={v[0]}/{v[1]}"
        else:
            kw[axis_name] = v
            cfg_kw[axis_name] = v
            label = f"{axis_name}={v}"
        t0 = time.time()
        sigs = engine.load_all_signals(**kw)
        cfg = engine.RunConfig(**cfg_kw)
        trades = engine.run_all(sigs, cfg)
        all_trades = [t for lst in trades.values() for t in lst]
        df = su.trades_df(all_trades)
        is_df, oos_df, full_df = su.split_is_oos(df)
        d = su.summary(oos_df, label)
        d["is_pf"] = su.pf_r(is_df)
        d["is_n"] = len(is_df)
        results.append(d)
        print(f"{label:28s} OOS n={d['n']:4d} PF(R)={d['pf_r']:.3f} t={d['t']:+.3f} "
             f"p={d['p']:.4f} || IS n={d['is_n']:4d} PF(R)={d['is_pf']:.3f}  "
             f"({time.time()-t0:.1f}s)")

with open(f"{common.SP}/results_sweep.pkl", "wb") as f:
    pickle.dump(results, f)
print("done")
