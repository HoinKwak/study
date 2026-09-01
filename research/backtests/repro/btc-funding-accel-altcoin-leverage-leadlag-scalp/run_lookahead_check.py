"""룩어헤드 점검: 데이터를 임의 시점에서 절단해도 절단 이전 구간의 트레이드가 완전 재현되는지 확인."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
import common
import engine

CUT = pd.Timestamp("2025-01-01", tz="UTC")

# --- 절단 없는 원본 ---
fa_full = common.build_funding_accel("BTCUSDT", window=60)
events_full = common.find_accel_events(fa_full, accel_z_threshold=1.5)
alts_full = engine.load_all_alts()
cfg = engine.RunConfig()
res_full = engine.run_all(alts_full, events_full, cfg)
full_trades = pd.concat([engine.trades_to_df(t) for t in res_full.values()], ignore_index=True)
full_before_cut = full_trades[pd.to_datetime(full_trades["entry_time"]) < CUT]

# --- CUT 이후 원본 데이터를 실제로 잘라서 재실행 ---
funding_df = common.load_funding("BTCUSDT")
funding_trunc = funding_df[funding_df.index < CUT]
delta = funding_trunc["last_funding_rate"].diff()
roll_std = delta.rolling(60, min_periods=60).std(ddof=0)
fa_trunc = common.FundingAccel(df=funding_trunc, delta=delta, roll_std=roll_std)
events_trunc = common.find_accel_events(fa_trunc, accel_z_threshold=1.5)

alts_trunc = {}
for sym in common.ALT_SYMBOLS:
    a = alts_full[sym]
    df15_trunc = a.df[a.df.index < CUT]
    n_trunc = len(df15_trunc)
    alts_trunc[sym] = common.AltSignals(
        df=df15_trunc,
        don_upper=a.don_upper.iloc[:n_trunc],
        don_lower=a.don_lower.iloc[:n_trunc],
        vol_avg=a.vol_avg.iloc[:n_trunc],
        atr1h_on15=a.atr1h_on15[:n_trunc],
    )

res_trunc = engine.run_all(alts_trunc, events_trunc, cfg)
trunc_trades = pd.concat([engine.trades_to_df(t) for t in res_trunc.values()], ignore_index=True)

print("절단 전 원본 트레이드 수(진입<CUT):", len(full_before_cut))
print("절단 재실행 트레이드 수(전체):", len(trunc_trades))

# 마지막 근처 트레이드는 절단 경계효과(진행 중 포지션 강제종료 등)로 다를 수 있어
# CUT 며칠 전(entry_time < CUT - 2일)까지만 엄격 비교
safe_cut = CUT - pd.Timedelta(days=2)
a = full_before_cut[pd.to_datetime(full_before_cut["entry_time"]) < safe_cut].sort_values(
    ["symbol", "entry_time"]).reset_index(drop=True)
b = trunc_trades[pd.to_datetime(trunc_trades["entry_time"]) < safe_cut].sort_values(
    ["symbol", "entry_time"]).reset_index(drop=True)

print("\n안전구간(entry<CUT-2일) 원본 n:", len(a), " 절단재실행 n:", len(b))
cols = ["symbol", "entry_time", "entry_price", "stop_price", "exit_time", "exit_price",
        "exit_reason", "pnl", "r_multiple"]
if len(a) == len(b):
    diff = (a[cols].astype(str) != b[cols].astype(str))
    mismatch = diff.any(axis=1).sum()
    print("불일치 행 수:", mismatch, "/", len(a))
    if mismatch > 0:
        print(a[diff.any(axis=1)][cols].head(10))
        print(b[diff.any(axis=1)][cols].head(10))
else:
    print("⚠️ 트레이드 수 자체가 다름 — 상세 비교 필요")
    print(a[cols].tail(5))
    print(b[cols].tail(5))
