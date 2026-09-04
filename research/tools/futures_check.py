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
    # ⚠️소수점에서 끊기면 "직전 회차 -11.10% 급락"의 '급락'이 살아남아 오탐이 된다
    #   (펀딩 절이 소수점에서 끊기던 것과 같은 부류). 숫자 앞의 점은 절 안으로 본다.
    # ⚠️가운뎃점도 마찬가지다 — "직전 DashCon·shielded베타 촉매발 급등"에서 절이
    #   DashCon에서 끊겨 과거 촉매의 '급등'이 이번 회차 주장으로 오탐됐다(9/4).
    #   다만 "직전 -3.2% 하락·이번 +5.1% 상승"처럼 가운뎃점이 **다음 주장**을 여는
    #   경우까지 삼키면 진짜 오류를 놓치므로, 뒤에 부호·숫자가 오는 점에서는 끊는다.
    #   또 '이번 …'이 시작되면 거기서부터는 이번 회차 주장이므로 절을 끊는다.
    t = re.sub(r"직전(?:(?!이번)(?:[^,·—.]|\.(?=\d)|·(?![-+\d]))){0,40}", " ", t)
    t = re.sub(r"([-+]?[\d.]+%\s*→\s*)+", " ", t)          # 다단계 체인 A→B→C
    # ⚠️"2회 연속 상승 흐름이 …", "2회 연속 큰 낙폭 이후 …"는 **과거 추세** 서술이라
    #   그 안의 방향어를 이번 회차 주장으로 보면 안 된다(9/4 오탐 7건의 원인).
    t = re.sub(r"\d+\s*회(?:차)?\s*(?:연속|이상)(?:[^,·—.]|\.(?=\d)){0,30}", " ", t)
    # "…던/…되던 <방향어> 흐름"처럼 과거 지속을 가리키는 수식절도 이번 회차 주장이 아니다
    #   (9/4: "10회차 이상 이어지던 CEX 최대 낙폭 흐름"이 CAP 반등 서술에서 오탐을 냈다).
    t = re.sub(r"(?:이어지|지속되|계속되)던(?:[^,·—.]|\.(?=\d)){0,30}", " ", t)
    return t


def real_moves(prev_path: str | None, cur_path: str | None) -> dict[str, list[float]]:
    """직전·이번 가격 스냅샷으로 종목별 실측%(회차 대비 실제 변동)를 만든다.

    ⚠️브리핑 서술의 주 근거는 chg24(24h 롤링)가 아니라 **실측%**다.
      chg24로 방향을 판정하면 둘이 어긋나는 종목에서 전건 오탐이 난다
      (9/3: ZEC chg24 +18.6% vs 실측 +2.12%, APR chg24 +17.4% vs 실측 -11.10%).
    """
    if not prev_path or not cur_path:
        return {}
    prev = json.loads(Path(prev_path).read_text())
    cur = json.loads(Path(cur_path).read_text())
    out: dict[str, list[float]] = {}
    for k, c in cur.items():
        p = prev.get(k)
        if not p or not c:
            continue
        sym = k.split(":", 1)[1].upper()
        out.setdefault(sym, []).append((float(c) / float(p) - 1) * 100)
    return out


def _basis_at(seg: str, pos: int) -> str | None:
    """방향어 하나의 판정 기준을, **그 앞에 마지막으로 나온 지표 이름**으로 정한다.

    ⚠️문장 단위로 "실측이 있으면 실측 기준"이라고만 보면, 두 지표를 **대비**하는
      서술("chg24는 +4.67%로 플러스인데 실측(2h)은 -4.95%로 하락")에서 chg24에 붙은
      '플러스'까지 실측으로 판정해 오탐이 난다(9/4 CHIP·MUBARAK).
      방향어마다 바로 앞의 지표를 보면 둘 다 올바르게 갈린다.
    """
    head = seg[:pos]
    i_real = max(head.rfind("실측"), head.rfind("실시간"))
    i_chg = max(head.rfind("chg24"), head.rfind("24h"))
    if i_real < 0 and i_chg < 0:
        return None
    return "real" if i_real > i_chg else "chg"


def _logical_lines(md: str):
    """목록 항목과 그 이어지는 들여쓰기 줄을 **한 문장으로 합쳐** 내보낸다.

    ⚠️발행본은 줄바꿈으로 감싸져 있어 "**CHIP**…: chg24 …" 다음 줄에 "…로 뚜렷한
      하락 전환입니다"가 온다. 줄 단위로 보면 심볼이 있는 줄엔 방향어가 없고 방향어가
      있는 줄엔 심볼이 없어 **방향 검사가 통째로 건너뛰어졌다**(9/4 주입 테스트로 발각).
    """
    buf: list[str] = []
    for line in md.splitlines():
        if not line.strip() or line.strip().startswith("|"):
            if buf:
                yield " ".join(buf)
                buf = []
            continue
        if line[:1] in (" ", "\t") and buf:
            buf.append(line.strip())
        else:
            if buf:
                yield " ".join(buf)
            buf = [line.strip()]
    if buf:
        yield " ".join(buf)


