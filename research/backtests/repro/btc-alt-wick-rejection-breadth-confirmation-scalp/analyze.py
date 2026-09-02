"""BTC 웍 리젝션 + 알트 브레드스 확인 스캘프 — 전체 분석 파이프라인.

실행: python3 analyze.py  (download.py 로 데이터 먼저 받아야 함)
전부 R-배수(net=수수료+슬리피지 0.14% 반영, gross=0비용) 기준.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import common as C
import engine as E

HERE = Path(__file__).resolve().parent
OUT = {}


def summarize_all(df: pd.DataFrame, col: str) -> dict:
    is_df, oos_df, full_df = E.split_is_oos(df, C.IS_START, C.IS_END, C.OOS_START, C.OOS_END)
    return {"IS": C.summarize(is_df, col), "OOS": C.summarize(oos_df, col),
            "FULL": C.summarize(full_df, col),
            "n_check": {"is": len(is_df), "oos": len(oos_df), "full": len(full_df),
                        "is_plus_oos_eq_full": len(is_df) + len(oos_df) == len(full_df)}}


def day_declustered(df: pd.DataFrame, col: str) -> dict:
    d = df.copy()
    d["day"] = d["entry_time"].dt.floor("D")
    g = d.groupby("day")[col].sum()
    return {"unique_days": int(len(g)), "pf": C.pf_r(g), "t": C.t_stat(g)}


def rolling5_cluster(df: pd.DataFrame, col: str = "net_R", n_windows: int = 3) -> dict:
    d = df.sort_values("entry_time").copy()
    d["day"] = d["entry_time"].dt.floor("D")
    daily = d.groupby("day")[col].sum()
    total = float(daily.sum())
    roll = daily.rolling(5, min_periods=1).sum()
    r = roll.copy()
    best_list, worst_list = [], []
    rb = r.copy()
    for _ in range(n_windows):
        if rb.isna().all():
            break
        wmax = rb.idxmax()
        best_list.append((str(wmax.date()), float(rb[wmax])))
        lo, hi = wmax - pd.Timedelta(days=4), wmax + pd.Timedelta(days=4)
        rb[(rb.index >= lo) & (rb.index <= hi)] = np.nan
    rw = r.copy()
    for _ in range(n_windows):
        if rw.isna().all():
            break
        wmin = rw.idxmin()
        worst_list.append((str(wmin.date()), float(rw[wmin])))
        lo, hi = wmin - pd.Timedelta(days=4), wmin + pd.Timedelta(days=4)
        rw[(rw.index >= lo) & (rw.index <= hi)] = np.nan
    worst_sum = sum(x[1] for x in worst_list)
    best_sum = sum(x[1] for x in best_list)
    return {"total": total, "best_nonoverlap_5d_windows": best_list,
            "worst_nonoverlap_5d_windows": worst_list,
            "best_frac_of_total": (best_sum / total) if total != 0 else None,
            "worst_frac_of_total": (worst_sum / total) if total != 0 else None}


def main() -> None:
    u = C.load_all()
    frame = E.build_confirm_frame(u)
    OUT["universe_coverage"] = {sym: int(len(u[sym])) for sym in C.SYMBOLS}
    OUT["confirm_frame_len"] = int(len(frame))

    # --- 1. 결합확률 실측 ---
    raw_upper = int(frame["btc_upper"].sum())
    raw_lower = int(frame["btc_lower"].sum())
    sig_all = E.find_signals(frame, None)
    sig_gated4 = E.find_signals(frame, 4)
    sig_gated3 = E.find_signals(frame, 3)
    years = (frame.index.max() - frame.index.min()).days / 365.25
    OUT["frequency"] = {
        "years_span": round(years, 3),
        "btc_raw_upper": raw_upper, "btc_raw_lower": raw_lower,
        "btc_raw_total": raw_upper + raw_lower,
        "btc_raw_per_year": round((raw_upper + raw_lower) / years, 1),
        "confirmed_th4_total": len(sig_gated4),
        "confirmed_th4_per_year": round(len(sig_gated4) / years, 1),
        "confirmed_th4_pass_rate": round(len(sig_gated4) / (raw_upper + raw_lower), 4),
        "confirmed_th3_total": len(sig_gated3),
        "confirmed_th3_per_year": round(len(sig_gated3) / years, 1),
        "spec_estimated_per_year_range": [27, 72],
    }

    # --- 2. 기본판(th=4) IS/OOS/FULL, net & gross ---
    trades_base = E.run_variant(frame, confirm_n_th=4)
    df_base = E.trades_to_df(trades_base)
    df_base.to_csv(HERE / "out_base_trades.csv", index=False)
    OUT["base_net"] = summarize_all(df_base, "net_R")
    OUT["base_gross"] = summarize_all(df_base, "gross_R")
    OUT["base_exit_reasons"] = df_base["exit_reason"].value_counts().to_dict()
    OUT["base_hold_bars_mean"] = float(df_base["hold_bars"].mean())
    OUT["base_k1_frac"] = float((df_base["hold_bars"] == 1).mean())

    # --- 3. de-clustering(캘린더일) ---
    is_df, oos_df, full_df = E.split_is_oos(df_base, C.IS_START, C.IS_END, C.OOS_START, C.OOS_END)
    OUT["declust_day"] = {
        "IS_net": day_declustered(is_df, "net_R"), "OOS_net": day_declustered(oos_df, "net_R"),
        "IS_gross": day_declustered(is_df, "gross_R"), "OOS_gross": day_declustered(oos_df, "gross_R"),
    }

    # --- 4. 5일 롤링 클러스터(손실 대칭점검) ---
    OUT["rolling5_cluster_OOS_net"] = rolling5_cluster(oos_df, "net_R")
    OUT["rolling5_cluster_OOS_gross"] = rolling5_cluster(oos_df, "gross_R")

    # --- 5. 반전 대조군 ---
    trades_rev = E.run_variant(frame, confirm_n_th=4, reverse=True)
    df_rev = E.trades_to_df(trades_rev)
    OUT["reverse_net"] = summarize_all(df_rev, "net_R")
    OUT["reverse_gross"] = summarize_all(df_rev, "gross_R")
    OUT["reverse_exit_reasons"] = df_rev["exit_reason"].value_counts().to_dict()
    OUT["reverse_k1_frac"] = float((df_rev["hold_bars"] == 1).mean())

    # --- 6. 대조군①: BTC 단독판(게이트 제거) ---
    trades_c1 = E.run_variant(frame, confirm_n_th=None)
    df_c1 = E.trades_to_df(trades_c1)
    OUT["control1_no_gate_net"] = summarize_all(df_c1, "net_R")
    OUT["control1_no_gate_gross"] = summarize_all(df_c1, "gross_R")

    # --- 7. 재포장 점검: confirm_n vs ATR z-score 상관(전구간 + 트리거시점) ---
    atr = frame["atr"]
    z = (atr - atr.rolling(60).mean()) / atr.rolling(60).std()
    frame_z = frame.copy()
    frame_z["atr_z"] = z
    full_corr_u = frame_z[["confirm_n_upper", "atr_z"]].corr().iloc[0, 1]
    full_corr_l = frame_z[["confirm_n_lower", "atr_z"]].corr().iloc[0, 1]
    frame_z["confirm_n_trig"] = np.where(frame_z["btc_upper"], frame_z["confirm_n_upper"],
                                          np.where(frame_z["btc_lower"], frame_z["confirm_n_lower"], np.nan))
    trig = frame_z.dropna(subset=["confirm_n_trig"])
    trig_corr = trig[["confirm_n_trig", "atr_z"]].corr().iloc[0, 1]
    OUT["repackaging_corr"] = {
        "full_period_confirm_upper_vs_atrz": float(full_corr_u),
        "full_period_confirm_lower_vs_atrz": float(full_corr_l),
        "trigger_time_only_corr": float(trig_corr), "trigger_n": int(len(trig)),
        "danger_threshold": 0.85,
    }

    # --- 8. 대조군②: 변동성 브레드스 대체판(표본수 매칭) ---
    target_rate = len(sig_gated4) / len(sig_all)
    valid = frame_z.loc[[s[0] for s in sig_all], "atr_z"].dropna()
    z_th = float(valid.quantile(1 - target_rate))
    gated_sig2 = [(t, d, cn) for (t, d, cn) in sig_all
                  if pd.notna(frame_z.loc[t, "atr_z"]) and frame_z.loc[t, "atr_z"] >= z_th]
    trades_c2 = E.run_variant(frame_z, signals=gated_sig2)
    df_c2 = E.trades_to_df(trades_c2)
    OUT["control2_volz_gate"] = {
        "z_threshold": z_th, "n_signals": len(gated_sig2),
        "net": summarize_all(df_c2, "net_R"), "gross": summarize_all(df_c2, "gross_R"),
    }

    # --- 9. LOO(알트 제외) ---
    idx = frame.index
    loo_rows = []
    for drop in C.ALTS:
        remain = [a for a in C.ALTS if a != drop]
        upper_cnt = pd.Series(0, index=idx)
        lower_cnt = pd.Series(0, index=idx)
        for alt in remain:
            a = u[alt].loc[idx]
            upper_cnt = upper_cnt.add(a["is_upper"].astype(int), fill_value=0)
            lower_cnt = lower_cnt.add(a["is_lower"].astype(int), fill_value=0)
        fr = frame[["open", "high", "low", "close", "atr", "btc_upper", "btc_lower"]].copy()
        fr["confirm_n_upper"] = upper_cnt
        fr["confirm_n_lower"] = lower_cnt
        for th in [3, 4]:
            sig = E.find_signals(fr, th)
            trades = E.run_variant(fr, signals=sig)
            dfv = E.trades_to_df(trades)
            _, oos_v, _ = E.split_is_oos(dfv, C.IS_START, C.IS_END, C.OOS_START, C.OOS_END)
            s = C.summarize(oos_v, "net_R")
            loo_rows.append({"drop_alt": drop, "confirm_n_th": th, "OOS_n": s["n"],
                              "OOS_pf": s["pf"], "OOS_t": s["t"]})
    OUT["loo_alt"] = loo_rows

    # --- 10. 파라미터 스윕 ---
    sweep_rows = []
    base_u_full = E.build_universe()
    base_frame_full = E.build_confirm_frame(base_u_full)

    def eval_v(fr, confirm_n_th=4, rr_target=C.RR_TARGET, sl_buffer=C.SL_BUFFER, reverse=False):
        trades = E.run_variant(fr, confirm_n_th=confirm_n_th, reverse=reverse,
                                rr_target=rr_target, sl_buffer=sl_buffer)
        dfv = E.trades_to_df(trades)
        is_v, oos_v, _ = E.split_is_oos(dfv, C.IS_START, C.IS_END, C.OOS_START, C.OOS_END)
        return C.summarize(is_v, "net_R"), C.summarize(oos_v, "net_R"), C.summarize(oos_v, "gross_R")

    for th in [3, 4, 5]:
        isr, oosr, oosg = eval_v(base_frame_full, confirm_n_th=th)
        sweep_rows.append(("confirm_n_th", th, isr, oosr, oosg))
    for wbm in [1.2, 1.5, 2.0]:
        fr = E.build_confirm_frame(E.build_universe(wick_body_mult=wbm))
        isr, oosr, oosg = eval_v(fr)
        sweep_rows.append(("wick_body_mult", wbm, isr, oosr, oosg))
    for wam in [0.8, 1.0, 1.5]:
        fr = E.build_confirm_frame(E.build_universe(wick_atr_mult=wam))
        isr, oosr, oosg = eval_v(fr)
        sweep_rows.append(("wick_atr_mult", wam, isr, oosr, oosg))
    for clt in [0.3, 0.4, 0.45]:
        fr = E.build_confirm_frame(E.build_universe(close_loc_th=clt))
        isr, oosr, oosg = eval_v(fr)
        sweep_rows.append(("close_loc_th", clt, isr, oosr, oosg))
    for rr in [1.0, 1.3, 1.8]:
        isr, oosr, oosg = eval_v(base_frame_full, rr_target=rr)
        sweep_rows.append(("rr_target", rr, isr, oosr, oosg))
    for slb in [0.15, 0.2, 0.3]:
        isr, oosr, oosg = eval_v(base_frame_full, sl_buffer=slb)
        sweep_rows.append(("sl_buffer", slb, isr, oosr, oosg))

    OUT["param_sweep"] = [
        {"param": p, "value": v, "IS_n": isr["n"], "IS_pf": isr["pf"], "IS_t": isr["t"],
         "OOS_n": oosr["n"], "OOS_pf": oosr["pf"], "OOS_t": oosr["t"],
         "OOS_gross_pf": oosg["pf"], "OOS_gross_t": oosg["t"]}
        for (p, v, isr, oosr, oosg) in sweep_rows
    ]

    # --- 11. 룩어헤드 절단 감사 ---
    cut = pd.Timestamp("2023-06-15", tz="UTC")
    u2 = {sym: df.loc[:cut] for sym, df in u.items()}
    frame_cut = E.build_confirm_frame(u2)
    sig_cut = E.find_signals(frame_cut, 4)
    margin = pd.Timedelta(minutes=90)
    sig_full_before = [s for s in sig_gated4 if s[0] <= cut - margin]
    sig_cut_before = [s for s in sig_cut if s[0] <= cut - margin]
    OUT["lookahead_audit"] = {
        "cutoff": str(cut), "n_full_before": len(sig_full_before),
        "n_cut_before": len(sig_cut_before),
        "identical": sig_full_before == sig_cut_before,
    }

    # --- 12. 무작위 방향 배정 대조(placebo) + 승률고정 순열검정 ---
    sig4 = E.find_signals(frame, 4)
    trades_fwd = E.run_variant(frame, signals=sig4, reverse=False)
    trades_rev2 = E.run_variant(frame, signals=sig4, reverse=True)
    df_fwd = E.trades_to_df(trades_fwd)
    df_rev2 = E.trades_to_df(trades_rev2)
    mask_oos = (df_fwd["entry_time"] >= C.OOS_START) & (df_fwd["entry_time"] <= C.OOS_END)
    fwd_R = df_fwd.loc[mask_oos, "net_R"].to_numpy()
    rev_R = df_rev2.loc[mask_oos, "net_R"].to_numpy()
    n = len(fwd_R)
    rng = np.random.default_rng(20260902)  # 고정시드(hash() 미사용)
    N = 200
    means, pfs = [], []
    for _ in range(N):
        choice = rng.integers(0, 2, size=n)
        mix = np.where(choice == 0, fwd_R, rev_R)
        means.append(mix.mean())
        pfs.append(C.pf_r(pd.Series(mix)))
    means = np.array(means)
    pfs = np.array(pfs)
    actual_pf = C.pf_r(pd.Series(fwd_R))
    win_rate = float((fwd_R > 0).mean())
    pos_vals = fwd_R[fwd_R > 0]
    neg_vals = fwd_R[fwd_R <= 0]
    N2 = 200
    pf_perm = []
    for _ in range(N2):
        perm_win = rng.random(n) < win_rate
        sample = np.where(perm_win, rng.choice(pos_vals, size=n), rng.choice(neg_vals, size=n))
        pf_perm.append(C.pf_r(pd.Series(sample)))
    pf_perm = np.array(pf_perm)
    OUT["placebo_random_direction"] = {
        "n_oos": n, "actual_mean_R": float(fwd_R.mean()), "actual_pf": float(actual_pf),
        "random_dir_mean_R_avg": float(means.mean()), "random_dir_mean_R_std": float(means.std()),
        "actual_percentile_mean_R": float((means < fwd_R.mean()).mean() * 100),
        "actual_percentile_pf": float((pfs < actual_pf).mean() * 100),
        "n_shuffles": N,
    }
    OUT["placebo_winrate_fixed_permutation"] = {
        "win_rate": win_rate, "pf_perm_mean": float(pf_perm.mean()),
        "pf_perm_std": float(pf_perm.std()),
        "actual_percentile_pf": float((pf_perm < actual_pf).mean() * 100),
        "n_perm": N2,
    }

    # --- 13. 사전 폐기조건 판정 ---
    oos_summary = OUT["base_net"]["OOS"]
    kill_a = oos_summary["n"] < 15
    kill_b = (oos_summary["pf"] < 1.15) or (abs(oos_summary["t"]) < 1.96)
    r_max = max(abs(full_corr_u), abs(full_corr_l), abs(trig_corr))
    kill_c = (r_max >= 0.85)  # AND절 뒷부분(구분불가)은 앞절이 거짓이라 평가 불필요
    worst_frac = OUT["rolling5_cluster_OOS_net"]["worst_frac_of_total"]
    kill_d = (worst_frac is not None) and (worst_frac >= 0.5)
    pass_bar = (oos_summary["pf"] >= 1.3) and (oos_summary["t"] >= 1.96)
    OUT["verdict"] = {
        "kill_a_n<15": bool(kill_a), "kill_b_pf<1.15_or_t_insig": bool(kill_b),
        "kill_c_repackaging_r>=0.85_and_indistinct": bool(kill_c),
        "kill_d_5day_cluster>=50pct": bool(kill_d),
        "pass_bar_met": bool(pass_bar),
        "final": "FAIL" if (kill_a or kill_b or kill_c or kill_d or not pass_bar) else "PASS",
    }

    def default(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return str(o)

    with open(HERE / "out_summary.json", "w") as f:
        json.dump(OUT, f, indent=2, default=default)
    print(json.dumps(OUT["verdict"], indent=2, default=default))
    print("frequency:", OUT["frequency"])
    print("base_net OOS:", OUT["base_net"]["OOS"])
    print("base_gross OOS:", OUT["base_gross"]["OOS"])


if __name__ == "__main__":
    main()
