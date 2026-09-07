"""메인 분석 — base 파라미터로 7종목 신호 생성·체결·IS/OOS/FULL 집계."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from common import SYMBOLS, pf_r, t_stat, win_rate, split_is_oos
from signals import build_signals
from events import gated_entries
from engine import simulate_trades, trades_to_df
from control import gate_none_entries, zscore_gate_entries

HERE = Path(__file__).resolve().parent

BASE = dict(gc_window=60, gc_lag=4, p_sig=0.05, p_insig=0.10,
           stop_mult=1.6, atr_trail_mult=2.2, max_hold_bars=18)


def run_variant(gc_window=60, gc_lag=4, p_sig=0.05, p_insig=0.10,
                stop_mult=1.6, atr_trail_mult=2.2, max_hold_bars=18,
                reverse=False, disable_regime_exit=False,
                control: str | None = None) -> list:
    all_trades = []
    for sym in SYMBOLS:
        sig = build_signals(sym, gc_window=gc_window, gc_lag=gc_lag,
                            p_sig=p_sig, p_insig=p_insig)
        if sig is None:
            continue
        if control == "gate_none":
            entries = gate_none_entries(sig)
        elif control == "zscore_gate":
            entries = zscore_gate_entries(sig)
        else:
            entries = gated_entries(sig)
        trades = simulate_trades(sig, entries, stop_mult=stop_mult,
                                 atr_trail_mult=atr_trail_mult, max_hold_bars=max_hold_bars,
                                 reverse=reverse, disable_regime_exit=disable_regime_exit)
        all_trades.extend(trades)
    return all_trades


def summarize(df: pd.DataFrame, col: str = "net_R") -> dict:
    if len(df) == 0:
        return {"n": 0, "pf": float("nan"), "t": float("nan"), "win_rate": float("nan"),
                "mean_R": float("nan")}
    s = df[col]
    return {"n": int(len(s)), "pf": pf_r(s), "t": t_stat(s), "win_rate": win_rate(s),
            "mean_R": float(s.mean())}


def full_report(trades: list, label: str) -> dict:
    df = trades_to_df(trades)
    if len(df) == 0:
        return {"label": label, "n_total": 0}
    is_df, oos_df, full_df = split_is_oos(df)
    out = {"label": label, "n_total": len(df)}
    for name, sub in [("IS", is_df), ("OOS", oos_df), ("FULL", full_df)]:
        out[name] = {
            "gross": summarize(sub, "gross_R"),
            "net": summarize(sub, "net_R"),
        }
    return out


if __name__ == "__main__":
    trades = run_variant(**BASE)
    df = trades_to_df(trades)
    print(f"base: n_total={len(df)}")
    rep = full_report(trades, "base")
    print(json.dumps(rep, indent=2, default=str))
    (HERE / "out_trades_base.csv").write_text(df.to_csv(index=False) if len(df) else "")
    (HERE / "out_summary.json").write_text(json.dumps(rep, indent=2, default=str))

    # 대조군: 게이트없음 · z-score 게이트 · 반전
    trades_none = run_variant(**{**BASE, "control": "gate_none"})
    df_none = trades_to_df(trades_none)
    (HERE / "out_trades_gate_none.csv").write_text(df_none.to_csv(index=False) if len(df_none) else "")
    rep_none = full_report(trades_none, "gate_none")

    trades_z = run_variant(**{**BASE, "control": "zscore_gate"})
    df_z = trades_to_df(trades_z)
    (HERE / "out_trades_zscore_gate.csv").write_text(df_z.to_csv(index=False) if len(df_z) else "")
    rep_z = full_report(trades_z, "zscore_gate")

    trades_rev = run_variant(**{**BASE, "reverse": True})
    df_rev = trades_to_df(trades_rev)
    (HERE / "out_trades_reverse.csv").write_text(df_rev.to_csv(index=False) if len(df_rev) else "")
    rep_rev = full_report(trades_rev, "reverse")

    all_controls = {"base": rep, "gate_none": rep_none, "zscore_gate": rep_z, "reverse": rep_rev}
    (HERE / "out_controls.json").write_text(json.dumps(all_controls, indent=2, default=str))
    print(json.dumps(all_controls, indent=2, default=str))
