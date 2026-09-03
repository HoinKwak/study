"""룩어헤드 점검 — 3종목을 임의 시점에서 절단해 재실행, 절단 이전 이벤트/신호가 bit 단위 일치하는지."""
from __future__ import annotations

import json

import pandas as pd

from common import load_funding, load_klines_4h
from events import detect_events, filter_8h
from engine import ema_4h, atr14_4h, find_signals


def run_full_and_cut(symbol: str, cut_frac: float):
    funding = load_funding(symbol)
    price_4h = load_klines_4h(symbol)

    def build(funding_df, price_df):
        f8, _ = filter_8h(funding_df)
        events, diag = detect_events(f8)
        ema = ema_4h(price_df)
        atr = atr14_4h(price_df)
        return {"symbol": symbol, "price_4h": price_df, "ema": ema, "atr": atr,
                "events": events}

    full_frame = build(funding, price_4h)
    full_sig = find_signals(full_frame)

    cut_idx_f = int(len(funding) * cut_frac)
    cut_time = funding.index[cut_idx_f]
    funding_cut = funding[funding.index <= cut_time]
    price_cut = price_4h[price_4h.index <= cut_time]
    cut_frame = build(funding_cut, price_cut)
    cut_sig = find_signals(cut_frame)

    # 절단 시점 이전(4h봉 확정 시차 감안 -8h 마진) 신호만 비교
    margin = cut_time - pd.Timedelta(hours=8)
    full_before = full_sig[full_sig["event_time"] <= margin].reset_index(drop=True)
    cut_before = cut_sig[cut_sig["event_time"] <= margin].reset_index(drop=True)
    match = full_before.equals(cut_before)
    return {"cut_time": str(cut_time), "n_full_before": len(full_before),
            "n_cut_before": len(cut_before), "bitwise_match": bool(match)}


def main() -> None:
    out = {}
    for sym in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]:
        out[sym] = run_full_and_cut(sym, 0.6)
    with open("out_diag_lookahead.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
