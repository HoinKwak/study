"""대시보드 부가 시장데이터 — 알트 상대강도, 시총 TOP10 BTC대비, 매크로 괴리.

무거운/외부 네트워크 조회이므로 state/market_extra.json 에 캐시(기본 30분 TTL)한다.
각 구성요소는 독립적으로 계산돼 하나가 실패해도 나머지는 표시된다.
- 알트 상대강도: 고유동성 USDT 페어의 1/7/30일 수익률 − BTC 수익률. 각 구간 TOP N.
- 시총 TOP10: 코인게코 시총 상위 코인(스테이블·BTC 제외)의 1/7/30일 BTC대비 수익률.
- 매크로 괴리: BTC/나스닥/금 일별 종가 정규화(시작=0%). 나스닥·금은 Yahoo(→stooq 폴백).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from ..connectors import BinanceDerivativesData, high_volume_usdt_symbols
from ..connectors.universe import NON_CRYPTO_BASES, STABLE_BASES
from ..utils import get_logger

log = get_logger("market_extra")

_UA = {"User-Agent": "Mozilla/5.0"}
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/"
COINGECKO_MARKETS = "https://api.coingecko.com/api/v3/coins/markets"

# 매크로 기간 → (Yahoo range, interval, 유지일수). 3·5·10년은 넉넉한 range로 받아 clip.
_MACRO_PERIODS: dict[str, tuple[str, str, int]] = {
    "1d":  ("1d",  "5m",   1),
    "1w":  ("5d",  "30m",  7),
    "1mo": ("1mo", "1d",   31),
    "3mo": ("3mo", "1d",   93),
    "6mo": ("6mo", "1d",   186),
    "1y":  ("1y",  "1d",   366),
    "3y":  ("5y",  "1wk",  1096),
    "5y":  ("5y",  "1wk",  1827),
    "10y": ("10y", "1wk",  3653),
}
# BTC vs 나스닥·금 괴리 라인(정규화 %). (label, color, Yahoo symbol)
# 증시는 현물지수(^IXIC 등) 대신 선물(NQ=F 등)을 쓴다 — 현물지수는 정규장 6.5h만
# 산출돼 야간·주말 공백이 크지만, 지수선물은 CME에서 ~23h(주중 1h 정비휴장·주말만
# 휴장) 거래돼 BTC·금(GC=F 선물)처럼 거의 연속. 소스 불일치로 나스닥만 끊기던 문제 해결.
_DIV_SYMS: list[tuple[str, str, str]] = [
    ("BTC",   "#f7931a", "BTC-USD"),
    ("나스닥", "#38bdf8", "NQ=F"),
    ("금",     "#eab308", "GC=F"),
]
# 우측 카드: 주요 증시 + 원자재. (label, Yahoo symbol, color)
# 나스닥·S&P·니케이는 선물(NQ·ES·NKD)로 연속 커버, 코스피·FTSE는 Yahoo 선물 부재로
# 현물지수 유지(야간·주말 공백은 세션 끊김으로 표시), 원자재는 이미 선물.
_MACRO_MARKETS: list[tuple[str, str, str]] = [
    ("나스닥",  "NQ=F",  "#38bdf8"),
    ("S&P500", "ES=F",  "#22c55e"),
    ("코스피",  "^KS11", "#e879f9"),
    ("니케이",  "NKD=F", "#f97316"),
    ("FTSE",   "^FTSE", "#94a3b8"),
    ("금",      "GC=F",  "#eab308"),
    ("은",      "SI=F",  "#cbd5e1"),
    ("WTI유",   "CL=F",  "#a3a3a3"),
]

# 캐시 스키마 버전 — 데이터 구조/소스가 바뀌면 올려 옛 캐시를 무효화
_CACHE_VERSION = 4

# 시총 상위에 섞여있는 스테이블/랩드 제외용
STABLE_LIKE = {
    "usdt", "usdc", "dai", "fdusd", "tusd", "busd", "usde", "usds", "pyusd",
    "usd1", "usdd", "gusd", "wbtc", "weth", "wbeth", "steth", "wsteth", "cbbtc",
    "lbtc", "susds", "buidl", "bsc-usd",
}


def _now() -> float:
    return datetime.now(timezone.utc).timestamp()


# ------------------------------------------------------------- 알트 상대강도

def _ret(closes: list[float], back: int) -> float | None:
    if len(closes) < back + 1 or closes[-1 - back] <= 0:
        return None
    return (closes[-1] / closes[-1 - back] - 1.0) * 100.0


def alt_strength(min_volume: float, top_n: int = 10, max_symbols: int = 45,
                 data: BinanceDerivativesData | None = None) -> dict:
    """1/7/30일 BTC 대비 상대강도 TOP N. {'1d':[{symbol,alt,btc,rel}], ...}."""
    data = data or BinanceDerivativesData()
    pairs = high_volume_usdt_symbols(min_volume)
    symbols = [s for s, _v in pairs][:max_symbols]

    btc = data.klines("BTC/USDT", "1d", limit=32)
    btc_closes = btc["close"] if btc else []
    btc_ret = {w: _ret(btc_closes, w) for w in (1, 7, 30)}

    rows: dict[int, list[dict]] = {1: [], 7: [], 30: []}
    for sym in symbols:
        if sym == "BTC/USDT":
            continue
        kl = data.klines(sym, "1d", limit=32)
        if not kl or not kl.get("close"):
            continue
        closes = kl["close"]
        for w in (1, 7, 30):
            a = _ret(closes, w)
            b = btc_ret.get(w)
            if a is None or b is None:
                continue
            rows[w].append({"symbol": sym, "alt": round(a, 2),
                            "btc": round(b, 2), "rel": round(a - b, 2)})
    out = {}
    for w, key in ((1, "1d"), (7, "7d"), (30, "30d")):
        out[key] = sorted(rows[w], key=lambda r: -r["rel"])[:top_n]
    return out


# ---------------------------------------------------- 시총 TOP10 (BTC 대비)

def mcap_top_relative(top_n: int = 10, timeout: int = 20) -> list[dict]:
    """코인게코 시총 상위 코인(스테이블·BTC 제외)의 1/7/30일 BTC대비 수익률."""
    r = requests.get(COINGECKO_MARKETS, params={
        "vs_currency": "usd", "order": "market_cap_desc", "per_page": 30,
        "page": 1, "price_change_percentage": "24h,7d,30d",
    }, headers=_UA, timeout=timeout)
    r.raise_for_status()
    rows = r.json()
    if not isinstance(rows, list):
        return []
    btc = next((x for x in rows if str(x.get("symbol", "")).lower() == "btc"), None)
    if not btc:
        return []
    b1 = btc.get("price_change_percentage_24h_in_currency")
    b7 = btc.get("price_change_percentage_7d_in_currency")
    b30 = btc.get("price_change_percentage_30d_in_currency")

    # 바이낸스 상장 코인만 남겨 잡토큰(FIGR_HELOC/RAIN/LEO 등) 제외
    try:
        tk = BinanceDerivativesData().all_24h_tickers() or {}
    except Exception:  # noqa: BLE001
        tk = {}

    def rel(a, b):
        return round(a - b, 1) if (a is not None and b is not None) else None

    out: list[dict] = []
    for x in rows:
        sym = str(x.get("symbol", "")).lower()
        if sym in STABLE_LIKE or sym == "btc" or "_" in sym:
            continue
        if tk and f"{sym.upper()}USDT" not in tk:
            continue  # 바이낸스 미상장 제외
        out.append({
            "symbol": sym.upper(),
            "r1": rel(x.get("price_change_percentage_24h_in_currency"), b1),
            "r7": rel(x.get("price_change_percentage_7d_in_currency"), b7),
            "r30": rel(x.get("price_change_percentage_30d_in_currency"), b30),
        })
        if len(out) >= top_n:
            break
    return out


# ----------------------------------------------------------- BTC·나스닥·금 괴리

def _fetch_yahoo(symbol: str, range_: str = "6mo", interval: str = "1d",
                 timeout: int = 15) -> list[tuple[float, float]] | None:
    """Yahoo Finance 차트 API → (epoch초, 종가) 리스트. 실패 시 None.

    symbol 은 원형(^IXIC·GC=F·BTC-USD 등)으로 넘기면 URL 인코딩한다.
    """
    from urllib.parse import quote
    try:
        r = requests.get(f"{YAHOO}{quote(symbol)}",
                         params={"range": range_, "interval": interval},
                         headers=_UA, timeout=timeout)
        r.raise_for_status()
        res = (r.json().get("chart", {}).get("result") or [None])[0]
        ts = res["timestamp"]
        closes = res["indicators"]["quote"][0]["close"]
    except (requests.RequestException, KeyError, TypeError, IndexError, ValueError) as e:
        log.info("yahoo %s 조회 실패: %s", symbol, str(e)[:60])
        return None
    return [(float(t), float(c)) for t, c in zip(ts, closes) if c is not None] or None


def _period_of(days: int) -> str:
    """일수 → 매크로 기간 키(하위호환용 — 스캐너의 macro_days 매핑)."""
    for key, thr in (("1d", 1), ("1w", 7), ("1mo", 31), ("3mo", 93),
                     ("6mo", 186), ("1y", 366), ("3y", 1096), ("5y", 1827)):
        if days <= thr:
            return key
    return "10y"


def _fetch_period(symbol: str, period: str) -> list[tuple[float, float]]:
    """기간 키로 Yahoo 조회 후 유지일수만큼 clip. 실패 시 빈 리스트."""
    range_, interval, clip = _MACRO_PERIODS.get(period, _MACRO_PERIODS["6mo"])
    raw = _fetch_yahoo(symbol, range_, interval)
    if not raw:
        return []
    cut = _now() - clip * 86400
    return [p for p in raw if p[0] >= cut] or raw


def _align_normalize(raw: dict[str, list[tuple[float, float]]],
                     syms: list[tuple[str, str, str]]) -> list[dict]:
    """여러 시리즈를 공통 시작(각 첫 ts 중 최댓값)에서 잘라 0%부터 정규화 — 라인 시작점 일원화."""
    firsts = [pts[0][0] for _, _, s in syms for pts in [raw.get(s) or []] if pts]
    if not firsts:
        return []
    common = max(firsts)
    out: list[dict] = []
    for label, color, s in syms:
        pts = [p for p in (raw.get(s) or []) if p[0] >= common]
        norm = _normalize(pts)
        if norm:
            out.append({"label": label, "color": color, "points": norm})
    return out


def macro_bundle(period: str = "6mo") -> dict:
    """기간별 매크로 묶음 — {divergence: [정규화 라인], cards: [증시·원자재 카드]}.

    BTC·나스닥·금은 Yahoo 단일 소스로 정렬 정규화(시작=0%). 카드는 각 시장의
    가격 스파크라인 + 기간 등락률. serve_dashboard /api/macro 가 호출.
    """
    if period not in _MACRO_PERIODS:
        period = "6mo"
    syms = {s for _, _, s in _DIV_SYMS} | {s for _, s, _ in _MACRO_MARKETS}
    raw = {s: _fetch_period(s, period) for s in syms}
    div = _align_normalize(raw, _DIV_SYMS)
    cards: list[dict] = []
    for label, sym, color in _MACRO_MARKETS:
        pts = raw.get(sym) or []
        if len(pts) < 2:
            continue
        first, last = pts[0][1], pts[-1][1]
        pct = (last / first - 1.0) * 100.0 if first else None
        cards.append({
            "label": label, "symbol": sym, "color": color, "price": last, "pct": pct,
            "points": [[round(t), round(c, 4)] for t, c in pts],
        })
    return {"period": period, "divergence": div, "cards": cards}


def macro_divergence(days: int = 90) -> list[dict]:
    """BTC/나스닥/금 정규화(%) 시계열 — 정적 렌더(스캐너 캐시)용. 시작점 정렬."""
    period = _period_of(days)
    raw = {s: _fetch_period(s, period) for _, _, s in _DIV_SYMS}
    return _align_normalize(raw, _DIV_SYMS)


def _normalize(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if not pts or pts[0][1] <= 0:
        return []
    base = pts[0][1]
    return [(t, (c / base - 1.0) * 100.0) for t, c in pts]


# ----------------------------------------------------- 상단 가격 티커/선택차트

def top_mcap_symbols(n: int = 12, timeout: int = 20) -> list[str]:
    """코인게코 시총 상위 n개 심볼(스테이블 제외, BTC/ETH 포함)."""
    r = requests.get(COINGECKO_MARKETS, params={
        "vs_currency": "usd", "order": "market_cap_desc", "per_page": 40, "page": 1,
    }, headers=_UA, timeout=timeout)
    r.raise_for_status()
    out: list[str] = []
    for x in r.json():
        sym = str(x.get("symbol", "")).lower()
        if sym in STABLE_LIKE or not sym:
            continue
        out.append(sym.upper())
        if len(out) >= n:
            break
    return out


def top_tickers(symbols: list, data: BinanceDerivativesData | None = None,
                tickers24: dict | None = None, kl_limit: int = 48) -> list[dict]:
    """각 심볼 현재가·24h변동·최근 시세(스파크라인용)."""
    data = data or BinanceDerivativesData()
    tk = tickers24 if tickers24 is not None else (data.all_24h_tickers() or {})
    out: list[dict] = []
    for base in symbols:
        t = tk.get(f"{base}USDT") or {}
        try:
            price = float(t.get("lastPrice")) or None
        except (TypeError, ValueError):
            price = None
        try:
            pct = float(t.get("priceChangePercent"))
        except (TypeError, ValueError):
            pct = None
        kl = data.klines(f"{base}/USDT", "1h", limit=kl_limit)
        closes = kl["close"] if kl else []
        times = [x / 1000.0 for x in kl["open_time"]] if kl else []
        out.append({"symbol": base, "price": price, "pct": pct,
                    "closes": closes, "times": times})
    return out


def binance_futures_list(data: BinanceDerivativesData | None = None,
                         tickers24: dict | None = None) -> list[dict]:
    """바이낸스 선물(USDT-M) 상장 코인 리스트 — 거래대금 내림차순. 스테이블/비크립토 제외."""
    data = data or BinanceDerivativesData()
    tk = tickers24 if tickers24 is not None else (data.all_24h_tickers() or {})
    out: list[dict] = []
    for pair, t in tk.items():
        if not pair.endswith("USDT"):
            continue
        base = pair[:-4]
        if not base or base in STABLE_BASES or base in NON_CRYPTO_BASES:
            continue
        try:
            price = float(t.get("lastPrice")) or None
            pct = float(t.get("priceChangePercent"))
            qv = float(t.get("quoteVolume") or 0.0)
        except (TypeError, ValueError):
            continue
        out.append({"symbol": base, "price": price, "pct": pct, "vol": qv})
    out.sort(key=lambda x: -x["vol"])
    return out


_FALLBACK_SYMS = ["BTC", "ETH", "BNB", "XRP", "SOL", "DOGE", "ADA", "TRX",
                  "LINK", "AVAX", "SUI", "DOT"]


def load_tickers(state_dir: str, ttl_sec: int = 60, want: int = 24) -> dict:
    """바이낸스 상장 + 시총 상위 코인의 시세(차트용)를 60초 캐시. {'top':[...]}.

    좌측 4×3 미니차트(상위 12) + 우측 선택 큰차트(검색)용. RWA/미상장 잡토큰
    (예: FIGR_HELOC), 언더스코어 심볼, 스테이블/비크립토는 제외.
    """
    path = Path(state_dir) / "top_tickers.json"
    if path.exists():
        try:
            c = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(c.get("data"), dict) and _now() - float(c.get("ts", 0)) < ttl_sec:
                return c["data"]
        except (json.JSONDecodeError, ValueError, OSError):
            pass
    try:
        data = BinanceDerivativesData()
        tk = data.all_24h_tickers() or {}
        try:
            mcaps = top_mcap_symbols(50)
        except Exception:  # noqa: BLE001
            mcaps = []
        cands = [s for s in (mcaps or _FALLBACK_SYMS)
                 if "_" not in s and s not in STABLE_BASES and s not in NON_CRYPTO_BASES
                 and (not tk or f"{s}USDT" in tk)][:want + 8]
        top = [t for t in top_tickers(cands, data, tk, kl_limit=168) if t.get("closes")][:want]
        result = {"top": top}
    except Exception as e:  # noqa: BLE001
        log.warning("load_tickers 실패: %s", e)
        return {}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"ts": _now(), "data": result}, ensure_ascii=False),
                        encoding="utf-8")
    except OSError:
        pass
    return result


# --------------------------------------------------------------- 캐시 래퍼

def load_cached(state_dir: str, min_volume: float, ttl_min: int = 30,
                macro_days: int = 90) -> dict:
    """계산 결과를 state/market_extra.json 에 캐시. 각 요소 독립 계산(부분 실패 허용)."""
    path = Path(state_dir) / "market_extra.json"
    if path.exists():
        try:
            cached = json.loads(path.read_text(encoding="utf-8"))
            if (cached.get("v") == _CACHE_VERSION
                    and _now() - float(cached.get("ts", 0)) < ttl_min * 60):
                return cached.get("data", {})
        except (json.JSONDecodeError, ValueError, OSError):
            pass

    data: dict = {}
    for key, fn in (
        ("alt_strength", lambda: alt_strength(min_volume)),
        ("mcap_top", lambda: mcap_top_relative()),
        ("macro", lambda: macro_divergence(macro_days)),
    ):
        try:
            data[key] = fn()
        except Exception as e:  # noqa: BLE001 — 부분 실패가 대시보드를 막지 않게
            log.warning("market_extra[%s] 실패: %s", key, str(e)[:80])
            data[key] = [] if key != "alt_strength" else {}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"v": _CACHE_VERSION, "ts": _now(), "data": data},
                       ensure_ascii=False),
            encoding="utf-8")
    except OSError:
        pass
    return data
