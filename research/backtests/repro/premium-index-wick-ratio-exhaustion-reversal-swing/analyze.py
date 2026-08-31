"""전체 분석 파이프라인: base + 무비용 진단 + 스윕 + 게이트대조군 + de-clustering(R배수) +
반전대조군 + LOO + top-N + 종목간상관(평시/위기) + 매크로클러스터 분해."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import IS_END, IS_START, OOS_END, OOS_START, SYMBOLS
from engine import (find_signals_gated, load_all, run_variant, split_is_oos, trades_to_df,
                     simulate_trade, build_frame, find_signals)


def pf_r(series: pd.Series) -> float:
    pos = series[series > 0].sum()
    neg = -series[series < 0].sum()
    if neg == 0:
        return float("inf") if pos > 0 else float("nan")
    return pos / neg


def t_stat(series: pd.Series) -> float:
    n = len(series)
    if n < 2:
        return float("nan")
    sd = series.std(ddof=1)
    if sd == 0:
        return float("nan")
    return series.mean() / (sd / np.sqrt(n))


DEFAULT = dict(atr_sl_mult=1.4, atr_trail_mult=2.2, max_hold_bars=30)


def summarize(df: pd.DataFrame, label: str, rcol: str = "net_R") -> dict:
    is_df, oos_df, full_df = split_is_oos(df, IS_START, IS_END, OOS_START, OOS_END)
    out = {"label": label, "n_full": len(full_df), "n_is": len(is_df), "n_oos": len(oos_df)}
    for name, sub in [("full", full_df), ("is", is_df), ("oos", oos_df)]:
        if len(sub) == 0:
            out[f"{name}_gross_pf"] = float("nan")
            out[f"{name}_net_pf"] = float("nan")
            out[f"{name}_net_t"] = float("nan")
            out[f"{name}_gross_t"] = float("nan")
            continue
        out[f"{name}_gross_pf"] = pf_r(sub["gross_R"])
        out[f"{name}_net_pf"] = pf_r(sub["net_R"])
        out[f"{name}_net_t"] = t_stat(sub["net_R"])
        out[f"{name}_gross_t"] = t_stat(sub["gross_R"])
    return out


def zero_cost_summary(df: pd.DataFrame) -> dict:
    """무비용(fee=0,slippage=0) 진단: gross_R 을 net 대신 사용한 별도 요약."""
    is_df, oos_df, full_df = split_is_oos(df, IS_START, IS_END, OOS_START, OOS_END)
    out = {}
    for name, sub in [("full", full_df), ("is", is_df), ("oos", oos_df)]:
        if len(sub) == 0:
            out[f"{name}_gross_pf"] = float("nan"); out[f"{name}_gross_t"] = float("nan")
            continue
        out[f"{name}_gross_pf"] = pf_r(sub["gross_R"])
        out[f"{name}_gross_t"] = t_stat(sub["gross_R"])
    return out


def calendar_declustered(df: pd.DataFrame, col: str = "net_R") -> pd.Series:
    """캘린더일(진입일) 단위로 그날의 트레이드 net_R 평균 -> 일 단위 시계열(중복표본 제거)."""
    d = df.copy()
    d["day"] = d["entry_time"].dt.floor("D")
    return d.groupby("day")[col].mean()


def rolling5d_declustered(df: pd.DataFrame, col: str = "net_R") -> pd.Series:
    """5일 롤링 클러스터: entry_time 순 정렬 후 이전 클러스터 종료로부터 5일 이내면 같은
    클러스터로 묶어 클러스터 평균을 반환."""
    d = df.sort_values("entry_time").copy()
    if len(d) == 0:
        return pd.Series(dtype=float)
    cluster_id = 0
    ids = [0]
    last_t = d["entry_time"].iloc[0]
    for t in d["entry_time"].iloc[1:]:
        if (t - last_t) > pd.Timedelta(days=5):
            cluster_id += 1
        ids.append(cluster_id)
        last_t = t
    d["cluster"] = ids
    return d.groupby("cluster")[col].mean()


def main() -> None:
    print("데이터 로딩...")
    universe = load_all()
    for sym, fr in universe.items():
        p = fr["prem"]
        print(f"  {sym}: n_bars={len(p)} range=[{p.index.min()}, {p.index.max()}] "
              f"nan_ext={p['ext_pct'].isna().sum()} nan_consec={p['consec_upper'].isna().sum()}")

    results = {}

    # ---------- ① 기본(base) ----------
    print("\n=== ① 기본 변형 ===")
    base_trades = run_variant(universe, **DEFAULT, gate="full")
    base_df = trades_to_df(base_trades)
    base_df.to_csv("out_base_trades.csv", index=False)
    print(f"n={len(base_df)}")
    summ_base = summarize(base_df, "base")
    print(json.dumps(summ_base, indent=2, default=str))
    results["base"] = summ_base

    is_df, oos_df, full_df = split_is_oos(base_df, IS_START, IS_END, OOS_START, OOS_END)
    assert len(is_df) + len(oos_df) == len(full_df), "IS+OOS != FULL"
    print(f"IS+OOS==FULL 확인: IS={len(is_df)} OOS={len(oos_df)} FULL={len(full_df)}")

    # ---------- ② 무비용 진단 ----------
    print("\n=== ② 무비용(gross) 진단 ===")
    zc = zero_cost_summary(base_df)
    print(json.dumps(zc, indent=2, default=str))
    results["zero_cost"] = zc

    # ---------- ③ 게이트 대조군 ----------
    print("\n=== ③ 게이트/조건제거 대조군 ===")
    gate_results = {}
    for gate in ["no_gate", "no_ext", "no_premium_sign"]:
        tr = run_variant(universe, **DEFAULT, gate=gate)
        gdf = trades_to_df(tr)
        s = summarize(gdf, gate)
        gate_results[gate] = s
        print(gate, json.dumps(s, indent=2, default=str))
    results["gate_controls"] = gate_results

    # ---------- ④ 파라미터 스윕 ----------
    print("\n=== ④ 파라미터 스윕 ===")
    sweep_rows = []
    # wick_th 0.3~0.6
    for wick_th in [0.3, 0.4, 0.5, 0.6]:
        uni = load_all(wick_th=wick_th)
        tr = run_variant(uni, **DEFAULT)
        df = trades_to_df(tr)
        s = summarize(df, f"wick_th={wick_th}")
        sweep_rows.append(s)
    # lookback/min_count 조합 (lookback 4~10, min_count 60~75%)
    for lb, mc in [(4, 3), (6, 4), (8, 5), (10, 7)]:
        uni = load_all(lookback_bars=lb, min_count=mc)
        tr = run_variant(uni, **DEFAULT)
        df = trades_to_df(tr)
        s = summarize(df, f"lookback={lb},min_count={mc}")
        sweep_rows.append(s)
    # ext_th 3~8%
    for ext_th in [0.03, 0.05, 0.08]:
        uni = load_all(ext_th=ext_th)
        tr = run_variant(uni, **DEFAULT)
        df = trades_to_df(tr)
        s = summarize(df, f"ext_th={ext_th}")
        sweep_rows.append(s)
    # atr_sl_mult / atr_trail_mult / max_hold_bars
    for sl, tr_m, mh in [(1.4, 2.2, 20), (1.4, 2.2, 40), (1.0, 3.0, 30), (2.0, 1.5, 30)]:
        trd = run_variant(universe, atr_sl_mult=sl, atr_trail_mult=tr_m, max_hold_bars=mh)
        df = trades_to_df(trd)
        s = summarize(df, f"sl={sl},trail={tr_m},hold={mh}")
        sweep_rows.append(s)
    sweep_df = pd.DataFrame(sweep_rows)
    print(sweep_df[["label", "n_oos", "oos_net_pf", "oos_net_t", "is_gross_pf"]].to_string(index=False))
    results["sweep"] = sweep_rows

    # ---------- ⑤ de-clustering(R배수) ----------
    print("\n=== ⑤ de-clustering(R배수 기준) ===")
    decl = {}
    for name, sub in [("full", full_df), ("oos", oos_df)]:
        if len(sub) == 0:
            continue
        cal = calendar_declustered(sub)
        r5 = rolling5d_declustered(sub)
        decl[f"{name}_calendar"] = {"n": len(cal), "pf": pf_r(cal), "t": t_stat(cal)}
        decl[f"{name}_5d_roll"] = {"n": len(r5), "pf": pf_r(r5), "t": t_stat(r5)}
    print(json.dumps(decl, indent=2, default=str))
    results["declustering"] = decl

    # ---------- ⑥ 반전 대조군 ----------
    print("\n=== ⑥ 반전 대조군(진입가 대칭 재배치 + 청산방향 분기) ===")
    rev_trades = run_variant(universe, **DEFAULT, reverse=True)
    rev_df = trades_to_df(rev_trades)
    rev_summ = summarize(rev_df, "reverse")
    print(json.dumps(rev_summ, indent=2, default=str))
    zero_hold = float((rev_df["hold_bars"] == 0).mean()) if len(rev_df) else float("nan")
    reason_dist = rev_df["exit_reason"].value_counts(normalize=True).to_dict() if len(rev_df) else {}
    hold_dist = rev_df["hold_bars"].describe().to_dict() if len(rev_df) else {}
    base_reason_dist = base_df["exit_reason"].value_counts(normalize=True).to_dict() if len(base_df) else {}
    base_hold_dist = base_df["hold_bars"].describe().to_dict() if len(base_df) else {}
    print(f"reverse zero_hold_frac={zero_hold:.4f}")
    print("reverse exit_reason 분포:", reason_dist)
    print("base exit_reason 분포:", base_reason_dist)
    results["reverse"] = {"summary": rev_summ, "zero_hold_frac": zero_hold,
                           "reason_dist": reason_dist, "hold_dist": hold_dist,
                           "base_reason_dist": base_reason_dist, "base_hold_dist": base_hold_dist}

    # ---------- ⑦ LOO / top-N 제거 ----------
    print("\n=== ⑦ LOO(종목 제외) ===")
    loo_rows = []
    for excl in SYMBOLS:
        uni2 = {k: v for k, v in universe.items() if k != excl}
        tr = run_variant(uni2, **DEFAULT)
        df = trades_to_df(tr)
        s = summarize(df, f"excl={excl}")
        loo_rows.append(s)
    print(pd.DataFrame(loo_rows)[["label", "n_oos", "oos_net_pf", "oos_net_t"]].to_string(index=False))
    results["loo"] = loo_rows

    print("\n=== top-N 제거(OOS, net_R 최상위 트레이드) ===")
    topn_rows = []
    oos_sorted = oos_df.sort_values("net_R", ascending=False)
    for n_rm in [1, 3, 5, 10]:
        remain = oos_sorted.iloc[n_rm:]
        topn_rows.append({"n_removed": n_rm, "n_remain": len(remain),
                           "pf": pf_r(remain["net_R"]), "t": t_stat(remain["net_R"])})
    print(pd.DataFrame(topn_rows).to_string(index=False))
    results["top_n_removed"] = topn_rows

    print("\n=== 최악(worst)-N 제거(OOS, 대칭 점검) ===")
    worstn_rows = []
    oos_sorted_w = oos_df.sort_values("net_R", ascending=True)
    for n_rm in [1, 3, 5, 10]:
        remain = oos_sorted_w.iloc[n_rm:]
        worstn_rows.append({"n_removed": n_rm, "n_remain": len(remain),
                             "pf": pf_r(remain["net_R"]), "t": t_stat(remain["net_R"])})
    print(pd.DataFrame(worstn_rows).to_string(index=False))
    results["worst_n_removed"] = worstn_rows

    # ---------- ⑧ 종목 간 신호 상관(평시/위기) ----------
    print("\n=== ⑧ 종목 간 신호 상관 ===")
    # 종목별 신호일(트리거된 4h 봉의 캘린더일) 이진 지시자 -> 일별 매트릭스
    sig_days = {}
    for sym, fr in universe.items():
        sigs = find_signals(fr)
        days = sorted({t.floor("D") for t, *_ in sigs})
        sig_days[sym] = set(days)
    all_days = sorted(set().union(*sig_days.values()))
    mat = pd.DataFrame(0, index=all_days, columns=SYMBOLS)
    for sym in SYMBOLS:
        mat.loc[list(sig_days[sym]), sym] = 1
    corr_normal = mat.corr()
    print("평시(전기간) 종목간 신호일 상관:")
    print(corr_normal.round(3).to_string())

    # 위기 국면: BTC 절대 일간 수익률 상위 5%
    btc_price = universe["BTCUSDT"]["price"]
    btc_daily = btc_price["close"].resample("1D").last()
    btc_ret = btc_daily.pct_change().abs()
    thresh = btc_ret.quantile(0.95)
    crisis_days = set(btc_ret[btc_ret >= thresh].index)
    crisis_days_in_mat = [d for d in mat.index if d.tz_localize(None).normalize() in
                           {c.tz_localize(None).normalize() for c in crisis_days}] if len(mat.index) else []
    # 단순화: mat.index 를 crisis_days 와 날짜만 비교
    crisis_norm = {pd.Timestamp(c).normalize() for c in crisis_days}
    mat_days_norm = pd.Series([pd.Timestamp(d).normalize() for d in mat.index], index=mat.index)
    mask_crisis = mat_days_norm.isin(crisis_norm)
    mat_crisis = mat.loc[mask_crisis.values]
    corr_crisis = mat_crisis.corr() if len(mat_crisis) >= 3 else None
    print(f"\n위기국면(BTC |일수익률| 상위5%) 신호일 n={len(mat_crisis)} / 전체={len(mat)}")
    if corr_crisis is not None:
        print(corr_crisis.round(3).to_string())
    results["cross_symbol_corr"] = {
        "normal_mean_offdiag": float(np.nanmean(corr_normal.values[np.triu_indices(7, 1)])),
        "n_crisis_days_signaled": int(len(mat_crisis)),
        "crisis_mean_offdiag": (float(np.nanmean(corr_crisis.values[np.triu_indices(7, 1)]))
                                 if corr_crisis is not None else None),
    }

    # ---------- ⑨ 매크로 클러스터 분해 ----------
    print("\n=== ⑨ 매크로 클러스터 분해(5일 롤링, 최고/최악 대칭) ===")
    r5_oos = rolling5d_declustered(oos_df, "net_R") if len(oos_df) else pd.Series(dtype=float)
    macro = {}
    if len(r5_oos) >= 3:
        total = r5_oos.sum()
        best_cluster = r5_oos.sort_values(ascending=False)
        worst_cluster = r5_oos.sort_values(ascending=True)
        for k in [1, 3]:
            rem_best = r5_oos.drop(best_cluster.index[:k])
            rem_worst = r5_oos.drop(worst_cluster.index[:k])
            macro[f"remove_top{k}_cluster"] = {
                "pf": pf_r(rem_best), "t": t_stat(rem_best),
                "removed_R_sum": float(best_cluster.iloc[:k].sum()),
                "removed_frac_of_total": float(best_cluster.iloc[:k].sum() / total) if total else None,
            }
            macro[f"remove_worst{k}_cluster"] = {
                "pf": pf_r(rem_worst), "t": t_stat(rem_worst),
                "removed_R_sum": float(worst_cluster.iloc[:k].sum()),
            }
    print(json.dumps(macro, indent=2, default=str))
    results["macro_cluster"] = macro

    with open("out_summary.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\n완료 — out_summary.json 저장")


if __name__ == "__main__":
    main()
