"""무비용(fee=0·slippage=0) 진단 — gross 엣지가 애초에 존재하는지 확인."""
from __future__ import annotations

import common
import engine
import stats_utils as su


def main():
    regime7 = common.build_regime_1h(symbols=common.SYMBOLS)
    regime35 = common.build_regime_1h(symbols=common.EXT_SYMBOLS)
    btc = common.build_btc_signals()
    aligned7 = common.align_regime_to_15m(btc.df15, regime7)
    aligned35 = common.align_regime_to_15m(btc.df15, regime35)

    for uni_label, aligned in [("n7", aligned7), ("n35", aligned35)]:
        for mode in ["gated", "ungated", "reverse", "gate_top"]:
            cfg = engine.RunConfig(mode=mode, fee_on=False)
            trades = engine.run_all(btc, aligned, cfg)
            df = su.trades_df(trades)
            is_df, oos_df, full_df = su.split_is_oos(df)
            for label, d in [("IS", is_df), ("OOS", oos_df)]:
                s = su.summary(d, f"GROSS_{uni_label}_{mode}_{label}")
                print(su.print_summary(s))


if __name__ == "__main__":
    main()
