"""텔레그램 알림 설정 도우미.

    # 1) 봇과 대화 시작 후 chat_id 자동 탐지 (토큰만 있으면 됨)
    python -m scripts.telegram_setup --discover-chat-id

    # 2) .env 에 TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID 넣은 뒤 테스트 전송
    python -m scripts.telegram_setup --test

설정 방법:
  1. 텔레그램에서 @BotFather 검색 → /newbot → 안내대로 봇 생성 → 토큰 복사
  2. .env 에 TELEGRAM_BOT_TOKEN=<토큰> 입력
  3. 생성한 봇과 대화창을 열고 아무 메시지나 전송 (예: "hi")
  4. python -m scripts.telegram_setup --discover-chat-id 실행 → chat_id 확인
  5. .env 에 TELEGRAM_CHAT_ID=<chat_id> 입력, NOTIFY_MIN_LEVEL=TRADE 권장
  6. python -m scripts.telegram_setup --test 로 수신 확인
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import requests  # noqa: E402

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.monitoring import Notifier, NotifyLevel  # noqa: E402


def discover_chat_id(token: str) -> None:
    if not token:
        print("TELEGRAM_BOT_TOKEN 이 .env 에 없습니다. 먼저 토큰을 입력하세요.")
        sys.exit(1)
    resp = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=10)
    data = resp.json()
    if not data.get("ok"):
        print("텔레그램 API 오류:", data)
        sys.exit(1)
    updates = data.get("result", [])
    if not updates:
        print("수신된 메시지가 없습니다. 봇과 대화창에서 아무 메시지나 먼저 보내세요.")
        return
    seen = {}
    for u in updates:
        msg = u.get("message") or u.get("channel_post") or {}
        chat = msg.get("chat", {})
        if chat.get("id") is not None:
            seen[chat["id"]] = chat.get("title") or chat.get("username") or chat.get("first_name")
    print("발견된 chat_id:")
    for cid, name in seen.items():
        print(f"  {cid}  ({name})")
    print("\n위 chat_id 를 .env 의 TELEGRAM_CHAT_ID 에 입력하세요.")


def main() -> None:
    parser = argparse.ArgumentParser(description="텔레그램 알림 설정")
    parser.add_argument("--discover-chat-id", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    s = get_settings()
    if args.discover_chat_id:
        discover_chat_id(s.telegram_bot_token)
        return
    if args.test:
        if not s.has_telegram:
            print("텔레그램 미설정: TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID 를 .env 에 넣으세요.")
            sys.exit(1)
        n = Notifier(s)
        n.notify("✅ crypto-trader 텔레그램 알림 테스트 — 정상 수신되면 성공입니다.",
                 NotifyLevel.TRADE, title="🤖 연결 테스트")
        print("전송 시도 완료. 텔레그램을 확인하세요.")
        return
    parser.print_help()


if __name__ == "__main__":
    main()
