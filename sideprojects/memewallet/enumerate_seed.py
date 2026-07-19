"""스테이지① — 2024+ 시총 $200M+ 밈코인 시드 열거 (CoinGecko 무료, 키 불필요).

현재 mcap≥$200M 밈코인 + ATH 정보로 '피크 ≥$200M 추정'까지 시드 목록을 만든다.
완전한 '2024+ 피크≥$200M' 목록은 과거 시총(Dune/Flipside/Bitquery, 키 필요)으로 백필 필요 —
이 스크립트는 키 없이 되는 시드까지만.

프록시: HTTPS_PROXY 환경변수를 urllib가 자동 사용.
실행: python sideprojects/memewallet/enumerate_seed.py
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime

CG = "https://api.coingecko.com/api/v3"
PEAK_MIN = 200_000_000  # $200M
SINCE = "2024-01-01"


def _get(url: str) -> list | dict:
    req = urllib.request.Request(url, headers={"User-Agent": "memewallet-seed/0.1"})
    with urllib.request.urlopen(req, timeout=25) as r:  # noqa: S310
        return json.load(r)


def fetch_meme_markets(pages: int = 2) -> list[dict]:
    out: list[dict] = []
    for p in range(1, pages + 1):
        url = (f"{CG}/coins/markets?vs_currency=usd&category=meme-token"
               f"&order=market_cap_desc&per_page=100&page={p}")
        rows = _get(url)
        if not isinstance(rows, list) or not rows:
            break
        out.extend(rows)
    return out


def est_peak_mcap(c: dict) -> float | None:
    """ATH가격 대비 현재 하락률로 피크 시총을 대략 추정(공급 불변 가정 — 부정확).

    현재 mcap = 현재가×공급, 피크 mcap ≈ ATH가×공급 = 현재mcap × (ATH가/현재가).
    ath_change_percentage = (현재가-ATH가)/ATH가 × 100.
    """
    mc = c.get("market_cap")
    chg = c.get("ath_change_percentage")  # 음수(예: -90)
    if not mc or chg is None or chg <= -100:
        return None
    ratio = 100.0 / (100.0 + chg)  # ATH가/현재가
    return mc * ratio


def main() -> None:
    rows = fetch_meme_markets(pages=2)
    print(f"밈 카테고리 {len(rows)}개 조회\n")

    cur = [c for c in rows if (c.get("market_cap") or 0) >= PEAK_MIN]
    peak = []
    for c in rows:
        ep = est_peak_mcap(c)
        athd = (c.get("ath_date") or "")[:10]
        if ep and ep >= PEAK_MIN and athd >= SINCE:
            peak.append((c, ep))

    print(f"[A] 현재 mcap≥$200M: {len(cur)}개")
    for c in cur:
        print(f"    {c.get('symbol','').upper():10} 현재 ${(c.get('market_cap') or 0)/1e6:,.0f}M"
              f"  ATH {(c.get('ath_date') or '')[:10]}")

    print(f"\n[B] ATH가 2024+ & 추정 피크 mcap≥$200M (하락분 포함, 추정치):")
    peak.sort(key=lambda x: -x[1])
    for c, ep in peak:
        print(f"    {c.get('symbol','').upper():10} 추정피크 ${ep/1e6:,.0f}M"
              f"  현재 ${(c.get('market_cap') or 0)/1e6:,.0f}M  ATH {(c.get('ath_date') or '')[:10]}")

    ids = sorted({c.get("id") for c in cur} | {c.get("id") for c, _ in peak})
    print(f"\n시드 토큰 총 {len(ids)}개(중복제거). 다음 단계(홀더·PnL)는 키 발급 후 진행.")


if __name__ == "__main__":
    main()
