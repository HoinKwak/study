"""메인 백테스트: gated(채택안) / ungated(게이트없음 대조군) / reverse(방향반전 대조군).
결과를 pickle 로 캐시(scratchpad)해 이후 진단 스크립트들이 재사용."""
import pickle
import sys
import time

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su

t0 = time.time()
print("신호 구축 중...")
sigs = engine.load_all_signals()
print(f"신호 구축 완료 ({time.time()-t0:.1f}s) — 심볼: {list(sigs.keys())}")
for sym, s in sigs.items():
    print(f"  {sym}: {len(s.df)} bars, {s.df.index.min()} ~ {s.df.index.max()}")

with open(f"{common.SP}/sigs.pkl", "wb") as f:
    pickle.dump(sigs, f)

results = {}
for mode in ["gated", "ungated", "reverse"]:
    cfg = engine.RunConfig(mode=mode)
    t1 = time.time()
    trades = engine.run_all(sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    results[mode] = df
    is_df, oos_df, full_df = su.split_is_oos(df)
    print(f"\n=== mode={mode} ({time.time()-t1:.1f}s) ===")
    print(su.print_summary(su.summary(full_df, "FULL")))
    print(su.print_summary(su.summary(is_df, "IS")))
    print(su.print_summary(su.summary(oos_df, "OOS")))
    print(f"  IS+OOS n={len(is_df)+len(oos_df)} vs FULL n={len(full_df)}")
    if mode == "gated":
        print("  종목별 OOS n:")
        for sym in common.SYMBOLS:
            sub = oos_df[oos_df.symbol == sym]
            print(f"    {sym}: n={len(sub)} PF(R)={su.pf_r(sub):.3f}")
    if mode == "reverse":
        print("  reason 분포:", df["reason"].value_counts().to_dict())
        print(f"  zero_hold_frac = {(df['holding_bars']==0).mean()*100:.2f}%")
        print("  holding_bars 분포(describe):")
        print(df["holding_bars"].describe())

with open(f"{common.SP}/results_main.pkl", "wb") as f:
    pickle.dump(results, f)
print("\n저장 완료: results_main.pkl")
