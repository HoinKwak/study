"""주문 실행 추상화. dry_run / paper / live 모드를 하나의 인터페이스로.

- dry_run : 주문 안 냄, 로그만 (기본)
- paper   : 바이낸스 테스트넷에 실제 주문 (모의 자금)
- live    : 실계좌 주문 (⚠️)
"""
from __future__ import annotations

from dataclasses import dataclass

from ..config import Settings, TradeMode
from ..connectors import BinanceClient
from ..risk import TradePlan
from ..signals.base import Direction
from ..utils import get_logger

log = get_logger("executor")

# 바이낸스 오류코드 → 사람이 읽을 원인. fatal=심볼 자체 문제(재시도 무의미→격리)
_ERROR_MAP = {
    "-4411": ("TradFi-Perps 약관 미서명 (주식·상품 토큰, 크립토 아님)", True),
    "-4028": ("레버리지 값 무효", False),   # set_leverage 가 자동 하향 처리 → 격리 아님
    "-1121": ("존재하지 않는 심볼", True),
    "-4108": ("심볼 거래 불가/정지", True),
    "-4131": ("호가 없음(유동성 부족)", True),
    "-2019": ("증거금 부족", False),
    "-4164": ("최소 명목가치 미달", False),
    "-1013": ("주문 필터 위반(수량/가격 정밀도)", False),
}


def _friendly_error(msg: str) -> str:
    for code, (desc, _fatal) in _ERROR_MAP.items():
        if code in msg:
            return f"{desc} [{code}]"
    # 코드 없으면 원문 축약
    return msg[:120]


def _is_fatal_symbol_error(msg: str) -> bool:
    return any(code in msg and fatal for code, (_d, fatal) in _ERROR_MAP.items())


@dataclass
class Fill:
    symbol: str
    side: str            # 'buy' | 'sell'
    quantity: float
    price: float
    mode: str
    order_id: str | None = None


class PaperBroker:
    """dry_run 모드에서 체결을 시뮬레이션하고 간단한 손익을 추적."""

    def __init__(self, starting_equity: float = 10_000.0):
        self.equity = starting_equity
        self.positions: dict[str, dict] = {}  # symbol -> {side, qty, entry}

    def fill(self, plan: TradePlan) -> Fill:
        side = "buy" if plan.direction is Direction.LONG else "sell"
        self.positions[plan.symbol] = {
            "side": plan.direction.value,
            "qty": plan.quantity,
            "entry": plan.entry_price,
            "stop": plan.stop_price,
            "tp": plan.take_profit,
        }
        return Fill(plan.symbol, side, plan.quantity, plan.entry_price, "dry_run")


