"""solbot 전용 솔라나 키페어 생성 (사장님 PC에서 1회 실행).

⚠️ 보안: 이 봇 전용 새 지갑을 만든다. **절대 사장님 메인 Phantom 시드를 봇에 넣지 않는다.**
   생성된 개인키는 `secret.json`(gitignore됨)에만 저장되고, 저장소엔 올라가지 않는다.
   최악의 경우도 이 지갑에 충전한 $100로 손실이 격리된다.

사용:
  pip install solders base58
  python sideprojects/solbot/keygen.py

출력:
  - 공개주소(이 주소로 Phantom에서 $100치 SOL 전송)
  - secret.json (봇이 라이브 서명에 사용, Solana id.json 배열 포맷)
  - Phantom 가져오기용 base58 문자열(선택 — 지갑앱에서 관리·감시하고 싶을 때)
"""
from __future__ import annotations

import json
from pathlib import Path

SECRET = Path(__file__).parent / "secret.json"


def main() -> None:
    try:
        from solders.keypair import Keypair
        import base58
    except ImportError:
        print("의존성이 필요합니다:  pip install solders base58")
        return

    if SECRET.exists():
        print(f"[중단] 이미 {SECRET} 가 존재합니다. 덮어쓰면 기존 지갑 키를 잃습니다.")
        print("       새로 만들려면 기존 파일을 수동으로 백업/삭제 후 다시 실행하세요.")
        return

    kp = Keypair()
    pub = str(kp.pubkey())
    secret_bytes = bytes(kp.to_bytes())            # 64바이트(seed32+pub32)

    SECRET.write_text(json.dumps(list(secret_bytes)))
    try:
        SECRET.chmod(0o600)
    except Exception:  # noqa: BLE001
        pass

    print("=" * 60)
    print("✅ 봇 전용 지갑 생성 완료")
    print("=" * 60)
    print(f"공개주소(입금용):  {pub}")
    print(f"개인키 저장:       {SECRET}  (gitignore됨 — 절대 공유·커밋 금지)")
    print()
    print("Phantom 가져오기(선택):")
    print(f"  {base58.b58encode(secret_bytes).decode()}")
    print()
    print("다음 단계:")
    print(f"  1) Phantom에서 위 '공개주소'로 $100치 SOL 전송")
    print(f"  2) 잔고 확인 후 드라이런/라이브 진행")
    print("⚠️  개인키·secret.json·base58 문자열을 캡처해 채팅에 붙여넣지 마세요.")


if __name__ == "__main__":
    main()
