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


def _max_notional_from_tiers(tiers: list, leverage: float) -> float | None:
    """레버리지 브라켓 목록에서 주어진 레버리지에 허용되는 최대 명목가치.

    각 tier: maxLeverage 이하에서만 maxNotional 까지 허용. 요청 레버리지를
    수용하는(최대레버리지 ≥ leverage) tier 들의 maxNotional 중 최댓값.
    tiers 비어있거나 파싱 불가 시 None.
    """
    best: float | None = None
    for t in tiers or []:
        info = t.get("info", {}) if isinstance(t, dict) else {}
        maxlev = t.get("maxLeverage") if isinstance(t, dict) else None
        maxnot = t.get("maxNotional") if isinstance(t, dict) else None
        if maxlev is None:
            maxlev = info.get("maxLeverage")
        if maxnot is None:
            maxnot = info.get("maxNotionalValue") or info.get("maxNotional")
        try:
            maxlev_f = float(maxlev)
            maxnot_f = float(maxnot)
        except (TypeError, ValueError):
            continue
        if maxlev_f >= leverage:
            best = maxnot_f if best is None else max(best, maxnot_f)
    return best


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

    @property
    def hedge(self) -> bool:
        return self.settings.binance_hedge_mode

    def ensure_position_mode(self) -> None:
        """헤지 모드(dualSidePosition) 설정. 이미 해당 모드면 조용히 통과."""
        try:
            self.exchange.set_position_mode(self.hedge)
            log.info("포지션 모드 설정: %s", "헤지(dual-side)" if self.hedge else "단방향(one-way)")
        except Exception as e:  # noqa: BLE001
            # -4059: 변경할 필요 없음(이미 해당 모드) → 정상
            if "-4059" in str(e) or "No need to change" in str(e):
                return
            log.warning("포지션 모드 설정 실패: %s", e)

    def set_margin_mode(self, symbol: str) -> None:
        """심볼 마진 모드(isolated/cross) 설정."""
        try:
            self.exchange.set_margin_mode(self.settings.margin_mode, self.resolve_symbol(symbol))
        except Exception as e:  # noqa: BLE001
            if "-4046" in str(e) or "No need to change" in str(e):
                return
            log.warning("마진 모드 설정 실패 %s: %s", symbol, e)

    @staticmethod
    def _pos_side(direction_or_side: str) -> str:
        """'long'/'short'/'buy'/'sell' → 'LONG'/'SHORT' (헤지 positionSide)."""
        v = direction_or_side.lower()
        if v in ("long", "buy"):
            return "LONG"
        return "SHORT"

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
        """USDT 계정 순자산(마진밸런스, 미실현손익 포함).

        'free'(가용잔고)만 쓰면 미체결 지정가 주문·포지션에 묶인 마진이 빠져
        재시작·주문대기 중 현재 자본이 낮게 잡혔다가 주문이 풀리며 서서히
        올라오는(정상화) 문제가 생긴다. 그래서 total(지갑잔고) 또는 마진밸런스를 쓴다.
        """
        bal = self.exchange.fetch_balance()
        usdt = bal.get("USDT", {}) or {}
        info = bal.get("info", {}) or {}
        # 1순위: 선물 계정 마진밸런스(uPnL 포함) — 미체결·마진과 무관하게 안정.
        for key in ("totalMarginBalance", "totalWalletBalance"):
            v = info.get(key)
            if v not in (None, ""):
                try:
                    return float(v)
                except (TypeError, ValueError):
                    pass
        # 2순위: ccxt 정규화 total(=free+used). 3순위: free.
        total = usdt.get("total")
        if total not in (None, ""):
            return float(total or 0.0)
        return float(usdt.get("free", 0.0) or 0.0)

    def fetch_positions(self, symbol: str | None = None) -> list[dict[str, Any]]:
        """0 이 아닌 포지션만. symbol 지정 시 해당 심볼만(레이트리밋 절약)."""
        symbols = [self.resolve_symbol(symbol)] if symbol else None
        positions = self.exchange.fetch_positions(symbols)
        return [p for p in positions if float(p.get("contracts") or 0) != 0]

    def fetch_position_side(self, symbol: str, direction: str) -> dict[str, Any] | None:
        """헤지 모드에서 특정 방향(long/short) 포지션만 반환."""
        want = self._pos_side(direction)
        canonical = self.resolve_symbol(symbol)
        for p in self.fetch_positions(symbol):
            if p.get("symbol") != canonical:
                continue
            info_side = (p.get("info", {}) or {}).get("positionSide", "").upper()
            if not self.hedge or info_side == want or (p.get("side") == direction.lower()):
                return p
        return None

    # ------------------------------------------------------------------ 주문

    # 레버리지 하향 사다리 — 30x 미지원 심볼은 지원되는 최대값을 자동 탐색
    _LEV_LADDER = [30, 25, 20, 15, 10, 8, 6, 5, 4, 3, 2, 1]

    def set_leverage(self, symbol: str, leverage: int) -> int:
        """원하는 레버리지 설정 시도. 미지원(-4028)이면 지원되는 최대값으로 하향.

        반환값 = 실제로 설정된 레버리지. 알트코인의 낮은 레버리지 한도에 자동 적응.
        (레버리지는 증거금 효율만 좌우 — 포지션 크기·손익은 수량으로 이미 결정됨)
        """
        canonical = self.resolve_symbol(symbol)
        ladder = [leverage] + [x for x in self._LEV_LADDER if x < leverage]
        for lev in ladder:
            try:
                self.exchange.set_leverage(lev, canonical)
                if lev != leverage:
                    log.info("레버리지 하향 적응 %s: %dx 미지원 → %dx 설정", symbol, leverage, lev)
                return lev
            except Exception as e:  # noqa: BLE001
                # -4028: 레버리지 값 무효 → 다음(더 낮은) 값 시도
                if "-4028" in str(e) or "not valid" in str(e).lower():
                    continue
                # 그 외 오류(이미 설정됨 등)는 요청값 유지로 간주
                log.warning("레버리지 설정 경고 %s x%d: %s", symbol, lev, str(e)[:80])
                return lev
        log.warning("레버리지 설정 전부 실패 %s — 거래소 기본값 사용", symbol)
        return 1

    def _order_params(self, position_side: str | None, reduce_only: bool,
                      extra: dict[str, Any] | None = None) -> dict[str, Any]:
        """헤지 모드면 positionSide 부여(reduceOnly 미사용), 단방향이면 reduceOnly 사용."""
        params: dict[str, Any] = dict(extra or {})
        if self.hedge:
            if position_side:
                params["positionSide"] = self._pos_side(position_side)
            # 헤지 모드에서는 reduceOnly 를 보내면 거부됨 → positionSide 로 방향 관리
        elif reduce_only:
            params["reduceOnly"] = True
        return params

    def create_market_order(self, symbol: str, side: str, amount: float,
                            params: dict[str, Any] | None = None,
                            position_side: str | None = None,
                            reduce_only: bool = False) -> dict[str, Any]:
        """시장가 주문. side = 'buy' | 'sell'. position_side = 'long'|'short'(헤지)."""
        p = self._order_params(position_side, reduce_only, params)
        return self.exchange.create_order(
            self.resolve_symbol(symbol), "market", side, amount, None, p)

    def create_post_only_order(self, symbol: str, side: str, amount: float, price: float,
                               position_side: str | None = None) -> dict[str, Any]:
        """포스트온리(GTX) 지정가 주문 — 메이커 체결 보장(테이커가 되면 거부됨)."""
        p = self._order_params(position_side, reduce_only=False,
                               extra={"timeInForce": "GTX"})
        return self.exchange.create_order(
            self.resolve_symbol(symbol), "limit", side, amount, price, p)

    def fetch_order(self, order_id: str, symbol: str) -> dict[str, Any]:
        return self.exchange.fetch_order(order_id, self.resolve_symbol(symbol))

    def cancel_order(self, order_id: str, symbol: str) -> None:
        try:
            self.exchange.cancel_order(order_id, self.resolve_symbol(symbol))
        except Exception as e:  # noqa: BLE001
            log.warning("주문 취소 실패 %s: %s", order_id, e)

    def best_bid_ask(self, symbol: str) -> tuple[float, float]:
        """(최우선 매수호가, 최우선 매도호가)."""
        ob = self.exchange.fetch_order_book(self.resolve_symbol(symbol), limit=5)
        bid = float(ob["bids"][0][0]) if ob.get("bids") else 0.0
        ask = float(ob["asks"][0][0]) if ob.get("asks") else 0.0
        return bid, ask

    def create_stop_order(self, symbol: str, side: str, amount: float, stop_price: float,
                          position_side: str | None = None) -> dict[str, Any]:
        """스톱마켓(손절) 주문. 포지션 청산용이므로 reduce_only/positionSide 로 관리."""
        p = self._order_params(position_side, reduce_only=True, extra={"stopPrice": stop_price})
        return self.exchange.create_order(
            self.resolve_symbol(symbol), "STOP_MARKET", side, amount, None, p)

    def create_take_profit_order(self, symbol: str, side: str, amount: float, tp_price: float,
                                 position_side: str | None = None) -> dict[str, Any]:
        """익절(트리거) 주문."""
        p = self._order_params(position_side, reduce_only=True, extra={"stopPrice": tp_price})
        return self.exchange.create_order(
            self.resolve_symbol(symbol), "TAKE_PROFIT_MARKET", side, amount, None, p)

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

    def close_quantity(self, symbol: str, direction: str, quantity: float) -> dict[str, Any] | None:
        """헤지 모드에서 특정 방향 포지션을 '지정 수량만큼만' 시장가 청산.

        여러 슬리브가 같은 심볼/방향을 합산 보유하므로, 각 슬리브는 자기 수량만
        reduceOnly 로 닫는다. 전체 포지션을 닫지 않는다.
        """
        qty = self.amount_to_precision(symbol, quantity)
        if float(qty) <= 0:
            return None
        order_side = "sell" if direction.lower() == "long" else "buy"
        log.info("부분 청산 %s %s qty=%s (%s)", symbol, order_side, qty, direction)
        return self.create_market_order(symbol, order_side, qty,
                                        position_side=direction.lower(), reduce_only=True)

    def close_position(self, symbol: str, direction: str | None = None) -> dict[str, Any] | None:
        """보유 포지션 청산. direction 지정 시 헤지 모드에서 해당 방향만 청산."""
        canonical = self.resolve_symbol(symbol)
        if direction is not None and self.hedge:
            pos = self.fetch_position_side(symbol, direction)
        else:
            pos = next((p for p in self.fetch_positions(symbol)
                        if p.get("symbol") == canonical), None)
        if pos is None:
            log.info("청산할 포지션 없음: %s %s", symbol, direction or "")
            return None
        contracts = abs(float(pos.get("contracts") or 0))
        if contracts == 0:
            return None
        pos_dir = pos.get("side") or (direction or "long")
        # 롱이면 sell, 숏이면 buy 로 반대 청산
        order_side = "sell" if pos_dir == "long" else "buy"
        qty = self.amount_to_precision(symbol, contracts)
        log.info("포지션 청산 %s %s qty=%s (side=%s)", symbol, order_side, qty, pos_dir)
        return self.create_market_order(symbol, order_side, qty,
                                        position_side=pos_dir, reduce_only=True)

    def market_meta(self, symbol: str) -> dict[str, Any]:
        """수량 정밀도/최소 주문량 등 마켓 메타."""
        self.exchange.load_markets()
        return self.exchange.market(self.resolve_symbol(symbol))

    def min_notional(self, symbol: str) -> float:
        """최소 명목가치(USDT). 없으면 5.0 기본."""
        m = self.market_meta(symbol)
        cost_min = (m.get("limits", {}).get("cost", {}) or {}).get("min")
        return float(cost_min) if cost_min else 5.0

    def min_amount(self, symbol: str) -> float:
        """최소 주문 수량(LOT_SIZE minQty). 없으면 0.0(제한 없음)."""
        try:
            m = self.market_meta(symbol)
        except Exception:  # noqa: BLE001 — 메타 조회 실패 시 제한 없음으로 처리
            return 0.0
        amt_min = (m.get("limits", {}).get("amount", {}) or {}).get("min")
        return float(amt_min) if amt_min else 0.0

    def max_position_notional(self, symbol: str, leverage: int) -> float | None:
        """해당 레버리지에서 이 심볼이 허용하는 최대 포지션 명목가치(USDT).

        바이낸스 레버리지 브라켓(tier)에서 산출. 소형 알트는 30배에서 한도가
        작아(예: $5,000) 초과 주문이 -2027 로 거부됨 → 사전 캡 용도.
        조회 실패 시 None(캡 미적용).
        """
        cache = self.__dict__.setdefault("_lev_tiers_cache", {})
        canonical = self.resolve_symbol(symbol)
        tiers = cache.get(canonical)
        if tiers is None:
            try:
                fetched = self.exchange.fetch_leverage_tiers([canonical])
                tiers = fetched.get(canonical) or []
            except Exception as e:  # noqa: BLE001 — 캡은 최선노력, 실패해도 진입은 진행
                log.warning("레버리지 브라켓 조회 실패 %s: %s", symbol, str(e)[:80])
                tiers = []
            cache[canonical] = tiers
        return _max_notional_from_tiers(tiers, leverage)

    def amount_to_precision(self, symbol: str, amount: float) -> float:
        return float(self.exchange.amount_to_precision(self.resolve_symbol(symbol), amount))
