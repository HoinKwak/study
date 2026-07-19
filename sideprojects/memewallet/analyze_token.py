"""스테이지②③ — 한 토큰(mint)의 지갑별 realized PnL + 내부자/봇 필터 (Dune).

사장님 스크리닝 기준:
- 비내부자: (a) 초기 할당·에어드랍 덤퍼 제외 = DEX 매수액이 매도액의 일정비율 이상 요구(MIN_BUY_FRAC),
  (b) 출시 초기 스나이퍼 제외 = 첫 거래가 출시+SNIPER_MIN분 이후.
- 실거래: 매수·매도 둘 다 존재.
- 수익: sell_usd - buy_usd ≥ MIN_PNL(=$10만).
봇/MM/DCA 프로그램(초고빈도)은 MAX_TRADES로 선택 배제(팔로우 무의미) — 기본 켜짐, 조정 가능.

주의(정직): pnl = 매도USD − 매수USD = 순 USD 흐름 근사. 현재 보유분 미반영이라 realized 하한.
"""
from __future__ import annotations

import sys

from dune_client import run_sql

MIN_PNL = 100_000
MIN_BUY_FRAC = 0.15    # 매수액 ≥ 매도액×이 비율(알로케이션 덤퍼 배제)
SNIPER_MIN = 60        # 출시+이 분(分) 이내 첫거래=스나이퍼/내부자 배제
MAX_TRADES = 5000      # 총 매매 이 이상=봇/MM/DCA로 보고 배제(None이면 비활성)


def analyze(mint: str, limit: int = 100, max_trades: int | None = MAX_TRADES) -> list[dict]:
    trade_cap = f"AND (w.buys + w.sells) <= {max_trades}" if max_trades else ""
    sql = f"""
    WITH t AS (
      SELECT trader_id AS wallet, block_time, amount_usd,
        CASE WHEN token_bought_mint_address = '{mint}' THEN 'buy'
             WHEN token_sold_mint_address   = '{mint}' THEN 'sell' END AS side
      FROM dex_solana.trades
      WHERE token_bought_mint_address = '{mint}' OR token_sold_mint_address = '{mint}'
    ),
    launch AS (SELECT min(block_time) AS t0 FROM t),
    w AS (
      SELECT wallet,
        sum(CASE WHEN side='buy'  THEN amount_usd ELSE 0 END) AS buy_usd,
        sum(CASE WHEN side='sell' THEN amount_usd ELSE 0 END) AS sell_usd,
        sum(CASE WHEN side='buy'  THEN 1 ELSE 0 END) AS buys,
        sum(CASE WHEN side='sell' THEN 1 ELSE 0 END) AS sells,
        min(block_time) AS first_trade
      FROM t GROUP BY wallet
    )
    SELECT w.wallet, round(w.buy_usd) AS buy_usd, round(w.sell_usd) AS sell_usd,
      round(w.sell_usd - w.buy_usd) AS pnl_usd, w.buys, w.sells,
      date_diff('minute', (SELECT t0 FROM launch), w.first_trade) AS mins_after_launch
    FROM w
    WHERE w.sell_usd - w.buy_usd >= {MIN_PNL}
      AND w.buys > 0 AND w.sells > 0
      AND w.buy_usd >= {MIN_BUY_FRAC} * w.sell_usd
      AND date_diff('minute', (SELECT t0 FROM launch), w.first_trade) > {SNIPER_MIN}
      {trade_cap}
    ORDER BY pnl_usd DESC
    LIMIT {limit}
    """
    return run_sql(f"memewallet_token_{mint[:8]}", sql, timeout=290)


if __name__ == "__main__":
    mint = sys.argv[1]
    rows = analyze(mint)
    print(f"비내부자·실거래·수익≥${MIN_PNL:,}·봇제외 지갑: {len(rows)}명\n")
    for r in rows[:25]:
        print(f"  {r['wallet'][:6]}… PnL ${r['pnl_usd']:>11,.0f} "
              f"(매수 ${r['buy_usd']:>10,.0f}/매도 ${r['sell_usd']:>10,.0f}) "
              f"매매 {r['buys']}/{r['sells']} 출시+{r['mins_after_launch']}분")
