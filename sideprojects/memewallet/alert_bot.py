"""스테이지⑤ — 스마트머니 지갑 F/U 알림봇.

smart_wallets.json(277 지갑)의 신규 밈 매수를 Bitquery realtime으로 감지 → 텔레그램 알림.
- 매수 정의: 베이스통화(SOL/USDC/USDT)로 토큰을 산 것(밈 매도·통화변환 제외).
- 필터: 지불액(Sell.AmountInUSD) ≥ MIN_USD(기본 $1,000, 분포분석 근거).
- 중복제거: 처리한 tx signature를 state에 저장. 폴링 간격마다 last_time 이후만.

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
        'Trade { Sell { AmountInUSD } Buy { Currency { Symbol MintAddress } Account { Owner } } } } } }'
    ) % (json.dumps(wallets), json.dumps(_BASE_MINTS), json.dumps(_BASE_MINTS), int(MIN_USD), since_iso)
    key = _env("BITQUERY_API_KEY")
    d = _post(_EAP, {"query": q}, {"Content-Type": "application/json", "X-API-KEY": key or ""})
    if not d.get("data"):
        raise RuntimeError(f"Bitquery 오류: {str(d.get('errors'))[:200]}")
    return d["data"]["Solana"]["DEXTrades"]


def send_telegram(text: str) -> None:
    # ★매매봇과 분리★ 전용 봇/채널 사용. 미설정 시 콘솔만(매매봇 채널로 폴백하지 않음).
    tok = _env("MEMEWALLET_TELEGRAM_BOT_TOKEN")
    chat = _env("MEMEWALLET_TELEGRAM_CHAT_ID")
    if not tok or not chat:
        print("[밈 알림봇 텔레그램 미설정 — 콘솔만. .env에 MEMEWALLET_TELEGRAM_BOT_TOKEN/"
              "MEMEWALLET_TELEGRAM_CHAT_ID 추가하면 별도 채널로 전송]"); return
    url = f"https://api.telegram.org/bot{tok}/sendMessage"
    body = {"chat_id": chat, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    try:
        _post(url, body, {"Content-Type": "application/json"})
    except Exception as e:  # noqa: BLE001
        print("텔레그램 전송 실패:", e)


def _fmt(t: dict, pnl_by_wallet: dict[str, float]) -> str:
    tr = t["Trade"]; owner = tr["Buy"]["Account"]["Owner"]
    sym = tr["Buy"]["Currency"]["Symbol"]; mint = tr["Buy"]["Currency"]["MintAddress"]
    usd = float(tr["Sell"]["AmountInUSD"]); life = pnl_by_wallet.get(owner, 0)
    return (f"🟢 <b>스마트머니 매수</b>\n"
            f"지갑 <code>{owner[:6]}…{owner[-4:]}</code> (통산 ${life:,.0f})\n"
            f"매수 <b>{sym}</b>  ${usd:,.0f}\n"
            f"<a href='https://gmgn.ai/sol/token/{mint}'>차트</a> · "
            f"<a href='https://solscan.io/account/{owner}'>지갑</a>")


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
                msg = _fmt(t, wmap)
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
