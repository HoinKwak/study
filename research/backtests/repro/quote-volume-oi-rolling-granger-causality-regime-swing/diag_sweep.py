"""파라미터 스윕: lag(2/4/8) × p_sig(0.01/0.05/0.10) 3×3 — 사전 등록 폐기조건 (d) 검정.
+ 완화된(loose) 전환 정의(lookback 3/5/10)도 보조 진단으로 함께 실행.

⚠️ 대부분의 그리드 셀은 표본이 너무 작아(diag_freq.py 결과) PF/t 가 정의되지 않거나 무의미할
수 있음 — 그 경우도 그대로 기록한다(임의로 숨기지 않음)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from common import SYMBOLS, pf_r, t_stat, split_is_oos
from signals import build_signals
from events import gated_entries
from events_loose import loose_gated_entries
from engine import simulate_trades, trades_to_df

HERE = Path(__file__).resolve().parent


def summarize(df: pd.DataFrame, col: str) -> dict:
    if len(df) == 0:
        return {"n": 0, "pf": float("nan"), "t": float("nan")}
    s = df[col]
    return {"n": int(len(s)), "pf": pf_r(s), "t": t_stat(s)}


def run_grid(entry_fn, label: str, **entry_kwargs) -> dict:
    all_trades = []
    for sym in SYMBOLS:
        sig = build_signals(sym, gc_lag=entry_kwargs.get("gc_lag", 4),
                            p_sig=entry_kwargs.get("p_sig", 0.05))
        if "lookback" in entry_kwargs:
            entries = entry_fn(sig, lookback=entry_kwargs["lookback"])
        else:
            entries = entry_fn(sig)
        trades = simulate_trades(sig, entries)
        all_trades.extend(trades)
    df = trades_to_df(all_trades)
    is_df, oos_df, full_df = split_is_oos(df) if len(df) else (df, df, df)
    out = {"label": label, "n_total": int(len(df))}
    for name, sub in [("IS", is_df), ("OOS", oos_df), ("FULL", full_df)]:
        out[name] = {"gross": summarize(sub, "gross_R"), "net": summarize(sub, "net_R")}
    return out


def main():
    results = {"strict_grid": [], "loose_grid": []}
    for lag in (2, 4, 8):
        for psig in (0.01, 0.05, 0.10):
            r = run_grid(gated_entries, f"lag{lag}_psig{psig}", gc_lag=lag, p_sig=psig)
            print(r["label"], r["n_total"], r.get("OOS"))
            results["strict_grid"].append(r)
    for lb in (3, 5, 10):
        r = run_grid(loose_gated_entries, f"loose_lb{lb}", gc_lag=4, p_sig=0.05, lookback=lb)
        print(r["label"], r["n_total"], r.get("OOS"))
        results["loose_grid"].append(r)
    (HERE / "out_diag_sweep.json").write_text(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
