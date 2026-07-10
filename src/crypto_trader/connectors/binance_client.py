"""바이낸스 USDT-M 선물 커넥터 (ccxt 래핑).

테스트넷/실전 전환은 설정으로만. OHLCV·잔고·포지션·주문·레버리지 API 제공.
네이티브 파생 데이터(펀딩비, OI, 롱숏비율)도 코인글래스 폴백용으로 노출한다.
"""
from __future__ import annotations

import os
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
                    # 스팟 테스트넷(testnet.binance.vision)은 이 환경에서 차단됨.
                    # USDT-M 선물(linear)만 로드해 불필요한 스팟 호출을 회피.
                    "fetchMarkets": ["linear"],
                    # ccxt 는 선물 테스트넷 private 호출에 경고 예외를 던지지만,
                    # 이 옵션으로 비활성화하고 testnet.binancefuture.com 을 계속 사용.
                    "disableFuturesSandboxWarning": True,
                },
            }
        )
        # 사설/기업 프록시(MITM) 환경 대응: CA 번들이 지정돼 있으면 ccxt 의 requests
        # 세션이 그 번들을 신뢰하고 env 프록시를 사용하도록 한다. ccxt 는 기본적으로
        # session.trust_env=False 라 env 의 HTTPS_PROXY/CA 를 무시하므로 명시 설정이 필요.
        # (일반 PC 에서는 해당 env 가 없어 이 블록이 건너뛰어져 기본 동작 유지 — 무영향)
        ca_bundle = os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("SSL_CERT_FILE")
        if ca_bundle:
            ex.session.verify = ca_bundle
            ex.session.trust_env = True

        if self.settings.binance_testnet:
            ex.set_sandbox_mode(True)
            log.info("바이낸스 테스트넷 모드로 연결")
        else:
            log.warning("바이낸스 실전(LIVE) 모드로 연결 — 실제 자금 주의")
        return ex

    # ------------------------------------------------------------------ 시세

    def resolve_symbol(self, symbol: str) -> str:
        """'BTC/USDT' → ccxt 정규 심볼 'BTC/USDT:USDT'(USDT-M 무기한).

        포지션/주문 조회 시 심볼 표기가 일치하도록 항상 이 형태로 정규화한다.
        이미 ':' 가 있으면 그대로 둔다.
        """
        if ":" in symbol:
            return symbol
        try:
            return self.exchange.market(symbol)["symbol"]
        except Exception:  # noqa: BLE001
            # 마켓 미로드 등 예외 시 관례적 형태로 폴백
            return f"{symbol}:USDT" if symbol.endswith("/USDT") else symbol

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 200) -> list[list[float]]:
        """[[ts, open, high, low, close, volume], ...]"""
        return self.exchange.fetch_ohlcv(self.resolve_symbol(symbol), timeframe=timeframe, limit=limit)

    def fetch_ticker(self, symbol: str) -> dict[str, Any]:
        return self.exchange.fetch_ticker(self.resolve_symbol(symbol))

    def last_price(self, symbol: str) -> float:
        return float(self.fetch_ticker(symbol)["last"])

    # ------------------------------------------------------- 파생 데이터 (폴백)

    def fetch_funding_rate(self, symbol: str) -> float | None:
        """현재 펀딩비 (예: 0.0001 = 0.01%)."""
        try:
            fr = self.exchange.fetch_funding_rate(self.resolve_symbol(symbol))
            return float(fr.get("fundingRate")) if fr.get("fundingRate") is not None else None
        except Exception as e:  # noqa: BLE001
            log.warning("펀딩비 조회 실패 %s: %s", symbol, e)
            return None

    def fetch_open_interest(self, symbol: str) -> float | None:
        """미결제약정(계약 수량 기준)."""
        try:
            oi = self.exchange.fetch_open_interest(self.resolve_symbol(symbol))
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

    def fetch_positions(self, symbol: str | None = None) -> list[dict[str, Any]]:
        """0 이 아닌 포지션만. symbol 지정 시 해당 심볼만(레이트리밋 절약)."""
        symbols = [self.resolve_symbol(symbol)] if symbol else None
        positions = self.exchange.fetch_positions(symbols)
        return [p for p in positions if float(p.get("contracts") or 0) != 0]

    # ------------------------------------------------------------------ 주문

    def set_leverage(self, symbol: str, leverage: int) -> None:
        try:
            self.exchange.set_leverage(leverage, self.resolve_symbol(symbol))
        except Exception as e:  # noqa: BLE001
            log.warning("레버리지 설정 실패 %s x%d: %s", symbol, leverage, e)

    def create_market_order(self, symbol: str, side: str, amount: float,
                            params: dict[str, Any] | None = None) -> dict[str, Any]:
        """시장가 주문. side = 'buy' | 'sell'."""
        return self.exchange.create_order(
            self.resolve_symbol(symbol), "market", side, amount, None, params or {})

    def create_stop_order(self, symbol: str, side: str, amount: float,
                          stop_price: float, reduce_only: bool = True) -> dict[str, Any]:
        """스톱마켓(손절/트리거) 주문."""
        params = {"stopPrice": stop_price, "reduceOnly": reduce_only}
        return self.exchange.create_order(
            self.resolve_symbol(symbol), "STOP_MARKET", side, amount, None, params)

    def create_take_profit_order(self, symbol: str, side: str, amount: float,
                                 tp_price: float, reduce_only: bool = True) -> dict[str, Any]:
        """익절(트리거) 주문."""
        params = {"stopPrice": tp_price, "reduceOnly": reduce_only}
        return self.exchange.create_order(
            self.resolve_symbol(symbol), "TAKE_PROFIT_MARKET", side, amount, None, params)

    def fetch_open_orders(self, symbol: str | None = None,
                          include_conditional: bool = True) -> list[dict[str, Any]]:
        """미체결 주문 조회.

        바이낸스 선물의 STOP_MARKET/TAKE_PROFIT_MARKET 은 '전략(strategy) 주문'이라
        기본 조회에 안 잡힌다. include_conditional=True 면 조건부 주문도 합쳐 반환.
        """
        sym = self.resolve_symbol(symbol) if symbol else None
        regular = self.exchange.fetch_open_orders(sym)
        if not include_conditional:
            return regular
        try:
            conditional = self.exchange.fetch_open_orders(sym, params={"stop": True})
        except Exception as e:  # noqa: BLE001
            log.warning("조건부 주문 조회 실패 %s: %s", symbol, e)
            conditional = []
        return regular + conditional

    def cancel_all_orders(self, symbol: str) -> None:
        """일반 주문 + 조건부(손절/익절) 주문을 모두 취소.

        cancel_all_orders 기본 호출은 조건부(전략) 주문을 취소하지 못하므로,
        조건부 주문은 개별적으로 params={'stop': True} 로 취소한다.
        """
        sym = self.resolve_symbol(symbol)
        try:
            self.exchange.cancel_all_orders(sym)
        except Exception as e:  # noqa: BLE001
            log.warning("일반 주문 취소 실패 %s: %s", symbol, e)
        try:
            for o in self.exchange.fetch_open_orders(sym, params={"stop": True}):
                try:
                    self.exchange.cancel_order(o["id"], sym, params={"stop": True})
                except Exception as e:  # noqa: BLE001
                    log.warning("조건부 주문 취소 실패 %s: %s", o.get("id"), e)
        except Exception as e:  # noqa: BLE001
            log.warning("조건부 주문 조회 실패 %s: %s", symbol, e)

    def close_position(self, symbol: str) -> dict[str, Any] | None:
        """보유 포지션을 시장가 reduceOnly 로 청산."""
        canonical = self.resolve_symbol(symbol)
        pos = next((p for p in self.fetch_positions(symbol) if p.get("symbol") == canonical), None)
        if pos is None:
            log.info("청산할 포지션 없음: %s", symbol)
            return None
        contracts = abs(float(pos.get("contracts") or 0))
        if contracts == 0:
            return None
        # 롱이면 sell, 숏이면 buy 로 반대 청산
        side = "sell" if (pos.get("side") == "long") else "buy"
        qty = self.amount_to_precision(symbol, contracts)
        log.info("포지션 청산 %s %s qty=%s", symbol, side, qty)
        return self.create_market_order(symbol, side, qty, {"reduceOnly": True})

    def market_meta(self, symbol: str) -> dict[str, Any]:
        """수량 정밀도/최소 주문량 등 마켓 메타."""
        self.exchange.load_markets()
        return self.exchange.market(self.resolve_symbol(symbol))

    def min_notional(self, symbol: str) -> float:
        """최소 명목가치(USDT). 없으면 5.0 기본."""
        m = self.market_meta(symbol)
        cost_min = (m.get("limits", {}).get("cost", {}) or {}).get("min")
        return float(cost_min) if cost_min else 5.0

    def amount_to_precision(self, symbol: str, amount: float) -> float:
        return float(self.exchange.amount_to_precision(self.resolve_symbol(symbol), amount))
