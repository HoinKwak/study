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
    """단타 전용 3-타임프레임 구성 (3m / 5m / 10m), 포트폴리오 100%.

    중기·스윙은 손익비(엣지)가 안 나와 제외한다(정의는 git 이력에 있어 필요 시 복원 가능).
    단타는 동적 유니버스(24h 거래대금 $30M 이상)에서 3개 타임프레임으로 신호 빈도를 넓힌다.
    (settings.symbols 는 유니버스 조회 실패 시 폴백으로만 사용)
    사이징은 증거금 기준이라 allocation 은 표시용이며, 합이 1.0(=100%)이 되게 둔다.
    """
    symbols = settings.symbols
    scalp_symbols = [s for s in symbols if s.split("/")[0] != "SOL"]

    def _scalp(name: str, signal_tf: str, confirm_tf: str,
               alloc: float, eval_sec: int) -> Sleeve:
        # 증거금 기준 사이징 → 충격 완화 위해 10분할 × 20초 시간분산.
        # 메이커(post-only) 진입: 수수료 절감. 미체결분은 시장가 폴백.
        # 10m 는 비네이티브 → 워커가 5m 에서 리샘플.
        return Sleeve(
            name=name, allocation=alloc,
            signal_tf=signal_tf, confirm_tf=confirm_tf,
            strategy_kind="scalp", eval_interval_sec=eval_sec,
            symbols=scalp_symbols, twap_slices=10, slice_interval_sec=20,
            leverage=settings.major_leverage, maker_entry=True,
            dynamic_universe=True, min_universe_volume=30e6,
        )

    # 5m 슬리브는 기존 이름 'scalp' 유지(진행 중 포지션 연속성 보존).
    return [
        _scalp("scalp3m",  "3m",  "15m", 0.34, 3 * 60),
        _scalp("scalp",    "5m",  "15m", 0.33, 5 * 60),
        _scalp("scalp10m", "10m", "30m", 0.33, 10 * 60),
    ]
