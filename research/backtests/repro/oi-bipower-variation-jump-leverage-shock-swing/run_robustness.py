"""LOO(종목별 제외) / top-N 제거 / 파라미터 스윕(R-배수 기준)."""
import pickle
import sys

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oibv")
import common
import engine
import stats_utils as su

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)
with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

print("=" * 70)
print("① LOO(종목 하나씩 제외) — OOS base")
print("=" * 70)
df = results["base"]
_is, oos, _full = su.split_is_oos(df)
print(su.print_summary(su.summary(oos, "OOS(전체7종목)")))
for sym in common.SYMBOLS:
    sub = oos[oos["symbol"] != sym]
    print(su.print_summary(su.summary(sub, f"OOS(-{sym})")))

print("\n=== 종목별 단독 성과 ===")
for sym in common.SYMBOLS:
    sub = oos[oos["symbol"] == sym]
    print(su.print_summary(su.summary(sub, sym)))

print("\n" + "=" * 70)
print("② top-N 제거(승리 트레이드 상위 N건 제외)")
print("=" * 70)
oos_sorted = oos.sort_values("r", ascending=False)
for k in [1, 3, 5, 10]:
    sub = oos_sorted.iloc[k:]
    print(su.print_summary(su.summary(sub, f"top-{k}제거")))

print("\n" + "=" * 70)
print("③ 파라미터 스윕(IS+OOS 별도 표기)")
print("=" * 70)
sweep_specs = []
for pw in [60, 90, 120, 180]:
    sweep_specs.append(dict(pctile_window=pw))
for jp in [85, 90, 92.5, 95]:
    sweep_specs.append(dict(jump_pctile=jp))
for pc in [1.0, 1.5, 2.0, 2.5]:
    sweep_specs.append(dict(price_confirm_th=pc))
for asm in [1.2, 1.5, 1.8, 2.0]:
    sweep_specs.append(dict(atr_stop_mult=asm))
for rr in [1.5, 2.0, 2.5, 3.0]:
    sweep_specs.append(dict(rr_target=rr))
for mh in [2, 3, 4, 5]:
    sweep_specs.append(dict(max_hold_days=mh))

sweep_results = []
for spec in sweep_specs:
    cfg = engine.RunConfig(mode="base", **spec)
    trades = engine.run_all(sigs, cfg)
    all_t = [t for lst in trades.values() for t in lst]
    tdf = su.trades_df(all_t)
    is_df, oos_df, _full = su.split_is_oos(tdf)
    is_s = su.summary(is_df, "IS")
    oos_s = su.summary(oos_df, "OOS")
    sweep_results.append((spec, is_s, oos_s))
    print(f"{str(spec):40s} IS  n={is_s['n']:4d} PF={is_s['pf_r']:.3f} t={is_s['t']:+.2f} | "
         f"OOS n={oos_s['n']:4d} PF={oos_s['pf_r']:.3f} t={oos_s['t']:+.2f}")

n_pass = sum(1 for spec, is_s, oos_s in sweep_results
             if oos_s["pf_r"] >= 1.3 and oos_s["n"] >= 20 and abs(oos_s.get("t") or 0) >= 1.96)
print(f"\n스윕 {len(sweep_results)}변형 중 통과선(OOS PF>=1.3, n>=20, |t|>=1.96) 충족: {n_pass}건")

with open(f"{common.SP}/robustness.pkl", "wb") as f:
    pickle.dump(dict(sweep_results=sweep_results), f)
print("\n저장 완료: robustness.pkl")
