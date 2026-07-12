"""거래 저널 심층 분석 + 개선 권고.

    python -m scripts.analyze_trades              # 전체 분석 + 권고
    python -m scripts.analyze_trades --top 12     # 심볼 상위 N 표시
    python -m scripts.analyze_trades --csv f.csv  # 저널 대신 CSV 파일 분석

승률·손익비(PF)·손익크기비·기대값·MDD·연승연패에 더해, **수수료 드래그**(taker_fee_pct
기준 추정)·방향/청산사유/슬리브/심볼별 분해·명목가 분포를 뜯어보고, 규칙 기반으로
**개선 권고**를 자동 생성한다. 표본이 작으면 그 한계도 함께 알린다. 투자조언 아님.
"""
from __future__ import annotations

import argparse
import csv as csvmod
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.monitoring import TradeJournal  # noqa: E402


@dataclass
class Row:
    symbol: str
    direction: str
    sleeve: str
    quantity: float
    entry: float
    exit: float
    pnl: float
    reason: str

    @property
    def notional(self) -> float:
        return self.entry * self.quantity

    def fee(self, taker_pct: float) -> float:
        """왕복 테이커 수수료 추정 = fee% × (진입가+청산가) × 수량."""
        return (taker_pct / 100.0) * (self.entry + self.exit) * self.quantity


def _rows_from_journal(state_dir: str) -> list[Row]:
    j = TradeJournal(state_dir)
    out = []
    for t in j.trades:
        if t.exit_price is None or t.pnl is None:
            continue
        out.append(Row(t.symbol, t.direction, getattr(t, "sleeve", "") or "",
                       t.quantity or 0.0, t.entry_price or 0.0, t.exit_price or 0.0,
                       float(t.pnl), getattr(t, "exit_reason", "") or ""))
    return out


def _rows_from_csv(path: str) -> list[Row]:
    out = []
    for r in csvmod.DictReader(open(path, encoding="utf-8-sig")):
        try:
            if not r.get("exit_price"):
                continue
            out.append(Row(r["symbol"], r["direction"], r.get("sleeve", ""),
                           float(r["quantity"]), float(r["entry_price"]),
                           float(r["exit_price"]), float(r["pnl_usdt"]),
                           r.get("exit_reason", "")))
        except (ValueError, KeyError):
            continue
    return out


def _max_drawdown(pnls: list[float]) -> float:
    cum = peak = mdd = 0.0
    for p in pnls:
        cum += p
        peak = max(peak, cum)
        mdd = min(mdd, cum - peak)
    return mdd


def _streaks(pnls: list[float]) -> tuple[int, int]:
    """(최대 연승, 최대 연패)."""
    mw = ml = cw = cl = 0
    for p in pnls:
        if p > 0:
            cw += 1; cl = 0
        elif p < 0:
            cl += 1; cw = 0
        else:
            cw = cl = 0
        mw = max(mw, cw); ml = max(ml, cl)
    return mw, ml


def _fmt_group(title: str, groups: dict, key_w: int = 18) -> list[str]:
    lines = [f"  ── {title} ──"]
    for k, v in sorted(groups.items(), key=lambda x: sum(x[1])):
        wr = sum(1 for x in v if x > 0) / len(v) * 100 if v else 0
        lines.append(f"    {str(k)[:key_w]:<{key_w}} {len(v):>3}건  {sum(v):>+9.2f}  승률 {wr:>3.0f}%")
    return lines


def _recommend(rows: list[Row], taker_pct: float) -> list[str]:
    pnls = [r.pnl for r in rows]
    n = len(rows)
    gp = sum(p for p in pnls if p > 0)
    gl = -sum(p for p in pnls if p < 0)
    net = sum(pnls)
    fee = sum(r.fee(taker_pct) for r in rows)
    net_af = net - fee
    recs: list[str] = []

    if n < 30:
        recs.append(f"표본 {n}건 — 통계적으로 확정하기엔 작다. 경향 파악·비용 구조 점검 위주로 해석.")
    if gp > 0 and fee / gp >= 0.25:
        recs.append(f"⚠️ 수수료가 총이익의 {fee/gp*100:.0f}%를 잠식(-{fee:.0f}). "
                    f"메이커(post-only) 진입 비중↑·진입 빈도↓·최소 익절폭↑로 비용을 줄여야 엣지가 남는다.")
    if net > 0 and net_af < net * 0.5:
        recs.append(f"⚠️ 수수료가 순익의 대부분을 먹음: 차감 전 {net:+.0f} → 차감 후 {net_af:+.0f}"
                    f"({(1-net_af/net)*100:.0f}% 감소). 실질 엣지가 얇으니 비용 절감이 최우선.")
    if net_af <= 0 < net:
        recs.append(f"⚠️ 수수료 차감 후 순손실({net_af:+.0f}) — 현 빈도·사이즈로는 실질 엣지 없음.")
    # 단일 종목 편중(꼬리 의존): 최고 손익 종목을 빼면 순손익이 뒤집히는지
    bysym: dict[str, float] = defaultdict(float)
    for r in rows:
        bysym[r.symbol] += r.pnl
    if bysym:
        best_sym = max(bysym, key=bysym.get)
        net_wo = net - bysym[best_sym]
        if bysym[best_sym] > 0 and net_wo <= 0:
            recs.append(f"성과가 '{best_sym}' 한 종목에 편중(+{bysym[best_sym]:.0f}). "
                        f"이 종목 빼면 순손익 {net_wo:+.0f} — 우연/뒷북일 수 있어 신뢰도 낮게 볼 것.")
    # 청산사유별 순손실
    byreason: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        byreason[r.reason].append(r.pnl)
    for k, v in byreason.items():
        if len(v) >= 3 and sum(v) < 0:
            recs.append(f"청산사유 '{k}' {len(v)}건 순손실({sum(v):+.0f}) — 이 청산 규칙(조건·타이밍)을 재검토.")
    # 방향 편향
    for d in ("long", "short"):
        sub = [r.pnl for r in rows if r.direction == d]
        opp = [r.pnl for r in rows if r.direction != d]
        if sub and opp and sum(sub) < 0 < sum(opp):
            recs.append(f"{d.upper()} 방향만 순손실({sum(sub):+.0f}) — 해당 방향 진입·청산 규칙 또는 시장국면 필터 점검.")
    # 대박거래 편중
    if gp > 0:
        top = max(pnls)
        if top / gp > 0.4:
            recs.append(f"성과가 단일 대박거래에 편중(최고 +{top:.0f} = 총이익의 {top/gp*100:.0f}%). "
                        f"그 거래 빼면 결과가 크게 달라짐 — 신뢰도 낮게 볼 것.")
    # 대형 명목가 성과
    notl = sorted(r.notional for r in rows)
    if len(notl) >= 8:
        thr = notl[int(len(notl) * 0.75)]
        big = [r.pnl for r in rows if r.notional >= thr]
        if big and sum(big) < 0:
            recs.append(f"명목가 상위 25%(≥{thr:,.0f}) 포지션이 순손실({sum(big):+.0f}) — "
                        f"사이즈/레버리지를 키운 거래가 오히려 손실. 대형 포지션 진입 기준을 더 엄격히.")
    if not recs:
        recs.append("치명적 이상 신호는 없음 — 표본을 더 쌓으며 수수료·MDD를 모니터링.")
    return recs


