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
    """설계 문서 기준 기본 3-슬리브 구성 (50/25/25)."""
    symbols = settings.symbols
    # 단타는 동적 유니버스: 24h 거래대금 $100M 이상 전 페어 (회전율 확보).
    # 스퀴즈 필터가 진입을 강하게 거르므로 유니버스를 넓혀 신호 빈도를 복구한다.
    # (settings.symbols 는 유니버스 조회 실패 시 폴백으로만 사용)
    scalp_symbols = [s for s in symbols if s.split("/")[0] != "SOL"]
    return [
        Sleeve(
            name="swing", allocation=0.50,
            signal_tf="4h", confirm_tf="1d",
            strategy_kind="swing",            # RSI 20/80 역추세 → 슈퍼트렌드 피라미딩
            eval_interval_sec=4 * 3600,
            symbols=symbols, twap_slices=3, leverage=10,
        ),
        Sleeve(
            name="mid", allocation=0.25,
            signal_tf="15m", confirm_tf="1h",
            strategy_kind="mid",              # 1h 추세 + 15m 볼린저 눌림목 평균회귀
            eval_interval_sec=15 * 60,
            symbols=symbols, twap_slices=1, leverage=5,
        ),
        Sleeve(
            name="scalp", allocation=0.25,
            # 1m → 5m 상향: 백테스트 결과 1m 모멘텀은 수수료를 못 이김
            # (5m + vol 4배가 최선: 승률 68%). TWAP 3슬라이스 = 15분 창.
            signal_tf="5m", confirm_tf="15m",
            strategy_kind="scalp",
            eval_interval_sec=5 * 60,
            # 증거금 기준 사이징($15k 명목) → 충격 완화 위해 10분할 × 10초 시간분산.
            symbols=scalp_symbols, twap_slices=10, slice_interval_sec=10,
            leverage=30, maker_entry=False,
            dynamic_universe=True, min_universe_volume=50e6,
        ),
    ]
