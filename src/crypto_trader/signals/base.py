"""시그널 공통 타입.

모든 개별 시그널은 -1.0 ~ +1.0 점수를 낸다.
  +1.0 = 강한 롱, -1.0 = 강한 숏, 0.0 = 중립.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Direction(str, Enum):
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"

    @classmethod
    def from_score(cls, score: float, threshold: float) -> "Direction":
        if score >= threshold:
            return cls.LONG
        if score <= -threshold:
            return cls.SHORT
        return cls.FLAT


@dataclass
class SignalResult:
    """개별 시그널의 출력."""

    name: str
    score: float  # -1.0 ~ +1.0
    detail: dict = field(default_factory=dict)

    def clamped(self) -> "SignalResult":
        self.score = max(-1.0, min(1.0, self.score))
        return self


def clamp(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))
