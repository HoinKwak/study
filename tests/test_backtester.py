import numpy as np
import pandas as pd

from crypto_trader.backtest import Backtester
from crypto_trader.config import Settings


def _settings():
    return Settings(
        binance_api_key="", binance_api_secret="", binance_testnet=True,
        max_leverage=3, risk_per_trade_pct=1.0, max_open_positions=3,
        daily_max_loss_pct=100.0, entry_score_threshold=0.3,
    )


def _wave_df(n=600):
    """추세+되돌림이 섞인 합성 시계열 (매매가 발생하도록)."""
    t = np.arange(n)
    close = 100 + 20 * np.sin(t / 30.0) + t * 0.02
    close = close + np.random.default_rng(3).normal(0, 0.3, n)
    high = close * 1.003
    low = close * 0.997
    open_ = np.concatenate([[close[0]], close[:-1]])
    vol = np.full(n, 500.0)
    idx = pd.date_range("2024-01-01", periods=n, freq="1h", tz="UTC")
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": vol},
        index=idx,
    )


def test_backtester_runs_and_reports():
    bt = Backtester(_settings(), starting_equity=10_000.0, warmup=50)
    df = _wave_df()
    result = bt.run("BTC/USDT", df)

    assert len(result.equity_curve) == len(df) - 50
    assert result.starting_equity == 10_000.0
    assert result.num_trades >= 0
    assert 0.0 <= result.win_rate <= 100.0
    assert result.max_drawdown_pct >= 0.0
    # 리포트 문자열 생성 확인
    assert "백테스트 결과" in result.report()


def test_backtester_no_lookahead_equity_len():
    bt = Backtester(_settings(), warmup=60)
    df = _wave_df(300)
    result = bt.run("ETH/USDT", df)
    assert len(result.equity_curve) == len(df) - 60
