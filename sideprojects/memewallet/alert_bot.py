"""스테이지⑤ — 스마트머니 지갑 F/U 알림봇.

smart_wallets.json(277 지갑)의 신규 밈 매수를 Bitquery realtime으로 감지 → 텔레그램 알림.
- 매수 정의: 베이스통화(SOL/USDC/USDT)로 토큰을 산 것(밈 매도·통화변환 제외).
- 필터: 지불액(Sell.AmountInUSD) ≥ MIN_USD(기본 $1,000, 분포분석 근거).
- 중복제거: 처리한 tx signature를 state에 저장. 폴링 간격마다 last_time 이후만.
- 부가정보(enrich): ① 신규매수 vs 추매(현재잔고와 이번 매수량 비교) ② 현재 해당코인 잔고
  (공개 RPC getTokenAccountsByOwner) ③ 해당코인 역대 실현손익 근사(Bitquery 매수/매도 누적).

실행: python sideprojects/memewallet/alert_bot.py          (상시 폴링)
      python sideprojects/memewallet/alert_bot.py --once   (1회 조회·알림, 테스트)
      python sideprojects/memewallet/alert_bot.py --dry     (텔레그램 미발송, 콘솔만)
키: .env 의 BITQUERY_API_KEY + **매매봇과 분리된 전용** MEMEWALLET_TELEGRAM_BOT_TOKEN,
    MEMEWALLET_TELEGRAM_CHAT_ID. 프록시 HTTPS_PROXY 자동.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

_DIR = Path(__file__).parent
_STATE = _DIR / "alert_state.json"
_EAP = "https://streaming.bitquery.io/eap"
_BASE_MINTS = [
    "So11111111111111111111111111111111111111112",   # WSOL
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",   # USDC
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",   # USDT
]
MIN_USD = 1000.0
POLL_SEC = 120


def _env(k: str) -> str | None:
    v = os.environ.get(k)
    if not v and (_DIR.parents[1] / ".env").exists():
        for ln in (_DIR.parents[1] / ".env").read_text().splitlines():
            if ln.startswith(f"{k}="):
                return ln.split("=", 1)[1].strip()
    return v


def _wallets() -> dict[str, float]:
    return {w["wallet"]: w["lifetime_pnl"] for w in json.loads((_DIR / "smart_wallets.json").read_text())}


def _post(url: str, body: dict, headers: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=40) as r:  # noqa: S310
        return json.load(r)


def query_new_buys(wallets: list[str], since_iso: str) -> list[dict]:
    q = (
        'query { Solana { DEXTrades(limit: {count: 50}, orderBy: {descending: Block_Time}, '
        'where: {Trade: {Buy: {Account: {Owner: {in: %s}}, Currency: {MintAddress: {notIn: %s}}}, '
        'Sell: {Currency: {MintAddress: {in: %s}}, AmountInUSD: {ge: "%d"}}}, '
        'Block: {Time: {after: "%s"}}}) '
        '{ Block { Time } Transaction { Signature } '
        'Trade { Sell { AmountInUSD } Buy { Amount Currency { Symbol MintAddress } Account { Owner } } } } } }'
    ) % (json.dumps(wallets), json.dumps(_BASE_MINTS), json.dumps(_BASE_MINTS), int(MIN_USD), since_iso)
    key = _env("BITQUERY_API_KEY")
    d = _post(_EAP, {"query": q}, {"Content-Type": "application/json", "X-API-KEY": key or ""})
    if not d.get("data"):
        raise RuntimeError(f"Bitquery 오류: {str(d.get('errors'))[:200]}")
    return d["data"]["Solana"]["DEXTrades"]


_RPC = "https://api.mainnet-beta.solana.com"


def token_balance(owner: str, mint: str) -> float | None:
    """지갑의 해당 토큰 현재 잔고(UI 수량). 공개 RPC getTokenAccountsByOwner. 실패 시 None."""
    body = {"jsonrpc": "2.0", "id": 1, "method": "getTokenAccountsByOwner",
            "params": [owner, {"mint": mint}, {"encoding": "jsonParsed"}]}
    try:
        d = _post(_RPC, body, {"Content-Type": "application/json"})
        tot = 0.0
        for a in (d.get("result") or {}).get("value") or []:
            amt = a["account"]["data"]["parsed"]["info"]["tokenAmount"]
            tot += float(amt.get("uiAmount") or 0.0)
        return tot
    except Exception:  # noqa: BLE001
        return None


def token_realized(wallet: str, mint: str) -> dict | None:
    """해당 (지갑,토큰)의 매수누적·매도누적 USD → 실현손익 근사. Bitquery(무료=최근 롤링윈도우).

    반환 {"buy_usd","sell_usd","pnl","sells"}. pnl=매도누적−매수누적(순현금흐름). 실패 시 None.
    ※ 무료 플랜은 realtime(롤링) 데이터라 아주 오래된 이력은 빠질 수 있어 '근사'다.
    """
    base = json.dumps(_BASE_MINTS)
    w = json.dumps([wallet]); mt = json.dumps([mint])   # 검증된 감지쿼리와 동일한 in-리스트 패턴
    q = (
        'query { Solana {'
        ' buys: DEXTrades(limit: {count: 300}, where: {Trade: {Buy: {Account: {Owner: {in: %s}}, '
        'Currency: {MintAddress: {in: %s}}}, Sell: {Currency: {MintAddress: {in: %s}}}}}) '
        '{ Trade { Sell { AmountInUSD } } }'
        ' sells: DEXTrades(limit: {count: 300}, where: {Trade: {Sell: {Account: {Owner: {in: %s}}, '
        'Currency: {MintAddress: {in: %s}}}, Buy: {Currency: {MintAddress: {in: %s}}}}}) '
        '{ Trade { Buy { AmountInUSD } } }'
        ' } }'
    ) % (w, mt, base, w, mt, base)
    try:
        key = _env("BITQUERY_API_KEY")
        d = _post(_EAP, {"query": q}, {"Content-Type": "application/json", "X-API-KEY": key or ""})
        sol = (d.get("data") or {}).get("Solana") or {}
        buy_usd = sum(float(r["Trade"]["Sell"].get("AmountInUSD") or 0.0) for r in sol.get("buys") or [])
        sells = sol.get("sells") or []
        sell_usd = sum(float(r["Trade"]["Buy"].get("AmountInUSD") or 0.0) for r in sells)
        return {"buy_usd": buy_usd, "sell_usd": sell_usd, "pnl": sell_usd - buy_usd, "sells": len(sells)}
    except Exception:  # noqa: BLE001
        return None


def enrich(t: dict) -> dict:
    """알림 1건에 신규/추매·현재잔고·해당코인 역대손익 부가정보 계산."""
    tr = t["Trade"]; owner = tr["Buy"]["Account"]["Owner"]; mint = tr["Buy"]["Currency"]["MintAddress"]
    usd = float(tr["Sell"].get("AmountInUSD") or 0.0)
    bought = float(tr["Buy"].get("Amount") or 0.0)            # 이번에 산 토큰 수량(UI)
    bal = token_balance(owner, mint)                          # 현재 총 보유(이번 매수 반영 후)
    # 신규 vs 추매: 잔고가 이번 매수분보다 유의미하게 크면 기존 보유가 있던 것 → 추매
    is_add = None
    if bal is not None and bought > 0:
        is_add = bal > bought * 1.3
    price = (usd / bought) if bought > 0 else None            # 이번 매수 단가(USD/토큰)
    bal_usd = (bal * price) if (bal is not None and price) else None
    return {"owner": owner, "mint": mint, "usd": usd, "bal": bal, "is_add": is_add,
            "bal_usd": bal_usd, "hist": token_realized(owner, mint)}


def _tg_call(url: str, body: dict) -> tuple[bool, str]:
    """텔레그램 sendMessage 호출 → (성공, 사유). 실패 시 텔레그램 JSON description 반환."""
    import urllib.error
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310
            json.load(r)
        return True, ""
    except urllib.error.HTTPError as e:
        try:
            desc = json.loads(e.read().decode()).get("description", "")
        except Exception:  # noqa: BLE001
            desc = str(e)
        return False, desc
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def send_telegram(text: str) -> None:
    # ★매매봇과 분리★ 전용 봇/채널 사용. 미설정 시 콘솔만(매매봇 채널로 폴백하지 않음).
    tok = _env("MEMEWALLET_TELEGRAM_BOT_TOKEN")
    chat = _env("MEMEWALLET_TELEGRAM_CHAT_ID")
    if not tok or not chat:
        print("[밈 알림봇 텔레그램 미설정 — 콘솔만. .env에 MEMEWALLET_TELEGRAM_BOT_TOKEN/"
              "MEMEWALLET_TELEGRAM_CHAT_ID 추가하면 별도 채널로 전송]"); return
    url = f"https://api.telegram.org/bot{tok}/sendMessage"
    ok, why = _tg_call(url, {"chat_id": chat, "text": text, "parse_mode": "HTML",
                             "disable_web_page_preview": True})
    if ok:
        return
    # HTML 파싱 실패면 평문으로 자동 재시도(태그 제거)
    if "parse" in why.lower() or "entit" in why.lower() or "tag" in why.lower():
        import re
        plain = re.sub(r"<[^>]+>", "", text)
        ok2, why2 = _tg_call(url, {"chat_id": chat, "text": plain, "disable_web_page_preview": True})
        if ok2:
            return
        why = f"HTML실패({why}) → 평문도실패({why2})"
    print(f"텔레그램 전송 실패: {why}")


def _fmt(t: dict, pnl_by_wallet: dict[str, float], ex: dict | None = None) -> str:
    tr = t["Trade"]; owner = tr["Buy"]["Account"]["Owner"]
    sym = tr["Buy"]["Currency"]["Symbol"]; mint = tr["Buy"]["Currency"]["MintAddress"]
    usd = float(tr["Sell"]["AmountInUSD"]); life = pnl_by_wallet.get(owner, 0)
    ex = ex or {}
    # 신규매수 vs 추매(기존 보유 위에 더 삼)
    tag = "🆕 신규매수" if ex.get("is_add") is False else ("➕ 추매" if ex.get("is_add") else "매수")
    lines = [f"🟢 <b>스마트머니 {tag}</b>",
             f"지갑 <code>{owner[:6]}…{owner[-4:]}</code> (통산 ${life:,.0f})",
             f"매수 <b>{sym}</b>  ${usd:,.0f}"]
    # 현재 해당코인 잔고
    if ex.get("bal") is not None:
        bal_usd = f" (≈${ex['bal_usd']:,.0f})" if ex.get("bal_usd") else ""
        lines.append(f"보유 {ex['bal']:,.0f} {sym}{bal_usd}")
    # 해당코인 역대 손익(실현 근사)
    h = ex.get("hist")
    if h:
        sign = "＋" if h["pnl"] >= 0 else "－"
        lines.append(f"이 코인 역대손익 {sign}${abs(h['pnl']):,.0f} "
                     f"(매수 ${h['buy_usd']:,.0f}/매도 ${h['sell_usd']:,.0f})")
    lines.append(f"<a href='https://gmgn.ai/sol/token/{mint}'>차트</a> · "
                 f"<a href='https://solscan.io/account/{owner}'>지갑</a>")
    return "\n".join(lines)


def run(once: bool = False, dry: bool = False) -> None:
    wmap = _wallets(); wallets = list(wmap)
    st = json.loads(_STATE.read_text()) if _STATE.exists() else {}
    seen = set(st.get("seen", []))
    since = st.get("last_time") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 600))
    print(f"[알림봇] 감시 {len(wallets)}지갑, ≥${MIN_USD:,.0f}, since {since}, dry={dry}")
    while True:
        try:
            trades = query_new_buys(wallets, since)
            # signature 기준 중복제거(같은 tx 다중 leg) + 이미 처리분 제외
            uniq: dict[str, dict] = {}
            for t in trades:
                sig = t["Transaction"]["Signature"]
                if sig not in seen and sig not in uniq:
                    uniq[sig] = t
            new = sorted(uniq.values(), key=lambda t: t["Block"]["Time"])
            for t in new:
                ex = enrich(t)                       # 신규/추매·현재잔고·역대손익
                msg = _fmt(t, wmap, ex)
                print(msg.replace("\n", " | "))
                if not dry:
                    send_telegram(msg)
                seen.add(t["Transaction"]["Signature"])
                since = max(since, t["Block"]["Time"])
            # state 저장(seen은 최근 2000개만 유지)
            _STATE.write_text(json.dumps({"seen": list(seen)[-2000:], "last_time": since}))
            if new:
                print(f"  → {len(new)}건 신규 알림")
        except Exception as e:  # noqa: BLE001
            print("폴링 오류:", e)
        if once:
            break
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    run(once="--once" in sys.argv, dry="--dry" in sys.argv)
