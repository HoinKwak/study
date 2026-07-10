"""메인 오케스트레이션 엔진.

주기마다:
  0) 기존 포지션 청산 조건 점검(SL/TP) 및 저널 반영
  1) 각 심볼 OHLCV + 파생 데이터 수집
  2) 기술/파생 시그널 계산 → 가중 합산
  3) 진입 방향 결정 → 리스크 매니저로 매매 계획 수립
  4) 실행(dry_run/paper/live) + 저널 기록 + 알림
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
from ..signals import DerivativesSignals, SignalAggregator, TechnicalSignals
from ..signals import indicators as ind
from ..signals.base import Direction
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

        # 시그널
        self.tech = TechnicalSignals()
        self.deriv = DerivativesSignals()
        self.aggregator = SignalAggregator(entry_threshold=settings.entry_score_threshold)

        # 리스크 / 실행 / 모니터링
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
                # 키 없이 공개 OHLCV — ccxt 익명 인스턴스로 폴백
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

    # ------------------------------------------------- 청산 조건 점검(SL/TP)

    def _check_exits(self) -> None:
        """dry_run: 페이퍼 포지션의 SL/TP 도달 여부를 현재가로 점검·청산.
        paper/live: 거래소에서 사라진 포지션을 청산으로 간주해 저널 반영."""
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
            if not hit:
                continue
            pnl = self._pnl(direction, pos["entry"], exit_price, pos["qty"])
            self.paper.equity += pnl
            del self.paper.positions[symbol]
            self.risk.register_realized_pnl(pnl)
            self.journal.record_close(symbol, exit_price, _now_iso(), pnl, reason)
            self.notifier.trade(
                f"{symbol} {direction.value.upper()} 청산 ({reason})\n"
                f"진입 {pos['entry']:.4f} → 청산 {exit_price:.4f}\n"
                f"손익 {pnl:+.2f} USDT | 잔고 {self.paper.equity:.2f}",
                title="📕 포지션 청산",
            )

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
            # 거래소에서 사라짐 → 청산됨. 현재가로 근사 손익 기록 후 잔여 주문 정리.
            try:
                price = self.binance.last_price(rec.symbol)
            except Exception:  # noqa: BLE001
                price = rec.entry_price
            pnl = self._pnl(Direction(rec.direction), rec.entry_price, price, rec.quantity)
            self.journal.record_close(rec.symbol, price, _now_iso(), pnl, "exchange_closed")
            self.binance.cancel_all_orders(rec.symbol)
            self.notifier.trade(
                f"{rec.symbol} {rec.direction.upper()} 청산 감지\n"
                f"진입 {rec.entry_price:.4f} → 근사청산 {price:.4f}\n"
                f"근사손익 {pnl:+.2f} USDT",
                title="📕 포지션 청산(리컨실)",
            )

    @staticmethod
    def _exit_hit(direction: Direction, price: float, stop: float, tp: float
                  ) -> tuple[bool, float, str]:
        if direction is Direction.LONG:
            if price <= stop:
                return True, stop, "stop_loss"
            if price >= tp:
                return True, tp, "take_profit"
        else:  # SHORT
            if price >= stop:
                return True, stop, "stop_loss"
            if price <= tp:
                return True, tp, "take_profit"
        return False, 0.0, ""

    @staticmethod
    def _pnl(direction: Direction, entry: float, exit_price: float, qty: float) -> float:
        if direction is Direction.LONG:
            return (exit_price - entry) * qty
        return (entry - exit_price) * qty

    # ------------------------------------------------------- 심볼 1회 평가

    def evaluate_symbol(self, symbol: str) -> None:
        df = self._fetch_ohlcv_df(symbol)
        if df is None or len(df) < 30:
            log.info("%s: 데이터 부족, 스킵", symbol)
            return

        tech_sig = self.tech.compute(df)
        snap = self.deriv_data.snapshot(symbol)
        deriv_sig = self.deriv.compute(snap)

        agg = self.aggregator.aggregate(symbol, [tech_sig, deriv_sig])
        log.info(agg.summary())

        if agg.direction is Direction.FLAT:
            return

        # 이미 같은 심볼 포지션 보유 시 중복 진입 방지(간단 버전)
        if symbol in self.paper.positions and self.s.trade_mode is TradeMode.DRY_RUN:
            log.info("%s: 기존 포지션 보유 중, 신규 진입 스킵", symbol)
            return

        ok, reason = self.risk.can_open(self._open_position_count())
        if not ok:
            self.notifier.warn(f"{symbol}: 진입 차단 — {reason}")
            return

        entry_price = float(df["close"].iloc[-1])
        atr_value = float(ind.atr(df).iloc[-1])
        equity = self._current_equity()

        plan = self.risk.build_plan(symbol, agg.direction, entry_price, atr_value, equity)
        if plan is None:
            log.info("%s: 매매 계획 수립 불가", symbol)
            return

        fill = self.executor.open_position(plan)
        if fill is None:
            self.notifier.error(f"{symbol}: 주문 실패")
            return

        # 저널 기록 + 알림
        self.journal.record_open(TradeRecord(
            symbol=symbol,
            direction=plan.direction.value,
            entry_price=fill.price,
            quantity=fill.quantity,
            opened_at=_now_iso(),
            mode=self.s.trade_mode.value,
            stop_price=plan.stop_price,
            take_profit=plan.take_profit,
            order_id=fill.order_id,
        ))
        self.notifier.trade(
            f"{symbol} {plan.direction.value.upper()} 진입 (score={agg.score:+.2f})\n"
            f"진입 {fill.price:.4f} | SL {plan.stop_price:.4f} | TP {plan.take_profit:.4f}\n"
            f"수량 {fill.quantity} | 리스크 {plan.risk_amount:.2f} USDT",
            title="📗 신규 진입",
        )

    # ------------------------------------------------------------- 루프

    def run_once(self) -> None:
        if not self._started:
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
