"""LOO(종목별 제외) · top-N 트레이드 제거 · 파라미터 스윕(10변형+) · 셔플대조군 100회."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import pf_r, t_stat, SYMBOLS
from engine import build_frame, find_signals, simulate_trades, trades_to_df, load_all, run_variant


def summarize(r: pd.Series) -> dict:
    if len(r) < 2:
        return {"n": int(len(r)), "pf": float("nan"), "t": float("nan")}
    return {"n": int(len(r)), "pf": pf_r(r), "t": t_stat(r), "mean": float(r.mean())}


def oos_slice(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["entry_time"] >= "2024-07-01") & (df["entry_time"] <= "2026-06-30 23:59:59")]


def main() -> None:
    univ = load_all()
    base_trades = run_variant(univ)
    base_df = trades_to_df(base_trades)
    base_oos = oos_slice(base_df)

    out = {}

    # === LOO ===
    loo = {}
    for excl in SYMBOLS:
        sub_univ = {s: f for s, f in univ.items() if s != excl}
        tr = run_variant(sub_univ)
        d = trades_to_df(tr)
        loo[excl] = summarize(oos_slice(d)["net_R"]) if len(d) else {"n": 0}
    out["loo_exclude"] = loo

    # === top-N 제거(OOS, net_R 기준 상위 N건 제거) ===
    topn = {}
    sorted_oos = base_oos.sort_values("net_R", ascending=False)
    for n in [1, 3, 5, 10]:
        rest = sorted_oos.iloc[n:]
        topn[f"top{n}_removed"] = summarize(rest["net_R"])
    out["top_n_removed"] = topn

    # === 파라미터 스윕 ===
    sweep_results = []
    sweep_grid = [
        {"baseline_window": 40}, {"baseline_window": 90},
        {"cusum_k": 0.3}, {"cusum_k": 0.8},
        {"cusum_h": 3.0}, {"cusum_h": 6.0},
        {"stop_mult": 1.0}, {"stop_mult": 2.0},
        {"atr_trail_mult": 2.0}, {"atr_trail_mult": 4.0},
        {"max_hold_bars": 30}, {"max_hold_bars": 60},
        {"ema_fast": 10, "ema_slow": 30},
    ]
    for params in sweep_grid:
        bw = params.get("baseline_window", 60)
        ck = params.get("cusum_k", 0.5)
        ch = params.get("cusum_h", 4.0)
        ef = params.get("ema_fast", 20)
        es = params.get("ema_slow", 60)
        sm = params.get("stop_mult", 1.5)
        atm = params.get("atr_trail_mult", 3.0)
        mhb = params.get("max_hold_bars", 45)

        if bw != 60 or ck != 0.5 or ch != 4.0 or ef != 20 or es != 60:
            u2 = load_all(baseline_window=bw, cusum_k=ck, cusum_h=ch, ema_fast=ef, ema_slow=es)
        else:
            u2 = univ
        tr = run_variant(u2, stop_mult=sm, atr_trail_mult=atm, max_hold_bars=mhb)
        d = trades_to_df(tr)
        s = summarize(oos_slice(d)["net_R"]) if len(d) else {"n": 0}
        sweep_results.append({"params": params, **s})
    out["param_sweep"] = sweep_results

    # === 셔플/순열 대조군 100회(부호 무작위화 — direction 무작위 재배정, 진입/청산 구조는 유지) ===
    rng = np.random.default_rng(42)
    real_mean = base_oos["net_R"].mean()
    perm_means = []
    for _ in range(100):
        signs = rng.choice([1, -1], size=len(base_oos))
        # gross_R/net_R 은 trade_dir 에 따라 부호가 결정되므로 근사: R을 |R|로 만들고 무작위부호 재부여
        shuffled = base_oos["net_R"].abs().to_numpy() * signs
        # 원 net_R 부호와 비용 비대칭을 근사 보존하려면 cost 성분을 감안해야 하나, 표준 관행대로
        # 단순 부호 무작위화(50/50)를 사용(부호가 무작위였다면 이 정도 평균이 나온다는 벤치마크)
        perm_means.append(float(np.mean(shuffled)))
    perm_means = np.array(perm_means)
    percentile = float((perm_means < real_mean).mean() * 100)
    out["sign_shuffle_100"] = {
        "real_mean_R": float(real_mean), "perm_mean_avg": float(perm_means.mean()),
        "perm_mean_std": float(perm_means.std()), "real_percentile": percentile,
    }

    with open("out_diag_robust.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
