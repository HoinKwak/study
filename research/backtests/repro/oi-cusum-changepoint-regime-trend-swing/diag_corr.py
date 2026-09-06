"""§종목 간 신호 상관(평시 + 위기 국면). 위기 = BTC 4h |로그수익률| 상위 5% 봉."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import SYMBOLS
from signals import build_signals


def main():
    sig_btc = build_signals("BTCUSDT")
    btc_ret = np.log(sig_btc.df["close"] / sig_btc.df["close"].shift(1)).abs()
    thresh = btc_ret.quantile(0.95)
    crisis_idx = btc_ret[btc_ret >= thresh].index
    print("BTC 4h |logret| 상위5% 문턱:", thresh, "위기봉 수:", len(crisis_idx), "/", len(btc_ret))

    sigs = {s: build_signals(s) for s in SYMBOLS}
    z_all = pd.DataFrame({s: sigs[s].z for s in SYMBOLS if sigs[s] is not None})

    corr_full = z_all.corr()["BTCUSDT"].drop("BTCUSDT")
    normal_idx = z_all.index.difference(crisis_idx)
    corr_normal = z_all.loc[z_all.index.intersection(normal_idx)].corr()["BTCUSDT"].drop("BTCUSDT")
    corr_crisis = z_all.loc[z_all.index.intersection(crisis_idx)].corr()["BTCUSDT"].drop("BTCUSDT")

    print("\nz(t) 상관(BTC 대비) 전체구간:\n", corr_full.to_string())
    print("\n평시:\n", corr_normal.to_string())
    print("\n위기국면(BTC 상위5%):\n", corr_crisis.to_string())

    # 체인지포인트(원시, 방향무관) 동시발생율 — ±1일(6봉) 이내, 평시 vs 위기
    from events import raw_cp_events
    cp_by_sym = {s: raw_cp_events(sigs[s]) for s in SYMBOLS if sigs[s] is not None}
    btc_cp_times = pd.DatetimeIndex(cp_by_sym["BTCUSDT"]["cp_time"])
    tol = pd.Timedelta(days=1)

    def co_rate(sym: str, time_filter: pd.DatetimeIndex | None) -> tuple[int, int]:
        times = pd.DatetimeIndex(cp_by_sym[sym]["cp_time"])
        if time_filter is not None:
            times = times[times.isin(time_filter)]
            base_times = btc_cp_times[btc_cp_times.isin(time_filter)]
        else:
            base_times = btc_cp_times
        if len(base_times) == 0:
            return (0, 0)
        hits = 0
        for t in base_times:
            if len(times) and (np.abs(times - t) <= tol).any():
                hits += 1
        return hits, len(base_times)

    co_full, co_normal, co_crisis = {}, {}, {}
    for s in SYMBOLS:
        if s == "BTCUSDT":
            continue
        h, n = co_rate(s, None)
        co_full[s] = f"{h}/{n}"
        h, n = co_rate(s, normal_idx)
        co_normal[s] = f"{h}/{n}"
        h, n = co_rate(s, crisis_idx)
        co_crisis[s] = f"{h}/{n}"

    print("\nBTC CP ±1일 동시발생(다른 심볼) — 전체:", co_full)
    print("평시:", co_normal)
    print("위기:", co_crisis)

    out = {
        "crisis_bars": int(len(crisis_idx)), "total_bars": int(len(btc_ret)),
        "corr_full": corr_full.to_dict(), "corr_normal": corr_normal.to_dict(),
        "corr_crisis": corr_crisis.to_dict(),
        "cp_co_occurrence_full": co_full, "cp_co_occurrence_normal": co_normal,
        "cp_co_occurrence_crisis": co_crisis,
    }
    with open("out_diag_corr.json", "w") as f:
        json.dump(out, f, indent=2, default=str)


if __name__ == "__main__":
    main()
