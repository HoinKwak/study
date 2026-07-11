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

    # ------------------------------------------------------------ 캔들(공개)

    def klines(self, symbol: str, interval: str = "5m", limit: int = 30
               ) -> dict[str, list[float]] | None:
        """공개 선물 캔들. {'open_time','open','high','low','close','volume'} 병렬 리스트.

        인증 불필요(실전 fapi). 지역차단 시 None.
        """
        data = self._get(
            "/fapi/v1/klines",
            {"symbol": self._pair(symbol), "interval": interval, "limit": limit},
        )
        if not isinstance(data, list) or not data:
            return None
        out: dict[str, list[float]] = {
            "open_time": [], "open": [], "high": [], "low": [], "close": [], "volume": [],
        }
        for row in data:
            # [openTime, open, high, low, close, volume, closeTime, ...]
            try:
                out["open_time"].append(float(row[0]))
                out["open"].append(float(row[1]))
                out["high"].append(float(row[2]))
                out["low"].append(float(row[3]))
                out["close"].append(float(row[4]))
                out["volume"].append(float(row[5]))
            except (TypeError, ValueError, IndexError):
                continue
        return out if out["close"] else None

    def open_interest_hist(self, symbol: str, period: str = "5m", limit: int = 6
                           ) -> list[float] | None:
        """최근 OI(sumOpenInterest) 시계열. 오래된→최신 순."""
        data = self._get(
            "/futures/data/openInterestHist",
            {"symbol": self._pair(symbol), "period": period, "limit": limit},
        )
        if not isinstance(data, list) or not data:
            return None
        series = [v for v in (_to_float(r.get("sumOpenInterest")) for r in data) if v is not None]
        return series or None

    def open_interest_value_series(self, symbol: str, period: str = "1h", limit: int = 48
                                   ) -> list[list[float]] | None:
        """OI 명목가치(sumOpenInterestValue) 시계열. [[ts_ms, notional_usdt], ...] 오래된→최신."""
        data = self._get(
            "/futures/data/openInterestHist",
            {"symbol": self._pair(symbol), "period": period, "limit": limit},
        )
        if not isinstance(data, list) or not data:
            return None
        out: list[list[float]] = []
        for r in data:
            ts = _to_float(r.get("timestamp"))
            val = _to_float(r.get("sumOpenInterestValue"))
            if ts is not None and val is not None:
                out.append([int(ts), val])
        return out or None

    def taker_volume_series(self, symbol: str, period: str = "1h", limit: int = 48
                            ) -> list[list[float]] | None:
        """테이커 매수/매도 거래량 시계열(CVD 계산용). [[ts_ms, buyVol, sellVol], ...] 오래된→최신."""
        data = self._get(
            "/futures/data/takerlongshortRatio",
            {"symbol": self._pair(symbol), "period": period, "limit": limit},
        )
        if not isinstance(data, list) or not data:
            return None
        out: list[list[float]] = []
        for r in data:
            ts = _to_float(r.get("timestamp"))
            bv = _to_float(r.get("buyVol"))
            sv = _to_float(r.get("sellVol"))
            if ts is not None and bv is not None and sv is not None:
                out.append([int(ts), bv, sv])
        return out or None

    # ---------------------------------------------------- 전체 심볼 벌크(공개)

    def all_24h_tickers(self) -> dict[str, dict[str, Any]] | None:
        """모든 선물 심볼의 24h 티커를 한 번에. {'BTCUSDT': {...}, ...}."""
        data = self._get("/fapi/v1/ticker/24hr", {})
        if not isinstance(data, list):
            return None
        return {str(r.get("symbol", "")): r for r in data if r.get("symbol")}

    def all_funding_rates(self) -> dict[str, float] | None:
        """모든 심볼의 현재 펀딩비를 한 번에. {'BTCUSDT': 0.0001, ...}."""
        data = self._get("/fapi/v1/premiumIndex", {})
        if not isinstance(data, list):
            return None
        out: dict[str, float] = {}
        for r in data:
            sym = str(r.get("symbol", ""))
            fr = _to_float(r.get("lastFundingRate"))
            if sym and fr is not None:
                out[sym] = fr
        return out or None

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
