"""고아 슬리브 리컨실 — 제거·개명된 옛 슬리브의 열린 포지션을 엔진이 정리."""
from __future__ import annotations

from crypto_trader.config import Settings, TradeMode
from crypto_trader.monitoring import TradeJournal, TradeRecord
from crypto_trader.portfolio.engine import PortfolioEngine
from crypto_trader.portfolio.sleeve import Sleeve


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
    def info(self, *a, **k): pass


def _engine(binance, journal, notifier, active_names=("scalp",)):
    """__init__(네트워크) 없이 리컨실에 필요한 속성만 채운 엔진."""
    e = object.__new__(PortfolioEngine)
    e.s = Settings(binance_api_key="", binance_api_secret="", trade_mode=TradeMode.PAPER)
    e.binance = binance
    e.journal = journal
    e.notifier = notifier
    e.sleeves = [Sleeve(name=n, allocation=1.0, signal_tf="15m", confirm_tf="1h",
                        strategy_kind="scalp", eval_interval_sec=900, symbols=[])
                 for n in active_names]
    return e


def _open(journal, symbol, direction, sleeve, entry, qty, stop):
    journal.record_open(TradeRecord(
        symbol=symbol, direction=direction, entry_price=entry, quantity=qty,
        opened_at="2026-07-12T00:00:00+00:00", mode="paper",
        stop_price=stop, take_profit=entry * 1.05, sleeve=sleeve))


def test_orphan_of_removed_sleeve_is_reconciled(tmp_path):
    """제거된 슬리브('mid')로 열린 포지션이 거래소에서 사라지면 청산 반영."""
    j = TradeJournal(str(tmp_path))
    _open(j, "SOL/USDT", "short", "mid", entry=77.04, qty=7.0, stop=77.33)   # 고아
    _open(j, "MAGMA/USDT", "long", "scalp", entry=0.62, qty=100.0, stop=0.60)  # 활성
    # 거래소엔 포지션 없음(수동청산) + 실제 청산 VWAP 75.74, 실현손익 +9.1
    b = _FakeBinance(positions=[], realized=(75.74, 9.1))
    e = _engine(b, j, _Notifier())
    e._reconcile_orphan_exits()

    closed = {t.symbol: t for t in j.closed_trades()}
    opens = {t.symbol for t in j.open_trades()}
    assert "SOL/USDT" in closed                       # 고아 청산됨
    assert closed["SOL/USDT"].sleeve == "mid"         # 원 슬리브로 매칭
    assert abs(closed["SOL/USDT"].pnl - 9.1) < 1e-6   # 실현손익 그대로
    assert closed["SOL/USDT"].exit_reason == "수동/외부 청산"
    assert "MAGMA/USDT" in opens and "SOL/USDT" not in opens  # 활성 슬리브는 건드리지 않음
    assert "SOL/USDT" in b.canceled                   # 잔여 주문 정리


def test_orphan_still_live_is_not_closed(tmp_path):
    """고아 포지션이 거래소에 아직 열려 있으면 저널을 닫지 않는다(수동 정리 대상)."""
    j = TradeJournal(str(tmp_path))
    _open(j, "SOL/USDT", "short", "mid", entry=77.04, qty=7.0, stop=77.33)
    b = _FakeBinance(positions=[{"symbol": "SOL/USDT", "side": "short", "contracts": 7.0}])
    e = _engine(b, j, _Notifier())
    e._reconcile_orphan_exits()

    assert {t.symbol for t in j.open_trades()} == {"SOL/USDT"}  # 여전히 열림
    assert not j.closed_trades()


def test_no_orphans_no_network(tmp_path):
    """활성 슬리브 포지션만 있으면 고아 스윕이 거래소 조회조차 하지 않는다."""
    j = TradeJournal(str(tmp_path))
    _open(j, "MAGMA/USDT", "long", "scalp", entry=0.62, qty=100.0, stop=0.60)

    class _Boom(_FakeBinance):
        def fetch_positions(self, symbol=None):
            raise AssertionError("고아 없으면 조회하면 안 됨")

    e = _engine(_Boom(positions=[]), j, _Notifier())
    e._reconcile_orphan_exits()   # 예외 없이 통과해야 함
    assert {t.symbol for t in j.open_trades()} == {"MAGMA/USDT"}
