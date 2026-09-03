"""반전 대조군: 최종방향 뒤집기(SL/TP 원신호 기준 1회 계산 후 대칭 재배치, 청산조건도 최종방향
참조). net + gross 비교, 청산사유/보유기간 분포 비교(zero_hold_frac 대신)."""
from __future__ import annotations

import common as c
import engine
import stats_utils as su


def main():
    data = c.load_all()

    for fee_label, fee_on in [("net", True), ("gross", False)]:
        cfg_fwd = engine.Config(fee_on=fee_on, reverse=False)
        cfg_rev = engine.Config(fee_on=fee_on, reverse=True)
        df_fwd, _ = engine.run(c.SYMBOLS, data, cfg_fwd)
        df_rev, _ = engine.run(c.SYMBOLS, data, cfg_rev)
        _, oos_fwd, _ = su.split_is_oos(df_fwd)
        _, oos_rev, _ = su.split_is_oos(df_rev)
        print(f"\n=== {fee_label} OOS 정방향 vs 반전 ===")
        print(su.print_summary(su.summary(oos_fwd, f"{fee_label}-fwd")))
        print(su.print_summary(su.summary(oos_rev, f"{fee_label}-rev")))

        if fee_label == "net":
            print("\n청산사유 분포(정방향, OOS):")
            print(oos_fwd["reason"].value_counts(normalize=True).round(4) * 100)
            print("\n청산사유 분포(반전, OOS):")
            print(oos_rev["reason"].value_counts(normalize=True).round(4) * 100)
            print(f"\n평균 보유봉수: 정방향={oos_fwd['holding_bars'].mean():.2f} "
                 f"반전={oos_rev['holding_bars'].mean():.2f}")
            print(f"1봉 내 청산 비율: 정방향={100*(oos_fwd['holding_bars']<=0).mean():.1f}% "
                 f"반전={100*(oos_rev['holding_bars']<=0).mean():.1f}%")


if __name__ == "__main__":
    main()
