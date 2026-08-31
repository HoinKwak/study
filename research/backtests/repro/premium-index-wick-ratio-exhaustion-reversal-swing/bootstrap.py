"""③ 게이트 대조군 표본수 맞춘 부트스트랩(100회) + base⊆pool 독립검정
   ④ 정보원 무력화(wick_asym 셔플) 대조군 100회 — 결합 트리거 표본크기 변화 확인."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from scipy import stats

from common import IS_END, IS_START, OOS_END, OOS_START, SYMBOLS
from engine import (build_frame, load_all, run_variant, simulate_trade, split_is_oos,
                     trades_to_df)

DEFAULT = dict(atr_sl_mult=1.4, atr_trail_mult=2.2, max_hold_bars=30)
RNG = np.random.default_rng(20260831)


def pf_r(series) -> float:
    series = pd.Series(series)
    pos = series[series > 0].sum()
    neg = -series[series < 0].sum()
    if neg == 0:
        return float("inf") if pos > 0 else float("nan")
    return pos / neg


def t_stat(series) -> float:
    series = pd.Series(series)
    n = len(series)
    if n < 2:
        return float("nan")
    sd = series.std(ddof=1)
    if sd == 0:
        return float("nan")
    return series.mean() / (sd / np.sqrt(n))


def get_oos(df: pd.DataFrame) -> pd.DataFrame:
    _, oos, _ = split_is_oos(df, IS_START, IS_END, OOS_START, OOS_END)
    return oos


def main() -> None:
    print("데이터 로딩...")
    universe = load_all()

    base_trades = run_variant(universe, **DEFAULT, gate="full")
    base_df = trades_to_df(base_trades)
    base_oos = get_oos(base_df)
    base_mean_r = base_oos["net_R"].mean()
    base_pf = pf_r(base_oos["net_R"])
    print(f"base OOS n={len(base_oos)} mean_net_R={base_mean_r:.4f} PF={base_pf:.3f}")

    results = {}

    # ---------------- 게이트 대조군 부트스트랩 ----------------
    for gate in ["no_gate", "no_ext", "no_premium_sign"]:
        pool_trades = run_variant(universe, **DEFAULT, gate=gate)
        pool_df = trades_to_df(pool_trades)
        pool_oos = get_oos(pool_df)
        print(f"\n[{gate}] pool OOS n={len(pool_oos)}")

        # base ⊆ pool 여부(entry_time,symbol,direction 키로 부분집합 확인)
        base_keys = set(zip(base_oos["symbol"], base_oos["entry_time"], base_oos["direction"]))
        pool_keys = set(zip(pool_oos["symbol"], pool_oos["entry_time"], pool_oos["direction"]))
        overlap = len(base_keys & pool_keys)
        is_subset = base_keys <= pool_keys
        print(f"  base⊆pool: {is_subset} (overlap {overlap}/{len(base_keys)})")

        # 표본수 맞춘 부트스트랩(복원추출, n=len(base_oos), 100회)
        n = len(base_oos)
        boot_means, boot_pfs = [], []
        if len(pool_oos) >= 5 and n >= 5:
            vals = pool_oos["net_R"].to_numpy()
            for _ in range(100):
                samp = RNG.choice(vals, size=n, replace=True)
                boot_means.append(samp.mean())
                boot_pfs.append(pf_r(samp))
            pctile = float((np.array(boot_means) < base_mean_r).mean() * 100)
        else:
            pctile = float("nan")

        out = {"pool_n_oos": len(pool_oos), "base_subset_of_pool": is_subset,
               "overlap": overlap, "base_percentile_in_bootstrap": pctile,
               "boot_mean_avg": float(np.mean(boot_means)) if boot_means else None,
               "boot_mean_std": float(np.std(boot_means)) if boot_means else None}

        # base ⊆ pool 이면 중복 없는 독립 검정(pool - base) vs base
        if is_subset and overlap > 0:
            resid_mask = ~pool_oos.apply(
                lambda r: (r["symbol"], r["entry_time"], r["direction"]) in base_keys, axis=1)
            resid = pool_oos[resid_mask]
            if len(resid) >= 5:
                tstat, pval = stats.ttest_ind(base_oos["net_R"], resid["net_R"], equal_var=False)
                out["independent_welch"] = {
                    "resid_n": len(resid), "resid_mean_R": float(resid["net_R"].mean()),
                    "resid_pf": pf_r(resid["net_R"]), "base_mean_R": float(base_mean_r),
                    "welch_t": float(tstat), "welch_p": float(pval),
                }
        results[gate] = out
        print(json.dumps(out, indent=2, default=str))

    # ---------------- 정보원 무력화(wick_asym 셔플) ----------------
    print("\n=== 정보원 무력화(wick_asym 시계열 셔플) 100회 ===")
    shuffle_n = []
    shuffle_mean = []
    shuffle_pf = []
    frames_orig = {}
    for sym in SYMBOLS:
        fr = build_frame(sym)
        fr["_symbol"] = sym
        frames_orig[sym] = fr
    for trial in range(100):
        trial_trades = []
        for sym in SYMBOLS:
            fr_o = frames_orig[sym]
            prem = fr_o["prem"].copy()
            wick_th = fr_o["wick_th"]; lb = fr_o["lookback_bars"]
            min_count = fr_o["min_count"]; ext_th = fr_o["ext_th"]
            wa = prem["wick_asym"].to_numpy()
            valid_mask = np.isfinite(wa)
            wa_shuf = wa.copy()
            perm = RNG.permutation(np.where(valid_mask)[0])
            wa_shuf[valid_mask] = wa[perm]
            is_upper = (wa_shuf >= wick_th).astype(float)
            is_lower = (wa_shuf <= -wick_th).astype(float)
            cu = pd.Series(is_upper, index=prem.index).rolling(lb, min_periods=lb).sum().to_numpy()
            cl = pd.Series(is_lower, index=prem.index).rolling(lb, min_periods=lb).sum().to_numpy()
            pc = prem["premium_close"].to_numpy()
            ext = prem["ext_pct"].to_numpy()
            idx = prem.index
            for i in range(len(prem)):
                if not np.isfinite(cu[i]) or not np.isfinite(ext[i]):
                    continue
                if cu[i] >= min_count and pc[i] > 0 and ext[i] >= ext_th:
                    tr = simulate_trade(fr_o, idx[i], -1, int(cu[i]), float(pc[i]), float(ext[i]),
                                        DEFAULT["atr_sl_mult"], DEFAULT["atr_trail_mult"],
                                        DEFAULT["max_hold_bars"])
                    if tr is not None:
                        trial_trades.append(tr)
                elif cl[i] >= min_count and pc[i] < 0 and ext[i] <= -ext_th:
                    tr = simulate_trade(fr_o, idx[i], 1, int(cl[i]), float(pc[i]), float(ext[i]),
                                        DEFAULT["atr_sl_mult"], DEFAULT["atr_trail_mult"],
                                        DEFAULT["max_hold_bars"])
                    if tr is not None:
                        trial_trades.append(tr)
        tdf = trades_to_df(trial_trades)
        oos = get_oos(tdf)
        shuffle_n.append(len(oos))
        if len(oos) >= 2:
            shuffle_mean.append(oos["net_R"].mean())
            shuffle_pf.append(pf_r(oos["net_R"]))

    shuffle_n_arr = np.array(shuffle_n)
    base_n = len(base_oos)
    print(f"base OOS n={base_n}, shuffle OOS n 평균={shuffle_n_arr.mean():.1f} "
          f"(범위 {shuffle_n_arr.min()}~{shuffle_n_arr.max()}, "
          f"표본크기 변화율={100*(shuffle_n_arr.mean()-base_n)/base_n:.1f}%)")
    if shuffle_mean:
        pctile_shuf = float((np.array(shuffle_mean) < base_mean_r).mean() * 100)
        print(f"base 평균 net_R({base_mean_r:.4f})의 셔플분포 내 백분위: {pctile_shuf:.1f}")
    else:
        pctile_shuf = float("nan")

    results["shuffle_control"] = {
        "base_n_oos": base_n, "shuffle_n_mean": float(shuffle_n_arr.mean()),
        "shuffle_n_min": int(shuffle_n_arr.min()), "shuffle_n_max": int(shuffle_n_arr.max()),
        "n_change_pct": float(100 * (shuffle_n_arr.mean() - base_n) / base_n),
        "base_mean_net_R": float(base_mean_r),
        "shuffle_mean_net_R_avg": float(np.mean(shuffle_mean)) if shuffle_mean else None,
        "base_percentile_in_shuffle": pctile_shuf,
    }

    with open("out_bootstrap.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\n완료 — out_bootstrap.json 저장")


if __name__ == "__main__":
    main()
