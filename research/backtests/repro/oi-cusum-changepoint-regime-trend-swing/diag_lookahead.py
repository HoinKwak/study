"""§룩어헤드 절단 검증 — BTC 외 3종목(ETH·XRP·ADA) 포함 총 4종목. 데이터를 임의 시점에서
절단하고 재계산한 신호가 절단점 이전(여유마진 제외) 원본 신호와 완전 일치하는지 확인.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import load_klines_4h, load_metrics_5m, oi_4h_from_5m, ema_4h, atr14_4h
from cusum import build_oi_cusum
from events import raw_cp_events, gated_entries
from signals import Signals

CUT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT"]
MARGIN_BARS = 540 + 50  # z_window(90일=540봉) + 확인여유


def build_signals_truncated(symbol: str, cutoff_bar: int | None = None) -> Signals:
    df = load_klines_4h(symbol)
    if cutoff_bar is not None:
        df = df.iloc[:cutoff_bar]
    m5 = load_metrics_5m(symbol)
    if cutoff_bar is not None:
        cutoff_time = df.index[-1] + pd.Timedelta(hours=4)
        m5 = m5[m5.index < cutoff_time]
    oi4h = oi_4h_from_5m(m5)
    df = df.join(oi4h, how="left")
    cusum = build_oi_cusum(df["oi"])
    ema = ema_4h(df)
    atr14 = atr14_4h(df)
    return Signals(symbol=symbol, df=df[["open", "high", "low", "close", "volume"]],
                   oi=df["oi"], oi_5m_count=df["oi_5m_count"], oi_growth=cusum["oi_growth"],
                   z=cusum["z"], s_pos=cusum["s_pos"], s_neg=cusum["s_neg"],
                   s_pos_pre=cusum["s_pos_pre"], s_neg_pre=cusum["s_neg_pre"],
                   cp_up=cusum["cp_up"], cp_down=cusum["cp_down"],
                   ema_fast=ema["ema_fast"], ema_slow=ema["ema_slow"], atr14=atr14)


def main():
    out = {}
    for sym in CUT_SYMBOLS:
        sig_full = build_signals_truncated(sym, cutoff_bar=None)
        n_full = len(sig_full.df)
        cutoff_bar = n_full - 400  # 끝에서 400봉(약 67일) 남기고 절단
        sig_cut = build_signals_truncated(sym, cutoff_bar=cutoff_bar)

        cp_full = raw_cp_events(sig_full)
        cp_cut = raw_cp_events(sig_cut)

        safe_time = sig_cut.df.index[-1] - pd.Timedelta(hours=4 * MARGIN_BARS)
        cp_full_safe = cp_full[cp_full["cp_time"] <= safe_time]
        cp_cut_safe = cp_cut[cp_cut["cp_time"] <= safe_time]

        match = cp_full_safe.reset_index(drop=True).equals(cp_cut_safe.reset_index(drop=True))
        out[sym] = {
            "n_full_bars": n_full, "cutoff_bar": cutoff_bar, "safe_time": str(safe_time),
            "cp_full_safe_n": len(cp_full_safe), "cp_cut_safe_n": len(cp_cut_safe),
            "match": bool(match),
        }
        if not match:
            out[sym]["diff"] = "mismatch found — see manual inspection"
        print(sym, out[sym])
    with open("out_diag_lookahead.json", "w") as f:
        json.dump(out, f, indent=2, default=str)


if __name__ == "__main__":
    main()
