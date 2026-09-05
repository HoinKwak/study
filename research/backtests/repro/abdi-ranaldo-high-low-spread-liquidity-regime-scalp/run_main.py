"""메인 실행: 기본안(net/gross) + 서브모드별 분리 + 대조군 4종 + de-clustering + LOO."""
from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd

import common
import engine
import stats_utils as su
from crypto_trader.config import get_settings
from crypto_trader.risk import RiskManager

CACHE = common.SP / "signals_cache.pkl"


def get_signals(force: bool = False) -> dict[str, common.Signals]:
    if not force and CACHE.exists():
        with open(CACHE, "rb") as f:
            return pickle.load(f)
    sigs = engine.load_all_signals()
    with open(CACHE, "wb") as f:
        pickle.dump(sigs, f)
    return sigs


def run_cfg(sigs, cfg: engine.RunConfig) -> pd.DataFrame:
    settings = get_settings()
    risk = RiskManager(settings)
    all_trades = []
    for sym, sig in sigs.items():
        all_trades.extend(engine.run_symbol(sym, sig, cfg, settings, risk))
    return su.trades_df(all_trades)


def per_symbol_table(df: pd.DataFrame, label: str) -> None:
    print(f"--- {label}: 종목별 OOS ---")
    _, oos_df, _ = su.split_is_oos(df)
    for sym, g in oos_df.groupby("symbol"):
        print(" ", su.print_summary(su.summary(g, sym)))


def main():
    t0 = time.time()
    sigs = get_signals()
    print(f"signals loaded n_symbols={len(sigs)} t={time.time()-t0:.1f}s")

    # ---------------- 기본안(net) ----------------
    cfg = engine.RunConfig()
    df = run_cfg(sigs, cfg)
    is_df, oos_df, full_df = su.split_is_oos(df)
    print("\n===== 기본안(net, fee+slippage 0.14%) =====")
    print(su.print_summary(su.summary(is_df, "IS")))
    print(su.print_summary(su.summary(oos_df, "OOS")))
    print(su.print_summary(su.summary(full_df, "FULL")))
    print(f"IS+OOS={len(is_df)+len(oos_df)} FULL={len(full_df)}")
    per_symbol_table(df, "기본안")
    print("reason 분포(OOS):", oos_df["reason"].value_counts().to_dict())
    print("모드분포(OOS):", oos_df["mode"].value_counts().to_dict())

    # 서브모드별 분리
    for m in ["M", "R"]:
        sub = oos_df[oos_df["mode"] == m]
        print(f"  [서브모드 {m}] " + su.print_summary(su.summary(sub, f"OOS-{m}")))

    # ---------------- gross(fee=0, slippage=0) ----------------
    cfg_gross = engine.RunConfig(fee_on=False)
    dfg = run_cfg(sigs, cfg_gross)
    is_g, oos_g, full_g = su.split_is_oos(dfg)
    print("\n===== gross(fee=0, slippage=0) =====")
    print(su.print_summary(su.summary(is_g, "IS-gross")))
    print(su.print_summary(su.summary(oos_g, "OOS-gross")))
    print(su.print_summary(su.summary(full_g, "FULL-gross")))

    # ---------------- 대조군 ----------------
    print("\n===== 대조군 =====")
    cfg_none = engine.RunConfig(gate="none")
    df_none = run_cfg(sigs, cfg_none)
    _, oos_none, _ = su.split_is_oos(df_none)
    print("① 게이트없음 " + su.print_summary(su.summary(oos_none, "OOS-none")))

    cfg_atrp = engine.RunConfig(gate="atrp")
    df_atrp = run_cfg(sigs, cfg_atrp)
    _, oos_atrp, _ = su.split_is_oos(df_atrp)
    print("② ATR%게이트 " + su.print_summary(su.summary(oos_atrp, "OOS-atrp")))

    cfg_rev_regime = engine.RunConfig(gate="reverse_regime")
    df_rev_regime = run_cfg(sigs, cfg_rev_regime)
    _, oos_rev_regime, _ = su.split_is_oos(df_rev_regime)
    print("③ 레짐반전 " + su.print_summary(su.summary(oos_rev_regime, "OOS-regime_rev")))

    cfg_rev_dir = engine.RunConfig(direction_mode="reverse")
    df_rev_dir = run_cfg(sigs, cfg_rev_dir)
    _, oos_rev_dir, _ = su.split_is_oos(df_rev_dir)
    print("④ 방향반전 " + su.print_summary(su.summary(oos_rev_dir, "OOS-dir_rev")))

    cfg_rev_dir2 = engine.RunConfig(direction_mode="reverse_noinvalidation")
    df_rev_dir2 = run_cfg(sigs, cfg_rev_dir2)
    _, oos_rev_dir2, _ = su.split_is_oos(df_rev_dir2)
    print("④' 방향반전(무효화청산비활성) " + su.print_summary(su.summary(oos_rev_dir2, "OOS-dir_rev_noinval")))

    # ---------------- de-clustering(net) ----------------
    print("\n===== de-clustering(net, OOS) =====")
    cal = su.decluster_calendar_day(oos_df)
    print(" 캘린더일:", su.print_summary(su.summary(cal, "cal-day")))
    for w in (3, 4, 5):
        roll = su.decluster_rolling_days(oos_df, window_days=w)
        print(f" {w}일 롤링:", su.print_summary(su.summary(roll, f"roll-{w}d")))

    print("\n===== de-clustering(gross, OOS) =====")
    cal_g = su.decluster_calendar_day(oos_g)
    print(" 캘린더일:", su.print_summary(su.summary(cal_g, "cal-day-gross")))
    for w in (3, 4, 5):
        roll_g = su.decluster_rolling_days(oos_g, window_days=w)
        print(f" {w}일 롤링:", su.print_summary(su.summary(roll_g, f"roll-{w}d-gross")))

    # ---------------- LOO ----------------
    print("\n===== LOO(종목 제외, OOS net) =====")
    for sym in common.SYMBOLS:
        sub = oos_df[oos_df["symbol"] != sym]
        print(f" {sym} 제외:", su.print_summary(su.summary(sub, f"loo-ex-{sym}")))

    # ---------------- 저장 ----------------
    out = dict(
        base_is=su.summary(is_df, "IS"), base_oos=su.summary(oos_df, "OOS"),
        base_full=su.summary(full_df, "FULL"),
        gross_is=su.summary(is_g, "IS-gross"), gross_oos=su.summary(oos_g, "OOS-gross"),
        gross_full=su.summary(full_g, "FULL-gross"),
        ctrl_none=su.summary(oos_none, "none"), ctrl_atrp=su.summary(oos_atrp, "atrp"),
        ctrl_regime_rev=su.summary(oos_rev_regime, "regime_rev"),
        ctrl_dir_rev=su.summary(oos_rev_dir, "dir_rev"),
        ctrl_dir_rev2=su.summary(oos_rev_dir2, "dir_rev_noinval"),
    )
    with open(common.SP / "trades_all.pkl", "wb") as f:
        pickle.dump(dict(base=df, gross=dfg, none=df_none, atrp=df_atrp,
                         regime_rev=df_rev_regime, dir_rev=df_rev_dir,
                         dir_rev2=df_rev_dir2), f)
    with open(common.SP / "main_summary.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\n총 실행시간 {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
