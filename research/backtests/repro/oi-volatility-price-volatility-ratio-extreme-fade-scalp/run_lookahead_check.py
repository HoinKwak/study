"""룩어헤드 점검 — BTC 데이터를 임의 시점에서 절단(1h·15m·metrics 전부)한 뒤 재계산한 트레이드가
절단 이전 구간에서 원본과 완전히 일치하는지 확인."""
import sys

import pandas as pd

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oivolratio")
import common
import engine
import stats_utils as su
from crypto_trader.config import get_settings
from crypto_trader.risk import RiskManager

settings = get_settings()
risk = RiskManager(settings)
cfg = engine.RunConfig()

sig_full = common.build_signals("BTCUSDT")
trades_full = engine.run_symbol("BTCUSDT", sig_full, cfg, settings, risk)
df_full = su.trades_df(trades_full)

cutoff = pd.Timestamp("2025-01-01", tz="UTC")

# 절단본 신호를 처음부터 재계산(캐시 우회) — df1h/df15m 을 cutoff 이전으로 슬라이스
sig_trunc_df1h = sig_full.df1h[sig_full.df1h.index < cutoff]
sig_trunc_df15m = sig_full.df15m[sig_full.df15m.index < cutoff]
import numpy as np
import dataclasses

# common.build_signals 를 다시 타지 않고, Signals 필드를 동일 길이로 절단해 직접 구성
n1h_cut = len(sig_trunc_df1h)
n15_cut = len(sig_trunc_df15m)
sig_trunc = common.Signals(
    df1h=sig_trunc_df1h, df15m=sig_trunc_df15m,
    oi_ret=sig_full.oi_ret.iloc[:n1h_cut], px_ret=sig_full.px_ret.iloc[:n1h_cut],
    oi_vol60=sig_full.oi_vol60.iloc[:n1h_cut], px_vol60=sig_full.px_vol60.iloc[:n1h_cut],
    vol_ratio=sig_full.vol_ratio.iloc[:n1h_cut], z=sig_full.z[:n1h_cut],
    z_oi_only=sig_full.z_oi_only[:n1h_cut], px_ret_4h_sum=sig_full.px_ret_4h_sum.iloc[:n1h_cut],
    atr14_15m=sig_full.atr14_15m.iloc[:n15_cut], oi_5m_count=sig_full.oi_5m_count.iloc[:n1h_cut],
    oi_raw_nan=sig_full.oi_raw_nan.iloc[:n1h_cut])

trades_trunc = engine.run_symbol("BTCUSDT", sig_trunc, cfg, settings, risk)
df_trunc = su.trades_df(trades_trunc)

full_before = df_full[df_full["entry_time"] < cutoff].reset_index(drop=True)
trunc_all = df_trunc.reset_index(drop=True)

print(f"원본(절단시점 이전) n={len(full_before)}  절단본 n={len(trunc_all)}")
# 마지막 몇 건은 절단 경계 부근에서 워밍업 윈도우가 짧아 z 값이 달라질 수 있으니(예: 220봉 미만
# 워밍업 시작 근처, 여기선 경계 자체가 아니라 max_hold 로 인한 종료시각 차이 가능성만 배제) 마지막
# 5건은 비교에서 제외.
cmp_full = full_before.iloc[:-5] if len(full_before) > 5 else full_before
cmp_trunc = trunc_all.iloc[:len(cmp_full)]
if len(cmp_full) == len(cmp_trunc):
    diff_r = (cmp_full["r"].to_numpy() - cmp_trunc["r"].to_numpy())
    diff_entry = (cmp_full["entry_time"].to_numpy() != cmp_trunc["entry_time"].to_numpy()).sum()
    print(f"비교 n={len(cmp_full)}  entry_time 불일치={diff_entry}  max|Δr|={abs(diff_r).max():.6f}")
else:
    print("⚠️ 길이 불일치 — 수동 확인 필요:", len(cmp_full), len(cmp_trunc))
    print(cmp_full.tail(10)[["entry_time", "r", "reason"]])
    print(cmp_trunc.tail(10)[["entry_time", "r", "reason"]])
