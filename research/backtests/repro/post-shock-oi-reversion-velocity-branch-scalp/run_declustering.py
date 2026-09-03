"""de-clustering: 캘린더일 단위 + 3~5일 롤링, net·gross 병행."""
from __future__ import annotations

import common as c
import engine
import stats_utils as su


def main():
    data = c.load_all()
    for fee_label, fee_on in [("net", True), ("gross", False)]:
        cfg = engine.Config(fee_on=fee_on)
        df, _ = engine.run(c.SYMBOLS, data, cfg)
        _, oos, _ = su.split_is_oos(df)
        print(f"\n=== {fee_label} ===")
        print(su.print_summary(su.summary(oos, f"{fee_label}-트레이드단위")))

        cal = su.decluster_calendar_day(oos)
        print(su.print_summary(su.summary(cal, f"{fee_label}-캘린더일")))

        for w in [3, 4, 5]:
            roll = su.decluster_rolling_days(oos, window_days=w)
            print(su.print_summary(su.summary(roll, f"{fee_label}-{w}일롤링")))


if __name__ == "__main__":
    main()
