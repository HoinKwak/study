"""현재 상태/성과 출력 및 HTML 대시보드 생성.

    python -m scripts.status              # CLI 요약 출력
    python -m scripts.status --html       # state/dashboard.html 생성
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.monitoring import TradeJournal  # noqa: E402
from crypto_trader.monitoring.dashboard import render_html, render_text  # noqa: E402
from crypto_trader.scanner import EventStore  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="crypto-trader 상태 대시보드")
    parser.add_argument("--html", action="store_true", help="HTML 대시보드 생성")
    args = parser.parse_args()

    s = get_settings()
    journal = TradeJournal(s.state_dir)

    # 잔고는 거래소 연결이 되면 표시(없으면 생략)
    equity = None
    if s.has_binance_keys:
        try:
            from crypto_trader.connectors import BinanceClient
            equity = BinanceClient(s).fetch_balance_usdt()
        except Exception:  # noqa: BLE001
            equity = None

    print(render_text(journal, equity))

    if args.html:
        from crypto_trader.monitoring.dashboard import (  # noqa: E402
            btc_buyhold_series, journal_span_days, load_start_equity)
        events = EventStore.load(s.state_dir).recent(40)
        start_eq = load_start_equity(s.state_dir)
        btc = btc_buyhold_series(journal_span_days(journal))
        out = Path(s.state_dir) / "dashboard.html"
        out.write_text(render_html(journal, equity, events=events,
                                   start_equity=start_eq, btc_series=btc),
                       encoding="utf-8")
        print(f"\nHTML 대시보드 생성: {out}")


if __name__ == "__main__":
    main()
