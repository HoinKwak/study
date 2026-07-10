"""시그널 가중 합산 엔진.

기술지표 점수 + 파생 데이터 점수를 카테고리 가중치로 합쳐
최종 방향(LONG/SHORT/FLAT)과 강도를 결정한다.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .base import Direction, SignalResult, clamp

# 카테고리 가중치 (합 1.0). 코인글래스 미구독 → 바이낸스 지표만 사용.
DEFAULT_WEIGHTS = {
    "technical": 0.55,
    "derivatives": 0.45,
}


@dataclass
class AggregatedSignal:
    symbol: str
    score: float                       # -1.0 ~ +1.0
    direction: Direction
    components: list[SignalResult] = field(default_factory=list)

    def summary(self) -> str:
        comp = ", ".join(f"{c.name}={c.score:+.2f}" for c in self.components)
        return f"{self.symbol} score={self.score:+.3f} → {self.direction.value.upper()} [{comp}]"


class SignalAggregator:
    def __init__(self, weights: dict[str, float] | None = None,
                 entry_threshold: float = 0.5):
        self.weights = weights or dict(DEFAULT_WEIGHTS)
        self.entry_threshold = entry_threshold

    def aggregate(self, symbol: str, components: list[SignalResult]) -> AggregatedSignal:
        total = 0.0
        weight_sum = 0.0
        for c in components:
            w = self.weights.get(c.name, 0.0)
            if w <= 0:
                continue
            total += w * c.score
            weight_sum += w

        score = clamp(total / weight_sum) if weight_sum > 0 else 0.0
        direction = Direction.from_score(score, self.entry_threshold)
        return AggregatedSignal(symbol, score, direction, components)
