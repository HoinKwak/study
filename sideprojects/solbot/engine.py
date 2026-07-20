"""solbot 페이퍼 브로커 — 드라이런 자동매매 엔진.

시그널(밈월렛 스마트머니 매수 등)이 들어오면 필터→사이징→가상 매수를 하고,
주기적으로 마크(왕복 견적)해 청산 조건을 판정한다. 실제 스왑은 하지 않고(DRY_RUN),
가상 PnL을 저널에 남겨 "이 시그널이 수수료·슬리피지 감안해도 +인지"를 검증한다.

라이브 전환(config.DRY_RUN=False) 시 execute_live(미구현)에서 Jupiter 스왑을 서명·전송한다.
"""
from __future__ import annotations

import json
import time
import urllib.request
from datetime import datetime, timezone

from . import config as C
from . import jupiter as J


# ── DexScreener 보조(유동성·심볼) ────────────────────────────────────────────
def token_info(mint: str) -> dict:
    """DexScreener로 심볼·유동성·priceUsd 조회. 실패 시 빈 기본값."""
    out = {"symbol": mint[:4], "liquidity_usd": 0.0, "price_usd": 0.0}
    try:
        req = urllib.request.Request(   # UA 없으면 DexScreener(CF)가 차단 → 반드시 지정
            f"https://api.dexscreener.com/latest/dex/tokens/{mint}",
            headers={"User-Agent": "Mozilla/5.0 (solbot)"})
        with urllib.request.urlopen(req, timeout=12) as r:  # noqa: S310
            d = json.load(r)
        best = None
        for p in (d.get("pairs") or []):
            if (p.get("baseToken") or {}).get("address") != mint:
                continue
            liq = float((p.get("liquidity") or {}).get("usd") or 0.0)
            if best is None or liq > best[0]:
                best = (liq, p)
        if best:
            _, p = best
            out["symbol"] = (p.get("baseToken") or {}).get("symbol") or out["symbol"]
            out["liquidity_usd"] = float((p.get("liquidity") or {}).get("usd") or 0.0)
            out["price_usd"] = float(p.get("priceUsd") or 0.0)
    except Exception:  # noqa: BLE001
        pass
    return out


def _now() -> float:
    return time.time()


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


