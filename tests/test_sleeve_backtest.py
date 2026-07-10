import numpy as np
import pandas as pd

from crypto_trader.backtest import SleeveBacktester, resample_ohlcv
from crypto_trader.config import Settings


def _settings():
    return Settings(binance_api_key="", binance_api_secret="",
                    entry_score_threshold=0.3, risk_per_trade_pct=1.0,
                    daily_max_loss_pct=100.0)


def _wave_df(n=800, freq="15min", seed=7):
    t = np.arange(n)
    close = 100 + 15 * np.sin(t / 40.0) + t * 0.01
    close = close + np.random.default_rng(seed).normal(0, 0.4, n)
    high = close * 1.003
    low = close * 0.997
    open_ = np.concatenate([[close[0]], close[:-1]])
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close,
                         "volume": np.abs(np.random.default_rng(seed).normal(500, 200, n))},
                        index=pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC"))


def test_resample_ohlcv_correctness():
    df = _wave_df(96, freq="15min")  # 하루치
    out = resample_ohlcv(df, "1h")
    assert len(out) == 24
    # 첫 1h 봉 = 첫 4개 15m 봉의 집계
    first4 = df.iloc[:4]
    assert out["open"].iloc[0] == first4["open"].iloc[0]
    assert out["close"].iloc[0] == first4["close"].iloc[-1]
    assert out["high"].iloc[0] == first4["high"].max()
    assert abs(out["volume"].iloc[0] - first4["volume"].sum()) < 1e-9


def test_mid_sleeve_backtest_runs():
    bt = SleeveBacktester(_settings(), "mid", confirm_tf="1h", warmup=100)
    res = bt.run("BTC/USDT", _wave_df(800))
    assert len(res.equity_curve) == 800 - 100
    assert res.max_drawdown_pct >= 0
    # 수수료가 거래마다 기록되는지
    for t in res.trades:
        assert t.fees >= 0


def test_swing_sleeve_backtest_runs():
    bt = SleeveBacktester(_settings(), "swing", confirm_tf="1d", warmup=100)
    df = _wave_df(600, freq="4h")
    res = bt.run("BTC/USDT", df)
    assert len(res.equity_curve) == 600 - 100
    assert "백테스트" in res.report()


def test_scalp_sleeve_backtest_runs():
    bt = SleeveBacktester(_settings(), "scalp", confirm_tf="5m", warmup=60)
    df = _wave_df(600, freq="1min")
    res = bt.run("BTC/USDT", df)
    assert len(res.equity_curve) == 600 - 60


def test_fees_reduce_pnl():
    """수수료 있는 버전이 없는 버전보다 손익이 낮거나 같아야 한다."""
    df = _wave_df(800)
    no_fee = SleeveBacktester(_settings(), "mid", confirm_tf="1h", warmup=100,
                              taker_fee=0.0, slippage=0.0).run("BTC/USDT", df)
    with_fee = SleeveBacktester(_settings(), "mid", confirm_tf="1h", warmup=100,
                                taker_fee=0.001, slippage=0.001).run("BTC/USDT", df)
    if no_fee.num_trades > 0:
        assert with_fee.ending_equity <= no_fee.ending_equity + 1e-6
