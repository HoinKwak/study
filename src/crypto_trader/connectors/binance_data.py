"""바이낸스 선물 공개 파생 데이터 소스 (인증 불필요).

코인글래스 없이도 바이낸스가 직접 제공하는 시장 집계 지표를 사용한다:
  - 펀딩비 (premiumIndex)
  - 미결제약정(OI) 변화율 (openInterestHist)
  - 글로벌 롱숏 계좌 비율 (globalLongShortAccountRatio)
  - 상위 트레이더 롱숏 포지션 비율 (topLongShortPositionRatio)
  - 테이커 매수/매도 비율 (takerlongshortRatio)  ← 청산 데이터 대체용

이 엔드포인트들은 시장 전체 공개 데이터이므로, 테스트넷에서 매매하더라도
실전(live) 공개 API 에서 실시간 값을 가져온다.
"""
from __future__ import annotations

from typing import Any

import requests

from ..utils import get_logger

log = get_logger("binance_data")

FAPI = "https://fapi.binance.com"


class BinanceDerivativesData:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"accept": "application/json"})

    @staticmethod
    def _pair(symbol: str) -> str:
        """'BTC/USDT' -> 'BTCUSDT'."""
        return symbol.replace("/", "").upper()

    def _get(self, path: str, params: dict[str, Any]) -> Any | None:
        try:
            resp = self._session.get(f"{FAPI}{path}", params=params, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            log.warning("바이낸스 데이터 요청 실패 %s: %s", path, e)
            return None

    # --------------------------------------------------------------- 펀딩비

    def funding_rate(self, symbol: str) -> float | None:
        """현재(직전) 펀딩비. 예: 0.0001 = 0.01%."""
        data = self._get("/fapi/v1/premiumIndex", {"symbol": self._pair(symbol)})
        if isinstance(data, dict):
            return _to_float(data.get("lastFundingRate"))
        return None

    # ------------------------------------------------------------------ OI

    def open_interest_change_pct(self, symbol: str, period: str = "1h", limit: int = 2) -> float | None:
        """최근 두 구간의 OI 변화율(%). 상승이면 양수."""
        data = self._get(
            "/futures/data/openInterestHist",
            {"symbol": self._pair(symbol), "period": period, "limit": limit},
        )
        if not isinstance(data, list) or len(data) < 2:
            return None
        prev = _to_float(data[-2].get("sumOpenInterest"))
        curr = _to_float(data[-1].get("sumOpenInterest"))
        if prev and curr and prev != 0:
            return (curr - prev) / prev * 100.0
        return None

    # ------------------------------------------------------------- 롱숏 비율

    def global_long_short_ratio(self, symbol: str, period: str = "1h") -> float | None:
        """일반 계좌 롱숏 비율 (롱계좌수/숏계좌수). >1 이면 롱 우세(군중 심리)."""
        data = self._get(
            "/futures/data/globalLongShortAccountRatio",
            {"symbol": self._pair(symbol), "period": period, "limit": 1},
        )
        if isinstance(data, list) and data:
            return _to_float(data[-1].get("longShortRatio"))
        return None

    def top_trader_position_ratio(self, symbol: str, period: str = "1h") -> float | None:
        """상위 트레이더 포지션 롱숏 비율. 스마트머니 성향 참고."""
        data = self._get(
            "/futures/data/topLongShortPositionRatio",
            {"symbol": self._pair(symbol), "period": period, "limit": 1},
        )
        if isinstance(data, list) and data:
            return _to_float(data[-1].get("longShortRatio"))
        return None

    # ---------------------------------------------------- 테이커 매수/매도 비율

    def taker_buy_sell_ratio(self, symbol: str, period: str = "1h") -> float | None:
        """테이커 매수량/매도량 비율. >1 이면 시장가 매수 우세(상승 압력)."""
        data = self._get(
            "/futures/data/takerlongshortRatio",
            {"symbol": self._pair(symbol), "period": period, "limit": 1},
        )
        if isinstance(data, list) and data:
            return _to_float(data[-1].get("buySellRatio"))
        return None

    # --------------------------------------------------------- 통합 스냅샷

    def snapshot(self, symbol: str, period: str = "1h") -> dict[str, float | None]:
        """한 심볼의 파생 지표를 한 번에 모아 dict 로 반환."""
        return {
            "funding_rate": self.funding_rate(symbol),
            "oi_change_pct": self.open_interest_change_pct(symbol, period),
            "global_ls_ratio": self.global_long_short_ratio(symbol, period),
            "top_trader_ls_ratio": self.top_trader_position_ratio(symbol, period),
            "taker_buy_sell_ratio": self.taker_buy_sell_ratio(symbol, period),
        }


def _to_float(v: Any) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None
