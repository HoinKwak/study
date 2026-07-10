import numpy as np
import pandas as pd

from crypto_trader.signals import (
    DerivativesSignals,
    SignalAggregator,
    TechnicalSignals,
)
from crypto_trader.signals.base import Direction


def _trend_df(direction="up", n=120):
    if direction == "up":
        close = np.linspace(100, 160, n)
    else:
        close = np.linspace(160, 100, n)
    close = close + np.random.default_rng(1).normal(0, 0.2, n)
    high = close * 1.002
    low = close * 0.998
    open_ = np.concatenate([[close[0]], close[:-1]])
    vol = np.full(n, 500.0)
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": vol})


def test_technical_score_in_range():
    sig = TechnicalSignals().compute(_trend_df("up"))
    assert -1.0 <= sig.score <= 1.0
    assert sig.name == "technical"


def test_technical_insufficient_data():
    df = _trend_df("up", n=10)
    sig = TechnicalSignals().compute(df)
    assert sig.score == 0.0
    assert sig.detail.get("reason") == "insufficient_data"


def test_derivatives_bullish_taker_and_top_trader():
    # 상위 트레이더 롱 우세 + 테이커 매수 우세 → 롱(+) 경향
    snap = {
        "funding_rate": 0.0,
        "oi_change_pct": 1.0,
        "global_ls_ratio": 1.0,
        "top_trader_ls_ratio": 2.0,
        "taker_buy_sell_ratio": 1.5,
    }
    sig = DerivativesSignals().compute(snap)
    assert sig.score > 0
    assert -1.0 <= sig.score <= 1.0


def test_derivatives_funding_contrarian():
    # 펀딩 매우 높음(롱 과열) → 숏(-) 경향
    snap = {"funding_rate": 0.002, "oi_change_pct": None,
            "global_ls_ratio": None, "top_trader_ls_ratio": None,
            "taker_buy_sell_ratio": None}
    sig = DerivativesSignals().compute(snap)
    assert sig.score < 0


def test_derivatives_empty_snapshot_neutral():
    snap = {k: None for k in
            ["funding_rate", "oi_change_pct", "global_ls_ratio",
             "top_trader_ls_ratio", "taker_buy_sell_ratio"]}
    sig = DerivativesSignals().compute(snap)
    assert sig.score == 0.0


def test_aggregator_direction_threshold():
    agg = SignalAggregator(entry_threshold=0.5)
    from crypto_trader.signals.base import SignalResult
    strong_long = [SignalResult("technical", 0.9), SignalResult("derivatives", 0.9)]
    out = agg.aggregate("BTC/USDT", strong_long)
    assert out.direction is Direction.LONG

    weak = [SignalResult("technical", 0.1), SignalResult("derivatives", 0.0)]
    out2 = agg.aggregate("BTC/USDT", weak)
    assert out2.direction is Direction.FLAT
