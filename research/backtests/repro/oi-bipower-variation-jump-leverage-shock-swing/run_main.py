"""메인 백테스트: base(채택안) / price_swap(핵심 대조군) / reverse / no_invalidation / placebo.
결과를 pickle 로 캐시(scratchpad)해 이후 진단 스크립트들이 재사용."""
import pickle
import sys
import time

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oibv")
import common
import engine
import stats_utils as su

t0 = time.time()
print("신호 구축 중...")
sigs = engine.load_all_signals()
print(f"신호 구축 완료 ({time.time()-t0:.1f}s) — 심볼: {list(sigs.keys())}")
for sym, s in sigs.items():
    print(f"  {sym}: d1 {len(s.d1)} bars {s.d1.index.min()}~{s.d1.index.max()} | "
         f"oi_jr {len(s.oi_jr)}일 | px_jr {len(s.px_jr)}일")

with open(f"{common.SP}/sigs.pkl", "wb") as f:
    pickle.dump(sigs, f)

results = {}
for mode in ["base", "price_swap", "reverse", "no_invalidation", "placebo"]:
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

# gross(fee=0, slippage=0) — base 모드만
cfg_gross = engine.RunConfig(mode="base", fee_on=False)
trades_g = engine.run_all(sigs, cfg_gross)
all_g = [t for lst in trades_g.values() for t in lst]
df_g = su.trades_df(all_g)
results["base_gross"] = df_g
is_g, oos_g, full_g = su.split_is_oos(df_g)
print("\n=== mode=base_gross(fee=0,slip=0) ===")
print(su.print_summary(su.summary(full_g, "FULL")))
print(su.print_summary(su.summary(is_g, "IS")))
print(su.print_summary(su.summary(oos_g, "OOS")))

# 조용한 점프 서브셋(핵심 차별화 가설)
cfg_q = engine.RunConfig(mode="base")
trades_q = engine.run_all_quiet(sigs, cfg_q)
all_q = [t for lst in trades_q.values() for t in lst]
df_q = su.trades_df(all_q)
results["quiet_follow"] = df_q
is_q, oos_q, full_q = su.split_is_oos(df_q)
print("\n=== mode=quiet_follow(조용한 점프 후속 브레이크아웃 추종) ===")
print(su.print_summary(su.summary(full_q, "FULL")))
print(su.print_summary(su.summary(is_q, "IS")))
print(su.print_summary(su.summary(oos_q, "OOS")))

with open(f"{common.SP}/results_main.pkl", "wb") as f:
    pickle.dump(results, f)
print("\n저장 완료: results_main.pkl")
