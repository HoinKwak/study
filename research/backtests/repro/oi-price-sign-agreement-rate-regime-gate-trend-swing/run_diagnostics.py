"""부호일치율(Co-Sign Agreement Rate) 게이트 + BTC EMA20/50 추세추종 — 전체 진단 실행."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sstats

import common
import engine
import stats_utils as su

pd.set_option("display.width", 160)


def run_gate(sig, gate: str, fee_on: bool = True, hi_th: float = common.HI_TH,
             atr_stop_mult: float = common.ATR_STOP_MULT):
    cfg = engine.RunConfig(gate=gate, fee_on=fee_on, hi_th=hi_th, atr_stop_mult=atr_stop_mult)
    trades = engine.run_config(sig, cfg)
    return su.trades_df(trades)


def report_block(df: pd.DataFrame, label: str):
    is_df, oos_df, full_df = su.split_is_oos(df)
    for sub, name in [(is_df, "IS"), (oos_df, "OOS"), (full_df, "FULL")]:
        print(su.print_summary(su.summary(sub, f"{label} {name}")))
    return is_df, oos_df, full_df


def main():
    print("=" * 100)
    print("0. 데이터 정합성")
    sig = common.build_signals()
    print(f"df4h range: {sig.df4h.index.min()} ~ {sig.df4h.index.max()}  n={len(sig.df4h)}")
    print(f"IS_START={common.IS_START} IS_END={common.IS_END} "
         f"OOS_START={common.OOS_START} OOS_END={common.OOS_END}")

    print("=" * 100)
    print("1. 기본안(base 게이트) — net vs gross")
    net_df = run_gate(sig, "base", fee_on=True)
    is_n, oos_n, full_n = report_block(net_df, "base net")
    gross_df = run_gate(sig, "base", fee_on=False)
    is_g, oos_g, full_g = report_block(gross_df, "base gross")

    print(f"IS+OOS==FULL(net) 확인: {len(is_n)}+{len(oos_n)}={len(is_n)+len(oos_n)} vs FULL={len(full_n)}")

    print("=" * 100)
    print("2. 대조군(net)")
    ctrl_dfs = {}
    for gate in ["none", "lowagree", "corr", "swap", "reverse"]:
        df = run_gate(sig, gate, fee_on=True)
        ctrl_dfs[gate] = df
        report_block(df, gate)

    print("2b. 대조군(gross)")
    ctrl_dfs_gross = {}
    for gate in ["none", "lowagree", "corr", "swap", "reverse"]:
        df = run_gate(sig, gate, fee_on=False)
        ctrl_dfs_gross[gate] = df
        report_block(df, f"{gate} gross")

    print("=" * 100)
    print("3. 표본수 맞춘 부트스트랩(OOS, base vs 각 대조군) — base_mean 이 pool 분포에서 몇 백분위인가")
    base_oos = oos_n["r"].to_numpy()
    for gate, df in ctrl_dfs.items():
        _, oos_c, _ = su.split_is_oos(df)
        pool_r = oos_c["r"].dropna().to_numpy()
        res = su.bootstrap_matched_n_diff(pool_r, base_oos)
        print(f"base vs {gate:10s}: base_mean(R)={res['base_mean']:+.4f} "
             f"pool_boot_mean={res['pool_dist_mean']:+.4f} base가 pool분포에서 {res['pctile']:.1f}백분위 "
             f"(n_base={res['n']}, n_pool={len(pool_r)})")

    print("=" * 100)
    print("4. base ⊆ pool 부분집합 관계(none 게이트 대비)")
    base_times = set(oos_n["entry_time"])
    _, oos_none, _ = su.split_is_oos(ctrl_dfs["none"])
    none_times = set(oos_none["entry_time"])
    overlap = base_times & none_times
    print(f"base OOS n={len(base_times)}, none OOS n={len(none_times)}, "
         f"overlap={len(overlap)} ({len(overlap)/len(base_times)*100:.1f}% of base)")
    ind = su.independent_pair_diff(oos_n, oos_none)
    print(f"독립 Welch(중복 제외 잔여표본): base_only n={ind['a_only_n']} none_only n={ind['b_only_n']} "
         f"t={ind['welch_t']:+.3f} p={ind['welch_p']:.4f}")

    print("=" * 100)
    print("5. de-clustering(OOS, net) — 캘린더일 / 3~5일 롤링")
    cal = su.decluster_calendar_day(oos_n)
    t_cal, p_cal = (sstats.ttest_1samp(cal["r"], 0.0) if len(cal) >= 2 else (float("nan"), float("nan")))
    print(f"캘린더일: n_unique_days={len(cal)} mean(R)={cal['r'].mean():+.4f} t={t_cal:+.3f} p={p_cal:.4f}")
    for w in [3, 4, 5]:
        roll = su.decluster_rolling_days(oos_n, window_days=w)
        t_r, p_r = (sstats.ttest_1samp(roll["r"], 0.0) if len(roll) >= 2 else (float("nan"), float("nan")))
        print(f"{w}일 롤링 클러스터: n_cluster={len(roll)} mean(R)={roll['r'].mean():+.4f} "
             f"t={t_r:+.3f} p={p_r:.4f}")

    print("5b. de-clustering(OOS, gross) — 동일 처리(폐기조건 gross 인용 시 병행 규칙)")
    cal_g = su.decluster_calendar_day(oos_g)
    t_calg, p_calg = (sstats.ttest_1samp(cal_g["r"], 0.0) if len(cal_g) >= 2 else (float("nan"), float("nan")))
    print(f"gross 캘린더일: n={len(cal_g)} mean(R)={cal_g['r'].mean():+.4f} t={t_calg:+.3f} p={p_calg:.4f}")
    for w in [3, 5]:
        roll_g = su.decluster_rolling_days(oos_g, window_days=w)
        t_rg, p_rg = (sstats.ttest_1samp(roll_g["r"], 0.0) if len(roll_g) >= 2 else (float("nan"), float("nan")))
        print(f"gross {w}일 롤링: n={len(roll_g)} mean(R)={roll_g['r'].mean():+.4f} t={t_rg:+.3f} p={p_rg:.4f}")

    print("=" * 100)
    print("6. 매크로 클러스터 분해(OOS, net) — 5일 롤링 클러스터별 순 R 기여도")
    roll5 = su.decluster_rolling_days(oos_n, window_days=5)
    total_r = oos_n["r"].sum()
    roll5_sorted = roll5.assign(sum_r=lambda d: d["r"] * d["n"]).sort_values("sum_r", ascending=False)
    print(f"OOS 순 R 합계={total_r:+.3f}, 클러스터 수={len(roll5)}")
    print(roll5_sorted[["entry_time", "n", "r", "sum_r"]].head(6).to_string(index=False))
    top3_sum = roll5_sorted["sum_r"].head(3).sum()
    print(f"상위 3개 클러스터 기여도: {top3_sum:+.3f} ({top3_sum/total_r*100:.1f}% of OOS 순R)" if total_r != 0 else "")
    # top-3 클러스터에 속한 트레이드 제외 후 재계산(클러스터 경계로 직접 매칭)
    d_sorted = oos_n.sort_values("entry_time").reset_index(drop=True)
    cluster_id = []
    cur_id = 0; last_time = None
    for tm in d_sorted["entry_time"]:
        if last_time is None or (tm - last_time) > pd.Timedelta(days=5):
            cur_id += 1
        cluster_id.append(cur_id)
        last_time = tm
    d_sorted["cluster5"] = cluster_id
    cluster_sum = d_sorted.groupby("cluster5")["r"].sum().sort_values(ascending=False)
    top3_clusters = cluster_sum.head(3).index
    remain = d_sorted[~d_sorted["cluster5"].isin(top3_clusters)]
    t_rem, p_rem = (sstats.ttest_1samp(remain["r"], 0.0) if len(remain) >= 2 else (float("nan"), float("nan")))
    print(f"top-3 클러스터 제외: 잔여 n={len(remain)} PF(R)={su.pf_r(remain):.3f} "
         f"mean(R)={remain['r'].mean():+.4f} t={t_rem:+.3f}")
    print("손실 클러스터 대칭점검(최악 클러스터 제외)")
    worst_clusters = cluster_sum.tail(3).index
    remain_w = d_sorted[~d_sorted["cluster5"].isin(worst_clusters)]
    t_w, p_w = (sstats.ttest_1samp(remain_w["r"], 0.0) if len(remain_w) >= 2 else (float("nan"), float("nan")))
    print(f"최악 3개 클러스터 제외: 잔여 n={len(remain_w)} PF(R)={su.pf_r(remain_w):.3f} "
         f"mean(R)={remain_w['r'].mean():+.4f} t={t_w:+.3f}")

    print("=" * 100)
    print("7. top-N 개별 트레이드 제거 민감도(OOS, net)")
    for topn in [1, 2, 3]:
        d = oos_n.sort_values("r", ascending=False).iloc[topn:]
        print(f"top-{topn} 제거: n={len(d)} PF(R)={su.pf_r(d):.3f} sum(R)={d['r'].sum():+.3f}")

    print("=" * 100)
    print("8. 동어반복 점검 — agree(t) vs 피어슨상관(같은 20봉창) 상관, ATR%·거래량z 상관")
    valid_all = sig.agree.notna() & sig.corr_roll.notna()
    r_full = sig.agree[valid_all].corr(sig.corr_roll[valid_all])
    print(f"agree vs corr_roll 전체구간 상관: r={r_full:.4f} (n={valid_all.sum()})")
    # 트리거 시점: signal_idx(크로스확정봉, entry_idx-1)의 agree/corr_roll
    trig_idx = net_df["entry_idx"].to_numpy() - 1
    trig_idx = trig_idx[(trig_idx >= 0) & (trig_idx < len(sig.agree))]
    ag_trig = sig.agree.iloc[trig_idx]
    cr_trig = sig.corr_roll.iloc[trig_idx]
    m = ag_trig.notna() & cr_trig.notna()
    r_trig = ag_trig[m].corr(cr_trig[m]) if m.sum() >= 2 else float("nan")
    print(f"agree vs corr_roll 트리거시점(base 진입신호) 상관: r={r_trig:.4f} (n={m.sum()})")

    valid_atr = sig.agree.notna() & sig.atr_pct.notna()
    r_atr = sig.agree[valid_atr].corr(sig.atr_pct[valid_atr])
    valid_vz = sig.agree.notna() & sig.vol_z.notna()
    r_volz = sig.agree[valid_vz].corr(sig.vol_z[valid_vz])
    print(f"agree vs ATR%: r={r_atr:.4f} (n={valid_atr.sum()})   agree vs 거래량z: r={r_volz:.4f} (n={valid_vz.sum()})")

    print("=" * 100)
    print("9. 사전 폐기조건 (b) 판정: |r(agree, corr_roll)| > 0.85 ?")
    print(f"전체구간 |r|={abs(r_full):.4f}   트리거시점 |r|={abs(r_trig):.4f}  "
         f"→ {'폐기(재포장)' if abs(r_full) > 0.85 or abs(r_trig) > 0.85 else '통과(별개 정보)'}")

    print("=" * 100)
    print("10. 반전 대조군 — 청산사유·보유기간 분포")
    rev_df = ctrl_dfs["reverse"]
    print(rev_df["reason"].value_counts())
    print(f"reverse 평균 보유봉수={rev_df['holding_bars'].mean():.2f}  base 평균 보유봉수={net_df['holding_bars'].mean():.2f}")
    print(f"reverse 1봉내 청산비율={(rev_df['holding_bars']<=1).mean()*100:.1f}%  "
         f"base 1봉내 청산비율={(net_df['holding_bars']<=1).mean()*100:.1f}%")

    print("=" * 100)
    print("11. 파라미터 스윕(IS/OOS PF(R), t) — agree_window/norm_days/hi_th/ema/atr_stop_mult")
    variants = [
        ("baseline", dict()),
        ("agree_window=12", dict(agree_window=12)),
        ("agree_window=30", dict(agree_window=30)),
        ("agree_window=40", dict(agree_window=40)),
        ("norm_days=180", dict(norm_days=180)),
        ("norm_days=540", dict(norm_days=540)),
        ("norm_days=730", dict(norm_days=730)),
        ("hi_th=60", dict(hi_th=60)),
        ("hi_th=80", dict(hi_th=80)),
        ("hi_th=85", dict(hi_th=85)),
        ("ema=10/40", dict(ema_fast_n=10, ema_slow_n=40)),
        ("ema=30/100", dict(ema_fast_n=30, ema_slow_n=100)),
        ("atr_stop=1.5", dict(atr_stop_mult=1.5)),
        ("atr_stop=3.5", dict(atr_stop_mult=3.5)),
    ]
    for name, kw in variants:
        sig_v = common.build_signals(**kw)
        hi_th_v = kw.get("hi_th", common.HI_TH)
        atr_v = kw.get("atr_stop_mult", common.ATR_STOP_MULT)
        df_v = run_gate(sig_v, "base", fee_on=True, hi_th=hi_th_v, atr_stop_mult=atr_v)
        is_v, oos_v, full_v = su.split_is_oos(df_v)
        t_is, _, n_is = su.t_stat(is_v)
        t_oos, _, n_oos = su.t_stat(oos_v)
        print(f"{name:16s} IS n={n_is:4d} PF={su.pf_r(is_v):.3f} t={t_is:+.2f} | "
             f"OOS n={n_oos:4d} PF={su.pf_r(oos_v):.3f} t={t_oos:+.2f}")

    print("=" * 100)
    print("12. 룩어헤드 절단검증(BTC 자기 시계열, 3개 절단시점) — 절단 전후 신호 완전일치 확인")
    from lookahead_check import run_lookahead_check
    run_lookahead_check()

    print("=" * 100)
    print("13. 설계판단 대안 실행 — (A) 1d EMA20/50 확인 매핑판 (B) zero-diff 처리 대안")
    from alt_designs import run_alt_1d_ema, run_alt_zero_diff
    run_alt_1d_ema()
    run_alt_zero_diff()

    print("=" * 100)
    print("14. 진입수수료 pnl 반영 확인")
    from fee_check import check_entry_fee
    check_entry_fee(sig)


if __name__ == "__main__":
    main()
