"""[단타] 글로벌 vs 탑트레이더 계정비율 상관 붕괴-재동조 스캘프 — 검증 드라이버.

사용법: python3 gtacrr_run.py <subcommand>
  diag        데이터 품질(결측) + 신호빈도 진단
  main        메인 IS/OOS/FULL (net + gross) PF(R)/t
  controls    핵심 대조군 ①재동조확인 제거 ②15m확인필터 제거 ③플라시보(무작위 타이밍)
  reverse     방향반전 대조군(+ 테제무효화 청산 구조 확인)
  shuffle     방향 부호 무작위화 100회
  declus      de-clustering(캘린더일 + 5일 롤링) + 종목간 동시신호
  loo         leave-one-symbol-out
  topn        top-N 트레이드 제거
  sweep       파라미터 스윕
  gatecheck   롤링 자기백분위 게이트 발화율(정보무관 대조) + 트리거시점 한정 상관
  lookahead   룩어헤드 절단 재실행
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gtacrr_common as c  # noqa: E402
import gtacrr_engine as eng  # noqa: E402
import gtacrr_signals as sig  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "backtests" / "repro" / \
    "global-toptrader-account-ratio-correlation-recoupling-scalp"
OUT.mkdir(parents=True, exist_ok=True)


def _split(trades_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    isd = trades_df[(trades_df.entry_time >= pd.Timestamp(c.IS_START)) &
                    (trades_df.entry_time <= pd.Timestamp(c.IS_END))]
    oosd = trades_df[(trades_df.entry_time >= pd.Timestamp(c.OOS_START)) &
                     (trades_df.entry_time <= pd.Timestamp(c.OOS_END))]
    return {"IS": isd, "OOS": oosd, "FULL": trades_df}


def _summ(sub: pd.DataFrame) -> dict:
    if sub.empty:
        return dict(n=0, pf=float("nan"), t=float("nan"), winrate=float("nan"))
    return dict(n=len(sub), pf=eng.pf_r(sub), t=eng.t_stat(sub),
               winrate=float((sub.r_multiple > 0).mean()))


def build_all_frames(params=None, require_confirm=True, skip_recouple_check=False):
    frames = {}
    for s in c.SYMBOLS:
        frames[s] = sig.build_signal_frame(s, params=params, require_confirm=require_confirm,
                                           skip_recouple_check=skip_recouple_check)
    return frames


def run_trades(frames: dict, params, **engine_kwargs) -> pd.DataFrame:
    all_trades = []
    for s, df in frames.items():
        all_trades += eng.simulate_symbol(s, df, params, **engine_kwargs)
    return eng.trades_to_df(all_trades)


def cmd_diag():
    print("== 데이터 결측 진단 (top_raw=탑트레이더, g_raw=글로벌) ==")
    for s in c.SYMBOLS:
        h = sig.resample_ratio_1h(s)
        h = h[(h.index >= pd.Timestamp(c.IS_START)) & (h.index <= pd.Timestamp(c.OOS_END))]
        by_year = h.groupby(h.index.year).apply(
            lambda d: pd.Series({"n": len(d), "g_nan%": d["g_raw"].isna().mean() * 100,
                                 "top_nan%": d["top_raw"].isna().mean() * 100}))
        print(s)
        print(by_year.to_string())
    print("\n== 신호빈도(파라미터 기본값) ==")
    frames = build_all_frames()
    tot_is = tot_oos = 0
    for s, df in frames.items():
        sigs = df[df["signal"]]
        valid_start = df["pctile"].first_valid_index()
        n_is = ((sigs.index >= pd.Timestamp(c.IS_START)) & (sigs.index <= pd.Timestamp(c.IS_END))).sum()
        n_oos = ((sigs.index >= pd.Timestamp(c.OOS_START)) & (sigs.index <= pd.Timestamp(c.OOS_END))).sum()
        tot_is += n_is; tot_oos += n_oos
        years = (df.index.max() - valid_start).days / 365.25
        print(f"{s}: valid_start={valid_start} n_signal={len(sigs)} "
              f"per_year={len(sigs)/years:.1f} IS={n_is} OOS={n_oos} breakdown_frac={df['in_breakdown'].mean():.3f}")
    print(f"TOTAL IS={tot_is} OOS={tot_oos}")
    with open(OUT / "out_diag.json", "w") as f:
        json.dump({"tot_is": int(tot_is), "tot_oos": int(tot_oos)}, f)


def cmd_main():
    frames = build_all_frames()
    for label, kwargs in [("net", dict(fee=eng.TAKER_FEE, slippage=eng.SLIPPAGE)),
                          ("gross", dict(fee=0.0, slippage=0.0))]:
        tdf = run_trades(frames, sig.DEFAULT_PARAMS, **kwargs)
        splits = _split(tdf)
        print(f"--- {label} ---")
        for k, v in splits.items():
            s = _summ(v)
            print(f"{k}: n={s['n']} PF(R)={s['pf']:.4f} t={s['t']:.4f} winrate={s['winrate']:.3f}")
        tdf.to_pickle(OUT / f"trades_{label}.pkl")
    return frames


def cmd_controls():
    # ① 재동조확인 제거
    frames1 = build_all_frames(skip_recouple_check=True)
    tdf1 = run_trades(frames1, sig.DEFAULT_PARAMS)
    print("== 대조군① (붕괴확정 즉시 진입, 재동조 대기 없음) ==")
    for k, v in _split(tdf1).items():
        s = _summ(v); print(f"{k}: n={s['n']} PF(R)={s['pf']:.4f} t={s['t']:.4f}")

    # ② 15m 확인필터 제거
    frames2 = build_all_frames(require_confirm=False)
    tdf2 = run_trades(frames2, sig.DEFAULT_PARAMS)
    print("== 대조군② (15m EMA 확인필터 없음) ==")
    for k, v in _split(tdf2).items():
        s = _summ(v); print(f"{k}: n={s['n']} PF(R)={s['pf']:.4f} t={s['t']:.4f}")

    # ③ 플라시보: 종목별 실제 신호와 동일 '개수'를 무작위 시점(진짜 신호 인덱스 제외)에서 뽑아
    #    같은 청산엔진(ATR14 스톱/RR/시간청산, 방향은 동전던지기)으로 시뮬 — 100회 반복 평균/CI
    rng = np.random.default_rng(42)
    placebo_pfs = []
    base_frames = build_all_frames()
    for rep in range(30):
        all_trades = []
        for s, df in base_frames.items():
            n_sig = int(df["signal"].sum())
            if n_sig == 0:
                continue
            valid_idx = np.where(df["atr14"].notna().to_numpy() & df["pctile"].notna().to_numpy())[0]
            valid_idx = valid_idx[valid_idx < len(df) - 1]
            chosen = rng.choice(valid_idx, size=n_sig, replace=False)
            dirs = rng.choice([-1, 1], size=n_sig)
            dfx = df.copy()
            dfx["signal"] = False
            dfx.iloc[chosen, dfx.columns.get_loc("signal")] = True
            override = {int(idx): int(d) for idx, d in zip(chosen, dirs)}
            all_trades += eng.simulate_symbol(s, dfx, sig.DEFAULT_PARAMS,
                                              direction_override=override)
        tdf = eng.trades_to_df(all_trades)
        oos = _split(tdf)["OOS"]
        if len(oos) > 5:
            placebo_pfs.append(eng.pf_r(oos))
    placebo_pfs = np.array(placebo_pfs)
    print(f"== 대조군③ 플라시보(무작위 타이밍+무작위 방향, {len(placebo_pfs)}회) ==")
    print(f"OOS PF(R) 분포: mean={placebo_pfs.mean():.3f} median={np.median(placebo_pfs):.3f} "
         f"[{np.percentile(placebo_pfs,5):.3f},{np.percentile(placebo_pfs,95):.3f}]")
    actual_oos_pf = _summ(_split(pd.read_pickle(OUT / "trades_net.pkl"))["OOS"])["pf"] \
        if (OUT / "trades_net.pkl").exists() else float("nan")
    pctile_rank = float((placebo_pfs < actual_oos_pf).mean() * 100) if not np.isnan(actual_oos_pf) else float("nan")
    print(f"실제 채택안 OOS PF(R)={actual_oos_pf:.4f} -> 플라시보 분포 내 백분위={pctile_rank:.1f}")


def cmd_reverse():
    frames = build_all_frames()
    tdf_fwd = run_trades(frames, sig.DEFAULT_PARAMS)
    tdf_rev = run_trades(frames, sig.DEFAULT_PARAMS, reverse=True)
    print("== 정방향 vs 반전 ==")
    for label, tdf in [("정방향", tdf_fwd), ("반전", tdf_rev)]:
        for k, v in _split(tdf).items():
            s = _summ(v); print(f"{label} {k}: n={s['n']} PF(R)={s['pf']:.4f} t={s['t']:.4f}")
    # 제3의 대안: 테제무효화 청산 완전 비활성(구조상 direction 미참조라 반전에도 불변이어야 함)
    tdf_rev_noinval = run_trades(frames, sig.DEFAULT_PARAMS, reverse=True, disable_invalidation=True)
    print("== 반전 + 테제무효화 청산 비활성(대안, 구조상 결과 거의 동일해야 함) ==")
    for k, v in _split(tdf_rev_noinval).items():
        s = _summ(v); print(f"{k}: n={s['n']} PF(R)={s['pf']:.4f} t={s['t']:.4f}")
    zero_hold_fwd = (tdf_fwd["holding_bars"] == 0).mean()
    zero_hold_rev = (tdf_rev["holding_bars"] == 0).mean()
    print(f"zero_hold_frac fwd={zero_hold_fwd:.3f} rev={zero_hold_rev:.3f} (참고용, 트리비얼 지표 — 결론 근거로 미사용)")
    reason_fwd = tdf_fwd["reason"].value_counts(normalize=True)
    reason_rev = tdf_rev["reason"].value_counts(normalize=True)
    print("정방향 청산사유 분포:\n", reason_fwd)
    print("반전 청산사유 분포:\n", reason_rev)


def cmd_shuffle():
    frames = build_all_frames()
    rng = np.random.default_rng(7)
    n_reps = 100
    means = []
    actual = None
    for rep in range(n_reps):
        all_trades = []
        for s, df in frames.items():
            sig_idx = np.where(df["signal"].to_numpy(bool))[0]
            flips = rng.choice([-1, 1], size=len(sig_idx))
            override = {int(i): int(f * df["direction"].iloc[i]) for i, f in zip(sig_idx, flips)}
            all_trades += eng.simulate_symbol(s, df, sig.DEFAULT_PARAMS, direction_override=override)
        tdf = eng.trades_to_df(all_trades)
        oos = _split(tdf)["OOS"]
        means.append(oos["r_multiple"].mean())
    means = np.array(means)
    tdf_actual = run_trades(frames, sig.DEFAULT_PARAMS)
    actual_mean = _split(tdf_actual)["OOS"]["r_multiple"].mean()
    pctile_rank = float((means < actual_mean).mean() * 100)
    print(f"셔플 {n_reps}회 OOS mean(R) 분포: mean={means.mean():.4f} std={means.std():.4f}")
    print(f"실제 mean(R)={actual_mean:.4f} -> 백분위={pctile_rank:.1f}")


def _daily_agg(tdf: pd.DataFrame) -> pd.Series:
    d = tdf.copy()
    d["day"] = d["entry_time"].dt.floor("D")
    return d.groupby("day")["r_multiple"].sum()


def _tstat_arr(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return float("nan")
    sd = x.std(ddof=1)
    if sd == 0:
        return float("nan")
    return x.mean() / (sd / np.sqrt(n))


def cmd_declus():
    frames = build_all_frames()
    tdf = run_trades(frames, sig.DEFAULT_PARAMS)
    oos = _split(tdf)["OOS"]
    print(f"OOS 트레이드 단위: n={len(oos)} t={eng.t_stat(oos):.3f}")

    daily = _daily_agg(oos)
    print(f"OOS 캘린더일 단위: 고유일={len(daily)} (명목 {len(oos)}) t={_tstat_arr(daily.to_numpy()):.3f} "
         f"mean={daily.mean():.4f}")

    # 5일 롤링 블록: entry_time 을 5일 버킷으로 묶어 버킷 합
    d = oos.copy()
    d["bucket"] = (d["entry_time"] - pd.Timestamp(c.OOS_START)).dt.days // 5
    bucket_sum = d.groupby("bucket")["r_multiple"].sum()
    print(f"OOS 5일 블록 단위: 고유블록={len(bucket_sum)} t={_tstat_arr(bucket_sum.to_numpy()):.3f} "
         f"mean={bucket_sum.mean():.4f}")

    # 종목 간 동시신호(같은 캘린더일) 비율 + 5일 롤링 클러스터 기여도
    entries = oos[["symbol", "entry_time"]].copy()
    entries["day"] = entries["entry_time"].dt.floor("D")
    per_day_syms = entries.groupby("day")["symbol"].nunique()
    print(f"같은 날 동시신호 분포:\n{per_day_syms.value_counts().sort_index()}")
    same_day_multi = (per_day_syms >= 2).sum()
    print(f"2종목 이상 동시신호 일수={same_day_multi} / 고유신호일={len(per_day_syms)}")

    # 5일 롤링 윈도우 최대 기여 클러스터(순 R 기준)
    oos2 = oos.copy().sort_values("entry_time")
    oos2["t_days"] = (oos2["entry_time"] - pd.Timestamp(c.OOS_START)).dt.days
    best_sum, best_start = -1e18, None
    for start in range(0, int(oos2["t_days"].max()) + 1):
        window = oos2[(oos2["t_days"] >= start) & (oos2["t_days"] < start + 5)]
        s = window["r_multiple"].sum()
        if s > best_sum:
            best_sum, best_start = s, start
    total_r = oos2["r_multiple"].sum()
    print(f"OOS 순 R 합계={total_r:.3f}, 최대 기여 5일 클러스터(day {best_start}~{best_start+5}) 합={best_sum:.3f} "
         f"({(best_sum/total_r*100 if total_r!=0 else float('nan')):.1f}%)")
    window_best = oos2[(oos2["t_days"] >= best_start) & (oos2["t_days"] < best_start + 5)]
    print(window_best[["symbol", "entry_time", "r_multiple"]].to_string())
    # 클러스터 제거 대칭점검
    without = oos2[~((oos2["t_days"] >= best_start) & (oos2["t_days"] < best_start + 5))]
    print(f"최대 클러스터 제외 후: n={len(without)} PF(R)={eng.pf_r(without):.4f} t={eng.t_stat(without):.4f}")


def cmd_loo():
    frames = build_all_frames()
    for excl in c.SYMBOLS:
        sub_frames = {s: f for s, f in frames.items() if s != excl}
        tdf = run_trades(sub_frames, sig.DEFAULT_PARAMS)
        oos = _split(tdf)["OOS"]
        s = _summ(oos)
        print(f"제외={excl}: OOS n={s['n']} PF(R)={s['pf']:.4f} t={s['t']:.4f}")


def cmd_topn():
    frames = build_all_frames()
    tdf = run_trades(frames, sig.DEFAULT_PARAMS)
    oos = _split(tdf)["OOS"].sort_values("r_multiple", ascending=False)
    for n in [1, 3, 5, 10]:
        rest = oos.iloc[n:]
        print(f"top-{n} 제거: n={len(rest)} PF(R)={eng.pf_r(rest):.4f} t={eng.t_stat(rest):.4f}")


def cmd_sweep():
    variants = {
        "base": {},
        "dwell3": {"min_dwell": 3}, "dwell12": {"min_dwell": 12},
        "bpct5": {"breakdown_pctile": 5}, "bpct20": {"breakdown_pctile": 20},
        "rpct40": {"recouple_pctile": 40}, "rpct70": {"recouple_pctile": 70},
        "corrw48": {"corr_window": 48}, "corrw120": {"corr_window": 120},
        "pctw480": {"pctile_window": 480}, "pctw1080": {"pctile_window": 1080},
        "atrmult1.0": {"atr_stop_mult": 1.0}, "atrmult1.6": {"atr_stop_mult": 1.6},
        "rr1.0": {"rr_target": 1.0}, "rr2.0": {"rr_target": 2.0},
        "dirlb3": {"direction_lookback": 3}, "dirlb12": {"direction_lookback": 12},
    }
    rows = []
    for name, override in variants.items():
        params = {**sig.DEFAULT_PARAMS, **override}
        frames = build_all_frames(params=params)
        tdf = run_trades(frames, params)
        splits = _split(tdf)
        is_s = _summ(splits["IS"]); oos_s = _summ(splits["OOS"])
        rows.append(dict(name=name, n_is=is_s["n"], pf_is=is_s["pf"], n_oos=oos_s["n"],
                         pf_oos=oos_s["pf"], t_oos=oos_s["t"]))
        print(f"{name}: IS n={is_s['n']} PF={is_s['pf']:.3f} | OOS n={oos_s['n']} "
             f"PF={oos_s['pf']:.3f} t={oos_s['t']:.3f}")
    pd.DataFrame(rows).to_csv(OUT / "sweep.csv", index=False)


def cmd_gatecheck():
    frames = build_all_frames()
    for s in c.SYMBOLS[:2]:
        df = frames[s]
        pctile = df["pctile"].dropna()
        below10 = (pctile <= 10).mean()
        print(f"{s}: pctile<=10 비율={below10*100:.2f}% (설계상 ~10% 근접 기대, 정보무관 트리비얼 발화율)")
    # 트리거 시점 한정 상관: gd/td 의 레벨 상관을 트리거 시점만으로 좁혀서 비교
    for s in c.SYMBOLS[:3]:
        df = frames[s]
        g_level = df["g_raw"]; top_level = df["top_raw"]
        overall_corr = g_level.corr(top_level)
        trig_idx = df.index[df["signal"]]
        # 트리거 전후 24시간 윈도우 내 레벨 상관(표본 다소 필요)
        window_mask = pd.Series(False, index=df.index)
        for t in trig_idx:
            lo = df.index.searchsorted(t - pd.Timedelta(hours=24))
            hi = df.index.searchsorted(t + pd.Timedelta(hours=24))
            window_mask.iloc[lo:hi] = True
        trig_corr = g_level[window_mask].corr(top_level[window_mask])
        print(f"{s}: 레벨 상관 전체={overall_corr:.4f} 트리거±24h윈도우한정={trig_corr:.4f} "
             f"(n_window={window_mask.sum()})")


def cmd_lookahead():
    """룩어헤드 절단 재실행: 데이터 뒷부분을 자른 뒤 앞부분 신호가 그대로인지 확인."""
    s = "BTCUSDT"
    df_full = sig.build_signal_frame(s)
    cut = 20000  # 임의 절단점(2023년대 중반 근처)
    k1h_full = c.load_klines(s, "1h", c.IS_START, c.OOS_END)
    cut_time = k1h_full.index[cut]
    # 절단 재현: OOS_END 를 절단 시점으로 좁혀 재계산
    df_cut = sig.build_signal_frame(s, params={**sig.DEFAULT_PARAMS})
    df_cut = df_cut[df_cut.index <= cut_time]
    df_full_pre = df_full[df_full.index <= cut_time]
    cols = ["corr", "pctile", "trigger", "direction", "signal"]
    diffs = 0
    for col in cols:
        a = df_cut[col].to_numpy()
        b = df_full_pre[col].to_numpy()
        if col in ("trigger", "signal"):
            d = (a != b).sum()
        else:
            d = (~np.isclose(a, b, equal_nan=True)).sum()
        diffs += d
        print(f"{col}: mismatch={d}/{len(a)}")
    print("룩어헤드 절단검사:", "PASS(0건)" if diffs == 0 else f"FAIL({diffs}건 불일치)")


CMDS = {
    "diag": cmd_diag, "main": cmd_main, "controls": cmd_controls, "reverse": cmd_reverse,
    "shuffle": cmd_shuffle, "declus": cmd_declus, "loo": cmd_loo, "topn": cmd_topn,
    "sweep": cmd_sweep, "gatecheck": cmd_gatecheck, "lookahead": cmd_lookahead,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print("사용법: python3 gtacrr_run.py <" + "|".join(CMDS) + ">")
        sys.exit(1)
    CMDS[sys.argv[1]]()
