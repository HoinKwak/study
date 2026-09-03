"""부트스트랩(대조군 비교, base⊆pool 중첩점검, 폐기조건 e/f 검증) + de-clustering(net/gross 병행,
캘린더일+3/4/5일롤링) + LOO + top-N + 셔플(부호무작위 100회 + 승률고정 순열검정)."""
from __future__ import annotations
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import ibs_ctrl
import stats_utils as su


def build_all_signals():
    cfg0 = engine.RunConfig()
    return {sym: engine.build_signals(sym, cfg0) for sym in common.SYMBOLS}


def get_trades_df(sigs, cfg, rcol):
    trades_all = []
    for sym, sig in sigs.items():
        trades_all.extend(engine.run_symbol(sym, sig, cfg))
    return su.trades_df(trades_all, rcol=rcol)


def win_rate_fixed_permutation(df: pd.DataFrame, n_perm: int = 2000, seed: int = 17) -> dict:
    """승률 고정 순열검정: 실제 승/패 여부(부호)는 그대로 두고, 승리분/패배분 R크기를 서로
    무작위로 재배정(승-패 결합 안 바뀜)해 실제 mean(R)의 백분위 산출. 승률<50%인 전략에서
    부호 무작위화가 과장된 극단치를 주는 문제를 우회."""
    if df.empty:
        return dict(pctile=float("nan"))
    r = df["r"].to_numpy()
    wins = r[r > 0]
    losses = r[r <= 0]
    n = len(r)
    rng = np.random.default_rng(seed)
    means = np.empty(n_perm)
    for i in range(n_perm):
        signs = rng.random(n) < (len(wins) / n if n else 0.5)
        sample = np.empty(n)
        n_w = signs.sum()
        n_l = n - n_w
        sample[signs] = rng.choice(wins, size=n_w, replace=True) if n_w and len(wins) else 0.0
        sample[~signs] = rng.choice(losses, size=n_l, replace=True) if n_l and len(losses) else 0.0
        means[i] = sample.mean()
    real_mean = r.mean()
    pctile = float((means <= real_mean).mean() * 100)
    return dict(pctile=pctile, real_mean=float(real_mean), perm_mean=float(means.mean()),
               n_perm=n_perm, win_rate=len(wins) / n if n else float("nan"))


