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


def build_truncated(symbol: str, cutoff: pd.Timestamp) -> common.Signals:
    df1h = common.load_klines_1h(symbol)
    df15m = common.load_klines_15m(symbol)
    m5 = common.load_metrics_5m(symbol)
    df1h_t = df1h[df1h.index <= cutoff]
    df15m_t = df15m[df15m.index <= cutoff]
    m5_t = m5[m5.index <= cutoff]

    oi15 = common.oi_15m_from_5m(m5_t)
    df15m_t = df15m_t.join(oi15, how="left")
    df15m_t.index = df15m_t.index.as_unit("ns")
    df1h_t.index = df1h_t.index.as_unit("ns")

    idx = df15m_t.index
    gap_min = idx.to_series().diff().dt.total_seconds() / 60.0
    gap_too_large = (gap_min > 15.0 + 1e-6).to_numpy()
    oi_delta = df15m_t["oi"].diff()
    oi_delta = oi_delta.where(~gap_too_large)

    win_norm = common.ZCR_NORMALIZE_WINDOW_DAYS * common.BARS_PER_DAY_15M
    sign = np.sign(oi_delta.to_numpy(float))
    sign_prev = np.roll(sign, 1)
    sign_prev[0] = np.nan
    valid_pair = np.isfinite(sign) & np.isfinite(sign_prev) & (sign != 0) & (sign_prev != 0)
    crossing = np.where(valid_pair, (sign != sign_prev).astype(float), np.nan)
    crossing_s = pd_series = __import__("pandas").Series(crossing, index=df15m_t.index)
    zcr = crossing_s.rolling(common.ZCR_MAX_TRANSITIONS,
                             min_periods=common.ZCR_MAX_TRANSITIONS).mean()
    zcr_pctile = common.rolling_pctile_of_last(zcr, win_norm)
    oi_cumsum_window = oi_delta.rolling(common.ZCR_WINDOW, min_periods=common.ZCR_WINDOW).sum()

    high, low = df15m_t["high"], df15m_t["low"]
    donch_upper = high.shift(1).rolling(common.DONCHIAN_LB).max()
    donch_lower = low.shift(1).rolling(common.DONCHIAN_LB).min()

    return dict(df15m=df15m_t, zcr=zcr, zcr_pctile=zcr_pctile,
               oi_cumsum_window=oi_cumsum_window, donch_upper=donch_upper, donch_lower=donch_lower)


for symbol, cutoff in CUTS.items():
    full = common.build_signals(symbol)
    trunc = build_truncated(symbol, cutoff)

    common_idx = trunc["df15m"].index
    n = len(common_idx)

    diffs = {}
    for name, full_s, trunc_s in [
        ("zcr", full.zcr, trunc["zcr"]),
        ("zcr_pctile", full.zcr_pctile, trunc["zcr_pctile"]),
        ("oi_cumsum_window", full.oi_cumsum_window, trunc["oi_cumsum_window"]),
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
