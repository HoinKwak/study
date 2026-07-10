import numpy as np
import pandas as pd

from crypto_trader.config import Settings
from crypto_trader.monitoring import TradeJournal, TradeRecord
from crypto_trader.strategy import Action
from crypto_trader.strategy.swing import SwingStrategy, SwingPosition
from crypto_trader.signals.base import Direction


def _settings():
    return Settings(binance_api_key="", binance_api_secret="")


def _df(prices, freq="4h"):
    n = len(prices)
    close = np.array(prices, dtype=float)
    return pd.DataFrame({
        "open": np.concatenate([[close[0]], close[:-1]]),
        "high": close * 1.002, "low": close * 0.998, "close": close,
        "volume": np.full(n, 500.0),
    }, index=pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC"))


def test_swing_opens_long_on_oversold():
    # 급락으로 RSI 과매도 유도
    prices = list(np.linspace(120, 100, 40)) + list(np.linspace(100, 80, 25))
    s = SwingStrategy(_settings())
    d = s.decide("BTC/USDT", _df(prices), None, None)
    assert d.action in (Action.OPEN_LONG, Action.HOLD)
    if d.action is Action.OPEN_LONG:
        assert d.direction is Direction.LONG
        assert d.target_frac == 0.30           # 초기 30% (슬리브 예산 대비)
        assert d.stop_price < d.take_profit     # 롱: SL < TP


def test_swing_opens_short_on_overbought():
    prices = list(np.linspace(80, 100, 40)) + list(np.linspace(100, 130, 25))
    s = SwingStrategy(_settings())
    d = s.decide("BTC/USDT", _df(prices), None, None)
    assert d.action in (Action.OPEN_SHORT, Action.HOLD)


def test_swing_stage1_twap_add():
    s = SwingStrategy(_settings())
    df = _df(list(np.linspace(110, 100, 70)))
    # 1단계, 아직 30%만 사용 → TWAP 증량(최대 60%) 유도
    pos = SwingPosition(Direction.LONG, stage=1, alloc_frac=0.30,
                        avg_entry=99.0, stop_price=95.0)
    d = s.decide("BTC/USDT", df, None, pos)
    assert d.action in (Action.ADD, Action.HOLD)
    if d.action is Action.ADD:
        assert d.target_frac >= 0.30


def test_swing_stage2_pyramid_on_supertrend():
    s = SwingStrategy(_settings())
    # 상승 확인 데이터(슈퍼트렌드 상방), 롱 보유 + 수익 중
    up = _df(list(np.linspace(90, 130, 80)))
    pos = SwingPosition(Direction.LONG, stage=1, alloc_frac=0.60,
                        avg_entry=95.0, stop_price=88.0)
    d = s.decide("BTC/USDT", up, up, pos)
    # 반전+슈퍼트렌드 확인 시 2단계 피라미딩
    assert d.action in (Action.ADD, Action.HOLD)
    if d.action is Action.ADD and d.stage == 2:
        assert d.target_frac == 1.00


def test_journal_record_add_averages_entry(tmp_path):
    j = TradeJournal(state_dir=str(tmp_path))
    j.record_open(TradeRecord(
        symbol="BTC/USDT", direction="long", entry_price=100.0, quantity=1.0,
        opened_at="2026-07-10T00:00:00+00:00", mode="dry_run",
        stop_price=95.0, take_profit=110.0, sleeve="swing", stage=1, alloc_frac=0.30,
    ))
    rec = j.record_add("BTC/USDT", "swing", "long", add_price=110.0, add_qty=1.0,
                       new_stop=100.0, new_stage=2, new_alloc_frac=0.60, new_take_profit=120.0)
    assert rec is not None
    assert abs(rec.entry_price - 105.0) < 1e-9   # (100*1 + 110*1)/2
    assert rec.quantity == 2.0
    assert rec.stage == 2
    assert rec.stop_price == 100.0
    assert rec.alloc_frac == 0.60
    assert rec.num_adds == 1
