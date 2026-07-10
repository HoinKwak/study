"""거래 유니버스 선별 — 24h 거래대금 기준 고유동성 USDT 페어.

우선순위:
  1) 바이낸스 선물(fapi) 24h 티커 — 실전 기준
  2) 코인게코 파생 API — 실제 바이낸스 선물 거래대금 (fapi 지역차단 시)
  3) 현물 미러(data-api.binance.vision) — 최후 폴백 (보정 계수 적용)

스테이블코인 페어, 비USDT 페어는 제외한다.
"""
from __future__ import annotations

import requests

from ..utils import get_logger

log = get_logger("universe")

FAPI = "https://fapi.binance.com"
COINGECKO = "https://api.coingecko.com/api/v3/derivatives/exchanges/binance_futures"
MIRROR = "https://data-api.binance.vision"

# 기준 자산이 스테이블/법정화폐성인 페어 제외
STABLE_BASES = {
    "USDC", "FDUSD", "TUSD", "BUSD", "DAI", "USDP", "EUR", "AEUR", "EURI",
    "XUSD", "USDE", "PAXG", "USD1", "RLUSD", "PYUSD", "GUSD", "USDD",
}

# 비(非)크립토 상품 제외 — 바이낸스 TradFi-Perps(주식·상품·지수·거시지표 토큰).
# 별도 약관 서명이 필요하고 레버리지 한도가 달라 크립토 단타 대상이 아니다.
# (모호한 심볼은 주문 실패 시 자동 격리로 처리 — 여기엔 명확한 것만 등록)
NON_CRYPTO_BASES = {
    # 귀금속·원자재
    "XAU", "XAG", "XPT", "XPD", "CL", "BZ", "NG", "HG", "WTI", "GOLD", "SILVER",
    # 미국 주식·ETF
    "TSLA", "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "MSTR",
    "COIN", "HOOD", "CRCL", "SPCX", "MU", "PLTR", "AMD", "NFLX", "SOXL", "TQQQ",
    "SPY", "QQQ", "SNDK", "DRAM", "GME", "AMC", "NVDX", "CRCX",
    # 한국·아시아 주식
    "SAMSUNG", "SKHYNIX", "KORU", "EWY",
    # 거시지표·지수
    "NFP", "CPI", "SPX", "NDX", "VIX", "DXY",
}


def _filter_rows(rows: list[dict], min_quote_volume: float) -> list[tuple[str, float]]:
    """24h 티커 rows → [('BTC/USDT', 거래대금), ...] 거래대금 내림차순."""
    out: list[tuple[str, float]] = []
    for r in rows:
        sym = str(r.get("symbol", ""))
        if not sym.endswith("USDT"):
            continue
        base = sym[:-4]
        if not base or base in STABLE_BASES or base in NON_CRYPTO_BASES:
            continue
        # 현물 레버리지 토큰(UP/DOWN/BULL/BEAR) 방어
        if base.endswith(("UP", "DOWN", "BULL", "BEAR")) and base not in ("SUI",):
            continue
        try:
            qv = float(r.get("quoteVolume") or 0.0)
        except (TypeError, ValueError):
            continue
        if qv >= min_quote_volume:
            out.append((f"{base}/USDT", qv))
    out.sort(key=lambda x: -x[1])
    return out


# 현물 폴백 보정: 대형 페어의 현물 거래대금은 선물의 대략 1/5~1/10 수준.
# '선물 기준 $100M' 을 현물 티커로 근사할 때 임계값을 이 비율로 낮춘다.
SPOT_PROXY_SCALE = 0.2


def _from_coingecko(session: requests.Session, min_quote_volume: float,
                    timeout: int) -> list[tuple[str, float]]:
    """코인게코 파생 API — 실제 바이낸스 선물 24h 거래대금(USD)."""
    resp = session.get(COINGECKO, params={"include_tickers": "unexpired"},
                       timeout=timeout)
    resp.raise_for_status()
    tickers = resp.json().get("tickers", [])
    rows = []
    for t in tickers:
        sym = str(t.get("symbol", ""))
        try:
            usd = float((t.get("converted_volume") or {}).get("usd") or 0.0)
        except (TypeError, ValueError):
            continue
        rows.append({"symbol": sym, "quoteVolume": usd})
    return _filter_rows(rows, min_quote_volume)


def high_volume_usdt_symbols(min_quote_volume: float = 100e6,
                             timeout: int = 30) -> list[tuple[str, float]]:
    """24h 거래대금 ≥ min_quote_volume(선물 기준) 인 USDT 페어.

    [(심볼, 거래대금)] 반환 (거래대금 내림차순).
    """
    session = requests.Session()

    # 1) 선물 fapi (실전 기준)
    try:
        resp = session.get(f"{FAPI}/fapi/v1/ticker/24hr", timeout=timeout)
        resp.raise_for_status()
        rows = resp.json()
        if isinstance(rows, list) and rows:
            out = _filter_rows(rows, min_quote_volume)
            if out:
                log.info("유니버스 소스=선물: %.0fM 이상 %d 페어",
                         min_quote_volume / 1e6, len(out))
                return out
    except requests.RequestException as e:
        log.info("유니버스 소스 선물 실패(%s) — 코인게코 시도", str(e)[:60])

    # 2) 코인게코 파생 (실제 선물 거래대금)
    try:
        out = _from_coingecko(session, min_quote_volume, timeout)
        if out:
            log.info("유니버스 소스=코인게코(선물): %.0fM 이상 %d 페어",
                     min_quote_volume / 1e6, len(out))
            return out
    except requests.RequestException as e:
        log.info("유니버스 소스 코인게코 실패(%s) — 현물 미러 시도", str(e)[:60])

    # 3) 현물 미러 (보정 계수)
    try:
        resp = session.get(f"{MIRROR}/api/v3/ticker/24hr", timeout=timeout)
        resp.raise_for_status()
        rows = resp.json()
        if isinstance(rows, list) and rows:
            out = _filter_rows(rows, min_quote_volume * SPOT_PROXY_SCALE)
            if out:
                log.info("유니버스 소스=현물 미러: 임계 %.0fM(보정 ×%.1f) %d 페어",
                         min_quote_volume * SPOT_PROXY_SCALE / 1e6,
                         SPOT_PROXY_SCALE, len(out))
                return out
    except requests.RequestException as e:
        log.info("유니버스 소스 현물 미러 실패(%s)", str(e)[:60])

    log.warning("유니버스 조회 전부 실패")
    return []
