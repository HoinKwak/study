"""슬리브 워커 — 한 슬리브의 심볼들을 자기 타임프레임/전략/자본으로 평가·실행.

전략 종류:
  - 'regime' : 레짐 인지 멀티 시그널 Strategy (중기/중장기 기본)
  - 'scalp'  : 볼린저+거래량+OI 단타 ScalpStrategy (TWAP 진입)

포지션은 저널의 sleeve 태그로 슬리브별로 구분·추적한다.
청산 시 해당 슬리브 거래의 수량만큼만 닫는다(부분 청산).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import pandas as pd

from ..config import Settings, TradeMode
from ..connectors import BinanceClient, BinanceDerivativesData
from ..data import ohlcv_to_df
from ..execution import Executor
from ..monitoring import Notifier, TradeJournal, TradeRecord
from ..risk import RiskManager, TradePlan
from ..signals import indicators as ind
from ..signals.base import Direction
from ..strategy import Action, MidStrategy, Strategy
from ..strategy.regime import detect_regime
from ..strategy.scalp import ScalpStrategy
from ..strategy.swing import SwingDecision, SwingPosition, SwingStrategy
from ..utils import get_logger
from .sleeve import Sleeve

log = get_logger("sleeve")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class SleeveWorker:
    def __init__(self, sleeve: Sleeve, settings: Settings,
                 binance: BinanceClient | None, deriv_data: BinanceDerivativesData,
                 executor: Executor, journal: TradeJournal, notifier: Notifier,
                 realize_cb: Callable[[float], None] | None = None,
                 equity_provider: Callable[[], float] | None = None,
                 start_equity_provider: Callable[[], float] | None = None):
        self.sleeve = sleeve
        self.s = settings
        self.binance = binance
        self.deriv_data = deriv_data
        self.executor = executor
        self.journal = journal
        self.notifier = notifier
        self.realize_cb = realize_cb or (lambda pnl: None)
        self.equity_provider = equity_provider          # 현재 포트폴리오 총자본
        self.start_equity_provider = start_equity_provider  # 시작 자본(누적 수익률 기준)
        self.risk = RiskManager(settings, max_leverage=sleeve.leverage)
        self._account_equity: float | None = None
        self._quarantine_path = Path(settings.state_dir) / "quarantine.json"
        self._quarantined: dict[str, str] = self._load_quarantine()

        if sleeve.strategy_kind == "scalp":
            self.strategy = ScalpStrategy(settings)
        elif sleeve.strategy_kind == "mid":
            self.strategy = MidStrategy(settings)
        elif sleeve.strategy_kind == "swing":
            self.strategy = SwingStrategy(settings)
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

    @staticmethod
    def _trade_return_pct(rec: TradeRecord, pnl: float) -> float:
        """이번 거래 손익률(명목가치 대비, 즉 가격 변동률)."""
        notional = rec.entry_price * rec.quantity
        return pnl / notional * 100.0 if notional > 0 else 0.0

    def _portfolio_line(self) -> str:
        """청산 알림에 붙일 포트폴리오 잔고·누적 수익률 줄."""
        if self.equity_provider is None:
            return ""
        try:
            cur = self.equity_provider()
        except Exception:  # noqa: BLE001
            return ""
        start = None
        if self.start_equity_provider is not None:
            try:
                start = self.start_equity_provider()
            except Exception:  # noqa: BLE001
                start = None
        line = f"\n💰 포트폴리오 {cur:,.2f} USDT"
        if start and start > 0:
            line += f" (누적 {(cur / start - 1) * 100:+.2f}%)"
        return line

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
        ret_pct = self._trade_return_pct(rec, pnl)
        self.notifier.trade(
            f"[{self.sleeve.name}] {rec.symbol} {rec.direction.upper()} 청산 ({reason})\n"
            f"진입 {rec.entry_price:.4f} → {exit_price:.4f} | 보유 {rec.holding_human(_now_iso())}\n"
            f"손익 {pnl:+.2f} USDT ({ret_pct:+.2f}%)"
            f"{self._portfolio_line()}",
            title="📕 청산",
        )

    # ------------------------------------------------------- 심볼 격리

    def _load_quarantine(self) -> dict[str, str]:
        try:
            if self._quarantine_path.exists():
                return json.loads(self._quarantine_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass
        return {}

    def _quarantine(self, symbol: str, reason: str) -> None:
        """주문 불가 심볼을 영구 제외(상태파일 영속화). 이후 평가에서 스킵."""
        self._quarantined[symbol] = reason
        try:
            self._quarantine_path.parent.mkdir(parents=True, exist_ok=True)
            self._quarantine_path.write_text(
                json.dumps(self._quarantined, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
        log.warning("[%s] %s 격리(유니버스 제외): %s", self.sleeve.name, symbol, reason)

    def _check_sl_tp(self, symbol: str, price: float) -> None:
        """dry_run: 슬리브 보유분의 SL/TP 도달 점검.

        단타(momentum 청산 모드)는 고정 TP 를 쓰지 않으므로 SL 만 점검한다.
        """
        rec = self._sleeve_trade(symbol)
        if not rec:
            return
        use_tp = not (self.sleeve.strategy_kind == "scalp" and rec.signal_high)
        direction = Direction(rec.direction)
        if direction is Direction.LONG:
            if price <= rec.stop_price:
                self._close_trade(rec, rec.stop_price, "stop_loss")
            elif use_tp and price >= rec.take_profit:
                self._close_trade(rec, rec.take_profit, "take_profit")
        else:
            if price >= rec.stop_price:
                self._close_trade(rec, rec.stop_price, "stop_loss")
            elif use_tp and price <= rec.take_profit:
                self._close_trade(rec, rec.take_profit, "take_profit")

    # ------------------------------------------------------------- 평가

    def evaluate(self, total_equity: float) -> None:
        allocated = self.sleeve.allocated_equity(total_equity)
        self._account_equity = total_equity   # 포지션당 명목 상한 계산 기준(계좌 총자본)
        for symbol in self.sleeve.symbols:
            if symbol in self._quarantined:
                continue  # 주문 불가로 격리된 심볼 스킵
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
        elif self.sleeve.strategy_kind == "mid":
            decision = self.strategy.decide(symbol, df, confirm_df, current_dir)
            self._act_regime(symbol, df, decision, allocated_equity, current_dir)
        elif self.sleeve.strategy_kind == "swing":
            self._act_swing(symbol, df, confirm_df, allocated_equity)
        else:
            snap = self.deriv_data.snapshot(symbol)
            decision = self.strategy.decide(symbol, df, snap, current_dir)
            self._act_regime(symbol, df, decision, allocated_equity, current_dir)

    # ------------------------------------------------------------- 실행

    def _notify_block(self, symbol: str, why: str) -> None:
        """진입 차단 알림. 포지션 수 초과 같은 일상 차단은 로그만(폰 알림 스팸 방지),
        일일 손실한도 등 중요 차단만 폰으로 경고."""
        if "손실 한도" in why:
            self.notifier.warn(f"[{self.sleeve.name}] {symbol}: 진입 차단 — {why}")
        else:
            log.info("[%s] %s 진입 차단 — %s", self.sleeve.name, symbol, why)

    def _open_common(self, plan, symbol: str, direction: Direction, price: float,
                     reason: str, signal_high: float = 0.0, signal_low: float = 0.0,
                     place_tp: bool = True, maker_entry: bool = False) -> None:
        ok, why = self.risk.can_open(len([t for t in self.journal.open_trades()
                                          if t.sleeve == self.sleeve.name]))
        if not ok:
            self._notify_block(symbol, why)
            return
        if plan is None:
            return

        if self.s.trade_mode is TradeMode.DRY_RUN:
            fill_price, qty, oid = price, plan.quantity, None
        else:
            fill = self.executor.open_position(plan, twap_slices=self.sleeve.twap_slices,
                                               place_tp=place_tp, maker_entry=maker_entry)
            if fill is None:
                reason_txt = self.executor.last_error or "알 수 없는 오류"
                # 심볼 자체가 문제면 격리(반복 실패·알림 스팸 방지)
                if self.executor.last_error_fatal:
                    self._quarantine(symbol, reason_txt)
                    self.notifier.warn(
                        f"[{self.sleeve.name}] {symbol}: 유니버스 제외 — {reason_txt}")
                else:
                    self.notifier.error(f"[{self.sleeve.name}] {symbol}: 주문 실패 — {reason_txt}")
                return
            fill_price, qty, oid = fill.price, fill.quantity, fill.order_id

        self.journal.record_open(TradeRecord(
            symbol=symbol, direction=direction.value, entry_price=fill_price, quantity=qty,
            opened_at=_now_iso(), mode=self.s.trade_mode.value, stop_price=plan.stop_price,
            take_profit=plan.take_profit, order_id=oid, sleeve=self.sleeve.name,
            signal_high=signal_high, signal_low=signal_low,
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
            if getattr(decision, "stop_price", 0.0):
                plan = self.risk.build_plan_with_stop(symbol, decision.direction, price,
                                                      decision.stop_price,
                                                      decision.take_profit, equity,
                                                      account_equity=self._account_equity)
            else:
                atr_value = float(ind.atr(df).iloc[-1])
                plan = self.risk.build_plan(symbol, decision.direction, price, atr_value, equity,
                                            account_equity=self._account_equity)
            self._open_common(plan, symbol, decision.direction, price, decision.regime.value)

    # ------------------------------------------------- 단타 (모멘텀 청산)

    def _scalp_momentum_exit(self, symbol: str, df) -> bool:
        """신호봉 고가/저가 갱신 → 다음 평가(봉) 종가 청산. 청산했으면 True.

        백테스터의 momentum exit 와 동일 로직 (라이브 패리티):
          - armed 상태에서 이번 평가 도달 → 최소익절 이상이면 종가 청산
          - 미달이면 재무장 대기 (SL 은 계속 유효)
          - 미무장 상태에서 신고가/신저가 갱신 → armed
        """
        rec = self._sleeve_trade(symbol)
        if rec is None or not rec.signal_high:
            return False
        price = float(df["close"].iloc[-1])
        bar_high = float(df["high"].iloc[-1])
        bar_low = float(df["low"].iloc[-1])
        direction = Direction(rec.direction)
        min_tp = getattr(self.strategy, "min_tp_frac", 0.0008)

        if rec.momentum_armed:
            profit_frac = ((price - rec.entry_price) / rec.entry_price
                           if direction is Direction.LONG
                           else (rec.entry_price - price) / rec.entry_price)
            if profit_frac >= min_tp:
                self._close_trade(rec, price, "momentum_tp")
                return True
            rec.momentum_armed = False
            self.journal.save()

        if not rec.momentum_armed:
            if direction is Direction.LONG and bar_high > rec.signal_high:
                rec.momentum_armed = True
                self.journal.save()
            elif direction is Direction.SHORT and bar_low < rec.signal_low:
                rec.momentum_armed = True
                self.journal.save()
        return False

    _TF_SEC = {"1m": 60, "3m": 180, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400}

    def _scalp_in_cooldown(self, symbol: str, cooldown_bars: int = 15) -> bool:
        """직전 청산 후 N봉 재진입 금지 (백테스터 쿨다운과 패리티, 시그널 TF 기준)."""
        from datetime import datetime
        cooldown_sec = cooldown_bars * self._TF_SEC.get(self.sleeve.signal_tf, 60)
        latest = None
        for t in self.journal.closed_trades():
            if t.sleeve == self.sleeve.name and t.symbol == symbol and t.closed_at:
                latest = t.closed_at
        if not latest:
            return False
        try:
            closed = datetime.fromisoformat(latest)
            now = datetime.fromisoformat(_now_iso())
            return (now - closed).total_seconds() < cooldown_sec
        except ValueError:
            return False

    def _act_scalp(self, symbol, df, decision, equity, current_dir) -> None:
        # 0) 보유 중이면 모멘텀 청산 우선 점검
        if current_dir is not None and self._scalp_momentum_exit(symbol, df):
            return

        if decision.action is Action.CLOSE and current_dir is not None:
            rec = self._sleeve_trade(symbol)
            if rec:
                self._close_trade(rec, float(df["close"].iloc[-1]), decision.reason or "scalp_exit")
            return

        if decision.action in (Action.OPEN_LONG, Action.OPEN_SHORT):
            if self._scalp_in_cooldown(symbol):
                log.info("[%s] %s 쿨다운 중 — 진입 스킵", self.sleeve.name, symbol)
                return
            price = float(df["close"].iloc[-1])
            plan = self.risk.build_plan_with_stop(symbol, decision.direction, price,
                                                  decision.stop_price, decision.take_profit,
                                                  equity, account_equity=self._account_equity)
            # 모멘텀 청산 모드: 고정 TP 주문은 내지 않음 (SL 만 예약).
            # 진입방식은 슬리브 설정(scalp 은 테이커=시장가 — 돌파매매는 메이커가
            # 잘 안 붙고 테스트넷은 호가창이 얇아 어차피 시장가 폴백됨).
            self._open_common(plan, symbol, decision.direction, price, "scalp",
                              signal_high=decision.signal_high,
                              signal_low=decision.signal_low, place_tp=False,
                              maker_entry=self.sleeve.maker_entry)

    # ------------------------------------------------------- 중장기(피라미딩)

    def _act_swing(self, symbol, df, confirm_df, equity) -> None:
        price = float(df["close"].iloc[-1])
        rec = self._sleeve_trade(symbol)

        # dry_run 은 봉 종가로 SL/TP 점검
        if self.s.trade_mode is TradeMode.DRY_RUN and rec is not None:
            self._check_sl_tp(symbol, price)
            rec = self._sleeve_trade(symbol)  # 청산됐을 수 있음

        position = None
        if rec is not None:
            position = SwingPosition(Direction(rec.direction), rec.stage, rec.alloc_frac,
                                     rec.entry_price, rec.stop_price)
        decision: SwingDecision = self.strategy.decide(symbol, df, confirm_df, position)
        log.info("[swing] %s %s", symbol, decision.summary())

        if decision.action in (Action.OPEN_LONG, Action.OPEN_SHORT):
            self._swing_open(symbol, decision, price, equity)
        elif decision.action is Action.ADD and rec is not None:
            self._swing_add(rec, symbol, decision, price, equity)

    def _swing_qty(self, frac: float, equity: float, price: float) -> float:
        """배분 비율(슬리브 예산 대비)로 수량 산정. 명목가치 = frac × 배정자본."""
        notional = max(0.0, frac) * equity
        return notional / price if price > 0 else 0.0

    def _swing_open(self, symbol, decision, price, equity) -> None:
        ok, why = self.risk.can_open(len([t for t in self.journal.open_trades()
                                          if t.sleeve == self.sleeve.name]))
        if not ok:
            self._notify_block(symbol, why)
            return
        qty = self.risk_amount_to_qty(symbol, self._swing_qty(decision.target_frac, equity, price))
        if qty <= 0:
            return
        plan = TradePlan(symbol=symbol, direction=decision.direction, entry_price=price,
                         stop_price=decision.stop_price, take_profit=decision.take_profit,
                         quantity=qty, leverage=1, risk_amount=qty * abs(price - decision.stop_price),
                         notional=qty * price)
        if self.s.trade_mode is TradeMode.DRY_RUN:
            fill_price, fqty, oid = price, qty, None
        else:
            fill = self.executor.open_position(plan, twap_slices=self.sleeve.twap_slices)
            if fill is None:
                self.notifier.error(f"[swing] {symbol}: 주문 실패")
                return
            fill_price, fqty, oid = fill.price, fill.quantity, fill.order_id

        self.journal.record_open(TradeRecord(
            symbol=symbol, direction=decision.direction.value, entry_price=fill_price, quantity=fqty,
            opened_at=_now_iso(), mode=self.s.trade_mode.value, stop_price=decision.stop_price,
            take_profit=decision.take_profit, order_id=oid, sleeve=self.sleeve.name,
            stage=1, alloc_frac=decision.target_frac,
        ))
        self.notifier.trade(
            f"[swing] {symbol} {decision.direction.value.upper()} 진입 ({decision.reason})\n"
            f"진입 {fill_price:.4f} | SL {decision.stop_price:.4f} | TP {decision.take_profit:.4f}\n"
            f"비중 {decision.target_frac:.0%} | 수량 {fqty}",
            title="📗 중장기 진입",
        )

    def _swing_add(self, rec, symbol, decision, price, equity) -> None:
        add_frac = decision.target_frac - rec.alloc_frac
        if add_frac <= 1e-9 and decision.stop_price == rec.stop_price:
            return  # 증량도 SL 변경도 없음
        add_qty = self.risk_amount_to_qty(symbol, self._swing_qty(add_frac, equity, price))

        if self.s.trade_mode is not TradeMode.DRY_RUN and self.binance is not None and add_qty > 0:
            side = "buy" if rec.direction == "long" else "sell"
            self.binance.create_market_order(symbol, side, add_qty, position_side=rec.direction)
            # 총수량 기준 SL/TP 재예약
            self._rebracket(symbol, rec.direction, rec.quantity + add_qty,
                            decision.stop_price, decision.take_profit)

        self.journal.record_add(symbol, self.sleeve.name, rec.direction, price, add_qty,
                                decision.stop_price, decision.stage, decision.target_frac,
                                decision.take_profit)
        self.notifier.trade(
            f"[swing] {symbol} {rec.direction.upper()} 추가 ({decision.reason})\n"
            f"+{add_qty} @ {price:.4f} | 누적비중 {decision.target_frac:.0%} "
            f"| SL {decision.stop_price:.4f} stage{decision.stage}",
            title="📗 중장기 피라미딩",
        )

    def _rebracket(self, symbol, direction, total_qty, stop, tp) -> None:
        """추가 후 총수량 기준으로 SL/TP 재예약."""
        if self.binance is None:
            return
        self.binance.cancel_all_orders(symbol)
        close_side = "sell" if direction == "long" else "buy"
        qty = self.binance.amount_to_precision(symbol, total_qty)
        try:
            self.binance.create_stop_order(symbol, close_side, qty, stop, position_side=direction)
            self.binance.create_take_profit_order(symbol, close_side, qty, tp, position_side=direction)
        except Exception as e:  # noqa: BLE001
            log.warning("[swing] SL/TP 재예약 실패 %s: %s", symbol, e)

    def risk_amount_to_qty(self, symbol: str, qty: float) -> float:
        """거래소 정밀도로 수량 반올림(라이브). dry_run 은 그대로."""
        if self.binance is not None:
            try:
                return self.binance.amount_to_precision(symbol, qty)
            except Exception:  # noqa: BLE001
                return qty
        return qty


def allocated_str(worker: SleeveWorker) -> str:
    return f"{worker.sleeve.allocation:.0%}"
