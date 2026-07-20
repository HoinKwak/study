"""Jupiter 애그리게이터 견적/스왑 래퍼 (솔라나 DEX 실행).

드라이런은 **견적(quote)만** 사용한다 — 실제 서명·전송 없이 실효 체결가·슬리피지를 계산.
라이브(build_swap)는 solders/solana-py + 봇 키페어가 있는 사장님 PC에서만 동작한다.

수량 단위는 전부 base units(정수). USDC는 6dp, SOL은 9dp(lamports).
PnL 계산은 **USDC 뉴머레르**로 왕복 견적을 써서 슬리피지를 양방향 반영한다
(실지갑은 SOL 보유라 SOL레그 변동이 별도지만, 밈코인 알파 계측엔 USD 기준이 명료 — 근사).
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

_QUOTE = "https://lite-api.jup.ag/swap/v1/quote"
_SWAP = "https://lite-api.jup.ag/swap/v1/swap"

SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=20) as r:  # noqa: S310
        return json.load(r)


def quote(input_mint: str, output_mint: str, amount: int, slippage_bps: int = 150) -> dict | None:
    """스왑 견적. amount는 input_mint의 base units(정수). 실패 시 None."""
    q = urllib.parse.urlencode({
        "inputMint": input_mint, "outputMint": output_mint,
        "amount": int(amount), "slippageBps": slippage_bps,
    })
    try:
        return _get(f"{_QUOTE}?{q}")
    except Exception:  # noqa: BLE001
        return None


def sol_usd() -> float:
    """1 SOL의 USD가(USDC 기준). 실패 시 0."""
    q = quote(SOL, USDC, 1_000_000_000)   # 1 SOL = 1e9 lamports
    return int(q["outAmount"]) / 1e6 if q else 0.0


def sim_buy(mint: str, usd: float, slippage_bps: int = 150) -> dict | None:
    """usd 어치 USDC로 mint 매수 시뮬레이션.

    반환 {tokens_base, entry_usd, price_impact_pct} | None.
    tokens_base = 받게 될 토큰 base units(정수). entry_usd = 투입 USD(=usd).
    """
    usdc_in = int(usd * 1e6)
    q = quote(USDC, mint, usdc_in, slippage_bps)
    if not q or int(q.get("outAmount", 0)) <= 0:
        return None
    return {
        "tokens_base": int(q["outAmount"]),
        "entry_usd": usd,
        "price_impact_pct": float(q.get("priceImpactPct") or 0.0) * 100.0,
    }


def sim_value(mint: str, tokens_base: int, slippage_bps: int = 150) -> float | None:
    """보유 tokens_base를 지금 매도했을 때 받을 USD(왕복 슬리피지 반영). 실패 시 None."""
    if tokens_base <= 0:
        return 0.0
    q = quote(mint, USDC, tokens_base, slippage_bps)
    if not q:
        return None
    return int(q.get("outAmount", 0)) / 1e6


if __name__ == "__main__":   # 간이 점검: python jupiter.py <mint> <usd>
    import sys
    m = sys.argv[1] if len(sys.argv) > 1 else "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm"  # WIF
    usd = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    print("SOL/USD:", round(sol_usd(), 2))
    b = sim_buy(m, usd)
    print("sim_buy:", b)
    if b:
        v = sim_value(m, b["tokens_base"])
        print(f"즉시 왕복가치: ${v:.4f} (투입 ${usd} → 왕복손실 ${usd - (v or 0):.4f}, 슬리피지+영향)")
