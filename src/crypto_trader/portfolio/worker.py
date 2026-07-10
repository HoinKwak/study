"""슬리브 워커 — 한 슬리브의 심볼들을 자기 타임프레임/전략/자본으로 평가·실행.

전략 종류:
  - 'regime' : 레짐 인지 멀티 시그널 Strategy (중기/중장기 기본)
  - 'scalp'  : 볼린저+거래량+OI 단타 ScalpStrategy (TWAP 진입)

포지션은 저널의 sleeve 태그로 슬리브별로 구분·추적한다.
청산 시 해당 슬리브 거래의 수량만큼만 닫는다(부분 청산).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

import pandas as pd

from ..config import Settings, TradeMode
from ..connectors import BinanceClient, BinanceDerivativesData
from ..data import ohlcv_to_df
from ..execution import Executor
from ..monitoring import Notifier, TradeJournal, TradeRecord
from ..risk import RiskManager
from ..signals import indicators as ind
from ..signals.base import Direction
from ..strategy import Action, Strategy
from ..strategy.regime import detect_regime
from ..strategy.scalp import ScalpStrategy
from ..utils import get_logger
from .sleeve import Sleeve

log = get_logger("sleeve")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class SleeveWorker:
    def __init__(self, sleeve: Sleeve, settings: Settings,
                 binance: BinanceClient | None, deriv_data: BinanceDerivativesData,
                 executor: Executor, journal: TradeJournal, notifier: Notifier,
                 realize_cb: Callable[[float], None] | None = None):
        self.sleeve = sleeve
        self.s = settings
        self.binance = binance
        self.deriv_data = deriv_data
        self.executor = executor
        self.journal = journal
        self.notifier = notifier
        self.realize_cb = realize_cb or (lambda pnl: None)
        self.risk = RiskManager(settings)

        if sleeve.strategy_kind == "scalp":
            self.strategy: Strategy | ScalpStrategy = ScalpStrategy(settings)
        else:
            self.strategy = Strategy(settings)

        self._last_oi: dict[str, float] = {}
        self._last_eval_ts: float = 0.0

    # ------------------------------------------------------------- 데이터

    def _fetch_df(self, symbol: str, timeframe: str, limit: int = 200) -> pd.DataFrame | None:
        try:
            if self.binance is not None:
                raw = self.binance.fetch_ohlcv(symbol, timeframe, limit=limit)
            else:
                import ccxt
                ex = ccxt.binance({"options": {"defaultType": "future"}})
                raw = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            return ohlcv_to_df(raw)
        except Exception as e:  # noqa: BLE001
            log.warning("[%s] OHLCV 실패 %s %s: %s", self.sleeve.name, symbol, timeframe, e)
            return None

    def _oi_delta(self, symbol: str) -> float | None:
        """실시간 OI 스냅샷을 직전 값과 비교한 증감(없으면 None)."""
        if self.binance is None:
            return None
        oi = self.binance.fetch_open_interest(symbol)
        if oi is None:
            return None
        prev = self._last_oi.get(symbol)
        self._last_oi[symbol] = oi
        return None if prev is None else (oi - prev)

    def _sleeve_trade(self, symbol: str) -> TradeRecord | None:
        for t in self.journal.open_trades():
            if t.sleeve == self.sleeve.name and t.symbol == symbol:
                return t
        return None

    def _current_dir(self, symbol: str) -> Direction | None:
        t = self._sleeve_trade(symbol)
        return Direction(t.direction) if t else None

    # ------------------------------------------------------------- 청산

    @staticmethod
    def _pnl(direction: Direction, entry: float, exit_price: float, qty: float) -> float:
        return (exit_price - entry) * qty if direction is Direction.LONG else (entry - exit_price) * qty

    def _close_trade(self, rec: TradeRecord, exit_price: float, reason: str) -> None:
        direction = Direction(rec.direction)
        pnl = self._pnl(direction, rec.entry_price, exit_price, rec.quantity)
        if self.s.trade_mode is not TradeMode.DRY_RUN and self.binance is not None:
            self.binance.close_quantity(rec.symbol, rec.direction, rec.quantity)
            self.binance.cancel_all_orders(rec.symbol)  # 잔여 SL/TP 정리
        self.risk.register_realized_pnl(pnl)
        self.realize_cb(pnl)
        self.journal.record_close(rec.symbol, exit_price, _now_iso(), pnl, reason,
                                  sleeve=self.sleeve.name, direction=rec.direction)
        self.notifier.trade(
            f"[{self.sleeve.name}] {rec.symbol} {rec.direction.upper()} 청산 ({reason})\n"
            f"진입 {rec.entry_price:.4f} → {exit_price:.4f} | 손익 {pnl:+.2f} USDT "
            f"| 보유 {rec.holding_human(_now_iso())}",
            title="📕 청산",
        )

    def _check_sl_tp(self, symbol: str, price: float) -> None:
        """dry_run: 슬리브 보유분의 SL/TP 도달 점검."""
        rec = self._sleeve_trade(symbol)
        if not rec:
            return
        direction = Direction(rec.direction)
        if direction is Direction.LONG:
            if price <= rec.stop_price:
                self._close_trade(rec, rec.stop_price, "stop_loss")
            elif price >= rec.take_profit:
                self._close_trade(rec, rec.take_profit, "take_profit")
        else:
            if price >= rec.stop_price:
                self._close_trade(rec, rec.stop_price, "stop_loss")
            elif price <= rec.take_profit:
                self._close_trade(rec, rec.take_profit, "take_profit")

    # ------------------------------------------------------------- 평가

    def evaluate(self, total_equity: float) -> None:
        allocated = self.sleeve.allocated_equity(total_equity)
        for symbol in self.sleeve.symbols:
            try:
                self._evaluate_symbol(symbol, allocated)
            except Exception as e:  # noqa: BLE001
                log.exception("[%s] %s 평가 오류: %s", self.sleeve.name, symbol, e)

    def _evaluate_symbol(self, symbol: str, allocated_equity: float) -> None:
        df = self._fetch_df(symbol, self.sleeve.signal_tf)
        if df is None or len(df) < 30:
            return
        price = float(df["close"].iloc[-1])

        # dry_run 은 봉 종가 기준 SL/TP 시뮬레이션
        if self.s.trade_mode is TradeMode.DRY_RUN:
            self._check_sl_tp(symbol, price)

        current_dir = self._current_dir(symbol)
        confirm_df = self._fetch_df(symbol, self.sleeve.confirm_tf, limit=100)
        confirm_regime = detect_regime(confirm_df)[0] if confirm_df is not None else None

        if self.sleeve.strategy_kind == "scalp":
            oi_delta = self._oi_delta(symbol)
            decision = self.strategy.decide(symbol, df, oi_delta=oi_delta,
                                            current_direction=current_dir,
                                            confirm_regime=confirm_regime)
            self._act_scalp(symbol, df, decision, allocated_equity, current_dir)
        else:
            snap = self.deriv_data.snapshot(symbol)
            decision = self.strategy.decide(symbol, df, snap, current_dir)
            self._act_regime(symbol, df, decision, allocated_equity, current_dir)

    # ------------------------------------------------------------- 실행

    def _open_common(self, plan, symbol: str, direction: Direction, price: float,
                     reason: str) -> None:
        ok, why = self.risk.can_open(len([t for t in self.journal.open_trades()
                                          if t.sleeve == self.sleeve.name]))
        if not ok:
            self.notifier.warn(f"[{self.sleeve.name}] {symbol}: 진입 차단 — {why}")
            return
        if plan is None:
            return

        if self.s.trade_mode is TradeMode.DRY_RUN:
            fill_price, qty, oid = price, plan.quantity, None
        else:
            fill = self.executor.open_position(plan, twap_slices=self.sleeve.twap_slices)
            if fill is None:
                self.notifier.error(f"[{self.sleeve.name}] {symbol}: 주문 실패")
                return
            fill_price, qty, oid = fill.price, fill.quantity, fill.order_id

        self.journal.record_open(TradeRecord(
            symbol=symbol, direction=direction.value, entry_price=fill_price, quantity=qty,
            opened_at=_now_iso(), mode=self.s.trade_mode.value, stop_price=plan.stop_price,
            take_profit=plan.take_profit, order_id=oid, sleeve=self.sleeve.name,
        ))
        self.notifier.trade(
            f"[{self.sleeve.name}] {symbol} {direction.value.upper()} 진입 ({reason})\n"
            f"진입 {fill_price:.4f} | SL {plan.stop_price:.4f} | TP {plan.take_profit:.4f}\n"
            f"수량 {qty} | 배정자본 {allocated_str(self)}",
            title="📗 진입",
        )

    def _act_regime(self, symbol, df, decision, equity, current_dir) -> None:
        if decision.action is Action.CLOSE and current_dir is not None:
            rec = self._sleeve_trade(symbol)
            if rec:
                self._close_trade(rec, float(df["close"].iloc[-1]), "signal_flip")
            return
        if decision.action in (Action.OPEN_LONG, Action.OPEN_SHORT):
            price = float(df["close"].iloc[-1])
            atr_value = float(ind.atr(df).iloc[-1])
            plan = self.risk.build_plan(symbol, decision.direction, price, atr_value, equity)
            self._open_common(plan, symbol, decision.direction, price, decision.regime.value)

    def _act_scalp(self, symbol, df, decision, equity, current_dir) -> None:
        if decision.action is Action.CLOSE and current_dir is not None:
            rec = self._sleeve_trade(symbol)
            if rec:
                self._close_trade(rec, float(df["close"].iloc[-1]), decision.reason or "scalp_exit")
            return
        if decision.action in (Action.OPEN_LONG, Action.OPEN_SHORT):
            price = float(df["close"].iloc[-1])
            plan = self.risk.build_plan_with_stop(symbol, decision.direction, price,
                                                  decision.stop_price, decision.take_profit, equity)
            self._open_common(plan, symbol, decision.direction, price, "scalp")


def allocated_str(worker: SleeveWorker) -> str:
    return f"{worker.sleeve.allocation:.0%}"
