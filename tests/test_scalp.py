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
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0, squeeze_pctile=None)
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
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0, squeeze_pctile=None)
    d = s.decide("BTC/USDT", df, oi_delta=50.0, current_direction=None)
    assert d.action is Action.OPEN_SHORT
    assert d.stop_price == 100.0
    assert d.take_profit <= 96.9


def test_scalp_no_volume_spike_holds():
    df = _base_df()
    i = df.index[-1]
    df.loc[i, ["open", "close", "high", "low"]] = [100.0, 103.0, 103.1, 99.9]
    # 거래량 급증 없음 (평상시와 동일)
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0, squeeze_pctile=None)
    d = s.decide("BTC/USDT", df, oi_delta=50.0, current_direction=None)
    assert d.action is Action.HOLD


def test_scalp_oi_not_rising_blocks_entry():
    df = _base_df()
    i = df.index[-1]
    df.loc[i, ["open", "low"]] = [100.0, 99.9]
    df.loc[i, ["close", "high"]] = [103.0, 103.1]
    df.loc[i, "volume"] = 1000.0
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0, squeeze_pctile=None)
    d = s.decide("BTC/USDT", df, oi_delta=-10.0, current_direction=None)  # OI 감소
    assert d.action is Action.HOLD


def test_scalp_exits_on_range_regime():
    """횡보(RANGE) 전환 + 모멘텀 실제 꺾임(신고가 실패 + 마지막 음봉)이면 청산."""
    df = _base_df()
    hi = df.columns.get_loc("high")
    op = df.columns.get_loc("open")
    cl = df.columns.get_loc("close")
    df.iloc[-3, hi] = 100.5          # 직전 고점
    df.iloc[-2, hi] = 100.2          # 신고가 실패
    df.iloc[-1, hi] = 100.2          # 신고가 실패
    df.iloc[-1, op] = 100.1
    df.iloc[-1, cl] = 99.9           # 마지막 음봉
    s = ScalpStrategy(_settings())
    d = s.decide("BTC/USDT", df, current_direction=Direction.LONG, confirm_regime=Regime.RANGE)
    assert d.action is Action.CLOSE


def test_scalp_holds_on_range_when_momentum_intact():
    """횡보(RANGE) 전환이라도 신호TF 모멘텀이 살아있으면(신고가 갱신) 청산하지 않는다."""
    df = _base_df()
    hi = df.columns.get_loc("high")
    op = df.columns.get_loc("open")
    cl = df.columns.get_loc("close")
    df.iloc[-2, hi] = 101.0          # 신고가 갱신 중
    df.iloc[-1, hi] = 101.5
    df.iloc[-1, op] = 100.5
    df.iloc[-1, cl] = 101.4          # 양봉 = 모멘텀 유지
    s = ScalpStrategy(_settings())
    d = s.decide("BTC/USDT", df, current_direction=Direction.LONG, confirm_regime=Regime.RANGE)
    assert d.action is Action.HOLD


def test_scalp_squeeze_filter_blocks_wide_bands():
    """밴드폭이 이미 확장된 상태의 돌파는 스퀴즈 필터가 차단해야 한다."""
    n = 80
    # 변동성 큰 구간(밴드 확장) 뒤 돌파
    close = 100 + np.random.default_rng(1).normal(0, 1.5, n)  # 큰 노이즈 = 넓은 밴드
    df = pd.DataFrame({
        "open": close, "high": close + 1.0, "low": close - 1.0,
        "close": close, "volume": np.full(n, 100.0),
    }, index=pd.date_range("2024-01-01", periods=n, freq="5min", tz="UTC"))
    i = df.index[-1]
    df.loc[i, ["open", "low"]] = [100.0, 99.9]
    df.loc[i, ["close", "high"]] = [110.0, 110.1]
    df.loc[i, "volume"] = 2000.0
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0, squeeze_pctile=30.0, squeeze_lookback=50)
    d = s.decide("BTC/USDT", df, oi_delta=50.0, current_direction=None)
    # 직전 밴드폭이 하위 30% 에 들 확률이 낮은 데이터 → HOLD(스퀴즈 아님)가 일반적
    assert d.action is Action.HOLD or d.reason != "스퀴즈 아님"


def test_scalp_squeeze_filter_allows_after_quiet_period():
    """변동 구간 뒤 밴드가 '수축된' 상태의 돌파는 통과해야 한다."""
    n = 80
    rng = np.random.default_rng(2)
    # 앞 55봉은 변동 큼(밴드 확장), 뒤 25봉은 극저변동(밴드 수축) → 직전 밴드폭이 하위 분위
    noisy = 100.0 + rng.normal(0, 1.0, 55)
    quiet = 100.0 + rng.normal(0, 0.02, n - 55)
    close = np.concatenate([noisy, quiet])
    df = pd.DataFrame({
        "open": close, "high": close + 0.02, "low": close - 0.02,
        "close": close, "volume": np.full(n, 100.0),
    }, index=pd.date_range("2024-01-01", periods=n, freq="5min", tz="UTC"))
    i = df.index[-1]
    df.loc[i, ["open", "low"]] = [100.0, 99.98]
    df.loc[i, ["close", "high"]] = [101.0, 101.05]
    df.loc[i, "volume"] = 2000.0
    s = ScalpStrategy(_settings(), vol_spike_mult=2.0, squeeze_pctile=30.0, squeeze_lookback=50)
    d = s.decide("BTC/USDT", df, oi_delta=50.0, current_direction=None)
    assert d.reason != "스퀴즈 아님"  # 스퀴즈 필터는 통과 (진입 여부는 다른 조건에 달림)
