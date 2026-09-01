"""메인 백테스트: signal_source(resid/oi_zscore) x dir_mode(A/B) x fee_on(True/False).
결과를 pickle 로 캐시(scratchpad)해 이후 진단 스크립트들이 재사용."""
import itertools
import pickle
import sys
import time

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiresid")
import common
import engine
import stats_utils as su

t0 = time.time()
print("신호 구축 중...")
sigs = engine.load_all_signals()
print(f"신호 구축 완료 ({time.time()-t0:.1f}s) — 심볼: {list(sigs.keys())}")

with open(f"{common.SP}/sigs.pkl", "wb") as f:
    pickle.dump(sigs, f)

results = {}
for source, mode, fee_on in itertools.product(["resid", "oi_zscore"], ["A", "B"], [True, False]):
    cfg = engine.RunConfig(signal_source=source, dir_mode=mode, fee_on=fee_on)
    t1 = time.time()
    trades = engine.run_all(sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    key = (source, mode, fee_on)
    results[key] = df
    is_df, oos_df, full_df = su.split_is_oos(df)
    label = f"{source}/{mode}/{'net' if fee_on else 'gross'}"
    print(f"\n=== {label} ({time.time()-t1:.1f}s) ===")
    print(su.print_summary(su.summary(full_df, "FULL")))
    print(su.print_summary(su.summary(is_df, "IS")))
    print(su.print_summary(su.summary(oos_df, "OOS")))
    print(f"  IS+OOS n={len(is_df)+len(oos_df)} vs FULL n={len(full_df)}")
    # 종목별 OOS 트레이드 수
    print("  종목별 OOS n:", oos_df.groupby("symbol").size().to_dict())

with open(f"{common.SP}/results_main.pkl", "wb") as f:
    pickle.dump(results, f)
print("\n저장 완료: results_main.pkl")
