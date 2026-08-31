"""de-clustering: 캘린더일 단위 + 3~5일 롤링 윈도우. base(net) 와 base_gross 모두 R-배수로."""
import pickle
import sys

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oibv")
import common
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

for label, key in [("base(net)", "base"), ("base(gross)", "base_gross")]:
    df = results[key]
    _is, oos, full = su.split_is_oos(df)
    print(f"\n=== {label} ===")
    print("원본:      ", su.print_summary(su.summary(oos, "OOS")))
    cal = su.decluster_calendar_day(oos)
    print("캘린더일:  ", su.print_summary(su.summary(cal, "OOS-cal")))
    for w in [3, 4, 5]:
        roll = su.decluster_rolling_days(oos, window_days=w)
        print(f"{w}일롤링:   ", su.print_summary(su.summary(roll, f"OOS-roll{w}")))

print("\n=== 대칭점검: 최대 손실 클러스터 제거 후 잔여 ===")
df = results["base"]
_is, oos, full = su.split_is_oos(df)
roll = su.decluster_rolling_days(oos, window_days=5)
roll_sorted = roll.sort_values("r")
for k in [1, 3]:
    remain = roll_sorted.iloc[k:]
    print(f"최악 {k}클러스터 제외: ", su.print_summary(su.summary(remain, f"remove_worst_{k}")))
