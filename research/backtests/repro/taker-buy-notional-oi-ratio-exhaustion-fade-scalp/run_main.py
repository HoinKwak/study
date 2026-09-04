"""메인 백테스트 — 정방향(스펙 기본, mode=oi_buy_sell) x reverse(False/True) x fee_on(True/False)
→ results_main.pkl 저장 + IS/OOS 요약 출력."""
import pickle

import common
import engine
import stats_utils as su

with open(common.SP / "sigs_200.pkl", "rb") as f:
    sigs = pickle.load(f)

results = {}
for reverse in (False, True):
    for fee_on in (True, False):
        cfg = engine.RunConfig(mode="oi_buy_sell", reverse=reverse, fee_on=fee_on)
        trades = engine.run_all(sigs, cfg)
        all_trades = [t for lst in trades.values() for t in lst]
        df = su.trades_df(all_trades)
        results[(reverse, fee_on)] = df
        is_df, oos_df, full_df = su.split_is_oos(df)
        print(f"reverse={reverse!s:5s} fee_on={fee_on!s:5s}")
        print("  " + su.print_summary(su.summary(is_df, "IS")))
        print("  " + su.print_summary(su.summary(oos_df, "OOS")))
        print("  " + su.print_summary(su.summary(full_df, "FULL")))

with open(common.SP / "results_main.pkl", "wb") as f:
    pickle.dump(results, f)
print("\n저장: results_main.pkl")
