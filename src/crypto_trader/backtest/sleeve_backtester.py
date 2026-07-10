"""슬리브 백테스터 — 라이브와 동일한 슬리브 전략(swing/mid/scalp)을 재생.

라이브 워커와 조건을 맞춘다:
  - 시그널 TF 윈도우 = 최근 200봉 (라이브 fetch limit=200 과 동일)
  - 확인 TF 윈도우 = 완결된 상위봉 최근 100개 (리샘플, lookahead 방지:
    현재 진행 중인 상위봉은 제외 — 보수적)
  - 수수료: 테이커 왕복 (기본 0.05%/side) + 슬리피지 (기본 0.02%)
  - 같은 봉에 SL/TP 둘 다 닿으면 손절 우선(보수적)

단순화(문서화된 근사):
  - TWAP 분할 진입은 신호봉 종가+슬리피지 일괄 체결로 근사
  - 단타 OI 는 과거 이력이 없어 백테스트에서 제외(oi_delta=None → 통과)
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..config import Settings
from ..risk import RiskManager
from ..signals import indicators as ind
from ..signals.base import Direction
from ..strategy import Action, MidStrategy, ScalpStrategy, SwingStrategy
from ..strategy.regime import detect_regime, Regime
from ..strategy.swing import SwingPosition
from .backtester import BacktestResult, Trade
from .multi_tf import TF_RULE, resample_ohlcv

SIGNAL_WINDOW = 200
CONFIRM_WINDOW = 100


class SleeveBacktester:
    # 청산 후 재진입 금지 봉수(과매매 억제). 슬리브별 기본값.
    DEFAULT_COOLDOWN = {"scalp": 15, "mid": 8, "swing": 2}

    def __init__(self, settings: Settings, sleeve_kind: str,
                 confirm_tf: str | None = None,
                 starting_equity: float = 10_000.0, warmup: int = 60,
                 taker_fee: float = 0.0005, slippage: float = 0.0002,
                 cooldown_bars: int | None = None):
        self.s = settings
        self.kind = sleeve_kind
        self.confirm_tf = confirm_tf
        self.starting_equity = starting_equity
        self.warmup = warmup
        self.taker_fee = taker_fee
        self.slippage = slippage
        self.cooldown_bars = (cooldown_bars if cooldown_bars is not None
                              else self.DEFAULT_COOLDOWN.get(sleeve_kind, 0))
        self.risk = RiskManager(settings)

        if sleeve_kind == "scalp":
            self.strategy = ScalpStrategy(settings)
        elif sleeve_kind == "mid":
            self.strategy = MidStrategy(settings)
        elif sleeve_kind == "swing":
            self.strategy = SwingStrategy(settings)
        else:
            raise ValueError(f"지원하지 않는 슬리브: {sleeve_kind}")

    # ------------------------------------------------------------ 헬퍼

    def _confirm_slices(self, df: pd.DataFrame):
        """확인 TF 리샘플 + 각 시그널봉 시점의 '완결 상위봉 수' 사전 계산."""
        if self.confirm_tf is None:
            return None, None
        confirm = resample_ohlcv(df, self.confirm_tf)
        delta = pd.tseries.frequencies.to_offset(TF_RULE[self.confirm_tf])
        ends = (confirm.index + delta).asi8          # 상위봉 종료 시각
        sig_ts = df.index.asi8
        counts = np.searchsorted(ends, sig_ts, side="right")  # t 까지 완결된 상위봉 수
        return confirm, counts

    def _confirm_window(self, confirm, counts, i):
        if confirm is None:
            return None
        n = int(counts[i])
        if n < 20:
            return None
        lo = max(0, n - CONFIRM_WINDOW)
        return confirm.iloc[lo:n]

    def _fill(self, price: float, direction: Direction, closing: bool = False) -> float:
        """슬리피지 반영 체결가."""
        adverse = 1 if (direction is Direction.LONG) != closing else -1
        return price * (1 + adverse * self.slippage)

    def _fee(self, notional: float) -> float:
        return abs(notional) * self.taker_fee

    @staticmethod
    def _pnl(direction: Direction, entry: float, exit_price: float, qty: float) -> float:
        return (exit_price - entry) * qty if direction is Direction.LONG else (entry - exit_price) * qty

    @staticmethod
    def _sl_tp_hit(direction: Direction, high: float, low: float,
                   stop: float, tp: float) -> tuple[float | None, str]:
        if direction is Direction.LONG:
            if low <= stop:
                return stop, "stop_loss"
            if high >= tp:
                return tp, "take_profit"
        else:
            if high >= stop:
                return stop, "stop_loss"
            if low <= tp:
                return tp, "take_profit"
        return None, ""

    # ------------------------------------------------------------ 메인

    def run(self, symbol: str, df: pd.DataFrame) -> BacktestResult:
        result = BacktestResult(symbol, starting_equity=self.starting_equity)
        equity = self.starting_equity
        trade: Trade | None = None
        alloc_frac = 0.0
        stage = 1

        confirm, counts = self._confirm_slices(df)
        atr_series = ind.atr(df)
        last_exit_idx = -10**9

        for i in range(self.warmup, len(df)):
            bar = df.iloc[i]
            price, high, low = float(bar["close"]), float(bar["high"]), float(bar["low"])
            window = df.iloc[max(0, i - SIGNAL_WINDOW + 1): i + 1]
            confirm_win = self._confirm_window(confirm, counts, i)

            # 1) SL/TP 인트라바 체크
            if trade is not None:
                exit_px, reason = self._sl_tp_hit(trade.direction, high, low,
                                                  trade.stop_price, trade.take_profit)
                if exit_px is not None:
                    fill = self._fill(exit_px, trade.direction, closing=True)
                    equity += self._close(trade, i, fill, reason, df)
                    trade = None
                    alloc_frac, stage = 0.0, 1
                    last_exit_idx = i

            # 쿨다운: 청산 직후 재진입 금지 (과매매 억제)
            in_cooldown = trade is None and (i - last_exit_idx) <= self.cooldown_bars

            # 2) 전략 결정
            cur_dir = trade.direction if trade else None
            if in_cooldown:
                result.equity_curve.append(equity)
                continue
            had_trade = trade is not None
            if self.kind == "swing":
                pos = None
                if trade is not None:
                    pos = SwingPosition(trade.direction, stage, alloc_frac,
                                        trade.entry_price, trade.stop_price)
                d = self.strategy.decide(symbol, window, confirm_win, pos)
                trade, equity, alloc_frac, stage = self._apply_swing(
                    result, trade, d, i, price, equity, alloc_frac, stage, df)
            elif self.kind == "mid":
                d = self.strategy.decide(symbol, window, confirm_win, cur_dir)
                trade, equity = self._apply_simple(result, trade, d, i, price,
                                                   equity, atr_series, df, use_plan=True)
            else:  # scalp
                regime = detect_regime(confirm_win)[0] if confirm_win is not None else Regime.NEUTRAL
                d = self.strategy.decide(symbol, window, oi_delta=None,
                                         current_direction=cur_dir, confirm_regime=regime)
                trade, equity = self._apply_simple(result, trade, d, i, price,
                                                   equity, atr_series, df, use_plan=False)

            if had_trade and trade is None:
                last_exit_idx = i  # 시그널 청산도 쿨다운 대상

            result.equity_curve.append(equity)

        # 미청산 정리
        if trade is not None and trade.exit_idx is None:
            fill = self._fill(float(df["close"].iloc[-1]), trade.direction, closing=True)
            pnl = self._close(trade, len(df) - 1, fill, "end_of_data", df)
            if result.equity_curve:
                result.equity_curve[-1] += pnl

        return result

    # ------------------------------------------------------------ 적용

    def _open_trade(self, result, direction, i, price, qty, stop, tp, df) -> Trade:
        fill = self._fill(price, direction)
        t = Trade(symbol=result.symbol, direction=direction, entry_idx=i,
                  entry_price=fill, stop_price=stop, take_profit=tp, quantity=qty,
                  opened_at=str(df.index[i]))
        t.fees += self._fee(fill * qty)
        result.trades.append(t)
        return t

    def _close(self, trade: Trade, idx: int, fill: float, reason: str, df) -> float:
        fee = self._fee(fill * trade.quantity)
        trade.fees += fee
        pnl = self._pnl(trade.direction, trade.entry_price, fill, trade.quantity) - trade.fees
        trade.exit_idx = idx
        trade.exit_price = fill
        trade.pnl = pnl
        trade.reason = reason
        trade.closed_at = str(df.index[idx])
        trade.holding_bars = idx - trade.entry_idx
        return pnl

    def _apply_simple(self, result, trade, d, i, price, equity, atr_series, df,
                      use_plan: bool):
        """mid/scalp: 단일 진입/청산 모델."""
        if trade is not None and d.action is Action.CLOSE:
            fill = self._fill(price, trade.direction, closing=True)
            equity += self._close(trade, i, fill, d.reason or "signal_exit", df)
            return None, equity
        if trade is None and d.action in (Action.OPEN_LONG, Action.OPEN_SHORT):
            if use_plan:  # mid: ATR 사이징
                atr_v = float(atr_series.iloc[i])
                plan = self.risk.build_plan(result.symbol, d.direction, price, atr_v, equity)
            else:         # scalp: 전략 제시 SL/TP 사이징
                plan = self.risk.build_plan_with_stop(result.symbol, d.direction, price,
                                                      d.stop_price, d.take_profit, equity)
            if plan is not None:
                trade = self._open_trade(result, d.direction, i, price, plan.quantity,
                                         plan.stop_price, plan.take_profit, df)
        return trade, equity

    def _apply_swing(self, result, trade, d, i, price, equity, alloc_frac, stage, df):
        """swing: 배분 기반 + 피라미딩."""
        if d.action in (Action.OPEN_LONG, Action.OPEN_SHORT) and trade is None:
            qty = (d.target_frac * equity) / price if price > 0 else 0.0
            if qty > 0:
                trade = self._open_trade(result, d.direction, i, price, qty,
                                         d.stop_price, d.take_profit, df)
                alloc_frac, stage = d.target_frac, d.stage
        elif d.action is Action.ADD and trade is not None:
            add_frac = d.target_frac - alloc_frac
            if add_frac > 1e-9:
                add_qty = (add_frac * equity) / price if price > 0 else 0.0
                if add_qty > 0:
                    fill = self._fill(price, trade.direction)
                    total = trade.quantity + add_qty
                    trade.entry_price = (trade.entry_price * trade.quantity + fill * add_qty) / total
                    trade.quantity = total
                    trade.fees += self._fee(fill * add_qty)
                    trade.num_adds += 1
                    alloc_frac = d.target_frac
            # SL/TP 갱신(트레일링 포함)
            trade.stop_price = d.stop_price
            if d.take_profit:
                trade.take_profit = d.take_profit
            stage = d.stage
        return trade, equity, alloc_frac, stage
