"""포트폴리오 엔진 — 여러 슬리브를 각자 주기로 평가·실행.

- 헤지 모드 + isolated 로 슬리브 간 방향 독립.
- 자본은 논리적 배분(50/25/25). 각 슬리브는 배정 자본으로 사이징.
- 단일 프로세스에서 슬리브별 독립 주기(단타 1분 / 중기 15분 / 중장기 4시간).
"""
from __future__ import annotations

import time

from ..config import Settings, TradeMode
from ..connectors import BinanceClient, BinanceDerivativesData
from ..execution import Executor, PaperBroker
from ..monitoring import Notifier, TradeJournal
from ..utils import get_logger
from .sleeve import Sleeve, default_sleeves
from .worker import SleeveWorker

log = get_logger("portfolio")


class PortfolioEngine:
    def __init__(self, settings: Settings, sleeves: list[Sleeve] | None = None,
                 paper_start_equity: float = 10_000.0):
        self.s = settings
        self.sleeves = sleeves or default_sleeves(settings)

        self.binance: BinanceClient | None = None
        if settings.has_binance_keys or settings.trade_mode is not TradeMode.DRY_RUN:
            self.binance = BinanceClient(settings)
        self.deriv_data = BinanceDerivativesData()
        self.executor = Executor(settings, self.binance, PaperBroker(paper_start_equity))
        self.journal = TradeJournal(settings.state_dir)
        self.notifier = Notifier(settings)

        self._paper_equity = paper_start_equity
        self.workers = [
            SleeveWorker(sl, settings, self.binance, self.deriv_data, self.executor,
                         self.journal, self.notifier, realize_cb=self._realize)
            for sl in self.sleeves
        ]
        self._last_eval: dict[str, float] = {sl.name: 0.0 for sl in self.sleeves}
        self._started = False

    def _realize(self, pnl: float) -> None:
        self._paper_equity += pnl

    def _total_equity(self) -> float:
        if self.binance is not None and self.s.trade_mode is not TradeMode.DRY_RUN:
            try:
                return self.binance.fetch_balance_usdt()
            except Exception as e:  # noqa: BLE001
                log.warning("잔고 조회 실패, 페이퍼 잔고 사용: %s", e)
        return self._paper_equity

    def _startup(self) -> None:
        if self.binance is not None and self.s.trade_mode is not TradeMode.DRY_RUN:
            self.binance.ensure_position_mode()
        equity = self._total_equity()
        alloc = ", ".join(f"{sl.name} {sl.allocation:.0%}({sl.signal_tf})" for sl in self.sleeves)
        self.notifier.info(
            f"포트폴리오 시작 — mode={self.s.trade_mode.value} equity={equity:.2f}\n{alloc}",
            title="🤖 crypto-trader 포트폴리오",
        )
        self._started = True

    def run_once(self, force_all: bool = False) -> None:
        """주기 도래한 슬리브만 평가. force_all=True 면 전부 평가(테스트/1회 실행용)."""
        if not self._started:
            self._startup()
        now = time.time()
        total_equity = self._total_equity()
        for worker in self.workers:
            name = worker.sleeve.name
            due = force_all or (now - self._last_eval[name]) >= worker.sleeve.eval_interval_sec
            if not due:
                continue
            log.info("[%s] 평가 (자본 %.2f × %.0f%%)", name, total_equity, worker.sleeve.allocation * 100)
            worker.evaluate(total_equity)
            self._last_eval[name] = now

    def run_forever(self, tick_sec: int | None = None) -> None:
        # 가장 짧은 슬리브 주기를 틱으로(기본 60s)
        tick = tick_sec or min((sl.eval_interval_sec for sl in self.sleeves), default=60)
        log.info("포트폴리오 엔진 시작 — tick=%ds sleeves=%s",
                 tick, [sl.name for sl in self.sleeves])
        while True:
            try:
                self.run_once()
            except KeyboardInterrupt:
                log.info("사용자 중단 — 종료")
                break
            except Exception as e:  # noqa: BLE001
                log.exception("포트폴리오 루프 오류: %s", e)
                self.notifier.error(f"포트폴리오 루프 오류: {e}")
            time.sleep(tick)
