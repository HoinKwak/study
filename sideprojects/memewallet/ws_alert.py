"""Helius WebSocket 실시간 감지 알림봇 (Bitquery 폴링 대체 · 재설계판).

Bitquery 폴링(무료 월 1,000pt라 몇 시간이면 소진)을 버리고, Helius 무료(월 1M 크레딧) WebSocket
`logsSubscribe`로 스마트머니 지갑들의 트랜잭션을 **실시간 푸시**로 받아 베이스(SOL/USDC/USDT)→밈
매수를 판별한다. 알림 부가정보·포맷·텔레그램·중복제거는 기존 alert_bot.py를 그대로 재사용.

왜 WebSocket인가: 봇이 로컬 PC에서 돌아 공개 URL이 없으므로 웹훅(Helius→URL POST) 대신 봇이
밖으로 연결하는 WS가 맞다. 무료 티어는 표준 `logsSubscribe`만 되고(지갑당 1구독), 향상된
`transactionSubscribe`(다주소 1구독)는 유료 Developer($49/월)부터다.

동작:
1. wss://mainnet.helius-rpc.com/?api-key=KEY 에 연결, 감시 지갑마다 logsSubscribe.
2. 알림(logsNotification)에서 signature 획득 → Helius Enhanced Tx(/v0/transactions)로 파싱.
3. tokenTransfers/nativeTransfers에서 '지갑이 받은 비베이스 토큰(매수) + 지불한 베이스(USD)' 추출.
4. ≥ MIN_USD($1,000) 매수만 → enrich(신규/추매·잔고·역대손익) → send_telegram.

실행: python sideprojects/memewallet/ws_alert.py [--dry] [--keep-exited] [--min USD]
      python sideprojects/memewallet/ws_alert.py --test-sig <SIGNATURE>   # 파싱만 검증(키 필요)
      --min: 매수 최소 USD 하향(기본 $1,000). 예 `--min 50` = 파이프라인 감지·발송 검증용.
키: .env HELIUS_API_KEY + (기존) MEMEWALLET_TELEGRAM_BOT_TOKEN/CHAT_ID.
의존: pip install websocket-client
"""
from __future__ import annotations

import json
import sys
import threading
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import alert_bot as _ab  # 모듈 참조(enrich가 쓰는 token_balance/token_realized를 Helius판으로 교체용)
from alert_bot import (  # 기존 헬퍼 재사용
    MIN_USD, _BASE_MINTS, _STATE, _env, _fmt, _wallets, enrich, send_telegram,
)

_WSOL = "So11111111111111111111111111111111111111112"
_USD_BASE = {  # 지불액이 곧 USD인 스테이블
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",   # USDC
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",   # USDT
}
_BASE = set(_BASE_MINTS)
_ENH = "https://api.helius.xyz/v0/transactions/?api-key={k}"
_WS = "wss://mainnet.helius-rpc.com/?api-key={k}"
_sym_cache: dict[str, str] = {}
_sol_px = [0.0, 0.0]   # (price, ts)
_MIN = MIN_USD   # 매수 최소 USD(기본 $1,000). --min 으로 낮춰 파이프라인 검증 가능.
_parse_errs: list[str] = []   # parse_signature 실패 사유(첫 5건) — 크레딧소진/레이트리밋 진단용


def _post_json(url: str, body: dict) -> dict | list:
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:  # noqa: S310
        return json.load(r)


def _get_json(url: str):
    with urllib.request.urlopen(url, timeout=15) as r:  # noqa: S310
        return json.load(r)


