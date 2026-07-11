"""상태/성과 대시보드 렌더링 — 텍스트(CLI) + HTML."""
from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path

from ..utils.timez import KST, kst_display
from . import charts


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _epoch(iso: str | None) -> float | None:
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(iso)
    except (ValueError, TypeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


# ---------------------------------------------------------- 데이터 로딩(차트용)

def load_start_equity(state_dir: str) -> float | None:
    """state/portfolio.json 의 누적수익률 기준자본."""
    path = Path(state_dir) / "portfolio.json"
    if not path.exists():
        return None
    try:
        v = float(json.loads(path.read_text(encoding="utf-8")).get("starting_equity", 0.0))
        return v or None
    except (json.JSONDecodeError, ValueError, TypeError, OSError):
        return None


def journal_span_days(journal) -> int:
    """첫 청산~지금 까지의 일수(BTC 비교 구간 산정용). 최소 7, 최대 120."""
    closed = [t for t in journal.closed_trades() if t.closed_at]
    if not closed:
        return 7
    first = min(_epoch(t.closed_at) or 0.0 for t in closed)
    now = datetime.now(timezone.utc).timestamp()
    days = int((now - first) / 86_400) + 1
    return max(7, min(days, 120))


def btc_buyhold_series(days: int = 30) -> list[tuple[float, float]] | None:
    """최근 days 일 BTC 일봉 종가 → (epoch초, 시작대비 %) 시계열. 실패 시 None."""
    try:
        from ..connectors import BinanceDerivativesData
        kl = BinanceDerivativesData().klines("BTC/USDT", "1d", limit=min(days + 1, 200))
    except Exception:  # noqa: BLE001
        return None
    if not kl or not kl.get("close"):
        return None
    closes, times = kl["close"], kl["open_time"]
    c0 = closes[0]
    if c0 <= 0:
        return None
    return [(t / 1000.0, (c / c0 - 1.0) * 100.0) for t, c in zip(times, closes)]


def _return_series(journal, start_equity: float) -> tuple[list[tuple[float, float]], list[tuple[str, float]], float]:
    """(누적수익률% 점들, 일별손익 막대, 최종수익률%) 산출 — 청산 거래 기준."""
    closed = [t for t in journal.closed_trades()
              if t.closed_at and t.pnl is not None]
    closed.sort(key=lambda t: t.closed_at or "")
    pts: list[tuple[float, float]] = []
    daily: dict[str, float] = {}
    cum = 0.0
    base = start_equity if start_equity and start_equity > 0 else 10_000.0
    for t in closed:
        ep = _epoch(t.closed_at)
        if ep is None:
            continue
        cum += float(t.pnl)
        pts.append((ep, cum / base * 100.0))
        day = datetime.fromtimestamp(ep, KST).strftime("%m-%d")
        daily[day] = daily.get(day, 0.0) + float(t.pnl)
    bars = sorted(daily.items())
    final_pct = pts[-1][1] if pts else 0.0
    return pts, bars, final_pct


def _short_time(iso: str | None) -> str:
    """ISO8601 → 'MM-DD HH:MM' (KST 표시용)."""
    return kst_display(iso, "%m-%d %H:%M")


def render_text(journal, equity: float | None = None) -> str:
    st = journal.stats()
    now = _now_iso()
    lines = [
        "",
        "════════════ crypto-trader 상태 ════════════",
    ]
    if equity is not None:
        lines.append(f" 현재 자본        : {equity:,.2f} USDT")
    lines += [
        f" 총 실현손익      : {st['total_pnl']:+,.2f} USDT",
        f" 청산 거래 수     : {st['total_trades']}  (승 {st['wins']} / 패 {st['losses']})",
        f" 승률             : {st['win_rate']:.1f}%",
        f" 손익비(PF)       : {st['profit_factor']:.2f}",
        f" 평균 수익/손실   : {st['avg_win']:+.2f} / {-st['avg_loss']:+.2f}",
        f" 최고/최악        : {st['best']:+.2f} / {st['worst']:+.2f}",
        f" 평균 유지시간    : {st['avg_holding_human']}",
        f" 열린 포지션      : {st['open_trades']}",
        "─────────────────────────────────────────────",
    ]
    opens = journal.open_trades()
    if opens:
        lines.append(" [열린 포지션]")
        for t in opens:
            lines.append(f"   {t.symbol} {t.direction.upper()} @ {t.entry_price:.4f} "
                         f"SL {t.stop_price:.4f} TP {t.take_profit:.4f} "
                         f"| 오픈 {_short_time(t.opened_at)} 유지 {t.holding_human(now)} ({t.mode})")
    recent = journal.closed_trades()[-5:]
    if recent:
        lines.append(" [최근 청산 5건]")
        for t in recent:
            lines.append(f"   {t.symbol} {t.direction.upper()} "
                         f"{t.entry_price:.4f}→{t.exit_price:.4f} "
                         f"{t.pnl:+.2f} ({t.exit_reason}) "
                         f"| {_short_time(t.opened_at)}→{_short_time(t.closed_at)} 유지 {t.holding_human()}")
    lines.append("═════════════════════════════════════════════")
    return "\n".join(lines)


_EVENT_COLOR = {
    "PUMP": "#16a34a", "DUMP": "#dc2626", "VOL_SPIKE": "#f59e0b",
    "OI_SURGE": "#22c55e", "OI_DROP": "#ef4444", "FUNDING": "#a855f7",
}
_EVENT_EMOJI = {
    "PUMP": "🚀", "DUMP": "🔻", "VOL_SPIKE": "📊",
    "OI_SURGE": "🟢", "OI_DROP": "🔴", "FUNDING": "💰",
}
_EVENT_LABEL = {
    "PUMP": "급등", "DUMP": "급락", "VOL_SPIKE": "거래량급증",
    "OI_SURGE": "OI급증", "OI_DROP": "OI급감", "FUNDING": "펀딩극단",
}


def _event_rows(events: list) -> str:
    out = []
    for e in events:
        # e 는 ScanEvent 또는 dict 둘 다 허용
        etype = getattr(e, "type", None) or (e.get("type") if isinstance(e, dict) else "")
        symbol = getattr(e, "symbol", None) or (e.get("symbol") if isinstance(e, dict) else "")
        detail = getattr(e, "detail", None) or (e.get("detail") if isinstance(e, dict) else "")
        ts = getattr(e, "ts", None) or (e.get("ts") if isinstance(e, dict) else "")
        color = _EVENT_COLOR.get(etype, "#e2e8f0")
        label = f"{_EVENT_EMOJI.get(etype, '')} {_EVENT_LABEL.get(etype, etype)}"
        out.append(
            f"<tr><td>{_short_time(ts)}</td>"
            f"<td><b>{html.escape(str(symbol))}</b></td>"
            f"<td style='color:{color}'>{html.escape(label)}</td>"
            f"<td>{html.escape(str(detail))}</td></tr>"
        )
    return "\n".join(out)


def _strength_table(title: str, rows: list) -> str:
    body = []
    for i, r in enumerate(rows or []):
        rel = r.get("rel", 0.0)
        c = "#16a34a" if rel >= 0 else "#dc2626"
        sym = str(r.get("symbol", "")).replace("/USDT", "")
        body.append(
            f"<tr><td>{i + 1}</td><td><b>{html.escape(sym)}</b></td>"
            f"<td style='color:{c}'>{rel:+.2f}%</td>"
            f"<td class='muted'>{r.get('alt', 0.0):+.1f}%</td></tr>"
        )
    inner = "".join(body) or "<tr><td colspan=4 class='muted'>데이터 없음</td></tr>"
    return (f"<div class='card' style='flex:1;min-width:220px'>"
            f"<div class='muted' style='margin-bottom:6px'>{title}</div>"
            f"<table><thead><tr><th>#</th><th>심볼</th><th>BTC대비</th><th>수익률</th>"
            f"</tr></thead><tbody>{inner}</tbody></table></div>")


def render_html(journal: TradeJournal, equity: float | None = None,
                events: list | None = None, refresh_sec: int = 0,
                start_equity: float | None = None,
                btc_series: list | None = None,
                market_extra: dict | None = None) -> str:
    st = journal.stats()
    pnl_color = "#16a34a" if st["total_pnl"] >= 0 else "#dc2626"
    events = events or []
    refresh_tag = (f'<meta http-equiv="refresh" content="{refresh_sec}">'
                   if refresh_sec > 0 else "")
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")

    # --- 포트폴리오 차트 데이터 ---
    ret_pts, daily_bars, final_pct = _return_series(journal, start_equity or 0.0)
    port_color = "#38bdf8"
    line_series = [{"label": "포트폴리오 수익률", "color": port_color, "points": ret_pts}]
    if btc_series and len(btc_series) >= 2:
        line_series.append({"label": "BTC 매수후보유", "color": "#f7931a",
                            "points": [(x, y) for x, y in btc_series]})
    ret_color = "#16a34a" if final_pct >= 0 else "#dc2626"
    btc_final = btc_series[-1][1] if btc_series else None
    btc_cmp = (f" · BTC {btc_final:+.1f}%" if btc_final is not None else "")

    chart_section = f"""
  <h2>📈 포트폴리오 추이 (수익률 vs BTC 매수후보유)</h2>
  <div class="card">{charts.line_chart(line_series)}</div>
  <h2>📊 일별 손익 (USDT)</h2>
  <div class="card">{charts.bar_chart(daily_bars, unit="")}</div>
"""

    # --- 알트 상대강도 + 매크로 괴리 ---
    me = market_extra or {}
    alt = me.get("alt_strength") or {}
    macro = me.get("macro") or []
    strength_section = f"""
  <h2>💪 알트 BTC 대비 강도 TOP 10 (스테이블 제외)</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap">
    {_strength_table("1일", alt.get("1d", []))}
    {_strength_table("7일", alt.get("7d", []))}
    {_strength_table("30일", alt.get("30d", []))}
  </div>
""" if alt else ""
    macro_section = f"""
  <h2>🌐 BTC vs 나스닥·금 괴리 (시작=0%)</h2>
  <div class="card">{charts.line_chart(macro, y_suffix="%")}</div>
""" if macro else ""

    event_section = f"""
  <details class="events">
    <summary>🛰️ 시장 이벤트 (최근 {min(len(events), 40)}건) — 펼치기/접기</summary>
    <table><thead><tr><th>시각(KST)</th><th>심볼</th><th>유형</th><th>상세</th></tr></thead>
    <tbody>{_event_rows(events[:40]) or "<tr><td colspan=4>아직 감지된 이벤트 없음</td></tr>"}</tbody></table>
  </details>
"""

    def rows(trades: list, closed: bool) -> str:
        out = []
        for t in trades:
            if closed:
                pnl = t.pnl or 0.0
                c = "#16a34a" if pnl >= 0 else "#dc2626"
                out.append(
                    f"<tr><td>{html.escape(t.symbol)}</td>"
                    f"<td>{t.direction.upper()}</td>"
                    f"<td>{t.entry_price:.4f}</td>"
                    f"<td>{(t.exit_price or 0):.4f}</td>"
                    f"<td style='color:{c}'>{pnl:+.2f}</td>"
                    f"<td>{html.escape(t.exit_reason)}</td></tr>"
                )
            else:
                out.append(
                    f"<tr><td>{html.escape(t.symbol)}</td>"
                    f"<td>{t.direction.upper()}</td>"
                    f"<td>{t.entry_price:.4f}</td>"
                    f"<td>{t.stop_price:.4f}</td>"
                    f"<td>{t.take_profit:.4f}</td>"
                    f"<td>{html.escape(t.mode)}</td></tr>"
                )
        return "\n".join(out)

    equity_row = f"<div class='stat'><span>현재 자본</span><b>{equity:,.2f}</b></div>" if equity is not None else ""

    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{refresh_tag}
<title>crypto-trader 대시보드</title>
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; background:#0f172a; color:#e2e8f0; margin:0; padding:24px; }}
  h1 {{ font-size:20px; }} h2 {{ font-size:15px; color:#94a3b8; margin-top:28px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:16px 0; }}
  .stat {{ background:#1e293b; border-radius:10px; padding:14px; display:flex; flex-direction:column; gap:6px; }}
  .stat span {{ font-size:12px; color:#94a3b8; }} .stat b {{ font-size:20px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ text-align:left; padding:8px 10px; border-bottom:1px solid #334155; }}
  th {{ color:#94a3b8; font-weight:600; }}
  .card {{ background:#1e293b; border-radius:10px; padding:14px; margin:10px 0; overflow-x:auto; }}
  .muted {{ color:#64748b; font-size:12px; }}
  details.events {{ background:#1e293b; border-radius:10px; padding:8px 14px; margin-top:28px; }}
  details.events summary {{ cursor:pointer; color:#94a3b8; font-size:14px; padding:6px 0; }}
</style></head>
<body>
  <h1>🤖 crypto-trader 대시보드</h1>
  <div class="muted">생성 {now_kst}</div>
  <div class="grid">
    {equity_row}
    <div class="stat"><span>누적 수익률</span><b style="color:{ret_color}">{final_pct:+.2f}%</b><span class="muted">{btc_cmp}</span></div>
    <div class="stat"><span>총 실현손익 (USDT)</span><b style="color:{pnl_color}">{st['total_pnl']:+,.2f}</b></div>
    <div class="stat"><span>승률</span><b>{st['win_rate']:.1f}%</b></div>
    <div class="stat"><span>손익비 (PF)</span><b>{st['profit_factor']:.2f}</b></div>
    <div class="stat"><span>청산 거래</span><b>{st['total_trades']} <small style="font-size:12px;color:#94a3b8">(승 {st['wins']}/패 {st['losses']})</small></b></div>
    <div class="stat"><span>열린 포지션</span><b>{st['open_trades']}</b></div>
  </div>
  {chart_section}
  {strength_section}
  {macro_section}
  <h2>열린 포지션</h2>
  <table><thead><tr><th>심볼</th><th>방향</th><th>진입가</th><th>손절</th><th>익절</th><th>모드</th></tr></thead>
  <tbody>{rows(journal.open_trades(), False) or "<tr><td colspan=6>없음</td></tr>"}</tbody></table>
  <h2>최근 청산 (최대 20건)</h2>
  <table><thead><tr><th>심볼</th><th>방향</th><th>진입</th><th>청산</th><th>손익</th><th>사유</th></tr></thead>
  <tbody>{rows(journal.closed_trades()[-20:][::-1], True) or "<tr><td colspan=6>없음</td></tr>"}</tbody></table>
  {event_section}
</body></html>"""
