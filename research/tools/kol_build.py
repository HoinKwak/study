#!/usr/bin/env python3
"""온체인 워치 산출물 조립기 — 에이전트 patch + 부모 실측을 합쳐 3파일을 만든다.

⚠️왜 만들었나(2026-09-06 07:00Z): kol-watch 에이전트가 **64k 출력 토큰 상한**에 걸려
  라운드가 통째로 실패했다. watch.md 59KB + watch.json 78KB를 매 회차 전문 재작성하는
  구조라 필연이었다(선물 브리핑이 78KB로 같은 상한에 걸려 2단계로 쪼갠 것과 동일한 부류).
  → 기계적으로 재생성 가능한 것(체인·CA·풀수·풀나이·지표 칼럼·notable 이월)은 부모가
  만들고, 에이전트는 **서사만** 담은 patch 하나만 쓴다.

사용: kol_build.py <ts> <kol_raw.json> <kol_patch.json>

patch 스키마:
  {"ts": "...",
   "header_note": "머리말 인용블록(> 로 시작하는 줄들, 제목/면책 아래에 그대로 들어간다)",
   "kol_md": "'## KOL 코로보' 본문(생략하면 직전 회차 이월)",
   "memo_md": "'## 메모' 본문",
   "tokens": [{"token","stage","kols","short","thesis","risk"}]}

- short : 표·CSV의 '서사(요지)' 한 줄
- thesis: md 상세줄·json 본문에 들어가는 긴 서술
- risk  : 표·json의 리스크 칼럼
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
KOL = R / "kol"


def chain_disp(hint: str) -> str:
    """'Robinhood Chain(Uniswap V3, WETH페어)' → 'Robinhood Chain/Uniswap V3'."""
    m = re.match(r"([^(]+)\(([^,)]+)", hint or "")
    return f"{m.group(1).strip()}/{m.group(2).strip()}" if m else (hint or "").strip()


def pools_disp(m: dict) -> str:
    if not m.get("ok"):
        return "풀수 미확인(계측 실패)"
    n, p = m.get("npools"), m.get("prev_npools")
    if p is None or n is None:
        return f"{n}풀" if n is not None else "풀수 미확인"
    if n == p:
        return f"{n}풀[변동없음]"
    return f"{n}풀[직전{p}풀,{n - p:+d},변동]"


def age_disp(m: dict) -> str:
    a = m.get("age_days")
    return f"풀나이 {a}일" if a is not None else "풀나이 미확인"


def metrics_cell(m: dict, rank) -> str:
    """표의 '온체인(거래량/유동성/홀더)' 칼럼 — 전부 실측이라 부모가 만든다."""
    if not m.get("ok"):
        return "⚠️계측 실패(재확인 실패) — 직전 값 이월 안 함"
    liq = f"유동성${m['liq']:,.0f}"
    if m.get("dliq_pct") is not None:
        liq += f"({m['dliq_pct']:+.1f}%)"
    vol = f"vol24 ${m['vol24']:,.0f}({rank}위)"
    tov = f"회전율{m['turnover']}배" if m.get("turnover") is not None else "회전율 미확인"
    return f"{liq}·{vol}·{tov}"


def q(s: str) -> str:
    """CSV 셀 — 전 행 8열·쉼표 포함 값은 예외 없이 큰따옴표(과거 9열/7열 사고 방지)."""
    return '"' + (s or "").replace('"', '""') + '"'


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    ts, raw_p, patch_p = sys.argv[1], sys.argv[2], sys.argv[3]
    if len(ts) == 17 and ts.endswith("Z"):        # 2026-09-06T07:00Z → 초까지
        ts = ts[:-1] + ":00Z"

    # ⚠️(2026-09-06) 실패 종목을 빼버리면 42종 연속성이 끊기고 kol_check가 종목 수
    #   불일치로 막힌다. 계측 실패도 **한 줄로 이어가되 수치를 만들지 않는다**
    #   (직전 값 이월은 금지 — "재확인 실패"로 정직 표기).
    raw = {t["token"]: t for t in json.load(io.open(raw_p, encoding="utf-8"))}
    patch = json.load(io.open(patch_p, encoding="utf-8"))
    prev = json.load(io.open(KOL / "watch.json", encoding="utf-8"))

    # vol24 순위는 실측에서 매긴다(에이전트가 세지 않는다)
    order = sorted(raw.values(), key=lambda x: -(x.get("vol24") or 0))
    rank = {t["token"]: i + 1 for i, t in enumerate(t2 for t2 in order if t2.get("ok"))}

    pt = {t["token"]: t for t in patch["tokens"]}
    missing = [k for k in raw if k not in pt]
    extra = [k for k in pt if k not in raw]
    if missing or extra:
        print(f"❌ patch 종목 불일치 — 실측에만 {missing} · patch에만 {extra}")
        return 1

    tokens, csv_rows, det = [], [], []
    for m in order:
        k = m["token"]
        p = pt[k]
        tokens.append({
            "token": k,
            "chain": m.get("chain_hint", ""),
            "ca": m.get("ca", ""),
            "stage": p.get("stage", ""),
            "kols": p.get("kols", ""),
            "thesis": p.get("thesis", ""),
            "risk": p.get("risk", ""),
        })
        csv_rows.append(",".join(q(x) for x in (
            k, m.get("chain_hint", ""), p.get("stage", ""), p.get("kols") or "-",
            p.get("short", ""), "-", ts, "다이제스트")))
        det.append(f"- **{k}** ({chain_disp(m.get('chain_hint',''))}, CA `{m.get('ca','')}`, "
                   f"{pools_disp(m)}, {age_disp(m)}): {p.get('thesis','')} · {ts} · 다이제스트")

    # ---------- watch.json ----------
    # ⚠️notable(80건·24KB)은 여러 회차째 이월만 된다 — 에이전트에 다시 쓰게 하면
    #   출력의 상당 부분을 여기에 쓰고도 바뀌는 게 없다. 부모가 바이트 그대로 옮긴다.
    out = {"ts": ts, "tokens": tokens, "notable": prev["notable"]}
    io.open(KOL / "watch.json", "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n")

    # ---------- watch.csv ----------
    io.open(KOL / "watch.csv", "w", encoding="utf-8").write(
        "토큰,체인,단계,KOL코로보,서사,신규여부,시점,출처\n" + "\n".join(csv_rows) + "\n")

    # ---------- watch.md ----------
    kst = ""
    mo = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})", ts)
    if mo:
        y, mth, d, h, mi = (int(x) for x in mo.groups())
        import datetime
        k = datetime.datetime(y, mth, d, h, mi) + datetime.timedelta(hours=9)
        kst = k.strftime("%Y-%m-%d %H:%M")
    head = (f"# 온체인 트렌딩 조기경보 — {ts[:10]} {ts[11:16]} UTC / {kst} (KST)\n\n"
            "> ⚠️ 아이디어 소싱·조기경보용. 투자조언 아님. 온체인 트렌딩은 봇·워시트레이딩·러그 편향이\n"
            "> 큼. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)\n"
            + patch.get("header_note", "").rstrip() + "\n")

    tbl = ["## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)", "",
           "| 토큰 | 체인/DEX | 단계 | KOL 코로보(있으면) | 서사(요지) | "
           "온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |",
           "|---|---|---|---|---|---|---|---|---|"]
    STAGE = {"조기": 0, "확산": 1, "뒷북": 2}
    for m in sorted(order, key=lambda x: (STAGE.get(pt[x["token"]].get("stage", ""), 3),
                                          -(x.get("vol24") or 0))):
        k = m["token"]
        p = pt[k]
        tbl.append(f"| {k} | {chain_disp(m.get('chain_hint',''))} | {p.get('stage','')} | "
                   f"{p.get('kols') or '-'} | {p.get('short','')} | {metrics_cell(m, rank.get(k))} | "
                   f"- | {p.get('risk','')} | 다이제스트 |")

    kol_md = patch.get("kol_md")
    if not kol_md:                       # 생략 시 직전 회차 절을 그대로 이월한다
        old = io.open(KOL / "watch.md", encoding="utf-8").read()
        mo2 = re.search(r"(?ms)^## KOL 코로보.*?(?=^## )", old)
        kol_md = mo2.group(0).split("\n", 1)[1].rstrip() if mo2 else ""

    md = "\n".join([head, "\n".join(tbl), "",
                    "## 온체인 신호 상세", "", "\n".join(det), "",
                    "## KOL 코로보 (확보된 것만)", kol_md.rstrip(), "",
                    "## 메모", patch.get("memo_md", "").rstrip(), ""])
    io.open(KOL / "watch.md", "w", encoding="utf-8").write(md)

    print(f"조립 완료 · ts {ts} · tokens {len(tokens)} · notable {len(out['notable'])}(이월) "
          f"· csv {len(csv_rows)}행 · md {len(md):,}자")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
