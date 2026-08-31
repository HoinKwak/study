"""룩어헤드 절단 테스트: 데이터를 임의 시점에서 절단해 신호를 재계산했을 때, 절단 이전
구간의 신호가 전체 데이터로 계산한 것과 완전히 일치하는지 확인(여러 종목)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import load_symbol, wick_asym
from engine import build_frame, find_signals

CUTOFF_FRACS = [0.3, 0.55, 0.8]


def truncated_frame(symbol: str, cutoff_ts: pd.Timestamp, wick_th=0.4, lookback_bars=6,
                     min_count=4, ext_th=0.05) -> dict:
    """build_frame 과 동일 로직이나 klines/premium 원본을 cutoff_ts 이전으로 잘라서 계산."""
    from crypto_trader.signals import indicators as _ind  # noqa

    data = load_symbol(symbol)
    prem = data["prem_4h"].copy()
    price = data["price_4h"]
    price1d = data["price_1d"]

    prem = prem[prem.index <= cutoff_ts]
    price = price[price.index <= cutoff_ts]
    price1d = price1d[price1d.index <= cutoff_ts]

    idx = prem.index.intersection(price.index)
    prem = prem.loc[idx]
    price_aligned = price.loc[idx]

    wa = wick_asym(prem)
    prem["wick_asym"] = wa
    is_upper = (wa >= wick_th).astype(float)
    is_lower = (wa <= -wick_th).astype(float)
    prem["consec_upper"] = is_upper.rolling(lookback_bars, min_periods=lookback_bars).sum()
    prem["consec_lower"] = is_lower.rolling(lookback_bars, min_periods=lookback_bars).sum()
    prem["premium_close"] = prem["close"]

    ema_1d = _ind.ema(price1d["close"], period=20)
    daily_closed_at = price1d.index + pd.DateOffset(days=1)
    order = np.argsort(daily_closed_at.values)
    closed_sorted = daily_closed_at.values[order]
    ema_sorted = ema_1d.values[order]
    pos = np.searchsorted(closed_sorted, price_aligned.index.values, side="right") - 1
    ema_aligned = np.where(pos >= 0, ema_sorted[np.clip(pos, 0, None)], np.nan)
    prem["ema20_1d"] = ema_aligned
    prem["price_close"] = price_aligned["close"]
    prem["ext_pct"] = (price_aligned["close"] - ema_aligned) / ema_aligned

    atr = _ind.atr(price, period=14)
    return {"prem": prem, "price": price, "atr": atr, "min_count": min_count,
            "wick_th": wick_th, "lookback_bars": lookback_bars, "ext_th": ext_th,
            "_symbol": symbol}


def main() -> None:
    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "XRPUSDT"]
    all_ok = True
    for sym in symbols:
        full = build_frame(sym)
        full["_symbol"] = sym
        full_signals = find_signals(full)
        n_full_bars = len(full["prem"])
        for frac in CUTOFF_FRACS:
            cutoff_pos = int(n_full_bars * frac)
            cutoff_ts = full["prem"].index[cutoff_pos]
            # 안전 여유(마지막 lookback/ema 워밍업 부근 신호 제외하고 비교): cutoff 이전
            # margin_bars 만큼 앞선 지점까지만 비교(경계 부근 rolling window 워밍업 차이 방지)
            margin = pd.Timedelta(hours=4 * 20)
            compare_before = cutoff_ts - margin

            trunc = truncated_frame(sym, cutoff_ts)
            trunc_signals = find_signals(trunc)

            full_before = [s for s in full_signals if s[0] <= compare_before]
            trunc_before = [s for s in trunc_signals if s[0] <= compare_before]

            full_set = set((t, d, c) for t, d, c, pc, ep in full_before)
            trunc_set = set((t, d, c) for t, d, c, pc, ep in trunc_before)
            match = full_set == trunc_set
            all_ok = all_ok and match
            print(f"{sym} cutoff_frac={frac} cutoff_ts={cutoff_ts} "
                  f"full_before_n={len(full_before)} trunc_before_n={len(trunc_before)} "
                  f"일치={match}" + ("" if match else f" 차이={full_set ^ trunc_set}"))
    print(f"\n전체 룩어헤드 절단 테스트 통과: {all_ok}")


if __name__ == "__main__":
    main()
