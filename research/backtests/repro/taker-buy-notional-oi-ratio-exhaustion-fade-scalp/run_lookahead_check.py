"""룩어헤드 점검 — BTC 데이터를 2025-01-01 에서 절단(15m·1h·metrics 전부)한 뒤 재계산한 트레이드가
절단 이전 구간에서 원본과 완전히 일치하는지 확인. 2종목(BTC/XRP) 각각 절단 시점을 달리해 확인."""
import sys

import numpy as np
import pandas as pd

import common
import engine
import stats_utils as su
from crypto_trader.config import get_settings
from crypto_trader.risk import RiskManager

settings = get_settings()
risk = RiskManager(settings)
cfg = engine.RunConfig()


def check(symbol: str, cutoff_str: str):
    cutoff = pd.Timestamp(cutoff_str, tz="UTC")
    sig_full = common.build_signals(symbol)
    trades_full = engine.run_symbol(symbol, sig_full, cfg, settings, risk)
    df_full = su.trades_df(trades_full)

    df15_c = sig_full.df15m[sig_full.df15m.index < cutoff]
    df1h_c = sig_full.df1h[sig_full.df1h.index < cutoff]
    n15c = len(df15_c)
    n1hc = len(df1h_c)

    completed_1h_idx_c = common._completed_1h_counts(df1h_c.index, df15_c.index.asi8)

    sig_trunc = common.Signals(
        symbol=symbol, df15m=df15_c, df1h=df1h_c,
        flow_buy_ratio=sig_full.flow_buy_ratio.iloc[:n15c],
        flow_sell_ratio=sig_full.flow_sell_ratio.iloc[:n15c],
        z_buy=sig_full.z_buy[:n15c], z_sell=sig_full.z_sell[:n15c],
        body_ratio=sig_full.body_ratio.iloc[:n15c],
        atr14_15m=sig_full.atr14_15m.iloc[:n15c],
        flow_total_ratio=sig_full.flow_total_ratio.iloc[:n15c], z_total=sig_full.z_total[:n15c],
        taker_buy_frac=sig_full.taker_buy_frac.iloc[:n15c], vol24h=sig_full.vol24h.iloc[:n15c],
        flow_vol24h_buy_ratio=sig_full.flow_vol24h_buy_ratio.iloc[:n15c],
        flow_vol24h_sell_ratio=sig_full.flow_vol24h_sell_ratio.iloc[:n15c],
        z_vol24h_buy=sig_full.z_vol24h_buy[:n15c], z_vol24h_sell=sig_full.z_vol24h_sell[:n15c],
        z_volume=sig_full.z_volume[:n15c], oi_pct_change=sig_full.oi_pct_change.iloc[:n15c],
        completed_1h_idx=completed_1h_idx_c, ema20_1h_slope=sig_full.ema20_1h_slope[:n1hc])

    trades_trunc = engine.run_symbol(symbol, sig_trunc, cfg, settings, risk)
    df_trunc = su.trades_df(trades_trunc)

    full_before = df_full[df_full["entry_time"] < cutoff].reset_index(drop=True)
    trunc_all = df_trunc.reset_index(drop=True)

    print(f"[{symbol} cutoff={cutoff_str}] 원본(절단시점 이전) n={len(full_before)}  "
         f"절단본 n={len(trunc_all)}")
    # 절단 경계 부근 마지막 몇 건은 워밍업/ATR lookback 차이로 달라질 수 있어 마지막 5건 제외.
    cmp_full = full_before.iloc[:-5] if len(full_before) > 5 else full_before
    cmp_trunc = trunc_all.iloc[:len(cmp_full)]
    if len(cmp_full) == len(cmp_trunc) and len(cmp_full) > 0:
        diff_r = (cmp_full["r"].to_numpy() - cmp_trunc["r"].to_numpy())
        diff_entry = (cmp_full["entry_time"].to_numpy() != cmp_trunc["entry_time"].to_numpy()).sum()
        diff_dir = (cmp_full["direction"].to_numpy() != cmp_trunc["direction"].to_numpy()).sum()
        print(f"  비교 n={len(cmp_full)}  entry_time 불일치={diff_entry}  direction 불일치={diff_dir} "
             f"max|Δr|={abs(diff_r).max():.8f}")
    else:
        print("  ⚠️ 길이 불일치 — 수동 확인 필요:", len(cmp_full), len(cmp_trunc))
        print(cmp_full.tail(10)[["entry_time", "r", "reason"]])
        print(cmp_trunc.tail(10)[["entry_time", "r", "reason"]])


check("BTCUSDT", "2025-01-01")
check("XRPUSDT", "2024-06-01")
