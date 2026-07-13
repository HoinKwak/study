"""단타 트레일링 러너 청산(dry_run 시뮬레이션): 1차 50% 익절 → 트레일 상향 → 이탈 청산."""
from __future__ import annotations

import pandas as pd

from crypto_trader.config import Settings, TradeMode
from crypto_trader.monitoring import TradeJournal, TradeRecord
from crypto_trader.portfolio.sleeve import Sleeve
from crypto_trader.portfolio.worker import SleeveWorker


class _Notifier:
    def __init__(self):
        self.msgs = []
    def trade(self, msg, title=""):
        self.msgs.append((title, msg))
    def warn(self, *a, **k): pass
    def error(self, *a, **k): pass
    def info(self, *a, **k): pass


def _worker(journal, mult=1.0):
    sleeve = Sleeve(name="scalp", allocation=1.0, signal_tf="15m", confirm_tf="1h",
                    strategy_kind="scalp", eval_interval_sec=900, symbols=["BTC/USDT"])
    s = Settings(binance_api_key="", binance_api_secret="", trade_mode=TradeMode.DRY_RUN,
                 scalp_exit_mode="trailing", scalp_trail_atr_mult=mult, daily_max_loss_pct=100.0)
    return SleeveWorker(sleeve, s, binance=None, deriv_data=None, executor=None,
                        journal=journal, notifier=_Notifier())


def _df(last_high, last_low, last_close, n=20, base=100.0, rng=0.5):
    """ATR≈1.0(범위 1.0)인 평탄 구간 + 지정한 마지막 봉."""
    rows = []
    idx = pd.date_range("2024-01-01", periods=n, freq="15min", tz="UTC")
    for _ in range(n - 1):
        rows.append((base, base + rng, base - rng, base))
    rows.append((last_close, last_high, last_low, last_close))
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=idx)
    df["volume"] = 100.0
    return df


def _open(journal, entry=100.0, stop=99.0, sig_high=100.6):
    journal.record_open(TradeRecord(
        symbol="BTC/USDT", direction="long", entry_price=entry, quantity=1.0,
        opened_at="2024-01-01T00:00:00+00:00", mode="dry_run",
        stop_price=stop, take_profit=0.0, sleeve="scalp", signal_high=sig_high,
        signal_low=99.4))
    return journal.open_trades()[-1]


def test_trailing_tp1_then_trail_up_then_exit(tmp_path):
    j = TradeJournal(str(tmp_path))
    rec = _open(j)
    w = _worker(j, mult=1.0)

    # 1) 신고가(101>100.6) → 1차 50% 익절, 러너 전환, 트레일=최고가−1×ATR(≈100)
    closed = w._scalp_momentum_exit("BTC/USDT", _df(101.0, 100.4, 100.8))
    assert closed is False
    assert rec.half_closed is True
    assert abs(rec.run_ext - 101.0) < 1e-9
    assert abs(rec.quantity - 0.5) < 1e-9            # 50% 남음
    assert 99.0 < rec.stop_price < 101.0             # 원 SL(99) 위로·최고가 아래로 트레일
    assert len(j.closed_trades()) == 1               # tp1 하위체결 기록
    s1 = rec.stop_price

    # 2) 더 높은 신고가(102) → 트레일 상향, 미청산
    closed = w._scalp_momentum_exit("BTC/USDT", _df(102.0, 101.4, 101.6))
    assert closed is False
    assert abs(rec.run_ext - 102.0) < 1e-9
    assert rec.stop_price > s1                       # 트레일 단조 상향
    s2 = rec.stop_price

    # 3) 트레일 이탈 종가(100.8 ≤ 트레일 s2≈101) → 러너 청산 at 트레일가
    closed = w._scalp_momentum_exit("BTC/USDT", _df(101.5, 100.5, 100.8))
    assert closed is True
    assert not j.open_trades()                       # 전량 청산됨
    runner = [t for t in j.closed_trades() if t.exit_reason == "momentum_trail"]
    assert runner and abs(runner[0].exit_price - s2) < 1e-9  # 직전 트레일 가격에 청산


def test_trailing_stop_is_monotonic(tmp_path):
    """되돌림이 와도 트레일 스톱은 내려가지 않는다(롱)."""
    j = TradeJournal(str(tmp_path))
    rec = _open(j)
    w = _worker(j, mult=1.0)
    w._scalp_momentum_exit("BTC/USDT", _df(101.0, 100.4, 100.8))   # 러너 전환, 트레일 s1
    s1 = rec.stop_price
    # 신고가 없이 눌림 → run_ext 유지, 트레일 하락 금지
    w._scalp_momentum_exit("BTC/USDT", _df(100.9, 100.2, 100.5))
    assert abs(rec.run_ext - 101.0) < 1e-9           # 최고가 유지
    assert rec.stop_price >= s1 - 1e-9               # 내려가지 않음
