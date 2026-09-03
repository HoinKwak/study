"""파라미터 민감도 스윕(gated 모드): spread_z 임계값·spread_z_window·rv_window·donchian_period·
atr_trail_mult·atr_stop_mult·max_hold 를 스펙이 명시한 범위 내에서 흔들어 강건성 확인(10변형+)."""
from __future__ import annotations

import common as C
import engine
import gates
import stats_utils as su


def run(rv_window=C.RV_WINDOW, spread_z_window=C.SPREAD_Z_WINDOW, short_th=C.SPREAD_Z_SHORT_TH,
       long_th=C.SPREAD_Z_LONG_TH, donchian_period=C.DONCHIAN_LOOKBACK,
       atr_trail_mult=C.ATR_TRAIL_MULT, atr_stop_mult=C.ATR_STOP_MULT, max_hold=C.MAX_HOLD):
    udata = C.build_universe_data(rv_window=rv_window)
    gate, _ = gates.build_gate_oiweighted(spread_z_window=spread_z_window, short_th=short_th,
                                          long_th=long_th, udata=udata)
    btc = C.build_btc_signals(donchian_period=donchian_period)
    aligned = C.align_1h_to_15m(btc.df15, gate.to_frame("gate"))["gate"]
    trades = engine.run_variant(btc.df15, btc.don_hi, btc.don_lo, btc.atr14, aligned, "gated",
                                atr_trail_mult=atr_trail_mult, atr_stop_mult=atr_stop_mult,
                                max_hold=max_hold)
    df = engine.trades_to_df(trades)
    is_df, oos_df, full_df = su.split_is_oos(df)
    return is_df, oos_df


def main():
    base = dict(rv_window=24, spread_z_window=90, short_th=1.5, long_th=-1.0, donchian_period=20,
               atr_trail_mult=1.4, atr_stop_mult=1.0, max_hold=10)
    variants = []
    for v in [12, 48]:
        variants.append(("rv_window", v, {**base, "rv_window": v}))
    for v in [60, 150]:
        variants.append(("spread_z_window", v, {**base, "spread_z_window": v}))
    for v in [1.0, 2.0]:
        variants.append(("short_th", v, {**base, "short_th": v}))
    for v in [-1.5, -0.5]:
        variants.append(("long_th", v, {**base, "long_th": v}))
    for v in [15, 30]:
        variants.append(("donchian_period", v, {**base, "donchian_period": v}))
    for v in [1.0, 2.0]:
        variants.append(("atr_trail_mult", v, {**base, "atr_trail_mult": v}))
    for v in [0.5, 1.5]:
        variants.append(("atr_stop_mult", v, {**base, "atr_stop_mult": v}))
    for v in [5, 20]:
        variants.append(("max_hold", v, {**base, "max_hold": v}))

    print("=== baseline ===")
    is_df, oos_df = run(**base)
    print(" IS ", su.print_summary(su.summary(is_df, "base_IS")))
    print(" OOS", su.print_summary(su.summary(oos_df, "base_OOS")))

    print(f"\n=== 스윕({len(variants)}변형) ===")
    pass_count = 0
    for name, val, kw in variants:
        is_df, oos_df = run(**kw)
        s_is = su.summary(is_df, f"{name}={val}_IS")
        s_oos = su.summary(oos_df, f"{name}={val}_OOS")
        ok = s_oos["pf_r"] >= 1.3 and s_oos["t"] >= 1.96
        pass_count += int(ok)
        print(f"{name}={val:>7}: IS  n={s_is['n']:5d} PF={s_is['pf_r']:.3f} t={s_is['t']:+.2f} | "
             f"OOS n={s_oos['n']:5d} PF={s_oos['pf_r']:.3f} t={s_oos['t']:+.2f} "
             f"{'PASS' if ok else ''}")
    print(f"\n통과선(OOS PF>=1.3 AND t>=1.96) 충족 변형 수: {pass_count}/{len(variants)}")


if __name__ == "__main__":
    main()
