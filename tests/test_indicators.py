import numpy as np
import pandas as pd

from crypto_trader.signals import indicators as ind


def _synthetic_df(n=200, seed=0):
    rng = np.random.default_rng(seed)
    returns = rng.normal(0, 0.01, n)
    close = 100 * np.exp(np.cumsum(returns))
    high = close * (1 + rng.uniform(0, 0.005, n))
    low = close * (1 - rng.uniform(0, 0.005, n))
    open_ = np.concatenate([[close[0]], close[:-1]])
    vol = rng.uniform(100, 1000, n)
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": vol})


def test_rsi_bounds():
    df = _synthetic_df()
    rsi = ind.rsi(df["close"])
    assert rsi.between(0, 100).all()
    assert len(rsi) == len(df)


def test_rsi_all_up_is_high():
    close = pd.Series(np.linspace(100, 200, 100))  # 계속 상승
    rsi = ind.rsi(close)
    assert rsi.iloc[-1] > 70  # 과매수 영역


def test_macd_shapes():
    df = _synthetic_df()
    macd_line, signal_line, hist = ind.macd(df["close"])
    assert len(macd_line) == len(signal_line) == len(hist) == len(df)
    # hist == macd - signal
    assert np.allclose((macd_line - signal_line).dropna(), hist.dropna())


def test_atr_positive():
    df = _synthetic_df()
    atr = ind.atr(df)
    assert (atr.dropna() >= 0).all()


def test_adx_bounds():
    df = _synthetic_df()
    adx, plus_di, minus_di = ind.adx(df)
    assert adx.between(0, 100).all()
    assert (plus_di >= 0).all() and (minus_di >= 0).all()
