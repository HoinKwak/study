"""리스크 관리: 포지션 사이징, 손절/익절, 레버리지·손실 한도.

핵심 원칙: "1회 매매에서 잃을 수 있는 금액 = 계좌의 risk_per_trade_pct%".
손절 거리(ATR 기반)로부터 수량을 역산하므로, 변동성이 큰 종목일수록 수량이 작아진다.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..config import Settings
from ..signals.base import Direction
from ..utils import get_logger

log = get_logger("risk")


@dataclass
class TradePlan:
    symbol: str
    direction: Direction
    entry_price: float
    stop_price: float
    take_profit: float
    quantity: float
    leverage: int
    risk_amount: float  # 이 거래에서 감수하는 최대 손실(USDT)
    notional: float     # 명목 가치(entry * qty)

    def describe(self) -> str:
        return (
            f"{self.symbol} {self.direction.value.upper()} "
            f"qty={self.quantity} entry={self.entry_price:.4f} "
            f"SL={self.stop_price:.4f} TP={self.take_profit:.4f} "
            f"lev=x{self.leverage} risk={self.risk_amount:.2f}USDT notional={self.notional:.2f}"
        )


class RiskManager:
    def __init__(self, settings: Settings,
                 atr_stop_mult: float | None = None,
                 reward_risk_ratio: float | None = None):
        self.s = settings
        self.atr_stop_mult = atr_stop_mult if atr_stop_mult is not None else settings.atr_stop_mult
        self.reward_risk_ratio = (reward_risk_ratio if reward_risk_ratio is not None
                                  else settings.reward_risk_ratio)
        self._day_start_equity: float | None = None
        self._realized_pnl_today: float = 0.0

    # ----------------------------------------------------- 일일 손실 한도

    def start_day(self, equity: float) -> None:
        self._day_start_equity = equity
        self._realized_pnl_today = 0.0

    def register_realized_pnl(self, pnl: float) -> None:
        self._realized_pnl_today += pnl

    def daily_loss_exceeded(self) -> bool:
        if self._day_start_equity is None or self._day_start_equity <= 0:
            return False
        loss_pct = -self._realized_pnl_today / self._day_start_equity * 100.0
        return loss_pct >= self.s.daily_max_loss_pct

    # --------------------------------------------------------- 진입 게이트

    def can_open(self, open_positions: int) -> tuple[bool, str]:
        if self.daily_loss_exceeded():
            return False, "일일 손실 한도 도달"
        if open_positions >= self.s.max_open_positions:
            return False, f"최대 포지션 수 도달 ({open_positions}/{self.s.max_open_positions})"
        return True, "ok"

    # ------------------------------------------------------- 포지션 사이징

    def build_plan(self, symbol: str, direction: Direction, entry_price: float,
                   atr_value: float, equity: float) -> TradePlan | None:
        """ATR 기반 손절 거리로 리스크 대비 수량 산정."""
        if direction is Direction.FLAT or entry_price <= 0 or atr_value <= 0 or equity <= 0:
            return None

        stop_distance = self.atr_stop_mult * atr_value
        if stop_distance <= 0:
            return None

        risk_amount = equity * (self.s.risk_per_trade_pct / 100.0)
        quantity = risk_amount / stop_distance
        if quantity <= 0:
            return None

        if direction is Direction.LONG:
            stop_price = entry_price - stop_distance
            take_profit = entry_price + stop_distance * self.reward_risk_ratio
        else:  # SHORT
            stop_price = entry_price + stop_distance
            take_profit = entry_price - stop_distance * self.reward_risk_ratio

        notional = entry_price * quantity

        # 레버리지 상한: 명목가치가 (증거금 × max_leverage) 넘지 않게 클램프
        max_notional = equity * self.s.max_leverage
        if notional > max_notional:
            scale = max_notional / notional
            quantity *= scale
            notional *= scale
            risk_amount *= scale
            log.info("레버리지 상한으로 수량 축소 %s (scale=%.3f)", symbol, scale)

        leverage = min(self.s.max_leverage, max(1, round(notional / equity))) if equity else 1

        return TradePlan(
            symbol=symbol,
            direction=direction,
            entry_price=entry_price,
            stop_price=stop_price,
            take_profit=take_profit,
            quantity=quantity,
            leverage=leverage,
            risk_amount=risk_amount,
            notional=notional,
        )

    def build_plan_with_stop(self, symbol: str, direction: Direction, entry_price: float,
                             stop_price: float, take_profit: float,
                             equity: float) -> TradePlan | None:
        """전략이 SL/TP 를 직접 제시한 경우(예: 단타), 손절 거리로 수량 산정."""
        if direction is Direction.FLAT or entry_price <= 0 or equity <= 0:
            return None
        stop_distance = abs(entry_price - stop_price)
        if stop_distance <= 0:
            return None

        risk_amount = equity * (self.s.risk_per_trade_pct / 100.0)
        quantity = risk_amount / stop_distance
        if quantity <= 0:
            return None

        notional = entry_price * quantity
        max_notional = equity * self.s.max_leverage
        if notional > max_notional:
            scale = max_notional / notional
            quantity *= scale
            notional *= scale
            risk_amount *= scale

        leverage = min(self.s.max_leverage, max(1, round(notional / equity))) if equity else 1
        return TradePlan(
            symbol=symbol, direction=direction, entry_price=entry_price,
            stop_price=stop_price, take_profit=take_profit, quantity=quantity,
            leverage=leverage, risk_amount=risk_amount, notional=notional,
        )
