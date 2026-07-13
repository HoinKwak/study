from crypto_trader.config import Settings
from crypto_trader.portfolio import default_sleeves
from crypto_trader.portfolio.sleeve import Sleeve


def _settings():
    return Settings(binance_api_key="", binance_api_secret="",
                    symbols=["BTC/USDT", "ETH/USDT", "SOL/USDT"])


def test_default_sleeves_allocations_sum_to_one():
    sleeves = default_sleeves(_settings())
    assert abs(sum(s.allocation for s in sleeves) - 1.0) < 1e-9
    names = {s.name for s in sleeves}
    # 단타 전용 단일 15m 슬리브(중기·스윙·저TF 제외)
    assert names == {"scalp"}


def test_sleeve_timeframes():
    sleeves = {s.name: s for s in default_sleeves(_settings())}
    assert sleeves["scalp"].signal_tf == "15m" and sleeves["scalp"].confirm_tf == "1h"
    assert all(sl.strategy_kind == "scalp" for sl in sleeves.values())


def test_allocated_equity():
    s = Sleeve(name="swing", allocation=0.5, signal_tf="4h", confirm_tf="1d",
               strategy_kind="regime", eval_interval_sec=3600)
    assert s.allocated_equity(10_000) == 5_000


def test_default_sleeves_use_configured_symbols():
    s = _settings()
    sleeves = {sl.name: sl for sl in default_sleeves(s)}
    # 단타는 SOL 제외 (백테스트에서 엣지 없음 확인). 유니버스 30M.
    assert sleeves["scalp"].symbols == ["BTC/USDT", "ETH/USDT"]
    assert sleeves["scalp"].min_universe_volume == 30e6
    assert sleeves["scalp"].dynamic_universe is True
