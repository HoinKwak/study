"""파라미터 스윕(6축 전부) + 대조군(no_rank/shuffle/reverse) + de-clustering + LOO/top-N."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import SYMBOLS, IS_START, IS_END, OOS_START, OOS_END
from engine import load_all, run_variant, trades_to_df, split_is_oos, pf_r, t_stat

DEFAULT = dict(squeeze_entry_pctile=0.20, squeeze_exit_pctile=0.70, trigger_window=10,
                top_k=2, donchian_len=15, atr_sl_mult=1.5, atr_trail_mult=3.0,
                max_hold_days=15)

_UNIVERSE_CACHE: dict[int, dict] = {}


def get_universe(squeeze_window: int, donchian_len: int):
    key = (squeeze_window, donchian_len)
    if key not in _UNIVERSE_CACHE:
        _UNIVERSE_CACHE[key] = load_all(squeeze_window=squeeze_window, donchian_len=donchian_len)
    return _UNIVERSE_CACHE[key]


def summarize(df: pd.DataFrame) -> dict:
    is_df, oos_df, full_df = split_is_oos(df)
    out = {"n_full": len(full_df), "n_is": len(is_df), "n_oos": len(oos_df)}
    for name, sub in [("full", full_df), ("is", is_df), ("oos", oos_df)]:
        if len(sub) == 0:
            for m in ["gross_pf", "net_pf", "net_t", "gross_t"]:
                out[f"{name}_{m}"] = float("nan")
            continue
        out[f"{name}_gross_pf"] = pf_r(sub["gross_R"])
        out[f"{name}_net_pf"] = pf_r(sub["net_R"])
        out[f"{name}_net_t"] = t_stat(sub["net_R"])
        out[f"{name}_gross_t"] = t_stat(sub["gross_R"])
    return out


def unique_calendar_days(df: pd.DataFrame, col: str = "entry_time") -> int:
    return df[col].dt.date.nunique()


def declustered_daily(df: pd.DataFrame, value_col: str) -> pd.Series:
    """같은 캘린더일(진입일) 트레이드를 평균해 일단위로 재집계."""
    if len(df) == 0:
        return pd.Series(dtype=float)
    g = df.copy()
    g["day"] = g["entry_time"].dt.date
    return g.groupby("day")[value_col].mean()


def declustered_rolling(df: pd.DataFrame, value_col: str, window_days: int = 5) -> pd.Series:
    """진입일을 window_days 블록으로 묶어(첫 진입일 기준 그리디 클러스터링) 평균 재집계."""
    if len(df) == 0:
        return pd.Series(dtype=float)
    g = df.sort_values("entry_time").copy()
    dates = g["entry_time"].dt.floor("D").tolist()
    clusters = []
    cur_start = None
    cur_vals = []
    for d, v in zip(dates, g[value_col]):
        if cur_start is None or (d - cur_start).days >= window_days:
            if cur_vals:
                clusters.append(np.mean(cur_vals))
            cur_start = d
            cur_vals = [v]
        else:
            cur_vals.append(v)
    if cur_vals:
        clusters.append(np.mean(cur_vals))
    return pd.Series(clusters)


def main() -> None:
    print("데이터 로딩...")
    base_universe = get_universe(60, 15)

    results = {}

    # === 기본 ===
    base_trades = run_variant(base_universe, **DEFAULT)
    base_df = trades_to_df(base_trades)
    base_df.to_csv("out_base_trades.csv", index=False)
    results["base"] = summarize(base_df)
    print("base:", json.dumps(results["base"], indent=2))
    print("exit_reason 분포:\n", base_df["exit_reason"].value_counts())
    print("종목별 트레이드수:\n", base_df["symbol"].value_counts())

    # === 스윕 6축 ===
    sweep_axes = {
        "squeeze_window": [40, 60, 90],
        "squeeze_entry_pctile": [0.15, 0.20, 0.30],
        "squeeze_exit_pctile": [0.60, 0.70, 0.80],
        "trigger_window": [7, 10, 15],
        "donchian_len": [10, 15, 25],
        "top_k": [1, 2, 3],
    }
    sweep_rows = []
    for axis, values in sweep_axes.items():
        for v in values:
            params = dict(DEFAULT)
            params[axis] = v
            uni_kwargs = {"squeeze_window": 60, "donchian_len": 15}
            if axis == "squeeze_window":
                uni_kwargs["squeeze_window"] = v
            if axis == "donchian_len":
                uni_kwargs["donchian_len"] = v
            uni = get_universe(**uni_kwargs)
            # squeeze_window/donchian_len 은 universe 재구성(uni_kwargs)으로 반영되고
            # run_variant 는 이를 받지 않음(중복/미사용 인자라 제거)
            rv_params = {k: v2 for k, v2 in params.items()
                         if k not in ("squeeze_window", "donchian_len")}
            trades = run_variant(uni, **rv_params)
            df = trades_to_df(trades)
            s = summarize(df)
            s["axis"] = axis
            s["value"] = v
            sweep_rows.append(s)
            print(f"스윕 {axis}={v}: n_full={s['n_full']} n_oos={s['n_oos']} "
                  f"OOS net_pf={s['oos_net_pf']:.3f} t={s['oos_net_t']:.2f} "
                  f"IS gross_pf={s['is_gross_pf']:.3f}" if s['n_is'] else "")
    sweep_df = pd.DataFrame(sweep_rows)
    sweep_df.to_csv("out_sweep.csv", index=False)
    results["sweep_n"] = len(sweep_df)

    # === 대조군: no_rank(임계 통과 전원, top_k 무제한) ===
    params_nr = dict(DEFAULT)
    nr_trades = run_variant(base_universe, squeeze_entry_pctile=params_nr["squeeze_entry_pctile"],
                             squeeze_exit_pctile=params_nr["squeeze_exit_pctile"],
                             trigger_window=params_nr["trigger_window"], top_k=999,
                             donchian_len=params_nr["donchian_len"],
                             atr_sl_mult=params_nr["atr_sl_mult"],
                             atr_trail_mult=params_nr["atr_trail_mult"],
                             max_hold_days=params_nr["max_hold_days"], rank_mode="no_rank")
    nr_df = trades_to_df(nr_trades)
    nr_df.to_csv("out_norank_trades.csv", index=False)
    results["no_rank"] = summarize(nr_df)
    print("\nno_rank 대조군:", json.dumps(results["no_rank"], indent=2))

    # === 대조군: shuffle(랭킹 무작위, 20회) ===
    shuffle_summaries = []
    for seed in range(20):
        sh_trades = run_variant(base_universe, **DEFAULT, rank_mode="shuffle", shuffle_seed=seed)
        sh_df = trades_to_df(sh_trades)
        s = summarize(sh_df)
        s["seed"] = seed
        shuffle_summaries.append(s)
    shuffle_df = pd.DataFrame(shuffle_summaries)
    shuffle_df.to_csv("out_shuffle.csv", index=False)
    results["shuffle_oos_net_pf_mean"] = float(shuffle_df["oos_net_pf"].mean())
    results["shuffle_oos_net_pf_median"] = float(shuffle_df["oos_net_pf"].median())
    base_oos_net_pf = results["base"]["oos_net_pf"]
    pct_rank = (shuffle_df["oos_net_pf"] < base_oos_net_pf).mean() * 100
    results["base_percentile_vs_shuffle"] = float(pct_rank)
    print(f"\nshuffle 대조군(20회) OOS net_pf 평균={results['shuffle_oos_net_pf_mean']:.3f} "
          f"median={results['shuffle_oos_net_pf_median']:.3f}, base 백분위={pct_rank:.1f}")

    # === 반전 대조군 ===
    rev_trades = run_variant(base_universe, **DEFAULT, reverse=True)
    rev_df = trades_to_df(rev_trades)
    rev_df.to_csv("out_reverse_trades.csv", index=False)
    results["reverse"] = summarize(rev_df)
    print("\n반전 대조군:", json.dumps(results["reverse"], indent=2))
    print("반전 exit_reason 분포:\n", rev_df["exit_reason"].value_counts())
    rev_zero_hold = (rev_df["hold_bars"] <= 1).mean() if len(rev_df) else float("nan")
    fwd_zero_hold = (base_df["hold_bars"] <= 1).mean() if len(base_df) else float("nan")
    results["reverse_hold_le1_frac"] = float(rev_zero_hold)
    results["base_hold_le1_frac"] = float(fwd_zero_hold)
    print(f"hold_bars<=1 비율: 반전={rev_zero_hold:.4f} 정방향={fwd_zero_hold:.4f}")

    # 제3의 대안: 반전 + 무효화 비활성
    rev_noinval_trades = run_variant(base_universe, **DEFAULT, reverse=True, disable_invalidation=True)
    rev_noinval_df = trades_to_df(rev_noinval_trades)
    rev_noinval_df.to_csv("out_reverse_noinval_trades.csv", index=False)
    results["reverse_no_invalidation"] = summarize(rev_noinval_df)
    print("\n반전(무효화 비활성):", json.dumps(results["reverse_no_invalidation"], indent=2))

    # === LOO(종목별 제외) ===
    loo_rows = []
    for excl in SYMBOLS:
        sub = base_df[base_df["symbol"] != excl]
        s = summarize(sub)
        s["excluded"] = excl
        loo_rows.append(s)
        print(f"LOO 제외={excl}: n_oos={s['n_oos']} OOS net_pf={s['oos_net_pf']:.3f} t={s['oos_net_t']:.2f}" if s['n_oos'] else f"LOO 제외={excl}: n_oos=0")
    pd.DataFrame(loo_rows).to_csv("out_loo.csv", index=False)

    # === top-N 제거 ===
    is_df, oos_df, full_df = split_is_oos(base_df)
    topn_rows = []
    for n in [1, 3, 5, 10]:
        if len(oos_df) > n:
            sorted_oos = oos_df.sort_values("net_R", ascending=False)
            trimmed = sorted_oos.iloc[n:]
            topn_rows.append({"n_removed": n, "oos_net_pf_after": pf_r(trimmed["net_R"]),
                               "oos_net_pf_before": pf_r(oos_df["net_R"])})
    pd.DataFrame(topn_rows).to_csv("out_topn.csv", index=False)
    print("\ntop-N 제거:", topn_rows)

    # === de-clustering: 캘린더일 / 3~5일 롤링 ===
    for name, sub in [("full", full_df), ("is", is_df), ("oos", oos_df)]:
        if len(sub) == 0:
            continue
        daily_net = declustered_daily(sub, "net_R")
        daily_gross = declustered_daily(sub, "gross_R")
        roll3_net = declustered_rolling(sub, "net_R", 3)
        roll5_net = declustered_rolling(sub, "net_R", 5)
        roll3_gross = declustered_rolling(sub, "gross_R", 3)
        roll5_gross = declustered_rolling(sub, "gross_R", 5)
        results[f"declus_{name}"] = {
            "n_trade": len(sub),
            "n_unique_day": len(daily_net),
            "n_roll3": len(roll3_net),
            "n_roll5": len(roll5_net),
            "daily_net_pf": pf_r(daily_net), "daily_net_t": t_stat(daily_net),
            "daily_gross_pf": pf_r(daily_gross), "daily_gross_t": t_stat(daily_gross),
            "roll3_net_pf": pf_r(roll3_net), "roll3_net_t": t_stat(roll3_net),
            "roll5_net_pf": pf_r(roll5_net), "roll5_net_t": t_stat(roll5_net),
            "roll3_gross_pf": pf_r(roll3_gross), "roll3_gross_t": t_stat(roll3_gross),
            "roll5_gross_pf": pf_r(roll5_gross), "roll5_gross_t": t_stat(roll5_gross),
        }
        print(f"\nde-clustering[{name}] n_trade={len(sub)} n_unique_day={len(daily_net)} "
              f"n_roll5={len(roll5_net)}")
        print(f"  일단위 net_pf={pf_r(daily_net):.3f} t={t_stat(daily_net):.2f} | "
              f"gross_pf={pf_r(daily_gross):.3f} t={t_stat(daily_gross):.2f}")
        print(f"  5일롤링 net_pf={pf_r(roll5_net):.3f} t={t_stat(roll5_net):.2f} | "
              f"gross_pf={pf_r(roll5_gross):.3f} t={t_stat(roll5_gross):.2f}")

    # === 동시진입 클러스터 점검(같은 캘린더일, 3~5일 롤링) ===
    if len(full_df):
        same_day = full_df.groupby(full_df["entry_time"].dt.date)["symbol"].nunique()
        results["max_symbols_same_day"] = int(same_day.max())
        results["frac_days_multi_symbol"] = float((same_day > 1).mean())
        print(f"\n같은 캘린더일 동시진입: 최대 {same_day.max()}종목, "
              f"다종목 동시진입일 비율={((same_day > 1).mean()):.3f} (n_days={len(same_day)})")

    with open("out_sweep_summary.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\n저장 완료: out_sweep_summary.json")


if __name__ == "__main__":
    main()
