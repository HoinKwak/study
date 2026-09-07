"""파라미터 민감도 스윕 — 핵심 파라미터 개별 변경(base 대비 1개씩), OOS net/gross PF·t 확인.
dev_breakout/dev_fade/hl_range/ou_window 4축, 각 축 2~3값 — 총 11변형."""
from __future__ import annotations

import json
import sys

import pandas as pd

sys.path.insert(0, ".")
from common import SYMBOLS, load_klines_4h, OOS_START, OOS_END
from signals import build_signals
from engine import simulate_symbol, trades_to_df
from stats_utils import summarize

VARIANTS = [
    {"name": "base", "rv_window": 42, "ou_window": 180, "dev_breakout": -1.5, "dev_fade": 2.0,
     "hl_min": 8, "hl_max": 40},
    {"name": "dev_breakout_-1.0", "dev_breakout": -1.0},
    {"name": "dev_breakout_-2.0", "dev_breakout": -2.0},
    {"name": "dev_fade_1.5", "dev_fade": 1.5},
    {"name": "dev_fade_2.5", "dev_fade": 2.5},
    {"name": "hl_5_60", "hl_min": 5, "hl_max": 60},
    {"name": "hl_10_30", "hl_min": 10, "hl_max": 30},
    {"name": "ou_window_90", "ou_window": 90},
    {"name": "ou_window_360", "ou_window": 360},
    {"name": "rv_window_21", "rv_window": 21},
    {"name": "rv_window_84", "rv_window": 84},
]


def run_variant(params: dict):
    base = VARIANTS[0].copy()
    base.update(params)
    p = {k: v for k, v in base.items() if k != "name"}
    results = {}
    for mode in ["breakout", "fade"]:
        dir_col = "raw_breakout_dir" if mode == "breakout" else "raw_fade_dir"
        all_trades = []
        for sym in SYMBOLS:
            df = load_klines_4h(sym)
            ind = build_signals(df, **p)
            trades = simulate_symbol(sym, mode, ind[["open", "high", "low", "close"]],
                                      ind["atr14"], ind["dev"], ind[dir_col])
            all_trades.extend(trades)
        tdf = trades_to_df(all_trades)
        if len(tdf):
            oos = tdf[(tdf["entry_time"] >= OOS_START) & (tdf["entry_time"] <= OOS_END)]
        else:
            oos = tdf
        net = summarize(oos["net_R"]) if len(oos) else summarize(pd.Series(dtype=float))
        gross = summarize(oos["gross_R"]) if len(oos) else summarize(pd.Series(dtype=float))
        results[mode] = {"n": len(oos), "net_PF": net["PF"], "net_t": net["t"],
                          "gross_PF": gross["PF"], "gross_t": gross["t"]}
    return results


def main():
    out = []
    for v in VARIANTS:
        name = v["name"]
        params = {k: val for k, val in v.items() if k != "name"}
        res = run_variant(params)
        row = {"variant": name}
        for mode in ["breakout", "fade"]:
            for k, val in res[mode].items():
                row[f"{mode}_{k}"] = val
        out.append(row)
        print(name, res)
    pd.DataFrame(out).to_csv("out_diag_sweep.csv", index=False)


if __name__ == "__main__":
    main()
