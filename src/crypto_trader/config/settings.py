"""환경변수(.env) → 타입 안전한 설정 객체.

pydantic-settings 로 .env 를 읽어 검증한다. 어디서든 `get_settings()` 로 접근.
"""
from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class TradeMode(str, Enum):
    DRY_RUN = "dry_run"  # 주문 안 냄, 로그만
    PAPER = "paper"      # 테스트넷에 실제 주문
    LIVE = "live"        # 실전 자금


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- 바이낸스 ---
    binance_api_key: str = ""
    binance_api_secret: str = ""
    binance_testnet: bool = True

    # --- 코인글래스 ---
    coinglass_api_key: str = ""

    # --- 실행 모드 ---
    trade_mode: TradeMode = TradeMode.DRY_RUN

    # --- 매매 대상 ---
    # NoDecode: pydantic-settings 의 자동 JSON 파싱을 끄고 아래 validator 로 쉼표 분리.
    symbols: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    )
    timeframe: str = "15m"
    loop_interval_sec: int = 60

    # --- 리스크 ---
    max_leverage: int = 3
    risk_per_trade_pct: float = 1.0
    max_open_positions: int = 3
    daily_max_loss_pct: float = 5.0

    # --- 시그널 / 전략 ---
    entry_score_threshold: float = 0.5
    exit_flip_threshold: float = 0.4   # 반대 시그널 강도 이 값 이상이면 조기 청산
    atr_stop_mult: float = 1.5         # 손절 거리 = ATR × 이 값
    reward_risk_ratio: float = 1.5     # 익절 = 손절거리 × 이 값 (R배수)

    # --- 알림 (텔레그램, 선택) ---
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    notify_min_level: str = "INFO"  # INFO / TRADE / WARN / ERROR

    # --- 상태 저장 ---
    state_dir: str = "state"

    # --- 로깅 ---
    log_level: str = "INFO"

    @property
    def has_telegram(self) -> bool:
        return bool(self.telegram_bot_token and self.telegram_chat_id)

    @field_validator("symbols", mode="before")
    @classmethod
    def _split_symbols(cls, v):
        """`BTC/USDT,ETH/USDT` 같은 쉼표 문자열도 리스트로 파싱."""
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    @property
    def has_binance_keys(self) -> bool:
        return bool(self.binance_api_key and self.binance_api_secret)

    @property
    def has_coinglass_key(self) -> bool:
        return bool(self.coinglass_api_key)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """설정 싱글턴. 프로세스 전체에서 한 번만 로드."""
    return Settings()
