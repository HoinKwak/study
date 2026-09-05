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
    # ⚠️오탐 수정(9/5 09:00Z): 여러 회차 이력을 화살표로 나열하면
    #   "(+8.22%→-13.37%→+14.68%)"처럼 **첫 값이 과거 회차 값**이다. 이번 회차 값은
    #   마지막이므로 화살표 사슬이면 끝 값을 쓴다(kol_digest 기준선 A→B와 같은 부류이나
    #   이번엔 항이 셋이라 '마지막'을 취해야 한다).
    #   실제 형태는 화살표만이 아니라 각 항에 회차 라벨이 붙는다:
    #   "증가최대(+8.22%,2회차전)→감소최대(-13.37%,직전)→…(+14.68%, $…)".
    #   → **뒤에 과거 회차 표지가 붙은 값은 건너뛰고** 남는 첫 값을 이번 회차 값으로 본다.
    # ⚠️회차 라벨은 구분자가 매 회차 바뀐다(9/5 11:00Z): 9/4엔 "(+8.22%,2회차전)"처럼
    #   괄호 안 쉼표였는데 이번엔 "+8.22%(3회차전)"처럼 **% 뒤에 괄호가 열린다**.
    #   여는 괄호를 안 받아 과거 값을 이번 값으로 읽고 오탐을 냈다.
    _PAST = r"\s*[,()\[]?\s*(?:\d+회차\s*전|직전|전회|과거)"
    dpos = th.find("유동성")
    if dpos >= 0 and m["dliq_pct"] is not None:
        seg = th[dpos:dpos + 200]
        cur = None
        for mo in re.finditer(r"\(?([+-][\d.]+)%", seg):
            if re.match(_PAST, seg[mo.end():]):
                continue
            cur = mo.group(1)
            break
        if cur is not None and abs(f(cur) - m["dliq_pct"]) > 0.35:
            bad.append(f"{name} 유동성Δ {cur}% != 실측 {m['dliq_pct']:+.1f}%")

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
    # ⚠️오탐 수정(9/4 13:00Z): "2풀→1풀"·"22풀에서 21풀로"처럼 **전이를 서술**하면
    #   앞 값은 직전 회차 값이다. 첫 매치를 잡아 CYBERCAT·CYBERLEEK·HOOKR 3건이
    #   오탐났다(kol_digest 기준선 A→B에서 B를 쓰도록 고친 것과 같은 부류).
    pm = (re.search(r"\d+풀\s*(?:→|->)\s*(\d+)풀", th)
          or re.search(r"\d+풀에서\s*(\d+)풀", th)
          or re.search(r"(\d+)풀", th))
    if pm and int(pm.group(1)) != m["npools"]:
        bad.append(f"{name} 풀수 {pm.group(1)} != 실측 {m['npools']}")
    # ⚠️md와 같은 이유로 thesis의 '변동없음' 주장도 직전 풀수와 대조한다(9/5 11:00Z).
    pn0 = m.get("prev_npools")
    if pn0 is not None and pn0 != m["npools"] and re.search(r"풀\s*\(?변동\s*없음", th):
        bad.append(f"{name} thesis '변동없음' 주장 != 실제 {pn0}풀→{m['npools']}풀 변동")
    # ⚠️회차 대조(9/5 15:00Z 신설): 발행본 "N회차"가 기준선+1과 맞는지 본다.
    #   기준선이 없는(회차 미확인) 종목은 검사하지 않는다.
    rn = m.get("round_no")
    rm = re.match(r"\s*(\d+)\s*회차", th)
    if rn is not None and rm and int(rm.group(1)) != rn:
        bad.append(f"{name} thesis 회차 {rm.group(1)} != 기준선+1 {rn}")
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

    # md 상세줄의 구조 필드(풀수·풀나이) 대조
    # ⚠️공백 메움(9/4 13:00Z): 풀수 검사가 watch.json의 thesis만 봐서
    #   md 상세줄("- **TOAD** (Solana/PumpSwap, CA `…`, 16풀, 풀나이 27.0일)")의
    #   오기는 통째로 지나쳤다. 구조 필드 이월(BARRON 7풀 건)이 바로 이 부류다.
    by_ca = {r["ca"].lower(): r for r in raw.values()}
    mdtxt = (KOL / "watch.md").read_text()
    for mo in re.finditer(
            r"^- \*\*(?P<tok>[^*]+)\*\*\s*\([^)]*?`(?P<ca>0x[0-9a-fA-F]+|[1-9A-HJ-NP-Za-km-z]+)`"
            r"[^)]*?,\s*(?P<np>\d+|단일)풀(?:,\s*풀나이\s*(?P<age>[\d.]+)일)?",
            mdtxt, re.M):
        m = by_ca.get(mo.group("ca").lower())
        if not m or not m["ok"]:
            continue
        rn2 = m.get("round_no")
        seg_r = mdtxt[mo.end():mo.end() + 120]
        rm2 = re.search(r"(\d+)\s*회차", seg_r)
        if rn2 is not None and rm2 and int(rm2.group(1)) != rn2:
            bad.append(f"{mo.group('tok')} md 회차 {rm2.group(1)} != 기준선+1 {rn2}")
        np_txt = mo.group("np")            # "단일풀"은 1풀이다(8종목이 이 표기다)
        if (1 if np_txt == "단일" else int(np_txt)) != m["npools"]:
            bad.append(f"{mo.group('tok')} md 풀수 {np_txt} != 실측 {m['npools']}")
        # ⚠️공백 메움(9/5 11:00Z): 값만 대조하면 **변동 주장**의 오류를 못 잡는다 —
        #   lickingcat이 3→2풀로 줄었는데 "2풀[변동없음]"이라 적혀 값 검사는 통과했다.
        #   직전 풀수(prev_npools)가 있어야 검사할 수 있어, 승격된 다음 회차부터 작동한다.
        pn = m.get("prev_npools")
        if pn is not None and pn != m["npools"]:
            seg = mdtxt[mo.start():mo.end() + 40]
            if re.search(r"변동\s*없음", seg):
                bad.append(f"{mo.group('tok')} md '변동없음' 주장 != 실제 "
                           f"{pn}풀→{m['npools']}풀 변동")
        if mo.group("age") and m["age_days"] is not None \
                and abs(float(mo.group("age")) - m["age_days"]) > 0.15:
            bad.append(f"{mo.group('tok')} md 풀나이 {mo.group('age')}일"
                       f" != 실측 {m['age_days']}일")

    # 최상급 표현 검증
    # ⚠️오탐 수정(9/3) 3건: ①최상급은 vol24만이 아니라 유동성에도 붙는다(지표 판별 필요)
    #   ②"최하위권/최상위권"은 '권'(범위)이라 최상급 주장이 아니다 — 검사 대상 아님
    #   ③주어가 표 행의 첫 칸이거나 문장 앞쪽 멀리 있다 — 전역 창이 아니라
    #     "행 단위"로 주어를 정해야 한다(전역 90자 창은 표 행에서 주어를 놓쳤다).
    ok = [r for r in raw.values() if r["ok"]]
    raw_by_token = {r["token"]: r for r in ok}
    ext = {
        ("vol24", "최대"): max(ok, key=lambda r: r["vol24"]),
        ("vol24", "최저"): min(ok, key=lambda r: r["vol24"]),
        ("liq", "최대"): max(ok, key=lambda r: r["liq"]),
        ("liq", "최저"): min(ok, key=lambda r: r["liq"]),
    }
    SUP = re.compile(r"42종중\s*(?:이번회차)?\s*(최대|최고|최저|최소|최하)(?!위권|위)")

    def _is_past(text: str, start: int) -> bool:
        """'직전회차 42종중 최대변동이었던' 같은 **과거 회차 서술**은 이번 회차 주장이
        아니다(9/4 13:00Z TOAD 2건 오탐). futures_check의 '직전 …' 절 처리와 같은 부류다.
        다만 '직전 …였으나 **이번** 회차 최대'처럼 중간에 이번 회차 표지가 오면 끊는다."""
        pre = text[max(0, start - 30):start]
        i = max(pre.rfind("직전"), pre.rfind("전회"), pre.rfind("과거"))
        return i >= 0 and "이번" not in pre[i:]

    def _metric_at(text: str, start: int, subj: str | None) -> str:
        """최상급의 기준 지표를 **바로 앞에 나온 지표어**로 정한다(9/4 13:00Z PEE 오탐:
        40자 창 저편의 '유동성'을 끌어와 vol24 주장을 유동성으로 판정했다).
        지표어가 없으면 직전 $금액을 실측 liq·vol24와 대조해 가까운 쪽으로 판별한다."""
        near = text[max(0, start - 24):start]
        # 괄호·쉼표·가운뎃점·"vs"를 넘어간 지표어는 **남의 절** 것이다
        #   ("…유동성도 최대) vs PEE $83(42종중 최소" → PEE는 vol24 기준).
        near = re.split(r"[(),·]|vs", near)[-1]
        i_liq = near.rfind("유동성")
        i_vol = max(near.rfind("vol24"), near.rfind("거래량"))
        if max(i_liq, i_vol) >= 0:
            return "liq" if i_liq > i_vol else "vol24"
        r = raw_by_token.get(subj)
        if r:
            mv = re.findall(r"\$([\d,.]+)", text[max(0, start - 40):start])
            if mv:
                try:
                    v = float(mv[-1].replace(",", ""))
                except ValueError:
                    v = None
                if v is not None and r["liq"] and r["vol24"]:
                    dl = abs(v - r["liq"]) / max(r["liq"], 1)
                    dv = abs(v - r["vol24"]) / max(r["vol24"], 1)
                    return "liq" if dl < dv else "vol24"
        return "vol24"

    def scan(text: str, subject: str | None, where: str) -> None:
        for mo in SUP.finditer(text):
            if _is_past(text, mo.start()):
                continue
            kind = "최대" if mo.group(1) in ("최대", "최고") else "최저"
            # ⚠️"42종중 최대 **변동**"은 수준이 아니라 **델타**가 최대라는 뜻이다
            #   (9/4 TOAD 유동성 +26.3%가 '유동성 최대'로 오탐됐다). 델타 최대와 대조한다.
            after = text[mo.end():mo.end() + 8]
            # ⚠️오탐 수정(9/4 13:00Z): 델타 표지가 **뒤에만** 온다고 봤으나
            #   "유동성 변동 상위 5종: 1B +10.1%(42종중최대)"처럼 앞에 오기도 한다.
            #   직전에 부호 붙은 %가 오거나 앞 창에 '변동'이 있으면 델타 기준이다.
            # ⚠️추가(9/4 15:00Z): "42종중 이번회차 최대폭(-25.3%)으로 유출" 처럼
            #   표지가 8자 창 **밖**에 있고 부호 %만 뒤따르는 형태도 델타다.
            pre_d = text[max(0, mo.start() - 14):mo.start()]
            post = text[mo.end():mo.end() + 20]
            # ⚠️오탐 수정(9/5 03:00Z): 앞쪽 델타 표지를 "변동" 하나만 봐서
            #   **"유동성 유입이 이번 회차 42종중 최대"**(=증가 최대, 정확한 서술)를
            #   유동성 **수준** 최대 주장으로 읽어 오탐 3건을 냈다. 앞 창의 델타
            #   표지도 '유입/증가/유출/감소' 전부를 본다.
            pre_w = text[max(0, mo.start() - 24):mo.start()]
            # ⚠️오탐 수정(9/5 13:00Z): "유동성은 42종중 **최대폭으로 빠졌다**"처럼
            #   델타를 **서술어**로 표현하면(빠지다/줄다/늘다/불다) 명사형 표지만 보던
            #   판정이 이를 **수준** 최대 주장으로 읽어 오탐이 났다(PROLOGUE, 실제로는
            #   감소폭 최대 -9.88%로 정확한 서술).
            is_delta = (bool(re.match(r"\s*폭?(?:으로|만큼)?\s*(?:변동|증가|증분|유입|유출|감소|급증|급감|빠|줄|늘|불)", after))
                        or bool(re.match(r"\s*(?:변동|증가|증분|유입|유출|감소|급증|급감)", after))
                        or bool(re.search(r"[+\-−]\s?[\d.,]+%", post))
                        or bool(re.search(r"[+\-−]\s?[\d.,]+%\s*\(?$", pre_d))
                        or bool(re.search(r"(변동|증가|증분|유입|유출|감소|급증|급감)", pre_w)))
            if is_delta:
                # ⚠️추가(9/4 15:00Z): 델타 최상급도 **증가/감소/변동**이 서로 다른
                #   주장이다. CATE는 최대 '증가'(+7.3%)이고 최대 '변동'은 TOAD(-25.3%)라,
                #   전부 절대값 최대와 대조하면 정확한 서술을 오탐한다.
                # ⚠️방향어는 **최상급 바로 뒤**의 것을 먼저 쓴다. 20자 창에서
                #   아무거나 잡으면 "…최대변동,직전대규모**유입**되돌림"의 유입을
                #   끌어와 TOAD의 정확한 '변동 최대' 서술을 오탐한다(9/4 15:00Z).
                _DIR = r"(변동|증가|증분|유입|유출|감소|급증|급감|빠졌|빠지|줄었|줄어|늘었|늘어|불었)"
                # 앞쪽에서 찾을 땐 **최상급에 가장 가까운**(마지막) 방향어를 쓴다 —
                #   "유동성 **유입**이 이번 회차 42종중 최대"에서 조사·어절이 끼면
                #   끝자리 제약으로 못 찾아 '변동'으로 잘못 떨어졌다(9/5 03:00Z).
                pre_hits = list(re.finditer(_DIR, pre_w))
                mw = re.match(r"\s*" + _DIR, after) or re.search(_DIR, post) \
                    or (pre_hits[-1] if pre_hits else None)
                w = mw.group(1) if mw else "변동"
                if w in ("증가", "증분", "유입", "급증", "늘었", "늘어", "불었"):
                    d, kindw = max(ok, key=lambda r: (r.get("dliq_pct") or 0)), "증가"
                elif w in ("유출", "감소", "급감", "빠졌", "빠지", "줄었", "줄어"):
                    d, kindw = min(ok, key=lambda r: (r.get("dliq_pct") or 0)), "감소"
                else:
                    d, kindw = max(ok, key=lambda r: abs(r.get("dliq_pct") or 0)), "변동"
                subj2 = subject
                # ⚠️수준 분기엔 있던 '주어가 목록 라벨이면 되돌린다' 가드가
                #   델타 분기엔 없어 라벨("유동성 변동 상위 5종")을 주어로 잡았다.
                if subj2 is not None and subj2 not in {r["token"] for r in ok}:
                    subj2 = None
                if subj2 is None:   # 표현 직전에 나온 토큰명을 주어로(수준 최상급과 동일)
                    pos = [(text.rfind(r["token"], 0, mo.start()), r["token"]) for r in ok]
                    pos = [x for x in pos if x[0] >= 0]
                    subj2 = max(pos)[1] if pos else None
                if subj2 and subj2 != d["token"]:
                    bad.append(f"최상급 의심 [{where}] '{mo.group(0)} {kindw}' 주어={subj2}"
                               f" — 실제 유동성 {kindw} 최대는 {d['token']}"
                               f"({d['dliq_pct']:+.1f}%)")
                continue
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
            metric = _metric_at(text, mo.start(), subj)
            tgt = ext[(metric, kind)]
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
             re.finditer(r"매도우위[^\n]{0,40}?(?:경계\s*신호|경계신호)[^\n]{0,400}", _text)]
    # ⚠️200자에서 잘려 "…미충족이다" 같은 **부정 표현이 구간 밖에 남는** 일이 있었다
    #   (9/4 BULLSHIT·DPG 오탐). 줄바꿈에서 멈추므로 넓혀도 다른 항목을 삼키지 않는다.
    seg = max(cands, key=lambda c: sum(r["token"] in c for r in ok), default=None)
    if seg and flagged and sum(r["token"] in seg for r in ok) >= 2:
        # ⚠️요약 줄은 **빠진 종목을 함께 짚는** 경우가 많다("FLUSH는 이번 회차 명시
        #   플래그가 사라졌다"). 이름이 구간에 있다는 이유만으로 주장 목록에 넣으면
        #   정확한 서술이 오탐된다(9/4 FLUSH). 토큰명 뒤 짧은 범위에 제외 표현이
        #   붙으면 '플래그 아님' 주장으로 본다 — 반대로 진짜 플래그 종목을 이렇게
        #   적으면 named에서 빠져 `누락`으로 잡히므로 HOOKR 유형은 그대로 걸린다.
        #   ⚠️판정 단위를 **문장**으로 잡아도 부족하다 — 한 문장이 정상 나열과 제외
        #     나열을 함께 담으면("LIZARD·PROLOGUE 2종이다(…4종에서 HOOKR·TOAD가
        #     빠졌다)") 네 종목이 통째로 제외로 분류돼 오탐이 난다(9/4 09:00Z).
        #     부정어의 **주어는 바로 앞의 토큰 나열**이므로 거기까지 좁힌다.
        # ⚠️seg 전체에서 토큰을 모으고 부정분만 빼면, **긍정 나열과 부정 나열에 같이
        #   등장한 종목**이 조용히 제외돼 오류를 놓친다(9/4 주입에서 확인 — 미플래그
        #   종목을 목록에 넣어도 뒤쪽 "미충족" 절 때문에 안 걸렸다).
        #   → 절(괄호·마침표 경계) 단위로 쪼개 **긍정 절에 나온 토큰만** 주장으로 본다.
        _NEG = re.compile(r"(사라졌|해제|제외|빠졌|없어졌|아니다|아니라|없다"
                          r"|미충족|불충족|않는다|않았다)")
        #   ⚠️괄호를 절 **구분자**로 쓰면 "…조건(설명) 미충족이다"에서 부정어가 다음
        #     조각으로 넘어가 긍정으로 오분류된다. 괄호는 **지우고** 마침표로만 나눈다.
        _clauses = [c for c in re.split(r"(?<!\d)\.(?!\d)",
                                        re.sub(r"\([^)]*\)", " ", seg)) if c.strip()]
        _clauses += re.findall(r"\(([^)]*)\)", seg)      # 괄호 안도 하나의 절
        named, denied = set(), set()
        for c in _clauses:
            hit = {r["token"] for r in ok if r["token"] in c}
            (denied if _NEG.search(c) else named).update(hit)

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
