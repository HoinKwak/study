#!/usr/bin/env python3
"""온체인 산출물 구조 검증기 — watch.{json,csv,md} 3파일 정합.

⚠️실제로 잡은 것: CSV 9열(쉼표 따옴표 누락)·7열(단계 열 누락) · 종목 1개 통째 누락(41 vs 42)
  · 빈 토큰명 · md 분량 붕괴(16,854→11,977자).
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

KOL = Path(__file__).resolve().parents[1] / "kol"
NCOL = 8
KEYS = {"token", "chain", "ca", "stage", "kols", "thesis", "risk"}


def main() -> int:
    ts = sys.argv[1]
    expect = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    # ⚠️직전 분량은 git에서 직접 읽는다 — 수동 인자로 넘기면 바이트/문자 단위를
    #   섞어 비교하게 되고(9/3 실제 발생) 분량 붕괴를 놓친다.
    g = subprocess.run(["git", "show", "HEAD:research/kol/watch.md"],
                       capture_output=True, text=True, cwd=KOL.parents[1])
    prev_md = len(g.stdout) if g.returncode == 0 else 0
    bad = []

    j = json.loads((KOL / "watch.json").read_text())
    if j.get("ts") != ts:
        bad.append(f"json ts {j.get('ts')} != {ts}")
    toks = j.get("tokens") or []
    if len(toks) != expect:
        bad.append(f"json tokens {len(toks)} != {expect}")
    for i, t in enumerate(toks):
        miss = KEYS - set(t)
        if miss:
            bad.append(f"json[{i}] 키 누락 {sorted(miss)}")
        if not (t.get("token") or "").strip():
            bad.append(f"json[{i}] 토큰명 비어 있음 (ca={t.get('ca')})")
        if not (t.get("thesis") or "").strip():
            bad.append(f"json[{i}] {t.get('token')} thesis 비어 있음")
        if t.get("stage") not in ("조기", "확산", "뒷북"):
            bad.append(f"json[{i}] {t.get('token')} stage 값 이상: {t.get('stage')}")
    if "notable" in j and not isinstance(j["notable"], list):
        bad.append("json notable 이 리스트가 아님")

    rows = list(csv.reader((KOL / "watch.csv").read_text().splitlines()))
    for i, r in enumerate(rows):
        if len(r) != NCOL:
            bad.append(f"csv 행{i + 1} 열수 {len(r)} != {NCOL}: {r[:3]}")
    if len(rows) - 1 != expect:
        bad.append(f"csv 데이터행 {len(rows) - 1} != {expect}")

    jn = [t["token"] for t in toks]
    cn = [r[0] for r in rows[1:]]
    if set(jn) != set(cn):
        bad.append(f"json/csv 종목 집합 불일치: json전용={sorted(set(jn) - set(cn))} "
                   f"csv전용={sorted(set(cn) - set(jn))}")

    md = (KOL / "watch.md").read_text()
    if ts not in md:
        bad.append(f"md 헤더에 {ts} 없음")
    if prev_md and len(md) < prev_md * 0.6:
        bad.append(f"md 분량 붕괴: {len(md):,}자 (직전 {prev_md:,}자의 "
                   f"{len(md) / prev_md * 100:.0f}%)")
    for n in jn:
        if n not in md:
            bad.append(f"md에 종목 {n} 없음")

    if bad:
        print(f"❌ {len(bad)}건")
        for b in bad:
            print("  -", b)
        return 1
    print(f"✅ 구조 검증 통과 (종목 {expect} · csv {NCOL}열 · md {len(md):,}자)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
