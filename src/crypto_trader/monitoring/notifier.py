"""알림 발송 — 채널 독립적. 콘솔(항상) + 텔레그램(선택).

레벨(NOTIFY_MIN_LEVEL) 이상만 외부 채널로 전송한다.
텔레그램 토큰이 없으면 콘솔/로그로만 남는다.
"""
from __future__ import annotations

from enum import IntEnum

import requests

from ..config import Settings
from ..utils import get_logger

log = get_logger("notify")


class NotifyLevel(IntEnum):
    INFO = 10    # 시그널/평가 등 일상 정보
    TRADE = 20   # 진입/청산 등 거래 이벤트
    WARN = 30    # 진입 차단, 일일손실한도 등
    ERROR = 40   # 예외/주문 실패

    @classmethod
    def parse(cls, name: str) -> "NotifyLevel":
        return cls.__members__.get(name.strip().upper(), cls.INFO)


class Notifier:
    def __init__(self, settings: Settings):
        self.s = settings
        self.min_level = NotifyLevel.parse(settings.notify_min_level)
        self._session = requests.Session()
        self._tg_enabled = settings.has_telegram
        if self._tg_enabled:
            log.info("텔레그램 알림 활성화")

    def notify(self, message: str, level: NotifyLevel = NotifyLevel.INFO,
               title: str | None = None) -> None:
        text = f"{title}\n{message}" if title else message

        # 콘솔/로그는 항상
        if level >= NotifyLevel.ERROR:
            log.error(text.replace("\n", " | "))
        elif level >= NotifyLevel.WARN:
            log.warning(text.replace("\n", " | "))
        else:
            log.info(text.replace("\n", " | "))

        # 외부 채널은 임계 레벨 이상만
        if level < self.min_level:
            return
        if self._tg_enabled:
            self._send_telegram(text, level)

    def _send_telegram(self, text: str, level: NotifyLevel) -> None:
        emoji = {
            NotifyLevel.INFO: "ℹ️",
            NotifyLevel.TRADE: "💹",
            NotifyLevel.WARN: "⚠️",
            NotifyLevel.ERROR: "🚨",
        }.get(level, "")
        url = f"https://api.telegram.org/bot{self.s.telegram_bot_token}/sendMessage"
        try:
            self._session.post(
                url,
                json={
                    "chat_id": self.s.telegram_chat_id,
                    "text": f"{emoji} {text}",
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
                timeout=10,
            )
        except requests.RequestException as e:
            log.warning("텔레그램 전송 실패: %s", e)

    # 편의 메서드
    def info(self, msg: str, title: str | None = None) -> None:
        self.notify(msg, NotifyLevel.INFO, title)

    def trade(self, msg: str, title: str | None = None) -> None:
        self.notify(msg, NotifyLevel.TRADE, title)

    def warn(self, msg: str, title: str | None = None) -> None:
        self.notify(msg, NotifyLevel.WARN, title)

    def error(self, msg: str, title: str | None = None) -> None:
        self.notify(msg, NotifyLevel.ERROR, title)
