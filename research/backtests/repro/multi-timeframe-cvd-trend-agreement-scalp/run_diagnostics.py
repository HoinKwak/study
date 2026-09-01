"""부트스트랩(대조군 비교) + de-clustering(net/gross 병행) + LOO + top-N + 셔플."""
from __future__ import annotations
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su


def build_all_signals():
    cfg0 = engine.RunConfig()
    return {sym: engine.build_signals(sym, cfg0) for sym in common.SYMBOLS}


def get_trades_df(sigs, cfg, rcol):
    trades_all = []
    for sym, sig in sigs.items():
        trades_all.extend(engine.run_symbol(sym, sig, cfg))
    return su.trades_df(trades_all, rcol=rcol)


if __name__ == "__main__":
    t0 = time.time()
    sigs = build_all_signals()

    cfg_base = engine.RunConfig(signal_mode="both", direction_mode="normal", cost_on=True)
    cfg_c1 = engine.RunConfig(signal_mode="h1_only", direction_mode="normal", cost_on=True)
    cfg_c2 = engine.RunConfig(signal_mode="h5_only", direction_mode="normal", cost_on=True)
    cfg_c3 = engine.RunConfig(signal_mode="none", direction_mode="normal", cost_on=True)

    df_base = get_trades_df(sigs, cfg_base, "r_net")
    df_c1 = get_trades_df(sigs, cfg_c1, "r_net")
    df_c2 = get_trades_df(sigs, cfg_c2, "r_net")
    df_c3 = get_trades_df(sigs, cfg_c3, "r_net")

    _, oos_base, _ = su.split_is_oos(df_base)
    _, oos_c1, _ = su.split_is_oos(df_c1)
    _, oos_c2, _ = su.split_is_oos(df_c2)
    _, oos_c3, _ = su.split_is_oos(df_c3)

    print("=== 사전 등록 폐기조건 (c): base vs 대조군 3종 부트스트랩(matched-n, 5000회) ===")
    for lbl, ctrl_df in [("ctrl1(1h단독)", oos_c1), ("ctrl2(5m단독)", oos_c2), ("ctrl3(게이트없음)", oos_c3)]:
        res = su.bootstrap_matched_n_diff(ctrl_df["r"].to_numpy(), oos_base["r"].to_numpy())
        print(f"base vs {lbl}: base백분위={res['pctile']:.1f} base_mean={res['base_mean']:.4f} "
              f"pool_dist_mean={res['pool_dist_mean']:.4f} n={res['n']}")
        res2 = su.bootstrap_diff_indep(oos_base["r"].to_numpy(), ctrl_df["r"].to_numpy())
        print(f"  독립표본 부트스트랩 P(base<=ctrl)={res2['p_a_le_b']:.4f} "
              f"(mean_base={res2['mean_a']:.4f} mean_ctrl={res2['mean_b']:.4f})")

    print("\n=== base ⊆ pool 중첩 점검(ctrl1 = 1h단독, base 의 상위집합인지) ===")
    ov = pd.merge(oos_base[["symbol", "entry_time"]], oos_c1[["symbol", "entry_time"]],
                  on=["symbol", "entry_time"], how="inner")
    print(f"base n={len(oos_base)}, ctrl1 n={len(oos_c1)}, 중첩={len(ov)} "
          f"({len(ov)/len(oos_base)*100:.1f}% of base)")

    print("\n=== de-clustering(캘린더일 + 3~5일 롤링, net) — base OOS ===")
    for label, fn in [("원본", lambda d: d),
                      ("캘린더일", su.decluster_calendar_day),
                      ("3일롤링", lambda d: su.decluster_rolling_days(d, 3)),
                      ("4일롤링", lambda d: su.decluster_rolling_days(d, 4)),
                      ("5일롤링", lambda d: su.decluster_rolling_days(d, 5))]:
        d = fn(oos_base)
        print(su.fmt(su.summary(d, f"net {label}")))

    print("\n=== de-clustering(gross, cost_on=False) — base OOS (폐기조건 gross 병행) ===")
    df_gross = get_trades_df(sigs, engine.RunConfig(signal_mode="both", cost_on=False), "r_gross")
    _, oos_gross, _ = su.split_is_oos(df_gross)
    for label, fn in [("원본", lambda d: d),
                      ("캘린더일", su.decluster_calendar_day),
                      ("3일롤링", lambda d: su.decluster_rolling_days(d, 3)),
                      ("4일롤링", lambda d: su.decluster_rolling_days(d, 4)),
                      ("5일롤링", lambda d: su.decluster_rolling_days(d, 5))]:
        d = fn(oos_gross)
        print(su.fmt(su.summary(d, f"gross {label}")))

    print("\n=== LOO(종목 제외) — base OOS net ===")
    for excl in common.SYMBOLS:
        d = oos_base[oos_base["symbol"] != excl]
        print(su.fmt(su.summary(d, f"제외={excl}")))

    print("\n=== top-N 대칭 제거 — base OOS net ===")
    sorted_r = oos_base.sort_values("r")
    for n in [1, 3, 5, 10, 20]:
        worst_removed = sorted_r.iloc[n:]
        best_removed = sorted_r.iloc[:-n]
        print(su.fmt(su.summary(best_removed, f"최대이익top{n}제거")))
        print(su.fmt(su.summary(worst_removed, f"최대손실top{n}제거")))

    print("\n=== 셔플(부호 무작위화, 100회) — base OOS net ===")
    res = su.sign_shuffle_test(oos_base, n_shuffle=100)
    print(f"실제mean(R)={res['real_mean']:.4f} 셔플평균={res['shuffle_mean']:.4f} "
          f"백분위={res['pctile']:.1f}")

    print(f"\nTOTAL TIME {time.time()-t0:.1f}s")
