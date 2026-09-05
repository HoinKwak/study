"""룩어헤드 점검 — 데이터를 임의 시점에서 절단(1h·15m 전부)한 뒤 재계산한 트레이드가 절단
이전 구간에서 원본과 완전히 일치하는지 확인. BTC 외 3종목 추가(ETH·XRP·DOGE), 절단시점 2개."""
from __future__ import annotations

import pandas as pd

import common
import engine
import stats_utils as su
from crypto_trader.config import get_settings
from crypto_trader.risk import RiskManager

settings = get_settings()
risk = RiskManager(settings)
cfg = engine.RunConfig()


def build_truncated(sig_full: common.Signals, cutoff: pd.Timestamp) -> common.Signals:
    d15 = sig_full.df15m[sig_full.df15m.index < cutoff]
    d1h = sig_full.df1h[sig_full.df1h.index < cutoff]
    n1h = len(d1h)
    n15 = len(d15)
    return common.Signals(
        df1h=d1h, df15m=d15,
        ar_spread=sig_full.ar_spread.iloc[:n1h], ar_cov=sig_full.ar_cov.iloc[:n1h],
        ar_product=sig_full.ar_product.iloc[:n1h], ar_pctile=sig_full.ar_pctile.iloc[:n1h],
        atrp=sig_full.atrp.iloc[:n1h], atrp_pctile=sig_full.atrp_pctile.iloc[:n1h],
        rv=sig_full.rv.iloc[:n1h], hlrange=sig_full.hlrange.iloc[:n1h],
        roll_sp=sig_full.roll_sp.iloc[:n1h], cs_sp=sig_full.cs_sp.iloc[:n1h],
        atr14_1h=sig_full.atr14_1h.iloc[:n1h], bb_mid=sig_full.bb_mid.iloc[:n1h],
        bb_upper=sig_full.bb_upper.iloc[:n1h], bb_lower=sig_full.bb_lower.iloc[:n1h],
        atr14_15m=sig_full.atr14_15m.iloc[:n15])


def check_one(symbol: str, cutoff: pd.Timestamp) -> None:
    sig_full = common.build_signals(symbol)
    trades_full = engine.run_symbol(symbol, sig_full, cfg, settings, risk)
    df_full = su.trades_df(trades_full)

    sig_trunc = build_truncated(sig_full, cutoff)
    trades_trunc = engine.run_symbol(symbol, sig_trunc, cfg, settings, risk)
    df_trunc = su.trades_df(trades_trunc)

    full_before = df_full[df_full["entry_time"] < cutoff].reset_index(drop=True)
    trunc_all = df_trunc.reset_index(drop=True)

    print(f"[{symbol} cutoff={cutoff.date()}] 원본(절단이전) n={len(full_before)}  절단본 n={len(trunc_all)}")
    # 절단 경계 부근 마지막 몇 건은 max_hold(12봉=3h)로 인한 종료시각 이동 가능성이 있어
    # 마지막 5건은 비교에서 제외.
    cmp_full = full_before.iloc[:-5] if len(full_before) > 5 else full_before
    cmp_trunc = trunc_all.iloc[:len(cmp_full)]
    if len(cmp_full) == len(cmp_trunc) and len(cmp_full) > 0:
        diff_r = (cmp_full["r"].to_numpy() - cmp_trunc["r"].to_numpy())
        diff_entry = (cmp_full["entry_time"].to_numpy() != cmp_trunc["entry_time"].to_numpy()).sum()
        print(f"  비교 n={len(cmp_full)}  entry_time 불일치={diff_entry}  max|Δr|={abs(diff_r).max():.10f}")
    elif len(cmp_full) == 0:
        print("  비교표본 0건(절단 이전 신호 없음) — 스킵")
    else:
        print(f"  ⚠️ 길이 불일치 — 수동 확인 필요: full={len(cmp_full)} trunc={len(cmp_trunc)}")
        print(cmp_full.tail(10)[["entry_time", "r", "reason"]])
        print(cmp_trunc.tail(10)[["entry_time", "r", "reason"]])


if __name__ == "__main__":
    for sym in ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT"]:
        for cutoff in [pd.Timestamp("2024-01-01", tz="UTC"), pd.Timestamp("2025-06-01", tz="UTC")]:
            check_one(sym, cutoff)
