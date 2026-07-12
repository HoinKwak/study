"""단타 부분청산 짜바리(dust) 방지 검증.

- 청산 수량을 스텝사이즈로 반올림하고 저널 잔량을 같은 값으로 동기화(드리프트 0).
- 분할 후 꼬리가 최소주문량 미만이면 분할을 포기(False)해 청산 불가 잔량을 안 남긴다.
"""
from __future__ import annotations

from crypto_trader.config import Settings, TradeMode
from crypto_trader.monitoring import TradeJournal, TradeRecord
from crypto_trader.portfolio.sleeve import Sleeve
from crypto_trader.portfolio.worker import SleeveWorker


class _FakeBinance:
    """수량 정밀도(step)와 최소주문량을 흉내내는 스텁."""
    def __init__(self, step: float, min_amt: float):
        self.step = step
        self.min_amt = min_amt
        self.closed: list[float] = []

    def amount_to_precision(self, symbol: str, amount: float) -> float:
        # step 배수로 내림
        return round((amount // self.step) * self.step, 10)

    def min_amount(self, symbol: str) -> float:
        return self.min_amt

    def close_quantity(self, symbol: str, direction: str, qty: float):
        self.closed.append(qty)
        return {"qty": qty}

    def cancel_all_orders(self, symbol: str):
        return None


class _Notifier:
    def trade(self, *a, **k): pass
    def warn(self, *a, **k): pass
    def error(self, *a, **k): pass


def _worker(binance, journal):
    sleeve = Sleeve(name="scalp", allocation=0.25, signal_tf="5m", confirm_tf="15m",
                    strategy_kind="scalp", eval_interval_sec=300, symbols=["WLD/USDT"])
    s = Settings(binance_api_key="", binance_api_secret="", trade_mode=TradeMode.PAPER)
    return SleeveWorker(sleeve, s, binance=binance, deriv_data=None,
                        executor=None, journal=journal, notifier=_Notifier())


def _open(journal, qty):
    journal.record_open(TradeRecord(
        symbol="WLD/USDT", direction="long", entry_price=0.41, quantity=qty,
        opened_at="2026-07-12T00:00:00+00:00", mode="paper",
        stop_price=0.40, take_profit=0.43, sleeve="scalp",
        signal_high=0.42, signal_low=0.40))
    return journal.open_trades()[-1]


def test_partial_close_syncs_journal_no_dust(tmp_path):
    """반올림된 청산분과 저널 잔량이 정확히 일치(드리프트 0)."""
    b = _FakeBinance(step=1.0, min_amt=1.0)
    j = TradeJournal(str(tmp_path))
    rec = _open(j, qty=101.0)          # 홀수 → 50%가 50.5 → step 반올림 필요
    w = _worker(b, j)

    ok = w._scalp_partial_close(rec, price=0.42, frac=0.5, reason="momentum_tp1")
    assert ok is True
    closed_qty = b.closed[-1]          # 거래소에 실제 보낸 수량
    assert closed_qty == 50.0          # 50.5 → step 1.0 내림
    assert rec.quantity == 51.0        # 저널 잔량 = 101 - 50 (동기화, 드리프트 없음)
    # 잔량 51 은 최소주문량 이상 → 전량 청산으로 짜바리 없이 닫을 수 있음
    assert rec.quantity >= b.min_amount("WLD/USDT")


def test_partial_close_refuses_when_tail_below_min(tmp_path):
    """분할 후 꼬리가 최소주문량 미만이면 분할 포기(False) → 전량청산에 맡김."""
    b = _FakeBinance(step=1.0, min_amt=60.0)   # 최소주문량 크게
    j = TradeJournal(str(tmp_path))
    rec = _open(j, qty=101.0)          # 50% = 50 < 60(min) → 분할 불가
    w = _worker(b, j)

    ok = w._scalp_partial_close(rec, price=0.42, frac=0.5, reason="momentum_tp1")
    assert ok is False
    assert b.closed == []              # 거래소 주문 안 보냄
    assert rec.quantity == 101.0       # 수량 그대로(상태 불변)
