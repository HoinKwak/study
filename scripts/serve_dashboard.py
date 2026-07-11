"""로컬 대시보드 웹서버 — 브라우저에서 실시간으로 보기.

    python -m scripts.serve_dashboard              # http://localhost:8787
    python -m scripts.serve_dashboard --port 9000

state/dashboard.html 을 서빙한다. 스캐너(run_scanner)가 이 파일을 매 사이클
갱신하므로, 페이지의 자동 새로고침으로 최신 이벤트가 계속 반영된다.
스캐너가 안 돌고 있으면 매 요청 시 거래 저널 + 저장된 이벤트로 즉석 렌더링한다.
"""
from __future__ import annotations

import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.monitoring import TradeJournal  # noqa: E402
from crypto_trader.monitoring.dashboard import (  # noqa: E402
    btc_buyhold_series, journal_span_days, load_start_equity, render_html)
from crypto_trader.scanner import EventStore  # noqa: E402


def _render(settings, refresh_sec: int) -> bytes:
    journal = TradeJournal(settings.state_dir)
    events = EventStore.load(settings.state_dir).recent(40)
    start_eq = load_start_equity(settings.state_dir)
    btc = btc_buyhold_series(journal_span_days(journal))
    return render_html(journal, equity=None, events=events, refresh_sec=refresh_sec,
                       start_equity=start_eq, btc_series=btc).encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="대시보드 로컬 웹서버")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--refresh", type=int, default=30, help="페이지 자동 새로고침(초)")
    args = parser.parse_args()

    settings = get_settings()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            if self.path not in ("/", "/index.html", "/dashboard.html"):
                self.send_response(404)
                self.end_headers()
                return
            body = _render(settings, args.refresh)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_a):  # 접속 로그 소음 억제
            pass

    server = HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"대시보드: http://localhost:{args.port}  (Ctrl+C 종료)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버 종료")
        server.server_close()


if __name__ == "__main__":
    main()
