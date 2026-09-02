"""전체 분석 파이프라인: base + 무비용진단 + 앵커이동대조군 + 스윕 + de-clustering(R배수) +
반전대조군 + LOO + top/worst-N + 종목간상관(동시진입비율 포함) + 승률고정 순열검정."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import (IS_END, IS_START, OOS_END, OOS_START, SYMBOLS, pf_r, split_is_oos,
                    t_stat, win_rate)
from engine import find_signals, load_all, run_variant, trades_to_df

DEFAULT = dict(z_threshold=2.0, atr_sl_mult=1.0, tp_r_mult=1.3, max_hold_bars=8)


def summarize(df: pd.DataFrame, label: str) -> dict:
    is_df, oos_df, full_df = split_is_oos(df, IS_START, IS_END, OOS_START, OOS_END)
    out = {"label": label, "n_full": len(full_df), "n_is": len(is_df), "n_oos": len(oos_df)}
    for name, sub in [("full", full_df), ("is", is_df), ("oos", oos_df)]:
        if len(sub) == 0:
            for k in ["gross_pf", "net_pf", "gross_t", "net_t", "win_rate"]:
                out[f"{name}_{k}"] = float("nan")
            continue
        out[f"{name}_gross_pf"] = pf_r(sub["gross_R"])
        out[f"{name}_net_pf"] = pf_r(sub["net_R"])
        out[f"{name}_gross_t"] = t_stat(sub["gross_R"])
        out[f"{name}_net_t"] = t_stat(sub["net_R"])
        out[f"{name}_win_rate"] = win_rate(sub["net_R"])
    return out


def calendar_declustered(df: pd.DataFrame, col: str = "net_R") -> pd.Series:
    d = df.copy()
    d["day"] = d["entry_time"].dt.floor("D")
    return d.groupby("day")[col].mean()


def rolling5d_declustered(df: pd.DataFrame, col: str = "net_R") -> pd.Series:
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


def perm_test_fixed_winrate(df: pd.DataFrame, col: str = "net_R", n_iter: int = 1000,
                            seed: int = 0) -> dict:
    """승률(부호 비율)은 그대로 고정하고, 부호를 트레이드에 무작위 재배당(shuffle)해
    mean(R) 의 귀무분포를 만든다(부호 무작위화 50/50 대신 관측 승률을 그대로 사용 —
    승률<50% 극단 백분위가 산술적 귀결로 나오는 것을 방지)."""
    rng = np.random.default_rng(seed)
    r = df[col].to_numpy()
    if len(r) == 0:
        return {"n": 0}
    magnitudes = np.abs(r)
    n_win = int((r > 0).sum())
    n = len(r)
    obs_mean = r.mean()
    sims = np.empty(n_iter)
    signs_template = np.array([1.0] * n_win + [-1.0] * (n - n_win))
    for i in range(n_iter):
        signs = rng.permutation(signs_template)
        sims[i] = (magnitudes * signs).mean()
    pct = float((sims <= obs_mean).mean() * 100)
    return {"n": n, "n_win": n_win, "win_rate": n_win / n, "obs_mean_R": float(obs_mean),
            "sim_mean": float(sims.mean()), "sim_std": float(sims.std()), "percentile": pct}


def main() -> None:
    print("데이터 로딩(base, anchor=0h)...")
    universe = load_all()
    for sym, fr in universe.items():
        ev = fr["events"]
        print(f"  {sym}: n_events={len(ev)} valid_cz={ev['c_z'].notna().sum()} "
              f"range=[{ev['t0'].min()}, {ev['t0'].max()}]")

    results = {}

    # ---------- ① 기본 ----------
    print("\n=== ① 기본(base) ===")
    base_trades = run_variant(universe, **DEFAULT)
    base_df = trades_to_df(base_trades)
    base_df.to_csv("out_base_trades.csv", index=False)
    print(f"n={len(base_df)}")
    summ_base = summarize(base_df, "base")
    print(json.dumps(summ_base, indent=2, default=str))
    results["base"] = summ_base

    is_df, oos_df, full_df = split_is_oos(base_df, IS_START, IS_END, OOS_START, OOS_END)
    assert len(is_df) + len(oos_df) == len(full_df), "IS+OOS != FULL"
    print(f"IS+OOS==FULL 확인: IS={len(is_df)} OOS={len(oos_df)} FULL={len(full_df)}")

    exit_dist = base_df["exit_reason"].value_counts(normalize=True).to_dict()
    print("exit_reason 분포:", exit_dist)
    results["exit_reason_dist"] = exit_dist

    # ---------- ② 앵커 이동 대조군 (사전 폐기조건과 별개, 정산 이벤트 테제 자체 검정) ----------
    print("\n=== ② 앵커 이동 대조군(02/10/18, 04/12/20 UTC) ===")
    anchor_results = {}
    for off_h in [2, 4]:
        uni_shift = load_all(anchor_offset_hours=off_h)
        tr = run_variant(uni_shift, **DEFAULT)
        df = trades_to_df(tr)
        s = summarize(df, f"anchor_offset={off_h}h")
        anchor_results[f"offset_{off_h}h"] = s
        print(f"offset={off_h}h:", json.dumps(s, indent=2, default=str))
    results["anchor_shift"] = anchor_results

    # ---------- ③ 파라미터 스윕 ----------
    print("\n=== ③ 파라미터 스윕 ===")
    sweep_rows = []
    for zt in [1.5, 1.75, 2.0, 2.25, 2.5]:
        tr = run_variant(universe, z_threshold=zt, atr_sl_mult=DEFAULT["atr_sl_mult"],
                         tp_r_mult=DEFAULT["tp_r_mult"], max_hold_bars=DEFAULT["max_hold_bars"])
        df = trades_to_df(tr)
        sweep_rows.append(summarize(df, f"z_threshold={zt}"))
    for slm in [0.8, 1.0, 1.2, 1.5]:
        tr = run_variant(universe, z_threshold=DEFAULT["z_threshold"], atr_sl_mult=slm,
                         tp_r_mult=DEFAULT["tp_r_mult"], max_hold_bars=DEFAULT["max_hold_bars"])
        df = trades_to_df(tr)
        sweep_rows.append(summarize(df, f"atr_sl_mult={slm}"))
    for mh in [4, 6, 8, 12, 16]:
        tr = run_variant(universe, z_threshold=DEFAULT["z_threshold"],
                         atr_sl_mult=DEFAULT["atr_sl_mult"], tp_r_mult=DEFAULT["tp_r_mult"],
                         max_hold_bars=mh)
        df = trades_to_df(tr)
        sweep_rows.append(summarize(df, f"max_hold_bars={mh}"))
    for lb in [30, 45, 60, 90, 120]:
        uni2 = load_all(lookback=lb)
        tr = run_variant(uni2, **DEFAULT)
        df = trades_to_df(tr)
        sweep_rows.append(summarize(df, f"lookback={lb}"))
    for co in [30, 60, 90, 120]:
        uni2 = load_all(check_offset_min=co)
        tr = run_variant(uni2, **DEFAULT)
        df = trades_to_df(tr)
        sweep_rows.append(summarize(df, f"check_offset_min={co}"))
    sweep_df = pd.DataFrame(sweep_rows)
    print(sweep_df[["label", "n_oos", "oos_net_pf", "oos_net_t", "is_gross_pf"]].to_string(index=False))
    results["sweep"] = sweep_rows

    # ---------- ④ de-clustering(R배수) ----------
    print("\n=== ④ de-clustering(캘린더일 / 5일 롤링, R배수) ===")
    decl = {}
    for name, sub in [("full", full_df), ("oos", oos_df), ("is", is_df)]:
        if len(sub) == 0:
            continue
        cal_net = calendar_declustered(sub, "net_R")
        cal_gross = calendar_declustered(sub, "gross_R")
        r5_net = rolling5d_declustered(sub, "net_R")
        decl[f"{name}_calendar_net"] = {"n": len(cal_net), "pf": pf_r(cal_net), "t": t_stat(cal_net)}
        decl[f"{name}_calendar_gross"] = {"n": len(cal_gross), "pf": pf_r(cal_gross),
                                          "t": t_stat(cal_gross)}
        decl[f"{name}_5d_roll_net"] = {"n": len(r5_net), "pf": pf_r(r5_net), "t": t_stat(r5_net)}
    print(json.dumps(decl, indent=2, default=str))
    results["declustering"] = decl

    # ---------- ⑤ 반전 대조군 ----------
    print("\n=== ⑤ 반전 대조군 ===")
    rev_trades = run_variant(universe, **DEFAULT, reverse=True)
    rev_df = trades_to_df(rev_trades)
    rev_summ = summarize(rev_df, "reverse")
    zero_hold = float((rev_df["hold_bars"] <= 1).mean()) if len(rev_df) else float("nan")
    zero_hold_base = float((base_df["hold_bars"] <= 1).mean()) if len(base_df) else float("nan")
    rev_reason = rev_df["exit_reason"].value_counts(normalize=True).to_dict() if len(rev_df) else {}
    print(json.dumps(rev_summ, indent=2, default=str))
    print(f"reverse hold<=1bar frac={zero_hold:.4f}  base hold<=1bar frac={zero_hold_base:.4f}")
    print("reverse exit_reason:", rev_reason)
    results["reverse"] = {"summary": rev_summ, "hold_le1_frac": zero_hold,
                          "base_hold_le1_frac": zero_hold_base, "reason_dist": rev_reason}

    # ---------- ⑥ LOO ----------
    print("\n=== ⑥ LOO(종목 제외) ===")
    loo_rows = []
    for excl in SYMBOLS:
        uni2 = {k: v for k, v in universe.items() if k != excl}
        tr = run_variant(uni2, **DEFAULT)
        df = trades_to_df(tr)
        loo_rows.append(summarize(df, f"excl={excl}"))
    print(pd.DataFrame(loo_rows)[["label", "n_oos", "oos_net_pf", "oos_net_t"]].to_string(index=False))
    results["loo"] = loo_rows

    # ---------- ⑦ top/worst-N 제거(OOS) ----------
    print("\n=== ⑦ top/worst-N 제거(OOS, net_R) ===")
    topn_rows, worstn_rows = [], []
    if len(oos_df):
        oos_sorted = oos_df.sort_values("net_R", ascending=False)
        oos_sorted_w = oos_df.sort_values("net_R", ascending=True)
        for n_rm in [1, 3, 5, 10]:
            rem = oos_sorted.iloc[n_rm:]
            topn_rows.append({"n_removed": n_rm, "n_remain": len(rem), "pf": pf_r(rem["net_R"]),
                              "t": t_stat(rem["net_R"])})
            remw = oos_sorted_w.iloc[n_rm:]
            worstn_rows.append({"n_removed": n_rm, "n_remain": len(remw),
                                "pf": pf_r(remw["net_R"]), "t": t_stat(remw["net_R"])})
    print("top-N(승리) 제거:"); print(pd.DataFrame(topn_rows).to_string(index=False))
    print("worst-N(패배) 제거:"); print(pd.DataFrame(worstn_rows).to_string(index=False))
    results["top_n_removed"] = topn_rows
    results["worst_n_removed"] = worstn_rows

    # ---------- ⑧ 종목 간 신호 상관 + 동시진입 비율 ----------
    print("\n=== ⑧ 종목 간 신호 상관 / 동시 정산시각 진입 비율 ===")
    sig_settle = {}
    for sym, fr in universe.items():
        sigs = find_signals(fr, z_threshold=DEFAULT["z_threshold"])
        sig_settle[sym] = set(sigs["settlement_time"])
    all_settle = sorted(set().union(*sig_settle.values()))
    mat = pd.DataFrame(0, index=all_settle, columns=SYMBOLS)
    for sym in SYMBOLS:
        mat.loc[sorted(sig_settle[sym]), sym] = 1
    n_symbols_per_slot = mat.sum(axis=1)
    overlap_frac = float((n_symbols_per_slot >= 2).mean())
    max_concurrent = int(n_symbols_per_slot.max())
    corr_normal = mat.corr()
    print(f"고유 정산이벤트슬롯 수={len(mat)}, 그중 2종목이상 동시신호 비율={overlap_frac:.4f}, "
          f"최대동시신호종목수={max_concurrent}")
    print("동시신호 슬롯 수 분포:", n_symbols_per_slot.value_counts().sort_index().to_dict())

    # 위기국면: BTC 절대 일간 수익률 상위 5%
    btc_price = universe["BTCUSDT"]["price_15m"]
    btc_daily = btc_price["close"].resample("1D").last()
    btc_ret = btc_daily.pct_change().abs()
    thresh = btc_ret.quantile(0.95)
    crisis_norm = {pd.Timestamp(c).normalize() for c in btc_ret[btc_ret >= thresh].index}
    mat_days_norm = pd.Series([pd.Timestamp(d).normalize() for d in mat.index], index=mat.index)
    mask_crisis = mat_days_norm.isin(crisis_norm)
    mat_crisis = mat.loc[mask_crisis.values]
    corr_crisis = mat_crisis.corr() if len(mat_crisis) >= 3 else None
    print(f"위기국면 신호슬롯 n={len(mat_crisis)} / 전체={len(mat)}")
    results["cross_symbol"] = {
        "n_slots": len(mat), "overlap_2plus_frac": overlap_frac, "max_concurrent": max_concurrent,
        "normal_mean_offdiag": float(np.nanmean(corr_normal.values[np.triu_indices(7, 1)])),
        "n_crisis_slots": int(len(mat_crisis)),
        "crisis_mean_offdiag": (float(np.nanmean(corr_crisis.values[np.triu_indices(7, 1)]))
                                if corr_crisis is not None else None),
    }

    # ---------- ⑨ 승률고정 순열검정 ----------
    print("\n=== ⑨ 승률고정 순열검정(net_R, OOS) ===")
    perm = perm_test_fixed_winrate(oos_df, "net_R", n_iter=1000, seed=0) if len(oos_df) else {}
    print(json.dumps(perm, indent=2, default=str))
    results["perm_test_oos"] = perm

    with open("out_summary.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\n완료 — out_summary.json 저장")


if __name__ == "__main__":
    main()
