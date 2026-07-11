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
STOOQ = "https://stooq.com/q/d/l/"
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/"
COINGECKO_MARKETS = "https://api.coingecko.com/api/v3/coins/markets"

# 캐시 스키마 버전 — 데이터 구조/소스가 바뀌면 올려 옛 캐시를 무효화
_CACHE_VERSION = 2

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

    def rel(a, b):
        return round(a - b, 1) if (a is not None and b is not None) else None

    out: list[dict] = []
    for x in rows:
        sym = str(x.get("symbol", "")).lower()
        if sym in STABLE_LIKE or sym == "btc":
            continue
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

def _fetch_yahoo(symbol: str, days: int, timeout: int = 15
                 ) -> list[tuple[float, float]] | None:
    """Yahoo Finance 차트 API → 최근 days 일 (epoch초, 종가). 실패 시 None."""
    try:
        r = requests.get(f"{YAHOO}{symbol}", params={"range": "6mo", "interval": "1d"},
                         headers=_UA, timeout=timeout)
        r.raise_for_status()
        res = (r.json().get("chart", {}).get("result") or [None])[0]
        ts = res["timestamp"]
        closes = res["indicators"]["quote"][0]["close"]
    except (requests.RequestException, KeyError, TypeError, IndexError, ValueError) as e:
        log.info("yahoo %s 조회 실패: %s", symbol, str(e)[:60])
        return None
    pts = [(float(t), float(c)) for t, c in zip(ts, closes) if c is not None]
    return pts[-days:] if pts else None


def _fetch_stooq(symbol: str, days: int, timeout: int = 15
                 ) -> list[tuple[float, float]] | None:
    """stooq 일별 CSV → 최근 days 일 (epoch초, 종가). 실패 시 None."""
    try:
        r = requests.get(STOOQ, params={"s": symbol, "i": "d"}, headers=_UA, timeout=timeout)
        r.raise_for_status()
        lines = r.text.strip().splitlines()
    except requests.RequestException as e:
        log.info("stooq %s 조회 실패: %s", symbol, str(e)[:60])
        return None
    if len(lines) < 3 or not lines[0].lower().startswith("date"):
        return None
    pts: list[tuple[float, float]] = []
    for ln in lines[1:]:
        parts = ln.split(",")
        if len(parts) < 5:
            continue
        try:
            dt = datetime.strptime(parts[0], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            pts.append((dt.timestamp(), float(parts[4])))
        except (ValueError, IndexError):
            continue
    return pts[-days:] if pts else None


def _normalize(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if not pts or pts[0][1] <= 0:
        return []
    base = pts[0][1]
    return [(t, (c / base - 1.0) * 100.0) for t, c in pts]


def macro_divergence(days: int = 90,
                     data: BinanceDerivativesData | None = None) -> list[dict]:
    """BTC/나스닥/금 정규화(%) 시계열 — line_chart 용 series 리스트."""
    data = data or BinanceDerivativesData()
    series: list[dict] = []

    btc = data.klines("BTC/USDT", "1d", limit=min(days + 1, 200))
    if btc and btc.get("close"):
        norm = _normalize(list(zip((t / 1000.0 for t in btc["open_time"]), btc["close"])))
        if norm:
            series.append({"label": "BTC", "color": "#f7931a", "points": norm})

    # Yahoo 우선(^IXIC 나스닥종합, GC=F 금선물) → 실패 시 stooq 폴백
    for yh, sq, label, color in (
        ("%5EIXIC", "^ndq", "나스닥", "#38bdf8"),
        ("GC=F", "xauusd", "금", "#eab308"),
    ):
        raw = _fetch_yahoo(yh, days) or _fetch_stooq(sq, days)
        norm = _normalize(raw) if raw else []
        if norm:
            series.append({"label": label, "color": color, "points": norm})
        else:
            log.info("매크로 %s 데이터 없음(yahoo·stooq 모두 실패)", label)
    return series


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
