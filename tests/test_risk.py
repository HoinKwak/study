from crypto_trader.config import Settings
from crypto_trader.risk import RiskManager
from crypto_trader.signals.base import Direction


def _settings(**kw):
    base = dict(
        binance_api_key="", binance_api_secret="", binance_testnet=True,
        max_leverage=3, risk_per_trade_pct=1.0, max_open_positions=3,
        daily_max_loss_pct=5.0, entry_score_threshold=0.5,
    )
    base.update(kw)
    return Settings(**base)


def test_position_sizing_respects_risk():
    rm = RiskManager(_settings())
    equity = 10_000.0
    plan = rm.build_plan("BTC/USDT", Direction.LONG, entry_price=50_000, atr_value=500, equity=equity)
    assert plan is not None
    # risk_per_trade 1% of 10000 = 100 USDT
    assert abs(plan.risk_amount - 100.0) < 1e-6 or plan.risk_amount <= 100.0 + 1e-6
    # SL 은 진입가 아래(롱)
    assert plan.stop_price < plan.entry_price
    assert plan.take_profit > plan.entry_price


def test_leverage_cap():
    rm = RiskManager(_settings(max_leverage=2))
    # ATR 가 매우 작아 수량이 커지면 레버리지 상한에 걸려야 함
    plan = rm.build_plan("BTC/USDT", Direction.LONG, entry_price=50_000, atr_value=1, equity=10_000)
    assert plan is not None
    assert plan.notional <= 10_000 * 2 + 1e-3


def test_short_plan():
    rm = RiskManager(_settings())
    plan = rm.build_plan("ETH/USDT", Direction.SHORT, entry_price=3000, atr_value=30, equity=5000)
    assert plan is not None
    assert plan.stop_price > plan.entry_price   # 숏은 SL 위
    assert plan.take_profit < plan.entry_price


def test_daily_loss_limit_blocks():
    rm = RiskManager(_settings(daily_max_loss_pct=5.0))
    rm.start_day(10_000)
    rm.register_realized_pnl(-600)  # 6% 손실
    ok, reason = rm.can_open(open_positions=0)
    assert not ok
    assert "손실" in reason


def test_max_positions_blocks():
    rm = RiskManager(_settings(max_open_positions=2))
    rm.start_day(10_000)
    ok, _ = rm.can_open(open_positions=2)
    assert not ok
