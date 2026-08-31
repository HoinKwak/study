"""파라미터 스윕: streak_th(3~8) / donchian_len(15~30) / ema_filter(30~100) / max_hold_bars(28~56).
스펙이 나열한 축 전부(atr_sl_mult·atr_trail_mult 는 스펙에 범위 미제시라 고정값 유지)."""
import pickle
import sys
import time
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su

AXES = [
    ("streak_th", [3, 4, 5, 6, 7, 8]),
    ("donchian_period", [15, 20, 25, 30]),
    ("ema_period", [30, 50, 70, 100]),
    ("max_hold_bars", [28, 35, 42, 49, 56]),
]

for short_mode in ["streak_down", "streak_up_alt"]:
    print(f"\n############ short_mode={short_mode} ############")
    for axis_name, values in AXES:
        for v in values:
            t0 = time.time()
            sig_kw = {}
            cfg_kw = {"short_mode": short_mode}
            if axis_name in ("donchian_period", "ema_period", "streak_th"):
                sig_kw[axis_name] = v
                if axis_name == "streak_th":
                    cfg_kw["streak_th"] = v
                elif axis_name == "donchian_period":
                    cfg_kw["donchian_period"] = v
                elif axis_name == "ema_period":
                    cfg_kw["ema_period"] = v
            else:
                cfg_kw[axis_name] = v
            sigs = engine.load_all_signals(**sig_kw)
            cfg = engine.RunConfig(mode="gated", **cfg_kw)
            trades = engine.run_all(sigs, cfg)
            df = su.trades_df([t for lst in trades.values() for t in lst])
            is_df, oos_df, full_df = su.split_is_oos(df)
            d = su.summary(oos_df, f"{axis_name}={v}")
            is_pf = su.pf_r(is_df)
            print(f"  {axis_name}={v:<6} OOS n={d['n']:4d} PF(R)={d['pf_r']:.3f} t={d['t']:+.3f} "
                 f"p={d['p']:.4f} || IS n={len(is_df):4d} PF(R)={is_pf:.3f}  ({time.time()-t0:.1f}s)")
