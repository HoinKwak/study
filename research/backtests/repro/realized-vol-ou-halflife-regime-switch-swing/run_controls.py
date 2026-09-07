"""대조군 3종 실행: gate_none / simple_alt(naive RV z) / reverse. 신호 중첩률도 계산.

argcount 로 함수 시그니처를 추측하는 방식은 취약(gate_none_fade 가 기본값 있는 2번째
인자를 가져 오탐 발생 이력) — 모드별로 명시적 분기해 dir_fn 을 항상 (df, ind) 로 통일 호출.
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
from common import SYMBOLS, load_klines_4h, OOS_START, OOS_END, IS_START, IS_END
from signals import build_signals
import control_signals as cs
from engine import simulate_symbol, trades_to_df
from stats_utils import summarize


def build_all():
    data = {}
    for sym in SYMBOLS:
        df = load_klines_4h(sym)
        ind = build_signals(df)
        data[sym] = {"df": df, "ind": ind}
    return data


def gate_none_dir(mode: str, df: pd.DataFrame, ind: pd.DataFrame) -> pd.Series:
    return cs.gate_none_breakout(ind) if mode == "breakout" else cs.gate_none_fade(ind)


def simple_alt_dir(mode: str, df: pd.DataFrame, ind: pd.DataFrame) -> pd.Series:
    return (cs.simple_alt_breakout(df, ind) if mode == "breakout"
            else cs.simple_alt_fade(df, ind))


def run_variant(data, mode: str, dir_fn_name: str, *, reverse=False) -> pd.DataFrame:
    trades_all = []
    for sym, d in data.items():
        ind = d["ind"]
        if dir_fn_name == "gate_none":
            directions = gate_none_dir(mode, d["df"], ind)
        elif dir_fn_name == "simple_alt":
            directions = simple_alt_dir(mode, d["df"], ind)
        else:
            raise ValueError(dir_fn_name)
        trades = simulate_symbol(sym, mode, ind[["open", "high", "low", "close"]], ind["atr14"],
                                  ind["dev"], directions, reverse=reverse)
        trades_all.extend(trades)
    return trades_to_df(trades_all)


def signal_overlap(base_dirs: dict[str, pd.Series], other_dirs: dict[str, pd.Series]):
    base_set = set()
    other_set = set()
    for sym in base_dirs:
        b = base_dirs[sym]
        o = other_dirs[sym]
        base_set |= {(sym, t) for t in b[b != 0].index}
        other_set |= {(sym, t) for t in o[o != 0].index}
    inter = base_set & other_set
    frac = len(inter) / len(base_set) if base_set else float("nan")
    return frac, len(base_set), len(other_set)


def split_summ(trades: pd.DataFrame) -> dict:
    r = {}
    for k, (s, e) in {"IS": (IS_START, IS_END), "OOS": (OOS_START, OOS_END)}.items():
        if len(trades) == 0:
            r[k] = summarize(pd.Series(dtype=float))
            r[k]["gross_PF"] = float("nan")
            continue
        m = (trades["entry_time"] >= s) & (trades["entry_time"] <= e)
        r[k] = summarize(trades.loc[m, "net_R"])
        r[k]["gross_PF"] = summarize(trades.loc[m, "gross_R"])["PF"]
    return r


def main():
    data = build_all()
    out = {}

    for mode in ["breakout", "fade"]:
        dir_col = "raw_breakout_dir" if mode == "breakout" else "raw_fade_dir"
        base_dirs = {sym: data[sym]["ind"][dir_col] for sym in SYMBOLS}

        none_trades = run_variant(data, mode, "gate_none")
        alt_trades = run_variant(data, mode, "simple_alt")

        none_dirs = {sym: gate_none_dir(mode, data[sym]["df"], data[sym]["ind"]) for sym in SYMBOLS}
        alt_dirs = {sym: simple_alt_dir(mode, data[sym]["df"], data[sym]["ind"]) for sym in SYMBOLS}

        # reverse: base 신호(진입시각) 그대로, engine reverse=True 로 부호만 뒤집음(대칭 재배치)
        rev_trades_list = []
        for sym in SYMBOLS:
            ind = data[sym]["ind"]
            trs = simulate_symbol(sym, mode, ind[["open", "high", "low", "close"]], ind["atr14"],
                                   ind["dev"], base_dirs[sym], reverse=True)
            rev_trades_list.extend(trs)
        rev_trades = trades_to_df(rev_trades_list)

        none_trades.to_csv(f"out_trades_{mode}_gate_none.csv", index=False)
        alt_trades.to_csv(f"out_trades_{mode}_simple_alt.csv", index=False)
        rev_trades.to_csv(f"out_trades_{mode}_reverse.csv", index=False)

        ov_none, n_base, n_none = signal_overlap(base_dirs, none_dirs)
        ov_alt, _, n_alt = signal_overlap(base_dirs, alt_dirs)
        ov_rev = 1.0  # reverse 는 base 신호(진입시각)를 그대로 재사용 — 정의상 100%

        out[mode] = {
            "gate_none": split_summ(none_trades),
            "simple_alt": split_summ(alt_trades),
            "reverse": split_summ(rev_trades),
            "overlap_base_vs_gate_none": ov_none,
            "overlap_base_vs_simple_alt": ov_alt,
            "overlap_base_vs_reverse": ov_rev,
            "n_base_signals": n_base, "n_gate_none_signals": n_none, "n_simple_alt_signals": n_alt,
        }
        print(mode, json.dumps(out[mode], indent=2, default=str))

    with open("out_controls_summary.json", "w") as f:
        json.dump(out, f, indent=2, default=str)


if __name__ == "__main__":
    main()
