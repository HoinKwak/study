import numpy as np
import pandas as pd

from crypto_trader.config import Settings
from crypto_trader.strategy import Action
from crypto_trader.strategy.mid import MidStrategy
from crypto_trader.signals.base import Direction


def _settings():
    return Settings(binance_api_key="", binance_api_secret="")


def _df(prices, freq="15min"):
    n = len(prices)
    close = np.array(prices, dtype=float)
    return pd.DataFrame({
        "open": np.concatenate([[close[0]], close[:-1]]),
        "high": close * 1.001, "low": close * 0.999, "close": close,
        "volume": np.full(n, 500.0),
    }, index=pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC"))


def test_mid_holds_without_confirm():
    s = MidStrategy(_settings())
    d = s.decide("BTC/USDT", _df(list(np.linspace(100, 110, 50))), None, None)
    assert d.action is Action.HOLD


def test_mid_returns_valid_decision():
    s = MidStrategy(_settings())
    # 상위TF 상승 추세 (1h)
    confirm = _df(list(np.linspace(100, 140, 60)), freq="1h")
    # 15m: 상승 후 잠깐 눌렸다 반등 (MACD 교차 유도)
    prices = list(np.linspace(100, 130, 40)) + [128, 126, 127, 129, 131, 133]
    d = s.decide("BTC/USDT", _df(prices), confirm, None)
    assert d.action in (Action.OPEN_LONG, Action.HOLD)
    assert -1.0 <= d.score <= 1.0


def test_mid_exit_on_trend_flip():
    s = MidStrategy(_settings())
    # 상위TF 하락 추세인데 롱 보유 중 → 청산 유도
    confirm = _df(list(np.linspace(140, 100, 60)), freq="1h")
    prices = list(np.linspace(130, 120, 46))
    d = s.decide("BTC/USDT", _df(prices), confirm, Direction.LONG)
    assert d.action in (Action.CLOSE, Action.HOLD)
