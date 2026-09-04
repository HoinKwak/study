#!/usr/bin/env python3
"""온체인 산출물 수치 검증기 — 산문에 쓴 수치가 실측(kol_raw.json)과 맞는지 대조.

⚠️매칭은 토큰명이 아니라 **CA 기준**이다 — 토큰명이 빈 문자열로 지워진 전례가 있다.
⚠️실제로 잡은 것: vol24 직전값 이월 인용 · 유동성Δ 누적 오염 40종 · h24 순서 뒤집힘
  (악화를 개선으로 서술) · 실측 부호 반대.
⚠️검증기 자체의 오탐도 즉시 고친다 — 틀린 경보가 진짜 오류를 묻는다.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KOL = Path(__file__).resolve().parents[1] / "kol"
TOOLS = Path(__file__).resolve().parent

NUM = r"[\d,]+(?:\.\d+)?"


def f(s: str) -> float:
    return float(s.replace(",", ""))


def close(a: float, b: float, tol: float = 0.02) -> bool:
    """반올림·자릿수 표기 차이를 흡수한다.

    ⚠️오탐 수정(9/3): vol24 실측 $5.42를 산문이 정상적으로 반올림해 '$5'로 쓴 것을
      오류로 잡았다. 산문은 소수점을 버리고 쓰므로 절대 0.5까지는 표기 차이로 본다.
    """
    return abs(a - b) <= max(abs(b) * tol, 0.5)


def check_token(name, th, m, bad):
    """thesis 한 편을 실측 m과 대조."""
    # 유동성 A→B: B가 이번 실측, A가 직전 실측이어야 한다.
    mm = re.search(rf"유동성.{{0,30}}?\${NUM}\s*→\s*\$({NUM})", th)
    if mm:
        if not close(f(mm.group(1)), m["liq"]):
            bad.append(f"{name} 유동성 종점 ${mm.group(1)} != 실측 ${m['liq']:,.0f}")
        a = re.search(rf"유동성.{{0,30}}?\$({NUM})\s*→", th)
        if a and m["prev_liq"] and not close(f(a.group(1)), m["prev_liq"]):
            bad.append(f"{name} 유동성 시점 ${a.group(1)} != 직전 실측 "
                       f"${m['prev_liq']:,.0f} (2회차 전 값 인용 의심)")
    else:
        mm = re.search(rf"유동성.{{0,30}}?\$({NUM})", th)
        if mm and not close(f(mm.group(1)), m["liq"]):
            bad.append(f"{name} 유동성 ${mm.group(1)} != 실측 ${m['liq']:,.0f}")

    # 유동성 Δ%
    d = re.search(r"유동성.{0,60}?\(([+-]?[\d.]+)%", th)
    if d and m["dliq_pct"] is not None and abs(f(d.group(1)) - m["dliq_pct"]) > 0.35:
        bad.append(f"{name} 유동성Δ {d.group(1)}% != 실측 {m['dliq_pct']:+.1f}%")

    # h1/h6/h24 — 첫 등장 숫자만 본다(뒤따르는 '직전 …%'는 대조 대상이 아니다).
    for k in ("h1", "h6", "h24"):
        for hm in re.finditer(rf"{k}\s*([+-]?[\d.]+)%", th):
            v = float(hm.group(1))
            if m[k] is None:
                bad.append(f"{name} {k} {v}% 인용했으나 실측은 결측")
            elif not close(v, m[k], 0.03):
                bad.append(f"{name} {k} {v}% != 실측 {m[k]:+.2f}%")
            break

    # vol24 / 거래량
    vm = re.search(rf"(?:vol24|거래량)\s*\$({NUM})", th)
    if vm:
        v = f(vm.group(1).rstrip(","))
        if not close(v, m["vol24"], 0.02):
            extra = ""
            if m.get("prev_vol24") and close(v, m["prev_vol24"], 0.02):
                extra = " ← 직전 회차 값 이월 인용"
            bad.append(f"{name} vol24 ${vm.group(1)} != 실측 ${m['vol24']:,.0f}{extra}")

    # 회전율 (조사 붙는 표기 허용: 회전율은/는/이/가)
    tm = re.search(r"회전율(?:은|는|이|가)?\s*([\d.]+)배", th)
    if tm and m["turnover"] is not None and abs(float(tm.group(1)) - m["turnover"]) > 0.06:
        bad.append(f"{name} 회전율 {tm.group(1)}배 != 실측 {m['turnover']}배")

    # 풀 수 / 풀나이
    pm = re.search(r"(\d+)풀", th)
    if pm and int(pm.group(1)) != m["npools"]:
        bad.append(f"{name} 풀수 {pm.group(1)} != 실측 {m['npools']}")
    am = re.search(r"풀나이\s*([\d.]+)일", th)
    if am and m["age_days"] is not None and abs(float(am.group(1)) - m["age_days"]) > 0.15:
        bad.append(f"{name} 풀나이 {am.group(1)}일 != 실측 {m['age_days']}일")


def main() -> int:
    raw = {r["ca"].lower(): r for r in json.loads(Path(sys.argv[1]).read_text())}
    j = json.loads((KOL / "watch.json").read_text())
    bad, unmatched = [], 0

    for t in j["tokens"]:
        m = raw.get((t.get("ca") or "").lower())
        if not m:
            unmatched += 1
            bad.append(f"CA 미매칭: {t.get('token')} {t.get('ca')}")
            continue
        if not m["ok"]:
            continue
        name = t.get("token") or m["token"]
        check_token(name, t.get("thesis", ""), m, bad)

    # 최상급 표현 검증
    # ⚠️오탐 수정(9/3) 3건: ①최상급은 vol24만이 아니라 유동성에도 붙는다(지표 판별 필요)
    #   ②"최하위권/최상위권"은 '권'(범위)이라 최상급 주장이 아니다 — 검사 대상 아님
    #   ③주어가 표 행의 첫 칸이거나 문장 앞쪽 멀리 있다 — 전역 창이 아니라
    #     "행 단위"로 주어를 정해야 한다(전역 90자 창은 표 행에서 주어를 놓쳤다).
    ok = [r for r in raw.values() if r["ok"]]
    ext = {
        ("vol24", "최대"): max(ok, key=lambda r: r["vol24"]),
        ("vol24", "최저"): min(ok, key=lambda r: r["vol24"]),
        ("liq", "최대"): max(ok, key=lambda r: r["liq"]),
        ("liq", "최저"): min(ok, key=lambda r: r["liq"]),
    }
    SUP = re.compile(r"42종중\s*(?:이번회차)?\s*(최대|최고|최저|최소|최하)(?!위권|위)")

    def scan(text: str, subject: str | None, where: str) -> None:
        for mo in SUP.finditer(text):
            kind = "최대" if mo.group(1) in ("최대", "최고") else "최저"
            before = text[max(0, mo.start() - 40):mo.start()]
            metric = ("liq" if ("유동성" in before and "vol24" not in before
                                and "거래량" not in before) else "vol24")
            tgt = ext[(metric, kind)]
            subj = subject
            # ⚠️오탐 수정(9/3): 목록 항목의 주어가 토큰명이 아니라 분류 라벨일 때가 있다
            #   ("- **뒷북 대형 토큰**: CATE(유동성 42종중 최대)…"). 알려진 토큰명이
            #   아니면 주어 미상으로 되돌려, 정답 토큰이 같은 블록에 있으면 통과시킨다.
            if subj is not None and subj not in {r["token"] for r in ok}:
                subj = None
            if subj is None:
                # 최상급 표현 **직전에 나온** 토큰명을 주어로 본다. 블록 아무 데나
                # 정답 토큰이 있으면 통과시키던 예전 방식은 오귀속을 놓쳤다.
                pos = [(text.rfind(r["token"], 0, mo.start()), r["token"]) for r in ok]
                pos = [x for x in pos if x[0] >= 0]
                subj = max(pos)[1] if pos else "?"
            if subj != tgt["token"]:
                bad.append(f"최상급 의심 [{where}] '{mo.group(0)}'({metric}) 주어={subj}"
                           f" — 실제 {metric} {kind}는 {tgt['token']}")

    for t in j["tokens"]:
        scan(t.get("thesis", ""), t.get("token"), "thesis")
    # ⚠️md는 줄바꿈으로 감싸져 있어 주어(토큰명)와 최상급 표현이 다른 줄에 있다
    #   — 줄 단위가 아니라 **블록 단위**(표 행 하나, 또는 '- ' 항목 + 이어지는 줄)로 본다.
    blocks, cur = [], []
    for line in (KOL / "watch.md").read_text().splitlines():
        st = line.strip()
        if st.startswith("|") or st.startswith("- ") or st.startswith("#") or not st:
            if cur:
                blocks.append("\n".join(cur))
            cur = [line] if st else []
        else:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    for b in blocks:
        if not SUP.search(b):
            continue
        subj = None
        first = b.strip().splitlines()[0].strip()
        if first.startswith("|"):
            c = [x.strip().strip("*` ") for x in first.strip("|").split("|")]
            if c:
                subj = c[0].split("(")[0].strip() or None
        elif first.startswith("- **"):
            subj = first[4:].split("**")[0].strip() or None
        scan(b, subj, "md")

    # 다이제스트 경계 플래그 주장 검증
    # ⚠️2026-09-04: 에이전트가 HOOKR를 '매도우위 플래그 해제'라고 3곳에 적었으나
    #   다이제스트는 그 회차에도 플래그를 달고 있었다(h24 +40.41%에 매수3,707/매도3,748).
    #   원인은 **직전 회차 risk 문구("가격-체결방향균형회복")를 이번 상태로 오독**한 것.
    #   플래그 대상은 계측에서 기계적으로 정해지므로 산문 주장과 대조할 수 있다.
    flagged = {r["token"] for r in ok
               if (r["h24"] or 0) > 20 and (r["sells24"] or 0) > (r["buys24"] or 0)}
    _text = ((KOL / "watch.md").read_text() + " "
             + " ".join(t.get("thesis", "") for t in j["tokens"]))
    # ⚠️"매도우위 … 경계신호"는 개별 토큰 서술에도 나오므로 **첫 매치를 쓰면 안 된다**.
    #   종목을 가장 많이 나열한 구간(요약 줄)을 골라 대조한다.
    cands = [m.group(0) for m in
             re.finditer(r"매도우위[^\n]{0,40}?(?:경계\s*신호|경계신호)[^\n]{0,200}", _text)]
    seg = max(cands, key=lambda c: sum(r["token"] in c for r in ok), default=None)
    if seg and flagged and sum(r["token"] in seg for r in ok) >= 2:
        # ⚠️요약 줄은 **빠진 종목을 함께 짚는** 경우가 많다("FLUSH는 이번 회차 명시
        #   플래그가 사라졌다"). 이름이 구간에 있다는 이유만으로 주장 목록에 넣으면
        #   정확한 서술이 오탐된다(9/4 FLUSH). 토큰명 뒤 짧은 범위에 제외 표현이
        #   붙으면 '플래그 아님' 주장으로 본다 — 반대로 진짜 플래그 종목을 이렇게
        #   적으면 named에서 빠져 `누락`으로 잡히므로 HOOKR 유형은 그대로 걸린다.
        #   판정 단위는 **문장**이다 — 고정 글자수로 뒤를 훑으면 다음 문장의 부정어까지
        #   끌어와 정상 나열(…·TOAD 4종이다)이 제외로 오판된다(9/4 TOAD).
        _NEG = re.compile(r"(사라졌|해제|제외|빠졌|없어졌|아니다|아니라|없다)")
        _sents = re.split(r"(?<!\d)\.(?!\d)\s*", seg)
        named = {r["token"] for r in ok
                 for sent in _sents if r["token"] in sent and not _NEG.search(sent)}
        # 제외 주장("X는 플래그가 해제됐다")은 그 자체로 대조한다 — 같은 종목이 구간
        # 다른 문장에 또 나오면 named에도 들어가 `누락` 검사만으로는 안 걸린다.
        denied = {r["token"] for r in ok
                  for sent in _sents if r["token"] in sent and _NEG.search(sent)}
        if denied & flagged:
            bad.append(f"플래그인데 해제됐다고 서술: {sorted(denied & flagged)}")
        missing = flagged - named
        extra = named - flagged
        if missing:
            bad.append(f"매도우위 플래그 주장에서 누락: {sorted(missing)} "
                       f"(다이제스트 플래그 {sorted(flagged)})")
        if extra:
            bad.append(f"매도우위 플래그 아닌데 포함: {sorted(extra)}")
        cnt = re.search(r"\*\*(\d+)종\*\*", seg)
        if cnt and int(cnt.group(1)) != len(flagged):
            bad.append(f"매도우위 플래그 종목수 {cnt.group(1)} != 실제 {len(flagged)}")

    if bad:
        print(f"❌ {len(bad)}건 (CA 미매칭 {unmatched})")
        for b in bad:
            print("  -", b)
        return 1
    print(f"✅ 수치 검증 통과 ({len(j['tokens'])}종목, CA 기준 매칭)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
