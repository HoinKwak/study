"""로컬 대시보드 웹서버 — 브라우저에서 실시간으로 보기.

    python -m scripts.serve_dashboard              # http://localhost:8787
    python -m scripts.serve_dashboard --port 9000

state/dashboard.html 을 서빙한다. 스캐너(run_scanner)가 이 파일을 매 사이클
갱신하므로, 페이지의 자동 새로고침으로 최신 이벤트가 계속 반영된다.
스캐너가 안 돌고 있으면 매 요청 시 거래 저널 + 저장된 이벤트로 즉석 렌더링한다.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.monitoring import TradeJournal  # noqa: E402
from crypto_trader.monitoring.dashboard import (  # noqa: E402
    btc_buyhold_series, journal_span_days, load_equity, load_start_equity, render_html)
from crypto_trader.monitoring.market_extra import load_cached, load_tickers  # noqa: E402
from crypto_trader.scanner import EventStore  # noqa: E402


def _render(settings, refresh_sec: int) -> bytes:
    journal = TradeJournal(settings.state_dir)
    events = EventStore.load(settings.state_dir).recent(40)
    start_eq = load_start_equity(settings.state_dir)
    btc = btc_buyhold_series(journal_span_days(journal))
    extra = load_cached(settings.state_dir, settings.scanner_min_volume)
    tickers = load_tickers(settings.state_dir)
    return render_html(journal, equity=load_equity(settings.state_dir), events=events, refresh_sec=refresh_sec,
                       start_equity=start_eq, btc_series=btc,
                       market_extra=extra, tickers=tickers).encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="대시보드 로컬 웹서버")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--refresh", type=int, default=30, help="페이지 자동 새로고침(초)")
    args = parser.parse_args()

    settings = get_settings()

    def _tf_params(tf: str):
        """타임프레임 → (interval, limit)."""
        table = {
            "1d": ("15m", 96), "7d": ("1h", 168), "30d": ("4h", 180),
            "6m": ("1d", 180), "1y": ("1d", 365),
        }
        if tf == "ytd":
            now = datetime.now(timezone.utc)
            jan1 = datetime(now.year, 1, 1, tzinfo=timezone.utc)
            return ("1d", max(2, min(366, (now - jan1).days + 1)))
        return table.get(tf, ("1h", 168))

    def _api_klines(qs) -> bytes:
        from crypto_trader.connectors import BinanceDerivativesData
        symbol = (qs.get("symbol", ["BTC"])[0] or "BTC").upper()
        tf = qs.get("tf", ["7d"])[0]
        interval, limit = _tf_params(tf)
        try:
            kl = BinanceDerivativesData().klines(f"{symbol}/USDT", interval, limit)
            points = [[int(kl["open_time"][i]), kl["open"][i], kl["high"][i],
                       kl["low"][i], kl["close"][i]]
                      for i in range(len(kl["close"]))] if kl else []
        except Exception:  # noqa: BLE001
            points = []
        return json.dumps({"symbol": symbol, "tf": tf, "points": points}).encode("utf-8")

    _DERIV_PERIODS = {"5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"}

    def _api_derivs(qs) -> bytes:
        """선택 티커의 파생 지표 스냅샷 — 펀딩비/OI/롱숏/테이커/24h. period 로 기간 선택."""
        from crypto_trader.connectors import BinanceDerivativesData
        symbol = (qs.get("symbol", ["BTC"])[0] or "BTC").upper()
        period = qs.get("period", ["1h"])[0]
        if period not in _DERIV_PERIODS:
            period = "1h"
        d = BinanceDerivativesData()
        pair = f"{symbol}/USDT"
        out = {"symbol": symbol, "period": period}
        try:
            out.update(d.snapshot(pair, period))
        except Exception:  # noqa: BLE001
            pass
        try:
            oi = d.open_interest_hist(pair, period, 2)
            out["oi_base"] = oi[-1] if oi else None
        except Exception:  # noqa: BLE001
            out["oi_base"] = None
        try:
            tk = d.all_24h_tickers() or {}
            row = tk.get(f"{symbol}USDT")
            if row:
                out["price"] = float(row.get("lastPrice"))
                out["vol24"] = float(row.get("quoteVolume"))
                out["chg24"] = float(row.get("priceChangePercent"))
        except Exception:  # noqa: BLE001
            pass
        if out.get("oi_base") and out.get("price"):
            out["oi_notional"] = out["oi_base"] * out["price"]
        return json.dumps(out).encode("utf-8")

    def _api_symbols() -> bytes:
        try:
            from crypto_trader.monitoring.market_extra import binance_futures_list
            syms = [f["symbol"] for f in binance_futures_list()]
        except Exception:  # noqa: BLE001
            syms = []
        return json.dumps(syms).encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def _send(self, body: bytes, ctype: str) -> None:
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path
            if path == "/api/klines":
                self._send(_api_klines(parse_qs(parsed.query)), "application/json")
                return
            if path == "/api/derivs":
                self._send(_api_derivs(parse_qs(parsed.query)), "application/json")
                return
            if path == "/api/symbols":
                self._send(_api_symbols(), "application/json")
                return
            if path in ("/", "/index.html", "/dashboard.html"):
                self._send(_render(settings, args.refresh), "text/html; charset=utf-8")
                return
            self.send_response(404)
            self.end_headers()

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
