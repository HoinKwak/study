"""LOO(leave-one-symbol-out) + top-N 제거 — base(zcr_lo) OOS net."""
import pickle

import common
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

df = results[("zcr_lo", True)]
_, oos_df, _ = su.split_is_oos(df)

print("=== 종목별 OOS(net) ===")
for sym, g in oos_df.groupby("symbol"):
    print(su.print_summary(su.summary(g, sym)))

print("\n=== LOO(종목 하나씩 제외) ===")
for sym in common.SYMBOLS:
    g = oos_df[oos_df["symbol"] != sym]
    print(su.print_summary(su.summary(g, f"exclude {sym}")))

print("\n=== top-N 승리트레이드 제거 ===")
sorted_r = oos_df.sort_values("r", ascending=False)
for n in (1, 3, 5, 10, 20, 50):
    g = sorted_r.iloc[n:]
    print(su.print_summary(su.summary(g, f"top-{n} 제거")))
