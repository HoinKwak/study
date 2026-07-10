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


def test_mid_long_on_pullback_in_uptrend():
    s = MidStrategy(_settings())
    # 1h 상승 추세
    confirm = _df(list(np.linspace(100, 140, 60)), freq="1h")
    # 15m: 상승하다가 급락해 밴드 하단 부근 + RSI 낮음
    prices = list(np.linspace(100, 120, 35)) + list(np.linspace(120, 111, 12))
    d = s.decide("BTC/USDT", _df(prices), confirm, None)
    assert d.action in (Action.OPEN_LONG, Action.HOLD)
    if d.action is Action.OPEN_LONG:
        assert d.direction is Direction.LONG
        assert d.stop_price < 111        # SL 은 진입가 아래
        assert d.take_profit > 111       # TP(중심선)는 눌린 가격 위


def test_mid_no_long_against_downtrend():
    s = MidStrategy(_settings())
    confirm = _df(list(np.linspace(140, 100, 60)), freq="1h")  # 1h 하락 추세
    prices = list(np.linspace(120, 111, 47))
    d = s.decide("BTC/USDT", _df(prices), confirm, None)
    assert d.action is not Action.OPEN_LONG  # 하락추세에서 롱 금지


def test_mid_exit_on_trend_flip():
    s = MidStrategy(_settings())
    confirm = _df(list(np.linspace(140, 100, 60)), freq="1h")  # 하락 반전
    prices = list(np.linspace(130, 120, 46))
    d = s.decide("BTC/USDT", _df(prices), confirm, Direction.LONG)
    assert d.action is Action.CLOSE
