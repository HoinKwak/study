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


def test_position_notional_cap():
    # 포지션당 명목가치를 계좌 10% 로 제한
    rm = RiskManager(_settings(max_leverage=30, max_position_notional_pct=10.0),
                     max_leverage=30)
    account = 10_000.0
    # ATR 이 매우 작아 수량이 커지는 상황 → 명목 상한(1000)에 걸려야 함
    plan = rm.build_plan("BTC/USDT", Direction.LONG, entry_price=50_000, atr_value=1,
                         equity=account, account_equity=account)
    assert plan is not None
    assert plan.notional <= account * 0.10 + 1e-6   # 계좌의 10% 이하


def test_position_notional_cap_with_stop():
    rm = RiskManager(_settings(max_leverage=30, max_position_notional_pct=10.0),
                     max_leverage=30)
    account = 10_000.0
    plan = rm.build_plan_with_stop("BTC/USDT", Direction.LONG, entry_price=50_000,
                                   stop_price=49_990, take_profit=50_050,
                                   equity=account, account_equity=account)
    assert plan is not None
    assert plan.notional <= account * 0.10 + 1e-6


def test_no_cap_when_pct_100():
    rm = RiskManager(_settings(max_leverage=30, max_position_notional_pct=100.0),
                     max_leverage=30)
    account = 10_000.0
    plan = rm.build_plan_with_stop("BTC/USDT", Direction.LONG, entry_price=50_000,
                                   stop_price=49_990, take_profit=50_050,
                                   equity=account, account_equity=account)
    assert plan is not None
    # 100% 면 상한 미적용 → 레버리지 상한(30x)까지 허용
    assert plan.notional > account * 0.10


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
