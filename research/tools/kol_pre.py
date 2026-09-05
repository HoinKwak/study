#!/usr/bin/env python3
"""온체인 트렌딩 조기경보 — 계측 수집기.

⚠️2026-09-03 컨테이너 재시작으로 스크래치패드가 통째로 비워지면서 온체인 파이프라인
  (kol_pre/kol_digest/kol_pools.json)이 유실됐다. 저장소에 없었기 때문이다.
  그래서 이번부터 research/tools/ 에 둔다.

  종목·CA·직전 유동성 기준선은 research/tools/kol_tokens.json 에 있다.
  기준선(prev_liquidity)은 매 회차 이 스크립트가 실측값으로 갱신하므로,
  더 이상 발행된 산문(thesis)에서 숫자를 되읽지 않는다 —
  과거 "유동성 $A→$B"에서 A(2회차 전 값)를 잡아 40종의 Δ가 누적되던 사고의 재발 방지.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CFG = Path(__file__).resolve().parent / "kol_tokens.json"
DS = "https://api.dexscreener.com/latest/dex/tokens/"


def fetch(ca: str, tries: int = 3) -> dict | None:
    """DexScreener 토큰 엔드포인트. 페어 엔드포인트는 실패율이 높아 쓰지 않는다."""
    for i in range(tries):
        try:
            r = subprocess.run(
                ["curl", "-s", "--max-time", "25", DS + ca],
                capture_output=True, text=True, timeout=40,
            )
            d = json.loads(r.stdout)
            if isinstance(d, dict):
                return d
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2 * (i + 1))
    return None


def pick(pairs: list[dict], prev_liq: float | None, pinned: str | None) -> dict | None:
    """대표 풀 선정.

    ⚠️최대 유동성 풀만 기계적으로 고르면 안 된다(회전율 1배짜리 죽은 풀이 뽑힌 전례).
      ①핀이 있으면 핀 ②직전 유동성에 가장 가까운 풀(연속성) ③거래량 최대 풀 순.
    """
    if not pairs:
        return None
    if pinned:
        for p in pairs:
            if (p.get("pairAddress") or "").lower() == pinned.lower():
                return p
    if prev_liq:
        def dist(p):
            liq = float((p.get("liquidity") or {}).get("usd") or 0)
            if liq <= 0:
                return 9e9
            return abs(liq - prev_liq) / prev_liq
        best = min(pairs, key=dist)
        if dist(best) < 0.60:  # 2시간 만에 60% 넘게 변하면 동일 풀로 단정하지 않는다
            return best
    return max(pairs, key=lambda p: float((p.get("volume") or {}).get("h24") or 0))


def promote(raw_path: str) -> int:
    """발행 확정 후 이번 회차 실측을 기준선으로 승격한다.

    ⚠️반드시 검증기(kol_check·kol_verify) 통과 후에만 돌린다 —
      승격하면 직전 값이 사라져 Δ 대조가 불가능해진다.
    """
    raw = {r["ca"].lower(): r for r in json.loads(Path(raw_path).read_text())}
    pub = json.loads((ROOT / "research" / "kol" / "watch.json").read_text())
    pub = {(t.get("ca") or "").lower(): t for t in pub["tokens"]}
    cfg = json.loads(CFG.read_text())
    for t in cfg:
        m = raw.get(t["ca"].lower())
        if not m or not m["ok"]:
            continue
        w = pub.get(t["ca"].lower(), {})
        t.update(prev_liquidity=m["liq"], prev_h1=m["h1"], prev_h6=m["h6"],
                 prev_h24=m["h24"], prev_vol24=m["vol24"],
                 # ⚠️풀수도 기준선에 남긴다(9/5 11:00Z): 검증기가 풀수 **값**만 대조해
                 #   "2풀[변동없음]"처럼 값은 맞고 **변동 주장이 틀린** 서술을 놓쳤다
                 #   (lickingcat 3→2풀). 직전 풀수가 있어야 그 주장을 검사할 수 있다.
                 prev_npools=m.get("npools"),
                 # ⚠️회차수 미확인 종목을 1로 바꿔 "2회차"라는 없는 이력을 만들면 안 된다(9/3 발생)
                 prev_round=(t["prev_round"] + 1) if t.get("prev_round") else None,
                 prev_stage=w.get("stage"), prev_risk=w.get("risk", ""),
                 prev_kols=w.get("kols", ""), prev_thesis=w.get("thesis", ""))
    CFG.write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
    print(f"기준선 승격 {len(cfg)}종목")
    return 0


def main() -> int:
    if sys.argv[1:2] == ["--promote"]:
        if len(sys.argv) < 3:
            print("인자 오류: --promote 는 kol_raw.json 경로가 필요하다.", file=sys.stderr)
            return 2
        return promote(sys.argv[2])
    cfg = json.loads(CFG.read_text())
    out, fails = [], []
    for i, t in enumerate(cfg):
        d = fetch(t["ca"])
        pairs = (d or {}).get("pairs") or []
        p = pick(pairs, t.get("prev_liquidity"), t.get("pinned_pair"))
        if p is None:
            fails.append(t["token"])
            out.append({**t, "ok": False, "npools": len(pairs)})
            continue
        liq = float((p.get("liquidity") or {}).get("usd") or 0)
        vol = float((p.get("volume") or {}).get("h24") or 0)
        txn = (p.get("txns") or {})
        pc = p.get("priceChange") or {}
        created = p.get("pairCreatedAt")
        out.append({
            "token": t["token"], "ca": t["ca"], "chain_hint": t["chain_hint"],
            "ok": True,
            "chain": p.get("chainId"), "dex": p.get("dexId"),
            "pair": p.get("pairAddress"),
            "quote": (p.get("quoteToken") or {}).get("symbol"),
            "npools": len(pairs),
            "prev_npools": t.get("prev_npools"),
            "price": p.get("priceUsd"),
            "liq": round(liq, 2),
            "prev_liq": t.get("prev_liquidity"),
            "dliq_pct": (round((liq - t["prev_liquidity"]) / t["prev_liquidity"] * 100, 2)
                         if t.get("prev_liquidity") else None),
            "vol24": round(vol, 2),
            "turnover": round(vol / liq, 2) if liq > 0 else None,
            "h1": pc.get("h1"), "h6": pc.get("h6"), "h24": pc.get("h24"),
            "buys24": (txn.get("h24") or {}).get("buys"),
            "sells24": (txn.get("h24") or {}).get("sells"),
            "buys1": (txn.get("h1") or {}).get("buys"),
            "sells1": (txn.get("h1") or {}).get("sells"),
            "age_days": (round((time.time() * 1000 - created) / 86400000, 1)
                         if created else None),
        })
        if i % 8 == 7:
            time.sleep(1)
    # ⚠️첫 인자가 곧 출력 경로다. `--out <경로>` 꼴로 부르면 "--out" 이름의 파일이
    #   저장소 루트에 생기고, 부모는 **직전 회차의 낡은 kol_raw.json**을 그대로 읽어
    #   "42/42 종목 전 필드 동결"이라는 가짜 데이터 정체를 보게 된다(9/4 발생).
    #   fetch_all.sh 인자 자리 실수와 같은 부류라 여기서 원천 차단한다.
    if len(sys.argv) > 1 and sys.argv[1].startswith("-"):
        print(f"인자 오류: 첫 인자는 출력 경로다(받은 값 {sys.argv[1]!r}). "
              "사용법: kol_pre.py <출력경로> | kol_pre.py --promote <kol_raw.json>",
              file=sys.stderr)
        return 2
    dst = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "kol_raw.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"수집 {sum(1 for x in out if x['ok'])}/{len(out)}종목 → {dst}")
    if fails:
        print("실패:", ", ".join(fails))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
