"""종목 간 신호 상관 — 평시 vs 위기국면(BTC 절대 일간수익률 상위 5%), 모드별.

일 단위 이진 신호(그날 신호 발생 여부)의 종목쌍 평균 피어슨 상관을 평시/위기로 나눠 비교.
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
from common import SYMBOLS, load_klines_4h
from signals import build_signals


def daily_signal_flag(ind: pd.DataFrame, dir_col: str) -> pd.Series:
    sig = (ind[dir_col] != 0).astype(int)
    return sig.resample("1D").max()


def main():
    btc_df = load_klines_4h("BTCUSDT")
    btc_close_1d = btc_df["close"].resample("1D").last()
    btc_ret_1d = btc_close_1d.pct_change().abs()
    crisis_thresh = btc_ret_1d.quantile(0.95)
    crisis_days = btc_ret_1d[btc_ret_1d >= crisis_thresh].index
    calm_days = btc_ret_1d[btc_ret_1d < crisis_thresh].index

    out = {}
    for mode in ["breakout", "fade"]:
        dir_col = "raw_breakout_dir" if mode == "breakout" else "raw_fade_dir"
        flags = {}
        for sym in SYMBOLS:
            df = load_klines_4h(sym)
            ind = build_signals(df)
            flags[sym] = daily_signal_flag(ind, dir_col)
        flag_df = pd.DataFrame(flags).fillna(0)

        calm = flag_df.reindex(calm_days).dropna(how="all")
        crisis = flag_df.reindex(crisis_days).dropna(how="all")

        def avg_pairwise_corr(frame: pd.DataFrame) -> float:
            c = frame.corr()
            n = len(c)
            vals = c.to_numpy()[np.triu_indices(n, k=1)]
            vals = vals[~np.isnan(vals)]
            return float(vals.mean()) if len(vals) else float("nan")

        out[mode] = {
            "calm_days_n": int(len(calm)), "crisis_days_n": int(len(crisis)),
            "calm_avg_pairwise_corr": avg_pairwise_corr(calm),
            "crisis_avg_pairwise_corr": avg_pairwise_corr(crisis),
            "crisis_threshold_abs_ret": float(crisis_thresh),
        }
        print(mode, out[mode])

    with open("out_diag_cross_corr.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
