"""바이낸스 smart-money(신 리더보드) API 진단 — 로컬 실행.

2026-07 개편된 실제 엔드포인트(DevTools로 확인):
- 목록:   GET bapi/futures/v1/friendly/future/smart-money/top-trader/list?...
- 프로필: GET bapi/asset/v1/friendly/future/smart-money/profile?topTraderId=...
- 포지션: GET bapi/asset/v1/private/future/smart-money/profile/query-positions?topTraderId=...  (/private/=인증 가능성)

★인증 없는 최소 헤더★로 공개 접근 여부·응답 구조를 확인한다(로그인 쿠키 미사용).
실행: python -m scripts.probe_binance_leaderboard  → 출력 전체를 붙여주세요.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

_H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept": "*/*",
      "clienttype": "web", "content-type": "application/json", "lang": "en", "bnc-location": "KR"}
_LIST = ("https://www.binance.com/bapi/futures/v1/friendly/future/smart-money/top-trader/list"
         "?page=1&rows=10&timeRange=30D&rankingType=PNL&onlyShowSharingPosition=true"
         "&onlyShowSignalEnabled=false&order=DESC")
_PROFILE = "https://www.binance.com/bapi/asset/v1/friendly/future/smart-money/profile?topTraderId=%s"
_POS = ("https://www.binance.com/bapi/asset/v1/private/future/smart-money/profile/query-positions"
        "?topTraderId=%s&marketType=UM&page=1&rows=9")


def _get(url: str):
    req = urllib.request.Request(url, headers=_H)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:  # noqa: BLE001
            return e.code, {"raw": str(e)[:200]}
    except Exception as e:  # noqa: BLE001
        return None, {"error": str(e)}


def main() -> None:
    print("=" * 64)
    print("1) top-trader/list (30D PNL 상위, /friendly)")
    st, d = _get(_LIST)
    print("HTTP:", st, "| code:", d.get("code"), "| msg:", d.get("message"))
    data = d.get("data")
    # data 구조가 list거나 {list:[...]} 형태일 수 있음
    rows = data if isinstance(data, list) else (data or {}).get("list") if isinstance(data, dict) else None
    if not rows:
        print("data 구조:", json.dumps(d, ensure_ascii=False)[:500]); print("=" * 64); return
    print(f"트레이더 {len(rows)}명. 첫 항목 키:", list(rows[0].keys()))
    print("첫 항목 샘플:", json.dumps(rows[0], ensure_ascii=False)[:500])
    tid = rows[0].get("topTraderId") or rows[0].get("id")
    if not tid:
        print("(topTraderId 필드 못 찾음 — 위 키 참고)"); print("=" * 64); return

    print(f"\n2) profile?topTraderId={tid} (/friendly)")
    st2, d2 = _get(_PROFILE % tid)
    print("HTTP:", st2, "| msg:", d2.get("message"))
    if isinstance(d2.get("data"), dict):
        print("profile 키:", list(d2["data"].keys()))
        print("profile 샘플:", json.dumps(d2["data"], ensure_ascii=False)[:500])

    print(f"\n3) query-positions?topTraderId={tid} (/private ← 인증필요 여부 관건)")
    st3, d3 = _get(_POS % tid)
    print("HTTP:", st3, "| code:", d3.get("code"), "| msg:", d3.get("message"))
    pd = d3.get("data")
    plist = pd if isinstance(pd, list) else (pd or {}).get("list") if isinstance(pd, dict) else None
    if plist:
        print("포지션 첫 항목 키:", list(plist[0].keys()))
        print("포지션 샘플:", json.dumps(plist[0], ensure_ascii=False)[:500])
    else:
        print("포지션 응답(인증필요면 여기서 실패/빈값):", json.dumps(d3, ensure_ascii=False)[:400])
    print("=" * 64)


if __name__ == "__main__":
    main()
