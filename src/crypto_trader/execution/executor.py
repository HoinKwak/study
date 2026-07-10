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

    def open_position(self, plan: TradePlan) -> Fill | None:
        side = "buy" if plan.direction is Direction.LONG else "sell"

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
            self.binance.set_leverage(plan.symbol, plan.leverage)
            qty = self.binance.amount_to_precision(plan.symbol, plan.quantity)
            order = self.binance.create_market_order(plan.symbol, side, qty, position_side=pos_side)
            entry = float(order.get("average") or order.get("price") or plan.entry_price)
            log.info("[%s] 진입 체결 → %s %s @ %.4f", mode.upper(), plan.symbol, pos_side, entry)

            # 손절/익절 예약 — 포지션 반대 방향으로 청산되도록 positionSide 지정
            close_side = "sell" if plan.direction is Direction.LONG else "buy"
            try:
                self.binance.create_stop_order(plan.symbol, close_side, qty,
                                               plan.stop_price, position_side=pos_side)
                self.binance.create_take_profit_order(plan.symbol, close_side, qty,
                                                      plan.take_profit, position_side=pos_side)
                log.info("[%s] SL=%.4f TP=%.4f 예약", mode.upper(),
                         plan.stop_price, plan.take_profit)
            except Exception as e:  # noqa: BLE001
                log.warning("SL/TP 주문 실패 %s: %s", plan.symbol, e)

            return Fill(plan.symbol, side, float(qty), entry, mode, str(order.get("id")))
        except Exception as e:  # noqa: BLE001
            log.error("주문 실패 %s: %s", plan.symbol, e)
            return None
