"""슬리브(sleeve) 정의 — 자본 배분·타임프레임·전략·평가주기.

계좌를 시간 지평별로 나눈 독립 운용 단위.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..config import Settings


@dataclass
class Sleeve:
    name: str                 # swing / mid / scalp
    allocation: float         # 계좌 배분 비율 (0~1)
    signal_tf: str            # 시그널 타임프레임
    confirm_tf: str           # 확인(상위) 타임프레임
    strategy_kind: str        # 'regime' | 'scalp'
    eval_interval_sec: int    # 평가 주기(초)
    symbols: list[str] = field(default_factory=list)
    twap_slices: int = 1      # TWAP 분할 수 (진입 시)

    def allocated_equity(self, total_equity: float) -> float:
        return total_equity * self.allocation


def default_sleeves(settings: Settings) -> list[Sleeve]:
    """설계 문서 기준 기본 3-슬리브 구성 (50/25/25)."""
    symbols = settings.symbols
    return [
        Sleeve(
            name="swing", allocation=0.50,
            signal_tf="4h", confirm_tf="1d",
            strategy_kind="swing",            # RSI 20/80 역추세 → 슈퍼트렌드 피라미딩
            eval_interval_sec=4 * 3600,
            symbols=symbols, twap_slices=3,
        ),
        Sleeve(
            name="mid", allocation=0.25,
            signal_tf="15m", confirm_tf="1h",
            strategy_kind="mid",              # 상위TF 추세 + 하위TF 눌림목
            eval_interval_sec=15 * 60,
            symbols=symbols, twap_slices=1,
        ),
        Sleeve(
            name="scalp", allocation=0.25,
            signal_tf="1m", confirm_tf="5m",
            strategy_kind="scalp",
            eval_interval_sec=60,
            symbols=symbols, twap_slices=3,
        ),
    ]
