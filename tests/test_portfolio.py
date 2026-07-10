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
    assert names == {"swing", "mid", "scalp"}


def test_sleeve_timeframes():
    sleeves = {s.name: s for s in default_sleeves(_settings())}
    assert sleeves["swing"].signal_tf == "4h" and sleeves["swing"].confirm_tf == "1d"
    assert sleeves["mid"].signal_tf == "15m" and sleeves["mid"].confirm_tf == "1h"
    assert sleeves["scalp"].signal_tf == "1m" and sleeves["scalp"].confirm_tf == "5m"
    assert sleeves["scalp"].strategy_kind == "scalp"
    assert sleeves["swing"].strategy_kind == "regime"


def test_allocated_equity():
    s = Sleeve(name="swing", allocation=0.5, signal_tf="4h", confirm_tf="1d",
               strategy_kind="regime", eval_interval_sec=3600)
    assert s.allocated_equity(10_000) == 5_000


def test_default_sleeves_use_configured_symbols():
    s = _settings()
    for sleeve in default_sleeves(s):
        assert sleeve.symbols == ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
