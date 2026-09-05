"""de-clustering(캘린더일·3~5일 롤링) — net·gross 둘 다 병행."""
import pickle

import common
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

for gate in ["zcr_lo"]:
    for fee_on in [True, False]:
        df = results[(gate, fee_on)]
        _, oos_df, _ = su.split_is_oos(df)
        label = f"{gate}/{'net' if fee_on else 'gross'}"
        print(f"\n=== {label} OOS de-clustering ===")
        print(" 원본(트레이드 단위):", su.print_summary(su.summary(oos_df, "raw")))
        cal = su.decluster_calendar_day(oos_df)
        print(" 캘린더일:          ", su.print_summary(su.summary(cal, "cal_day")))
        for w in (3, 4, 5):
            roll = su.decluster_rolling_days(oos_df, window_days=w)
            print(f" {w}일 롤링:          ", su.print_summary(su.summary(roll, f"roll{w}d")))