if __name__ == "__main__":
    t0 = time.time()
    sigs = build_all_signals()

    cfg_base = engine.RunConfig(signal_mode="all3", direction_mode="normal", cost_on=True)
    cfg_c1 = engine.RunConfig(signal_mode="15m_only", direction_mode="normal", cost_on=True)
    cfg_c2 = engine.RunConfig(signal_mode="two_tf", direction_mode="normal", cost_on=True)
    cfg_c3 = engine.RunConfig(signal_mode="no_gate", direction_mode="normal", cost_on=True)
    cfg_rev = engine.RunConfig(signal_mode="all3", direction_mode="reverse", cost_on=True)

    df_base = get_trades_df(sigs, cfg_base, "r_net")
    df_c1 = get_trades_df(sigs, cfg_c1, "r_net")
    df_c2 = get_trades_df(sigs, cfg_c2, "r_net")
    df_c3 = get_trades_df(sigs, cfg_c3, "r_net")
    df_rev = get_trades_df(sigs, cfg_rev, "r_net")

    _, oos_base, _ = su.split_is_oos(df_base)
    _, oos_c1, _ = su.split_is_oos(df_c1)
    _, oos_c2, _ = su.split_is_oos(df_c2)
    _, oos_c3, _ = su.split_is_oos(df_c3)
    _, oos_rev, _ = su.split_is_oos(df_rev)

    print("=== 사전 등록 폐기조건 (c) 성격 확인용: base vs 대조군3종 부트스트랩(matched-n, 5000회) ===")
    for lbl, ctrl_df in [("ctrl_15m단독", oos_c1), ("ctrl_두TF", oos_c2), ("ctrl_게이트없음", oos_c3)]:
        res = su.bootstrap_matched_n_diff(ctrl_df["r"].to_numpy(), oos_base["r"].to_numpy())
        print(f"base vs {lbl}: base백분위={res['pctile']:.1f} base_mean={res['base_mean']:.4f} "
              f"pool_dist_mean={res['pool_dist_mean']:.4f} n={res['n']}")
        res2 = su.bootstrap_diff_indep(oos_base["r"].to_numpy(), ctrl_df["r"].to_numpy())
        print(f"  독립표본 부트스트랩 P(base<=ctrl)={res2['p_a_le_b']:.4f} "
              f"(mean_base={res2['mean_a']:.4f} mean_ctrl={res2['mean_b']:.4f})")

    print("\n=== 폐기조건 (e): base vs ctrl_15m단독 트레이드 집합 중복률 + 성과차 ===")
    ov = pd.merge(oos_base[["symbol", "entry_time"]], oos_c1[["symbol", "entry_time"]],
                  on=["symbol", "entry_time"], how="inner")
    print(f"base n={len(oos_base)}, ctrl_15m단독 n={len(oos_c1)}, 중첩(base 기준)={len(ov)} "
          f"({len(ov)/len(oos_base)*100:.1f}% of base)")
    base_only = pd.merge(oos_base[["symbol", "entry_time", "r"]],
                         oos_c1[["symbol", "entry_time"]], on=["symbol", "entry_time"],
                         how="left", indicator=True)
    base_non_overlap = base_only[base_only["_merge"] == "left_only"]
    print(f"base 비중첩 잔여분(멀티TF만의 고유 트레이드) n={len(base_non_overlap)} "
          f"mean(R)={base_non_overlap['r'].mean():.4f}" if len(base_non_overlap) else "base 비중첩 잔여분 없음(완전포함)")
    print(f"base 전체 mean(R)={oos_base['r'].mean():.4f}  ctrl_15m단독 전체 mean(R)={oos_c1['r'].mean():.4f}")
    print(f"base ⊆ ctrl_15m단독(15m단독 필터 완화판이 base 를 포함) 여부 = "
          f"{len(ov) == len(oos_base)}")

    print("\n=== 폐기조건 (f): base(정방향) vs reverse 부트스트랩 비교 ===")
    res_rev = su.bootstrap_diff_indep(oos_base["r"].to_numpy(), oos_rev["r"].to_numpy())
    print(f"P(정방향<=반전)={res_rev['p_a_le_b']:.4f} (mean_정방향={res_rev['mean_a']:.4f} "
          f"mean_반전={res_rev['mean_b']:.4f})")
    # gross 버전도 병행
    cfg_base_g = engine.RunConfig(signal_mode="all3", direction_mode="normal", cost_on=False)
    cfg_rev_g = engine.RunConfig(signal_mode="all3", direction_mode="reverse", cost_on=False)
    df_base_g = get_trades_df(sigs, cfg_base_g, "r_gross")
    df_rev_g = get_trades_df(sigs, cfg_rev_g, "r_gross")
    _, oos_base_g, _ = su.split_is_oos(df_base_g)
    _, oos_rev_g, _ = su.split_is_oos(df_rev_g)
    res_rev_g = su.bootstrap_diff_indep(oos_base_g["r"].to_numpy(), oos_rev_g["r"].to_numpy())
    print(f"[gross] P(정방향<=반전)={res_rev_g['p_a_le_b']:.4f} (mean_정방향={res_rev_g['mean_a']:.4f} "
          f"mean_반전={res_rev_g['mean_b']:.4f})")

    print("\n=== de-clustering(캘린더일 + 3~5일 롤링, net) — base OOS ===")
    for label, fn in [("원본", lambda d: d),
                      ("캘린더일", su.decluster_calendar_day),
                      ("3일롤링", lambda d: su.decluster_rolling_days(d, 3)),
                      ("4일롤링", lambda d: su.decluster_rolling_days(d, 4)),
                      ("5일롤링", lambda d: su.decluster_rolling_days(d, 5))]:
        d = fn(oos_base)
        print(su.fmt(su.summary(d, f"net {label}")))

    print("\n=== de-clustering(gross, cost_on=False) — base OOS ===")
    for label, fn in [("원본", lambda d: d),
                      ("캘린더일", su.decluster_calendar_day),
                      ("3일롤링", lambda d: su.decluster_rolling_days(d, 3)),
                      ("4일롤링", lambda d: su.decluster_rolling_days(d, 4)),
                      ("5일롤링", lambda d: su.decluster_rolling_days(d, 5))]:
        d = fn(oos_base_g)
        print(su.fmt(su.summary(d, f"gross {label}")))

    print("\n=== de-clustering(gross, reverse) — OOS (폐기조건 f gross 근거 병행 검증) ===")
    for label, fn in [("원본", lambda d: d),
                      ("캘린더일", su.decluster_calendar_day),
                      ("3일롤링", lambda d: su.decluster_rolling_days(d, 3)),
                      ("5일롤링", lambda d: su.decluster_rolling_days(d, 5))]:
        d = fn(oos_rev_g)
        print(su.fmt(su.summary(d, f"reverse gross {label}")))

    print("\n=== LOO(종목 제외) — base OOS net ===")
    for excl in common.SYMBOLS:
        d = oos_base[oos_base["symbol"] != excl]
        print(su.fmt(su.summary(d, f"제외={excl}")))

    print("\n=== top-N 대칭 제거 — base OOS net ===")
    sorted_r = oos_base.sort_values("r")
    for n in [1, 3, 5, 10, 20, int(len(oos_base) * 0.05)]:
        worst_removed = sorted_r.iloc[n:]
        best_removed = sorted_r.iloc[:-n]
        print(su.fmt(su.summary(best_removed, f"최대이익top{n}제거")))
        print(su.fmt(su.summary(worst_removed, f"최대손실top{n}제거")))

    print("\n=== 셔플(부호 무작위화, 100회) — base OOS net ===")
    res = su.sign_shuffle_test(oos_base, n_shuffle=100)
    print(f"실제mean(R)={res['real_mean']:.4f} 셔플평균={res['shuffle_mean']:.4f} "
          f"백분위={res['pctile']:.1f}")

    print("\n=== 승률고정 순열검정(2000회) — base OOS net (승률<50%이므로 병행) ===")
    res2 = win_rate_fixed_permutation(oos_base, n_perm=2000)
    print(f"실제mean(R)={res2['real_mean']:.4f} 순열평균={res2['perm_mean']:.4f} "
          f"백분위={res2['pctile']:.1f} 승률={res2['win_rate']*100:.1f}%")

    print(f"\nTOTAL TIME {time.time()-t0:.1f}s")
