"""LOO(7종목 leave-one-out) + top-N 트레이드 제거(최고/최악 대칭 점검), R-배수 기준."""
import pickle
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

for short_mode in ["streak_down", "streak_up_alt"]:
    print(f"\n############ short_mode={short_mode} ############")
    cfg = engine.RunConfig(mode="gated", short_mode=short_mode)
    trades_full = engine.run_all(sigs, cfg)
    df_full = su.trades_df([t for lst in trades_full.values() for t in lst])
    _, oos_full, _ = su.split_is_oos(df_full)
    print(f"전체 OOS n={len(oos_full)} PF(R)={su.pf_r(oos_full):.3f} "
         f"t={su.t_stat(oos_full)[0]:+.3f}")

    print("--- LOO(종목 제외) ---")
    for excl in common.SYMBOLS:
        sub_sigs = {k: v for k, v in sigs.items() if k != excl}
        trades = engine.run_all(sub_sigs, cfg)
        df = su.trades_df([t for lst in trades.values() for t in lst])
        _, oos, _ = su.split_is_oos(df)
        t, p, n = su.t_stat(oos)
        print(f"  {excl} 제외: OOS n={n} PF(R)={su.pf_r(oos):.3f} t={t:+.3f} mean(R)={oos['r'].mean() if n else float('nan'):+.4f}")

    print("--- top-N 제거(최고 승리 트레이드) ---")
    sorted_r = oos_full.sort_values("r", ascending=False)
    for topn in [1, 2, 3, 5]:
        if len(sorted_r) <= topn:
            continue
        rest = sorted_r.iloc[topn:]
        print(f"  top-{topn} 제거: n={len(rest)} PF(R)={su.pf_r(rest):.3f} mean(R)={rest['r'].mean():+.4f} "
             f"sum(R)={rest['r'].sum():+.2f} (원 sum(R)={oos_full['r'].sum():+.2f})")

    print("--- bottom-N 제거(최악 손실 트레이드, 대칭점검) ---")
    sorted_r_asc = oos_full.sort_values("r", ascending=True)
    for botn in [1, 2, 3, 5]:
        if len(sorted_r_asc) <= botn:
            continue
        rest = sorted_r_asc.iloc[botn:]
        print(f"  bottom-{botn} 제거: n={len(rest)} PF(R)={su.pf_r(rest):.3f} mean(R)={rest['r'].mean():+.4f} "
             f"sum(R)={rest['r'].sum():+.2f}")
