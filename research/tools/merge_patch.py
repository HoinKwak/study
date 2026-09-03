#!/usr/bin/env python3
"""선물 브리핑 — 서사 패치를 스테이징에 머지해 발행본을 만든다.

사용: merge_patch.py <narrative_patch.json> <brief_staging.json> <out brief.json>

⚠️인자 순서 사고 전례: 예전 도구는 `merge(patch, brief)`가 정순인데 반대로 넘겨
  market·themes가 직전 회차 값으로 덮여쓴 적이 있다. 그래서 이 도구는 인자를
  파일 내용으로 판별하고(패치엔 overrides, 스테이징엔 cex/dex가 있다) 뒤바뀌면 거부한다.
⚠️오버라이드 매칭 사고 전례: 부분일치 폴백이 Binance venue 문자열에 든 "OKX" 때문에
  OKX 오버라이드를 Binance 항목에도 적용해 25건이 39건으로 번졌다.
  → 접두 일치를 먼저 쓰고, 0건일 때만 부분일치로 내려간다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def vkey(e: dict) -> str:
    return (e.get("venue") or e.get("protocol") or "")


def main() -> int:
    patch = json.loads(Path(sys.argv[1]).read_text())
    stag = json.loads(Path(sys.argv[2]).read_text())
    out = Path(sys.argv[3])

    if "overrides" not in patch or "cex" not in stag:
        print("❌ 인자 순서가 뒤바뀌었습니다: merge_patch.py <패치> <스테이징> <출력>")
        return 2

    if patch.get("market"):
        stag["market"] = patch["market"]
    if patch.get("themes"):
        stag["themes"] = patch["themes"]

    rows = stag["cex"] + stag["dex"]
    applied, unmatched = 0, []
    for o in patch.get("overrides", []):
        sym, ven = o.get("symbol"), (o.get("venue") or "")
        cand = [e for e in rows if e.get("symbol") == sym]
        hit = [e for e in cand if vkey(e).split("(")[0].lower() == ven.split("(")[0].lower()]
        if not hit:                       # 접두가 안 맞을 때만 부분일치로 내려간다
            hit = [e for e in cand if ven and ven.split("(")[0].lower() in vkey(e).lower()]
        if not hit and len(cand) == 1:
            hit = cand
        if not hit:
            unmatched.append(f"{sym}/{ven}")
            continue
        for e in hit:
            if o.get("why"):
                e["why"] = o["why"]
            if o.get("tag"):
                e["tag"] = o["tag"]
            applied += 1

    out.write_text(json.dumps(stag, ensure_ascii=False, indent=1))
    print(f"오버라이드 {applied}건 적용 · 미매칭 {len(unmatched)}건"
          + (f" ({', '.join(unmatched[:8])})" if unmatched else ""))
    print(f"market {len(stag.get('market') or '')}자 · themes {len(stag.get('themes') or [])}건"
          f" · cex {len(stag['cex'])} · dex {len(stag['dex'])} → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
