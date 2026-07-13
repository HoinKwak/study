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


def _breakout_df(n=200, seed=3):
    """스퀴즈→강봉 돌파→연속 신고가→하락 을 주기적으로 반복(스캘프 진입 유발)."""
    rng = np.random.default_rng(seed)
    close = np.full(n, 100.0)
    for i in range(1, n):
        close[i] = 100 + rng.normal(0, 0.02)      # 초저변동 스퀴즈
    for b in range(40, n, 50):                     # 주기적 돌파
        close[b] = close[b - 1] + 1.4
        for k in range(1, 4):
            if b + k < n:
                close[b + k] = close[b + k - 1] + 0.4
        if b + 4 < n:
            close[b + 4] = close[b + 3] - 0.6
    open_ = np.concatenate([[close[0]], close[:-1]])
    high = np.maximum(open_, close) + 0.02
    low = np.minimum(open_, close) - 0.02
    vol = np.full(n, 100.0)
    for b in range(40, n, 50):
        vol[b] = 2500.0                            # 돌파봉 거래량 급증
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close,
                         "volume": vol},
                        index=pd.date_range("2024-01-01", periods=n, freq="15min", tz="UTC"))


def _scalp_settings():
    return Settings(binance_api_key="", binance_api_secret="", scalp_vol_spike_mult=5.0,
                    scalp_squeeze_pctile=60.0, scalp_min_body_atr=1.0,
                    scalp_require_regime=False, daily_max_loss_pct=100.0)


def test_momentum_exit_modes_fire_their_logic():
    """회귀: momentum 계열이 고정TP로 새지 않고 각자 청산 로직을 실제로 실행한다.

    (과거 _scalp_ref 초기화가 == 'momentum' 에만 걸려 split/bandwalk 가 고정TP로
    빠지던 버그를 방지 — split→'momentum_split', be→'runner_be_stall' 사유 확인.)
    """
    df = _breakout_df()
    s = _scalp_settings()

    def reasons(mode, mult=1.5):
        bt = SleeveBacktester(s, "scalp", confirm_tf="1h", warmup=60,
                              scalp_exit_mode=mode, trail_atr_mult=mult)
        res = bt.run("X/USDT", df)
        return [t.reason for t in res.trades]

    r_single = reasons("momentum")
    r_split = reasons("momentum_split")
    r_be = reasons("momentum_be")
    r_trail = reasons("momentum_trail")

    assert r_single and all(x == "momentum_tp" for x in r_single)
    assert r_split and all(x == "momentum_split" for x in r_split)  # 분할이 실제로 발동
    assert r_be and all(x == "runner_be_stall" for x in r_be)       # [A] 본절 러너 스톨 청산
    assert r_trail and len(r_trail) == len(r_split)                 # [B] 트레일링도 동일 진입셋


def test_fees_reduce_pnl():
    """수수료 있는 버전이 없는 버전보다 손익이 낮거나 같아야 한다."""
    df = _wave_df(800)
    no_fee = SleeveBacktester(_settings(), "mid", confirm_tf="1h", warmup=100,
                              taker_fee=0.0, slippage=0.0).run("BTC/USDT", df)
    with_fee = SleeveBacktester(_settings(), "mid", confirm_tf="1h", warmup=100,
                                taker_fee=0.001, slippage=0.001).run("BTC/USDT", df)
    if no_fee.num_trades > 0:
        assert with_fee.ending_equity <= no_fee.ending_equity + 1e-6
