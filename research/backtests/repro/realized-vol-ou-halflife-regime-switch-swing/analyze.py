"""메인 백테스트 실행 — base 파라미터, 7종목, 브레이크아웃/페이드 모드 각각 독립.

산출: out_trades_breakout_base.csv, out_trades_fade_base.csv, out_summary.json
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
from common import SYMBOLS, IS_START, IS_END, OOS_START, OOS_END, load_klines_4h
from signals import build_signals
from engine import simulate_symbol, trades_to_df
from stats_utils import summarize, declustered_t, rolling_window_declustered_t


def load_all(rv_window=42, ou_window=180, dev_breakout=-1.5, dev_fade=2.0, hl_min=8, hl_max=40,
             body_mult=1.5):
    data = {}
    for sym in SYMBOLS:
        df = load_klines_4h(sym)
        ind = build_signals(df, rv_window=rv_window, ou_window=ou_window,
                             dev_breakout=dev_breakout, dev_fade=dev_fade,
                             hl_min=hl_min, hl_max=hl_max, body_mult=body_mult)
        data[sym] = ind
    return data


def run_mode(data: dict, mode: str, *, atr_sl=1.8, atr_trail_breakout=2.5, atr_tp_fade=1.5,
             max_hold_bars=20, reverse=False) -> pd.DataFrame:
    all_trades = []
    dir_col = "raw_breakout_dir" if mode == "breakout" else "raw_fade_dir"
    for sym, ind in data.items():
        directions = ind[dir_col]
        # fade 모드의 dev-0-재돌파 청산은 "전봉 확정치"를 써야 하므로 dev 자체를 넘기고
        # engine 내부에서 pos-1 인덱싱(이미 그렇게 구현됨. 여기서는 원 dev 시리즈 그대로 전달).
        trades = simulate_symbol(sym, mode, ind[["open", "high", "low", "close"]], ind["atr14"],
                                  ind["dev"], directions, atr_sl=atr_sl,
                                  atr_trail_breakout=atr_trail_breakout,
                                  atr_tp_fade=atr_tp_fade, max_hold_bars=max_hold_bars,
                                  reverse=reverse)
        all_trades.extend(trades)
    return trades_to_df(all_trades)


def split_is_oos(trades: pd.DataFrame) -> dict[str, pd.DataFrame]:
    if len(trades) == 0:
        return {"IS": trades, "OOS": trades, "FULL": trades}
    is_mask = (trades["entry_time"] >= IS_START) & (trades["entry_time"] <= IS_END)
    oos_mask = (trades["entry_time"] >= OOS_START) & (trades["entry_time"] <= OOS_END)
    return {"IS": trades[is_mask], "OOS": trades[oos_mask], "FULL": trades[is_mask | oos_mask]}


def report_mode(trades: pd.DataFrame, label: str) -> dict:
    out = {}
    splits = split_is_oos(trades)
    for k, df_ in splits.items():
        net = summarize(df_["net_R"]) if len(df_) else summarize(pd.Series(dtype=float))
        gross = summarize(df_["gross_R"]) if len(df_) else summarize(pd.Series(dtype=float))
        dc_net = declustered_t(df_, "net_R") if len(df_) else {"n": 0, "t": np.nan, "PF": np.nan}
        dc_gross = declustered_t(df_, "gross_R") if len(df_) else {"n": 0, "t": np.nan, "PF": np.nan}
        rw5_net = rolling_window_declustered_t(df_, "net_R", window_days=5) if len(df_) else {}
        rw5_gross = rolling_window_declustered_t(df_, "gross_R", window_days=5) if len(df_) else {}
        rw3_net = rolling_window_declustered_t(df_, "net_R", window_days=3) if len(df_) else {}
        out[k] = {"n": len(df_), "net": net, "gross": gross,
                  "declustered_1d_net": dc_net, "declustered_1d_gross": dc_gross,
                  "declustered_5d_net": rw5_net, "declustered_5d_gross": rw5_gross,
                  "declustered_3d_net": rw3_net}
    print(f"=== {label} ===")
    for k, v in out.items():
        print(k, v["n"], "net PF", round(v["net"]["PF"], 3) if v["n"] else None,
              "t", round(v["net"]["t"], 3) if v["n"] else None,
              "gross PF", round(v["gross"]["PF"], 3) if v["n"] else None)
    return out


def main():
    data = load_all()
    summary = {}
    for mode in ["breakout", "fade"]:
        trades = run_mode(data, mode)
        trades.to_csv(f"out_trades_{mode}_base.csv", index=False)
        summary[mode] = report_mode(trades, mode)
        # symbol-level breakdown (OOS)
        splits = split_is_oos(trades)
        oos = splits["OOS"]
        by_sym = {}
        for sym, g in oos.groupby("symbol"):
            by_sym[sym] = summarize(g["net_R"])
        summary[mode]["by_symbol_OOS"] = by_sym
        print(mode, "OOS by symbol:", {k: (v["n"], round(v["PF"], 3) if v["n"] else None)
                                         for k, v in by_sym.items()})
    with open("out_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)


if __name__ == "__main__":
    main()
