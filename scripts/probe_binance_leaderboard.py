"""바이낸스 리더보드 API 진단 — 로컬(바이낸스 접속 가능)에서 실행해 실제 응답 구조/차단여부 확인.

실행: python -m scripts.probe_binance_leaderboard   (또는 python scripts/probe_binance_leaderboard.py)
출력 전체를 복사해 주시면 커넥터를 실제 응답에 맞춰 고칩니다.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

_BASE = "https://www.binance.com/bapi/futures/v1/public/future/leaderboard"
_HDR = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json", "Accept": "*/*"}


def _post(path: str, body: dict):
    req = urllib.request.Request(_BASE + path, data=json.dumps(body).encode(), headers=_HDR)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:  # noqa: BLE001
            return e.code, {"raw": str(e)}
    except Exception as e:  # noqa: BLE001
        return None, {"error": str(e)}


def main() -> None:
    print("=" * 60)
    print("1) getLeaderboardRank (통산 PnL 상위)")
    st, d = _post("/getLeaderboardRank", {
        "isShared": True, "isTrader": False, "periodType": "ALL",
        "statisticsType": "PNL", "tradeType": "PERPETUAL",
    })
    print("HTTP:", st, "| code:", d.get("code"), "| msg:", d.get("message"))
    data = d.get("data")
    if isinstance(data, list) and data:
        print(f"상위 트레이더 {len(data)}명. 첫 항목 키:", list(data[0].keys()))
        print("첫 항목 샘플:", json.dumps(data[0], ensure_ascii=False)[:400])
        uid = data[0].get("encryptedUid")
        if uid:
            print("\n2) getOtherPosition (첫 트레이더 포지션)")
            st2, d2 = _post("/getOtherPosition", {"encryptedUid": uid, "tradeType": "PERPETUAL"})
            print("HTTP:", st2, "| code:", d2.get("code"), "| msg:", d2.get("message"))
            pd = (d2.get("data") or {})
            plist = pd.get("otherPositionRetList")
            if isinstance(plist, list) and plist:
                print("포지션 첫 항목 키:", list(plist[0].keys()))
                print("포지션 샘플:", json.dumps(plist[0], ensure_ascii=False)[:400])
            else:
                print("포지션 데이터 구조:", json.dumps(pd, ensure_ascii=False)[:400])
    else:
        print("리더보드 data 없음 — 전체 응답(차단/구조 확인용):")
        print(json.dumps(d, ensure_ascii=False)[:600])
    print("=" * 60)


if __name__ == "__main__":
    main()
