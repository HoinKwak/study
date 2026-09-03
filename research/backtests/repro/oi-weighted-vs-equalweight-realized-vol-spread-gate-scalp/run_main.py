"""메인 백테스트: 게이트 변형(gated/ungated/btc_solo/ew_solo/reverse/random_gate) × IS/OOS/FULL.
결과를 pickle 로 저장(추가 진단에서 재사용)."""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

import common as C
import engine
import gates
import stats_utils as su

OUT = Path(__file__).parent / "results_main.pkl"


def main():
    udata = C.build_universe_data()
    gate_oiw, spread_df = gates.build_gate_oiweighted(udata=udata)
    gate_btc = gates.build_gate_btc_solo()
    gate_ew = gates.build_gate_ew_solo(udata=udata)

    btc = C.build_btc_signals()
    aligned_oiw = C.align_1h_to_15m(btc.df15, gate_oiw.to_frame("gate"))["gate"]
    aligned_btc = C.align_1h_to_15m(btc.df15, gate_btc.to_frame("gate"))["gate"]
    aligned_ew = C.align_1h_to_15m(btc.df15, gate_ew.to_frame("gate"))["gate"]

    duty_oiw = gates.gate_duty_cycle(gate_oiw)
    print("OI가중 스프레드 게이트 duty cycle:", duty_oiw)

    rng = np.random.default_rng(2026)

    all_results = {}
    specs = [
        ("gated", aligned_oiw, False, None),
        ("ungated", None, False, None),
        ("btc_solo", aligned_btc, False, None),
        ("ew_solo", aligned_ew, False, None),
        ("reverse", aligned_oiw, True, None),
        ("random_gate", None, False, duty_oiw),
    ]
    for name, aligned, reverse, probs in specs:
        print("running", name)
        mode = "ungated" if name == "ungated" else ("random_gate" if name == "random_gate" else "gated")
        trades = engine.run_variant(btc.df15, btc.don_hi, btc.don_lo, btc.atr14, aligned, mode,
                                    reverse=reverse, rng=rng, random_probs=probs)
        df = engine.trades_to_df(trades)
        is_df, oos_df, full_df = su.split_is_oos(df)
        all_results[name] = dict(df=df, is_df=is_df, oos_df=oos_df, full_df=full_df)
        for label, d in [("IS", is_df), ("OOS", oos_df), ("FULL", full_df)]:
            s = su.summary(d, f"{name}_{label}", col="net_R")
            sg = su.summary(d, f"{name}_{label}_gross", col="gross_R")
            print(" ", su.print_summary(s))
            print(" ", su.print_summary(sg))

    with open(OUT, "wb") as f:
        pickle.dump(dict(results=all_results, duty_oiw=duty_oiw), f)
    print("saved", OUT)


if __name__ == "__main__":
    main()
