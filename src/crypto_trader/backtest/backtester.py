"""과거 캔들 재생(replay) 기반 백테스터.

라이브 엔진과 **동일한** TechnicalSignals / SignalAggregator / RiskManager 로직을
과거 OHLCV 에 적용해 전략을 검증한다.

주의: 바이낸스 파생 데이터(펀딩/OI/롱숏/테이커)는 REST 로 최근 ~30일만 제공되므로,
      장기 백테스트는 **기술지표 시그널만** 사용한다(파생 가중치 제외).
      → aggregator 가 사용 가능한 컴포넌트 가중치로 자동 정규화하므로,
        technical 단독이어도 점수 스케일은 일관되게 유지된다.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from ..config import Settings
from ..risk import RiskManager
from ..signals import SignalAggregator, TechnicalSignals
from ..signals import indicators as ind
from ..signals.base import Direction


@dataclass
class Trade:
    symbol: str
    direction: Direction
    entry_idx: int
    entry_price: float
    exit_idx: int | None = None
    exit_price: float | None = None
    stop_price: float = 0.0
    take_profit: float = 0.0
    quantity: float = 0.0
    pnl: float = 0.0
    reason: str = ""


@dataclass
class BacktestResult:
    symbol: str
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)
    starting_equity: float = 10_000.0

    @property
    def ending_equity(self) -> float:
        return self.equity_curve[-1] if self.equity_curve else self.starting_equity

    @property
    def total_return_pct(self) -> float:
        return (self.ending_equity / self.starting_equity - 1.0) * 100.0

    @property
    def num_trades(self) -> int:
        return len([t for t in self.trades if t.exit_idx is not None])

    @property
    def win_rate(self) -> float:
        closed = [t for t in self.trades if t.exit_idx is not None]
        if not closed:
            return 0.0
        wins = sum(1 for t in closed if t.pnl > 0)
        return wins / len(closed) * 100.0

    @property
    def profit_factor(self) -> float:
        gross_win = sum(t.pnl for t in self.trades if t.pnl > 0)
        gross_loss = -sum(t.pnl for t in self.trades if t.pnl < 0)
        return gross_win / gross_loss if gross_loss > 0 else float("inf")

    @property
    def max_drawdown_pct(self) -> float:
        peak = self.starting_equity
        max_dd = 0.0
        for eq in self.equity_curve:
            peak = max(peak, eq)
            dd = (peak - eq) / peak * 100.0
            max_dd = max(max_dd, dd)
        return max_dd

    def report(self) -> str:
        return (
            f"\n===== 백테스트 결과: {self.symbol} =====\n"
            f"기간 캔들 수      : {len(self.equity_curve)}\n"
            f"시작 자본         : {self.starting_equity:,.2f} USDT\n"
            f"종료 자본         : {self.ending_equity:,.2f} USDT\n"
            f"총 수익률         : {self.total_return_pct:+.2f}%\n"
            f"매매 횟수         : {self.num_trades}\n"
            f"승률              : {self.win_rate:.1f}%\n"
            f"손익비(PF)        : {self.profit_factor:.2f}\n"
            f"최대 낙폭(MDD)    : {self.max_drawdown_pct:.2f}%\n"
            f"========================================"
        )


class Backtester:
    """단일 심볼, 단일 포지션(피라미딩 없음) 백테스터."""

    def __init__(self, settings: Settings, starting_equity: float = 10_000.0,
                 warmup: int = 50):
        self.s = settings
        self.starting_equity = starting_equity
        self.warmup = warmup
        self.tech = TechnicalSignals()
        self.aggregator = SignalAggregator(entry_threshold=settings.entry_score_threshold)
        self.risk = RiskManager(settings)

    def run(self, symbol: str, df: pd.DataFrame) -> BacktestResult:
        result = BacktestResult(symbol, starting_equity=self.starting_equity)
        equity = self.starting_equity
        open_trade: Trade | None = None

        atr_series = ind.atr(df)

        for i in range(self.warmup, len(df)):
            window = df.iloc[: i + 1]
            bar = df.iloc[i]
            price = float(bar["close"])
            high = float(bar["high"])
            low = float(bar["low"])

            # 1) 오픈 포지션 청산 체크 (해당 봉의 고저로 SL/TP 터치 판정)
            if open_trade is not None:
                exit_price, reason = self._check_exit(open_trade, high, low)
                if exit_price is not None:
                    pnl = self._pnl(open_trade, exit_price)
                    open_trade.exit_idx = i
                    open_trade.exit_price = exit_price
                    open_trade.pnl = pnl
                    open_trade.reason = reason
                    equity += pnl
                    open_trade = None

            # 2) 신규 진입 (포지션 없을 때만)
            if open_trade is None:
                sig = self.tech.compute(window)
                agg = self.aggregator.aggregate(symbol, [sig])
                if agg.direction is not Direction.FLAT:
                    atr_value = float(atr_series.iloc[i])
                    plan = self.risk.build_plan(symbol, agg.direction, price, atr_value, equity)
                    if plan is not None:
                        open_trade = Trade(
                            symbol=symbol,
                            direction=plan.direction,
                            entry_idx=i,
                            entry_price=plan.entry_price,
                            stop_price=plan.stop_price,
                            take_profit=plan.take_profit,
                            quantity=plan.quantity,
                        )
                        result.trades.append(open_trade)

            result.equity_curve.append(equity)

        # 마지막 미청산 포지션은 종가로 정리
        if open_trade is not None and open_trade.exit_idx is None:
            last_price = float(df["close"].iloc[-1])
            open_trade.exit_idx = len(df) - 1
            open_trade.exit_price = last_price
            open_trade.pnl = self._pnl(open_trade, last_price)
            open_trade.reason = "end_of_data"
            if result.equity_curve:
                result.equity_curve[-1] += open_trade.pnl

        return result

    # ------------------------------------------------------------- 헬퍼

    @staticmethod
    def _check_exit(trade: Trade, high: float, low: float) -> tuple[float | None, str]:
        """보수적 가정: 같은 봉에 SL/TP 둘 다 닿으면 손절 우선."""
        if trade.direction is Direction.LONG:
            if low <= trade.stop_price:
                return trade.stop_price, "stop_loss"
            if high >= trade.take_profit:
                return trade.take_profit, "take_profit"
        else:  # SHORT
            if high >= trade.stop_price:
                return trade.stop_price, "stop_loss"
            if low <= trade.take_profit:
                return trade.take_profit, "take_profit"
        return None, ""

    @staticmethod
    def _pnl(trade: Trade, exit_price: float) -> float:
        if trade.direction is Direction.LONG:
            return (exit_price - trade.entry_price) * trade.quantity
        return (trade.entry_price - exit_price) * trade.quantity
