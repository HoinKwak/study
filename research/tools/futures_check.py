#!/usr/bin/env python3
"""선물 브리핑 산출물 검증기 — 발행본(brief.md/json)의 수치·방향을 digest와 대조.

⚠️표 헤더를 읽어 **칼럼별로** 대조한다(위치로 고정하면 칼럼 순서가 바뀔 때 조용히 틀린다).
⚠️실제로 잡은 것: 이월 `직전 why` 칼럼에서 수치를 가져온 오류(ENA·CRV·CASHCAT·MON·LIT)
  · 방향 모순 이월 서사 · 실측 부호 반대.
⚠️검증기 자체의 오탐도 즉시 고친다 — 틀린 경보가 진짜 오류를 묻는다.
   과거 고친 오탐: "낙폭이 축소"(완화 표현) · 펀딩 절이 소수점에서 끊김
   · chg24 절이 가격방향 서술로 번짐 · 이력 절("A%에서 B%로") · 다단계 체인(A→B→C)
   · 최상급에 교정절이 붙은 경우("최저는 X").
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FUT = Path(__file__).resolve().parents[1] / "futures"

# 하락을 뜻하는 말 / 상승을 뜻하는 말
DOWN = ("하락", "급락", "낙폭", "약세", "내림", "하방", "마이너스", "음전", "빠졌", "밀렸")
UP = ("상승", "급등", "강세", "오름", "상방", "플러스", "양전", "올랐", "뛰었")
# 방향 판정에서 제외할 완화 표현 — "낙폭이 축소"는 하락 주장이 아니다
MITIG = re.compile(r"(낙폭|하락세|약세)(?:이|가|은|는|도)?\s*(축소|진정|완화|둔화|멈춤)")


def f(s: str) -> float:
    return float(s.replace(",", "").replace("%", "").replace("+", ""))


def parse_tables(md: str) -> list[dict]:
    """마크다운 표를 헤더 기준 dict 리스트로 파싱한다."""
    rows, hdr = [], None
    for line in md.splitlines():
        if not line.strip().startswith("|"):
            hdr = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            continue
        if hdr is None:
            hdr = cells
            continue
        if len(cells) == len(hdr):
            rows.append(dict(zip(hdr, cells)))
    return rows


def col(row: dict, *names) -> str | None:
    for k, v in row.items():
        kl = k.lower()
        if any(n in kl for n in names):
            return v
    return None


def check(rows: list[dict], digest: dict, bad: list, label: str) -> None:
    """⚠️벤뉴 간 chg24는 비교 금지다 — 같은 심볼도 벤뉴마다 값이 다르므로
       표의 벤뉴 칼럼으로 좁혀서 대조하고, 벤뉴를 못 찾으면 그 심볼의
       어느 벤뉴 값과도 맞지 않을 때만 오류로 본다."""
    for r in rows:
        sym = (col(r, "심볼", "종목", "symbol") or "").strip("`* ")
        sym = sym.split("(")[0].strip()
        if not sym:
            continue
        byv = digest.get(sym.upper())
        if not byv:
            continue
        vcell = (col(r, "벤뉴", "거래소", "venue") or "").strip()
        cands = [v for k, v in byv.items() if vcell and k.split("(")[0].lower() in vcell.lower()]
        d = cands[0] if cands else None
        for field, keys in (("chg24", ("chg24", "24h", "변동")),
                            ("funding", ("펀딩", "funding")),
                            ("oi", ("oi", "미결제")),
                            ("vol24", ("거래대금", "거래량", "vol"))):
            cell = col(r, *keys)
            if cell is None:
                continue
            m = re.search(r"[-+]?[\d,]+(?:\.\d+)?", cell)
            if not m:
                continue
            got = f(m.group(0))
            pool = [d] if d else list(byv.values())
            exps = [float(x[field]) for x in pool if x.get(field) is not None]
            if not exps:
                continue
            floor = 0.0005 if field == "funding" else 0.02
            if not any(abs(got - e) <= max(abs(e) * 0.02, floor) for e in exps):
                bad.append(f"[{label}] {sym} {field} {m.group(0)} != digest "
                           + "/".join(f"{e:g}" for e in exps))


def _strip_clauses(t: str) -> str:
    """수치 인용이 아닌 절을 지운다 — 이력절·직전값·괄호주석."""
    t = re.sub(r"\([^)]*\)", " ", t)                       # 괄호 주석
    t = re.sub(r"[^→|]{0,80}?에서\s*[-+]?[\d.]+%?\s*로", " ", t)  # "A에서 B로"
    t = re.sub(r"직전[^,·—.]{0,40}", " ", t)                # "직전 …"
    t = re.sub(r"([-+]?[\d.]+%\s*→\s*)+", " ", t)          # 다단계 체인 A→B→C
    return t


def check_direction(md: str, digest: dict, bad: list) -> None:
    """산문에서 종목의 방향 서술이 실측 chg24 부호와 모순되는지 본다."""
    for line in md.splitlines():
        if line.strip().startswith("|") or not line.strip():
            continue
        t = _strip_clauses(line)
        for sym, byv in digest.items():
            all_c = [float(v["chg24"]) for v in byv.values() if v.get("chg24") is not None]
            # ⚠️벤뉴마다 부호가 갈리는 종목(CHIP Gate +12 vs MEXC -10)은 판정하지 않는다.
            #   다만 변동이 미미한 벤뉴 하나 때문에 검사가 통째로 꺼지면 안 되므로
            #   |chg|>=1%인 벤뉴들만 모아 부호 합의를 본다.
            chgs = [c for c in all_c if abs(c) >= 1.0]
            if not chgs or len({c > 0 for c in chgs}) != 1:
                continue
            if any(abs(c) >= 1.0 and (c > 0) != (chgs[0] > 0) for c in all_c):
                continue
            # ⚠️`\b`는 한글 조사에서 경계가 되지 않는다 — "BTC는"의 C와 는 사이는
            #   둘 다 \w라 \b가 성립하지 않아 방향 검사가 통째로 무력화됐다.
            for mo in re.finditer(rf"(?<![A-Za-z0-9]){re.escape(sym)}(?![A-Za-z0-9])", t):
                seg = t[mo.end():mo.end() + 40]
                if MITIG.search(seg):
                    continue
                up = any(w in seg for w in UP)
                dn = any(w in seg for w in DOWN)
                if up == dn:
                    continue
                if up != (chgs[0] > 0):
                    bad.append(f"[방향] {sym} 서술 '{seg.strip()[:32]}' "
                               f"vs 실측 {'/'.join(f'{c:+.2f}%' for c in chgs)}")
                break


def main() -> int:
    ts = sys.argv[1]
    st = json.loads(Path(sys.argv[2]).read_text())  # build_digest.py의 brief_staging.json
    digest: dict[str, dict[str, dict]] = {}
    for side in ("cex", "dex"):
        for e in st.get(side, []):
            key = e.get("venue") or e.get("protocol") or side
            digest.setdefault((e.get("symbol") or "").upper(), {})[key] = {
                "chg24": e.get("chg24"),
                "funding": (e["funding"] * 100) if e.get("funding") is not None else None,
                "oi": (e["oi_usd"] / 1e6) if e.get("oi_usd") else None,
                "vol24": (e["vol24_usd"] / 1e6) if e.get("vol24_usd") else None,
            }
    bad = []

    bj = json.loads((FUT / "brief.json").read_text())
    if bj.get("ts") != ts:
        bad.append(f"brief.json ts {bj.get('ts')} != {ts}")
    for k in ("ts", "market", "cex", "dex", "themes"):
        if k not in bj:
            bad.append(f"brief.json 키 누락: {k}")

    md = (FUT / "brief.md").read_text()
    alt = ts.replace("T", " ").rstrip("Z")[:16]
    if ts not in md and alt not in md:
        bad.append(f"brief.md 에 {ts}({alt}) 없음")

    check(parse_tables(md), digest, bad, "md표")
    check_direction(md, digest, bad)

    # 주식화 토큰 혼입
    EQ = set("NVDA SPY SOXL MU SNDK SKHYNIX TSLA AAPL GOLD SILVER OIL WTI".split())
    for side in ("cex", "dex"):
        for e in bj.get(side, []):
            s = (e.get("symbol") or "").upper().split(":")[-1].lstrip("K")
            if s in EQ or s.endswith("-USD-STOCK"):
                bad.append(f"[{side}] 주식화/상품 토큰 혼입: {e.get('symbol')}")

    if bad:
        print(f"❌ {len(bad)}건")
        for b in bad:
            print("  -", b)
        return 1
    print(f"✅ 선물 브리핑 검증 통과 (md {len(md):,}자)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
