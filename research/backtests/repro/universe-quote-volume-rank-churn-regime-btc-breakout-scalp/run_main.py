"""메인 백테스트: n=7(스펙 지정 프록시)/n=35(보조·진단) 유니버스 × gated/ungated/reverse/
random_gate/gate_top 모드 × IS/OOS/FULL. 결과를 pickle 로 저장(추가 진단에서 재사용)."""
from __future__ import annotations

import pickle
from pathlib import Path

import pandas as pd

import common
import engine
import stats_utils as su

OUT = Path(__file__).parent / "results_main.pkl"


def run_one(universe_symbols, universe_label: str, mode: str, gate_pctile: float = 10.0,
           pctile_window_days: int = 60) -> tuple[pd.DataFrame, list]:
    regime = common.build_regime_1h(pctile_window_days=pctile_window_days, symbols=universe_symbols)
    btc = common.build_btc_signals()
    aligned = common.align_regime_to_15m(btc.df15, regime)
    cfg = engine.RunConfig(mode=mode, gate_pctile=gate_pctile)
    trades = engine.run_all(btc, aligned, cfg)
    df = su.trades_df(trades)
    return df, trades


def main():
    all_results = {}
    for uni_label, uni_syms in [("n7", common.SYMBOLS), ("n35", common.EXT_SYMBOLS)]:
        for mode in ["gated", "ungated", "reverse", "random_gate", "gate_top"]:
            key = f"{uni_label}_{mode}"
            print("running", key)
            df, trades = run_one(uni_syms, uni_label, mode)
            is_df, oos_df, full_df = su.split_is_oos(df)
            all_results[key] = dict(df=df, is_df=is_df, oos_df=oos_df, full_df=full_df)
            for label, d in [("IS", is_df), ("OOS", oos_df), ("FULL", full_df)]:
                s = su.summary(d, f"{key}_{label}")
                print(" ", su.print_summary(s))

    with open(OUT, "wb") as f:
        pickle.dump(all_results, f)
    print("saved", OUT)


if __name__ == "__main__":
    main()
