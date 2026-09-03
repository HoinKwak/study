"""종목 간 신호 상관 — 평균 vs 위기국면(BTC 절대일수익률 상위 5%). 일별 진입발생 이진지표 상관."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import SYMBOLS, load_klines_4h


def main() -> None:
    df = pd.read_csv("out_base_trades.csv", parse_dates=["entry_time"])
    df["day"] = df["entry_time"].dt.floor("D")

    # 종목별 일별 진입 발생 이진 시계열(전체기간 캘린더일 그리드)
    all_days = pd.date_range(df["day"].min(), df["day"].max(), freq="D", tz="UTC")
    mat = pd.DataFrame(0, index=all_days, columns=SYMBOLS)
    for sym in SYMBOLS:
        d = df[df["symbol"] == sym]
        days = d["day"].unique()
        mat.loc[mat.index.isin(days), sym] = 1

    corr_full = mat.corr()
    pairs = [(a, b) for i, a in enumerate(SYMBOLS) for b in SYMBOLS[i + 1:]]
    avg_corr = np.mean([corr_full.loc[a, b] for a, b in pairs])

    # BTC 일간 절대수익률 상위 5% 국면
    btc_4h = load_klines_4h("BTCUSDT")
    btc_1d = btc_4h["close"].resample("1D").last()
    btc_ret = btc_1d.pct_change().abs()
    thresh = btc_ret.quantile(0.95)
    crisis_days = btc_ret[btc_ret >= thresh].index
    crisis_days = crisis_days.intersection(mat.index)

    if len(crisis_days) >= 5:
        mat_crisis = mat.loc[crisis_days]
        corr_crisis = mat_crisis.corr()
        avg_corr_crisis = np.mean([corr_crisis.loc[a, b] for a, b in pairs])
    else:
        avg_corr_crisis = float("nan")

    same_day_pct = float((mat.sum(axis=1) >= 2).sum() / (mat.sum(axis=1) >= 1).sum() * 100)
    all7_days = int((mat.sum(axis=1) == 7).sum())

    out = {
        "avg_pairwise_corr_full": float(avg_corr),
        "avg_pairwise_corr_crisis_top5pct_btc_absret": float(avg_corr_crisis),
        "n_crisis_days": int(len(crisis_days)),
        "pct_entry_days_with_2plus_symbols": same_day_pct,
        "n_days_all7_symbols_same_day": all7_days,
    }
    with open("out_diag_corr.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
