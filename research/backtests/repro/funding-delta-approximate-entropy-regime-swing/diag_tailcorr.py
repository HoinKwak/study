"""종목 간 신호(진입일 이진지표) 상관 — 평시 vs 위기국면(BTC 1d 절대수익률 상위 5%) 꼬리상관."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import split_is_oos, load_klines_4h
from events import build_universe
from engine import run_variant, trades_to_df


def main() -> dict:
    uni = build_universe()
    trades = trades_to_df(run_variant(uni))
    _, oos, _ = split_is_oos(trades)

    # 종목별 일자 진입 이진지표(entry_time.dt.date)
    oos = oos.copy()
    oos["date"] = oos["entry_time"].dt.date
    symbols = sorted(oos["symbol"].unique())
    all_dates = pd.date_range(oos["entry_time"].min().normalize(), oos["entry_time"].max().normalize(),
                              freq="D")
    ind = pd.DataFrame(0, index=all_dates, columns=symbols)
    for sym in symbols:
        # ⚠️자체발견: date 객체 -> to_datetime 이 tz-naive 를 만들어 tz-aware all_dates 와
        # isin 비교가 항상 False로 조용히 실패했다(에러 없이 0건) — UTC localize 로 정정.
        d = pd.to_datetime(oos.loc[oos["symbol"] == sym, "date"]).dt.tz_localize("UTC")
        ind.loc[ind.index.isin(d.dt.normalize()), sym] = 1

    full_corr = ind.corr().values
    iu = np.triu_indices_from(full_corr, k=1)
    full_mean_corr = float(np.nanmean(full_corr[iu]))

    # BTC 1d 절대수익률 상위 5%(OOS 구간)
    btc = load_klines_4h("BTCUSDT")["close"].resample("1D").last().dropna()
    btc_ret = btc.pct_change().abs()
    btc_ret_oos = btc_ret[(btc_ret.index >= oos["entry_time"].min().normalize()) &
                          (btc_ret.index <= oos["entry_time"].max().normalize())]
    thresh = btc_ret_oos.quantile(0.95)
    crisis_days = btc_ret_oos[btc_ret_oos >= thresh].index.normalize()

    ind_crisis = ind.loc[ind.index.isin(crisis_days)]
    crisis_corr = ind_crisis.corr().values
    crisis_mean_corr = float(np.nanmean(crisis_corr[iu])) if len(ind_crisis) > 1 else float("nan")

    out = {
        "n_days_total": int(len(ind)), "n_crisis_days": int(len(ind_crisis)),
        "btc_abs_ret_p95_thresh": float(thresh),
        "normal_mean_pairwise_corr": full_mean_corr,
        "crisis_mean_pairwise_corr": crisis_mean_corr,
        "n_symbols": len(symbols),
    }
    print(json.dumps(out, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
