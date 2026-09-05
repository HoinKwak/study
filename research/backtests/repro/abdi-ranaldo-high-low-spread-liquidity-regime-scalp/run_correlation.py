"""동어반복 점검: AR 스프레드 vs ATR%/RV/HL range/Roll/CS 상관(전체구간 vs 트리거시점 한정),
pandas.corr()(pairwise) 사용. 계열곱 음수비율(사전폐기조건 b)도 함께 진단."""
from __future__ import annotations

import pandas as pd

import common
import engine
import run_main as rm


def full_sample_corr(sigs) -> pd.DataFrame:
    rows = []
    for sym, sig in sigs.items():
        df = pd.DataFrame({
            "ar": sig.ar_spread, "atrp": sig.atrp.rolling(common.AR_WINDOW).mean(),
            "rv": sig.rv, "hl": sig.hlrange, "roll": sig.roll_sp, "cs": sig.cs_sp,
        })
        c = df.corr(method="pearson")["ar"].drop("ar")
        c.name = sym
        rows.append(c)
    out = pd.concat(rows, axis=1).T
    out.loc["mean"] = out.mean()
    return out


def trigger_time_corr(sigs, cfg: engine.RunConfig) -> pd.DataFrame:
    """트리거 확정 1h봉(signal_idx) 시점 한정 상관 — 프리미엄인덱스 건 함정(전체 0.246→트리거시
    0.928) 재확인용."""
    rows = []
    for sym, sig in sigs.items():
        events = engine._detect_1h_events(sig, cfg)
        if not events:
            continue
        idxs = sorted({e["signal_idx"] for e in events})
        df1h = sig.df1h
        atrp_roll = sig.atrp.rolling(common.AR_WINDOW).mean()
        sub = pd.DataFrame({
            "ar": sig.ar_spread.iloc[idxs].to_numpy(),
            "atrp": atrp_roll.iloc[idxs].to_numpy(),
            "rv": sig.rv.iloc[idxs].to_numpy(),
            "hl": sig.hlrange.iloc[idxs].to_numpy(),
            "roll": sig.roll_sp.iloc[idxs].to_numpy(),
            "cs": sig.cs_sp.iloc[idxs].to_numpy(),
        })
        c = sub.corr(method="pearson")["ar"].drop("ar")
        c.name = sym
        c["n_events"] = len(idxs)
        rows.append(c)
    out = pd.concat(rows, axis=1).T
    return out


def negative_product_ratio(sigs) -> pd.Series:
    out = {}
    for sym, sig in sigs.items():
        p = sig.ar_product.dropna()
        out[sym] = float((p < 0).mean())
    return pd.Series(out)


if __name__ == "__main__":
    sigs = rm.get_signals()
    print("===== 전체구간 AR 스프레드 vs 5개 지표 상관(pandas.corr, pairwise) =====")
    fc = full_sample_corr(sigs)
    print(fc.round(3).to_string())

    print("\n===== 트리거 시점 한정 상관(기본안 게이트='ar') =====")
    cfg = engine.RunConfig()
    tc = trigger_time_corr(sigs, cfg)
    print(tc.round(3).to_string())

    print("\n===== 계열곱(c_t*c_t-1) 음수비율(사전폐기조건 b: <50%면 정의결함) =====")
    npr = negative_product_ratio(sigs)
    print(npr.round(4).to_string())
    print("평균:", npr.mean())
