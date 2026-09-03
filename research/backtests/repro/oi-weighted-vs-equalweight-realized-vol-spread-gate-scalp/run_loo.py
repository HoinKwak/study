"""LOO: 게이트 계산(7종목 OI/RV 유니버스)에서 특정 1종목 제외 시 견고성(스펙 §종목간 신호상관
사전예상 문단 명시 요건 — BTC 단일종목 트레이드라 LOO 대신 "게이트 계산에서 1종목 제외" 민감도)."""
from __future__ import annotations

import common as C
import engine
import gates
import stats_utils as su


def main():
    btc = C.build_btc_signals()
    print("=== LOO: 게이트 계산 유니버스에서 1종목 제외 (OOS, net) ===")
    for excl in C.SYMBOLS:
        syms = [s for s in C.SYMBOLS if s != excl]
        udata = C.build_universe_data(syms)
        gate, _ = gates.build_gate_oiweighted(symbols=syms, udata=udata)
        aligned = C.align_1h_to_15m(btc.df15, gate.to_frame("gate"))["gate"]
        trades = engine.run_variant(btc.df15, btc.don_hi, btc.don_lo, btc.atr14, aligned, "gated")
        df = engine.trades_to_df(trades)
        _, oos_df, _ = su.split_is_oos(df)
        s = su.summary(oos_df, f"제외={excl}")
        print(" ", su.print_summary(s))


if __name__ == "__main__":
    main()
