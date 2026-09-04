"""메인 백테스트: 채택안(잔차 z-score, z_th=2.0) 6종목 IS/OOS 집계."""
from __future__ import annotations

import pandas as pd

import common
import engine
import stats_utils as su


def main():
    bundles = engine.load_all_bundles()
    print("로드된 종목:", list(bundles.keys()))
    cfg = engine.RunConfig()
    trades = engine.run_all(bundles, cfg)

    all_rows = []
    print("\n=== 종목별 (IS / OOS / FULL) ===")
    for sym in common.ALT_SYMBOLS:
        df = su.trades_df(trades.get(sym, []))
        all_rows.append(df)
        is_df, oos_df, full_df = su.split_is_oos(df)
        print(f"-- {sym} --")
        print(" ", su.print_summary(su.summary(is_df, "IS")))
        print(" ", su.print_summary(su.summary(oos_df, "OOS")))
        print(" ", su.print_summary(su.summary(full_df, "FULL")))

    pooled = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    is_p, oos_p, full_p = su.split_is_oos(pooled)
    print("\n=== 풀링(6종목 합산) ===")
    print(" ", su.print_summary(su.summary(is_p, "IS(pooled)")))
    print(" ", su.print_summary(su.summary(oos_p, "OOS(pooled)")))
    print(" ", su.print_summary(su.summary(full_p, "FULL(pooled)")))
    print(f"\nIS+OOS = {len(is_p)+len(oos_p)}  FULL(직접필터) = {len(full_p)}  "
         f"(IS_START~OOS_END 범위 내 전체 대비 검산)")

    # 청산사유 분포
    print("\n=== 청산사유 분포(풀링, FULL) ===")
    print(full_p["reason"].value_counts())

    # 방향별
    print("\n=== 방향별(풀링, OOS) ===")
    for d in ["long", "short"]:
        sub = oos_p[oos_p["direction"] == d]
        print(" ", su.print_summary(su.summary(sub, f"OOS {d}")))

    pooled.to_pickle(common.SP / "trades_base.pkl")
    print("\n저장: ", common.SP / "trades_base.pkl")


if __name__ == "__main__":
    main()
