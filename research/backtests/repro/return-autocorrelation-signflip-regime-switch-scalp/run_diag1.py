"""1차 진단: 재포장 점검(Hurst·분산비율·ROC·ADX·실현변동성과의 상관) + 결합확률 실측 +
레짐 체류시간/중립비율 실측. 스펙 사전 폐기조건 (c)의 |r|>=0.8 여부를 전 구간·트리거시점 둘 다 확인.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import indicators as racsr_ind
from crypto_trader.signals import indicators as ind

N_1H = 60
RHO_TH = 0.15


def build_diag_frame(symbol: str) -> pd.DataFrame | None:
    h1 = common.load_klines(symbol, "1h")
    if h1.empty:
        return None
    r1h = racsr_ind.log_returns(h1["close"])
    rho = racsr_ind.rolling_lag1_autocorr(r1h, N_1H)
    hurst = racsr_ind.rolling_hurst_rs(r1h, N_1H)
    vr2 = racsr_ind.rolling_variance_ratio2(r1h, N_1H)
    roc = racsr_ind.rolling_roc(h1["close"], N_1H)
    rvol = racsr_ind.rolling_realized_vol(r1h, N_1H)
    adx_, _, _ = ind.adx(h1, 14)
    df = pd.DataFrame({"rho": rho, "hurst": hurst, "vr2": vr2, "roc": roc,
                       "rvol": rvol, "adx": adx_})
    df["symbol"] = symbol
    return df


def main() -> None:
    frames = []
    for sym in common.SYMBOLS:
        d = build_diag_frame(sym)
        if d is not None:
            frames.append(d)
    full = pd.concat(frames)
    full_valid = full.dropna(subset=["rho", "hurst", "vr2", "roc", "rvol", "adx"])

    print("=" * 70)
    print("1) 전 구간 상관 (rho vs 비교지표), pooled 7종목, n=%d" % len(full_valid))
    for col in ["hurst", "vr2", "roc", "rvol", "adx"]:
        r = full_valid["rho"].corr(full_valid[col])
        print(f"   rho vs {col:6s}: r={r:+.4f}")

    print()
    print("   종목별 전 구간 상관(rho vs hurst, rho vs vr2):")
    for sym in common.SYMBOLS:
        sub = full_valid[full_valid["symbol"] == sym]
        if len(sub) < 30:
            continue
        rh = sub["rho"].corr(sub["hurst"])
        rv = sub["rho"].corr(sub["vr2"])
        print(f"   {sym:10s} n={len(sub):6d} rho~hurst={rh:+.4f} rho~vr2={rv:+.4f}")

    # ---- 2) 트리거 시점 상관: gated 베이스 전략의 실제 진입 신호봉만 추림 ----
    cfg = engine.RunConfig(signal_mode="gated", direction_mode="normal", cost_on=True)
    sigs = engine.load_all_signals(common.SYMBOLS, cfg)
    trades = engine.run_all(sigs, cfg)

    trig_rows = []
    diag_by_sym = {sym: build_diag_frame(sym) for sym in common.SYMBOLS}
    for sym, tlist in trades.items():
        sig = sigs[sym]
        h15 = sig.h15
        d1h = diag_by_sym[sym]
        if d1h is None:
            continue
        # 1h 비교지표를 15m 그리드에 rho15 와 동일 규칙(backward asof, +1h 확정)으로 매핑
        mapped = {}
        for col in ["hurst", "vr2", "roc", "rvol", "adx"]:
            mapped[col] = common.map_asof_backward(pd.DatetimeIndex(h15.index), d1h[col], 3600)
        for t in tlist:
            i = t.entry_idx - 1  # 신호봉(진입 판정 시점)
            if i < 0:
                continue
            row = {"symbol": sym, "mode": t.mode, "rho": sig.rho15[i]}
            for col in ["hurst", "vr2", "roc", "rvol", "adx"]:
                row[col] = mapped[col][i]
            trig_rows.append(row)

    trig_df = pd.DataFrame(trig_rows).dropna()
    print()
    print("=" * 70)
    print("2) 트리거 시점(gated 베이스 실제 진입 신호봉) 상관, n=%d" % len(trig_df))
    for col in ["hurst", "vr2", "roc", "rvol", "adx"]:
        r = trig_df["rho"].corr(trig_df[col])
        print(f"   rho vs {col:6s}: r={r:+.4f}")
    print()
    print("   서브모드별:")
    for mode in ["MR", "MOM"]:
        sub = trig_df[trig_df["mode"] == mode]
        if len(sub) < 5:
            print(f"   {mode}: n={len(sub)} (표본부족)")
            continue
        rh = sub["rho"].corr(sub["hurst"])
        rv = sub["rho"].corr(sub["vr2"])
        print(f"   {mode:4s} n={len(sub):6d} rho~hurst={rh:+.4f} rho~vr2={rv:+.4f}")

    # ---- 3) 레짐 체류시간·중립비율·결합확률 실측 ----
    print()
    print("=" * 70)
    print("3) 레짐 분포(1h 기준, 풀링 7종목) + 15m 트리거 발생률")
    reg_counts = {"MR": 0, "MOM": 0, "NEUTRAL": 0, "NA": 0}
    total_1h = 0
    for sym in common.SYMBOLS:
        d1h = diag_by_sym[sym]
        if d1h is None:
            continue
        rho = d1h["rho"]
        total_1h += len(rho)
        reg_counts["MR"] += int((rho <= -RHO_TH).sum())
        reg_counts["MOM"] += int((rho >= RHO_TH).sum())
        reg_counts["NA"] += int(rho.isna().sum())
    reg_counts["NEUTRAL"] = total_1h - reg_counts["MR"] - reg_counts["MOM"] - reg_counts["NA"]
    for k, v in reg_counts.items():
        print(f"   {k:8s}: {v:8d}  ({100*v/total_1h:.2f}%)")

    print()
    print("   15m 트리거 발생 수(진입 신호봉 기준, gated 베이스 실행 결과):")
    n_mr = sum(1 for tl in trades.values() for t in tl if t.mode == "MR")
    n_mom = sum(1 for tl in trades.values() for t in tl if t.mode == "MOM")
    print(f"   MR 트리거(진입) = {n_mr}, MOM 트리거(진입) = {n_mom}, 합계 = {n_mr+n_mom}")
    n_years = (common.OOS_END - common.IS_START).days / 365.25
    print(f"   기간 {n_years:.2f}년, 7종목 -> 종목당 연 {(n_mr+n_mom)/7/n_years:.1f}건"
         f" (스펙 예상 종목당 연 80~200건)")


if __name__ == "__main__":
    main()
