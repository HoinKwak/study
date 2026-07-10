from crypto_trader.config import Settings
from crypto_trader.monitoring import Notifier, NotifyLevel, TradeJournal, TradeRecord
from crypto_trader.monitoring.dashboard import render_html, render_text


def _journal(tmp_path):
    return TradeJournal(state_dir=str(tmp_path))


def test_journal_open_close_and_persist(tmp_path):
    j = _journal(tmp_path)
    j.record_open(TradeRecord(
        symbol="BTC/USDT", direction="long", entry_price=60000, quantity=0.01,
        opened_at="2026-07-10T00:00:00+00:00", mode="dry_run",
        stop_price=59000, take_profit=62000,
    ))
    assert len(j.open_trades()) == 1
    rec = j.record_close("BTC/USDT", 62000, "2026-07-10T01:00:00+00:00", 20.0, "take_profit")
    assert rec is not None
    assert len(j.open_trades()) == 0
    assert len(j.closed_trades()) == 1

    # 재로딩 시 영속화 확인
    j2 = TradeJournal(state_dir=str(tmp_path))
    assert len(j2.closed_trades()) == 1
    assert j2.closed_trades()[0].pnl == 20.0


def test_journal_stats(tmp_path):
    j = _journal(tmp_path)
    for i, pnl in enumerate([10, -5, 20, -8, 15]):
        j.record_open(TradeRecord(
            symbol="ETH/USDT", direction="long", entry_price=3000, quantity=0.1,
            opened_at=f"2026-07-10T0{i}:00:00+00:00", mode="dry_run",
        ))
        exit_price = 3000 + pnl / 0.1
        j.record_close("ETH/USDT", exit_price, f"2026-07-10T0{i}:30:00+00:00", pnl, "tp")
    st = j.stats()
    assert st["total_trades"] == 5
    assert st["wins"] == 3
    assert st["losses"] == 2
    assert abs(st["total_pnl"] - 32.0) < 1e-6
    assert 59.9 < st["win_rate"] < 60.1


def test_dashboard_renders(tmp_path):
    j = _journal(tmp_path)
    j.record_open(TradeRecord(
        symbol="SOL/USDT", direction="short", entry_price=150, quantity=1,
        opened_at="2026-07-10T00:00:00+00:00", mode="paper",
        stop_price=155, take_profit=140,
    ))
    txt = render_text(j, equity=10000)
    assert "crypto-trader" in txt
    assert "SOL/USDT" in txt
    htm = render_html(j, equity=10000)
    assert "<html" in htm and "SOL/USDT" in htm


def test_notifier_without_telegram_is_console_only():
    s = Settings(binance_api_key="", binance_api_secret="",
                 telegram_bot_token="", telegram_chat_id="", notify_min_level="TRADE")
    n = Notifier(s)
    assert not n._tg_enabled
    # 예외 없이 동작해야 함
    n.trade("테스트 거래 알림")
    n.warn("경고")
    assert NotifyLevel.parse("ERROR") is NotifyLevel.ERROR
    assert NotifyLevel.parse("bogus") is NotifyLevel.INFO
