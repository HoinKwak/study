"""메인 오케스트레이션 엔진.

주기마다 각 심볼에 대해:
  1) OHLCV + 파생 데이터 수집
  2) 기술/파생 시그널 계산 → 가중 합산
  3) 진입 방향 결정 → 리스크 매니저로 매매 계획 수립
  4) 실행(dry_run/paper/live)
"""
from __future__ import annotations

import time

import pandas as pd

from ..config import Settings, TradeMode
from ..connectors import BinanceClient, BinanceDerivativesData
from ..data import ohlcv_to_df
from ..execution import Executor, PaperBroker
from ..risk import RiskManager
from ..signals import DerivativesSignals, SignalAggregator, TechnicalSignals
from ..signals import indicators as ind
from ..signals.base import Direction
from ..utils import get_logger

log = get_logger("engine")


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

        # 리스크 / 실행
        self.risk = RiskManager(settings)
        self.paper = PaperBroker()
        self.executor = Executor(settings, self.binance, self.paper)

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
            log.info("%s: 진입 차단 — %s", symbol, reason)
            return

        entry_price = float(df["close"].iloc[-1])
        atr_value = float(ind.atr(df).iloc[-1])
        equity = self._current_equity()

        plan = self.risk.build_plan(symbol, agg.direction, entry_price, atr_value, equity)
        if plan is None:
            log.info("%s: 매매 계획 수립 불가", symbol)
            return

        self.executor.open_position(plan)

    # ------------------------------------------------------------- 루프

    def run_once(self) -> None:
        if not self._started:
            self.risk.start_day(self._current_equity())
            self._started = True
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
            time.sleep(self.s.loop_interval_sec)
