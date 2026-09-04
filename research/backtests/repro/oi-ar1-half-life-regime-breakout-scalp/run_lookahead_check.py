"""룩어헤드 점검 — 데이터를 임의 시점에서 절단(1h·15m·metrics 전부)한 뒤 재계산한 트레이드가
절단 이전 구간에서 원본과 완전히 일치하는지 확인. 여러 종목·여러 절단시점으로 확장."""
import sys

import pandas as pd

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiar1hl")
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
    n15 = len(d15)
    n1h = len(d1h)
    return common.Signals(
        df1h=d1h, df15m=d15,
        oi_growth=sig_full.oi_growth.iloc[:n15], phi=sig_full.phi.iloc[:n15],
        phi_pctile=sig_full.phi_pctile.iloc[:n15], oi_z=sig_full.oi_z.iloc[:n15],
        oi_z_pctile=sig_full.oi_z_pctile.iloc[:n15], oi_change_stdev=sig_full.oi_change_stdev.iloc[:n15],
        donch_upper=sig_full.donch_upper.iloc[:n15], donch_lower=sig_full.donch_lower.iloc[:n15],
        donch_mid10=sig_full.donch_mid10.iloc[:n15], atr14_15m=sig_full.atr14_15m.iloc[:n15],
        ema20_1h=sig_full.ema20_1h.iloc[:n1h], atr14_1h=sig_full.atr14_1h.iloc[:n1h],
        oi_5m_count=sig_full.oi_5m_count.iloc[:n15], oi_raw_nan=sig_full.oi_raw_nan.iloc[:n15])


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
    # 절단 경계 부근 마지막 몇 건은 max_hold(24봉=6h) 로 인한 종료시각 이동 가능성이 있어 안전하게
    # 마지막 5건은 비교에서 제외.
    cmp_full = full_before.iloc[:-5] if len(full_before) > 5 else full_before
    cmp_trunc = trunc_all.iloc[:len(cmp_full)]
    if len(cmp_full) == len(cmp_trunc) and len(cmp_full) > 0:
        diff_r = (cmp_full["r"].to_numpy() - cmp_trunc["r"].to_numpy())
        diff_entry = (cmp_full["entry_time"].to_numpy() != cmp_trunc["entry_time"].to_numpy()).sum()
        print(f"  비교 n={len(cmp_full)}  entry_time 불일치={diff_entry}  max|Δr|={abs(diff_r).max():.8f}")
    elif len(cmp_full) == 0:
        print("  비교표본 0건(절단 이전 신호 없음) — 스킵")
    else:
        print(f"  ⚠️ 길이 불일치 — 수동 확인 필요: full={len(cmp_full)} trunc={len(cmp_trunc)}")
        print(cmp_full.tail(10)[["entry_time", "r", "reason"]])
        print(cmp_trunc.tail(10)[["entry_time", "r", "reason"]])


for sym in ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT"]:
    for cutoff in [pd.Timestamp("2024-01-01", tz="UTC"), pd.Timestamp("2025-06-01", tz="UTC")]:
        check_one(sym, cutoff)
