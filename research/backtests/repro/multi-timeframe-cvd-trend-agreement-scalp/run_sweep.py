"""파라미터 민감도 스윕(단독 변경, OOS net) — base 대비."""
from __future__ import annotations
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su

BASE_KW = dict(slope_lookback=6, breakout_lookback=10, vol_confirm_mult=1.2,
              atr_trail_mult=1.3, max_hold_hours=8)

SWEEP = [
    ("slope_lookback", 4), ("slope_lookback", 8), ("slope_lookback", 10),
    ("breakout_lookback", 8), ("breakout_lookback", 15), ("breakout_lookback", 20),
    ("vol_confirm_mult", 1.1), ("vol_confirm_mult", 1.5),
    ("atr_trail_mult", 1.0), ("atr_trail_mult", 1.8),
    ("max_hold_hours", 4), ("max_hold_hours", 12),
]

_sig_cache = {}


def get_signals(slope_lookback, breakout_lookback):
    key = (slope_lookback, breakout_lookback)
    if key not in _sig_cache:
        cfg = engine.RunConfig(slope_lookback=slope_lookback, breakout_lookback=breakout_lookback)
        _sig_cache[key] = {sym: engine.build_signals(sym, cfg) for sym in common.SYMBOLS}
    return _sig_cache[key]


def run_one(kw):
    cfg = engine.RunConfig(**kw)
    sigs = get_signals(kw["slope_lookback"], kw["breakout_lookback"])
    trades_all = []
    for sym, sig in sigs.items():
        trades_all.extend(engine.run_symbol(sym, sig, cfg))
    df = su.trades_df(trades_all, rcol="r_net")
    _, oos_df, _ = su.split_is_oos(df)
    return su.summary(oos_df, "")


if __name__ == "__main__":
    t0 = time.time()
    base_res = run_one(dict(BASE_KW))
    print("BASE OOS:", su.fmt({**base_res, "label": "base"}))
    n_pass = 0
    for k, v in SWEEP:
        kw = dict(BASE_KW)
        kw[k] = v
        res = run_one(kw)
        passed = (res["pf_r"] >= 1.3) and (res["t"] >= 1.96)
        n_pass += int(passed)
        flag = "PASS" if passed else ""
        print(su.fmt({**res, "label": f"{k}={v}"}), flag)
    print(f"\n통과(PF>=1.3 AND t>=1.96): {n_pass}/{len(SWEEP)}")
    print(f"TOTAL TIME {time.time()-t0:.1f}s")
