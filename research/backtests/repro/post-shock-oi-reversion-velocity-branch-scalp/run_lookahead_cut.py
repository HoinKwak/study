"""룩어헤드 점검: 임의 시점에서 1h/15m 데이터를 절단(그 이후 데이터 완전 제거)해 재실행한
신호가 절단 이전 구간에서 원본과 bit 단위로 일치하는지 확인(최소 3종목)."""
from __future__ import annotations

import pandas as pd

import common as c
import engine


def run_symbol_events(sym: str, sd: c.SymbolData, cfg: engine.Config):
    return engine.detect_events(sym, sd, cfg)


def truncate(sd: c.SymbolData, cut_h1: pd.Timestamp) -> c.SymbolData:
    h1 = sd.h1[sd.h1.index <= cut_h1]
    m15 = sd.m15[sd.m15.index <= cut_h1]
    atr1h = sd.atr1h[sd.atr1h.index <= cut_h1]
    atr15m = sd.atr15m[sd.atr15m.index <= cut_h1]
    ema20 = sd.ema20_15m[sd.ema20_15m.index <= cut_h1]
    oi1h = sd.oi1h[sd.oi1h.index <= cut_h1]
    return c.SymbolData(h1=h1, m15=m15, atr1h=atr1h, atr15m=atr15m, ema20_15m=ema20, oi1h=oi1h)


def main():
    data = c.load_all()
    cfg = engine.Config()
    test_syms = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]
    cuts = {
        "BTCUSDT": pd.Timestamp("2023-11-15 12:00:00", tz="UTC"),
        "ETHUSDT": pd.Timestamp("2024-08-03 07:00:00", tz="UTC"),
        "XRPUSDT": pd.Timestamp("2025-02-21 19:00:00", tz="UTC"),
    }
    for sym in test_syms:
        sd_full = data[sym]
        cut = cuts[sym]
        events_full = run_symbol_events(sym, sd_full, cfg)
        events_before_cut = [e for e in events_full if e.confirm_time <= cut]

        sd_trunc = truncate(sd_full, cut)
        events_trunc = run_symbol_events(sym, sd_trunc, cfg)

        def key(e):
            return (e.shock_time, e.branch, e.orig_direction, round(e.revert_ratio, 8))

        set_full = sorted(key(e) for e in events_before_cut)
        set_trunc = sorted(key(e) for e in events_trunc)
        match = set_full == set_trunc
        print(f"{sym} cut={cut}: 절단전 원본이벤트={len(set_full)} 절단재실행이벤트={len(set_trunc)} "
             f"bit단위일치={match}")
        if not match:
            only_full = set(set_full) - set(set_trunc)
            only_trunc = set(set_trunc) - set(set_full)
            print("  원본에만 있음(최대 5):", list(only_full)[:5])
            print("  절단본에만 있음(최대 5):", list(only_trunc)[:5])


if __name__ == "__main__":
    main()
