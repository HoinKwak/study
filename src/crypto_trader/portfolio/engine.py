"""포트폴리오 엔진 — 여러 슬리브를 각자 주기로 평가·실행.

- 헤지 모드 + isolated 로 슬리브 간 방향 독립.
- 자본은 논리적 배분(50/25/25). 각 슬리브는 배정 자본으로 사이징.
- 단일 프로세스에서 슬리브별 독립 주기(단타 1분 / 중기 15분 / 중장기 4시간).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from ..config import Settings, TradeMode
from ..connectors import (BinanceClient, BinanceDerivativesData,
                          high_volume_usdt_symbols)
from ..execution import Executor, PaperBroker
from ..monitoring import Notifier, TradeJournal
from ..utils import get_logger
from .sleeve import Sleeve, default_sleeves
from .worker import SleeveWorker, _iso_to_ms, _now_iso

log = get_logger("portfolio")

UNIVERSE_REFRESH_SEC = 6 * 3600  # 동적 유니버스 갱신 주기


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
        self._starting_equity: float | None = None   # 시작 시점 총자본(누적 수익률 기준)
        self.workers = [
            SleeveWorker(sl, settings, self.binance, self.deriv_data, self.executor,
                         self.journal, self.notifier, realize_cb=self._realize,
                         equity_provider=self._total_equity,
                         start_equity_provider=lambda: self._starting_equity or 0.0)
            for sl in self.sleeves
        ]
        self._last_eval: dict[str, float] = {sl.name: 0.0 for sl in self.sleeves}
        self._universe_refreshed = 0.0
        self._started = False

    # ------------------------------------------------------- 동적 유니버스

    def _tradable_bases(self) -> set[str] | None:
        """거래 가능한 심볼 집합('BTC/USDT' 형태). 클라이언트 없으면 None(필터 생략)."""
        if self.binance is None:
            return None
        try:
            self.binance.exchange.load_markets()
            out = set()
            for m in self.binance.exchange.markets.values():
                if m.get("linear") and m.get("quote") == "USDT" and m.get("active"):
                    out.add(f"{m['base']}/USDT")
            return out
        except Exception as e:  # noqa: BLE001
            log.warning("마켓 목록 조회 실패(유니버스 필터 생략): %s", e)
            return None

    def _refresh_universe(self) -> None:
        dyn = [sl for sl in self.sleeves if sl.dynamic_universe]
        if not dyn:
            return
        tradable = self._tradable_bases()
        for sl in dyn:
            ranked = high_volume_usdt_symbols(sl.min_universe_volume)
            if not ranked:
                log.warning("[%s] 유니버스 조회 실패 — 기존 심볼 유지", sl.name)
                continue
            symbols = [sym for sym, _qv in ranked]
            if tradable is not None:
                dropped = [s for s in symbols if s not in tradable]
                symbols = [s for s in symbols if s in tradable]
                if dropped:
                    log.info("[%s] 거래소 미지원으로 제외: %s", sl.name, ",".join(dropped[:10]))
            if symbols:
                old = set(sl.symbols)
                sl.symbols = symbols
                added, removed = set(symbols) - old, old - set(symbols)
                if added or removed:
                    log.info("[%s] 유니버스 %d 페어 (+%d/-%d): %s%s",
                             sl.name, len(symbols), len(added), len(removed),
                             ",".join(symbols[:15]),
                             f" 외 {len(symbols)-15}" if len(symbols) > 15 else "")
        self._universe_refreshed = time.time()

    def _realize(self, pnl: float) -> None:
        self._paper_equity += pnl

    def _reconcile_orphan_exits(self) -> None:
        """활성 슬리브에 없는 열린 포지션(제거·개명된 옛 슬리브)을 청산 반영.

        슬리브 구성을 바꾸면(예: mid/scalp15m 제거) 그 슬리브로 열렸던 포지션은
        어느 워커의 리컨실도 훑지 않아(`t.sleeve == self.sleeve.name` 필터) 저널에
        영영 '열림'으로 남는다. 여기서 거래소에 이미 사라진(수동·외부 청산) 그런
        고아 포지션을 감지해 실제 체결가·실현손익으로 청산 처리한다. 슬리브가 없어졌으니
        어느 슬리브의 risk 카운터에도 넣지 않는다(paper 잔고는 거래소에서 실시간 조회).
        """
        if self.s.trade_mode is TradeMode.DRY_RUN or self.binance is None:
            return
        active = {sl.name for sl in self.sleeves}
        orphans = [t for t in self.journal.open_trades() if t.sleeve not in active]
        if not orphans:
            return
        try:
            live = self.binance.fetch_positions()
        except Exception as e:  # noqa: BLE001
            log.warning("고아 포지션 리컨실 조회 실패: %s", e)
            return
        live_keys = {(p.get("symbol"), p.get("side")) for p in live
                     if float(p.get("contracts") or 0) != 0}
        for rec in orphans:
            canonical = self.binance.resolve_symbol(rec.symbol)
            if (canonical, rec.direction) in live_keys:
                log.warning("고아 포지션 %s %s (슬리브 '%s' 제거됨)이 거래소에 아직 열려 있음 "
                            "— 봇이 관리하지 않으니 수동 정리 필요", rec.symbol, rec.direction, rec.sleeve)
                continue
            self.binance.cancel_all_orders(rec.symbol)  # 잔여 조건부 주문 정리
            since_ms = _iso_to_ms(rec.opened_at)
            res = None
            try:
                res = self.binance.fetch_realized_close(rec.symbol, rec.direction, since_ms)
            except Exception as e:  # noqa: BLE001
                log.warning("%s 실현손익 조회 실패: %s", rec.symbol, e)
            if res is not None:
                exit_price, pnl = res
            else:
                exit_price = rec.stop_price or rec.entry_price
                pnl = self._orphan_pnl(rec, exit_price)  # 조회 실패 → 가격차로 근사
            is_sl = (rec.stop_price and exit_price > 0
                     and abs(exit_price - rec.stop_price) / rec.stop_price < 0.0015)
            reason = "exchange_sl" if is_sl else "수동/외부 청산"
            self.journal.record_close(rec.symbol, exit_price, _now_iso(), pnl, reason,
                                      sleeve=rec.sleeve, direction=rec.direction)
            ret = (pnl / (rec.entry_price * rec.quantity) * 100.0
                   if rec.entry_price and rec.quantity else 0.0)
            label = "SL·고아정리" if is_sl else "수동/외부·고아정리"
            self.notifier.trade(
                f"[{rec.sleeve}·제거된슬리브] {rec.symbol} {rec.direction.upper()} 청산 ({label})\n"
                f"진입 {rec.entry_price:.4f} → {exit_price:.4f}\n"
                f"손익 {pnl:+.2f} USDT ({ret:+.2f}%)",
                title="📕 청산(고아 정리)")
            log.info("고아 포지션 정리: %s %s (슬리브 '%s') 손익 %+.2f",
                     rec.symbol, rec.direction, rec.sleeve, pnl)

    def _orphan_pnl(self, rec, exit_price: float) -> float:
        """실현손익 조회 실패 시 가격차 기반 근사(테이커 수수료 차감)."""
        gross = ((exit_price - rec.entry_price) * rec.quantity if rec.direction == "long"
                 else (rec.entry_price - exit_price) * rec.quantity)
        fee = (self.s.taker_fee_pct / 100.0) * (rec.entry_price + exit_price) * rec.quantity
        return gross - fee

    def _load_or_init_baseline(self, current_equity: float) -> float:
        """누적 수익률 기준 자본(인셉션 자본)을 산출.

        인셉션 자본 = 현재잔고 − 실현손익(저널 누적). 재시작·거래 진행과 무관하게
        일정하므로, 저장값이 이 값과 크게 어긋나면(예: 잘못된 10,000 기본값) 자동 교정한다.
        저장값이 ~2% 이내로 일치하면 안정성을 위해 유지(미실현손익 흔들림 흡수).
        """
        path = Path(self.s.state_dir) / "portfolio.json"
        try:
            realized = float(self.journal.stats().get("total_pnl", 0.0))
        except Exception:  # noqa: BLE001
            realized = 0.0
        true_start = current_equity - realized  # 인셉션 자본

        stored = None
        try:
            if path.exists():
                stored = float(json.loads(path.read_text()).get("starting_equity", 0.0))
        except Exception:  # noqa: BLE001
            stored = None

        if stored and stored > 0 and true_start > 0 and abs(stored - true_start) <= 0.02 * true_start:
            base = stored
        else:
            base = true_start if true_start > 0 else current_equity
            if stored and abs((stored or 0) - base) > 0.02 * max(base, 1):
                log.info("기준자본 교정: %.2f → %.2f (현재 %.2f − 실현 %.2f)",
                         stored, base, current_equity, realized)
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({"starting_equity": base,
                                            "mode": self.s.trade_mode.value}, indent=2))
            except Exception:  # noqa: BLE001
                pass
        return base

    def _persist_equity(self, equity: float) -> None:
        """현재 실잔고를 portfolio.json 에 기록(대시보드가 실제 누적수익률 계산에 사용)."""
        path = Path(self.s.state_dir) / "portfolio.json"
        try:
            data = json.loads(path.read_text()) if path.exists() else {}
        except Exception:  # noqa: BLE001
            data = {}
        now = time.time()
        data["equity"] = equity
        data["equity_ts"] = now
        # 실잔고 이력 — 일별손익·수익률곡선을 실잔고(수수료·펀딩 포함) 기준으로 그리기 위함.
        # 15분 스로틀로 append, 최근 500점 유지.
        hist = data.get("equity_history")
        if not isinstance(hist, list):
            hist = []
        try:
            last_ts = float(hist[-1][0]) if hist else 0.0
        except (TypeError, ValueError, IndexError):
            last_ts = 0.0
        if not hist or (now - last_ts) >= 900:
            hist.append([now, equity])
            data["equity_history"] = hist[-500:]
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2))
        except Exception:  # noqa: BLE001
            pass

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
        self._refresh_universe()
        equity = self._total_equity()
        self._starting_equity = self._load_or_init_baseline(equity)   # 누적 수익률 기준점
        alloc = ", ".join(f"{sl.name} {sl.allocation:.0%}({sl.signal_tf}, {len(sl.symbols)}페어)"
                          for sl in self.sleeves)
        self.notifier.info(
            f"포트폴리오 시작 — mode={self.s.trade_mode.value} equity={equity:.2f}\n{alloc}",
            title="🤖 crypto-trader 포트폴리오",
        )
        self._started = True

    def run_once(self, force_all: bool = False) -> None:
        """주기 도래한 슬리브만 평가. force_all=True 면 전부 평가(테스트/1회 실행용)."""
        if not self._started:
            self._startup()
        if time.time() - self._universe_refreshed >= UNIVERSE_REFRESH_SEC:
            self._refresh_universe()
        now = time.time()
        total_equity = self._total_equity()
        self._persist_equity(total_equity)
        for worker in self.workers:
            name = worker.sleeve.name
            due = force_all or (now - self._last_eval[name]) >= worker.sleeve.eval_interval_sec
            if not due:
                continue
            log.info("[%s] 평가 (자본 %.2f × %.0f%%)", name, total_equity, worker.sleeve.allocation * 100)
            worker.evaluate(total_equity)
            self._last_eval[name] = now
        self._reconcile_orphan_exits()   # 제거·개명된 옛 슬리브의 열린 포지션 정리

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
