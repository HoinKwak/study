"""시장 이벤트 모델 + 영속 저장소(쿨다운 중복 억제 포함).

스캐너가 포착한 급등/급락/거래량급증/OI급증/펀딩극단 이벤트를
JSON(state/scanner_events.json)에 롤링 저장하고, 같은 (심볼·타입) 이벤트가
쿨다운 안에 다시 뜨면 중복 알림을 막는다. 대시보드는 이 파일을 읽어 표시한다.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class EventType(str, Enum):
    PUMP = "PUMP"            # 급등
    DUMP = "DUMP"            # 급락
    VOL_SPIKE = "VOL_SPIKE"  # 거래량 급증
    OI_SURGE = "OI_SURGE"    # OI 급증
    OI_DROP = "OI_DROP"      # OI 급감
    FUNDING = "FUNDING"      # 펀딩비 극단

    @property
    def label(self) -> str:
        return {
            EventType.PUMP: "급등",
            EventType.DUMP: "급락",
            EventType.VOL_SPIKE: "거래량 급증",
            EventType.OI_SURGE: "OI 급증",
            EventType.OI_DROP: "OI 급감",
            EventType.FUNDING: "펀딩 극단",
        }[self]

    @property
    def emoji(self) -> str:
        return {
            EventType.PUMP: "🚀",
            EventType.DUMP: "🔻",
            EventType.VOL_SPIKE: "📊",
            EventType.OI_SURGE: "🟢",
            EventType.OI_DROP: "🔴",
            EventType.FUNDING: "💰",
        }[self]


@dataclass
class ScanEvent:
    symbol: str            # 'BTC/USDT'
    type: str              # EventType.value
    value: float           # 대표 수치(변동% / 배수 / 펀딩비)
    price: float           # 감지 시 가격
    detail: str            # 사람이 읽는 요약(부가 지표 포함)
    ts: str                # ISO8601 (UTC)

    @property
    def etype(self) -> EventType:
        return EventType(self.type)

    def key(self) -> str:
        return f"{self.symbol}|{self.type}"

    def to_line(self) -> str:
        """텔레그램/콘솔용 한 줄 요약."""
        e = self.etype
        return f"{e.emoji} <b>{self.symbol}</b> {e.label} — {self.detail}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class EventStore:
    """이벤트 롤링 저장 + (심볼·타입) 쿨다운."""
    path: Path
    max_events: int = 400
    events: list[ScanEvent] = field(default_factory=list)
    _cooldowns: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, state_dir: str, max_events: int = 400) -> "EventStore":
        path = Path(state_dir) / "scanner_events.json"
        store = cls(path=path, max_events=max_events)
        if path.exists():
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                store.events = [ScanEvent(**e) for e in raw.get("events", [])]
                store._cooldowns = dict(raw.get("cooldowns", {}))
            except (json.JSONDecodeError, TypeError, ValueError):
                pass
        return store

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, Any] = {
            "events": [asdict(e) for e in self.events[-self.max_events:]],
            "cooldowns": self._cooldowns,
        }
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def on_cooldown(self, symbol: str, etype: EventType, cooldown_min: int,
                    now: datetime | None = None) -> bool:
        """이 (심볼·타입)이 아직 쿨다운 중이면 True."""
        key = f"{symbol}|{etype.value}"
        last = self._cooldowns.get(key)
        if not last:
            return False
        now = now or datetime.now(timezone.utc)
        try:
            last_dt = datetime.fromisoformat(last)
        except ValueError:
            return False
        return (now - last_dt).total_seconds() < cooldown_min * 60

    def record(self, event: ScanEvent) -> None:
        """이벤트를 저장하고 쿨다운 타임스탬프 갱신."""
        self.events.append(event)
        self._cooldowns[event.key()] = event.ts
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]

    def recent(self, limit: int = 50) -> list[ScanEvent]:
        return self.events[-limit:][::-1]
