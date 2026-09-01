"""메인 백테스트: 채택안(accel_z=1.5, confirm_window=8h) 전 구간/IS/OOS/종목별."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
import common
import engine
import stats_utils as su

fa = common.build_funding_accel("BTCUSDT", window=60)
events = common.find_accel_events(fa, accel_z_threshold=1.5)
alts = engine.load_all_alts()

cfg = engine.RunConfig()
res = engine.run_all(alts, events, cfg)

all_trades = []
for sym, trades in res.items():
    df = engine.trades_to_df(trades)
    all_trades.append(df)
full = pd.concat(all_trades, ignore_index=True) if all_trades else pd.DataFrame()
full.to_csv(common.SP / "trades_main.csv", index=False)

print("=== 종목별 트레이드 수 ===")
for sym, trades in res.items():
    print(f"  {sym}: {len(trades)}")

print("\n=== IS/OOS/FULL 분할 (전종목 합산) ===")


def split(df):
    et = pd.to_datetime(df["entry_time"])
    is_ = df[et <= common.IS_END]
    oos = df[(et >= common.OOS_START) & (et <= common.OOS_END)]
    return is_, oos


is_df, oos_df = split(full)
print("FULL:", su.summarize(full["r_multiple"].to_numpy(), "FULL"))
print("IS  :", su.summarize(is_df["r_multiple"].to_numpy(), "IS"))
print("OOS :", su.summarize(oos_df["r_multiple"].to_numpy(), "OOS"))

print("\n=== 종목별 OOS ===")
for sym in common.ALT_SYMBOLS:
    sub = oos_df[oos_df["symbol"] == sym]
    print(f"  {sym}:", su.summarize(sub["r_multiple"].to_numpy(), sym))

print("\n=== 청산사유 분포(FULL) ===")
print(full["exit_reason"].value_counts())

print("\n=== IS+OOS == FULL 검증 ===")
print("IS+OOS n:", len(is_df) + len(oos_df), "FULL n:", len(full))

print("\n=== gross(fee=0,slip=0) 진단 ===")
cfg_gross = engine.RunConfig(fee_on=False)
res_gross = engine.run_all(alts, events, cfg_gross)
all_g = [engine.trades_to_df(t) for t in res_gross.values()]
full_g = pd.concat(all_g, ignore_index=True) if all_g else pd.DataFrame()
is_g, oos_g = split(full_g)
print("gross FULL:", su.summarize(full_g["r_multiple"].to_numpy(), "gross FULL"))
print("gross IS  :", su.summarize(is_g["r_multiple"].to_numpy(), "gross IS"))
print("gross OOS :", su.summarize(oos_g["r_multiple"].to_numpy(), "gross OOS"))
full_g.to_csv(common.SP / "trades_main_gross.csv", index=False)

print("\n=== 트리거 이벤트 요약 ===")
print("total events:", len(events))
ev_is = events[events["trigger_time"] <= common.IS_END]
ev_oos = events[(events["trigger_time"] >= common.OOS_START) & (events["trigger_time"] <= common.OOS_END)]
print("IS events:", len(ev_is), "OOS events:", len(ev_oos))