SYMS: re.Pattern | None = None


def check_direction(md: str, digest: dict, real: dict, bad: list) -> None:
    """산문의 방향 서술이 실측 부호와 모순되는지 본다.

    문장이 chg24를 명시했을 때만 chg24를 기준으로 삼는다.
    """
    global SYMS
    # 3글자 이상 심볼만 경계로 쓴다(ID·CA 같은 2글자 티커는 흔한 문자열과 겹친다)
    SYMS = re.compile("|".join(sorted(
        (rf"(?<![A-Za-z0-9]){re.escape(k)}(?![A-Za-z0-9])"
         for k in digest if len(k) >= 3), key=len, reverse=True)))
    for line in _logical_lines(md):
        t = _strip_clauses(line)
        # ⚠️서술의 주 근거는 실측%다. 한 문장에 둘 다 나오면(예: "실측 -5.40%로 하락.
        #   chg24는 +11.09%로 여전히 플러스") 방향어는 실측에 붙으므로 실측을 기준으로 본다.
        # 지표 이름이 방향어 앞에 없을 때 쓰는 줄 단위 기본값
        dflt = "chg" if (("chg24" in line or "24h" in line)
                         and "실측" not in line) else "real"
        for sym, byv in digest.items():
            pools = {"chg": [float(v["chg24"]) for v in byv.values()
                             if v.get("chg24") is not None],
                     "real": list(real.get(sym) or [])}
            if not pools["real"]:
                pools["real"] = pools["chg"]      # 실측이 없으면 chg24로 갈음
            # ⚠️벤뉴마다 부호가 갈리는 종목(CHIP Gate +12 vs MEXC -10)은 판정하지 않는다.
            #   다만 변동이 미미한 벤뉴 하나 때문에 검사가 통째로 꺼지면 안 되므로
            #   |chg|>=1%인 벤뉴들만 모아 부호 합의를 본다.
            agree = {}
            for b, all_c in pools.items():
                cs = [c for c in all_c if abs(c) >= 1.0]
                if cs and len({c > 0 for c in cs}) == 1:
                    agree[b] = cs
            if not agree:
                continue
            # ⚠️`\b`는 한글 조사에서 경계가 되지 않는다 — "BTC는"의 C와 는 사이는
            #   둘 다 \w라 \b가 성립하지 않아 방향 검사가 통째로 무력화됐다.
            for mo in re.finditer(rf"(?<![A-Za-z0-9]){re.escape(sym)}(?![A-Za-z0-9])", t):
                # ⚠️고정 60자 창은 줄 병합 뒤 문장이 길어지면 방향어에 닿지 못한다
                #   ("…chg24 …플러스지만 실측은 … 하락 전환입니다"에서 '하락'이 창 밖).
                #   문장 끝까지 보되, **다음 종목 서술이 시작되면 거기서 끊어** 남의
                #   방향어를 이 종목 주장으로 읽지 않게 한다.
                seg = t[mo.end():mo.end() + 200]
                mdot = re.search(r"(?<!\d)\.(?!\d)", seg)
                if mdot:
                    seg = seg[:mdot.start()]
                nxt = SYMS.search(seg) if SYMS else None
                if nxt:
                    seg = seg[:nxt.start()]
                # ⚠️"2회 연속 상승 흐름이 이번 회차 -1.15%로 꺾였다"처럼 앞 절이 **과거 추세**를
                #   서술하는 문장이 흔하다. '이번 회차/이번엔' 뒤부터가 이번 관측이므로
                #   그 표지가 있으면 뒤쪽만 방향 판정에 쓴다(9/4 오탐 7건의 원인).
                cut = re.search(r"이번\s*(?:회차|엔|은|라운드)", seg)
                if cut:
                    seg = seg[cut.end():]
                if MITIG.search(seg):
                    continue
                # 방향어를 위치와 함께 모아, 각자의 앞 지표로 기준을 나눈다.
                #   대비 서술("chg24는 …플러스인데 실측은 …하락")에서 두 방향어가
                #   서로 다른 지표를 가리키므로, 기준별로 따로 판정해야 한다.
                hits = [(m.start(), w in UP)
                        for w in UP + DOWN
                        for m in re.finditer(re.escape(w), seg)]
                hit = False
                for b, cs in agree.items():
                    sel = [u for pos, u in hits
                           if (_basis_at(seg, pos) or dflt) == b]
                    if not sel or len(set(sel)) != 1:
                        continue
                    if sel[0] != (cs[0] > 0):
                        label = "실측" if b == "real" else "chg24"
                        bad.append(f"[방향] {sym} 서술 '{seg.strip()[:32]}' "
                                   f"vs {label} "
                                   + "/".join(f"{c:+.2f}%" for c in cs))
                        hit = True
                if hit:
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

    real = real_moves(sys.argv[3] if len(sys.argv) > 3 else None,
                      sys.argv[4] if len(sys.argv) > 4 else None)
    check(parse_tables(md), digest, bad, "md표")
    check_direction(md, digest, real, bad)

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
