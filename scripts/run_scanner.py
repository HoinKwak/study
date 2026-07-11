"""바이낸스 선물 시장 스캐너 — 급등/급락/거래량·OI 급증/펀딩 극단 알림.

    python -m scripts.run_scanner            # 무한 루프(주기 스캔) + 대시보드 갱신
    python -m scripts.run_scanner --once     # 1회 스캔 후 종료

자동매매는 하지 않는다. 감지된 이벤트는 텔레그램으로 알림 + state/scanner_events.json
에 저장되고, state/dashboard.html 을 매 사이클 갱신한다(브라우저로 열어두면 자동 새로고침).
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.monitoring import Notifier, TradeJournal  # noqa: E402
from crypto_trader.monitoring.dashboard import (  # noqa: E402
    btc_buyhold_series, journal_span_days, load_equity, load_start_equity, render_html)
from crypto_trader.scanner import MarketScanner  # noqa: E402
from crypto_trader.utils import get_logger  # noqa: E402


def _write_dashboard(settings, scanner: MarketScanner, refresh_sec: int) -> None:
    """이벤트 + 거래 저널을 합쳐 state/dashboard.html 갱신."""
    try:
        journal = TradeJournal(settings.state_dir)
        events = scanner.store.recent(40)
        start_eq = load_start_equity(settings.state_dir)
        btc = btc_buyhold_series(journal_span_days(journal))
        from crypto_trader.monitoring.market_extra import load_cached, load_tickers
        from crypto_trader.monitoring.dashboard import load_equity_history
        extra = load_cached(settings.state_dir, settings.scanner_min_volume)
        tickers = load_tickers(settings.state_dir)
        out = Path(settings.state_dir) / "dashboard.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            render_html(journal, equity=load_equity(settings.state_dir), events=events, refresh_sec=refresh_sec,
                        start_equity=start_eq, btc_series=btc, market_extra=extra,
                        tickers=tickers, equity_history=load_equity_history(settings.state_dir)),
            encoding="utf-8",
        )
    except Exception:  # noqa: BLE001 — 대시보드 실패가 스캔을 막지 않게
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="바이낸스 선물 시장 스캐너")
    parser.add_argument("--once", action="store_true", help="1회 스캔 후 종료")
    args = parser.parse_args()

    settings = get_settings()
    log = get_logger("scanner-main", settings.log_level)

    scanner = MarketScanner(settings, notifier=Notifier(settings))
    refresh = max(30, settings.scanner_interval_sec)

    if args.once:
        scanner.scan_once()
        _write_dashboard(settings, scanner, refresh_sec=0)
        return

    log.info("시장 스캐너 상시 구동 — 주기 %ds (Ctrl+C 종료)", refresh)
    while True:
        try:
            scanner.scan_once()
        except KeyboardInterrupt:
            log.info("스캐너 종료")
            break
        except Exception as e:  # noqa: BLE001
            log.error("스캔 사이클 오류: %s", e)
        _write_dashboard(settings, scanner, refresh_sec=refresh)
        time.sleep(refresh)


if __name__ == "__main__":
    main()
