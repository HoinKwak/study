"""진단 1(최우선): 동어반복 점검 — wick_asym(프리미엄) vs ① 프리미엄 z-score, ② 프리미엄
실현변동성, ③ 가격 캔들 꼬리비율. 전체구간 + 트리거 시점 한정 양쪽. pandas.corr() 사용
(np.corrcoef 금지 — 과거 함정 재현 방지)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import SYMBOLS, load_symbol, wick_asym
from engine import build_frame, find_signals


def price_wick_asym(price4h: pd.DataFrame) -> pd.Series:
    return wick_asym(price4h)


def premium_zscore(prem4h: pd.DataFrame, window: int = 60) -> pd.Series:
    c = prem4h["close"]
    mean = c.rolling(window, min_periods=window).mean()
    std = c.rolling(window, min_periods=window).std(ddof=0)
    return (c - mean) / std.replace(0, np.nan)


def premium_realized_vol(prem4h: pd.DataFrame, window: int = 20) -> pd.Series:
    ret = prem4h["close"].diff()  # 프리미엄은 레벨이 0 근방을 오가므로 diff(수익률 아님)
    return ret.rolling(window, min_periods=window).std(ddof=0)


def main() -> None:
    rows_full = []
    rows_trig = []
    for sym in SYMBOLS:
        data = load_symbol(sym)
        prem = data["prem_4h"]
        price = data["price_4h"]
        idx = prem.index.intersection(price.index)
        prem_a = prem.loc[idx]
        price_a = price.loc[idx]

        wa_prem = wick_asym(prem_a)
        wa_price = wick_asym(price_a)
        z = premium_zscore(prem_a)
        rv = premium_realized_vol(prem_a)

        df = pd.DataFrame({"wa_prem": wa_prem, "wa_price": wa_price, "z": z, "rv": rv})
        df_valid = df.dropna()
        r_price = df_valid["wa_prem"].corr(df_valid["wa_price"])
        r_z = df_valid["wa_prem"].corr(df_valid["z"])
        r_rv = df_valid["wa_prem"].corr(df_valid["rv"])
        rows_full.append({"symbol": sym, "n": len(df_valid), "r_wick_price": r_price,
                           "r_zscore": r_z, "r_realized_vol": r_rv})

        # 트리거 시점 한정: 실제 진입조건(consec>=4 등)을 만족한 신호 시점만
        frame = build_frame(sym)
        signals = find_signals(frame)
        sig_times = pd.DatetimeIndex([s[0] for s in signals])
        sig_times = sig_times.intersection(df_valid.index)
        if len(sig_times) >= 5:
            sub = df_valid.loc[sig_times]
            r_price_t = sub["wa_prem"].corr(sub["wa_price"])
            r_z_t = sub["wa_prem"].corr(sub["z"])
            r_rv_t = sub["wa_prem"].corr(sub["rv"])
        else:
            r_price_t = r_z_t = r_rv_t = float("nan")
        rows_trig.append({"symbol": sym, "n_trigger": len(sig_times),
                           "r_wick_price_trigger": r_price_t, "r_zscore_trigger": r_z_t,
                           "r_realized_vol_trigger": r_rv_t})

    full_df = pd.DataFrame(rows_full)
    trig_df = pd.DataFrame(rows_trig)
    print("=== 전체구간 상관 (wick_asym vs ①zscore ②실현변동성 ③가격꼬리비율) ===")
    print(full_df.to_string(index=False))
    print("\n=== 트리거 시점 한정 상관 ===")
    print(trig_df.to_string(index=False))

    # 풀링(전종목 concat) 상관도 병기
    pooled_full = []
    pooled_trig = []
    for sym in SYMBOLS:
        data = load_symbol(sym)
        prem = data["prem_4h"]; price = data["price_4h"]
        idx = prem.index.intersection(price.index)
        prem_a = prem.loc[idx]; price_a = price.loc[idx]
        wa_prem = wick_asym(prem_a); wa_price = wick_asym(price_a)
        z = premium_zscore(prem_a); rv = premium_realized_vol(prem_a)
        df = pd.DataFrame({"wa_prem": wa_prem, "wa_price": wa_price, "z": z, "rv": rv}).dropna()
        pooled_full.append(df)
        frame = build_frame(sym)
        signals = find_signals(frame)
        sig_times = pd.DatetimeIndex([s[0] for s in signals]).intersection(df.index)
        if len(sig_times):
            pooled_trig.append(df.loc[sig_times])

    pf = pd.concat(pooled_full)
    pt = pd.concat(pooled_trig) if pooled_trig else pd.DataFrame()
    pooled_summary = {
        "pooled_full_n": len(pf),
        "pooled_full_r_wick_price": pf["wa_prem"].corr(pf["wa_price"]),
        "pooled_full_r_zscore": pf["wa_prem"].corr(pf["z"]),
        "pooled_full_r_realized_vol": pf["wa_prem"].corr(pf["rv"]),
        "pooled_trigger_n": len(pt),
        "pooled_trigger_r_wick_price": pt["wa_prem"].corr(pt["wa_price"]) if len(pt) else float("nan"),
        "pooled_trigger_r_zscore": pt["wa_prem"].corr(pt["z"]) if len(pt) else float("nan"),
        "pooled_trigger_r_realized_vol": pt["wa_prem"].corr(pt["rv"]) if len(pt) else float("nan"),
    }
    print("\n=== 풀링(전종목) ===")
    print(json.dumps(pooled_summary, indent=2, default=str))

    out = {"per_symbol_full": rows_full, "per_symbol_trigger": rows_trig,
           "pooled": pooled_summary}
    with open("out_diag_corr.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\n저장: out_diag_corr.json")


if __name__ == "__main__":
    main()
