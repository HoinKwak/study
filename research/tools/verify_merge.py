#!/usr/bin/env python3
"""머지 결과가 직전 발행본을 되돌려 놓지 않았는지 확인한다.

사용: verify_merge.py <merged brief.json> [ts]

⚠️전례: 인자 순서를 반대로 넘겨 market·themes가 직전 회차 값으로 덮여썼다.
  '오버라이드 0건 적용인데 미매칭도 0건'이라는 모순 출력이 유일한 단서였다.
  → 머지 후 market/themes가 직전 회차와 **다른지** 반드시 대조한다.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]


def main() -> int:
    new = json.loads(Path(sys.argv[1]).read_text())
    ts = sys.argv[2] if len(sys.argv) > 2 else None
    g = subprocess.run(["git", "show", "HEAD:research/futures/brief.json"],
                       capture_output=True, text=True, cwd=R)
    bad = []
    if g.returncode == 0:
        old = json.loads(g.stdout)
        if new.get("market") and new["market"] == old.get("market"):
            bad.append("market 이 직전 회차와 완전히 동일 — 머지 인자 순서 의심")
        if new.get("themes") and new["themes"] == old.get("themes"):
            bad.append("themes 가 직전 회차와 완전히 동일 — 머지 인자 순서 의심")
        if new.get("ts") == old.get("ts"):
            bad.append(f"ts 가 직전과 동일({new.get('ts')})")
    if ts and new.get("ts") != ts:
        bad.append(f"ts {new.get('ts')} != {ts}")
    if not new.get("market"):
        bad.append("market 이 비어 있음")
    blank = sum(1 for e in new["cex"] + new["dex"] if not (e.get("why") or "").strip())
    if bad:
        print("❌ " + "\n❌ ".join(bad))
        return 1
    print(f"✅ 머지 검증 통과 (why 비어있음 {blank}건)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
