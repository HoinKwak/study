"""메인 실행: IS/OOS/FULL, net/gross, 분기별(reversion/persistence) 요약."""
from __future__ import annotations

import sys

import pandas as pd

import common as c
import engine
import stats_utils as su


def main():
    data = c.load_all()
    print("로드된 종목:", list(data.keys()))
    for sym, sd in data.items():
        print(f"  {sym}: h1={len(sd.h1)} m15={len(sd.m15)} oi1h_nan%={sd.oi1h.isna().mean()*100:.2f}")

    cfg = engine.Config()
    df, events = engine.run(c.SYMBOLS, data, cfg)
    print(f"\n총 트레이드 수: {len(df)}")
    print("이벤트 수(종목별, 방향조건 충족분만):", {k: len(v) for k, v in events.items()})

    # 룩어헤드 확정 시각 검증
    bad = df[df["entry_time"] < df["confirm_time"]]
    print("진입시각 < 확정시각 위반건수:", len(bad))

    is_df, oos_df, full_df = su.split_is_oos(df)
    print(f"\nIS+OOS==FULL 검증: IS={len(is_df)} OOS={len(oos_df)} FULL={len(full_df)} "
         f"IS+OOS={len(is_df)+len(oos_df)} (일치={len(is_df)+len(oos_df)==len(full_df)})")

    print("\n=== net (수수료+슬리피지 반영) ===")
    for label, d in [("IS", is_df), ("OOS", oos_df), ("FULL", full_df)]:
        print(su.print_summary(su.summary(d, label)))

    print("\n분기별(branch) 요약 — OOS ===")
    for br in ["reversion", "persistence"]:
        d = oos_df[oos_df["branch"] == br]
        print(su.print_summary(su.summary(d, f"OOS-{br}")))
    print("\n분기별(branch) 요약 — IS ===")
    for br in ["reversion", "persistence"]:
        d = is_df[is_df["branch"] == br]
        print(su.print_summary(su.summary(d, f"IS-{br}")))

    print("\n방향(orig_direction) 별 — OOS ===")
    for dr in ["long", "short"]:
        d = oos_df[oos_df["orig_direction"] == dr]
        print(su.print_summary(su.summary(d, f"OOS-{dr}")))

    print("\n청산사유 분포(OOS):")
    print(oos_df["reason"].value_counts())
    print("\n평균 보유봉수(OOS):", oos_df["holding_bars"].mean())

    df.to_parquet(str(c.SP / "trades_net.parquet"))
    print("\n저장:", c.SP / "trades_net.parquet")

    # gross(무비용) 진단
    cfg_gross = engine.Config(fee_on=False)
    dfg, _ = engine.run(c.SYMBOLS, data, cfg_gross)
    is_g, oos_g, full_g = su.split_is_oos(dfg)
    print("\n=== gross (fee=0, slippage=0) 무비용 진단 ===")
    for label, d in [("IS", is_g), ("OOS", oos_g), ("FULL", full_g)]:
        print(su.print_summary(su.summary(d, f"gross-{label}")))
    dfg.to_parquet(str(c.SP / "trades_gross.parquet"))


if __name__ == "__main__":
    main()
