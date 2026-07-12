"""수동/외부 청산 리컨실 — 실제 체결가·실현손익 반영, SL과 라벨 구분."""
from __future__ import annotations

from crypto_trader.config import Settings, TradeMode
from crypto_trader.monitoring import TradeJournal, TradeRecord
from crypto_trader.portfolio.sleeve import Sleeve
from crypto_trader.portfolio.worker import SleeveWorker


class _FakeBinance:
    def __init__(self, positions, realized=None):
        self._positions = positions
        self._realized = realized  # (exit_vwap, realized_pnl) 또는 None
        self.canceled = []

    def fetch_positions(self, symbol=None):
        return self._positions

    def resolve_symbol(self, s):
        return s

    def cancel_all_orders(self, s):
        self.canceled.append(s)

    def fetch_realized_close(self, symbol, direction, since_ms):
        return self._realized


class _Notifier:
    def __init__(self):
        self.msgs = []
    def trade(self, msg, title=""):
        self.msgs.append((title, msg))
    def warn(self, *a, **k): pass
    def error(self, *a, **k): pass


def _worker(binance, journal):
    sleeve = Sleeve(name="scalp", allocation=0.25, signal_tf="5m", confirm_tf="15m",
                    strategy_kind="scalp", eval_interval_sec=300, symbols=["WLD/USDT"])
    s = Settings(binance_api_key="", binance_api_secret="", trade_mode=TradeMode.PAPER)
    n = _Notifier()
    w = SleeveWorker(sleeve, s, binance=binance, deriv_data=None,
                     executor=None, journal=journal, notifier=n)
    return w, n


def _open(journal, qty=1000.0, entry=0.41, stop=0.40):
    journal.record_open(TradeRecord(
        symbol="WLD/USDT", direction="long", entry_price=entry, quantity=qty,
        opened_at="2026-07-12T00:00:00+00:00", mode="paper",
        stop_price=stop, take_profit=0.43, sleeve="scalp"))
    return journal.open_trades()[-1]


def test_manual_close_uses_real_pnl_and_label(tmp_path):
    """포지션이 사라지고 청산가가 SL과 다르면 '수동/외부 청산'으로 실현손익 반영."""
    j = TradeJournal(str(tmp_path))
    _open(j, qty=1000.0, entry=0.41, stop=0.40)
    # 거래소엔 포지션 없음 + 실제 청산 VWAP 0.45(SL 0.40과 다름), 실현손익 +38.5
    b = _FakeBinance(positions=[], realized=(0.45, 38.5))
    w, n = _worker(b, j)
    w._reconcile_exchange_exits()

    closed = j.closed_trades()
    assert len(closed) == 1
    assert closed[0].exit_reason == "수동/외부 청산"
    assert abs(closed[0].pnl - 38.5) < 1e-6      # 거래소 실현손익 그대로
    assert abs(closed[0].exit_price - 0.45) < 1e-9
    assert n.msgs and "수동/외부" in n.msgs[-1][0]  # 알림 제목 구분


def test_sl_close_labeled_sl(tmp_path):
    """청산가가 SL 가격 근처면 'exchange_sl' 로 라벨."""
    j = TradeJournal(str(tmp_path))
    _open(j, qty=1000.0, entry=0.41, stop=0.40)
    b = _FakeBinance(positions=[], realized=(0.4001, -9.9))  # SL 0.40 근처
    w, n = _worker(b, j)
    w._reconcile_exchange_exits()

    closed = j.closed_trades()
    assert closed[0].exit_reason == "exchange_sl"
    assert "SL" in n.msgs[-1][0]


def test_fallback_to_sl_price_when_no_trades(tmp_path):
    """체결내역 조회 불가면 기존처럼 SL 가격으로 근사(reason exchange_sl)."""
    j = TradeJournal(str(tmp_path))
    _open(j, qty=1000.0, entry=0.41, stop=0.40)
    b = _FakeBinance(positions=[], realized=None)
    w, n = _worker(b, j)
    w._reconcile_exchange_exits()

    closed = j.closed_trades()
    assert closed[0].exit_reason == "exchange_sl"
    assert abs(closed[0].exit_price - 0.40) < 1e-9
