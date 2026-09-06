"""룩어헤드 절단검증: 임의 절단점 이전 데이터만으로 재계산한 신호가 절단점 이전 구간에서 전체
이력으로 계산한 신호와 완전히 일치하는지 확인(BTC + 3종목: ETH/SOL/ADA)."""
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
    df = common.load_klines_15m(symbol)
    df_t = df[df.index <= cutoff].copy()

    volume = df_t["volume"]
    taker_buy = df_t["taker_buy_volume"]
    close = df_t["close"]
    valid_bar = volume > 0
    ratio = (taker_buy / volume).where(valid_bar)
    buy_led = (valid_bar & (ratio > 0.5)).to_numpy()
    sell_led = (valid_bar & (ratio <= 0.5)).to_numpy()
    sv = 2.0 * taker_buy - volume
    delta_close = close.diff()
    sv_np = sv.to_numpy(float)
    dc_np = delta_close.to_numpy(float)

    lambda_buy, _ = common._masked_rolling_ols_slope(sv_np, dc_np, buy_led, common.LAMBDA_WINDOW,
                                                     common.MIN_SAMPLES_PER_SIDE)
    lambda_sell, _ = common._masked_rolling_ols_slope(sv_np, dc_np, sell_led, common.LAMBDA_WINDOW,
                                                      common.MIN_SAMPLES_PER_SIDE)
    lambda_gap = pd.Series(lambda_sell - lambda_buy, index=df_t.index)
    gap_pctile = common.rolling_pctile_of_last(lambda_gap, common.GAP_PCTILE_WINDOW)
    sv3 = sv.rolling(3, min_periods=3).sum()
    sv3_abs_pctile = common.rolling_pctile_of_last(sv3.abs(), common.GAP_PCTILE_WINDOW)
    from crypto_trader.signals import indicators as ind
    atr14 = ind.atr(df_t, 14)

    return dict(df=df_t, gap_pctile=gap_pctile, sv3_abs_pctile=sv3_abs_pctile, sv3=sv3, atr14=atr14)


for symbol, cutoff in CUTS.items():
    full = common.build_signals(symbol)
    trunc = build_truncated(symbol, cutoff)

    common_idx = trunc["df"].index
    n = len(common_idx)

    diffs = {}
    for name, full_s, trunc_s in [
        ("gap_pctile", full.gap_pctile, trunc["gap_pctile"]),
        ("sv3_abs_pctile", full.sv3_abs_pctile, trunc["sv3_abs_pctile"]),
        ("sv3", full.sv3, trunc["sv3"]),
        ("atr14", full.atr14, trunc["atr14"]),
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
