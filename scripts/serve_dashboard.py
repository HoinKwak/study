"""로컬 대시보드 웹서버 — 브라우저에서 실시간으로 보기.

    python -m scripts.serve_dashboard              # http://localhost:8787
    python -m scripts.serve_dashboard --port 9000

state/dashboard.html 을 서빙한다. 스캐너(run_scanner)가 이 파일을 매 사이클
갱신하므로, 페이지의 자동 새로고침으로 최신 이벤트가 계속 반영된다.
스캐너가 안 돌고 있으면 매 요청 시 거래 저널 + 저장된 이벤트로 즉석 렌더링한다.

리서치 파일(KOL 워치·시장 브리핑·차티스트·ETF)은 정기 루틴이 원격 브랜치에 push 하므로,
이 서버가 백그라운드에서 주기적으로 `git pull` 해 로컬 파일을 최신으로 유지한다
(`--pull-interval` 초, 0이면 비활성). 대시보드 창만 켜두면 리서치가 자동 갱신된다.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.monitoring import TradeJournal  # noqa: E402
from crypto_trader.monitoring.dashboard import (  # noqa: E402
    btc_buyhold_series, journal_span_days, load_equity, load_equity_history,
    load_start_equity, render_html)
from crypto_trader.monitoring.market_extra import load_cached, load_tickers  # noqa: E402
from crypto_trader.scanner import EventStore  # noqa: E402

_REPO_DIR = Path(__file__).resolve().parent.parent


def _autopull_loop(interval: int) -> None:
    """주기적으로 `git pull --ff-only` 해서 리서치 파일을 최신으로 유지(데몬 스레드).

    정기 루틴이 원격 브랜치에 push 한 리서치 갱신을 로컬 대시보드가 자동 반영하게 한다.
    ff-only 라 로컬 커밋이 없으면 항상 안전(충돌 시 병합 안 하고 조용히 넘어감).
    """
    while True:
        time.sleep(interval)
        try:
            r = subprocess.run(["git", "pull", "--ff-only"], cwd=str(_REPO_DIR),
                               capture_output=True, text=True, timeout=60)
            out = (r.stdout or "").strip()
            if r.returncode == 0 and out and "Already up to date" not in out:
                print(f"[autopull] 리서치 갱신 반영됨 — 새로고침 시 최신 표시")
            elif r.returncode != 0:
                # 네트워크·비-ff 등은 무해하게 무시(다음 주기 재시도). 소음 억제로 짧게만.
                err = (r.stderr or "").strip().splitlines()
                print(f"[autopull] pull 실패(무시): {err[-1] if err else r.returncode}")
        except Exception as e:  # noqa: BLE001
            print(f"[autopull] 예외(무시): {e}")



def _render(settings, refresh_sec: int) -> bytes:
    journal = TradeJournal(settings.state_dir)
    events = EventStore.load(settings.state_dir).recent(40)
    start_eq = load_start_equity(settings.state_dir)
    btc = btc_buyhold_series(journal_span_days(journal))
    extra = load_cached(settings.state_dir, settings.scanner_min_volume)
    tickers = load_tickers(settings.state_dir)
    return render_html(journal, equity=load_equity(settings.state_dir), events=events, refresh_sec=refresh_sec,
                       start_equity=start_eq, btc_series=btc,
                       market_extra=extra, tickers=tickers,
                       equity_history=load_equity_history(settings.state_dir)).encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="대시보드 로컬 웹서버")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--refresh", type=int, default=30, help="페이지 자동 새로고침(초)")
    parser.add_argument("--pull-interval", type=int, default=300,
                        help="리서치 자동 git pull 주기(초). 0이면 비활성")
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
                       kl["low"][i], kl["close"][i], kl["volume"][i]]
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

    def _api_oi_hist(qs) -> bytes:
        """OI 명목가치 시계열 — symbol·period(5m/1h/4h/1d). {points:[[ts,notional],...]}."""
        from crypto_trader.connectors import BinanceDerivativesData
        symbol = (qs.get("symbol", ["BTC"])[0] or "BTC").upper()
        period = qs.get("period", ["1h"])[0]
        if period not in _DERIV_PERIODS:
            period = "1h"
        try:
            s = BinanceDerivativesData().open_interest_value_series(f"{symbol}/USDT", period, 48) or []
        except Exception:  # noqa: BLE001
            s = []
        return json.dumps({"symbol": symbol, "period": period, "points": s}).encode("utf-8")

    def _api_cvd_hist(qs) -> bytes:
        """누적 CVD(테이커 매수−매도) 시계열 — symbol·period. {points:[[ts,cvd],...]}."""
        from crypto_trader.connectors import BinanceDerivativesData
        symbol = (qs.get("symbol", ["BTC"])[0] or "BTC").upper()
        period = qs.get("period", ["1h"])[0]
        if period not in _DERIV_PERIODS:
            period = "1h"
        try:
            raw = BinanceDerivativesData().taker_volume_series(f"{symbol}/USDT", period, 48) or []
        except Exception:  # noqa: BLE001
            raw = []
        pts = []
        cum = 0.0
        for row in raw:
            cum += (row[1] - row[2])
            pts.append([int(row[0]), cum])
        return json.dumps({"symbol": symbol, "period": period, "points": pts}).encode("utf-8")

    def _api_prices(qs) -> bytes:
        """열린 포지션 현재가 — symbols=BTC,ETH → {BTC: price, ...} (24h 티커의 lastPrice)."""
        from crypto_trader.connectors import BinanceDerivativesData
        raw = (qs.get("symbols", [""])[0] or "")
        syms = [s for s in raw.split(",") if s]
        out: dict[str, float] = {}
        try:
            tk = BinanceDerivativesData().all_24h_tickers() or {}
            for s in syms:
                base = s.split("/")[0].upper()
                row = tk.get(f"{base}USDT")
                if row:
                    out[base] = float(row.get("lastPrice"))
        except Exception:  # noqa: BLE001
            pass
        return json.dumps(out).encode("utf-8")

    def _api_symbols() -> bytes:
        try:
            from crypto_trader.monitoring.market_extra import binance_futures_list
            syms = [f["symbol"] for f in binance_futures_list()]
        except Exception:  # noqa: BLE001
            syms = []
        return json.dumps(syms).encode("utf-8")

    token = (settings.dashboard_token or "").strip()

    class Handler(BaseHTTPRequestHandler):
        def _authorized(self, qs) -> bool:
            """토큰 미설정 시 항상 허용(로컬 전용). 설정 시 ?key= 또는 쿠키 dtok 일치 요구."""
            if not token:
                return True
            if (qs.get("key", [""])[0] or "") == token:
                return True
            cookie = self.headers.get("Cookie", "") or ""
            return any(c.strip() == f"dtok={token}" for c in cookie.split(";"))

        def _deny(self) -> None:
            self.send_response(401)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("대시보드 접근에는 ?key=&lt;토큰&gt; 이 필요합니다.".encode("utf-8"))

        def _send(self, body: bytes, ctype: str) -> None:
            # 브라우저가 자동 새로고침 등으로 응답 도중 연결을 끊으면(WinError 10053 등)
            # 콘솔에 트레이스백이 찍힌다 — 무해하므로 조용히 무시.
            try:
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except (ConnectionError, BrokenPipeError):
                pass

        def do_GET(self):  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path
            qs = parse_qs(parsed.query)
            if not self._authorized(qs):
                self._deny()
                return
            if path in ("/", "/index.html", "/dashboard.html"):
                # 최초 ?key= 로 통과하면 쿠키를 심어 이후 API 호출(동일 출처)도 자동 인증.
                body = _render(settings, args.refresh)
                try:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    if token and qs.get("key", [""])[0] == token:
                        self.send_header("Set-Cookie", f"dtok={token}; Path=/; HttpOnly; SameSite=Lax")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                except (ConnectionError, BrokenPipeError):
                    pass
                return
            if path == "/api/klines":
                self._send(_api_klines(parse_qs(parsed.query)), "application/json")
                return
            if path == "/api/derivs":
                self._send(_api_derivs(parse_qs(parsed.query)), "application/json")
                return
            if path == "/api/oi_hist":
                self._send(_api_oi_hist(parse_qs(parsed.query)), "application/json")
                return
            if path == "/api/cvd_hist":
                self._send(_api_cvd_hist(parse_qs(parsed.query)), "application/json")
                return
            if path == "/api/prices":
                self._send(_api_prices(parse_qs(parsed.query)), "application/json")
                return
            if path == "/api/symbols":
                self._send(_api_symbols(), "application/json")
                return
            self.send_response(404)
            self.end_headers()

        def log_message(self, *_a):  # 접속 로그 소음 억제
            pass

    if args.pull_interval > 0:
        threading.Thread(target=_autopull_loop, args=(args.pull_interval,),
                         daemon=True).start()
        print(f"리서치 자동갱신: {args.pull_interval}초마다 git pull (--pull-interval 0 이면 끔)")

    server = HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"대시보드: http://localhost:{args.port}  (Ctrl+C 종료)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버 종료")
        server.server_close()


if __name__ == "__main__":
    main()
