"""메인 백테스트: gate(zcr_lo/none/zcr_hi/volz_hi/reverse) x fee_on(True/False). 결과 pickle 캐시."""
import pickle
import time

import common
import engine
import stats_utils as su

t0 = time.time()
with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)
print(f"신호 로드 완료 ({time.time()-t0:.1f}s) — 심볼: {list(sigs.keys())}")

results = {}
for gate in ["zcr_lo", "none", "zcr_hi", "volz_hi", "reverse"]:
    for fee_on in [True, False]:
        cfg = engine.RunConfig(gate=gate, fee_on=fee_on)
        t1 = time.time()
        trades = engine.run_all(sigs, cfg)
        all_trades = [t for lst in trades.values() for t in lst]
        df = su.trades_df(all_trades)
        key = (gate, fee_on)
        results[key] = df
        is_df, oos_df, full_df = su.split_is_oos(df)
        label = f"{gate}/{'net' if fee_on else 'gross'}"
        print(f"\n=== {label} ({time.time()-t1:.1f}s) ===")
        print(su.print_summary(su.summary(full_df, "FULL")))
        print(su.print_summary(su.summary(is_df, "IS")))
        print(su.print_summary(su.summary(oos_df, "OOS")))
        print(f"  IS+OOS n={len(is_df)+len(oos_df)} vs FULL n={len(full_df)}")
        if len(oos_df):
            print("  종목별 OOS n:", oos_df.groupby("symbol").size().to_dict())
            print("  reason 분포(OOS):", oos_df["reason"].value_counts().to_dict())
            zero_hold = (oos_df["holding_bars"] == 0).mean() * 100
            print(f"  zero_hold_frac(OOS)={zero_hold:.2f}%  mean_hold(OOS)={oos_df['holding_bars'].mean():.2f}봉")

with open(f"{common.SP}/results_main.pkl", "wb") as f:
    pickle.dump(results, f)
print("\n저장 완료: results_main.pkl")
