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
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
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
_FG_CACHE = {"t": 0.0, "data": None}   # 공포·탐욕 지수 캐시(30분)
_MACRO_CACHE: dict[str, dict] = {}     # 매크로 묶음 기간별 캐시(period → {t, data})
_LEADERBOARD_CACHE: dict[str, dict] = {}   # 리더보드 소스별 캐시(source → {t,data}, 10분)
_LB_REFRESHING: set = set()                # 현재 백그라운드 갱신 중인 소스(중복 갱신 방지)


def _refresh_leaderboard(source: str) -> None:
    """백그라운드에서 리더보드 번들 갱신 — 무거운 build_bundle을 요청 스레드 밖에서 돌린다."""
    try:
        if source == "binance":
            from crypto_trader.connectors.binance_leaderboard import build_bundle
        else:
            from crypto_trader.connectors.hyperliquid_leaderboard import build_bundle
        out = build_bundle()
        _LEADERBOARD_CACHE[source] = {"t": time.time(), "data": out}
    except Exception:  # noqa: BLE001
        pass
    finally:
        _LB_REFRESHING.discard(source)
_BTCD_CACHE = {"t": 0.0, "val": None}      # BTC 도미넌스 현재값 캐시(5분)


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
        """봉 기준 타임프레임 → (interval, 표시봉수). tf 자체가 캔들 간격.

        표시봉수는 '줌아웃 시 볼 수 있는 최대 이력'. 차트는 기본으로 최근 일부만
        보여주고(클라이언트 DEF_SHOWN), 휠로 축소하면 이 범위까지 펼쳐진다.
        warmup(210) + 표시봉 ≤ 1500(fapi 1회 최대)이어야 하므로 상한은 ~1290.
        """
        table = {
            "15m": ("15m", 960), "1h": ("1h", 1000), "4h": ("4h", 900),
            "1d": ("1d", 700), "1w": ("1w", 400), "1M": ("1M", 200),
        }
        return table.get(tf, ("1h", 1000))

    def _api_klines(qs) -> bytes:
        from crypto_trader.connectors import BinanceDerivativesData
        symbol = (qs.get("symbol", ["BTC"])[0] or "BTC").upper()
        tf = qs.get("tf", ["7d"])[0]
        interval, limit = _tf_params(tf)
        # 지표(MA200 등) 계산용 워밍업 봉을 앞에 더 받고, 차트는 표시구간(limit)만 그린다.
        warmup_bars = 210
        try:
            kl = BinanceDerivativesData().klines(f"{symbol}/USDT", interval, limit + warmup_bars)
            points = [[int(kl["open_time"][i]), kl["open"][i], kl["high"][i],
                       kl["low"][i], kl["close"][i], kl["volume"][i]]
                      for i in range(len(kl["close"]))] if kl else []
        except Exception:  # noqa: BLE001
            points = []
        warmup = max(0, len(points) - limit)  # 표시는 마지막 limit 봉, 앞 warmup 봉은 지표계산 전용
        return json.dumps({"symbol": symbol, "tf": tf, "points": points,
                           "warmup": warmup}).encode("utf-8")

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

    def _api_feargreed() -> bytes:
        """크립토 공포·탐욕 지수(alternative.me, 시장 전체) — 30분 캐시."""
        now = time.time()
        if _FG_CACHE["data"] is not None and now - _FG_CACHE["t"] < 1800:
            return json.dumps(_FG_CACHE["data"]).encode("utf-8")
        out = {"value": None, "label": ""}
        try:
            import requests
            d = requests.get("https://api.alternative.me/fng/", timeout=8).json()
            row = (d.get("data") or [{}])[0]
            out = {"value": int(row.get("value")), "label": row.get("value_classification", "")}
            _FG_CACHE["t"] = now
            _FG_CACHE["data"] = out
        except Exception:  # noqa: BLE001
            pass
        return json.dumps(out).encode("utf-8")

    def _api_btc_dominance() -> bytes:
        """BTC 도미넌스(%) 일별 — research/btcd 백필(1년, committed) + 라이브 일별 누적 병합.

        과거 BTC.D = BTC시총 ÷ 전체시총. 전체시총 과거는 사장님 CSV(research/btcd/total_mcap_daily.csv),
        BTC시총은 CoinGecko 무료(365일). 그 곱으로 만든 백필을 씨앗으로, 이후 /global 현재값을 일별 append.
        """
        from pathlib import Path as _P

        from crypto_trader.config import get_settings
        now = time.time()
        base_path = _REPO_DIR / "research" / "btcd" / "btc_dominance_daily.json"
        live_path = _P(get_settings().state_dir) / "btc_dominance_live.json"
        try:
            base = json.loads(base_path.read_text()) if base_path.exists() else []
        except Exception:  # noqa: BLE001
            base = []
        try:
            live = json.loads(live_path.read_text()) if live_path.exists() else []
        except Exception:  # noqa: BLE001
            live = []
        # 현재값(5분 캐시)
        if _BTCD_CACHE["val"] is None or now - _BTCD_CACHE["t"] >= 300:
            try:
                import requests
                d = requests.get("https://api.coingecko.com/api/v3/global", timeout=8).json()
                _BTCD_CACHE["val"] = float(d["data"]["market_cap_percentage"]["btc"])
                _BTCD_CACHE["t"] = now
            except Exception:  # noqa: BLE001
                pass
        dom = _BTCD_CACHE["val"]
        # 백필+라이브 병합(일 기준 dedup)
        merged: dict[int, float] = {}
        for t, v in base + live:
            merged[(int(t) // 86_400_000) * 86_400_000] = v
        # 오늘 라이브 append(마지막 샘플이 ~20h보다 오래됐을 때만)
        ts_ms = int(now * 1000)
        if dom is not None and (not merged or ts_ms - max(merged) >= 72_000_000):
            day = (ts_ms // 86_400_000) * 86_400_000
            merged[day] = round(dom, 3)
            live.append([day, round(dom, 3)])
            live = live[-400:]
            try:
                live_path.parent.mkdir(parents=True, exist_ok=True)
                live_path.write_text(json.dumps(live))
            except Exception:  # noqa: BLE001
                pass
        points = sorted([t, v] for t, v in merged.items())
        return json.dumps({"current": dom, "points": points[-400:]}).encode("utf-8")

    def _api_macro(qs) -> bytes:
        """BTC vs 증시·원자재 매크로 묶음(정규화 괴리 + 카드) — 기간별 10분 캐시."""
        period = (qs.get("period", ["6mo"])[0] or "6mo")
        now = time.time()
        c = _MACRO_CACHE.get(period)
        if c and now - c["t"] < 600:
            return json.dumps(c["data"]).encode("utf-8")
        out = {"period": period, "divergence": [], "cards": []}
        try:
            from crypto_trader.monitoring.market_extra import macro_bundle
            out = macro_bundle(period)
            _MACRO_CACHE[period] = {"t": now, "data": out}
        except Exception:  # noqa: BLE001
            pass
        return json.dumps(out).encode("utf-8")

    def _api_leaderboard(qs) -> bytes:
        """리더보드 — 캐시를 즉시 반환하고, 만료/부재 시 백그라운드로 갱신(요청을 안 막음).

        build_bundle이 무겁다(후보 수십명 순차 API 검증 ~수 분). 동기로 돌리면 최초 로드가 몇 분
        걸려 탭이 멈춘 것처럼 보인다. → 신선하면 그대로, 오래됐으면 stale값을 즉시 주면서 백그라운드
        갱신만 트리거. 바이낸스는 로컬 전용(개발환경은 지역차단으로 빈 결과).
        """
        source = (qs.get("source", ["hyperliquid"])[0] or "hyperliquid").lower()
        now = time.time()
        c = _LEADERBOARD_CACHE.get(source)
        fresh = bool(c and now - c["t"] < 600)
        if not fresh and source not in _LB_REFRESHING:
            _LB_REFRESHING.add(source)
            threading.Thread(target=_refresh_leaderboard, args=(source,), daemon=True).start()
        if c:
            return json.dumps({**c["data"], "stale": not fresh}).encode("utf-8")
        # 최초(캐시 없음): 백그라운드 로딩 중 — 빈 결과 + loading 플래그(프런트가 재폴링)
        return json.dumps({"source": source, "count": 0, "traders": [], "top": [],
                           "rising": [], "loading": True}).encode("utf-8")

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
            if path == "/api/btc_dominance":
                self._send(_api_btc_dominance(), "application/json")
                return
            if path == "/api/prices":
                self._send(_api_prices(parse_qs(parsed.query)), "application/json")
                return
            if path == "/api/symbols":
                self._send(_api_symbols(), "application/json")
                return
            if path == "/api/feargreed":
                self._send(_api_feargreed(), "application/json")
                return
            if path == "/api/macro":
                self._send(_api_macro(parse_qs(parsed.query)), "application/json")
                return
            if path == "/api/leaderboard":
                self._send(_api_leaderboard(parse_qs(parsed.query)), "application/json")
                return
            self.send_response(404)
            self.end_headers()

        def log_message(self, *_a):  # 접속 로그 소음 억제
            pass

    if args.pull_interval > 0:
        threading.Thread(target=_autopull_loop, args=(args.pull_interval,),
                         daemon=True).start()
        print(f"리서치 자동갱신: {args.pull_interval}초마다 git pull (--pull-interval 0 이면 끔)")

    # 스레딩 서버: 느린 요청(리더보드 build_bundle 등)이 사이트 전체를 멈추지 않게 한다.
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    # 리더보드 프리워밍: 서버 시작 즉시 백그라운드로 번들을 미리 채워 첫 방문도 빠르게.
    _LB_REFRESHING.add("hyperliquid")
    threading.Thread(target=_refresh_leaderboard, args=("hyperliquid",), daemon=True).start()
    print(f"대시보드: http://localhost:{args.port}  (Ctrl+C 종료)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버 종료")
        server.server_close()


if __name__ == "__main__":
    main()
