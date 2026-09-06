"""§파라미터 스윕 — h·k·z_window(스펙 명시범위) 각 조합에서 OOS net PF(R)·t 계산(빈도만이
아니라 실제 손익 강건성 확인). 청산 파라미터(atr_trail/atr_stop/max_hold)도 별도 스윕."""
from __future__ import annotations

import itertools
import json

import pandas as pd

from common import pf_r, t_stat, OOS_START, OOS_END, IS_START, IS_END
from signals import build_signals
from events import raw_cp_events, gated_entries
from engine import simulate_trades, trades_to_df, DEFAULT_DIRECTION_MAP

Z_WINDOWS = [60, 90, 120]
KS = [0.3, 0.5, 0.7, 1.0]
HS = [3.0, 5.0, 8.0]


def oos_stats(df: pd.DataFrame) -> dict:
    oos = df[(df["entry_time"] >= OOS_START) & (df["entry_time"] <= OOS_END)] if len(df) else df
    is_ = df[(df["entry_time"] >= IS_START) & (df["entry_time"] <= IS_END)] if len(df) else df
    return {"n_oos": len(oos), "oos_net_pf": pf_r(oos["net_R"]) if len(oos) else float("nan"),
            "oos_net_t": t_stat(oos["net_R"]) if len(oos) else float("nan"),
            "n_is": len(is_), "is_net_pf": pf_r(is_["net_R"]) if len(is_) else float("nan")}


def main():
    rows = []
    for zw, k, h in itertools.product(Z_WINDOWS, KS, HS):
        sig = build_signals("BTCUSDT", z_window_days=zw, k=k, h=h)
        raw_cp = raw_cp_events(sig)
        entries = gated_entries(sig, confirm_bars=2)
        trades = simulate_trades(sig, entries, DEFAULT_DIRECTION_MAP, stop_mult=1.5,
                                 atr_trail_mult=2.5, max_hold_bars=30, raw_cp=raw_cp)
        df = trades_to_df(trades)
        st = oos_stats(df)
        st.update({"z_window": zw, "k": k, "h": h})
        rows.append(st)
    sweep = pd.DataFrame(rows)
    sweep.to_csv("out_diag_sweep_hk.csv", index=False)
    print(sweep.to_string(index=False))
    n_pass = ((sweep["n_oos"] >= 15) & (sweep["oos_net_pf"] >= 1.3) & (sweep["oos_net_t"] >= 1.96)).sum()
    print(f"\n통과선(n>=15,PF>=1.3,t>=1.96) 충족 조합: {n_pass}/{len(sweep)}")
    print("OOS net PF>=1.0 인 조합 수:", (sweep["oos_net_pf"] >= 1.0).sum(), "/", len(sweep))

    # 청산 파라미터 스윕(base h/k/z 고정)
    sig = build_signals("BTCUSDT")
    raw_cp = raw_cp_events(sig)
    entries = gated_entries(sig, confirm_bars=2)
    rows2 = []
    for stop_mult, trail_mult, max_hold in itertools.product([1.1, 1.5, 2.0], [1.8, 2.5, 3.2],
                                                              [20, 30, 45]):
        trades = simulate_trades(sig, entries, DEFAULT_DIRECTION_MAP, stop_mult=stop_mult,
                                 atr_trail_mult=trail_mult, max_hold_bars=max_hold, raw_cp=raw_cp)
        df = trades_to_df(trades)
        st = oos_stats(df)
        st.update({"stop_mult": stop_mult, "trail_mult": trail_mult, "max_hold": max_hold})
        rows2.append(st)
    sweep2 = pd.DataFrame(rows2)
    sweep2.to_csv("out_diag_sweep_exit.csv", index=False)
    print("\n=== 청산 파라미터 스윕 ===")
    print(sweep2.to_string(index=False))
    n_pass2 = ((sweep2["n_oos"] >= 15) & (sweep2["oos_net_pf"] >= 1.3) & (sweep2["oos_net_t"] >= 1.96)).sum()
    print(f"\n통과선 충족 조합: {n_pass2}/{len(sweep2)}")


if __name__ == "__main__":
    main()
