#!/usr/bin/env python3
"""온체인 트렌딩 조기경보 — 다이제스트 생성기.

kol_pre.py의 실측(kol_raw.json)과 기준선(kol_tokens.json)을 대조해
작성자(서브에이전트)가 그대로 인용할 수 있는 다이제스트를 만든다.

⚠️작성자에게 넘기는 수치는 오직 이 다이제스트뿐이다. 부모가 별도로 라이브 재조회한
  퍼센트를 프롬프트에 섞어 넣으면 다이제스트와 어긋나 오류로 잡힌다(전례 3회).
⚠️먼지 풀(유동성 3~4자리)의 h1/h24는 허황된 값을 낸다 — 인용 금지, 이상 징후로만 기록.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
DUST_LIQ = 1000.0          # 이 미만은 먼지 풀
EXTREME = 500.0            # |%| 이 넘으면 아티팩트 의심


def sgn(v):
    return "미확인" if v is None else f"{v:+.2f}%"


def delta(cur, prev):
    """직전 대비 서술. ⚠️부호가 뒤집힌 경우를 '확대/축소'로 뭉개지 않는다."""
    if cur is None:
        return ""
    if prev is None:
        return "(직전 결측)"
    if (cur > 0) != (prev > 0) and abs(cur) > 0.3 and abs(prev) > 0.3:
        return f"(직전 {prev:+.2f}%에서 부호 반전)"
    if abs(cur - prev) < 0.5:
        return f"(직전 {prev:+.2f}%와 유사)"
    return f"(직전 {prev:+.2f}%에서 {'확대' if abs(cur) > abs(prev) else '완화'})"


def main() -> int:
    ts = sys.argv[1]
    raw = json.loads(Path(sys.argv[2]).read_text())
    cfg = {t["token"]: t for t in json.loads((TOOLS / "kol_tokens.json").read_text())}

    ok = [r for r in raw if r["ok"]]
    by_vol = sorted(ok, key=lambda r: -r["vol24"])
    rank = {r["token"]: i + 1 for i, r in enumerate(by_vol)}

    L = []
    L.append(f"# 온체인 다이제스트 — {ts}")
    L.append("")
    L.append(f"- 계측 {len(ok)}/{len(raw)}종목. 아래 수치만 인용한다(외부 재조회 금지).")
    L.append(f"- vol24 최대 {by_vol[0]['token']} ${by_vol[0]['vol24']:,.0f} · "
             f"최소 {by_vol[-1]['token']} ${by_vol[-1]['vol24']:,.0f}")
    L.append(f"- 유동성 최대 {max(ok, key=lambda r: r['liq'])['token']} · "
             f"최소 {min(ok, key=lambda r: r['liq'])['token']}")
    L.append("")

    for r in raw:
        c = cfg.get(r["token"], {})
        rd = c.get("prev_round")
        L.append(f"## {r['token']}  [{r['chain']}/{r['dex']}]  "
                 f"{('%d회차' % (rd + 1)) if rd else '회차수 미확인(carryover)'}")
        if not r["ok"]:
            L.append("- ⚠️계측 실패(DexScreener 무응답). 직전 값 이월 금지, '재확인 실패'로 표기.")
            L.append("")
            continue
        # ⚠️직전 풀수를 병기한다(9/5 11:00Z) — 값만 갱신하고 "변동없음"이라 쓰는
        #   오류가 반복됐다(BARRON 7풀 이월, lickingcat 3→2풀 변동없음 오기).
        pn = c.get("prev_npools")
        pnt = (f"{r['npools']}풀" if pn is None or pn == r["npools"]
               else f"{r['npools']}풀(직전 {pn}풀 — ⚠️변동)")
        L.append(f"- CA `{r['ca']}` · {pnt} · "
                 f"풀나이 {('%.1f일' % r['age_days']) if r['age_days'] is not None else '미확인'}")
        L.append(f"- 유동성 ${r['prev_liq']:,.0f} → ${r['liq']:,.0f} "
                 f"({r['dliq_pct']:+.1f}%) ← **Δ는 직전 회차 실측 대비다**")
        L.append(f"- vol24 ${r['vol24']:,.0f} (42종중 {rank[r['token']]}위)"
                 + (f" · 직전 ${c['prev_vol24']:,.0f}" if c.get("prev_vol24") else "")
                 + f" · 회전율 {r['turnover']}배")
        L.append(f"- h1 {sgn(r['h1'])} {delta(r['h1'], c.get('prev_h1'))}")
        L.append(f"- h6 {sgn(r['h6'])} {delta(r['h6'], c.get('prev_h6'))}")
        L.append(f"- h24 {sgn(r['h24'])} {delta(r['h24'], c.get('prev_h24'))}")
        L.append(f"- 체결 h24 매수{r['buys24']}/매도{r['sells24']} · "
                 f"h1 매수{r['buys1']}/매도{r['sells1']}")
        flags = []
        if r["liq"] < DUST_LIQ:
            flags.append("먼지 풀 — h1/h24 인용 금지")
        if r["h1"] is None:
            flags.append("h1 결측(체결 부재 가능 — 위 h1 체결건수 확인)")
        for k in ("h1", "h6", "h24"):
            if r[k] is not None and abs(r[k]) > EXTREME:
                flags.append(f"{k} {r[k]:+.0f}% 극단값 — 아티팩트 의심")
        if r["turnover"] is not None and r["turnover"] < 0.1:
            flags.append("회전율 극저 — 거래 사실상 부재")
        if (r["h24"] or 0) > 20 and (r["sells24"] or 0) > (r["buys24"] or 0):
            flags.append("가격 급등인데 h24 체결 매도우위 — 경계 신호")
        if flags:
            L.append("- ⚠️ " + " / ".join(flags))
        if c.get("prev_stage"):
            L.append(f"- 직전 단계 `{c['prev_stage']}` · 직전 risk: {c.get('prev_risk', '')}")
        L.append("")

    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
