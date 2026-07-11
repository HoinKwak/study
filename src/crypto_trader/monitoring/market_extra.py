"""대시보드 부가 시장데이터 — 알트 상대강도(vs BTC) + BTC·나스닥·금 괴리.

무거운 네트워크 조회이므로 state/market_extra.json 에 캐시(기본 30분 TTL)한다.
- 알트 상대강도: 고유동성 USDT 페어의 1일/7일/30일 수익률에서 BTC 수익률을 뺀 값
  (스테이블/비크립토는 유니버스에서 이미 제외). 각 구간 TOP N.
- 괴리 차트: BTC/나스닥/금 일별 종가를 시작=0% 로 정규화한 시계열.
  나스닥·금은 stooq(무료 CSV)에서. 조회 실패 시 해당 라인만 생략.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from ..connectors import BinanceDerivativesData, high_volume_usdt_symbols
from ..utils import get_logger

log = get_logger("market_extra")

STOOQ = "https://stooq.com/q/d/l/"


def _now() -> float:
    return datetime.now(timezone.utc).timestamp()


# ------------------------------------------------------------- 알트 상대강도

def _ret(closes: list[float], back: int) -> float | None:
    if len(closes) < back + 1 or closes[-1 - back] <= 0:
        return None
    return (closes[-1] / closes[-1 - back] - 1.0) * 100.0


def alt_strength(min_volume: float, top_n: int = 10, max_symbols: int = 45,
                 data: BinanceDerivativesData | None = None) -> dict:
    """1일/7일/30일 BTC 대비 상대강도 TOP N.

    반환: {'1d': [{symbol, alt, btc, rel}], '7d': [...], '30d': [...]}
    """
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
        ranked = sorted(rows[w], key=lambda r: -r["rel"])[:top_n]
        out[key] = ranked
    return out


# ----------------------------------------------------------- BTC·나스닥·금 괴리

def _fetch_stooq(symbol: str, days: int, timeout: int = 15
                 ) -> list[tuple[float, float]] | None:
    """stooq 일별 CSV → 최근 days 일 (epoch초, 종가). 실패 시 None."""
    try:
        r = requests.get(STOOQ, params={"s": symbol, "i": "d"},
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=timeout)
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
            close = float(parts[4])
        except (ValueError, IndexError):
            continue
        pts.append((dt.timestamp(), close))
    return pts[-days:] if pts else None


def _normalize(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """(epoch, 종가) → (epoch, 시작대비 %)."""
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
        pts = list(zip((t / 1000.0 for t in btc["open_time"]), btc["close"]))
        norm = _normalize(pts)
        if norm:
            series.append({"label": "BTC", "color": "#f7931a", "points": norm})

    for sym, label, color in (("^ndq", "나스닥", "#38bdf8"), ("xauusd", "금", "#eab308")):
        raw = _fetch_stooq(sym, days)
        norm = _normalize(raw) if raw else []
        if norm:
            series.append({"label": label, "color": color, "points": norm})
    return series


# --------------------------------------------------------------- 캐시 래퍼

def load_cached(state_dir: str, min_volume: float, ttl_min: int = 30,
                macro_days: int = 90) -> dict:
    """계산 결과를 state/market_extra.json 에 캐시. 신선하면 재사용."""
    path = Path(state_dir) / "market_extra.json"
    if path.exists():
        try:
            cached = json.loads(path.read_text(encoding="utf-8"))
            if _now() - float(cached.get("ts", 0)) < ttl_min * 60:
                return cached.get("data", {})
        except (json.JSONDecodeError, ValueError, OSError):
            pass
    try:
        data = {
            "alt_strength": alt_strength(min_volume),
            "macro": macro_divergence(macro_days),
        }
    except Exception as e:  # noqa: BLE001 — 부가데이터 실패가 대시보드를 막지 않게
        log.warning("market_extra 계산 실패: %s", e)
        return {}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"ts": _now(), "data": data}, ensure_ascii=False),
                        encoding="utf-8")
    except OSError:
        pass
    return data
