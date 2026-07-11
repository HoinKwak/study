"""시장 스캐너 — 바이낸스 선물 전 종목에서 이벤트를 포착해 알림.

자동매매는 하지 않는다. 한 사이클마다:
  1) 고유동성 유니버스 갱신(TTL 캐시)
  2) 전 심볼 24h 티커 + 펀딩비를 벌크 조회
  3) 심볼별 캔들 + OI 시계열 조회 후 detectors 실행
  4) 쿨다운을 통과한 새 이벤트를 저장 + 심볼별로 묶어 텔레그램 알림

공개 fapi(실전) 데이터를 쓰므로 지역차단이 없는 로컬 PC에서 동작한다.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone

from ..config import Settings
from ..connectors import BinanceDerivativesData, high_volume_usdt_symbols
from ..monitoring import Notifier, NotifyLevel
from ..utils import get_logger
from . import detectors
from .events import EventStore, EventType, ScanEvent, _now_iso

log = get_logger("scanner")

_UNIVERSE_TTL_SEC = 1800  # 유니버스 30분마다 갱신


class MarketScanner:
    def __init__(self, settings: Settings, notifier: Notifier | None = None,
                 store: EventStore | None = None,
                 data: BinanceDerivativesData | None = None):
        self.s = settings
        self.notifier = notifier or Notifier(settings)
        self.store = store or EventStore.load(settings.state_dir)
        self.data = data or BinanceDerivativesData()
        self._universe: list[str] = []
        self._universe_ts: float = 0.0

    # ------------------------------------------------------------- 유니버스

    def _refresh_universe(self, now_mono: float) -> list[str]:
        if self._universe and (now_mono - self._universe_ts) < _UNIVERSE_TTL_SEC:
            return self._universe
        pairs = high_volume_usdt_symbols(self.s.scanner_min_volume)
        symbols = [sym for sym, _vol in pairs][: self.s.scanner_max_symbols]
        if symbols:
            self._universe = symbols
            self._universe_ts = now_mono
            log.info("스캐너 유니버스 %d 심볼 (≥%.0fM)",
                     len(symbols), self.s.scanner_min_volume / 1e6)
        return self._universe

    # ------------------------------------------------------- 심볼별 감지

    def _detect_symbol(self, symbol: str, funding: float | None,
                       ticker24: dict | None, now: datetime) -> list[ScanEvent]:
        """한 심볼에서 발생한 (쿨다운 통과) 이벤트들."""
        s = self.s
        events: list[ScanEvent] = []
        need = max(s.scanner_price_window, s.scanner_vol_lookback) + 2
        kl = self.data.klines(symbol, s.scanner_timeframe, limit=need)
        price = 0.0
        vol1h = 0.0
        pct24 = None
        vol24 = None
        if ticker24:
            try:
                pct24 = float(ticker24.get("priceChangePercent"))
            except (TypeError, ValueError):
                pct24 = None
            try:
                vol24 = float(ticker24.get("quoteVolume"))  # 24h 거래대금(USDT)
            except (TypeError, ValueError):
                vol24 = None

        def ctx() -> str:
            bits = []
            if price:
                bits.append(f"${_fmt_price(price)}")
            if pct24 is not None:
                bits.append(f"24h {pct24:+.1f}%")
            if vol24:
                bits.append(f"24h량 {_fmt_vol(vol24)}")
            if vol1h:
                bits.append(f"1h량 {_fmt_vol(vol1h)}")
            if funding is not None:
                bits.append(f"펀딩 {funding * 100:+.3f}%")
            return " · ".join(bits)

        def add(etype: EventType, value: float, detail: str) -> None:
            if self.store.on_cooldown(symbol, etype, s.scanner_cooldown_min, now):
                return
            extra = ctx()
            full = f"{detail} · {extra}" if extra else detail
            events.append(ScanEvent(symbol=symbol, type=etype.value, value=value,
                                    price=price, detail=full, ts=_now_iso()))

        if kl and kl["close"]:
            closes = kl["close"]
            volumes = kl["volume"]
            price = closes[-1]

            # 최근 1시간 거래대금 근사 = 최근 12개 '닫힌' 5m 캔들의 (거래량×종가) 합
            n_1h = max(1, 3600 // 300)  # 5m 기준 12개
            closed_lo = max(0, len(closes) - 1 - n_1h)
            vol1h = sum(volumes[i] * closes[i] for i in range(closed_lo, len(closes) - 1))

            # 직전(닫힌) 캔들 거래량 배수 — 급등/급락 잡음 컷에 사용
            vol_ratio = _closed_vol_ratio(volumes, s.scanner_vol_lookback)

            pm = detectors.price_move(closes, s.scanner_price_window, s.scanner_price_move_pct)
            if pm and vol_ratio >= s.scanner_move_min_vol_ratio:
                pct, det = pm
                add(EventType.PUMP if pct >= 0 else EventType.DUMP,
                    pct, f"{det}·거래량 {vol_ratio:.1f}x")

            # 거래량 급증은 '닫힌' 캔들 기준 → 진행 중인 마지막 캔들 제외
            vs = detectors.volume_spike(volumes[:-1], s.scanner_vol_lookback, s.scanner_vol_mult)
            if vs:
                ratio, det = vs
                add(EventType.VOL_SPIKE, ratio, det)

        oi = self.data.open_interest_hist(symbol, s.scanner_oi_period, s.scanner_oi_lookback + 2)
        if oi:
            om = detectors.oi_move(oi, s.scanner_oi_lookback, s.scanner_oi_move_pct)
            if om:
                pct, det = om
                add(EventType.OI_SURGE if pct >= 0 else EventType.OI_DROP, pct, det)

        fe = detectors.funding_extreme(funding, s.scanner_funding_abs)
        if fe:
            fr, det = fe
            add(EventType.FUNDING, fr, det)

        return events

    # ---------------------------------------------------------- 한 사이클

    def scan_once(self) -> list[ScanEvent]:
        now = datetime.now(timezone.utc)
        symbols = self._refresh_universe(time.monotonic())
        if not symbols:
            log.warning("스캔 대상 유니버스가 비어있음")
            return []

        tickers = self.data.all_24h_tickers() or {}
        fundings = self.data.all_funding_rates() or {}

        new_events: list[ScanEvent] = []
        for symbol in symbols:
            pair = symbol.replace("/", "")
            try:
                evs = self._detect_symbol(symbol, fundings.get(pair),
                                          tickers.get(pair), now)
            except Exception as e:  # noqa: BLE001 — 한 심볼 실패가 전체를 막지 않게
                log.debug("심볼 스캔 실패 %s: %s", symbol, e)
                continue
            for ev in evs:
                self.store.record(ev)
                new_events.append(ev)

        if new_events:
            self.store.save()
            self._notify(new_events)
        else:
            # 쿨다운 타임스탬프 유지 위해 주기적으로도 저장
            self.store.save()
        log.info("스캔 완료: %d 심볼, 새 이벤트 %d건", len(symbols), len(new_events))
        return new_events

    def _notify(self, events: list[ScanEvent]) -> None:
        """심볼별로 묶어 한 메시지로 전송(알림 폭주 방지)."""
        by_symbol: dict[str, list[ScanEvent]] = {}
        for ev in events:
            by_symbol.setdefault(ev.symbol, []).append(ev)
        for symbol, evs in by_symbol.items():
            title = f"🛰️ 시장 이벤트 · {symbol}"
            lines = [f"{e.etype.emoji} {e.etype.label} — {e.detail}" for e in evs]
            self.notifier.notify("\n".join(lines), NotifyLevel.TRADE, title=title)

    # ------------------------------------------------------------ 루프

    def run_forever(self) -> None:
        interval = max(30, self.s.scanner_interval_sec)
        log.info("시장 스캐너 시작 — 주기 %ds", interval)
        while True:
            try:
                self.scan_once()
            except KeyboardInterrupt:
                raise
            except Exception as e:  # noqa: BLE001
                log.error("스캔 사이클 오류: %s", e)
            time.sleep(interval)


def _closed_vol_ratio(volumes: list[float], lookback: int) -> float:
    """직전(닫힌) 캔들 거래량 / 그 이전 lookback 평균. 데이터 부족 시 0."""
    if len(volumes) < lookback + 2:
        return 0.0
    closed = volumes[-2]                    # 마지막(-1)은 진행 중 → 그 앞이 닫힌 캔들
    base = volumes[-2 - lookback:-2]
    avg = sum(base) / len(base) if base else 0.0
    return closed / avg if avg > 0 else 0.0


def _fmt_vol(usd: float | None) -> str:
    """거래대금(USD)을 사람이 읽기 좋게. 예: $12M, $340K, $1.2B."""
    if not usd:
        return "?"
    if usd >= 1e9:
        return f"${usd / 1e9:.1f}B"
    if usd >= 1e6:
        return f"${usd / 1e6:.0f}M"
    if usd >= 1e3:
        return f"${usd / 1e3:.0f}K"
    return f"${usd:.0f}"


def _fmt_price(p: float) -> str:
    if p >= 100:
        return f"{p:,.2f}"
    if p >= 1:
        return f"{p:.3f}"
    return f"{p:.6f}"
