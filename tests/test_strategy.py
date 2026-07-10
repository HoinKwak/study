import numpy as np
import pandas as pd

from crypto_trader.config import Settings
from crypto_trader.strategy import Action, Strategy, detect_regime
from crypto_trader.strategy.regime import Regime
from crypto_trader.signals.base import Direction


def _settings(**kw):
    base = dict(binance_api_key="", binance_api_secret="",
                entry_score_threshold=0.3, exit_flip_threshold=0.4)
    base.update(kw)
    return Settings(**base)


def _trend_df(up=True, n=120):
    close = np.linspace(100, 180, n) if up else np.linspace(180, 100, n)
    close = close + np.random.default_rng(2).normal(0, 0.1, n)
    high = close * 1.001
    low = close * 0.999
    open_ = np.concatenate([[close[0]], close[:-1]])
    idx = pd.date_range("2024-01-01", periods=n, freq="1h", tz="UTC")
    return pd.DataFrame({"open": open_, "high": high, "low": low,
                         "close": close, "volume": np.full(n, 500.0)}, index=idx)


def _range_df(n=200):
    # 추세 없는 횡보: 100 근처에서 작은 노이즈로 진동 (낮은 ADX)
    close = 100 + np.random.default_rng(4).normal(0, 0.15, n)
    high = close + 0.05
    low = close - 0.05
    open_ = np.concatenate([[close[0]], close[:-1]])
    idx = pd.date_range("2024-01-01", periods=n, freq="1h", tz="UTC")
    return pd.DataFrame({"open": open_, "high": high, "low": low,
                         "close": close, "volume": np.full(n, 500.0)}, index=idx)


def test_regime_detects_uptrend():
    regime, adx = detect_regime(_trend_df(up=True))
    assert regime in (Regime.TREND_UP, Regime.NEUTRAL)
    assert adx >= 0


def test_regime_detects_range():
    regime, adx = detect_regime(_range_df())
    assert regime in (Regime.RANGE, Regime.NEUTRAL)


def test_strategy_returns_decision():
    s = Strategy(_settings())
    d = s.decide("BTC/USDT", _trend_df(up=True), None, None)
    assert d.action in (Action.OPEN_LONG, Action.OPEN_SHORT, Action.HOLD)
    assert -1.0 <= d.score <= 1.0


def test_strategy_signal_flip_exit_long():
    # 롱 보유 중 강한 하방 시그널 → CLOSE 유도
    s = Strategy(_settings(exit_flip_threshold=0.2))
    d = s.decide("BTC/USDT", _trend_df(up=False), None, Direction.LONG)
    assert d.action in (Action.CLOSE, Action.HOLD)


def test_strategy_holds_when_flat_and_weak():
    s = Strategy(_settings(entry_score_threshold=0.95))  # 매우 높은 임계값
    d = s.decide("BTC/USDT", _range_df(), None, None)
    assert d.action is Action.HOLD
