"""de-clustering: 캘린더일 단위 및 3~5일 롤링 윈도우, R-배수 기준. gross 도 병행(gross t 인용 대비)."""
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
    for fee_on in [True, False]:
        tag = "net" if fee_on else "gross"
        cfg = engine.RunConfig(mode="gated", short_mode=short_mode, fee_on=fee_on)
        trades = engine.run_all(sigs, cfg)
        df = su.trades_df([t for lst in trades.values() for t in lst])
        is_df, oos_df, full_df = su.split_is_oos(df)
        print(f"--- [{tag}] 트레이드 단위 ---")
        print(" ", su.print_summary(su.summary(oos_df, "OOS(트레이드단위)")))

        for name, decl_fn in [("캘린더일", su.decluster_calendar_day),
                              ("3일롤링", lambda d: su.decluster_rolling_days(d, 3)),
                              ("5일롤링", lambda d: su.decluster_rolling_days(d, 5))]:
            d_oos = decl_fn(oos_df)
            t, p, n = su.t_stat(d_oos)
            pf = su.pf_r(d_oos)
            print(f"  [{tag}][{name}] OOS 고유표본 n={n} PF(R)={pf:.3f} t={t:+.3f} p={p:.4f}")

        # 전체(IS+OOS) 기준 고유표본(사전폐기조건 (b) 판정용)
        d_full_cal = su.decluster_calendar_day(full_df)
        d_full_5d = su.decluster_rolling_days(full_df, 5)
        print(f"  [{tag}] FULL 캘린더일 고유표본 n={len(d_full_cal)}, 5일롤링 고유표본 n={len(d_full_5d)}")
