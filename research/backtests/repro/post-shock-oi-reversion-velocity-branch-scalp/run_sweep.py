"""파라미터 스윕(10변형+) — OOS net·gross PF(R)·t 보고."""
from __future__ import annotations

import common as c
import engine
import stats_utils as su


VARIANTS = [
    ("base", dict()),
    ("shock_atr_mult=1.5", dict(shock_atr_mult=1.5)),
    ("shock_atr_mult=1.75", dict(shock_atr_mult=1.75)),
    ("shock_atr_mult=2.5", dict(shock_atr_mult=2.5)),
    ("shock_atr_mult=3.0", dict(shock_atr_mult=3.0)),
    ("reversion_window=2", dict(reversion_window=2)),
    ("reversion_window=4", dict(reversion_window=4)),
    ("reversion_window=6", dict(reversion_window=6)),
    ("revert_pct=0.3", dict(revert_pct=0.3)),
    ("revert_pct=0.5", dict(revert_pct=0.5)),
    ("breakout_lookback=3", dict(breakout_lookback=3)),
    ("breakout_lookback=8", dict(breakout_lookback=8)),
    ("atr_trail_mult=1.0", dict(atr_trail_mult=1.0)),
    ("atr_trail_mult=2.0", dict(atr_trail_mult=2.0)),
    ("atr_stop_mult=0.75", dict(atr_stop_mult=0.75)),
    ("atr_stop_mult=1.5", dict(atr_stop_mult=1.5)),
    ("rr_target=1.2", dict(rr_target=1.2)),
    ("rr_target=2.0", dict(rr_target=2.0)),
    ("max_hold_bars=8", dict(max_hold_bars=8)),
    ("max_hold_bars=16", dict(max_hold_bars=16)),
    ("no_ema_confirm", dict(require_ema_confirm=False)),
]


def main():
    data = c.load_all()
    print(f"{'variant':24s} {'n_OOS':>6s} {'net_PF':>8s} {'net_t':>8s} {'gross_PF':>9s} {'gross_t':>8s}")
    for name, kw in VARIANTS:
        cfg_net = engine.Config(fee_on=True, **kw)
        df_net, _ = engine.run(c.SYMBOLS, data, cfg_net)
        _, oos_net, _ = su.split_is_oos(df_net)
        s_net = su.summary(oos_net, name)

        cfg_gross = engine.Config(fee_on=False, **kw)
        df_gross, _ = engine.run(c.SYMBOLS, data, cfg_gross)
        _, oos_gross, _ = su.split_is_oos(df_gross)
        s_gross = su.summary(oos_gross, name)

        print(f"{name:24s} {s_net['n']:6d} {s_net['pf_r']:8.3f} {s_net['t']:8.3f} "
             f"{s_gross['pf_r']:9.3f} {s_gross['t']:8.3f}")


if __name__ == "__main__":
    main()
