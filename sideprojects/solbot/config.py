"""solbot 설정 — 솔라나 밈코인 자동매매(드라이런 우선).

리스크·전략 파라미터는 사장님 결정값이다. 여기 값만 바꾸면 동작이 바뀐다.
※ 실제 자금이 걸리므로 DRY_RUN=True(드라이런)로 검증한 뒤에만 라이브로 전환한다.
"""
from __future__ import annotations

import os
from pathlib import Path

# ── 자본·사이징 (사장님 결정) ────────────────────────────────────────────────
PORTFOLIO_START_USD = 100.0     # 시작 자본(실제 충전한 SOL 가치와 맞출 것)
PER_TRADE_PCT = 0.05            # 트레이드당 포트폴리오 5%
MAX_CONCURRENT = 20             # 동시 보유 최대 20개 (5%×20=100% 완전투입 상한)
DAILY_LOSS_LIMIT_PCT = 0.30     # 일일 실현손실 이 %면 당일 신규진입 중단(킬스위치)

# ── 진입 필터 (러그·저유동·짜바리 방어) ──────────────────────────────────────
MIN_LIQUIDITY_USD = 30_000.0    # DexScreener 풀 유동성 최소치
MAX_PRICE_IMPACT_PCT = 3.0      # 진입 견적 가격영향(슬리피지) 상한 %
MIN_BUY_SIGNAL_USD = 1_000.0    # 스마트머니 매수 신호 최소 규모(밈월렛 MIN_USD와 정렬)
MAX_TOKEN_AGE_OK = True         # (예약) 신생토큰 허용 여부

# ── 청산 (3-A 반자동 기본; trailing/fixed도 파라미터 준비) ────────────────────
EXIT_MODE = "assist"            # assist(반자동:알림+승인) | trailing | fixed
TP_PCT = 0.50                   # fixed 익절 +50%
SL_PCT = 0.30                   # fixed/assist 손절 -30% (assist에선 강제알림 트리거)
TRAIL_PCT = 0.25               # trailing 신고가 대비 -25%
MAX_HOLD_HOURS = 48             # 안전판: 이 시간 넘으면 청산 알림/청산

# ── 실행 모드 ────────────────────────────────────────────────────────────────
DRY_RUN = True                  # True=실제 스왑 안 함(페이퍼). 검증 후에만 False.
DEFAULT_SLIPPAGE_BPS = 150      # 스왑 슬리피지 허용치(1.5%)

# ── 파일 경로 ────────────────────────────────────────────────────────────────
STATE_DIR = Path(__file__).parent / "state"
JOURNAL = STATE_DIR / "paper_journal.json"      # 페이퍼 포지션·실현손익 저널

# ── 워시트레이딩/데이터동결 의심 심볼(KOL 워치 플래그 재사용, 소프트 필터) ──────
#   ※ 심볼 기반이라 완벽치 않음. 라이브 전 mint 기반 블랙리스트로 강화 예정.
BLACKLIST_SYMBOLS = {"401K", "CASHDOG", "MYSTERY", "530A", "JOHN", "LITTLE JOHN"}


def env(key: str, default: str = "") -> str:
    """.env/환경변수 조회(라이브 서명키 등). 드라이런에선 불필요."""
    return os.environ.get(key, default)
