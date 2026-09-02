"""파라미터 민감도 스윕(n=35, gated 모드): gate_pctile·pctile_window_days·donchian_period·
body_atr_mult·atr_trail_mult 를 스펙이 명시한 범위 내에서 흔들어 강건성 확인."""
from __future__ import annotations

import common
import engine
import stats_utils as su


def run(gate_pctile=10.0, pctile_window_days=60, donchian_period=20, body_atr_mult=1.0,
       atr_trail_mult=1.5):
    regime = common.build_regime_1h(pctile_window_days=pctile_window_days, symbols=common.EXT_SYMBOLS)
    btc = common.build_btc_signals(donchian_period=donchian_period)
    aligned = common.align_regime_to_15m(btc.df15, regime)
    cfg = engine.RunConfig(mode="gated", gate_pctile=gate_pctile, body_atr_mult=body_atr_mult,
                           atr_trail_mult=atr_trail_mult)
    trades = engine.run_all(btc, aligned, cfg)
    df = su.trades_df(trades)
    is_df, oos_df, full_df = su.split_is_oos(df)
    return is_df, oos_df


def main():
    base = dict(gate_pctile=10.0, pctile_window_days=60, donchian_period=20, body_atr_mult=1.0,
               atr_trail_mult=1.5)
    variants = []
    for gp in [5.0, 15.0, 20.0]:
        variants.append(("gate_pctile", gp, {**base, "gate_pctile": gp}))
    for pw in [30, 90]:
        variants.append(("pctile_window_days", pw, {**base, "pctile_window_days": pw}))
    for dp in [10, 30]:
        variants.append(("donchian_period", dp, {**base, "donchian_period": dp}))
    for ba in [0.8, 1.2, 1.5]:
        variants.append(("body_atr_mult", ba, {**base, "body_atr_mult": ba}))
    for at in [1.0, 2.0, 2.5]:
        variants.append(("atr_trail_mult", at, {**base, "atr_trail_mult": at}))

    print("=== baseline ===")
    is_df, oos_df = run(**base)
    print(" IS ", su.print_summary(su.summary(is_df, "base_IS")))
    print(" OOS", su.print_summary(su.summary(oos_df, "base_OOS")))

    print("\n=== 스윕 ===")
    for name, val, kw in variants:
        is_df, oos_df = run(**kw)
        s_is = su.summary(is_df, f"{name}={val}_IS")
        s_oos = su.summary(oos_df, f"{name}={val}_OOS")
        print(f"{name}={val:>6}: IS  n={s_is['n']:4d} PF={s_is['pf_r']:.3f} t={s_is['t']:+.2f} | "
             f"OOS n={s_oos['n']:4d} PF={s_oos['pf_r']:.3f} t={s_oos['t']:+.2f}")


if __name__ == "__main__":
    main()
