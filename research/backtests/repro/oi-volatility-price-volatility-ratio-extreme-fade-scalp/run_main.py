"""메인 백테스트: dir_mode(A/B) x fee_on(True/False). 결과를 pickle 로 캐시."""
import itertools
import pickle
import sys
import time

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oivolratio")
import common
import engine
import stats_utils as su

t0 = time.time()
with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)
print(f"신호 로드 완료 ({time.time()-t0:.1f}s) — 심볼: {list(sigs.keys())}")

results = {}
for mode, fee_on in itertools.product(["A", "B"], [True, False]):
    cfg = engine.RunConfig(dir_mode=mode, fee_on=fee_on)
    t1 = time.time()
    trades = engine.run_all(sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    key = (mode, fee_on)
    results[key] = df
    is_df, oos_df, full_df = su.split_is_oos(df)
    label = f"{mode}/{'net' if fee_on else 'gross'}"
    print(f"\n=== {label} ({time.time()-t1:.1f}s) ===")
    print(su.print_summary(su.summary(full_df, "FULL")))
    print(su.print_summary(su.summary(is_df, "IS")))
    print(su.print_summary(su.summary(oos_df, "OOS")))
    print(f"  IS+OOS n={len(is_df)+len(oos_df)} vs FULL n={len(full_df)}")
    print("  종목별 OOS n:", oos_df.groupby("symbol").size().to_dict())
    print("  reason 분포(전체):", df["reason"].value_counts().to_dict())
    zero_hold = (df["holding_bars"] == 0).mean() * 100 if len(df) else float("nan")
    print(f"  zero_hold_frac={zero_hold:.2f}%")

with open(f"{common.SP}/results_main.pkl", "wb") as f:
    pickle.dump(results, f)
print("\n저장 완료: results_main.pkl")
