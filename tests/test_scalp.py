import numpy as np
import pandas as pd

from crypto_trader.config import Settings
from crypto_trader.strategy.scalp import ScalpStrategy
from crypto_trader.strategy import Action
from crypto_trader.strategy.regime import Regime
from crypto_trader.signals.base import Direction


def _settings():
    return Settings(binance_api_key="", binance_api_secret="", reward_risk_ratio=1.5)


def _base_df(n=40, price=100.0, vol=100.0):
    close = np.full(n, price) + np.random.default_rng(0).normal(0, 0.05, n)
    return pd.DataFrame({
        "open": close, "high": close + 0.05, "low": close - 0.05,
        "close": close, "volume": np.full(n, vol),
    }, index=pd.date_range("2024-01-01", periods=n, freq="1min", tz="UTC"))


def test_scalp_bullish_breakout_opens_long():
    df = _base_df()
    # 마지막 봉: 강한 양봉 + 거래량 급증 + 볼린저 상단 이탈
    i = df.index[-1]
    df.loc[i, ["open", "low"]] = [100.0, 99.9]
    df.loc[i, ["close", "high"]] = [103.0, 103.1]
    df.loc[i, "volume"] = 1000.0  # 10배 급증
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0)
    d = s.decide("BTC/USDT", df, oi_delta=50.0, current_direction=None)
    assert d.action is Action.OPEN_LONG
    assert d.direction is Direction.LONG
    assert d.stop_price == 100.0                 # 신호봉 시가
    assert d.take_profit >= 103.1                # 최소 신호봉 고가 이상
    assert d.use_twap is True


def test_scalp_bearish_breakout_opens_short():
    df = _base_df()
    i = df.index[-1]
    df.loc[i, ["open", "high"]] = [100.0, 100.1]
    df.loc[i, ["close", "low"]] = [97.0, 96.9]
    df.loc[i, "volume"] = 1000.0
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0)
    d = s.decide("BTC/USDT", df, oi_delta=50.0, current_direction=None)
    assert d.action is Action.OPEN_SHORT
    assert d.stop_price == 100.0
    assert d.take_profit <= 96.9


def test_scalp_no_volume_spike_holds():
    df = _base_df()
    i = df.index[-1]
    df.loc[i, ["open", "close", "high", "low"]] = [100.0, 103.0, 103.1, 99.9]
    # 거래량 급증 없음 (평상시와 동일)
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0)
    d = s.decide("BTC/USDT", df, oi_delta=50.0, current_direction=None)
    assert d.action is Action.HOLD


def test_scalp_oi_not_rising_blocks_entry():
    df = _base_df()
    i = df.index[-1]
    df.loc[i, ["open", "low"]] = [100.0, 99.9]
    df.loc[i, ["close", "high"]] = [103.0, 103.1]
    df.loc[i, "volume"] = 1000.0
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0)
    d = s.decide("BTC/USDT", df, oi_delta=-10.0, current_direction=None)  # OI 감소
    assert d.action is Action.HOLD


def test_scalp_exits_on_range_regime():
    df = _base_df()
    s = ScalpStrategy(_settings())
    d = s.decide("BTC/USDT", df, current_direction=Direction.LONG, confirm_regime=Regime.RANGE)
    assert d.action is Action.CLOSE