def sol_price() -> float:
    """SOL 현재가(USD). 5분 캐시, 실패 시 마지막값/폴백."""
    if _sol_px[0] > 0 and time.time() - _sol_px[1] < 300:
        return _sol_px[0]
    try:
        d = _get_json("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
        _sol_px[0] = float(d["solana"]["usd"]); _sol_px[1] = time.time()
    except Exception:  # noqa: BLE001
        pass
    return _sol_px[0] or 150.0


def token_symbol(mint: str) -> str:
    """DexScreener로 심볼 조회(캐시). 실패 시 mint 앞 4자."""
    if mint in _sym_cache:
        return _sym_cache[mint]
    sym = mint[:4]
    try:
        d = _get_json(f"https://api.dexscreener.com/latest/dex/tokens/{mint}")
        for p in (d.get("pairs") or []):
            if (p.get("baseToken") or {}).get("address") == mint:
                sym = p["baseToken"].get("symbol") or sym; break
    except Exception:  # noqa: BLE001
        pass
    _sym_cache[mint] = sym
    return sym


def _helius_rpc(method: str, params: list):
    key = _env("HELIUS_API_KEY")
    return _post_json(f"https://mainnet.helius-rpc.com/?api-key={key}",
                      {"jsonrpc": "2.0", "id": 1, "method": method, "params": params})


def token_balance_helius(owner: str, mint: str) -> float | None:
    """지갑의 해당 토큰 현재 잔고(UI). Helius RPC getTokenAccountsByOwner. (Bitquery 미사용)"""
    try:
        d = _helius_rpc("getTokenAccountsByOwner", [owner, {"mint": mint}, {"encoding": "jsonParsed"}])
        tot = 0.0
        for a in (d.get("result") or {}).get("value") or []:
            tot += float(a["account"]["data"]["parsed"]["info"]["tokenAmount"].get("uiAmount") or 0.0)
        return tot
    except Exception:  # noqa: BLE001
        return None


def token_realized_helius(wallet: str, mint: str, pages: int = 3) -> dict | None:
    """해당 (지갑,토큰) 매수/매도 누적 USD → 실현손익 근사. Helius 주소 SWAP tx. (Bitquery 대체)

    USD: 스테이블(USDC/USDT) 레그=정확, SOL 레그=현재 SOL가 근사. 최근 pages×100건 창(근사).
    반환 {"buy_usd","sell_usd","pnl","sells"} | None.
    """
    key = _env("HELIUS_API_KEY")
    if not key:
        return None
    buy_usd = sell_usd = 0.0
    sells = 0
    px = sol_price()
    before = None
    try:
        for _ in range(pages):
            url = (f"https://api.helius.xyz/v0/addresses/{wallet}/transactions/"
                   f"?api-key={key}&type=SWAP&limit=100")
            if before:
                url += f"&before={before}"
            txs = _get_json(url)
            if not isinstance(txs, list) or not txs:
                break
            for tx in txs:
                recv = sent = 0.0
                sol_o = sol_i = usd_o = usd_i = 0.0
                involved = False
                for tt in tx.get("tokenTransfers") or []:
                    m = tt.get("mint"); amt = float(tt.get("tokenAmount") or 0.0)
                    if m == mint:
                        involved = True
                        if tt.get("toUserAccount") == wallet:
                            recv += amt
                        if tt.get("fromUserAccount") == wallet:
                            sent += amt
                    if tt.get("fromUserAccount") == wallet:
                        if m in _USD_BASE:
                            usd_o += amt
                        elif m == _WSOL:
                            sol_o += amt
                    if tt.get("toUserAccount") == wallet:
                        if m in _USD_BASE:
                            usd_i += amt
                        elif m == _WSOL:
                            sol_i += amt
                for nt in tx.get("nativeTransfers") or []:
                    a = float(nt.get("amount") or 0.0) / 1e9
                    if nt.get("fromUserAccount") == wallet:
                        sol_o += a
                    elif nt.get("toUserAccount") == wallet:
                        sol_i += a
                if not involved:
                    continue
                if recv > sent:       # 순매수
                    buy_usd += usd_o + max(0.0, sol_o - sol_i) * px
                elif sent > recv:     # 순매도
                    sell_usd += usd_i + max(0.0, sol_i - sol_o) * px
                    sells += 1
            before = txs[-1].get("signature")
            if len(txs) < 100:
                break
        return {"buy_usd": buy_usd, "sell_usd": sell_usd, "pnl": sell_usd - buy_usd, "sells": sells}
    except Exception:  # noqa: BLE001
        return None


def extract_buy(tx: dict, wallet: str) -> dict | None:
    """Helius Enhanced Tx에서 wallet의 '베이스→밈 매수' 추출 → {mint,bought,usd} | None.

    - 매수 토큰: wallet이 받은(toUserAccount) 비베이스 mint 중 최대 수량.
    - 지불 USD: 나간 USDC/USDT(≈USD) + 나간 SOL(WSOL 언랩+네이티브)×SOL가. 되받은 SOL은 상계.
    """
    if not tx or tx.get("transactionError"):
        return None
    bought_mint, bought_amt = None, 0.0
    usd_out = 0.0
    sol_out = sol_in = 0.0
    for tt in tx.get("tokenTransfers") or []:
        mint = tt.get("mint"); amt = float(tt.get("tokenAmount") or 0.0)
        if tt.get("toUserAccount") == wallet and mint not in _BASE and amt > bought_amt:
            bought_mint, bought_amt = mint, amt
        if tt.get("fromUserAccount") == wallet:
            if mint in _USD_BASE:
                usd_out += amt
            elif mint == _WSOL:
                sol_out += amt
        if tt.get("toUserAccount") == wallet and mint == _WSOL:
            sol_in += amt
    for nt in tx.get("nativeTransfers") or []:
        amt = float(nt.get("amount") or 0.0) / 1e9
        if nt.get("fromUserAccount") == wallet:
            sol_out += amt
        elif nt.get("toUserAccount") == wallet:
            sol_in += amt
    usd = usd_out + max(0.0, sol_out - sol_in) * sol_price()
    if not bought_mint or usd < _MIN:
        return None
    return {"mint": bought_mint, "bought": bought_amt, "usd": usd}


def _to_trade(buy: dict, wallet: str, sig: str) -> dict:
    """extract_buy 결과 → 기존 enrich/_fmt가 먹는 t(Trade) 구조로 변환."""
    return {"Trade": {"Sell": {"AmountInUSD": buy["usd"]},
                      "Buy": {"Amount": buy["bought"],
                              "Currency": {"Symbol": token_symbol(buy["mint"]),
                                           "MintAddress": buy["mint"]},
                              "Account": {"Owner": wallet}}},
            "Transaction": {"Signature": sig}}


def parse_signature(sig: str, key: str) -> dict | None:
    """signature → Helius Enhanced Tx(파싱). 실패/미발견 시 None."""
    try:
        d = _post_json(_ENH.format(k=key), {"transactions": [sig]})
    except Exception as e:  # noqa: BLE001
        if len(_parse_errs) < 5:      # 첫 5건만 보관(크레딧소진 401·레이트리밋 429 등 진단)
            _parse_errs.append(str(e)[:120])
        return None
    return d[0] if isinstance(d, list) and d else None


def handle_signature(sig: str, wallet: str, key: str, wmap: dict, seen: set,
                     dry: bool, keep_exited: bool, funnel: dict | None = None) -> str:
    """서명 1건 처리: 파싱→매수판별→enrich→발송. 반환: 'sent'|'skip'|'none'.

    funnel(선택): 어디서 걸러지는지 계측 카운터(attempt/parse_fail/parsed/buy). 진단용.
    """
    if sig in seen:
        return "none"
    seen.add(sig)
    if funnel is not None:
        funnel["attempt"] += 1
    tx = parse_signature(sig, key)
    if not tx:
        if funnel is not None:
            funnel["parse_fail"] += 1
        return "none"
    if funnel is not None:
        funnel["parsed"] += 1
    buy = extract_buy(tx, wallet)
    if not buy:
        return "none"
    if funnel is not None:
        funnel["buy"] += 1
    t = _to_trade(buy, wallet, sig)
    ex = enrich(t, keep_exited=keep_exited)   # 스킵분은 Bitquery 생략(포인트 절약)
    if ex.get("skip"):
        print(f"[스킵] 사자마자 매도 — {t['Trade']['Buy']['Currency']['Symbol']} {wallet[:6]}…{wallet[-4:]}")
        return "skip"
    msg = _fmt(t, wmap, ex)
    print(msg.replace("\n", " | "))
    if not dry:
        send_telegram(msg)
    return "sent"


def run(dry: bool = False, keep_exited: bool = False, min_usd: float | None = None) -> None:
    import websocket  # 지연 임포트(미설치 시 안내)

    global _MIN
    if min_usd is not None:
        _MIN = min_usd   # 검증용 임계값 하향(--min). 기본은 $1,000.
    key = _env("HELIUS_API_KEY")
    if not key:
        print("[오류] .env에 HELIUS_API_KEY가 없습니다. helius.dev 무료 가입 후 키를 추가하세요.")
        return
    # ★Bitquery 완전 제거★ enrich의 잔고·역대손익을 Helius판으로 교체(monkeypatch)
    _ab.token_balance = token_balance_helius
    _ab.token_realized = token_realized_helius
    wmap = _wallets(); wallets = list(wmap)
    st = json.loads(_STATE.read_text()) if _STATE.exists() else {}
    seen: set[str] = set(st.get("seen", []))
    sub_wallet: dict[int, str] = {}      # 구독번호 → 지갑
    req_wallet: dict[int, str] = {}      # 요청id → 지갑
    stat = {"sent": 0, "skip": 0}
    state = {"confirmed": 0, "sub_err": 0, "events": 0}
    funnel = {"resolved": 0, "attempt": 0, "parse_fail": 0, "parsed": 0, "buy": 0}  # 진단 퍼널

    def on_open(ws):
        sub_wallet.clear(); req_wallet.clear()
        state["confirmed"] = 0; state["sub_err"] = 0
        for i, w in enumerate(wallets):
            req_wallet[i] = w
            ws.send(json.dumps({"jsonrpc": "2.0", "id": i, "method": "logsSubscribe",
                                "params": [{"mentions": [w]}, {"commitment": "confirmed"}]}))
        print(f"[WS] {len(wallets)}지갑 구독 요청, ≥${_MIN:,.0f}, dry={dry}, "
              f"사자마자매도={'표시' if keep_exited else '필터링'}")

    def on_message(ws, raw):
        try:
            m = json.loads(raw)
        except Exception:  # noqa: BLE001
            return
        # 구독 오류: {id, error}
        if "error" in m:
            state["sub_err"] += 1
            if state["sub_err"] <= 3:
                print("[WS] 구독 오류:", str(m.get("error"))[:140])
            return
        # 구독 확정: {id, result: subNumber}
        if "id" in m and isinstance(m.get("result"), int):
            w = req_wallet.get(m["id"])
            if w:
                sub_wallet[m["result"]] = w
            state["confirmed"] += 1
            if state["confirmed"] == len(wallets):
                print(f"[WS] ✅ 구독 확정 {state['confirmed']}/{len(wallets)} — 실시간 감시 시작"
                      + (f" (구독오류 {state['sub_err']})" if state["sub_err"] else ""))
            return
        if m.get("method") != "logsNotification":
            return
        state["events"] += 1
        val = (((m.get("params") or {}).get("result") or {}).get("value") or {})
        if val.get("err"):     # 실패 tx 무시
            return
        sig = val.get("signature")
        w = sub_wallet.get((m.get("params") or {}).get("subscription"))
        if not sig or not w:
            return
        funnel["resolved"] += 1   # 지갑·서명 매핑 성공(여기까진 정상 수신)
        try:
            r = handle_signature(sig, w, key, wmap, seen, dry, keep_exited, funnel)
        except Exception as e:  # noqa: BLE001
            print("처리 오류:", str(e)[:120]); return
        if r in stat:
            stat[r] += 1
        # 주기적 state 저장(seen 최근 4000개)
        _STATE.write_text(json.dumps({"seen": list(seen)[-4000:], "last_time": st.get("last_time", "")}))

    def on_error(ws, e):
        print("[WS 오류]", str(e)[:120])

    def on_close(ws, code, msg):
        sub_wallet.clear(); req_wallet.clear()
        print(f"[WS 종료] code={code} → 재접속 대기")

    def _heartbeat():
        # 조용해도 살아있음을 보이게 상태 출력(감시 대상 매수는 원래 드묾).
        # 첫 틱은 2분 뒤(진단 빠르게), 이후 10분 주기.
        interval = 120
        while True:
            time.sleep(interval)
            interval = 600
            print(f"[WS] 감시 중 — 구독 {state['confirmed']}/{len(wallets)} · "
                  f"수신이벤트 {state['events']} · 발송 {stat['sent']} · 스킵 {stat['skip']}")
            # 진단 퍼널: 어디서 걸러지는지. parse_fail이 크면 Helius 크레딧소진/레이트리밋 의심.
            print(f"[WS] 퍼널 — 매핑 {funnel['resolved']} · 파싱시도 {funnel['attempt']} · "
                  f"파싱실패 {funnel['parse_fail']} · 파싱성공 {funnel['parsed']} · 매수감지 {funnel['buy']}")
            if _parse_errs:
                print(f"[WS] 파싱에러 예시: {_parse_errs[0]}")
    threading.Thread(target=_heartbeat, daemon=True).start()

    ws = websocket.WebSocketApp(_WS.format(k=key), on_open=on_open, on_message=on_message,
                                on_error=on_error, on_close=on_close)
    ws.run_forever(reconnect=5, ping_interval=30, ping_timeout=10)   # 끊기면 자동 재접속·재구독


def _test_sig(sig: str) -> None:
    """단일 서명 파싱 검증(라이브 발송 없이). 감시 지갑 중 매수자 자동 탐지."""
    key = _env("HELIUS_API_KEY")
    if not key:
        print("[오류] HELIUS_API_KEY 필요"); return
    _ab.token_balance = token_balance_helius
    _ab.token_realized = token_realized_helius
    tx = parse_signature(sig, key)
    if not tx:
        print("파싱 실패/미발견"); return
    print("type:", tx.get("type"), "| tokenTransfers:", len(tx.get("tokenTransfers") or []),
          "| nativeTransfers:", len(tx.get("nativeTransfers") or []))
    wmap = _wallets()
    hit = False
    for w in wmap:
        buy = extract_buy(tx, w)
        if buy:
            hit = True
            print(f"  매수감지 지갑 {w[:6]}…: {token_symbol(buy['mint'])} "
                  f"{buy['bought']:,.0f}개 ≈${buy['usd']:,.0f} (mint {buy['mint']})")
    if not hit:
        print("  (감시 지갑의 ≥$%.0f 베이스→밈 매수 없음)" % MIN_USD)


if __name__ == "__main__":
    if "--test-sig" in sys.argv:
        i = sys.argv.index("--test-sig")
        _test_sig(sys.argv[i + 1])
    else:
        _min = None
        if "--min" in sys.argv:
            _min = float(sys.argv[sys.argv.index("--min") + 1])
        run(dry="--dry" in sys.argv, keep_exited="--keep-exited" in sys.argv, min_usd=_min)