def analyze(rows: list[Row], taker_pct: float, top: int) -> str:
    if not rows:
        return "청산된 거래가 없습니다."
    pnls = [r.pnl for r in rows]
    n = len(rows)
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    gp, gl, net = sum(wins), -sum(losses), sum(pnls)
    pf = gp / gl if gl > 0 else float("inf")
    aw = gp / len(wins) if wins else 0.0
    al = gl / len(losses) if losses else 0.0
    payoff = aw / al if al > 0 else float("inf")
    fee = sum(r.fee(taker_pct) for r in rows)
    mw, ml = _streaks(pnls)
    notl = [r.notional for r in rows]

    out = ["", "══════════ 거래 분석 ══════════",
           f" 청산 {n}건 (부분청산 포함) | 승 {len(wins)} / 패 {len(losses)}",
           f" 순손익      : {net:+.2f} USDT   (총이익 {gp:.2f} / 총손실 -{gl:.2f})",
           f" 손익비(PF)  : {pf:.2f}   승률 {len(wins)/n*100:.1f}%   손익크기비 {payoff:.2f}",
           f" 기대값/건   : {net/n:+.2f}   최고 {max(pnls):+.2f} / 최악 {min(pnls):+.2f}",
           f" 최대낙폭    : {_max_drawdown(pnls):.2f} USDT   연승 {mw} / 연패 {ml}",
           f" 명목가 합   : {sum(notl):,.0f}   (중앙 {sorted(notl)[n//2]:,.0f})",
           f" 추정 수수료 : -{fee:.2f}  (taker {taker_pct}%/편도 왕복)  →  수수료차감 순손익 {net-fee:+.2f}",
           ""]
    bydir = defaultdict(list); byreason = defaultdict(list)
    bysleeve = defaultdict(list); bysym = defaultdict(list)
    for r in rows:
        bydir[r.direction].append(r.pnl); byreason[r.reason].append(r.pnl)
        bysleeve[r.sleeve or "-"].append(r.pnl); bysym[r.symbol].append(r.pnl)
    out += _fmt_group("방향별", bydir)
    out += _fmt_group("청산사유별", byreason, 22)
    if len(bysleeve) > 1:
        out += _fmt_group("슬리브별", bysleeve)
    out.append(f"  ── 심볼별 (손익 하위/상위 {top}) ──")
    ranked = sorted(bysym.items(), key=lambda x: sum(x[1]))
    show = ranked[:top] + ([("...", [])] if len(ranked) > 2 * top else []) + ranked[-top:] \
        if len(ranked) > 2 * top else ranked
    for k, v in show:
        if k == "...":
            out.append("    ...")
            continue
        out.append(f"    {k[:14]:<14} {len(v):>3}건  {sum(v):>+9.2f}")

    out += ["", "💡 개선 권고", "─────────────"]
    for i, rec in enumerate(_recommend(rows, taker_pct), 1):
        out.append(f" {i}. {rec}")
    out += ["", "※ 참고용 분석이며 투자조언 아님. 표본이 쌓일수록 신뢰도가 올라갑니다."]
    return "\n".join(out)


def main() -> None:
    p = argparse.ArgumentParser(description="거래 저널 심층 분석 + 개선 권고")
    p.add_argument("--top", type=int, default=10, help="심볼별 표시 개수")
    p.add_argument("--csv", help="저널 대신 이 CSV 파일 분석(대시보드 다운로드 CSV)")
    args = p.parse_args()

    s = get_settings()
    rows = _rows_from_csv(args.csv) if args.csv else _rows_from_journal(s.state_dir)
    print(analyze(rows, s.taker_fee_pct, args.top))


if __name__ == "__main__":
    main()
