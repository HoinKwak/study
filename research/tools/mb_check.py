#!/usr/bin/env python3
"""시장 브리핑 산출물 검증기.

검사: ①flows.json append-only(과거 이력 바이트 보존·중복·역행 없음)
      ②chartist_views.json 인물 6인 고정 ③brief.json 스키마(notable 미포함)
      ④brief.md 구조(섹션 소실·LIT 섹션 필수·제목 번호 금지·분량 붕괴)

⚠️실제로 잡은 것: brief.md 8,136→2,844자(35%)로 4개 섹션 소실(LIT 포함) · 제목 번호 삽입
  · ETF 과거이력 임의수정.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
CHARTISTS = {"Peter Brandt", "KillaXBT", "Benjamin Cowen",
             "Rekt Capital", "TechDev", "Doctor Profit"}


def git_show(path: str, rev: str = "HEAD") -> str | None:
    r = subprocess.run(["git", "show", f"{rev}:{path}"],
                       capture_output=True, text=True, cwd=R.parent)
    return r.stdout if r.returncode == 0 else None


def main() -> int:
    ts = sys.argv[1]
    bad = []

    # ① ETF flows — append-only
    cur = json.loads((R / "etf" / "flows.json").read_text())
    old_txt = git_show("research/etf/flows.json")
    if old_txt:
        old = json.loads(old_txt)
        if len(old.get("source", "")) != len(cur.get("source", "")):
            bad.append(f"flows source 길이 변경 {len(old.get('source',''))}"
                       f"→{len(cur.get('source',''))} (임의 절삭 금지)")
        for k, ov in old.items():
            if not isinstance(ov, list):
                continue
            nv = cur.get(k)
            if not isinstance(nv, list):
                bad.append(f"flows[{k}] 리스트가 아니게 됨")
                continue
            if len(nv) < len(ov):
                bad.append(f"flows[{k}] 길이 감소 {len(ov)}→{len(nv)}")
            elif nv[:len(ov)] != ov:
                for i, (a, b) in enumerate(zip(ov, nv)):
                    if a != b:
                        bad.append(f"flows[{k}][{i}] 과거이력 변조: {a} → {b}")
                        break
    for k, v in cur.items():
        if not isinstance(v, list) or not v or not isinstance(v[0], dict):
            continue
        ds = [x.get("date") for x in v if isinstance(x, dict) and "date" in x]
        if len(ds) != len(set(ds)):
            dup = [d for d in set(ds) if ds.count(d) > 1]
            bad.append(f"flows[{k}] 날짜 중복: {dup[:5]}")
        if ds != sorted(ds):
            bad.append(f"flows[{k}] 날짜 역순/뒤섞임")

    # ② 차티스트 6인 고정
    cv = json.loads((R / "kol" / "chartist_views.json").read_text())
    people = cv if isinstance(cv, list) else (cv.get("chartists") or cv.get("views") or [])
    names = {p.get("name") or p.get("chartist") for p in people if isinstance(p, dict)}
    names.discard(None)
    if names != CHARTISTS:
        bad.append(f"차티스트 인물 변경: 추가={sorted(names - CHARTISTS)} "
                   f"삭제={sorted(CHARTISTS - names)}")

    # ③ brief.json
    bj = json.loads((R / "market" / "brief.json").read_text())
    if bj.get("ts") != ts:
        bad.append(f"brief.json ts {bj.get('ts')} != {ts}")
    for k in ("ts", "market", "assets"):
        if k not in bj:
            bad.append(f"brief.json 키 누락: {k}")
    if "notable" in bj:
        bad.append("brief.json 에 notable 이 있음 (이 파일엔 넣지 않는다)")

    # ④ brief.md 구조
    md = (R / "market" / "brief.md").read_text()
    old_md = git_show("research/market/brief.md")
    heads = re.findall(r"^#{2,3}\s*(.+)$", md, re.M)
    if old_md:
        if len(md) < len(old_md) * 0.6:
            bad.append(f"brief.md 분량 붕괴 {len(old_md):,}→{len(md):,}자")
        old_heads = re.findall(r"^#{2,3}\s*(.+)$", old_md, re.M)
        lost = [h for h in old_heads if h not in heads]
        if lost:
            bad.append(f"brief.md 섹션 소실: {lost}")
    if not any("LIT" in h for h in heads):
        bad.append("brief.md 에 LIT 섹션 없음 (사장님 수동 트레이딩 종목 — 필수)")
    numbered = [h for h in heads if re.match(r"^\d+[.)]\s", h)]
    if numbered:
        bad.append(f"brief.md 제목에 번호 삽입: {numbered}")
    # ⚠️md 헤더는 "2026-09-03 12:15 UTC" 형태라 ISO ts 문자열과 다르다(오탐 원인).
    alt = ts.replace("T", " ").rstrip("Z")[:16]
    if ts not in md and alt not in md:
        bad.append(f"brief.md 에 {ts}({alt}) 없음")

    if bad:
        print(f"❌ {len(bad)}건")
        for b in bad:
            print("  -", b)
        return 1
    print(f"✅ 시장브리핑 검증 통과 (brief.md {len(md):,}자 · 섹션 {len(heads)}개)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
