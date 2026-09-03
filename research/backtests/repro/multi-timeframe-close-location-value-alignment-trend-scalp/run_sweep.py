"""파라미터 민감도 스윕(단독 변경, OOS net) — base 대비 12변형."""
from __future__ import annotations
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su

BASE_KW = dict(clv15_th_long=0.75, clv15_th_short=0.25, clv1h_th_long=0.65, clv1h_th_short=0.35,
              clv4h_th_long=0.60, clv4h_th_short=0.40, vol_mult=1.2, atr_stop_mult=1.0,
              atr_trail_mult=2.0, max_hold_bars=32)

SWEEP = [
    ("clv15_th_long", 0.65, "clv15_th_short", 0.35),
    ("clv15_th_long", 0.85, "clv15_th_short", 0.15),
    ("clv1h_th_long", 0.55, "clv1h_th_short", 0.45),
    ("clv1h_th_long", 0.75, "clv1h_th_short", 0.25),
    ("clv4h_th_long", 0.50, "clv4h_th_short", 0.50),
    ("clv4h_th_long", 0.70, "clv4h_th_short", 0.30),
    ("vol_mult", 1.0, None, None),
    ("vol_mult", 1.5, None, None),
    ("atr_stop_mult", 0.7, None, None),
    ("atr_stop_mult", 1.5, None, None),
    ("atr_trail_mult", 1.5, None, None),
    ("atr_trail_mult", 3.0, None, None),
    ("max_hold_bars", 16, None, None),
    ("max_hold_bars", 48, None, None),
]

_sig_cache = {}


def get_signals(kw):
    key = tuple(sorted(kw.items()))
    if key not in _sig_cache:
        cfg = engine.RunConfig(**kw)
        _sig_cache[key] = {sym: engine.build_signals(sym, cfg) for sym in common.SYMBOLS}
    return _sig_cache[key]


def run_one(kw):
    cfg = engine.RunConfig(**kw)
    sigs = get_signals(kw)
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
    for k1, v1, k2, v2 in SWEEP:
        kw = dict(BASE_KW)
        kw[k1] = v1
        if k2:
            kw[k2] = v2
        res = run_one(kw)
        passed = (res["pf_r"] >= 1.3) and (res["t"] >= 1.96)
        n_pass += int(passed)
        flag = "PASS" if passed else ""
        lbl = f"{k1}={v1}" + (f",{k2}={v2}" if k2 else "")
        print(su.fmt({**res, "label": lbl}), flag)
    print(f"\n통과(PF>=1.3 AND t>=1.96): {n_pass}/{len(SWEEP)}")
    print(f"TOTAL TIME {time.time()-t0:.1f}s")
