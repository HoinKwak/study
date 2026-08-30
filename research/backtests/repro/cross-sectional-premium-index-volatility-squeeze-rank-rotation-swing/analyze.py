"""전체 분석 파이프라인: base 변형 + 스윕 + 대조군 + de-clustering + 룩어헤드 감사."""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

from common import SYMBOLS, IS_START, IS_END, OOS_START, OOS_END
from engine import (load_all, run_variant, trades_to_df, split_is_oos, pf_r, t_stat)

DEFAULT = dict(squeeze_entry_pctile=0.20, squeeze_exit_pctile=0.70, trigger_window=10,
                top_k=2, donchian_len=15, atr_sl_mult=1.5, atr_trail_mult=3.0,
                max_hold_days=15)


def summarize(df: pd.DataFrame, label: str) -> dict:
    is_df, oos_df, full_df = split_is_oos(df)
    out = {"label": label, "n_full": len(full_df), "n_is": len(is_df), "n_oos": len(oos_df)}
    for name, sub in [("full", full_df), ("is", is_df), ("oos", oos_df)]:
        if len(sub) == 0:
            out[f"{name}_gross_pf"] = float("nan")
            out[f"{name}_net_pf"] = float("nan")
            out[f"{name}_net_t"] = float("nan")
            out[f"{name}_gross_t"] = float("nan")
            continue
        out[f"{name}_gross_pf"] = pf_r(sub["gross_R"])
        out[f"{name}_net_pf"] = pf_r(sub["net_R"])
        out[f"{name}_net_t"] = t_stat(sub["net_R"])
        out[f"{name}_gross_t"] = t_stat(sub["gross_R"])
    return out


def main() -> None:
    print("데이터 로딩(squeeze_window=60, donchian_len=15)...")
    universe = load_all(squeeze_window=60, donchian_len=15)
    for sym, d in universe.items():
        daily = d["daily"]
        print(f"  {sym}: daily rows={len(daily)} range=[{daily.index.min()}, {daily.index.max()}]"
              f" nan_pctile={daily['squeeze_pctile'].isna().sum()}")

    print("\n=== ①기본 변형(top_k=2) ===")
    base_trades = run_variant(universe, **DEFAULT)
    base_df = trades_to_df(base_trades)
    print(f"총 트레이드 n={len(base_df)}")
    base_df.to_csv("out_base_trades.csv", index=False)
    summ = summarize(base_df, "base")
    print(json.dumps(summ, indent=2, default=str))

    with open("out_summary.json", "w") as f:
        json.dump({"base": summ}, f, indent=2, default=str)

    print("\n완료 — out_base_trades.csv, out_summary.json 저장")


if __name__ == "__main__":
    main()
