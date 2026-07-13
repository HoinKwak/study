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
    strategy_kind: str        # 'regime' | 'scalp' | 'mid' | 'swing'
    eval_interval_sec: int    # 평가 주기(초)
    symbols: list[str] = field(default_factory=list)
    twap_slices: int = 1      # TWAP 분할 수 (진입 시)
    slice_interval_sec: int = 0  # 분할 슬라이스 간 대기(초). >0 이면 시간분산 진입
    leverage: int = 3         # 슬리브 레버리지 상한 (isolated)
    maker_entry: bool = False  # True=post-only 지정가(메이커), False=시장가(테이커)
    # 동적 유니버스: 24h 거래대금 기준 고유동성 페어를 자동 선별해 symbols 대체
    dynamic_universe: bool = False
    min_universe_volume: float = 100e6   # 거래대금 하한 (USD)

    def allocated_equity(self, total_equity: float) -> float:
        return total_equity * self.allocation


def default_sleeves(settings: Settings) -> list[Sleeve]:
    """단타 전용 단일 구성 (15m), 포트폴리오 100%.

    중기·스윙은 손익비(엣지)가 안 나와 제외(정의는 git 이력에 있어 필요 시 복원 가능).
    거래량 임계값 스윕 결과 **15m·유니버스 30M** 이 엣지 최대(PF≈1.06). 3·5·10분은
    전 구간 약함, 10M 는 잡알트 희석으로 손실 → 15m 단독·30M 채택.
    (settings.symbols 는 유니버스 조회 실패 시 폴백으로만 사용)
    사이징은 증거금 기준이라 allocation 은 표시용(단일 슬리브라 1.0).
    """
    symbols = settings.symbols
    scalp_symbols = [s for s in symbols if s.split("/")[0] != "SOL"]

    # 증거금 기준 사이징 → 충격 완화 위해 10분할 시간분산. 메이커(post-only) 진입.
    return [
        Sleeve(
            name="scalp", allocation=1.0,
            signal_tf="15m", confirm_tf="1h",
            strategy_kind="scalp", eval_interval_sec=15 * 60,
            symbols=scalp_symbols, twap_slices=10, slice_interval_sec=20,
            leverage=settings.major_leverage, maker_entry=True,
            dynamic_universe=True, min_universe_volume=30e6,
        ),
    ]