class PaperBroker:
    """페이퍼 포지션·현금·실현손익을 저널에 영속화하는 드라이런 브로커."""

    def __init__(self) -> None:
        C.STATE_DIR.mkdir(parents=True, exist_ok=True)
        self.st = self._load()

    # 영속화 ------------------------------------------------------------------
    def _load(self) -> dict:
        if C.JOURNAL.exists():
            return json.loads(C.JOURNAL.read_text())
        return {"cash_usd": C.PORTFOLIO_START_USD, "positions": [], "closed": [],
                "realized_pnl": 0.0, "day": _today(), "day_realized": 0.0,
                "created": _now()}

    def _save(self) -> None:
        C.JOURNAL.write_text(json.dumps(self.st, ensure_ascii=False, indent=2))

    # 조회 --------------------------------------------------------------------
    def portfolio_value(self) -> float:
        return self.st["cash_usd"] + sum(p["last_mark_usd"] for p in self.st["positions"])

    def _roll_day(self) -> None:
        if self.st["day"] != _today():
            self.st["day"] = _today()
            self.st["day_realized"] = 0.0

    def _held_mints(self) -> set[str]:
        return {p["mint"] for p in self.st["positions"]}

    # 진입 --------------------------------------------------------------------
    def can_buy(self, mint: str, symbol: str) -> tuple[bool, str]:
        """진입 가능 여부와 사유. 필터·상한·킬스위치 점검."""
        self._roll_day()
        if C.DRY_RUN is False:
            return False, "라이브 미구현(execute_live 필요)"
        if len(self.st["positions"]) >= C.MAX_CONCURRENT:
            return False, f"동시보유 상한({C.MAX_CONCURRENT}) 도달"
        if mint in self._held_mints():
            return False, "이미 보유중(추매 미지원)"
        if (symbol or "").upper() in C.BLACKLIST_SYMBOLS:
            return False, f"블랙리스트 심볼({symbol})"
        loss_limit = -C.DAILY_LOSS_LIMIT_PCT * C.PORTFOLIO_START_USD
        if self.st["day_realized"] <= loss_limit:
            return False, f"일일 손실한도 도달(킬스위치, {self.st['day_realized']:.1f})"
        return True, "ok"

    def buy(self, mint: str, signal: dict | None = None) -> dict | None:
        """시그널 매수. 필터 통과 시 가상 포지션 오픈, 실패 시 None(사유 print)."""
        info = token_info(mint)
        symbol = info["symbol"]
        ok, why = self.can_buy(mint, symbol)
        if not ok:
            print(f"[진입거부] {symbol} {mint[:6]}… — {why}")
            return None
        if info["liquidity_usd"] < C.MIN_LIQUIDITY_USD:
            print(f"[진입거부] {symbol} — 유동성 부족 ${info['liquidity_usd']:,.0f} < ${C.MIN_LIQUIDITY_USD:,.0f}")
            return None
        pv = self.portfolio_value()
        size = round(C.PER_TRADE_PCT * pv, 2)
        if size > self.st["cash_usd"]:
            size = round(self.st["cash_usd"], 2)   # 남은 현금까지만
        if size < 1.0:
            print(f"[진입거부] {symbol} — 가용현금 부족(${self.st['cash_usd']:.2f})")
            return None
        sim = J.sim_buy(mint, size, C.DEFAULT_SLIPPAGE_BPS)
        if not sim:
            print(f"[진입거부] {symbol} — Jupiter 견적 실패(라우트 없음)")
            return None
        if sim["price_impact_pct"] > C.MAX_PRICE_IMPACT_PCT:
            print(f"[진입거부] {symbol} — 가격영향 {sim['price_impact_pct']:.2f}% > {C.MAX_PRICE_IMPACT_PCT}%")
            return None
        pos = {
            "id": f"{mint[:6]}-{int(_now())}", "mint": mint, "symbol": symbol,
            "entry_ts": _now(), "entry_usd": size, "tokens_base": sim["tokens_base"],
            "high_usd": size, "last_mark_usd": size, "last_mark_ts": _now(),
            "entry_impact_pct": round(sim["price_impact_pct"], 3),
            "signal": signal or {},
        }
        self.st["cash_usd"] -= size
        self.st["positions"].append(pos)
        self._save()
        print(f"[가상매수] {symbol} ${size:.2f} (영향 {sim['price_impact_pct']:.2f}%, "
              f"현금 ${self.st['cash_usd']:.2f}, 보유 {len(self.st['positions'])}개)")
        return pos

    # 마크·청산 ---------------------------------------------------------------
    def mark_all(self) -> None:
        """보유 포지션 왕복 견적으로 현재가치 갱신 + 신고가 추적."""
        for p in self.st["positions"]:
            v = J.sim_value(p["mint"], p["tokens_base"], C.DEFAULT_SLIPPAGE_BPS)
            if v is not None:
                p["last_mark_usd"] = round(v, 4)
                p["last_mark_ts"] = _now()
                if v > p["high_usd"]:
                    p["high_usd"] = round(v, 4)
        self._save()

    def _exit_reason(self, p: dict) -> str | None:
        """청산 사유 판정(EXIT_MODE별). None=유지."""
        entry, mark, high = p["entry_usd"], p["last_mark_usd"], p["high_usd"]
        held_h = (_now() - p["entry_ts"]) / 3600.0
        if held_h >= C.MAX_HOLD_HOURS:
            return f"시간초과({held_h:.0f}h)"
        if C.EXIT_MODE == "fixed":
            if mark >= entry * (1 + C.TP_PCT):
                return f"익절+{C.TP_PCT*100:.0f}%"
            if mark <= entry * (1 - C.SL_PCT):
                return f"손절-{C.SL_PCT*100:.0f}%"
        elif C.EXIT_MODE == "trailing":
            if mark <= high * (1 - C.TRAIL_PCT):
                return f"트레일링(신고가${high:.2f}대비-{C.TRAIL_PCT*100:.0f}%)"
        else:   # assist(반자동): 하드 손절만 자동, 익절은 알림(측정 위해 손절·시간만 종료)
            if mark <= entry * (1 - C.SL_PCT):
                return f"손절-{C.SL_PCT*100:.0f}%(하드)"
        return None

    def check_exits(self) -> list[dict]:
        """청산 조건 충족분 종료(페이퍼). 종료 목록 반환."""
        exited = []
        keep = []
        for p in self.st["positions"]:
            reason = self._exit_reason(p)
            if reason is None:
                # assist 모드: 익절 구간이면 청산 '제안' 알림만(자동종료 X)
                if C.EXIT_MODE == "assist" and p["last_mark_usd"] >= p["entry_usd"] * (1 + C.TP_PCT):
                    print(f"[청산제안] {p['symbol']} +{(p['last_mark_usd']/p['entry_usd']-1)*100:.0f}% — 승인 시 청산")
                keep.append(p)
                continue
            pnl = round(p["last_mark_usd"] - p["entry_usd"], 4)
            rec = {**p, "exit_ts": _now(), "exit_usd": p["last_mark_usd"],
                   "pnl_usd": pnl, "pnl_pct": round(pnl / p["entry_usd"] * 100, 2),
                   "reason": reason}
            self.st["cash_usd"] += p["last_mark_usd"]
            self.st["realized_pnl"] += pnl
            self.st["day_realized"] += pnl
            self.st["closed"].append(rec)
            exited.append(rec)
            print(f"[가상청산] {p['symbol']} {reason} → PnL ${pnl:+.2f} ({rec['pnl_pct']:+.1f}%)")
        self.st["positions"] = keep
        self._save()
        return exited

    def summary(self) -> str:
        pv = self.portfolio_value()
        n_closed = len(self.st["closed"])
        wins = sum(1 for c in self.st["closed"] if c["pnl_usd"] > 0)
        wr = (wins / n_closed * 100) if n_closed else 0.0
        return (f"[요약] 포트폴리오 ${pv:.2f} (시작 ${C.PORTFOLIO_START_USD:.0f}, "
                f"현금 ${self.st['cash_usd']:.2f}, 보유 {len(self.st['positions'])}개) · "
                f"실현 ${self.st['realized_pnl']:+.2f} · 청산 {n_closed}건 승률 {wr:.0f}%")


if __name__ == "__main__":   # 데모: python -m sideprojects.solbot.engine <mint> [usd]
    import sys
    b = PaperBroker()
    if len(sys.argv) > 1:
        b.buy(sys.argv[1], signal={"src": "manual-demo"})
    b.mark_all()
    b.check_exits()
    print(b.summary())
