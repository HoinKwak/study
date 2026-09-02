"""LOO·top-N·de-clustering(양방향)·파라미터 스윕·부트스트랩(게이트 부가가치, base⊆pool 비중첩
독립검정)·부호셔플(100회)·승률고정 순열검정·꼬리상관(위기구간) 진단.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sstats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su

OUT = common.SP / "out"


def load(name: str, tag: str) -> pd.DataFrame:
    p = OUT / f"trades_{name}_{tag}.csv"
    d = pd.read_csv(p, parse_dates=["entry_time", "exit_time"])
    for c in ("entry_time", "exit_time"):
        d[c] = pd.to_datetime(d[c], utc=True)
    d["r"] = d["r_net"] if tag == "net" else d["r_gross"]
    return d


def oos(d: pd.DataFrame) -> pd.DataFrame:
    return d[(d["entry_time"] >= common.OOS_START) & (d["entry_time"] <= common.OOS_END)]


def is_(d: pd.DataFrame) -> pd.DataFrame:
    return d[(d["entry_time"] >= common.IS_START) & (d["entry_time"] <= common.IS_END)]


# --------------------------------------------------------------- LOO / top-N

def loo(d: pd.DataFrame, label: str) -> None:
    print(f"\n--- LOO(종목 하나씩 제외) OOS — {label} ---")
    o = oos(d)
    print("   " + su.fmt(su.summary(o, "전체")))
    for sym in common.SYMBOLS:
        sub = o[o["symbol"] != sym]
        print("   " + su.fmt(su.summary(sub, f"제외={sym}")))


def top_n_removed(d: pd.DataFrame, label: str) -> None:
    print(f"\n--- top-N 승리 트레이드 제거 OOS — {label} ---")
    o = oos(d).sort_values("r", ascending=False).reset_index(drop=True)
    for n in (0, 5, 10, 20):
        sub = o.iloc[n:]
        print("   " + su.fmt(su.summary(sub, f"top-{n} 제거")))


def worst_cluster_symmetric(d: pd.DataFrame, label: str) -> None:
    print(f"\n--- 최악 5일 롤링 클러스터 제거 대칭점검 OOS — {label} ---")
    o = oos(d).copy()
    if o.empty:
        print("   표본 없음")
        return
    agg = su.decluster_rolling_days(o, window_days=5)
    if agg.empty:
        print("   표본 없음")
        return
    agg = agg.sort_values("r")
    worst3 = set(agg.index[:3])
    best3 = set(agg.index[-3:])
    total_r = o["r"].sum()
    print(f"   전체 클러스터수={len(agg)}, OOS 순 R 합={total_r:+.2f}")
    worst_share = -agg.loc[list(worst3), "r"].sum() * agg.loc[list(worst3), "n"].mean() \
        if len(worst3) else 0.0
    # 클러스터 손익 기여도(단순 클러스터 r*n 합)로 근사 표기
    contrib = (agg["r"] * agg["n"])
    print(f"   최악 3개 클러스터 손익기여 합={contrib.loc[list(worst3)].sum():+.2f}"
         f" / 최고 3개={contrib.loc[list(best3)].sum():+.2f} / 전체={contrib.sum():+.2f}")
    # 최악 3개 제외 재계산(트레이드 단위로 근사: 해당 클러스터 대표시각 인근 트레이드 제거)
    # decluster_rolling_days 는 클러스터별 평균만 반환하므로, 원 트레이드에 클러스터ID 재부여해 검증
    dd = o.sort_values("entry_time").reset_index(drop=True)
    cluster_id, cur_id, last_time = [], 0, None
    for t in dd["entry_time"]:
        if last_time is None or (t - last_time) > pd.Timedelta(days=5):
            cur_id += 1
        cluster_id.append(cur_id)
        last_time = t
    dd["cluster"] = cluster_id
    # cluster id -> agg row 매핑(순서 동일)
    id_map = {i + 1: idx for i, idx in enumerate(agg.index)}
    dd["agg_idx"] = dd["cluster"].map(id_map)
    excl_worst = dd[~dd["agg_idx"].isin(worst3)]
    excl_best = dd[~dd["agg_idx"].isin(best3)]
    print("   " + su.fmt(su.summary(excl_worst, "최악3 클러스터 제외")))
    print("   " + su.fmt(su.summary(excl_best, "최고3 클러스터 제외(대칭점검)")))


# --------------------------------------------------------------- de-clustering

def decluster_report(d: pd.DataFrame, label: str) -> None:
    print(f"\n--- de-clustering(캘린더일 단위) OOS — {label} ---")
    o = oos(d)
    print("   " + su.fmt(su.summary(o, "트레이드 단위")))
    cal = su.decluster_calendar_day(o)
    t, p, n = su.t_stat(cal)
    print(f"   캘린더일 단위: n(고유일)={n} mean(R)={cal['r'].mean() if n else float('nan'):+.4f}"
         f" t={t:+.3f} p={p:.4f}")
    roll = su.decluster_rolling_days(o, window_days=5)
    t2, p2, n2 = su.t_stat(roll)
    print(f"   5일 롤링클러스터 단위: n(클러스터)={n2} "
         f"mean(R)={roll['r'].mean() if n2 else float('nan'):+.4f} t={t2:+.3f} p={p2:.4f}")


# --------------------------------------------------------------- 부트스트랩(게이트 부가가치)

def gate_value_bootstrap() -> None:
    print("\n=== 게이트 부가가치 부트스트랩(표본수 맞춤) — OOS net ===")
    base = oos(load("base_gated", "net"))
    always_mr = oos(load("always_mr", "net"))
    always_mom = oos(load("always_mom", "net"))
    no_gate = oos(load("no_gate_both", "net"))

    for ctrl_name, ctrl in [("always_mr", always_mr), ("always_mom", always_mom),
                            ("no_gate_both", no_gate)]:
        res = su.bootstrap_diff_indep(base["r"].to_numpy(), ctrl["r"].to_numpy())
        print(f"   base_gated vs {ctrl_name}: mean_base={res['mean_a']:+.4f} "
             f"mean_ctrl={res['mean_b']:+.4f} P(base<=ctrl)={res['p_a_le_b']:.4f} "
             f"(n_base={len(base)}, n_ctrl={len(ctrl)})")

    # base ⊆ no_gate_both 비중첩 독립 Welch
    base_keys = set(zip(base["symbol"], base["mode"], base["entry_idx"]))
    pool_keys = set(zip(no_gate["symbol"], no_gate["mode"], no_gate["entry_idx"]))
    overlap = base_keys & pool_keys
    pool_only_mask = [(s, m, i) not in base_keys
                      for s, m, i in zip(no_gate["symbol"], no_gate["mode"], no_gate["entry_idx"])]
    pool_only = no_gate[pool_only_mask]
    print(f"\n   base⊆no_gate_both 중첩: base n={len(base_keys)} pool n={len(pool_keys)} "
         f"overlap={len(overlap)} ({100*len(overlap)/max(1,len(base_keys)):.1f}% of base)")
    if len(pool_only) >= 5 and len(base) >= 5:
        tw, pw = sstats.ttest_ind(base["r"], pool_only["r"], equal_var=False)
        print(f"   비중첩(pool_only, n={len(pool_only)}) vs base(n={len(base)}) Welch: "
             f"t={tw:+.3f} p={pw:.4f} mean_base={base['r'].mean():+.4f} "
             f"mean_pool_only={pool_only['r'].mean():+.4f}")
    else:
        print(f"   비중첩 표본 부족(pool_only n={len(pool_only)}) — 독립검정 생략")


# --------------------------------------------------------------- 셔플/순열검정

def shuffle_tests(d: pd.DataFrame, label: str) -> None:
    o = oos(d)
    print(f"\n--- 셔플 검정(100회) OOS — {label} (n={len(o)}) ---")
    if len(o) < 5:
        print("   표본부족")
        return
    res = su.sign_shuffle_test(o, n_shuffle=100)
    print(f"   부호(50/50) 셔플: 백분위={res['pctile']:.1f} real_mean={res['real_mean']:+.4f} "
         f"shuffle_mean={res['shuffle_mean']:+.4f}")
    win_rate = (o["r"] > 0).mean()
    rng = np.random.default_rng(9)
    r = o["r"].to_numpy()
    abs_r = np.abs(r)
    n = len(r)
    means = np.empty(100)
    for i in range(100):
        signs = np.where(rng.random(n) < win_rate, 1.0, -1.0)
        means[i] = (abs_r * signs).mean()
    real_mean = r.mean()
    pctile = float((means <= real_mean).mean() * 100)
    print(f"   승률고정({win_rate*100:.1f}%) 순열검정: 백분위={pctile:.1f} "
         f"real_mean={real_mean:+.4f} perm_mean={means.mean():+.4f}")


# --------------------------------------------------------------- 파라미터 스윕

SWEEP_PARAMS = [
    ("rho_th", 0.10), ("rho_th", 0.25),
    ("k", 2), ("k", 5),
    ("ext_mult", 1.0), ("ext_mult", 2.0),
    ("donchian_n", 15), ("donchian_n", 30),
    ("vol_mult", 1.2), ("vol_mult", 2.0),
    ("sl_mult", 0.8), ("sl_mult", 1.3),
    ("trail_mult", 1.2), ("trail_mult", 2.0),
]


def sweep() -> None:
    print("\n=== 파라미터 스윕(1개씩 변경, gated 베이스, OOS net) ===")
    base_kw = dict(signal_mode="gated", direction_mode="normal", cost_on=True)
    for pname, pval in SWEEP_PARAMS:
        kw = dict(base_kw)
        kw[pname] = pval
        cfg = engine.RunConfig(**kw)
        sigs = engine.load_all_signals(common.SYMBOLS, cfg)
        trades = engine.run_all(sigs, cfg)
        all_trades = [t for tl in trades.values() for t in tl]
        df = su.trades_df(all_trades, rcol="r_net")
        o = oos(df)
        s = su.summary(o, f"{pname}={pval}")
        print("   " + su.fmt(s))


# --------------------------------------------------------------- 꼬리상관(위기구간)

CRISIS_WINDOWS = [
    ("2024-08-01", "2024-08-10", "2024-08 엔캐리 청산"),
    ("2025-02-01", "2025-02-10", "2025-02 Bybit 해킹"),
]


def tail_correlation() -> None:
    print("\n=== 종목 간 신호 상관 — 평시 vs 위기구간(진입일 이진 지표) ===")
    base = load("base_gated", "net")
    base["entry_day"] = base["entry_time"].dt.floor("D")
    # 종목 x 일자 진입여부 피벗
    days = pd.date_range(common.IS_START.floor("D"), common.OOS_END.floor("D"), freq="D", tz="UTC")
    mat = pd.DataFrame(0, index=days, columns=common.SYMBOLS)
    for _, row in base.iterrows():
        if row["entry_day"] in mat.index:
            mat.loc[row["entry_day"], row["symbol"]] = 1
    full_corr = mat.corr().to_numpy()
    iu = np.triu_indices(len(common.SYMBOLS), k=1)
    print(f"   평시(전체기간) 종목쌍 평균 상관: {full_corr[iu].mean():+.4f}")

    for start, end, label in CRISIS_WINDOWS:
        sub = mat.loc[start:end]
        if sub.shape[0] < 3 or sub.sum().sum() == 0:
            print(f"   {label}: 표본부족/무진입")
            continue
        c = sub.corr().to_numpy()
        c = np.nan_to_num(c, nan=0.0)
        print(f"   {label}: 종목쌍 평균 상관={c[iu].mean():+.4f}, 총진입={int(sub.sum().sum())}")

    # 동시진입일(3종목 이상) 비율
    same_day_ge3 = (mat.sum(axis=1) >= 3).sum()
    same_day_ge5 = (mat.sum(axis=1) >= 5).sum()
    print(f"   3종목↑ 동시진입일: {same_day_ge3}일, 5종목↑ 동시진입일: {same_day_ge5}일 "
         f"(전체 {len(days)}일)")


def main() -> None:
    print("############ base_gated (net) ############")
    d_base_net = load("base_gated", "net")
    loo(d_base_net, "base_gated net")
    top_n_removed(d_base_net, "base_gated net")
    worst_cluster_symmetric(d_base_net, "base_gated net")
    decluster_report(d_base_net, "base_gated net")
    shuffle_tests(d_base_net, "base_gated net")

    print("\n############ base_gated (gross, de-clustering 병행) ############")
    d_base_gross = load("base_gated", "gross")
    decluster_report(d_base_gross, "base_gated gross")

    print("\n############ 서브모드별 (base_gated net) ############")
    for mode in ("MR", "MOM"):
        sub = d_base_net[d_base_net["mode"] == mode]
        print(f"\n--- {mode} 서브모드 ---")
        loo(sub, f"base_gated/{mode} net")
        decluster_report(sub, f"base_gated/{mode} net")

    print("\n############ base_gated_reverse (net) ############")
    d_rev = load("base_gated_reverse", "net")
    print("   " + su.fmt(su.summary(oos(d_rev), "reverse OOS")))
    for mode in ("MR", "MOM"):
        sub = d_rev[d_rev["mode"] == mode]
        print("   " + su.fmt(su.summary(oos(sub), f"reverse/{mode} OOS")))
        rc = sub["reason"].value_counts(normalize=True) if len(sub) else pd.Series(dtype=float)
        hb = sub["holding_bars"].describe() if len(sub) else None
        print(f"      청산사유분포: {dict(rc.round(3))}")
        if hb is not None:
            print(f"      holding_bars: mean={hb['mean']:.2f} median={sub['holding_bars'].median():.1f}"
                 f" zero_frac={(sub['holding_bars']==0).mean()*100:.1f}%")

    print("\n############ 무조건부 대조군 3종 (net, OOS) ############")
    for name in ("always_mr", "always_mom", "no_gate_both"):
        d = load(name, "net")
        print(f"\n--- {name} ---")
        print("   " + su.fmt(su.summary(oos(d), f"{name} OOS")))

    gate_value_bootstrap()
    sweep()
    tail_correlation()


if __name__ == "__main__":
    main()