class Executor:
    def __init__(self, settings: Settings, binance: BinanceClient | None,
                 paper_broker: PaperBroker | None = None):
        self.s = settings
        self.binance = binance
        self.paper = paper_broker or PaperBroker()
        self.last_error: str = ""
        self.last_error_fatal: bool = False

    def _market_entry(self, plan: TradePlan, side: str, pos_side: str,
                      twap_slices: int, slice_interval_sec: float = 0.0) -> float:
        """시장가 진입. twap_slices>1 이면 수량을 균등 분할해 순차 체결.

        slice_interval_sec>0 이면 슬라이스 사이에 그만큼 대기해 시간 분산(TWAP).
        최소 명목가치 미만이 되지 않도록 분할 수를 자동 축소한다.
        진입 중에도 SL 은 첫 슬라이스 후 거래소 스톱주문으로 보호됨(엔진이 예약).
        """
        import time as _time

        n = max(1, twap_slices)
        min_notional = self.binance.min_notional(plan.symbol)
        # 슬라이스가 최소 명목가치 미만이면 분할 수 축소
        while n > 1 and (plan.quantity / n) * plan.entry_price < min_notional:
            n -= 1
        slice_qty = self.binance.amount_to_precision(plan.symbol, plan.quantity / n)
        prices, weights = [], []
        for i in range(n):
            if float(slice_qty) <= 0:
                break
            order = self.binance.create_market_order(plan.symbol, side, slice_qty,
                                                     position_side=pos_side)
            px = float(order.get("average") or order.get("price") or plan.entry_price)
            prices.append(px)
            weights.append(float(slice_qty))
            if slice_interval_sec > 0 and i < n - 1:
                _time.sleep(slice_interval_sec)
        if not prices:
            return plan.entry_price
        tot = sum(weights)
        return sum(p * w for p, w in zip(prices, weights)) / tot if tot else prices[-1]

    def _maker_twap_entry(self, plan: TradePlan, side: str, pos_side: str,
                          twap_slices: int, slice_wait_sec: float = 20.0
                          ) -> tuple[float, float]:
        """메이커(post-only) TWAP 진입. (평균체결가, 체결수량) 반환.

        슬라이스마다 최우선 호가에 GTX 지정가를 걸고 slice_wait_sec 대기:
          - 체결되면 다음 슬라이스로
          - 미체결이면 취소 후 다음 슬라이스에서 재호가
        마지막 슬라이스까지 미체결 잔량은 시장가 폴백(진입 기회 놓침 방지).
        수수료: 체결된 지정가 = 메이커, 폴백 = 테이커.
        """
        import time as _time

        n = max(1, twap_slices)
        min_notional = self.binance.min_notional(plan.symbol)
        # 슬라이스가 최소 명목가치 미만이면 분할 수를 줄인다
        while n > 1 and (plan.quantity / n) * plan.entry_price < min_notional:
            n -= 1
        slice_qty = self.binance.amount_to_precision(plan.symbol, plan.quantity / n)
        fills: list[tuple[float, float]] = []  # (price, qty)
        remaining = plan.quantity

        for i in range(n):
            if float(slice_qty) <= 0 or remaining <= 0:
                break
            qty = self.binance.amount_to_precision(plan.symbol, min(slice_qty, remaining))
            if float(qty) <= 0 or float(qty) * plan.entry_price < min_notional:
                break  # 최소 명목가치 미만 슬라이스는 잔량 폴백으로 넘김
            bid, ask = self.binance.best_bid_ask(plan.symbol)
            limit_price = bid if side == "buy" else ask   # 호가에 걸어 메이커 보장
            try:
                order = self.binance.create_post_only_order(
                    plan.symbol, side, qty, limit_price, position_side=pos_side)
            except Exception as e:  # noqa: BLE001
                log.warning("포스트온리 거부(%s) — 이번 슬라이스 시장가 폴백", e)
                mkt = self.binance.create_market_order(plan.symbol, side, qty,
                                                       position_side=pos_side)
                px = float(mkt.get("average") or mkt.get("price") or limit_price)
                fills.append((px, float(qty)))
                remaining -= float(qty)
                continue

            _time.sleep(slice_wait_sec)
            oid = str(order.get("id"))
            status = self.binance.fetch_order(oid, plan.symbol)
            filled_qty = float(status.get("filled") or 0.0)
            if float(qty) - filled_qty > 0:
                self.binance.cancel_order(oid, plan.symbol)
                # 레이스 대비: 취소 직전 체결됐을 수 있으므로 최종 상태 재확인
                try:
                    status = self.binance.fetch_order(oid, plan.symbol)
                    filled_qty = float(status.get("filled") or 0.0)
                except Exception:  # noqa: BLE001
                    pass
            if filled_qty > 0:
                px = float(status.get("average") or limit_price)
                fills.append((px, filled_qty))
                remaining -= filled_qty
            # 미체결분은 remaining 에 남겨 다음 슬라이스/폴백에서 재시도

        # 잔량 시장가 폴백 (최소 명목가치 이상일 때만 — 미만이면 거래소가 거부)
        if remaining > 0:
            qty = self.binance.amount_to_precision(plan.symbol, remaining)
            if float(qty) > 0 and float(qty) * plan.entry_price >= min_notional:
                mkt = self.binance.create_market_order(plan.symbol, side, qty,
                                                       position_side=pos_side)
                px = float(mkt.get("average") or mkt.get("price") or plan.entry_price)
                fills.append((px, float(qty)))
                log.info("메이커 TWAP 잔량 시장가 폴백: %s %s", plan.symbol, qty)
            elif float(qty) > 0:
                log.info("메이커 TWAP 잔량 %s 은 최소 명목가치 미만 — 무시", qty)

        total_qty = sum(q for _, q in fills)
        avg = (sum(p * q for p, q in fills) / total_qty) if total_qty > 0 else plan.entry_price
        return avg, total_qty

    def open_position(self, plan: TradePlan, twap_slices: int = 1,
                      maker_entry: bool = False, place_tp: bool = True,
                      slice_interval_sec: float = 0.0) -> Fill | None:
        side = "buy" if plan.direction is Direction.LONG else "sell"
        self.last_error = ""        # 실패 원인(알림/격리 판단용)
        self.last_error_fatal = False  # 심볼 자체가 문제(재시도 무의미) 여부

        if self.s.trade_mode is TradeMode.DRY_RUN:
            log.info("[DRY_RUN] 진입 → %s", plan.describe())
            return self.paper.fill(plan)

        if self.binance is None:
            log.error("거래소 클라이언트 없음 — 주문 불가")
            return None

        # paper(테스트넷) / live 공통 실주문 경로
        mode = self.s.trade_mode.value
        pos_side = plan.direction.value  # 'long' | 'short'
        try:
            self.binance.set_margin_mode(plan.symbol)
            actual_lev = self.binance.set_leverage(plan.symbol, plan.leverage)
            plan.leverage = actual_lev   # 실제 설정된 레버리지 반영(하향됐을 수 있음)
            close_side = "sell" if plan.direction is Direction.LONG else "buy"
            planned_qty = self.binance.amount_to_precision(plan.symbol, plan.quantity)

            # 분할 진입 전에 SL 을 먼저 예약 — 90초 분할 체결 중에도 급락 보호.
            # (헤지 모드 조건부 스톱은 트리거 시 존재하는 포지션만큼만 청산하므로,
            #  계획 수량으로 미리 걸어두면 부분 체결 상태에서도 안전)
            slice_interval = slice_interval_sec if not maker_entry else 0.0
            if slice_interval > 0:
                try:
                    self.binance.create_stop_order(plan.symbol, close_side, planned_qty,
                                                   plan.stop_price, position_side=pos_side)
                    log.info("[%s] 진입 전 SL 선예약 SL=%.4f", mode.upper(), plan.stop_price)
                except Exception as e:  # noqa: BLE001
                    log.warning("진입 전 SL 예약 실패 %s: %s", plan.symbol, e)

            if maker_entry:
                entry, filled_qty = self._maker_twap_entry(plan, side, pos_side, twap_slices)
                qty = self.binance.amount_to_precision(plan.symbol, filled_qty)
            else:
                qty = planned_qty
                entry = self._market_entry(plan, side, pos_side, twap_slices, slice_interval)
            if float(qty) <= 0:
                log.warning("체결 수량 0 — 진입 실패 %s", plan.symbol)
                return None
            log.info("[%s] 진입 체결 → %s %s @ %.4f qty=%s", mode.upper(),
                     plan.symbol, pos_side, entry, qty)

            # SL 을 선예약 안 했으면 지금 예약. TP 는 옵션.
            try:
                if slice_interval <= 0:
                    self.binance.create_stop_order(plan.symbol, close_side, qty,
                                                   plan.stop_price, position_side=pos_side)
                if place_tp:
                    self.binance.create_take_profit_order(plan.symbol, close_side, qty,
                                                          plan.take_profit,
                                                          position_side=pos_side)
                log.info("[%s] SL=%.4f%s", mode.upper(), plan.stop_price,
                         f" TP={plan.take_profit:.4f}" if place_tp else " (TP 미사용)")
            except Exception as e:  # noqa: BLE001
                log.warning("SL/TP 주문 실패 %s: %s", plan.symbol, e)

            return Fill(plan.symbol, side, float(qty), entry, mode, None)
        except Exception as e:  # noqa: BLE001
            self.last_error = _friendly_error(str(e))
            self.last_error_fatal = _is_fatal_symbol_error(str(e))
            log.error("주문 실패 %s: %s", plan.symbol, e)
            return None
