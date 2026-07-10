"""바이낸스 USDT-M 선물 커넥터 (ccxt 래핑).

테스트넷/실전 전환은 설정으로만. OHLCV·잔고·포지션·주문·레버리지 API 제공.
네이티브 파생 데이터(펀딩비, OI, 롱숏비율)도 코인글래스 폴백용으로 노출한다.
"""
from __future__ import annotations

from typing import Any

import ccxt

from ..config import Settings
from ..utils import get_logger

log = get_logger("binance")


class BinanceClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.exchange = self._build_exchange()

    def _build_exchange(self) -> ccxt.binance:
        ex = ccxt.binance(
            {
                "apiKey": self.settings.binance_api_key,
                "secret": self.settings.binance_api_secret,
                "enableRateLimit": True,
                "options": {
                    "defaultType": "future",  # USDT-M 선물
                    "adjustForTimeDifference": True,
                },
            }
        )
        if self.settings.binance_testnet:
            ex.set_sandbox_mode(True)
            log.info("바이낸스 테스트넷 모드로 연결")
        else:
            log.warning("바이낸스 실전(LIVE) 모드로 연결 — 실제 자금 주의")
        return ex

    # ------------------------------------------------------------------ 시세

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 200) -> list[list[float]]:
        """[[ts, open, high, low, close, volume], ...]"""
        return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    def fetch_ticker(self, symbol: str) -> dict[str, Any]:
        return self.exchange.fetch_ticker(symbol)

    def last_price(self, symbol: str) -> float:
        return float(self.fetch_ticker(symbol)["last"])

    # ------------------------------------------------------- 파생 데이터 (폴백)

    def fetch_funding_rate(self, symbol: str) -> float | None:
        """현재 펀딩비 (예: 0.0001 = 0.01%)."""
        try:
            fr = self.exchange.fetch_funding_rate(symbol)
            return float(fr.get("fundingRate")) if fr.get("fundingRate") is not None else None
        except Exception as e:  # noqa: BLE001
            log.warning("펀딩비 조회 실패 %s: %s", symbol, e)
            return None

    def fetch_open_interest(self, symbol: str) -> float | None:
        """미결제약정(계약 수량 기준)."""
        try:
            oi = self.exchange.fetch_open_interest(symbol)
            val = oi.get("openInterestAmount") or oi.get("openInterestValue")
            return float(val) if val is not None else None
        except Exception as e:  # noqa: BLE001
            log.warning("OI 조회 실패 %s: %s", symbol, e)
            return None

    # ------------------------------------------------------------------ 계좌

    def fetch_balance_usdt(self) -> float:
        """USDT 가용 잔고."""
        bal = self.exchange.fetch_balance()
        usdt = bal.get("USDT", {})
        return float(usdt.get("free", 0.0) or 0.0)

    def fetch_positions(self) -> list[dict[str, Any]]:
        """0 이 아닌 포지션만."""
        positions = self.exchange.fetch_positions()
        return [p for p in positions if float(p.get("contracts") or 0) != 0]

    # ------------------------------------------------------------------ 주문

    def set_leverage(self, symbol: str, leverage: int) -> None:
        try:
            self.exchange.set_leverage(leverage, symbol)
        except Exception as e:  # noqa: BLE001
            log.warning("레버리지 설정 실패 %s x%d: %s", symbol, leverage, e)

    def create_market_order(self, symbol: str, side: str, amount: float,
                            params: dict[str, Any] | None = None) -> dict[str, Any]:
        """시장가 주문. side = 'buy' | 'sell'."""
        return self.exchange.create_order(symbol, "market", side, amount, None, params or {})

    def create_stop_order(self, symbol: str, side: str, amount: float,
                          stop_price: float, reduce_only: bool = True) -> dict[str, Any]:
        """스톱마켓(손절/트리거) 주문."""
        params = {"stopPrice": stop_price, "reduceOnly": reduce_only}
        return self.exchange.create_order(symbol, "STOP_MARKET", side, amount, None, params)

    def market_meta(self, symbol: str) -> dict[str, Any]:
        """수량 정밀도/최소 주문량 등 마켓 메타."""
        self.exchange.load_markets()
        return self.exchange.market(symbol)

    def amount_to_precision(self, symbol: str, amount: float) -> float:
        return float(self.exchange.amount_to_precision(symbol, amount))
