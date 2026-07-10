"""메인 오케스트레이션 엔진.

주기마다:
  0) 기존 포지션 SL/TP 청산 점검 및 저널 반영
  1) 각 심볼 OHLCV + 파생 데이터 수집
  2) Strategy.decide → 레짐 인지 시그널 합산 → 진입/청산/관망 결정
  3) 실행(dry_run/paper/live) + 저널 기록 + 알림
"""
from __future__ import annotations

import time
from datetime import datetime, timezone

import pandas as pd

from ..config import Settings, TradeMode
from ..connectors import BinanceClient, BinanceDerivativesData
from ..data import ohlcv_to_df
from ..execution import Executor, PaperBroker
from ..monitoring import Notifier, TradeJournal, TradeRecord
from ..risk import RiskManager
from ..signals import indicators as ind
from ..signals.base import Direction
from ..strategy import Action, Strategy
from ..utils import get_logger

log = get_logger("engine")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class TradingEngine:
    def __init__(self, settings: Settings):
        self.s = settings

        # 커넥터: dry_run 이고 키가 없으면 거래소 클라이언트 없이도 동작(공개 데이터만)
        self.binance: BinanceClient | None = None
        if settings.has_binance_keys or settings.trade_mode is not TradeMode.DRY_RUN:
            self.binance = BinanceClient(settings)
        self.deriv_data = BinanceDerivativesData()

        # 전략 / 리스크 / 실행 / 모니터링
        self.strategy = Strategy(settings)
        self.risk = RiskManager(settings)
        self.paper = PaperBroker()
        self.executor = Executor(settings, self.binance, self.paper)
        self.notifier = Notifier(settings)
        self.journal = TradeJournal(settings.state_dir)

        self._started = False

    # -------------------------------------------------------- 데이터 수집

    def _fetch_ohlcv_df(self, symbol: str) -> pd.DataFrame | None:
        try:
            if self.binance is not None:
                raw = self.binance.fetch_ohlcv(symbol, self.s.timeframe, limit=200)
            else:
                import ccxt
                ex = ccxt.binance({"options": {"defaultType": "future"}})
                raw = ex.fetch_ohlcv(symbol, timeframe=self.s.timeframe, limit=200)
            return ohlcv_to_df(raw)
        except Exception as e:  # noqa: BLE001
            log.warning("OHLCV 수집 실패 %s: %s", symbol, e)
            return None

    def _last_price(self, symbol: str, df: pd.DataFrame | None = None) -> float:
        if df is not None and len(df):
            return float(df["close"].iloc[-1])
        if self.binance is not None:
            return self.binance.last_price(symbol)
        raise RuntimeError(f"가격 조회 불가: {symbol}")

    def _current_equity(self) -> float:
        if self.binance is not None and self.s.trade_mode is not TradeMode.DRY_RUN:
            try:
                return self.binance.fetch_balance_usdt()
            except Exception as e:  # noqa: BLE001
                log.warning("잔고 조회 실패, 페이퍼 잔고 사용: %s", e)
        return self.paper.equity

    def _open_position_count(self) -> int:
        if self.binance is not None and self.s.trade_mode is not TradeMode.DRY_RUN:
            try:
                return len(self.binance.fetch_positions())
            except Exception:  # noqa: BLE001
                pass
        return len(self.paper.positions)

    def _current_direction(self, symbol: str) -> Direction | None:
        """해당 심볼의 현재 포지션 방향(없으면 None)."""
        if self.s.trade_mode is TradeMode.DRY_RUN:
            pos = self.paper.positions.get(symbol)
            return Direction(pos["side"]) if pos else None
        if self.binance is None:
            return None
        canonical = self.binance.resolve_symbol(symbol)
        for p in self.binance.fetch_positions(symbol):
            if p.get("symbol") == canonical and float(p.get("contracts") or 0) != 0:
                return Direction.LONG if p.get("side") == "long" else Direction.SHORT
        return None

    # --------------------------------------------------------- 청산 처리

    @staticmethod
    def _pnl(direction: Direction, entry: float, exit_price: float, qty: float) -> float:
        if direction is Direction.LONG:
            return (exit_price - entry) * qty
        return (entry - exit_price) * qty

    def _finalize_close(self, symbol: str, direction: Direction, entry: float, qty: float,
                        exit_price: float, reason: str, title: str) -> float:
        pnl = self._pnl(direction, entry, exit_price, qty)
        if self.s.trade_mode is TradeMode.DRY_RUN:
            self.paper.equity += pnl
            self.paper.positions.pop(symbol, None)
        self.risk.register_realized_pnl(pnl)
        self.journal.record_close(symbol, exit_price, _now_iso(), pnl, reason)
        bal = f" | 잔고 {self.paper.equity:.2f}" if self.s.trade_mode is TradeMode.DRY_RUN else ""
        self.notifier.trade(
            f"{symbol} {direction.value.upper()} 청산 ({reason})\n"
            f"진입 {entry:.4f} → 청산 {exit_price:.4f}\n손익 {pnl:+.2f} USDT{bal}",
            title=title,
        )
        return pnl

    def _check_exits(self) -> None:
        """dry_run: 페이퍼 포지션 SL/TP 점검. paper/live: 거래소 포지션 리컨실."""
        if self.s.trade_mode is TradeMode.DRY_RUN:
            self._check_exits_paper()
        else:
            self._reconcile_live_exits()

    def _check_exits_paper(self) -> None:
        for symbol in list(self.paper.positions.keys()):
            pos = self.paper.positions[symbol]
            try:
                price = self._last_price(symbol)
            except Exception:  # noqa: BLE001
                continue
            direction = Direction(pos["side"])
            hit, exit_price, reason = self._exit_hit(direction, price, pos["stop"], pos["tp"])
            if hit:
                self._finalize_close(symbol, direction, pos["entry"], pos["qty"],
                                     exit_price, reason, "📕 포지션 청산")

    def _reconcile_live_exits(self) -> None:
        if self.binance is None:
            return
        try:
            live = {p.get("symbol") for p in self.binance.fetch_positions()}
        except Exception as e:  # noqa: BLE001
            log.warning("포지션 리컨실 실패: %s", e)
            return
        for rec in self.journal.open_trades():
            canonical = self.binance.resolve_symbol(rec.symbol)
            if canonical in live:
                continue  # 아직 보유 중
            try:
                price = self.binance.last_price(rec.symbol)
            except Exception:  # noqa: BLE001
                price = rec.entry_price
            self.binance.cancel_all_orders(rec.symbol)
            self._finalize_close(rec.symbol, Direction(rec.direction), rec.entry_price,
                                 rec.quantity, price, "exchange_closed", "📕 포지션 청산(리컨실)")

    @staticmethod
    def _exit_hit(direction: Direction, price: float, stop: float, tp: float
                  ) -> tuple[bool, float, str]:
        if direction is Direction.LONG:
            if price <= stop:
                return True, stop, "stop_loss"
            if price >= tp:
                return True, tp, "take_profit"
        else:
            if price >= stop:
                return True, stop, "stop_loss"
            if price <= tp:
                return True, tp, "take_profit"
        return False, 0.0, ""

    def _close_by_signal(self, symbol: str, direction: Direction) -> None:
        """시그널 반전에 의한 조기 청산."""
        price = self._last_price(symbol)
        if self.s.trade_mode is TradeMode.DRY_RUN:
            pos = self.paper.positions.get(symbol)
            if not pos:
                return
            self._finalize_close(symbol, direction, pos["entry"], pos["qty"],
                                 price, "signal_flip", "📕 반전 청산")
        else:
            if self.binance is None:
                return
            rec = next((t for t in self.journal.open_trades() if t.symbol == symbol), None)
            self.binance.close_position(symbol, direction.value)
            self.binance.cancel_all_orders(symbol)
            entry = rec.entry_price if rec else price
            qty = rec.quantity if rec else 0.0
            self._finalize_close(symbol, direction, entry, qty, price,
                                 "signal_flip", "📕 반전 청산")

    # ------------------------------------------------------- 심볼 1회 평가

    def evaluate_symbol(self, symbol: str) -> None:
        df = self._fetch_ohlcv_df(symbol)
        if df is None or len(df) < 30:
            log.info("%s: 데이터 부족, 스킵", symbol)
            return

        current_dir = self._current_direction(symbol)
        snap = self.deriv_data.snapshot(symbol)
        decision = self.strategy.decide(symbol, df, snap, current_dir)
        log.info("%s %s", symbol, decision.summary())

        if decision.action is Action.HOLD:
            return

        if decision.action is Action.CLOSE and current_dir is not None:
            self._close_by_signal(symbol, current_dir)
            return

        if decision.action in (Action.OPEN_LONG, Action.OPEN_SHORT):
            self._open(symbol, decision, df)

    def _open(self, symbol: str, decision, df: pd.DataFrame) -> None:
        ok, reason = self.risk.can_open(self._open_position_count())
        if not ok:
            self.notifier.warn(f"{symbol}: 진입 차단 — {reason}")
            return

        entry_price = float(df["close"].iloc[-1])
        atr_value = float(ind.atr(df).iloc[-1])
        equity = self._current_equity()

        plan = self.risk.build_plan(symbol, decision.direction, entry_price, atr_value, equity)
        if plan is None:
            log.info("%s: 매매 계획 수립 불가", symbol)
            return

        fill = self.executor.open_position(plan)
        if fill is None:
            self.notifier.error(f"{symbol}: 주문 실패")
            return

        self.journal.record_open(TradeRecord(
            symbol=symbol, direction=plan.direction.value, entry_price=fill.price,
            quantity=fill.quantity, opened_at=_now_iso(), mode=self.s.trade_mode.value,
            stop_price=plan.stop_price, take_profit=plan.take_profit, order_id=fill.order_id,
        ))
        self.notifier.trade(
            f"{symbol} {plan.direction.value.upper()} 진입 "
            f"(score={decision.score:+.2f}, {decision.regime.value})\n"
            f"진입 {fill.price:.4f} | SL {plan.stop_price:.4f} | TP {plan.take_profit:.4f}\n"
            f"수량 {fill.quantity} | 리스크 {plan.risk_amount:.2f} USDT",
            title="📗 신규 진입",
        )

    # ------------------------------------------------------------- 루프

    def run_once(self) -> None:
        if not self._started:
            if self.binance is not None and self.s.trade_mode is not TradeMode.DRY_RUN:
                self.binance.ensure_position_mode()
            equity = self._current_equity()
            self.risk.start_day(equity)
            self.notifier.info(
                f"엔진 시작 — mode={self.s.trade_mode.value} "
                f"symbols={','.join(self.s.symbols)} equity={equity:.2f}",
                title="🤖 crypto-trader",
            )
            self._started = True

        self._check_exits()
        for symbol in self.s.symbols:
            self.evaluate_symbol(symbol)

    def run_forever(self) -> None:
        log.info("트레이딩 엔진 시작 — mode=%s symbols=%s tf=%s",
                 self.s.trade_mode.value, self.s.symbols, self.s.timeframe)
        while True:
            try:
                self.run_once()
            except KeyboardInterrupt:
                log.info("사용자 중단 — 종료")
                break
            except Exception as e:  # noqa: BLE001
                log.exception("루프 오류: %s", e)
                self.notifier.error(f"루프 오류: {e}")
            time.sleep(self.s.loop_interval_sec)
