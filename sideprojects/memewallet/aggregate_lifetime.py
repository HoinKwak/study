"""스테이지④ — 대상 밈 토큰 전체에서 지갑별 lifetime PnL 집계·최종 선별 (Dune).

토큰별로 내부자/봇/스나이퍼 필터를 적용한 (지갑,토큰) 수익을 지갑 단위로 합산해 lifetime PnL 산출.
사장님 기준: lifetime PnL≥$10만 + 다수 토큰 수익(생존편향 방지) + 최근 활동(최근 90일).

산출 → research 용 CSV/JSON은 호출측에서 저장. 결과는 최종 팔로우 후보 지갑 리스트.
주의(정직): pnl=순 USD흐름 근사(보유분 미반영, realized 하한). last_active는 대상토큰 거래 기준.
"""
from __future__ import annotations

import json
from pathlib import Path

from dune_client import run_sql

MIN_LIFETIME_PNL = 100_000
MIN_TOKENS = 2         # 다수 토큰에서 수익(생존편향 방지) — 1로 낮추면 단일토큰 대박도 포함
MIN_BUY_FRAC = 0.15
SNIPER_MIN = 60
MAX_TRADES_PER_TOKEN = 5000
RECENT_DAYS = 90       # 최근 활동


def _mints() -> list[str]:
    m = json.loads((Path(__file__).parent / "mints.json").read_text())
    return list(m.values())


def aggregate(limit: int = 300) -> list[dict]:
    mints = _mints()
    in_list = ",".join(f"'{m}'" for m in mints)
    sql = f"""
    WITH long AS (
      SELECT trader_id AS wallet, token_bought_mint_address AS mint, 'buy' AS side,
             block_time, amount_usd
      FROM dex_solana.trades WHERE token_bought_mint_address IN ({in_list})
      UNION ALL
      SELECT trader_id AS wallet, token_sold_mint_address AS mint, 'sell' AS side,
             block_time, amount_usd
      FROM dex_solana.trades WHERE token_sold_mint_address IN ({in_list})
    ),
    launch AS (SELECT mint, min(block_time) AS t0 FROM long GROUP BY mint),
    wt AS (
      SELECT wallet, mint,
        sum(CASE WHEN side='buy'  THEN amount_usd ELSE 0 END) AS buy_usd,
        sum(CASE WHEN side='sell' THEN amount_usd ELSE 0 END) AS sell_usd,
        sum(CASE WHEN side='buy'  THEN 1 ELSE 0 END) AS buys,
        sum(CASE WHEN side='sell' THEN 1 ELSE 0 END) AS sells,
        min(block_time) AS first_trade, max(block_time) AS last_trade
      FROM long GROUP BY wallet, mint
    ),
    qual AS (
      SELECT wt.*, wt.sell_usd - wt.buy_usd AS pnl
      FROM wt JOIN launch ON wt.mint = launch.mint
      WHERE wt.buys > 0 AND wt.sells > 0
        AND wt.buy_usd >= {MIN_BUY_FRAC} * wt.sell_usd
        AND date_diff('minute', launch.t0, wt.first_trade) > {SNIPER_MIN}
        AND (wt.buys + wt.sells) <= {MAX_TRADES_PER_TOKEN}
    ),
    life AS (
      SELECT wallet, sum(pnl) AS lifetime_pnl, count(*) AS tokens_traded,
             max(last_trade) AS last_active, sum(buys+sells) AS total_trades
      FROM qual GROUP BY wallet
    )
    SELECT wallet, round(lifetime_pnl) AS lifetime_pnl, tokens_traded,
      cast(last_active AS varchar) AS last_active, total_trades
    FROM life
    WHERE lifetime_pnl >= {MIN_LIFETIME_PNL}
      AND tokens_traded >= {MIN_TOKENS}
      AND last_active >= (now() - interval '{RECENT_DAYS}' day)
    ORDER BY lifetime_pnl DESC
    LIMIT {limit}
    """
    return run_sql("memewallet_lifetime", sql, timeout=1500)


if __name__ == "__main__":
    rows = aggregate()
    out = Path(__file__).parent / "smart_wallets.json"
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"최종 스마트머니 지갑: {len(rows)}명 → {out.name}\n")
    print(f"기준: lifetime PnL≥${MIN_LIFETIME_PNL:,} · 토큰≥{MIN_TOKENS}종 · 최근{RECENT_DAYS}일 활동 · 봇/내부자 제외\n")
    for r in rows[:30]:
        print(f"  {r['wallet'][:6]}… lifetime ${r['lifetime_pnl']:>12,.0f} | 토큰 {r['tokens_traded']}종 | 매매 {r['total_trades']} | 최근 {r['last_active'][:10]}")
