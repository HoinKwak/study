"""바이낸스 smart-money 목록 파라미터 진단 — 로컬 실행(지역차단 없는 사장님 PC).

대시보드 Binance가 비는 원인 특정용. onlyShowSharingPosition(true/false)·rows(10/20/50)·
rankingType(PNL/ROI) 조합별로 실제 rows가 오는지 본다. 어떤 조합이 rows>0인지 확인 후
그 파라미터로 커넥터를 고정한다.

실행: python -m scripts.probe_binance_list   → 출력 전체를 붙여주세요.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

_BASE = "https://www.binance.com/bapi/futures/v1/friendly/future/smart-money/top-trader/list"
_H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept": "*/*",
      "clienttype": "web", "content-type": "application/json", "lang": "en", "bnc-location": "KR"}


def _get(url: str):
    req = urllib.request.Request(url, headers=_H)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:  # noqa: S310
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:  # noqa: BLE001
            return e.code, {"raw": str(e)[:200]}
    except Exception as e:  # noqa: BLE001
        return None, {"error": str(e)}


def _qs(rows: int, ranking: str, sharing: str) -> str:
    return (f"?page=1&rows={rows}&timeRange=30D&rankingType={ranking}"
            f"&onlyShowSharingPosition={sharing}&onlyShowSignalEnabled=false&order=DESC")


def main() -> None:
    cases = [
        ("커넥터현재  sharing=false rows=60 PNL", 60, "PNL", "false"),
        ("probe성공  sharing=true  rows=10 PNL", 10, "PNL", "true"),
        ("변형A      sharing=true  rows=20 PNL", 20, "PNL", "true"),
        ("변형B      sharing=true  rows=50 PNL", 50, "PNL", "true"),
        ("변형C      sharing=true  rows=20 ROI", 20, "ROI", "true"),
        ("변형D      sharing=false rows=20 PNL", 20, "PNL", "false"),
    ]
    print("=" * 72)
    for name, rows, ranking, sharing in cases:
        st, d = _get(_BASE + _qs(rows, ranking, sharing))
        data = d.get("data") if isinstance(d, dict) else None
        rws = data.get("rows") if isinstance(data, dict) else None
        n = len(rws) if isinstance(rws, list) else rws
        print(f"{name} | HTTP {st} | code {d.get('code')} | msg {d.get('message')} | rows={n}")
        if isinstance(rws, list) and rws:
            r0 = rws[0]
            print(f"    예: {r0.get('traderName')} pnl={r0.get('pnl')} roi={r0.get('roi')} "
                  f"assets={r0.get('assets')} posStatus={r0.get('positionStatus')}")
    print("=" * 72)
    print("→ rows>0 나오는 조합을 알려주시면 그 파라미터로 커넥터를 고정합니다.")


if __name__ == "__main__":
    main()
