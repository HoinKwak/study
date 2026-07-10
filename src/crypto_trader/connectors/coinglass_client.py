"""코인글래스 v4 REST 클라이언트.

펀딩비 / 미결제약정(OI) / 청산 / 롱숏비율 등 파생 집계 데이터를 가져온다.
API 키가 없으면 모든 메서드가 None 을 반환하고, 상위 레이어가 바이낸스
네이티브 데이터로 폴백한다.

참고: 코인글래스 엔드포인트/스펙은 플랜과 버전에 따라 다를 수 있으므로,
      실제 응답 스키마에 맞춰 `_get` 파싱부를 조정해야 할 수 있다.
"""
from __future__ import annotations

from typing import Any

import requests

from ..config import Settings
from ..utils import get_logger

log = get_logger("coinglass")

BASE_URL = "https://open-api-v4.coinglass.com"


class CoinglassClient:
    def __init__(self, settings: Settings, timeout: int = 10):
        self.settings = settings
        self.timeout = timeout
        self.enabled = settings.has_coinglass_key
        self._session = requests.Session()
        if self.enabled:
            self._session.headers.update(
                {
                    "accept": "application/json",
                    "CG-API-KEY": settings.coinglass_api_key,
                }
            )
        else:
            log.info("코인글래스 키 없음 — 바이낸스 네이티브 데이터로 폴백")

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any | None:
        if not self.enabled:
            return None
        url = f"{BASE_URL}{path}"
        try:
            resp = self._session.get(url, params=params or {}, timeout=self.timeout)
            resp.raise_for_status()
            payload = resp.json()
            # v4 는 보통 {"code": "0", "data": [...]} 형태
            if isinstance(payload, dict):
                if payload.get("code") not in (None, "0", 0):
                    log.warning("코인글래스 오류 %s: %s", path, payload.get("msg"))
                    return None
                return payload.get("data", payload)
            return payload
        except requests.RequestException as e:
            log.warning("코인글래스 요청 실패 %s: %s", path, e)
            return None

    @staticmethod
    def _base_coin(symbol: str) -> str:
        """'BTC/USDT' -> 'BTC'."""
        return symbol.split("/")[0].upper()

    # ------------------------------------------------------------- 엔드포인트

    def funding_rate(self, symbol: str) -> float | None:
        """OI 가중 펀딩비(있으면). 값이 없으면 None."""
        coin = self._base_coin(symbol)
        data = self._get("/api/futures/funding-rate/oi-weight-history",
                         {"symbol": coin, "interval": "8h", "limit": 1})
        return _last_numeric(data, keys=("fundingRate", "funding_rate", "close"))

    def open_interest_change(self, symbol: str, interval: str = "1h") -> float | None:
        """최근 구간 OI 변화율(%). 상승이면 양수."""
        coin = self._base_coin(symbol)
        data = self._get("/api/futures/open-interest/aggregated-history",
                         {"symbol": coin, "interval": interval, "limit": 2})
        return _pct_change(data, keys=("close", "openInterest", "open_interest"))

    def long_short_ratio(self, symbol: str, interval: str = "1h") -> float | None:
        """글로벌 롱숏 계좌 비율 (롱/숏). >1 이면 롱 우세."""
        coin = self._base_coin(symbol)
        data = self._get("/api/futures/global-long-short-account-ratio/history",
                         {"symbol": coin, "interval": interval, "limit": 1})
        return _last_numeric(data, keys=("longShortRatio", "long_short_ratio", "ratio"))

    def liquidation_net(self, symbol: str, interval: str = "1h") -> float | None:
        """최근 구간 순청산액 (롱청산 - 숏청산, USD).

        양수 = 롱이 더 많이 청산됨(하락 압력 후 반등 여지),
        음수 = 숏이 더 많이 청산됨(상승 압력 후 되돌림 여지).
        """
        coin = self._base_coin(symbol)
        data = self._get("/api/futures/liquidation/aggregated-history",
                         {"symbol": coin, "interval": interval, "limit": 1})
        if not data:
            return None
        row = data[-1] if isinstance(data, list) else data
        if not isinstance(row, dict):
            return None
        long_liq = _to_float(row.get("longLiquidationUsd") or row.get("long_liquidation_usd"))
        short_liq = _to_float(row.get("shortLiquidationUsd") or row.get("short_liquidation_usd"))
        if long_liq is None and short_liq is None:
            return None
        return (long_liq or 0.0) - (short_liq or 0.0)


# ------------------------------------------------------------------ 파싱 헬퍼

def _to_float(v: Any) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _last_row(data: Any) -> dict | None:
    if isinstance(data, list) and data:
        return data[-1] if isinstance(data[-1], dict) else None
    if isinstance(data, dict):
        return data
    return None


def _last_numeric(data: Any, keys: tuple[str, ...]) -> float | None:
    row = _last_row(data)
    if not row:
        return None
    for k in keys:
        if k in row:
            val = _to_float(row[k])
            if val is not None:
                return val
    return None


def _pct_change(data: Any, keys: tuple[str, ...]) -> float | None:
    if not isinstance(data, list) or len(data) < 2:
        return None
    prev, curr = _last_row(data[:-1]), _last_row(data)
    if not prev or not curr:
        return None
    for k in keys:
        p, c = _to_float(prev.get(k)), _to_float(curr.get(k))
        if p and c and p != 0:
            return (c - p) / p * 100.0
    return None
