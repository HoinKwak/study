"""⚠️ 최우선 검증: 동어반복(재포장) 점검.

곡률계수 c(2차 회귀)가 기존 프리미엄인덱스 계열 스펙들의 1차 통계량 재포장인지 상관계수로 확인.
- 비교대상 ①: `premium-index-momentum-trend-continuation-scalp.md`의 실제 신호원 —
  `EMA(premium,20,15m)`의 8봉 기울기(mom_ema_slope), 체크포인트 시각 기준 causal 조회.
- 비교대상 ②: `premium-index-intraday-volatility-squeeze-...-scalp.md`의 실제 신호원 —
  정산(체크포인트) 직전 30분 프리미엄인덱스 range(=high-low, squeeze_range30).
전체 구간 상관 + **트리거 시점 한정**(|c_z|>=z_threshold) 상관을 모두 산출.
c(레벨) 뿐 아니라 c_z(우리가 실제 게이트로 쓰는 z-score) 대 같은 방식으로 causal z-score한
경쟁지표(mom_z, range_z)의 상관도 병기.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from common import SYMBOLS, load_symbol
from crypto_trader.signals import indicators as _ind  # noqa: E402  (common.py 가 sys.path 세팅)
from events import build_events, causal_zscore

Z_THRESHOLD = 2.0


def compute_symbol(symbol: str) -> pd.DataFrame:
    data = load_symbol(symbol)
    prem_1m = data["prem_1m"]["close"]
    premium_15m = prem_1m.resample("15min", label="left", closed="left").last()
    ema15 = _ind.ema(premium_15m, 20)
    mom_slope = ema15 - ema15.shift(8)

    events = build_events(prem_1m, lookback=60)
    events = events[events["c_z"].notna()].copy()
    if events.empty:
        return pd.DataFrame()

    # 15m 인덱스 배열(ns) — 완결봉만 참조: open_time + 15min <= checkpoint_time
    idx15_ns = premium_15m.index.values.astype("datetime64[ns]").astype(np.int64)
    fifteen_min_ns = np.int64(15 * 60_000_000_000)
    ck_ns = events["checkpoint_time"].values.astype("datetime64[ns]").astype(np.int64)
    pos15 = np.searchsorted(idx15_ns, ck_ns - fifteen_min_ns, side="right") - 1
    pos15 = np.clip(pos15, 0, len(idx15_ns) - 1)
    mom_vals = mom_slope.to_numpy()[pos15]
    mom_vals = np.where(pos15 >= 0, mom_vals, np.nan)

    # 1분봉 range30: [checkpoint_time-30min, checkpoint_time) 구간의 high-low(=max-min of close)
    ts1_ns = prem_1m.index.values.astype("datetime64[ns]").astype(np.int64)
    vals1 = prem_1m.to_numpy(dtype=float)
    thirty_min_ns = np.int64(30 * 60_000_000_000)
    range30 = np.full(len(events), np.nan)
    lo_idx = np.searchsorted(ts1_ns, ck_ns - thirty_min_ns, side="left")
    hi_idx = np.searchsorted(ts1_ns, ck_ns, side="left")  # exclusive of checkpoint itself
    for i in range(len(events)):
        lo, hi = lo_idx[i], hi_idx[i]
        if hi > lo:
            seg = vals1[lo:hi]
            if len(seg) >= 5:
                range30[i] = seg.max() - seg.min()

    events["mom_slope"] = mom_vals
    events["range30"] = range30
    events["mom_z"] = causal_zscore(events["mom_slope"].reset_index(drop=True), 60).to_numpy()
    events["range_z"] = causal_zscore(events["range30"].reset_index(drop=True), 60).to_numpy()
    events["symbol"] = symbol
    return events


def main():
    frames = [compute_symbol(s) for s in SYMBOLS]
    all_ev = pd.concat(frames, ignore_index=True)
    all_ev.to_parquet("out_diag_events.parquet")

    def corr_report(df: pd.DataFrame, label: str):
        n = len(df)
        r_mom = df["c"].corr(df["mom_slope"])
        r_range = df["c"].corr(df["range30"])
        r_mom_z = df["c_z"].corr(df["mom_z"])
        r_range_z = df["c_z"].corr(df["range_z"])
        print(f"[{label}] n={n}")
        print(f"  corr(c, mom_ema_slope)   = {r_mom:+.4f}")
        print(f"  corr(c, squeeze_range30) = {r_range:+.4f}")
        print(f"  corr(c_z, mom_z)         = {r_mom_z:+.4f}")
        print(f"  corr(c_z, range_z)       = {r_range_z:+.4f}")
        return dict(n=n, r_mom=r_mom, r_range=r_range, r_mom_z=r_mom_z, r_range_z=r_range_z)

    out = {}
    out["full"] = corr_report(all_ev.dropna(subset=["mom_slope", "range30"]), "전체 구간")
    trig = all_ev[all_ev["c_z"].abs() >= Z_THRESHOLD].dropna(subset=["mom_slope", "range30"])
    out["trigger"] = corr_report(trig, f"트리거 시점(|c_z|>={Z_THRESHOLD})")

    # 종목별 트리거시점 상관도 병기(단일 종목 쏠림 확인)
    print("\n종목별 트리거시점 corr(c, mom_slope) / corr(c, range30):")
    per_sym = {}
    for sym, g in trig.groupby("symbol"):
        rm = g["c"].corr(g["mom_slope"]); rr = g["c"].corr(g["range30"])
        print(f"  {sym}: n={len(g)}  r_mom={rm:+.4f}  r_range={rr:+.4f}")
        per_sym[sym] = dict(n=len(g), r_mom=rm, r_range=rr)
    out["per_symbol_trigger"] = per_sym

    import json
    with open("out_diag_corr.json", "w") as f:
        json.dump(out, f, indent=2, default=float)
    print("\nsaved out_diag_corr.json, out_diag_events.parquet")


if __name__ == "__main__":
    main()
