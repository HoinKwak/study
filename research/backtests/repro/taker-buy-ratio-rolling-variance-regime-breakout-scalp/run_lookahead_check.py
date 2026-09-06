"""룩어헤드 절단검증: 임의 절단점 이전 데이터만으로 재계산한 신호가 절단점 이전 구간에서
전체 이력으로 계산한 신호와 완전히 일치하는지 확인(4종목: BTC/ETH/SOL/ADA)."""
import numpy as np
import pandas as pd

import common

CUTS = {
    "BTCUSDT": pd.Timestamp("2024-03-15 00:00:00", tz="UTC"),
    "ETHUSDT": pd.Timestamp("2023-11-01 00:00:00", tz="UTC"),
    "SOLUSDT": pd.Timestamp("2025-02-20 00:00:00", tz="UTC"),
    "ADAUSDT": pd.Timestamp("2022-09-10 00:00:00", tz="UTC"),
}


def build_truncated(symbol: str, cutoff: pd.Timestamp) -> dict:
    df1h = common.load_klines_1h(symbol)
    df15m = common.load_klines_15m(symbol)
    m5 = common.load_metrics_5m(symbol)
    df1h_t = df1h[df1h.index <= cutoff]
    df15m_t = df15m[df15m.index <= cutoff]
    m5_t = m5[m5.index <= cutoff]

    tvr15 = common.tvr_15m_from_5m(m5_t)  # ffill(limit=4) 버그수정 반영판(common.py 참조)
    df15m_t = df15m_t.join(tvr15, how="left")
    df15m_t.index = df15m_t.index.as_unit("ns")
    df1h_t.index = df1h_t.index.as_unit("ns")

    idx = df15m_t.index
    gap_min = idx.to_series().diff().dt.total_seconds() / 60.0
    gap_too_large = (gap_min > 15.0 + 1e-6).to_numpy()
    tvr = df15m_t["tvr"].where(~gap_too_large)

    win_norm = common.TVR_NORMALIZE_WINDOW_DAYS * common.BARS_PER_DAY_15M
    tvr_std = tvr.rolling(common.TVR_WINDOW, min_periods=common.TVR_WINDOW).std(ddof=0)
    tvr_std_pctile = common.rolling_pctile_of_last(tvr_std, win_norm)
    tvr_mean_window = tvr.rolling(common.TVR_WINDOW, min_periods=common.TVR_WINDOW).mean()

    high, low = df15m_t["high"], df15m_t["low"]
    donch_upper = high.shift(1).rolling(common.DONCHIAN_LB).max()
    donch_lower = low.shift(1).rolling(common.DONCHIAN_LB).min()

    return dict(df15m=df15m_t, tvr_std=tvr_std, tvr_std_pctile=tvr_std_pctile,
               tvr_mean_window=tvr_mean_window, donch_upper=donch_upper, donch_lower=donch_lower)


for symbol, cutoff in CUTS.items():
    full = common.build_signals(symbol)
    trunc = build_truncated(symbol, cutoff)

    common_idx = trunc["df15m"].index
    n = len(common_idx)

    diffs = {}
    for name, full_s, trunc_s in [
        ("tvr_std", full.tvr_std, trunc["tvr_std"]),
        ("tvr_std_pctile", full.tvr_std_pctile, trunc["tvr_std_pctile"]),
        ("tvr_mean_window", full.tvr_mean_window, trunc["tvr_mean_window"]),
        ("donch_upper", full.donch_upper, trunc["donch_upper"]),
        ("donch_lower", full.donch_lower, trunc["donch_lower"]),
    ]:
        fs = full_s.reindex(common_idx)
        ts = trunc_s.reindex(common_idx)
        both_finite = fs.notna() & ts.notna()
        diff = (fs - ts).abs()
        max_diff = diff[both_finite].max() if both_finite.any() else float("nan")
        n_mismatch_na = (fs.notna() != ts.notna()).sum()
        diffs[name] = (max_diff, n_mismatch_na, both_finite.sum())

    print(f"=== {symbol} cutoff={cutoff} n_bars(trunc)={n} ===")
    for name, (max_diff, n_mismatch_na, n_both) in diffs.items():
        print(f"  {name:20s} max|diff|={max_diff!r:>12}  NA불일치={n_mismatch_na:4d}  "
             f"공통유효={n_both}")
