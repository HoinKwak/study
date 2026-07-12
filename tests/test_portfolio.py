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
    # 단타 전용 3-타임프레임(중기·스윙 제외)
    assert names == {"scalp3m", "scalp", "scalp10m"}


def test_sleeve_timeframes():
    sleeves = {s.name: s for s in default_sleeves(_settings())}
    assert sleeves["scalp3m"].signal_tf == "3m" and sleeves["scalp3m"].confirm_tf == "15m"
    assert sleeves["scalp"].signal_tf == "5m" and sleeves["scalp"].confirm_tf == "15m"
    assert sleeves["scalp10m"].signal_tf == "10m" and sleeves["scalp10m"].confirm_tf == "30m"
    assert all(sl.strategy_kind == "scalp" for sl in sleeves.values())


def test_allocated_equity():
    s = Sleeve(name="swing", allocation=0.5, signal_tf="4h", confirm_tf="1d",
               strategy_kind="regime", eval_interval_sec=3600)
    assert s.allocated_equity(10_000) == 5_000


def test_default_sleeves_use_configured_symbols():
    s = _settings()
    sleeves = {sl.name: sl for sl in default_sleeves(s)}
    # 단타는 SOL 제외 (백테스트에서 엣지 없음 확인). 3개 슬리브 모두 동일 유니버스.
    for name in ("scalp3m", "scalp", "scalp10m"):
        assert sleeves[name].symbols == ["BTC/USDT", "ETH/USDT"]
        assert sleeves[name].min_universe_volume == 30e6
        assert sleeves[name].dynamic_universe is True
