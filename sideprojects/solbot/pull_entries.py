"""엔트리 추출 (사장님 PC에서 1회 실행 — Helius 키 필요).

277개 스마트머니 지갑의 **과거 베이스→밈 매수 ≥$MIN**를 Helius 주소 SWAP 이력에서 뽑아
백테스트용 엔트리 신호로 저장한다. 실제 매수신호를 그대로 재구성 → "따라 샀으면?" 검증의 입력.

왜 PC에서 도나: Helius 키가 로컬 .env에만 있어(클라우드 미보유) 여기서만 히스토리를 뽑을 수 있다.
출력 `state/entries.json` 을 커밋/전달하면, 청산 시뮬·집계는 클라우드(backtest.py)가 수행한다.

사용:
  .\.venv\Scripts\Activate.ps1
  python sideprojects\memewallet\..\solbot\pull_entries.py     # 또는 solbot 폴더에서 python pull_entries.py
키: .env HELIUS_API_KEY (기존 밈월렛과 동일).
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# 밈월렛의 Helius 헬퍼·매수판별 재사용
_MW = Path(__file__).resolve().parents[1] / "memewallet"
sys.path.insert(0, str(_MW))
import ws_alert as W          # extract_buy, parse는 tx단위 — 여기선 주소 이력 엔드포인트 사용
from alert_bot import MIN_USD, _env

SINCE_ISO = "2026-06-01T00:00:00Z"        # 백테스트 시작일(사장님 지정)
OUT = Path(__file__).parent / "state" / "entries.json"
_ADDR = "https://api.helius.xyz/v0/addresses/{w}/transactions/?api-key={k}&type=SWAP&limit=100"


def _wallets() -> list[str]:
    data = json.loads((_MW / "smart_wallets.json").read_text())
    return [w["wallet"] for w in data]


def pull_wallet(wallet: str, key: str, since_ts: int) -> list[dict]:
    """지갑 1개의 SINCE 이후 베이스→밈 매수(≥MIN_USD) 목록."""
    out: list[dict] = []
    before = None
    while True:
        url = _ADDR.format(w=wallet, k=key)
        if before:
            url += f"&before={before}"
        try:
            txs = W._get_json(url)
        except Exception as e:  # noqa: BLE001
            print(f"  [경고] {wallet[:6]} 조회 실패: {str(e)[:80]}")
            break
        if not isinstance(txs, list) or not txs:
            break
        stop = False
        for tx in txs:
            ts = int(tx.get("timestamp") or 0)      # unix seconds
            if ts and ts < since_ts:
                stop = True
                break
            buy = W.extract_buy(tx, wallet)          # {mint, bought, usd} | None (≥MIN_USD 내부판정)
            if buy:
                out.append({"wallet": wallet, "mint": buy["mint"], "ts": ts,
                            "usd": round(buy["usd"], 2), "tokens": buy["bought"],
                            "sig": tx.get("signature")})
        before = txs[-1].get("signature")
        if stop or len(txs) < 100:
            break
        time.sleep(0.15)      # 예의상 딜레이
    return out


def main() -> None:
    key = _env("HELIUS_API_KEY")
    if not key:
        print("[오류] .env에 HELIUS_API_KEY가 없습니다.")
        return
    since_ts = int(datetime.fromisoformat(SINCE_ISO.replace("Z", "+00:00")).timestamp())
    wallets = _wallets()
    print(f"엔트리 추출 시작: {len(wallets)}지갑, {SINCE_ISO} 이후, ≥${MIN_USD:,.0f} 베이스→밈 매수")
    all_entries: list[dict] = []
    for i, w in enumerate(wallets, 1):
        es = pull_wallet(w, key, since_ts)
        all_entries.extend(es)
        if i % 20 == 0 or es:
            print(f"  [{i}/{len(wallets)}] {w[:6]}… +{len(es)}건 (누적 {len(all_entries)})")
    all_entries.sort(key=lambda e: e["ts"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"since": SINCE_ISO, "min_usd": MIN_USD,
                               "pulled_at": datetime.now(timezone.utc).isoformat(),
                               "n": len(all_entries), "entries": all_entries},
                              ensure_ascii=False, indent=1))
    uniq_tokens = len({e["mint"] for e in all_entries})
    print(f"\n완료: 엔트리 {len(all_entries)}건, 고유토큰 {uniq_tokens}개 → {OUT}")
    print("이 파일을 커밋/전달하면 클라우드에서 백테스트를 돌립니다:")
    print("  git add sideprojects/solbot/state/entries.json -f && git commit -m 'solbot 엔트리 데이터' && git push")


if __name__ == "__main__":
    main()
