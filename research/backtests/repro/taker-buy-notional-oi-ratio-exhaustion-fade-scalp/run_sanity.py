"""회계정합·IS+OOS==FULL·0-fill 결측·반전대조군 청산사유/보유기간 분포·방향분포."""
import pickle

import numpy as np
import pandas as pd

import common
import stats_utils as su

with open(common.SP / "sigs_200.pkl", "rb") as f:
    sigs = pickle.load(f)
with open(common.SP / "results_main.pkl", "rb") as f:
    results = pickle.load(f)

net = results[(False, True)]
is_df, oos_df, full_df = su.split_is_oos(net)
print(f"IS n={len(is_df)} + OOS n={len(oos_df)} = {len(is_df)+len(oos_df)}  FULL n={len(full_df)}")
print(f"IS+OOS == FULL: {len(is_df)+len(oos_df) == len(full_df)}")

print("\n### 반전 대조군(reverse=True, net) — 청산사유/보유기간/방향 분포(OOS) ###")
rev = results[(True, True)]
_, rev_oos, _ = su.split_is_oos(rev)
print(rev_oos["reason"].value_counts())
print("zero_hold_frac =", (rev_oos["holding_bars"] == 0).mean())
print(rev_oos["direction"].value_counts())
print("holding_bars describe:\n", rev_oos["holding_bars"].describe())

print("\n### 0-fill 결측 점검(과거 문제구간 2024-07-09~15) — 7종목 OI raw_nan 발생 여부 ###")
for sym, sig in sigs.items():
    m5 = common.load_metrics_5m(sym)
    if m5.empty:
        continue
    sub = m5.loc[(m5.index >= pd.Timestamp("2024-07-09", tz="UTC"))
                & (m5.index <= pd.Timestamp("2024-07-15", tz="UTC"))]
    n_missing = sub["sum_open_interest_value"].isna().sum()
    print(f"  {sym:10s} n_missing(5m,해당구간)={n_missing} / {len(sub)}")

print("\n### 0-fill 결측 점검 2(2022-03-07~08) ###")
for sym, sig in sigs.items():
    m5 = common.load_metrics_5m(sym)
    if m5.empty:
        continue
    sub = m5.loc[(m5.index >= pd.Timestamp("2022-03-07", tz="UTC"))
                & (m5.index <= pd.Timestamp("2022-03-08", tz="UTC"))]
    n_missing = sub["sum_open_interest_value"].isna().sum()
    print(f"  {sym:10s} n_missing(5m,해당구간)={n_missing} / {len(sub)}")

print("\n### 회계정합: raw_pnl - fees == pnl (엔진 재실행으로 직접 확인) ###")
import engine
from crypto_trader.config import get_settings
from crypto_trader.risk import RiskManager
settings = get_settings()
risk = RiskManager(settings)
cfg = engine.RunConfig()
trades = engine.run_symbol("BTCUSDT", sigs["BTCUSDT"], cfg, settings, risk)
max_diff = 0.0
for t in trades:
    is_long = t.direction == "long"
    raw = ((t.exit_price - t.entry_price) if is_long else (t.entry_price - t.exit_price)) * t.quantity
    diff = abs((raw - t.fees) - t.pnl)
    max_diff = max(max_diff, diff)
print(f"BTCUSDT {len(trades)}건 max|raw_pnl-fees-pnl| = {max_diff:.12f}")
