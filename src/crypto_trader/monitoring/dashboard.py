"""상태/성과 대시보드 렌더링 — 텍스트(CLI) + HTML."""
from __future__ import annotations

import csv
import html
import io
import json
from datetime import datetime, timezone
from pathlib import Path

from ..utils.timez import KST, kst_display
from . import charts


_RESEARCH = Path(__file__).resolve().parents[3] / "research"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_json(rel: str) -> dict | list | None:
    """repo research/ 아래 JSON 로드(없거나 깨지면 None)."""
    try:
        return json.loads((_RESEARCH / rel).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def load_kol_watch() -> dict:
    """KOL 토큰 데이터. watch.json 우선, 없으면 watch.csv 를 토큰별로 집계."""
    j = _load_json("kol/watch.json")
    if j and j.get("tokens"):
        return j
    try:
        text = (_RESEARCH / "kol" / "watch.csv").read_text(encoding="utf-8")
    except OSError:
        return {}
    agg: dict[str, dict] = {}
    for r in csv.DictReader(io.StringIO(text)):
        tok = (r.get("token") or r.get("토큰") or "").strip()
        if not tok:
            continue
        d = agg.setdefault(tok, {
            "token": tok,
            "chain": (r.get("chain") or r.get("체인") or "").strip(),
            "stage": (r.get("stage") or r.get("단계") or "").strip(),
            "kols": set(),
            "thesis": (r.get("thesis") or r.get("서사") or "").strip(),
            "risk": (r.get("risk") or r.get("리스크") or "").strip(),
        })
        kol = (r.get("KOL") or r.get("kol") or r.get("KOL수") or "").split("(")[0].strip()
        if kol:
            d["kols"].add(kol)
    tokens = []
    for t in agg.values():
        ks = list(t["kols"])
        t["kols"] = (", ".join(ks[:2]) + (f" 외{len(ks) - 2}" if len(ks) > 2 else "")) if ks else ""
        tokens.append(t)
    return {"tokens": tokens[:15]}


def load_market_brief() -> dict:
    return _load_json("market/brief.json") or {}


def load_chartist_views() -> dict:
    """상위 차티스트 5인의 현재 크립토 뷰. research/kol/chartist_views.json."""
    return _load_json("kol/chartist_views.json") or {}


def load_etf_flows() -> dict:
    """BTC·ETH·SOL·XRP 스팟 ETF 일별 순유입. research/etf/flows.json."""
    return _load_json("etf/flows.json") or {}


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
    return _portfolio_field(state_dir, "starting_equity")


def load_equity(state_dir: str) -> float | None:
    """엔진이 기록한 현재 실잔고(있으면). 대시보드 누적수익률 계산 기준."""
    return _portfolio_field(state_dir, "equity")


def load_equity_history(state_dir: str) -> list[list[float]]:
    """엔진이 기록한 (ts_sec, equity) 실잔고 이력. 없으면 빈 리스트."""
    path = Path(state_dir) / "portfolio.json"
    if not path.exists():
        return []
    try:
        h = json.loads(path.read_text(encoding="utf-8")).get("equity_history")
    except (json.JSONDecodeError, OSError):
        return []
    out: list[list[float]] = []
    for row in (h or []):
        try:
            out.append([float(row[0]), float(row[1])])
        except (TypeError, ValueError, IndexError):
            continue
    return out


def _portfolio_field(state_dir: str, key: str) -> float | None:
    path = Path(state_dir) / "portfolio.json"
    if not path.exists():
        return None
    try:
        v = float(json.loads(path.read_text(encoding="utf-8")).get(key, 0.0))
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
    # 시작점(0%)을 첫 거래 진입 시각에 심어, 청산 1건만 있어도 선이 그려지게.
    if pts:
        starts = [_epoch(t.opened_at) for t in closed if getattr(t, "opened_at", None)]
        starts = [s for s in starts if s is not None and s < pts[0][0]]
        base_ep = min(starts) if starts else pts[0][0] - 3600.0
        pts.insert(0, (base_ep, 0.0))
    bars = sorted(daily.items())
    final_pct = pts[-1][1] if pts else 0.0
    return pts, bars, final_pct


def _return_series_equity(history: list, start_equity: float):
    """실잔고 이력 기반 (누적수익률% 점, 일별손익 막대, 최종%). 이력 2점 미만이면 None.

    거래실현(저널) 대신 실제 잔고 변화로 그려 수수료·펀딩·슬리피지까지 반영한다.
    """
    if not history or len(history) < 2:
        return None
    base = start_equity if start_equity and start_equity > 0 else (history[0][1] or 10_000.0)
    if base <= 0:
        return None
    pts = [(float(ts), (float(eq) / base - 1.0) * 100.0) for ts, eq in history]
    # 일별손익: 각 날짜 마지막 잔고 − 전일 마지막 잔고(첫날은 기준자본 대비).
    last_by_day: dict[str, float] = {}
    order: list[str] = []
    for ts, eq in history:
        day = datetime.fromtimestamp(float(ts), KST).strftime("%m-%d")
        if day not in last_by_day:
            order.append(day)
        last_by_day[day] = float(eq)
    bars: list[tuple[str, float]] = []
    prev = base
    for day in order:
        bars.append((day, last_by_day[day] - prev))
        prev = last_by_day[day]
    return pts, bars, pts[-1][1]


def _trades_csv(journal) -> str:
    """전체 거래내역을 CSV 텍스트로. (대시보드 다운로드 버튼용)"""
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["opened_at", "closed_at", "symbol", "direction", "sleeve", "mode",
                "quantity", "entry_price", "exit_price", "notional_usdt",
                "pnl_usdt", "pnl_pct", "stop_price", "take_profit", "exit_reason", "order_id"])
    for t in getattr(journal, "trades", []):
        qty = t.quantity or 0.0
        entry = t.entry_price or 0.0
        notional = entry * qty
        pnl = t.pnl
        pnl_pct = (pnl / notional * 100.0) if (pnl is not None and notional) else ""
        w.writerow([
            getattr(t, "opened_at", "") or "", t.closed_at or "", t.symbol, t.direction,
            getattr(t, "sleeve", "") or "", getattr(t, "mode", "") or "",
            qty, entry, (t.exit_price if t.exit_price is not None else ""),
            round(notional, 4),
            (round(pnl, 6) if pnl is not None else ""),
            (round(pnl_pct, 4) if pnl_pct != "" else ""),
            getattr(t, "stop_price", "") or "", getattr(t, "take_profit", "") or "",
            getattr(t, "exit_reason", "") or "", getattr(t, "order_id", "") or "",
        ])
    return buf.getvalue()


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
    recent = sorted(journal.closed_trades(), key=lambda t: t.closed_at or "", reverse=True)[:5]
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
    "PUMP": "#16a34a", "DUMP": "#e23b4a", "VOL_SPIKE": "#f59e0b",
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
        c = "#16a34a" if rel >= 0 else "#e23b4a"
        sym = str(r.get("symbol", "")).replace("/USDT", "")
        body.append(
            f"<tr><td>{i + 1}</td>"
            f"<td><b class='symlink' data-sym='{html.escape(sym)}'>{html.escape(sym)}</b></td>"
            f"<td style='color:{c}'>{rel:+.2f}%</td>"
            f"<td class='muted'>{r.get('alt', 0.0):+.1f}%</td></tr>"
        )
    inner = "".join(body) or "<tr><td colspan=4 class='muted'>데이터 없음</td></tr>"
    return (f"<div class='card' style='min-width:0'>"
            f"<div class='muted' style='margin-bottom:6px'>{title}</div>"
            f"<table class='mtbl'><thead><tr><th>#</th><th>심볼</th><th>BTC대비</th><th>수익률</th>"
            f"</tr></thead><tbody>{inner}</tbody></table></div>")


def _mcap_table(rows: list) -> str:
    """시총 TOP10 코인의 1/7/30일 BTC 대비 수익률 — 한 테이블."""
    def cell(v) -> str:
        if v is None:
            return "<td class='muted'>-</td>"
        c = "#16a34a" if v >= 0 else "#e23b4a"
        return f"<td style='color:{c}'>{v:+.1f}%</td>"

    body = []
    for i, r in enumerate(rows or []):
        msym = html.escape(str(r.get("symbol", "")))
        body.append(
            f"<tr><td>{i + 1}</td>"
            f"<td><b class='symlink' data-sym='{msym}'>{msym}</b></td>"
            f"{cell(r.get('r1'))}{cell(r.get('r7'))}{cell(r.get('r30'))}</tr>"
        )
    inner = "".join(body) or "<tr><td colspan=5 class='muted'>데이터 없음</td></tr>"
    return (f"<div class='card' style='min-width:0'>"
            f"<div class='muted' style='margin-bottom:6px'>시총 TOP10 · BTC 대비 수익률</div>"
            f"<table class='mtbl'><thead><tr><th>#</th><th>심볼</th><th>1일</th><th>7일</th><th>30일</th>"
            f"</tr></thead><tbody>{inner}</tbody></table></div>")


def _watchlist_card() -> str:
    """관심종목(워치리스트) — 사용자가 최대 10개 지정. localStorage 저장·JS가 시세 채움.

    시세는 /api/quotes 배치 조회(가격·24h%). 심볼 클릭 시 해당 종목 차트 로드.
    """
    return (
        "<div class='card' style='min-width:0'>"
        "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>"
        "<span class='muted'>⭐ 관심종목 <span id='wl-count' style='font-size:11px'></span></span></div>"
        "<div style='display:flex;gap:5px;margin-bottom:8px'>"
        "<input class='futsearch' id='wl-input' placeholder='심볼 추가 (예: SOL)' "
        "autocomplete='off' style='flex:1'>"
        "<button class='tfbtn' id='wl-add' style='margin-left:0;white-space:nowrap'>추가</button></div>"
        "<div id='wl-list'></div></div>")


def _fmt_px(p) -> str:
    if not p:
        return "-"
    if p >= 1000:
        return f"${p:,.0f}"
    if p >= 1:
        return f"${p:,.2f}"
    return f"${p:.4f}"


def _pct_pts(closes: list, times: list) -> list:
    if len(closes) < 2 or not closes[0]:
        return []
    c0 = closes[0]
    if len(times) == len(closes):
        return [(times[k], (closes[k] / c0 - 1) * 100.0) for k in range(len(closes))]
    return [(k, (v / c0 - 1) * 100.0) for k, v in enumerate(closes)]


def _tickers_of(tickers) -> list:
    return tickers.get("top") if isinstance(tickers, dict) else (
        tickers if isinstance(tickers, list) else [])


def _ticker_strip(tickers) -> str:
    """상시 상단: 시총 상위 10 미니 티커(현재가·24h·스파크라인) — 시장 맥박.

    반응형 그리드로 전체 폭에 맞춰 정렬 — 가로 스크롤바 없이 넓은 화면에선 한 줄,
    좁아지면 폭에 맞춰 깔끔히 줄바꿈된다.
    """
    top = _tickers_of(tickers)
    if not top:
        return ""
    minis = []
    for t in top[:10]:
        pct = t.get("pct")
        c = "#16a34a" if (pct or 0) >= 0 else "#e23b4a"
        sym = html.escape(str(t.get("symbol", "")))
        spark = charts.sparkline((t.get("closes") or [])[-48:], width=150, height=36, color=c)
        pct_txt = f"{pct:+.1f}%" if pct is not None else "-"
        minis.append(
            f"<div class='card symlink' data-sym='{sym}' style='margin:0;padding:9px 11px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:baseline'>"
            f"<b style='font-size:14px'>{sym}</b><span style='color:{c};font-size:11px'>{pct_txt}</span></div>"
            f"<div class='muted' style='font-size:11px;margin-bottom:2px'>{_fmt_px(t.get('price'))}</div>"
            f"{spark}</div>")
    return (f"<div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));"
            f"gap:8px;margin:12px 0'>{''.join(minis)}</div>")


def _market_view(tickers) -> str:
    """시장 탭: 캔들+거래량 차트(좌) + 파생 요약(우), 하단 OI·CVD 차트 카드."""
    top = _tickers_of(tickers)
    if not top:
        return ""
    tfs = [("15분", "15m"), ("1시간", "1h"), ("4시간", "4h"),
           ("일봉", "1d"), ("주봉", "1w"), ("월봉", "1M")]
    tfbtns = "".join(f'<button class="tfbtn" data-tf="{v}">{lbl}</button>' for lbl, v in tfs)
    ptfs = [("5분", "5m"), ("1시간", "1h"), ("4시간", "4h"), ("1일", "1d")]
    oitfs = "".join(f'<button class="oitf" data-oitf="{v}">{lbl}</button>' for lbl, v in ptfs)
    cvdtfs = "".join(f'<button class="cvdtf" data-cvdtf="{v}">{lbl}</button>' for lbl, v in ptfs)
    d1 = str(top[0].get("symbol", "BTC"))
    chart = (
        f'<div class="card mkt-chartcard" style="flex:2;min-width:340px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'
        f'<span style="display:flex;align-items:baseline;gap:10px">'
        f'<button class="tkname" id="mkt-name"><span id="mkt-sym">{html.escape(d1)}</span> ▾</button>'
        f'<b id="mkt-price" style="font-size:16px">—</b></span>'
        f'<span>{tfbtns}</span></div>'
        f'<div id="mkt-ind" style="display:flex;gap:5px;flex-wrap:wrap;margin-top:6px">'
        f'<button class="tfbtn indbtn" data-ind="ma100">MA100</button>'
        f'<button class="tfbtn indbtn" data-ind="ma200">MA200</button>'
        f'<button class="tfbtn indbtn" data-ind="st">Supertrend</button>'
        f'<button class="tfbtn indbtn" data-ind="rsi">RSI</button>'
        f'<button class="tfbtn indbtn" data-ind="poc">POC</button>'
        f'<span class="muted" style="align-self:center;font-size:11px;margin-left:6px">채널</span>'
        f'<button class="tfbtn chanbtn" data-chan="none">없음</button>'
        f'<button class="tfbtn chanbtn" data-chan="keltner">켈트너</button>'
        f'<button class="tfbtn chanbtn" data-chan="donchian">돈치안</button></div>'
        f'<div id="mkt-search" style="display:none;margin:8px 0">'
        f'<input class="futsearch" id="mkt-input" placeholder="심볼 검색…">'
        f'<div class="tklist" id="mkt-list"></div></div>'
        f'<div id="mkt-chart" class="chartarea"><div class="muted">로딩…</div></div>'
        f'<div class="muted" style="text-align:right;font-size:10px;margin-top:2px">휠=확대/축소 · 드래그=좌우 이동 · 더블클릭=전체 · ↕모서리=높이 · 하단막대=거래량</div></div>')
    derivs = (
        f'<div class="card mkt-derivcard">'
        f'<div class="muted" style="margin-bottom:8px">파생 지표 · <b id="mkt-dsym">{html.escape(d1)}</b> '
        f'<span style="font-size:11px">(1h)</span></div>'
        f'<div id="mkt-derivs"><div class="muted">로딩…</div></div></div>')
    # 파생지표 하단: 기술적 종합 점수 3카드(공포·탐욕 / 기술적 분석 / 추세 분석)
    scores = (
        f'<div class="card">'
        f'<div class="muted" style="margin-bottom:8px">📊 기술적 종합 · <b id="sc-sym">{html.escape(d1)}</b> '
        f'<span style="font-size:11px" id="sc-tf">(4h)</span></div>'
        f'<div id="sc-body"><div class="muted">로딩…</div></div>'
        f'<div class="muted" style="font-size:10px;margin-top:6px">기술·추세는 좌측 차트 봉(tf) 기준 산출 · 참고용, 투자조언 아님</div></div>')
    rightcol = (f'<div style="flex:1;min-width:250px;display:flex;flex-direction:column;gap:14px">'
                f'{derivs}{scores}</div>')
    oicard = (
        f'<div class="card" style="flex:1;min-width:300px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">'
        f'<span class="muted">미결제약정 (OI) · <b id="oi-val">—</b></span>'
        f'<span>{oitfs}</span></div>'
        f'<div id="mkt-oi" class="minichart"><div class="muted">로딩…</div></div></div>')
    cvdcard = (
        f'<div class="card" style="flex:1;min-width:300px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">'
        f'<span class="muted">누적 CVD (테이커 매수−매도) · <b id="cvd-val">—</b></span>'
        f'<span>{cvdtfs}</span></div>'
        f'<div id="mkt-cvd" class="minichart"><div class="muted">로딩…</div></div></div>')
    domcard = (
        f'<div class="card" style="flex:1;min-width:300px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">'
        f'<span class="muted">BTC 도미넌스 (%) · <b id="dom-val">—</b></span>'
        f'<span class="muted" style="font-size:11px">일별 · 1년 백필</span></div>'
        f'<div id="mkt-dom" class="minichart"><div class="muted">로딩…</div></div></div>')
    cfg = ("<script>window.MKTCFG=" + json.dumps(
        {"syms": [str(t.get("symbol", "")) for t in top], "d1": d1}) + ";</script>")
    return (f'<div style="display:flex;flex-wrap:wrap;gap:14px;align-items:stretch">{chart}{rightcol}</div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:14px">{oicard}{cvdcard}{domcard}</div>'
            f'{cfg}{_CHART_JS}')


def _strategy_metrics(journal, start_equity: float | None) -> dict:
    """전략 유효성 지표: 샤프·소르티노·MDD·기대값·손익비 (청산거래 기준)."""
    import math
    closed = [t for t in journal.closed_trades() if t.pnl is not None]
    out = {"n": len(closed), "sharpe": 0.0, "sortino": 0.0, "mdd_pct": 0.0,
           "expectancy_pct": 0.0, "payoff": 0.0}
    if not closed:
        return out
    rets = [(t.pnl / (t.entry_price * t.quantity))
            if (t.entry_price and t.quantity) else 0.0 for t in closed]
    n = len(rets)
    mean = sum(rets) / n
    std = math.sqrt(sum((r - mean) ** 2 for r in rets) / n)
    downs = [r for r in rets if r < 0]
    dstd = math.sqrt(sum(r * r for r in downs) / n) if downs else 0.0
    out["sharpe"] = mean / std if std > 0 else 0.0
    out["sortino"] = mean / dstd if dstd > 0 else 0.0
    out["expectancy_pct"] = mean * 100.0
    wins = [t.pnl for t in closed if t.pnl > 0]
    losses = [-t.pnl for t in closed if t.pnl < 0]
    aw = sum(wins) / len(wins) if wins else 0.0
    al = sum(losses) / len(losses) if losses else 0.0
    out["payoff"] = aw / al if al > 0 else 0.0
    base = start_equity if start_equity and start_equity > 0 else 10_000.0
    cum = peak = mdd = 0.0
    for t in closed:
        cum += t.pnl
        peak = max(peak, cum)
        mdd = min(mdd, cum - peak)
    out["mdd_pct"] = mdd / base * 100.0
    return out


_CHART_JS = r"""<script>
(function(){
 var cfg=window.MKTCFG||{syms:[],d1:'BTC'};
 var SYMS=(cfg.syms||[]).slice();
 var SEL={s:cfg.d1,tf:'4h',oitf:'1h',cvdtf:'1h'};   // tf=캔들 간격(15m/1h/4h/1d/1w/1M)
 var TFSET={'15m':1,'1h':1,'4h':1,'1d':1,'1w':1,'1M':1};
 var IND={ma100:true,ma200:true,st:true,rsi:true,poc:true};   // 차트 기본 지표(모두 ON)
 try{var _pi=localStorage.getItem('ct_ind');if(_pi){var _po=JSON.parse(_pi);
   for(var _k in _po)if(_k in IND)IND[_k]=!!_po[_k];}}catch(_e){}
 var CHAN='none';   // 가격밴드 채널(배타 선택): none|keltner|donchian
 try{var _ch=localStorage.getItem('ct_chan');if(_ch)CHAN=_ch;}catch(_e){}
 function save(k,v){try{localStorage.setItem(k,v);}catch(_e){}}
 // 선택한 심볼·타임프레임 복원(새로고침 후에도 유지)
 try{var _s=localStorage.getItem('ct_sym');if(_s)SEL.s=_s;
   var _t=localStorage.getItem('ct_tf');if(_t)SEL.tf=_t;
   var _o=localStorage.getItem('ct_oitf');if(_o)SEL.oitf=_o;
   var _c=localStorage.getItem('ct_cvdtf');if(_c)SEL.cvdtf=_c;}catch(_e){}
 if(!TFSET[SEL.tf])SEL.tf='4h';   // 옛 기간기준(7d 등) 저장값 보정
 var LAST=null, OILAST=null, CVDLAST=null, DOMLAST=null;
 // 차트 줌/팬 뷰 윈도우. i0..i1 = 표시가능 전체구간(pAll)에서 화면에 그릴 인덱스 범위.
 // key(심볼|tf|길이)가 바뀌면(=종목·간격 전환) 최근 DEF_SHOWN봉으로 리셋한다.
 var VIEW={key:null,i0:0,i1:0}, DEF_SHOWN=200;
 var root=document.getElementById('mkt-chart');
 if(!root)return;
 var card=root.closest('.card');
 var oiEl=document.getElementById('mkt-oi'), cvdEl=document.getElementById('mkt-cvd'), domEl=document.getElementById('mkt-dom');
 // 사용자가 조절한 차트 높이 복원(새로고침 후에도 유지)
 try{var sh=parseInt(localStorage.getItem('ct_chart_h'),10);
   if(sh>0)root.style.height=Math.min(720,Math.max(140,sh))+'px';}catch(_e){}
 function setTxt(id,t){var e=document.getElementById(id);if(e)e.textContent=t;}
 function hlTf(){card.querySelectorAll('.tfbtn[data-tf]').forEach(function(b){
   b.classList.toggle('tfbtn-active', b.getAttribute('data-tf')===SEL.tf);});}
 function hlBtns(sel,attr,val){document.querySelectorAll(sel).forEach(function(b){
   b.classList.toggle('tfbtn-active', b.getAttribute(attr)===val);});}
 function fmtPx(v){if(v>=1000)return '$'+v.toLocaleString('en-US',{maximumFractionDigits:0});
   if(v>=1)return '$'+v.toFixed(2); if(v>=0.01)return '$'+v.toFixed(4); return '$'+v.toFixed(6);}
 function usd(v){if(v==null)return '-'; var a=Math.abs(v); if(a>=1e9)return '$'+(v/1e9).toFixed(2)+'B';
   if(a>=1e6)return '$'+(v/1e6).toFixed(1)+'M'; if(a>=1e3)return '$'+(v/1e3).toFixed(0)+'K'; return '$'+v.toFixed(0);}
 function num(v){if(v==null)return '-'; var s=v<0?'-':'+',a=Math.abs(v);
   if(a>=1e9)return s+(a/1e9).toFixed(2)+'B'; if(a>=1e6)return s+(a/1e6).toFixed(2)+'M';
   if(a>=1e3)return s+(a/1e3).toFixed(1)+'K'; return s+a.toFixed(0);}
 // ---- 지표 계산 헬퍼(전 배열에 대해, null=워밍업 부족) ----
 function smaArr(v,p){var o=new Array(v.length).fill(null),s=0;
   for(var i=0;i<v.length;i++){s+=v[i];if(i>=p)s-=v[i-p];if(i>=p-1)o[i]=s/p;}return o;}
 function rsiArr(cl,p){p=p||14;var o=new Array(cl.length).fill(null);if(cl.length<=p)return o;
   var ag=0,al=0,k,d;for(k=1;k<=p;k++){d=cl[k]-cl[k-1];if(d>=0)ag+=d;else al-=d;}
   ag/=p;al/=p;o[p]=al===0?100:100-100/(1+ag/al);
   for(k=p+1;k<cl.length;k++){d=cl[k]-cl[k-1];var g=d>0?d:0,l2=d<0?-d:0;
     ag=(ag*(p-1)+g)/p;al=(al*(p-1)+l2)/p;o[k]=al===0?100:100-100/(1+ag/al);}return o;}
 function superTrend(hi,lo,cl,p,m){p=p||10;m=m||3;var n=cl.length;
   var atr=new Array(n).fill(null),rma=0,tr,pc;
   for(var i=0;i<n;i++){pc=i>0?cl[i-1]:cl[i];
     tr=Math.max(hi[i]-lo[i],Math.abs(hi[i]-pc),Math.abs(lo[i]-pc));
     if(i<p){rma+=tr;if(i===p-1)atr[i]=rma/p;}else{rma=(atr[i-1]*(p-1)+tr);atr[i]=rma/p;}}
   var st=new Array(n).fill(null),dir=new Array(n).fill(1),fu=null,fl=null;
   for(var j=0;j<n;j++){if(atr[j]==null)continue;
     var hl2=(hi[j]+lo[j])/2,ub=hl2+m*atr[j],lb=hl2-m*atr[j];
     if(fu==null){fu=ub;fl=lb;dir[j]=cl[j]>=hl2?1:-1;st[j]=dir[j]===1?fl:fu;continue;}
     fu=(ub<fu||cl[j-1]>fu)?ub:fu; fl=(lb>fl||cl[j-1]<fl)?lb:fl;
     var pd=dir[j-1]||1,nd=pd;
     if(pd===1&&cl[j]<fl)nd=-1;else if(pd===-1&&cl[j]>fu)nd=1;
     dir[j]=nd;st[j]=nd===1?fl:fu;}
   return {st:st,dir:dir};}
 // Wilder ATR 배열(켈트너용)
 function atrArr(hi,lo,cl,p){p=p||10;var n=cl.length,atr=new Array(n).fill(null),rma=0,tr,pc;
   for(var i=0;i<n;i++){pc=i>0?cl[i-1]:cl[i];
     tr=Math.max(hi[i]-lo[i],Math.abs(hi[i]-pc),Math.abs(lo[i]-pc));
     if(i<p){rma+=tr;if(i===p-1)atr[i]=rma/p;}else{rma=(atr[i-1]*(p-1)+tr);atr[i]=rma/p;}}
   return atr;}
 // 켈트너 채널: EMA(ep) ± mult×ATR(ap)
 function keltner(hi,lo,cl,ep,ap,mult){ep=ep||20;ap=ap||10;mult=mult||2;
   var mid=emaA(cl,ep),atr=atrArr(hi,lo,cl,ap),n=cl.length,up=new Array(n).fill(null),lw=new Array(n).fill(null);
   for(var i=0;i<n;i++){if(mid[i]!=null&&atr[i]!=null){up[i]=mid[i]+mult*atr[i];lw[i]=mid[i]-mult*atr[i];}}
   return {up:up,mid:mid,lo:lw};}
 // 돈치안 채널: 최근 p봉 최고가/최저가, 중앙선=평균
 function donchian(hi,lo,p){p=p||20;var n=hi.length,up=new Array(n).fill(null),lw=new Array(n).fill(null),md=new Array(n).fill(null);
   for(var i=p-1;i<n;i++){var hh=-Infinity,ll=Infinity;
     for(var j=i-p+1;j<=i;j++){if(hi[j]>hh)hh=hi[j];if(lo[j]<ll)ll=lo[j];}
     up[i]=hh;lw[i]=ll;md[i]=(hh+ll)/2;}
   return {up:up,mid:md,lo:lw};}
 // 매물대(볼륨 프로파일): 표시구간을 가격대 bins로 나눠 각 봉 거래량을 고~저 범위에 분배.
 // POC=최대거래 가격대, VAH/VAL=누적 70% 밸류에어리어 상·하단.
 function volProfile(p,bins){bins=bins||48;
   var lo=Infinity,hi=-Infinity,i;
   for(i=0;i<p.length;i++){if(p[i][3]<lo)lo=p[i][3];if(p[i][2]>hi)hi=p[i][2];}
   if(!(hi>lo))return null;
   var bw=(hi-lo)/bins,vol=new Array(bins).fill(0);
   for(i=0;i<p.length;i++){var l=p[i][3],h=p[i][2],v=p[i][5]||0;
     var b0=Math.max(0,Math.min(bins-1,Math.floor((l-lo)/bw)));
     var b1=Math.max(0,Math.min(bins-1,Math.floor((h-lo)/bw)));
     var share=v/(b1-b0+1);for(var b=b0;b<=b1;b++)vol[b]+=share;}
   var pocB=0;for(b=1;b<bins;b++)if(vol[b]>vol[pocB])pocB=b;
   var total=vol.reduce(function(a,c){return a+c;},0);
   var loB=pocB,hiB=pocB,acc=vol[pocB],target=total*0.70;
   while(acc<target&&(loB>0||hiB<bins-1)){
     var up=hiB<bins-1?vol[hiB+1]:-1,dn=loB>0?vol[loB-1]:-1;
     if(up>=dn){hiB++;acc+=vol[hiB];}else{loB--;acc+=vol[loB];}}
   return {poc:lo+(pocB+0.5)*bw, vah:lo+(hiB+1)*bw, val:lo+loB*bw,
           vol:vol, lo:lo, bw:bw, bins:bins, vmax:Math.max.apply(null,vol)||1};}
 function poly(pts){if(!pts.length)return '';var s='';for(var i=0;i<pts.length;i++)s+=(i?'L':'M')+pts[i][0].toFixed(1)+','+pts[i][1].toFixed(1);return s;}
 // ---- 기술적 종합 점수용 추가 지표 ----
 function clamp(x,a,b){return x<a?a:(x>b?b:x);}
 function lastNN(a){for(var i=a.length-1;i>=0;i--)if(a[i]!=null)return a[i];return null;}
 function emaA(v,p){var o=new Array(v.length).fill(null),k=2/(p+1),e=null;
   for(var i=0;i<v.length;i++){if(v[i]==null){o[i]=null;continue;}e=(e==null?v[i]:v[i]*k+e*(1-k));o[i]=e;}return o;}
 function macdH(cl){var e12=emaA(cl,12),e26=emaA(cl,26),ml=new Array(cl.length).fill(null);
   for(var i=0;i<cl.length;i++)if(e12[i]!=null&&e26[i]!=null)ml[i]=e12[i]-e26[i];
   return {ml:ml,sg:emaA(ml.map(function(x){return x==null?0:x;}),9)};}
 function trixSig(cl,n){n=n||15;var e3=emaA(emaA(emaA(cl,n),n),n),tx=new Array(cl.length).fill(null);
   for(var i=1;i<cl.length;i++)if(e3[i]!=null&&e3[i-1]!=null&&e3[i-1]!==0)tx[i]=(e3[i]-e3[i-1])/e3[i-1];
   return {tx:tx,sg:emaA(tx.map(function(x){return x==null?0:x;}),9)};}
 function willR(hi,lo,cl,p){p=p||14;var o=new Array(cl.length).fill(null);
   for(var i=p-1;i<cl.length;i++){var hh=-1e18,ll=1e18;for(var j=i-p+1;j<=i;j++){if(hi[j]>hh)hh=hi[j];if(lo[j]<ll)ll=lo[j];}
     o[i]=hh===ll?-50:-100*(hh-cl[i])/(hh-ll);}return o;}
 function stochK(cl){var r=rsiArr(cl,14),p=14,st=new Array(cl.length).fill(null);
   for(var i=0;i<cl.length;i++){if(r[i]==null)continue;var lo=1e18,hi=-1e18,ok=true;
     for(var j=i-p+1;j<=i;j++){if(j<0||r[j]==null){ok=false;break;}if(r[j]<lo)lo=r[j];if(r[j]>hi)hi=r[j];}
     if(ok)st[i]=hi===lo?50:(r[i]-lo)/(hi-lo)*100;}
   var k=new Array(cl.length).fill(null);for(var m=2;m<cl.length;m++)if(st[m]!=null&&st[m-1]!=null&&st[m-2]!=null)k[m]=(st[m]+st[m-1]+st[m-2])/3;return k;}
 function bbA(cl,p,mult){p=p||20;mult=mult||2;var mid=smaArr(cl,p),up=new Array(cl.length).fill(null),lo=new Array(cl.length).fill(null);
   for(var i=p-1;i<cl.length;i++){var s=0;for(var j=i-p+1;j<=i;j++){var dd=cl[j]-mid[i];s+=dd*dd;}var sd=Math.sqrt(s/p);up[i]=mid[i]+mult*sd;lo[i]=mid[i]-mult*sd;}
   return {mid:mid,up:up,lo:lo};}
 function adxA(hi,lo,cl,p){p=p||14;var n=cl.length,tr=new Array(n).fill(0),pm=new Array(n).fill(0),nm=new Array(n).fill(0);
   for(var i=1;i<n;i++){var u=hi[i]-hi[i-1],d=lo[i-1]-lo[i];pm[i]=(u>d&&u>0)?u:0;nm[i]=(d>u&&d>0)?d:0;
     tr[i]=Math.max(hi[i]-lo[i],Math.abs(hi[i]-cl[i-1]),Math.abs(lo[i]-cl[i-1]));}
   function rma(a){var o=new Array(n).fill(null),s=0;for(var i=1;i<=p&&i<n;i++)s+=a[i];if(p<n)o[p]=s;for(var i=p+1;i<n;i++)o[i]=o[i-1]-o[i-1]/p+a[i];return o;}
   var tr2=rma(tr),pr=rma(pm),nr=rma(nm),pdi=new Array(n).fill(null),ndi=new Array(n).fill(null),dx=new Array(n).fill(null),adx=new Array(n).fill(null);
   for(var i=p;i<n;i++)if(tr2[i]){pdi[i]=100*pr[i]/tr2[i];ndi[i]=100*nr[i]/tr2[i];var sm=pdi[i]+ndi[i];dx[i]=sm?100*Math.abs(pdi[i]-ndi[i])/sm:0;}
   for(var i=2*p;i<n;i++){if(dx[i]==null)continue;if(adx[i-1]==null){var s2=0,c=0;for(var j=i-p+1;j<=i;j++)if(dx[j]!=null){s2+=dx[j];c++;}adx[i]=c?s2/c:null;}else adx[i]=(adx[i-1]*(p-1)+dx[i])/p;}
   return {adx:adx,pdi:pdi,ndi:ndi};}
 function scoreTech(full){if(full.length<40)return null;
   var cl=full.map(function(a){return a[4];}),hi=full.map(function(a){return a[2];}),lo=full.map(function(a){return a[3];}),vo=full.map(function(a){return a[5]||0;}),L=cl.length-1,vt=[];
   var rsi=lastNN(rsiArr(cl,14));if(rsi!=null)vt.push(clamp((rsi-50)/20,-1,1));
   var md=macdH(cl),ml=lastNN(md.ml),sg=lastNN(md.sg);if(ml!=null&&sg!=null)vt.push(ml>sg?0.6:-0.6);
   var tx=trixSig(cl,15),txv=lastNN(tx.tx),txs=lastNN(tx.sg);if(txv!=null&&txs!=null)vt.push((txv>txs?0.6:-0.6)+(txv>0?0.4:-0.4));
   var wr=lastNN(willR(hi,lo,cl,14));if(wr!=null)vt.push(clamp((wr+50)/30,-1,1));
   var sk=lastNN(stochK(cl));if(sk!=null)vt.push(clamp((sk-50)/30,-1,1));
   var va=0,cc=0;for(var i=Math.max(0,L-19);i<=L;i++){va+=vo[i];cc++;}va=cc?va/cc:0;
   if(va>0&&L>0)vt.push(clamp(vo[L]/va-1,-1,1)*0.5*(cl[L]>=cl[L-1]?1:-1));
   if(!vt.length)return null;var s=0;for(var i2=0;i2<vt.length;i2++)s+=clamp(vt[i2],-1,1);
   return 50+(s/vt.length)*50;}
 function scoreTrend(full){if(full.length<60)return null;
   var cl=full.map(function(a){return a[4];}),hi=full.map(function(a){return a[2];}),lo=full.map(function(a){return a[3];}),vo=full.map(function(a){return a[5]||0;}),L=cl.length-1,c=cl[L],vt=[];
   var st=superTrend(hi,lo,cl,10,3),sd=lastNN(st.dir);if(sd!=null)vt.push(sd>0?1:-1);
   var m50=lastNN(smaArr(cl,50)),m100=lastNN(smaArr(cl,100)),m200=lastNN(smaArr(cl,200)),al=0,cn=0;
   if(m50!=null){al+=c>m50?1:-1;cn++;}if(m100!=null){al+=c>m100?1:-1;cn++;}if(m200!=null){al+=c>m200?1:-1;cn++;}
   if(m100!=null&&m200!=null){al+=m100>m200?1:-1;cn++;}if(cn)vt.push(al/cn);
   var b=bbA(cl,20,2),mid=lastNN(b.mid),up=lastNN(b.up);if(mid!=null&&up!=null&&up>mid)vt.push(clamp((c-mid)/(up-mid),-1,1));
   var ax=adxA(hi,lo,cl,14),adL=lastNN(ax.adx),pL=lastNN(ax.pdi),nL=lastNN(ax.ndi);
   if(pL!=null&&nL!=null)vt.push((pL>nL?1:-1)*(adL!=null?clamp(adL/40,0.3,1):0.6));
   var r1=0,r2=0;for(var i=Math.max(0,L-9);i<=L;i++)r1+=vo[i];for(var i=Math.max(0,L-19);i<=L-10;i++)if(i>=0)r2+=vo[i];
   if(r2>0)vt.push(clamp(r1/r2-1,-0.5,0.5)*2*(c>=cl[Math.max(0,L-10)]?1:-1));
   if(!vt.length)return null;var s=0;for(var i3=0;i3<vt.length;i3++)s+=clamp(vt[i3],-1,1);
   return 50+(s/vt.length)*50*(adL!=null?clamp(adL/30,0.5,1):0.8);}
 // ---- 점수 카드 렌더 ----
 var FG=null;
 function scColor(v){return v>=75?'#16a34a':(v>=56?'#5fb85f':(v>=45?'#8d969e':(v>=25?'#e07a4a':'#e23b4a')));}
 function scLabel(v,kind){if(kind==='fg')return v>=75?'극단적 탐욕':(v>=56?'탐욕':(v>=45?'중립':(v>=25?'공포':'극단적 공포')));
   if(kind==='trend')return v>=75?'강한 상승':(v>=56?'상승':(v>=45?'중립':(v>=25?'하락':'강한 하락')));
   return v>=75?'강한 매수':(v>=56?'매수':(v>=45?'중립':(v>=25?'매도':'강한 매도')));}
 function gauge(title,val,kind,sub){
   if(val==null)return '<div style="margin-bottom:11px"><div style="display:flex;justify-content:space-between"><span class="dlab">'+title+'</span><b style="color:#8d969e">-</b></div></div>';
   var col=scColor(val),pct=clamp(val,0,100);
   return '<div style="margin-bottom:11px"><div style="display:flex;justify-content:space-between;align-items:baseline">'+
     '<span class="dlab">'+title+'</span><span><b style="color:'+col+';font-size:16px">'+Math.round(val)+'</b> '+
     '<span style="color:'+col+';font-size:11px">'+scLabel(val,kind)+'</span></span></div>'+
     '<div style="height:6px;background:rgba(255,255,255,0.08);border-radius:3px;margin-top:4px;position:relative">'+
     '<div style="position:absolute;left:0;top:0;height:6px;width:'+pct+'%;background:'+col+';border-radius:3px"></div></div>'+
     (sub?'<div class="dsub" style="margin-top:2px">'+sub+'</div>':'')+'</div>';}
 function renderScores(full){var el=document.getElementById('sc-body');if(!el)return;
   setTxt('sc-tf','('+SEL.tf+')');setTxt('sc-sym',SEL.s);
   var fgv=(FG&&FG.value!=null)?FG.value:null;
   var h=gauge('😱 공포·탐욕(시장)',fgv,'fg',FG&&FG.label?('alternative.me · '+FG.label):'크립토 시장 전체');
   h+=gauge('📈 기술적 분석',scoreTech(full),'sig','RSI·MACD·TRIX·W%R·StochRSI·거래량');
   h+=gauge('🧭 추세 분석',scoreTrend(full),'trend','Supertrend·MA50/100/200·BB·ADX·거래량');
   el.innerHTML=h;}
 function loadFearGreed(){fetch('/api/feargreed').then(function(r){return r.json();}).then(function(d){FG=d;
   if(LAST)renderScores((LAST&&LAST.points)||[]);}).catch(function(){});}
 // ---- 캔들 + MA/Supertrend 오버레이 + RSI 하단패널 + 거래량 ----
 function drawCandles(d){LAST=d;var full=(d&&d.points)||[];var warm=(d&&d.warmup)||0;
   if(full.length-warm<2){root.innerHTML='<div class="muted">데이터 없음</div>';return;}
   var fCl=full.map(function(a){return a[4];}),fHi=full.map(function(a){return a[2];}),fLo=full.map(function(a){return a[3];});
   var ma100=IND.ma100?smaArr(fCl,100):null, ma200=IND.ma200?smaArr(fCl,200):null;
   var rsi=IND.rsi?rsiArr(fCl,14):null, stObj=IND.st?superTrend(fHi,fLo,fCl,10,3):null;
   var chan=CHAN==='keltner'?keltner(fHi,fLo,fCl,20,10,2):(CHAN==='donchian'?donchian(fHi,fLo,20):null);
   var pAll=full.slice(warm);   // 표시가능 전체구간(줌아웃 최대)
   // 줌/팬 뷰 적용: key가 바뀌면(종목·간격 전환) 최근 DEF_SHOWN봉으로 리셋
   var vk=((d&&d.symbol)||SEL.s)+'|'+((d&&d.tf)||SEL.tf)+'|'+pAll.length;
   if(VIEW.key!==vk){VIEW.key=vk;VIEW.i1=pAll.length;VIEW.i0=Math.max(0,pAll.length-DEF_SHOWN);}
   VIEW.i0=Math.max(0,Math.min(pAll.length-3,VIEW.i0|0));
   VIEW.i1=Math.max(VIEW.i0+3,Math.min(pAll.length,VIEW.i1|0));
   warm=warm+VIEW.i0;            // full 인덱스 오프셋을 줌 시작점으로 이동(이하 warm+t 그대로 사용)
   var p=pAll.slice(VIEW.i0,VIEW.i1);   // 화면에 그릴 구간(줌/팬 적용)
   var vp=IND.poc?volProfile(p):null;   // 매물대(볼륨 프로파일) — 보이는 구간 기준
   var W=Math.max(320,root.clientWidth||680),H=Math.max(180,root.clientHeight||340);
   var padL=64,padR=12,padT=12,padB=26,gap=6;
   var avail=H-padT-padB;
   var volH=Math.max(24,Math.round(avail*0.16));
   var rsiH=IND.rsi?Math.max(30,Math.round(avail*0.20)):0;
   var priceBottom=padT+(avail-volH-rsiH-gap*(rsiH?2:1));
   var volTop=priceBottom+gap, volBottom=volTop+volH;      // 거래량(가격 아래)
   var rsiTop=volBottom+gap, rsiBottom=rsiTop+rsiH;         // RSI(거래량 아래, 최하단)
   var xs=p.map(function(a){return a[0];});
   var xmin=Math.min.apply(null,xs),xmax=Math.max.apply(null,xs);
   var lows=p.map(function(a){return a[3];}),highs=p.map(function(a){return a[2];});
   var ymin=Math.min.apply(null,lows),ymax=Math.max.apply(null,highs);
   // MA·Supertrend·채널 선이 잘리지 않게 y범위에 포함
   for(var t=0;t<p.length;t++){var fi=warm+t;
     [ma100&&ma100[fi],ma200&&ma200[fi],stObj&&stObj.st[fi],
      chan&&chan.up[fi],chan&&chan.lo[fi]].forEach(function(v){
       if(v!=null){if(v<ymin)ymin=v;if(v>ymax)ymax=v;}});}
   if(xmax===xmin)xmax+=1; if(ymax===ymin)ymax+=1; var yr=ymax-ymin;
   var vols=p.map(function(a){return a[5]||0;}),vmax=Math.max.apply(null,vols)||1;
   function sx(x){return padL+(x-xmin)/(xmax-xmin)*(W-padL-padR);}
   function sy(v){return priceBottom-(v-ymin)/yr*(priceBottom-padT);}
   var cw=Math.max(1.4,(W-padL-padR)/p.length*0.62);
   var o=['<svg viewBox="0 0 '+W+' '+H+'" width="100%" height="100%" style="display:block" preserveAspectRatio="none">'];
   for(var i=0;i<5;i++){var yv=ymin+yr*i/4,y=sy(yv);
     o.push('<line x1="'+padL+'" y1="'+y+'" x2="'+(W-padR)+'" y2="'+y+'" stroke="rgba(255,255,255,0.06)"/>');
     o.push('<text x="6" y="'+(y+4)+'" fill="#8d969e" font-size="11">'+fmtPx(yv)+'</text>');}
   // 가격밴드 채널(켈트너/돈치안) — 캔들 뒤 배경으로 밴드+옅은 채움
   if(chan){var upP=[],loP=[],mdP=[];
     for(var c=0;c<p.length;c++){var cfi=warm+c,cx=sx(xs[c]);
       if(chan.up[cfi]!=null)upP.push([cx,sy(chan.up[cfi])]);
       if(chan.lo[cfi]!=null)loP.push([cx,sy(chan.lo[cfi])]);
       if(chan.mid[cfi]!=null)mdP.push([cx,sy(chan.mid[cfi])]);}
     if(upP.length>1&&loP.length>1){
       o.push('<path d="'+poly(upP.concat(loP.slice().reverse()))+'Z" fill="#2dd4bf" opacity="0.06" stroke="none"/>');
       o.push('<path d="'+poly(upP)+'" fill="none" stroke="#2dd4bf" stroke-width="1.2" opacity="0.9"/>');
       o.push('<path d="'+poly(loP)+'" fill="none" stroke="#2dd4bf" stroke-width="1.2" opacity="0.9"/>');
       if(mdP.length>1)o.push('<path d="'+poly(mdP)+'" fill="none" stroke="#2dd4bf" stroke-width="1" opacity="0.5" stroke-dasharray="3 3"/>');
       o.push('<text x="'+(padL+2)+'" y="'+(padT+11)+'" fill="#2dd4bf" font-size="10">'+(CHAN==='keltner'?'Keltner(20,10,2)':'Donchian(20)')+'</text>');}}
   // 매물대 히스토그램(우측, 배경) — POC 막대는 금색 강조
   if(vp){var mW=(W-padL-padR)*0.14,xR=W-padR,binH=(priceBottom-padT)/vp.bins;
     for(var vb=0;vb<vp.bins;vb++){var bpx=vp.lo+(vb+0.5)*vp.bw,by=sy(bpx);
       var bwid=(vp.vol[vb]/vp.vmax)*mW;if(bwid<0.5)continue;
       var isPoc=Math.abs(bpx-vp.poc)<vp.bw*0.6;
       o.push('<rect x="'+(xR-bwid).toFixed(1)+'" y="'+(by-binH*0.45).toFixed(1)+'" width="'+bwid.toFixed(1)+'" height="'+Math.max(1,binH*0.9).toFixed(1)+'" fill="'+(isPoc?'#fbbf24':'#8d969e')+'" opacity="'+(isPoc?0.5:0.20)+'"/>');}}
   // Supertrend(방향별 색 세그먼트)
   if(stObj){var seg=[],pdir=null;
     for(var s2=0;s2<p.length;s2++){var v=stObj.st[warm+s2];if(v==null){if(seg.length>1)o.push('<path d="'+poly(seg)+'" fill="none" stroke="'+(pdir===1?'#16a34a':'#e23b4a')+'" stroke-width="1.5" opacity="0.9"/>');seg=[];pdir=null;continue;}
       var dr=stObj.dir[warm+s2];if(pdir!==null&&dr!==pdir){o.push('<path d="'+poly(seg)+'" fill="none" stroke="'+(pdir===1?'#16a34a':'#e23b4a')+'" stroke-width="1.5" opacity="0.9"/>');seg=[seg[seg.length-1]];}
       seg.push([sx(xs[s2]),sy(v)]);pdir=dr;}
     if(seg.length>1)o.push('<path d="'+poly(seg)+'" fill="none" stroke="'+(pdir===1?'#16a34a':'#e23b4a')+'" stroke-width="1.5" opacity="0.9"/>');}
   // 캔들 + 거래량
   for(var j=0;j<p.length;j++){var op=p[j][1],hi=p[j][2],lo=p[j][3],cl=p[j][4];
     var x=sx(xs[j]),up=cl>=op,col=up?'#16a34a':'#e23b4a';
     o.push('<line x1="'+x.toFixed(1)+'" y1="'+sy(hi).toFixed(1)+'" x2="'+x.toFixed(1)+'" y2="'+sy(lo).toFixed(1)+'" stroke="'+col+'" stroke-width="1"/>');
     var yo=sy(op),yc=sy(cl),tp=Math.min(yo,yc),bh=Math.max(1,Math.abs(yc-yo));
     o.push('<rect x="'+(x-cw/2).toFixed(1)+'" y="'+tp.toFixed(1)+'" width="'+cw.toFixed(1)+'" height="'+bh.toFixed(1)+'" fill="'+col+'"/>');
     var vHt=(vols[j]/vmax)*volH,vy=volBottom-vHt;
     o.push('<rect x="'+(x-cw/2).toFixed(1)+'" y="'+vy.toFixed(1)+'" width="'+cw.toFixed(1)+'" height="'+Math.max(0.5,vHt).toFixed(1)+'" fill="'+col+'" opacity="0.45"/>');}
   // 이동평균선
   function maPath(arr,color){if(!arr)return;var pts=[];for(var t2=0;t2<p.length;t2++){var vv=arr[warm+t2];if(vv!=null)pts.push([sx(xs[t2]),sy(vv)]);}
     if(pts.length>1)o.push('<path d="'+poly(pts)+'" fill="none" stroke="'+color+'" stroke-width="1.3" opacity="0.95"/>');}
   maPath(ma100,'#f7931a'); maPath(ma200,'#3b82f6');
   // 매물대 수평선: POC(실선) + VAH/VAL(점선), 금색
   if(vp){function hline(price,dash,lbl){var y=sy(price);
     o.push('<line x1="'+padL+'" y1="'+y.toFixed(1)+'" x2="'+(W-padR)+'" y2="'+y.toFixed(1)+'" stroke="#fbbf24" stroke-width="1" opacity="0.9"'+(dash?' stroke-dasharray="4 3"':'')+'/>');
     o.push('<text x="'+(padL+2)+'" y="'+(y-2).toFixed(1)+'" fill="#fbbf24" font-size="9">'+lbl+'</text>');}
     hline(vp.vah,true,'VAH'); hline(vp.val,true,'VAL'); hline(vp.poc,false,'POC');}
   // RSI 하단패널(거래량 아래) — 과매수(>70) 붉은띠 / 과매도(<30) 초록띠 강조
   if(rsiH){function ry(v){return rsiBottom-(v/100)*(rsiBottom-rsiTop);}var pw=(W-padL-padR);
     o.push('<rect x="'+padL+'" y="'+rsiTop.toFixed(1)+'" width="'+pw+'" height="'+rsiH.toFixed(1)+'" fill="rgba(255,255,255,0.02)"/>');
     o.push('<rect x="'+padL+'" y="'+ry(100).toFixed(1)+'" width="'+pw+'" height="'+(ry(70)-ry(100)).toFixed(1)+'" fill="#e23b4a" opacity="0.09"/>');
     o.push('<rect x="'+padL+'" y="'+ry(30).toFixed(1)+'" width="'+pw+'" height="'+(ry(0)-ry(30)).toFixed(1)+'" fill="#16a34a" opacity="0.09"/>');
     [30,50,70].forEach(function(lv){var y=ry(lv),ob=(lv!==50);
       o.push('<line x1="'+padL+'" y1="'+y.toFixed(1)+'" x2="'+(W-padR)+'" y2="'+y.toFixed(1)+'" stroke="'+(lv===70?'rgba(226,59,74,0.5)':(lv===30?'rgba(22,163,74,0.5)':'rgba(255,255,255,0.05)'))+'" stroke-dasharray="'+(ob?'3 3':'')+'"/>');
       o.push('<text x="'+(W-padR+2)+'" y="'+(y+3)+'" fill="#8d969e" font-size="9">'+lv+'</text>');});
     // RSI 선(구간별 색: >70 빨강, <30 초록, 그 외 보라)
     function zcol(v){return v>=70?'#e23b4a':(v<=30?'#16a34a':'#a855f7');}
     var rseg=[],pz=null;
     for(var t3=0;t3<p.length;t3++){var rv=rsi[warm+t3];
       if(rv==null){if(rseg.length>1)o.push('<path d="'+poly(rseg)+'" fill="none" stroke="'+pz+'" stroke-width="1.3"/>');rseg=[];pz=null;continue;}
       var zc=zcol(rv);if(pz!==null&&zc!==pz){o.push('<path d="'+poly(rseg)+'" fill="none" stroke="'+pz+'" stroke-width="1.3"/>');rseg=[rseg[rseg.length-1]];}
       rseg.push([sx(xs[t3]),ry(rv)]);pz=zc;}
     if(rseg.length>1)o.push('<path d="'+poly(rseg)+'" fill="none" stroke="'+pz+'" stroke-width="1.3"/>');
     // 과매수/과매도 강조 점
     for(var t4=0;t4<p.length;t4++){var rv2=rsi[warm+t4];if(rv2==null)continue;
       if(rv2>=70)o.push('<circle cx="'+sx(xs[t4]).toFixed(1)+'" cy="'+ry(rv2).toFixed(1)+'" r="1.7" fill="#e23b4a"/>');
       else if(rv2<=30)o.push('<circle cx="'+sx(xs[t4]).toFixed(1)+'" cy="'+ry(rv2).toFixed(1)+'" r="1.7" fill="#16a34a"/>');}
     o.push('<text x="'+(padL+2)+'" y="'+(rsiTop+11)+'" fill="#a855f7" font-size="10">RSI(14)</text>');}
   var tf=(d&&d.tf)||SEL.tf,intraday=(tf==='15m'||tf==='1h'||tf==='4h');
   for(var k=0;k<5;k++){var xv=xmin+(xmax-xmin)*k/4,dt=new Date(xv);
     var lab=dt.getFullYear()+'-'+('0'+(dt.getMonth()+1)).slice(-2)+'-'+('0'+dt.getDate()).slice(-2);
     if(intraday)lab+=' '+('0'+dt.getHours()).slice(-2)+':'+('0'+dt.getMinutes()).slice(-2);
     var an=k===0?'start':(k===4?'end':'middle');
     o.push('<text x="'+sx(xv).toFixed(1)+'" y="'+(H-6)+'" fill="#8d969e" font-size="'+(intraday?9:10)+'" text-anchor="'+an+'">'+lab+'</text>');}
   o.push('</svg>');root.innerHTML=o.join('');
   renderScores(full);   // 기술/추세 점수(좌측 차트 tf 기준) 갱신
   var pe=document.getElementById('mkt-price');if(pe && (pe.textContent==='—'||pe.textContent===''))pe.textContent=fmtPx(p[p.length-1][4]);}
 function loadChart(){hlTf();
   fetch('/api/klines?symbol='+encodeURIComponent(SEL.s)+'&tf='+SEL.tf)
   .then(function(r){return r.json();}).then(function(d){drawCandles(d);})
   .catch(function(){LAST=null;root.innerHTML='<div class="muted">차트는 serve_dashboard 서버 모드에서 표시됩니다.</div>';});}
 // ---- 범용 라인 차트(OI·CVD) ----
 function drawLine(el,pts,opts){opts=opts||{};
   if(!pts||pts.length<2){el.innerHTML='<div class="muted">데이터 없음</div>';return;}
   var W=Math.max(260,el.clientWidth||360),H=Math.max(120,el.clientHeight||170);
   var padL=58,padR=10,padT=10,padB=20;
   var xs=pts.map(function(a){return a[0];}),ys=pts.map(function(a){return a[1];});
   var xmin=Math.min.apply(null,xs),xmax=Math.max.apply(null,xs);
   var ymin=Math.min.apply(null,ys),ymax=Math.max.apply(null,ys);
   if(opts.zero){ymin=Math.min(ymin,0);ymax=Math.max(ymax,0);}
   if(xmax===xmin)xmax+=1; if(ymax===ymin)ymax+=1; var yr=ymax-ymin;
   function sx(x){return padL+(x-xmin)/(xmax-xmin)*(W-padL-padR);}
   function sy(v){return H-padB-(v-ymin)/yr*(H-padB-padT);}
   var fmt=opts.fmt||function(v){return v.toFixed(0);},col=opts.color||'#6c72ff';
   var o=['<svg viewBox="0 0 '+W+' '+H+'" width="100%" height="100%" style="display:block" preserveAspectRatio="none">'];
   for(var i=0;i<4;i++){var yv=ymin+yr*i/3,y=sy(yv);
     o.push('<line x1="'+padL+'" y1="'+y+'" x2="'+(W-padR)+'" y2="'+y+'" stroke="rgba(255,255,255,0.06)"/>');
     o.push('<text x="6" y="'+(y+4)+'" fill="#8d969e" font-size="10">'+fmt(yv)+'</text>');}
   if(opts.zero&&ymin<0&&ymax>0){var zy=sy(0);
     o.push('<line x1="'+padL+'" y1="'+zy.toFixed(1)+'" x2="'+(W-padR)+'" y2="'+zy.toFixed(1)+'" stroke="rgba(255,255,255,0.22)" stroke-dasharray="3 3"/>');}
   var dpath='';for(var j=0;j<pts.length;j++){dpath+=(j?'L':'M')+sx(xs[j]).toFixed(1)+','+sy(ys[j]).toFixed(1);}
   var baseV=opts.zero?Math.max(ymin,Math.min(ymax,0)):ymin,by=sy(baseV);
   o.push('<path d="'+dpath+'L'+sx(xs[xs.length-1]).toFixed(1)+','+by.toFixed(1)+'L'+sx(xs[0]).toFixed(1)+','+by.toFixed(1)+'Z" fill="'+col+'" opacity="0.10"/>');
   o.push('<path d="'+dpath+'" fill="none" stroke="'+col+'" stroke-width="1.6"/>');
   for(var k=0;k<4;k++){var xv=xmin+(xmax-xmin)*k/3,dt=new Date(xv);
     var lab=('0'+(dt.getMonth()+1)).slice(-2)+'-'+('0'+dt.getDate()).slice(-2)+' '+('0'+dt.getHours()).slice(-2)+'h';
     var an=k===0?'start':(k===3?'end':'middle');
     o.push('<text x="'+sx(xv).toFixed(1)+'" y="'+(H-5)+'" fill="#8d969e" font-size="9" text-anchor="'+an+'">'+lab+'</text>');}
   o.push('</svg>');el.innerHTML=o.join('');}
 // ---- 파생 요약(펀딩 행 + 포지셔닝 박스) ----
 function cell(lab,val,col,sub){return '<div class="dfcell"><span class="dlab">'+lab+'</span>'+
   '<b style="color:'+(col||'#e6e8ea')+'">'+val+'</b>'+(sub?'<span class="dsub">'+sub+'</span>':'')+'</div>';}
 function prow(lab,val,col,sub){return '<div class="prow"><span class="dlab">'+lab+'</span>'+
   '<span><b style="color:'+(col||'#e6e8ea')+'">'+val+'</b>'+(sub?' <span class="dsub">'+sub+'</span>':'')+'</span></div>';}
 function renderDerivs(d){var el=document.getElementById('mkt-derivs');
   if(!d){el.innerHTML='<div class="muted">파생 데이터는 serve_dashboard 서버 모드에서 표시됩니다.</div>';return;}
   var g='#16a34a',r='#e23b4a',n='#8d969e';
   if(d.price!=null){var pe=document.getElementById('mkt-price');if(pe)pe.textContent=fmtPx(d.price);}
   var fr=d.funding_rate,frp=(fr==null)?null:fr*100;
   var apr=(frp==null)?null:frp*3*365;
   var gl=d.global_ls_ratio,tt=d.top_trader_ls_ratio;
   var netLong=(gl==null)?null:gl/(1+gl)*100, ttNet=(tt==null)?null:tt/(1+tt)*100;
   var gap=(netLong==null||ttNet==null)?null:(ttNet-netLong);
   var frow='<div class="dfrow">'+
     cell('펀딩비', frp==null?'-':(frp>=0?'+':'')+frp.toFixed(4)+'%', frp==null?n:(frp>=0?g:r), frp==null?'':(frp>=0?'롱→숏':'숏→롱'))+
     cell('연환산(APR)', apr==null?'-':(apr>=0?'+':'')+apr.toFixed(1)+'%', apr==null?n:(apr>=0?g:r), '×3×365')+
     cell('24h 거래량', usd(d.vol24), d.chg24==null?n:(d.chg24>=0?g:r), d.chg24==null?'':((d.chg24>=0?'+':'')+d.chg24.toFixed(2)+'%'))+
     '</div>';
   var pbox='<div class="dbox"><div class="dboxh">포지셔닝 (1h)</div>'+
     prow('넷 롱 비중', netLong==null?'-':netLong.toFixed(1)+'%', netLong==null?n:(netLong>=50?g:r), '롱/숏 '+(gl==null?'-':gl.toFixed(2)))+
     prow('상위 트레이더 넷롱', ttNet==null?'-':ttNet.toFixed(1)+'%', ttNet==null?n:(ttNet>=50?g:r), 'L/S '+(tt==null?'-':tt.toFixed(2)))+
     prow('스마트머니 갭', gap==null?'-':(gap>=0?'+':'')+gap.toFixed(1)+'p', gap==null?n:(gap>=0?g:r), '상위−전체')+
     '</div>';
   el.innerHTML=frow+pbox;}
 function loadDerivs(){setTxt('mkt-dsym',SEL.s);
   document.getElementById('mkt-derivs').innerHTML='<div class="muted">로딩…</div>';
   fetch('/api/derivs?symbol='+encodeURIComponent(SEL.s))
   .then(function(r){return r.json();}).then(function(d){renderDerivs(d);})
   .catch(function(){renderDerivs(null);});}
 // ---- OI / CVD 차트 ----
 function loadOI(){hlBtns('.oitf','data-oitf',SEL.oitf);if(!oiEl)return;
   oiEl.innerHTML='<div class="muted">로딩…</div>';
   fetch('/api/oi_hist?symbol='+encodeURIComponent(SEL.s)+'&period='+SEL.oitf)
   .then(function(r){return r.json();}).then(function(d){var p=(d&&d.points)||[];OILAST=p;
     if(p.length<2){oiEl.innerHTML='<div class="muted">데이터 없음</div>';setTxt('oi-val','-');return;}
     var last=p[p.length-1][1],first=p[0][1],chg=first?((last-first)/first*100):0;
     setTxt('oi-val',usd(last)+' ('+(chg>=0?'+':'')+chg.toFixed(1)+'%)');
     drawLine(oiEl,p,{color:'#6c72ff',fmt:usd});})
   .catch(function(){OILAST=null;oiEl.innerHTML='<div class="muted">OI는 serve_dashboard 서버 모드에서 표시됩니다.</div>';setTxt('oi-val','-');});}
 function loadCVD(){hlBtns('.cvdtf','data-cvdtf',SEL.cvdtf);if(!cvdEl)return;
   cvdEl.innerHTML='<div class="muted">로딩…</div>';
   fetch('/api/cvd_hist?symbol='+encodeURIComponent(SEL.s)+'&period='+SEL.cvdtf)
   .then(function(r){return r.json();}).then(function(d){var p=(d&&d.points)||[];CVDLAST=p;
     if(p.length<2){cvdEl.innerHTML='<div class="muted">데이터 없음</div>';setTxt('cvd-val','-');return;}
     var last=p[p.length-1][1],col=last>=0?'#16a34a':'#e23b4a';
     setTxt('cvd-val',num(last));var ve=document.getElementById('cvd-val');if(ve)ve.style.color=col;
     drawLine(cvdEl,p,{color:col,fmt:num,zero:true});})
   .catch(function(){CVDLAST=null;cvdEl.innerHTML='<div class="muted">CVD는 serve_dashboard 서버 모드에서 표시됩니다.</div>';setTxt('cvd-val','-');});}
 function domFmt(v){return v.toFixed(2)+'%';}
 function loadDom(){if(!domEl)return;
   fetch('/api/btc_dominance')
   .then(function(r){return r.json();}).then(function(d){var p=(d&&d.points)||[];DOMLAST=p;
     setTxt('dom-val',(d&&d.current!=null)?d.current.toFixed(2)+'%':'-');
     if(p.length<2){domEl.innerHTML='<div class="muted">누적 수집 중 — 갱신될수록 채워집니다</div>';return;}
     drawLine(domEl,p,{color:'#e0964a',fmt:domFmt});})
   .catch(function(){DOMLAST=null;domEl.innerHTML='<div class="muted">BTC.D는 serve_dashboard 서버 모드에서 표시됩니다.</div>';setTxt('dom-val','-');});}
 // 리사이즈 재렌더 + 차트 높이 저장(캔들), OI·CVD 폭 변화 재렌더
 if(window.ResizeObserver){
   new ResizeObserver(function(){if(LAST)drawCandles(LAST);
     // 탭 전환으로 차트가 숨겨지면 clientHeight=0 → 이 0을 저장하면 다음 복원 때
     // sh>0 조건에 걸려 무시돼 높이가 리셋된다. 실제로 보이는 높이(≥140)만 저장.
     try{var _h=Math.round(root.clientHeight);if(_h>=140)localStorage.setItem('ct_chart_h',_h);}catch(_e){}}).observe(root);
   if(oiEl)new ResizeObserver(function(){if(OILAST&&OILAST.length>1)drawLine(oiEl,OILAST,{color:'#6c72ff',fmt:usd});}).observe(oiEl);
   if(cvdEl)new ResizeObserver(function(){if(CVDLAST&&CVDLAST.length>1){var lv=CVDLAST[CVDLAST.length-1][1];
     drawLine(cvdEl,CVDLAST,{color:lv>=0?'#16a34a':'#e23b4a',fmt:num,zero:true});}}).observe(cvdEl);
   if(domEl)new ResizeObserver(function(){if(DOMLAST&&DOMLAST.length>1)drawLine(domEl,DOMLAST,{color:'#e0964a',fmt:domFmt});}).observe(domEl);}
 // ---- 차트 줌(휠)·팬(드래그)·더블클릭 리셋 ----
 function viewN(){return LAST?(((LAST.points||[]).length)-((LAST.warmup)||0)):0;}  // 표시가능 전체 봉수
 root.addEventListener('wheel',function(e){
   if(!LAST)return;var n=viewN();if(n<8)return;e.preventDefault();
   var w=VIEW.i1-VIEW.i0;if(w<=0)w=Math.min(n,DEF_SHOWN);
   var rect=root.getBoundingClientRect();
   var frac=Math.max(0,Math.min(1,(e.clientX-rect.left)/(rect.width||1)));  // 커서 위치를 줌 기준점으로
   var f=e.deltaY<0?0.82:1.22;                    // 위로 스크롤=확대, 아래로=축소
   var nw=Math.max(12,Math.min(n,Math.round(w*f)));
   var anchor=VIEW.i0+frac*w;
   var ni0=Math.round(anchor-frac*nw);
   ni0=Math.max(0,Math.min(n-nw,ni0));
   VIEW.i0=ni0;VIEW.i1=ni0+nw;drawCandles(LAST);
 },{passive:false});
 var _drag=null;
 root.addEventListener('mousedown',function(e){
   if(!LAST)return;var rect=root.getBoundingClientRect();
   // 우하단 리사이즈 그립(약 18px)은 브라우저 기본 높이조절에 양보
   if(e.clientX>rect.right-18&&e.clientY>rect.bottom-18)return;
   _drag={x:e.clientX,i0:VIEW.i0,i1:VIEW.i1};root.style.cursor='grabbing';
 });
 window.addEventListener('mousemove',function(e){
   if(!_drag||!LAST)return;e.preventDefault();var n=viewN();var w=_drag.i1-_drag.i0;if(w<=0)return;
   var rect=root.getBoundingClientRect();
   var dxBars=Math.round((e.clientX-_drag.x)/(rect.width||1)*w);  // 오른쪽 드래그=과거로 이동
   var ni0=_drag.i0-dxBars;ni0=Math.max(0,Math.min(n-w,ni0));
   if(ni0!==VIEW.i0){VIEW.i0=ni0;VIEW.i1=ni0+w;drawCandles(LAST);}
 });
 window.addEventListener('mouseup',function(){if(_drag){_drag=null;root.style.cursor='';}});
 root.addEventListener('dblclick',function(){        // 더블클릭=전체 이력(줌 리셋)
   if(!LAST)return;var n=viewN();VIEW.i0=0;VIEW.i1=n;drawCandles(LAST);});
 // ---- 심볼 검색 ----
 function renderSyms(q){q=(q||'').toUpperCase();var box=document.getElementById('mkt-list');
   box.innerHTML=SYMS.filter(function(x){return x.toUpperCase().indexOf(q)>=0;}).slice(0,150)
   .map(function(x){return '<div class="tkopt" data-s="'+x+'">'+x+'</div>';}).join('');}
 function hlInd(){document.querySelectorAll('.indbtn').forEach(function(b){
   b.classList.toggle('tfbtn-active', !!IND[b.getAttribute('data-ind')]);});}
 function hlChan(){document.querySelectorAll('.chanbtn').forEach(function(b){
   b.classList.toggle('tfbtn-active', b.getAttribute('data-chan')===CHAN);});}
 // ---- 관심종목(워치리스트) — localStorage 저장, /api/quotes 배치 시세 ----
 var WL=[]; try{var _wl=localStorage.getItem('ct_wl');if(_wl)WL=(JSON.parse(_wl)||[]).slice(0,10);}catch(_e){}
 function wlSave(){try{localStorage.setItem('ct_wl',JSON.stringify(WL));}catch(_e){}}
 function wlRender(q){var box=document.getElementById('wl-list');if(!box)return;q=q||{};
   var cnt=document.getElementById('wl-count');if(cnt)cnt.textContent='('+WL.length+'/10)';
   if(!WL.length){box.innerHTML='<div class="muted" style="font-size:12px;padding:4px 0">심볼을 추가하세요 (최대 10개)</div>';return;}
   var h='<table style="width:100%"><tbody>';
   for(var i=0;i<WL.length;i++){var s=WL[i],d=q[s]||{};
     var pc=(d.chg24==null)?null:d.chg24,col=(pc==null)?'#8d969e':(pc>=0?'#16a34a':'#e23b4a');
     var pct=(pc==null)?'-':((pc>=0?'+':'')+pc.toFixed(2)+'%'),px=(d.price==null)?'-':fmtPx(d.price);
     h+='<tr class="wl-row" draggable="true" data-idx="'+i+'" style="cursor:move">'+
        '<td style="color:#8d969e;padding-right:2px" title="드래그로 순서변경">⠿</td>'+
        '<td><b class="wl-sym" data-s="'+s+'" style="cursor:pointer">'+s+'</b></td>'+
        '<td style="text-align:right">'+px+'</td>'+
        '<td style="text-align:right;color:'+col+'">'+pct+'</td>'+
        '<td style="text-align:right"><span class="wl-del" data-s="'+s+'" title="삭제" style="cursor:pointer;color:#8d969e;padding:0 3px">✕</span></td></tr>';}
   box.innerHTML=h+'</tbody></table>';}
 function wlLoad(){if(!WL.length){wlRender({});return;}
   fetch('/api/quotes?symbols='+encodeURIComponent(WL.join(',')))
   .then(function(r){return r.json();}).then(function(q){wlRender(q);}).catch(function(){wlRender({});});}
 function wlAdd(sym){sym=(sym||'').toUpperCase().replace(/[^A-Z0-9]/g,'');if(!sym)return;
   if(WL.indexOf(sym)>=0)return; if(WL.length>=10){alert('관심종목은 최대 10개까지입니다.');return;}
   WL.push(sym);wlSave();wlLoad();renderTopStrip();}
 function wlDel(sym){var i=WL.indexOf(sym);if(i>=0){WL.splice(i,1);wlSave();wlLoad();renderTopStrip();}}
 function wlSelect(s){if(!s)return;SEL.s=s;save('ct_sym',s);setTxt('mkt-sym',s);setTxt('mkt-price','—');
   loadChart();loadDerivs();loadOI();loadCVD();loadDom();
   if(root&&root.scrollIntoView)root.scrollIntoView({behavior:'smooth',block:'center'});}
 // 상단 티커 스트립을 관심종목으로 대체(지정 시). closes로 미니 스파크라인 직접 그림.
 function jspark(cl,col){cl=(cl||[]).filter(function(v){return v!=null;});if(cl.length<2)return '';
   var w=150,h=36,mn=Math.min.apply(null,cl),mx=Math.max.apply(null,cl);if(mx===mn)mx=mn+1;
   var n=cl.length,p='';for(var i=0;i<n;i++){p+=(i?' ':'')+(i/(n-1)*(w-2)+1).toFixed(1)+','+(h-2-(cl[i]-mn)/(mx-mn)*(h-4)).toFixed(1);}
   return '<svg viewBox="0 0 '+w+' '+h+'" width="100%" height="'+h+'" preserveAspectRatio="none"><polyline points="'+p+'" fill="none" stroke="'+col+'" stroke-width="1.5"/></svg>';}
 function renderTopStrip(){var strip=document.getElementById('ticker-strip');if(!strip)return;
   if(!WL.length)return;   // 관심종목 미지정 시 서버렌더(시총 상위) 유지
   fetch('/api/quotes?spark=1&symbols='+encodeURIComponent(WL.join(',')))
   .then(function(r){return r.json();}).then(function(q){var cards=[];
     for(var i=0;i<WL.length;i++){var s=WL[i],dd=q[s]||{};
       var pc=(dd.chg24==null)?null:dd.chg24,col=(pc==null)?'#8d969e':(pc>=0?'#16a34a':'#e23b4a');
       var pct=(pc==null)?'-':((pc>=0?'+':'')+pc.toFixed(1)+'%'),px=(dd.price==null)?'-':fmtPx(dd.price);
       cards.push('<div class="card symlink" data-sym="'+s+'" style="margin:0;padding:9px 11px">'+
         '<div style="display:flex;justify-content:space-between;align-items:baseline">'+
         '<b style="font-size:14px">'+s+'</b><span style="color:'+col+';font-size:11px">'+pct+'</span></div>'+
         '<div class="muted" style="font-size:11px;margin-bottom:2px">'+px+'</div>'+jspark(dd.closes,col)+'</div>');}
     strip.innerHTML='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin:12px 0">'+cards.join('')+'</div>';
   }).catch(function(){});}
 window.CT_WL=WL; window.CT_renderTopStrip=renderTopStrip;
 // 관심종목 순서 변경(드래그 앤 드롭) — 위임 핸들러
 var _wlDrag=null;
 document.addEventListener('dragstart',function(e){var tr=e.target.closest&&e.target.closest('tr.wl-row');
   if(!tr)return;_wlDrag=parseInt(tr.getAttribute('data-idx'),10);
   if(e.dataTransfer){e.dataTransfer.effectAllowed='move';try{e.dataTransfer.setData('text/plain',String(_wlDrag));}catch(_e){}}});
 document.addEventListener('dragover',function(e){var tr=e.target.closest&&e.target.closest('tr.wl-row');
   if(tr&&_wlDrag!=null){e.preventDefault();if(e.dataTransfer)e.dataTransfer.dropEffect='move';}});
 document.addEventListener('drop',function(e){var tr=e.target.closest&&e.target.closest('tr.wl-row');
   if(!tr||_wlDrag==null)return;e.preventDefault();var to=parseInt(tr.getAttribute('data-idx'),10);
   if(isNaN(to)||to===_wlDrag){_wlDrag=null;return;}
   var it=WL.splice(_wlDrag,1)[0];WL.splice(to,0,it);_wlDrag=null;wlSave();wlLoad();renderTopStrip();});
 document.addEventListener('dragend',function(){_wlDrag=null;});
 document.addEventListener('click',function(e){var t=e.target;if(!t.closest)return;
   var wd=t.closest('.wl-del');if(wd){wlDel(wd.getAttribute('data-s'));return;}
   var wsm=t.closest('.wl-sym');if(wsm){wlSelect(wsm.getAttribute('data-s'));return;}
   var wab=t.closest('#wl-add');if(wab){var wi=document.getElementById('wl-input');if(wi){wlAdd(wi.value);wi.value='';}return;}
   var ib=t.closest('.indbtn');if(ib){var ik=ib.getAttribute('data-ind');IND[ik]=!IND[ik];
     save('ct_ind',JSON.stringify(IND));hlInd();if(LAST)drawCandles(LAST);return;}
   var cb=t.closest('.chanbtn');if(cb){CHAN=cb.getAttribute('data-chan');
     save('ct_chan',CHAN);hlChan();if(LAST)drawCandles(LAST);return;}
   var tf=t.closest('.tfbtn');if(tf){SEL.tf=tf.getAttribute('data-tf');save('ct_tf',SEL.tf);loadChart();return;}
   var oi=t.closest('.oitf');if(oi){SEL.oitf=oi.getAttribute('data-oitf');save('ct_oitf',SEL.oitf);loadOI();return;}
   var cv=t.closest('.cvdtf');if(cv){SEL.cvdtf=cv.getAttribute('data-cvdtf');save('ct_cvdtf',SEL.cvdtf);loadCVD();return;}
   var nm=t.closest('#mkt-name');if(nm){var s=document.getElementById('mkt-search');
     s.style.display=s.style.display==='none'?'block':'none';if(s.style.display==='block')renderSyms('');return;}
   var op=t.closest('.tkopt');if(op){SEL.s=op.getAttribute('data-s');save('ct_sym',SEL.s);
     setTxt('mkt-sym',SEL.s);setTxt('mkt-price','—');
     document.getElementById('mkt-search').style.display='none';loadChart();loadDerivs();loadOI();loadCVD();loadDom();return;}
   // 강도·시총 표 / 상단 티커 카드 심볼 클릭 → 시장 탭으로 전환 + 해당 종목 차트 로드 + 스크롤
   var sl=t.closest('.symlink');if(sl){var sy2=(sl.getAttribute('data-sym')||'').toUpperCase();
     if(sy2){if(window.__showTab){window.__showTab('market');try{localStorage.setItem('ct_tab','market');}catch(_e2){}}
       SEL.s=sy2;save('ct_sym',SEL.s);setTxt('mkt-sym',SEL.s);setTxt('mkt-price','—');
       loadChart();loadDerivs();loadOI();loadCVD();loadDom();
       if(root&&root.scrollIntoView)root.scrollIntoView({behavior:'smooth',block:'center'});}return;}});
 document.addEventListener('input',function(e){var t=e.target;
   if(t.id==='mkt-input')renderSyms(t.value);});
 document.addEventListener('keydown',function(e){
   if(e.target&&e.target.id==='wl-input'&&e.key==='Enter'){wlAdd(e.target.value);e.target.value='';}});
 fetch('/api/symbols').then(function(r){return r.json();}).then(function(a){if(a&&a.length)SYMS=a;}).catch(function(){});
 setTxt('mkt-sym',SEL.s);   // 복원된 심볼 라벨 반영
 hlInd();hlChan();
 loadChart();loadDerivs();loadOI();loadCVD();loadDom();loadFearGreed();wlLoad();renderTopStrip();
 // 시장 탭이 보일 때 주기적으로 차트·파생 재조회(전체 리로드 없이 갱신)
 (function(){var SEC=window.CT_REFRESH||0;if(!SEC||SEC<5)return;
   setInterval(function(){var mp=document.querySelector('.tabpane[data-pane="market"]');
     if(mp&&mp.style.display==='none')return;   // 안 보이는 탭이면 스킵
     loadChart();loadDerivs();loadOI();loadCVD();loadDom();wlLoad();},SEC*1000);})();
})();
</script>"""


# 매크로(BTC vs 증시·원자재) 기간 선택 표시명
_MACRO_PERIOD_LABELS = [("1일", "1d"), ("1주일", "1w"), ("한달", "1mo"), ("3개월", "3mo"),
                        ("6개월", "6mo"), ("1년", "1y"), ("3년", "3y"), ("5년", "5y"),
                        ("10년", "10y")]


def _macro_view(macro) -> str:
    """BTC vs 증시·원자재 매크로 섹션 — 좌: 정규화 괴리(기간선택), 우: 증시·원자재 카드.

    기간 버튼/카드는 serve_dashboard /api/macro 로 라이브 갱신(서버 모드).
    정적 렌더에선 캐시된 괴리(macro)를 초기 표시.
    """
    btns = "".join(f'<button class="tfbtn mptf" data-mp="{v}">{lbl}</button>'
                   for lbl, v in _MACRO_PERIOD_LABELS)
    init = charts.line_chart(macro, y_suffix="%") if macro else '<div class="muted">로딩…</div>'
    return (
        '<h2>🌐 BTC vs 증시·원자재 '
        '<span class="muted" style="font-size:12px">· 시작=0% 정규화</span></h2>'
        '<div style="display:flex;flex-wrap:wrap;gap:14px;align-items:stretch">'
        '<div class="card" style="flex:2;min-width:340px;display:flex;flex-direction:column">'
        '<div style="display:flex;justify-content:space-between;align-items:center;'
        'flex-wrap:wrap;gap:8px">'
        '<span class="muted">BTC vs 나스닥·금 괴리</span>'
        f'<span id="macro-tf">{btns}</span></div>'
        f'<div id="macro-div" style="margin-top:8px;min-height:300px">{init}</div></div>'
        '<div class="card" style="flex:1;min-width:280px">'
        '<div class="muted" style="margin-bottom:8px">주요 증시 · 원자재 '
        '<span id="macro-cards-lbl" style="font-size:11px">(6개월)</span></div>'
        '<div id="macro-cards" style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px">'
        '<div class="muted">서버 모드에서 표시됩니다.</div></div></div>'
        '</div>' + _MACRO_JS)


_MACRO_JS = r"""<script>
(function(){
 var W=720,H=300,PAD=44,BPAD=60;
 var PLBL={'1d':'1일','1w':'1주일','1mo':'한달','3mo':'3개월','6mo':'6개월',
   '1y':'1년','3y':'3년','5y':'5년','10y':'10년'};
 var period='6mo';
 try{var s=localStorage.getItem('ct_macro_tf');if(s&&PLBL[s])period=s;}catch(_e){}
 var box=document.getElementById('macro-div');
 if(!box)return;
 function esc(s){return String(s).replace(/[&<>]/g,function(c){
   return c==='&'?'&amp;':c==='<'?'&lt;':'&gt;';});}
 function pad2(n){return (n<10?'0':'')+n;}
 function dlab(ts,span){var d=new Date(ts*1000);
   var Y=d.getFullYear(),M=pad2(d.getMonth()+1),D=pad2(d.getDate());
   if(span<=3*86400)return M+'-'+D+' '+pad2(d.getHours())+':'+pad2(d.getMinutes());
   if(span<=95*86400)return M+'-'+D;
   if(span<=800*86400)return (Y%100)+'-'+M;
   return ''+Y;}
 function hlTf(){document.querySelectorAll('.mptf').forEach(function(b){
   b.classList.toggle('tfbtn-active', b.getAttribute('data-mp')===period);});}
 // 다중 시계열 정규화 라인 (charts.line_chart 의 JS판)
 function drawDiv(series){
   var pts=[];series.forEach(function(s){(s.points||[]).forEach(function(p){pts.push(p);});});
   if(pts.length<2){box.innerHTML='<div class="muted">데이터 없음</div>';return;}
   var xs=pts.map(function(p){return p[0];}),ys=pts.map(function(p){return p[1];});
   var xmin=Math.min.apply(null,xs),xmax=Math.max.apply(null,xs);
   var ymin=Math.min.apply(null,ys.concat([0])),ymax=Math.max.apply(null,ys.concat([0]));
   if(xmax===xmin)xmax=xmin+1; if(ymax===ymin)ymax=ymin+1;
   var yr=ymax-ymin,span=xmax-xmin;
   function sx(x){return PAD+(x-xmin)/(xmax-xmin)*(W-2*PAD);}
   function sy(y){return H-BPAD-(y-ymin)/yr*(H-BPAD-PAD);}
   var o=['<svg viewBox="0 0 '+W+' '+H+'" width="100%" style="max-width:'+W+'px" xmlns="http://www.w3.org/2000/svg">'];
   for(var i=0;i<5;i++){var yv=ymin+yr*i/4,y=sy(yv);
     o.push('<line x1="'+PAD+'" y1="'+y.toFixed(1)+'" x2="'+(W-PAD)+'" y2="'+y.toFixed(1)+'" stroke="#232838" stroke-width="1"/>');
     o.push('<text x="6" y="'+(y+4).toFixed(1)+'" fill="#8b93a7" font-size="11">'+(yv>=0?'+':'')+yv.toFixed(1)+'%</text>');}
   if(ymin<0&&ymax>0){var y0=sy(0);
     o.push('<line x1="'+PAD+'" y1="'+y0.toFixed(1)+'" x2="'+(W-PAD)+'" y2="'+y0.toFixed(1)+'" stroke="#3a4a56" stroke-width="1.3" stroke-dasharray="3 3"/>');}
   series.forEach(function(s){var p=s.points||[];if(p.length<2)return;
     // 장 마감/주말 공백(정상 간격의 3.5배 초과)은 직선으로 잇지 않고 세션별로 끊는다.
     var ds=[];for(var j=1;j<p.length;j++)ds.push(p[j][0]-p[j-1][0]);
     ds.sort(function(a,b){return a-b;});
     var md=ds.length?ds[Math.floor(ds.length/2)]:0;
     // 장중(분봉, 표본간격<6h) 구간만 야간·주말 공백을 끊는다. 일봉+는 주말을
     // 잇는 게 표준이라 끊지 않음(md>=6h면 gap=무한 → 항상 연결).
     var gap=(md>0&&md<21600)?md*3.5:Infinity;
     var seg=[];
     function flush(){if(seg.length>1)o.push('<polyline points="'+seg.join(' ')+
       '" fill="none" stroke="'+s.color+'" stroke-width="2"/>');seg=[];}
     for(var i=0;i<p.length;i++){
       if(i>0&&(p[i][0]-p[i-1][0])>gap)flush();
       seg.push(sx(p[i][0]).toFixed(1)+','+sy(p[i][1]).toFixed(1));}
     flush();});
   for(var k=0;k<5;k++){var xv=xmin+span*k/4,a=k===0?'start':(k===4?'end':'middle');
     o.push('<text x="'+sx(xv).toFixed(1)+'" y="'+(H-6)+'" fill="#8b93a7" font-size="10" text-anchor="'+a+'">'+dlab(xv,span)+'</text>');}
   var lx=PAD+6;series.forEach(function(s){
     o.push('<rect x="'+lx+'" y="8" width="10" height="10" fill="'+s.color+'"/>');
     o.push('<text x="'+(lx+15)+'" y="17" fill="#c7cede" font-size="12">'+esc(s.label)+'</text>');
     lx+=15+esc(s.label).length*11+22;});
   o.push('</svg>');box.innerHTML=o.join('');
 }
 function spark(pts,col){
   var ys=pts.map(function(p){return p[1];});if(ys.length<2)return '';
   var mn=Math.min.apply(null,ys),mx=Math.max.apply(null,ys);if(mx===mn)mx=mn+1;
   var w=150,h=40,n=ys.length;
   var d=ys.map(function(v,i){return (i/(n-1)*w).toFixed(1)+','+(h-2-(v-mn)/(mx-mn)*(h-4)).toFixed(1);}).join(' ');
   return '<svg viewBox="0 0 '+w+' '+h+'" width="100%" style="max-width:'+w+'px" xmlns="http://www.w3.org/2000/svg">'+
     '<polyline points="'+d+'" fill="none" stroke="'+col+'" stroke-width="1.6"/></svg>';
 }
 function fmtP(v){if(v==null)return '-';var a=Math.abs(v);
   if(a>=1000)return v.toLocaleString('en-US',{maximumFractionDigits:0});
   return v.toLocaleString('en-US',{maximumFractionDigits:2});}
 function drawCards(cards){
   var el=document.getElementById('macro-cards');if(!el)return;
   if(!cards||!cards.length){el.innerHTML='<div class="muted">데이터 없음</div>';return;}
   el.innerHTML=cards.map(function(c){
     var pc=c.pct==null?0:c.pct,col=pc>=0?'#16a34a':'#e23b4a';
     return '<div style="border:1px solid #232838;border-radius:8px;padding:8px">'+
       '<div style="display:flex;justify-content:space-between;align-items:baseline">'+
       '<b style="font-size:12px">'+esc(c.label)+'</b>'+
       '<span style="color:'+col+';font-size:12px">'+(pc>=0?'+':'')+pc.toFixed(2)+'%</span></div>'+
       '<div class="muted" style="font-size:11px;margin:2px 0">'+fmtP(c.price)+'</div>'+
       spark(c.points,c.color)+'</div>';}).join('');
 }
 function load(){
   hlTf();
   var lbl=document.getElementById('macro-cards-lbl');if(lbl)lbl.textContent='('+(PLBL[period]||period)+')';
   fetch('/api/macro?period='+period).then(function(r){return r.json();}).then(function(d){
     if(d&&d.divergence&&d.divergence.length)drawDiv(d.divergence);
     drawCards(d&&d.cards);
   }).catch(function(){
     var el=document.getElementById('macro-cards');
     if(el)el.innerHTML='<div class="muted">증시·원자재 카드는 serve_dashboard 서버 모드에서 표시됩니다.</div>';
   });
 }
 document.addEventListener('click',function(e){var t=e.target;if(!t.closest)return;
   var b=t.closest('.mptf');if(!b)return;
   period=b.getAttribute('data-mp');try{localStorage.setItem('ct_macro_tf',period);}catch(_e){}
   load();});
 load();
})();
</script>"""


_STAGE_COLOR = {"조기": "#22c55e", "확산": "#eab308", "뒷북": "#94a3b8"}


def _kol_section(kol: dict) -> str:
    """KOL 하이프 토큰 + 주목 프로젝트/토큰(통합). 둘 다 kol/watch.json 에서 로드."""
    kol = kol or {}
    tokens = kol.get("tokens") or []
    notable = kol.get("notable") or []
    if not tokens and not notable:
        return ""
    ts = kst_display(kol.get("ts"), "%m-%d %H:%M")

    hype_html = ""
    if tokens:
        body = []
        for t in tokens[:15]:
            stage = str(t.get("stage", ""))
            sc = next((c for k, c in _STAGE_COLOR.items() if k in stage), "#e2e8f0")
            ca = str(t.get("ca") or t.get("contract") or t.get("address") or "").strip()
            if ca:
                short = ca if len(ca) <= 13 else f"{ca[:6]}…{ca[-4:]}"
                ca_html = (f"<a href='https://dexscreener.com/search?q={html.escape(ca)}' "
                           f"target='_blank' rel='noopener' title='{html.escape(ca)}' "
                           f"style='color:var(--accent);font-family:monospace;font-size:11px'>{html.escape(short)}</a>")
            else:
                ca_html = "<span class='muted'>-</span>"
            body.append(
                f"<tr><td><b>{html.escape(str(t.get('token', '')))}</b></td>"
                f"<td class='muted'>{html.escape(str(t.get('chain', '')))}</td>"
                f"<td>{ca_html}</td>"
                f"<td style='color:{sc}'>{html.escape(stage)}</td>"
                f"<td>{html.escape(str(t.get('kols', '')))}</td>"
                f"<td>{html.escape(str(t.get('thesis', ''))[:70])}</td>"
                f"<td class='muted'>{html.escape(str(t.get('risk', ''))[:40])}</td></tr>"
            )
        hype_html = f"""
  <h2>🐦 KOL 하이프 토큰 <span class="muted">({ts} KST)</span></h2>
  <div class="card" style="overflow-x:auto"><table>
  <thead><tr><th>토큰</th><th>체인</th><th>CA</th><th>단계</th><th>KOL</th><th>서사</th><th>리스크</th></tr></thead>
  <tbody>{"".join(body)}</tbody></table>
  <div class="muted" style="margin-top:8px">⚠️ 아이디어·조기경보용, 투자조언 아님. 자체 검증 필수.</div></div>
"""

    notable_html = ""
    if notable:
        nrows = "".join(
            f"<tr><td><b>{html.escape(str(n.get('token', '')))}</b></td>"
            f"<td class='muted'>{html.escape(str(n.get('status', '')))}</td>"
            f"<td>{html.escape(str(n.get('summary', ''))[:140])}</td></tr>"
            for n in notable[:12]
        )
        notable_html = f"""
  <h2>📌 주목 프로젝트/토큰 <span class="muted">({ts} KST)</span></h2>
  <div class="card" style="overflow-x:auto"><table>
  <thead><tr><th>토큰</th><th>상태</th><th>요약</th></tr></thead>
  <tbody>{nrows}</tbody></table></div>
"""
    return hype_html + notable_html


def _brief_section(brief: dict) -> str:
    if not brief:
        return ""
    ts = kst_display(brief.get("ts"), "%m-%d %H:%M")
    market = brief.get("market", "")
    cards = []
    for a in brief.get("assets", [])[:6]:
        bias = str(a.get("bias", ""))
        bc = "#16a34a" if "롱" in bias or "상승" in bias or "bull" in bias.lower() else (
            "#e23b4a" if "숏" in bias or "하락" in bias or "bear" in bias.lower() else "#94a3b8")
        cards.append(
            f"<div class='card' style='flex:1;min-width:240px'>"
            f"<b>{html.escape(str(a.get('symbol', '')))}</b> "
            f"<span style='color:{bc}'>{html.escape(bias)}</span>"
            f"<div style='font-size:13px;margin-top:6px'>{html.escape(str(a.get('summary', ''))[:1500])}</div>"
            f"<div class='muted' style='margin-top:6px'>레벨: {html.escape(str(a.get('levels', '')))}</div>"
            f"<div class='muted'>촉매: {html.escape(str(a.get('catalysts', ''))[:500])}</div></div>"
        )
    # 주목 프로젝트/토큰은 KOL 워치(_kol_section)로 통합 이관 — 여기선 렌더하지 않음.
    market_html = (f"<div class='card'>{html.escape(str(market)[:3000])}</div>"
                   if market else "")
    return f"""
  <h2>📰 시장 분석 요약 <span class="muted">({ts} KST)</span></h2>
  {market_html}
  <div style="display:flex;gap:12px;flex-wrap:wrap">{"".join(cards)}</div>
"""


def _bias_color(bias: str) -> str:
    b = str(bias or "")
    if any(k in b for k in ("상승", "롱", "bull")) or "bull" in b.lower():
        return "#16a34a"
    if any(k in b for k in ("하락", "숏", "bear")) or "bear" in b.lower():
        return "#e23b4a"
    if "경계" in b or "주의" in b:
        return "#eab308"
    return "#94a3b8"


def _chartists_section(data: dict) -> str:
    """상위 차티스트 5인의 현재 크립토 뷰 카드."""
    rows = (data or {}).get("chartists") or []
    if not rows:
        return ""
    ts = kst_display((data or {}).get("ts"), "%m-%d %H:%M")
    cards = []
    for c in rows[:8]:
        bias = str(c.get("bias", ""))
        bc = _bias_color(bias)
        conf = html.escape(str(c.get("confidence", "")))
        name = html.escape(str(c.get("name", "")))
        handle = html.escape(str(c.get("handle", "")))
        style = html.escape(str(c.get("style", "")))
        asof = html.escape(str(c.get("asof", "")))
        src = str(c.get("source", ""))
        src_txt = html.escape(src[:60])
        src_html = (f"<a href='{html.escape(src)}' target='_blank' rel='noopener' "
                    f"style='color:var(--muted-2)'>{src_txt}</a>"
                    if src.startswith("http") else f"<span class='muted'>{src_txt}</span>")
        cards.append(
            f"<div class='card' style='flex:1;min-width:280px;max-width:420px;margin:0'>"
            f"<div style='display:flex;justify-content:space-between;align-items:baseline;gap:8px'>"
            f"<span><b>{name}</b> <span class='muted' style='font-size:12px'>{handle}</span></span>"
            f"<span style='color:{bc};font-weight:700;font-size:13px'>{html.escape(bias)}</span></div>"
            f"<div class='muted' style='font-size:11px;margin:2px 0 8px'>{style} · 신뢰도 {conf}</div>"
            f"<div style='font-size:13px;margin-bottom:5px'><b style='color:var(--muted-2)'>BTC</b> {html.escape(str(c.get('btc', ''))[:220])}</div>"
            f"<div style='font-size:13px;margin-bottom:5px'><b style='color:var(--muted-2)'>ETH</b> {html.escape(str(c.get('eth', ''))[:160])}</div>"
            f"<div style='font-size:13px;margin-bottom:8px'><b style='color:var(--muted-2)'>시장</b> {html.escape(str(c.get('market', ''))[:220])}</div>"
            f"<div class='muted' style='font-size:11px;display:flex;justify-content:space-between;gap:8px'>"
            f"<span>기준 {asof}</span>{src_html}</div></div>"
        )
    return f"""
  <h2>📐 상위 차티스트 현재 뷰 <span class="muted">({ts} KST 기준)</span></h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap">{"".join(cards)}</div>
  <div class="muted" style="margin-top:8px">⚠️ 각 인물의 주장이며 사실·투자조언 아님. 뷰는 수시로 바뀌며 과거 적중이 미래를 보장하지 않습니다.</div>
"""


_ETF_JS = r"""<script>
(function(){
 var D=(window.ETFDATA||{}).assets||{};
 var TF='90'; try{var s=localStorage.getItem('ct_etf_tf');if(s)TF=s;}catch(_e){}
 function musd(v){var a=Math.abs(v),s=v<0?'-':'+';
   if(a>=1000)return s+'$'+(a/1000).toFixed(2)+'B';
   if(a>=1)return s+'$'+a.toFixed(0)+'M'; return s+'$'+(a*1000).toFixed(0)+'K';}
 function hl(){document.querySelectorAll('.etftf').forEach(function(b){
   b.classList.toggle('tfbtn-active', b.getAttribute('data-etf')===TF);});}
 function draw(sym){
   var el=document.getElementById('etf-'+sym); if(!el)return;
   var rows=D[sym]||[];
   var sel=(TF==='all')?rows:rows.slice(-parseInt(TF,10));
   if(sel.length<2){el.innerHTML='<div class="muted">구간 데이터 부족</div>';
     var v0=document.getElementById('etfv-'+sym); if(v0)v0.textContent='—'; return;}
   var flows=sel.map(function(r){return r[1];});
   var cum=[],c=0; for(var i=0;i<flows.length;i++){c+=flows[i];cum.push(c);}
   var net=c,last=flows[flows.length-1];
   var vh=document.getElementById('etfv-'+sym);
   if(vh){vh.classList.remove('muted');
     vh.innerHTML='구간 순유입 <b style="color:'+(net>=0?'#16a34a':'#e23b4a')+'">'+musd(net)+'</b>'+
       ' · 최근일 <b style="color:'+(last>=0?'#16a34a':'#e23b4a')+'">'+musd(last)+'</b>'+
       ' <span class="muted">('+sel.length+'일)</span>';}
   var W=Math.max(300,el.clientWidth||560),H=Math.max(140,el.clientHeight||200);
   var padL=54,padR=54,padT=10,padB=22,plotW=W-padL-padR,plotH=H-padT-padB,n=sel.length;
   var fmax=Math.max.apply(null,flows.map(function(x){return Math.abs(x);}).concat([1]));
   var cmin=Math.min.apply(null,cum.concat([0])),cmax=Math.max.apply(null,cum.concat([0])); if(cmax===cmin)cmax+=1;
   var bx=function(i){return padL+(i+0.5)/n*plotW;};
   var zeroY=padT+plotH*0.5;
   var by=function(v){return padT+plotH*(1-(v+fmax)/(2*fmax));};
   var cy=function(v){return padT+plotH*(1-(v-cmin)/(cmax-cmin));};
   var bw=Math.max(0.6,plotW/n*0.62);
   var o=['<svg viewBox="0 0 '+W+' '+H+'" width="100%" height="100%" style="display:block" preserveAspectRatio="none">'];
   o.push('<line x1="'+padL+'" y1="'+zeroY.toFixed(1)+'" x2="'+(W-padR)+'" y2="'+zeroY.toFixed(1)+'" stroke="rgba(255,255,255,0.18)"/>');
   for(var j=0;j<n;j++){var f=flows[j],col=f>=0?'#16a34a':'#e23b4a',y1=by(f),top=Math.min(zeroY,y1),h=Math.max(0.6,Math.abs(y1-zeroY));
     o.push('<rect x="'+(bx(j)-bw/2).toFixed(1)+'" y="'+top.toFixed(1)+'" width="'+bw.toFixed(1)+'" height="'+h.toFixed(1)+'" fill="'+col+'" opacity="0.72"/>');}
   var d='';for(var k=0;k<n;k++){d+=(k?'L':'M')+bx(k).toFixed(1)+','+cy(cum[k]).toFixed(1);}
   o.push('<path d="'+d+'" fill="none" stroke="#6c72ff" stroke-width="1.7"/>');
   o.push('<text x="6" y="'+(padT+8)+'" fill="#8d969e" font-size="10">'+musd(fmax)+'</text>');
   o.push('<text x="6" y="'+(H-padB)+'" fill="#8d969e" font-size="10">'+musd(-fmax)+'</text>');
   o.push('<text x="'+(W-padR+4)+'" y="'+(cy(cmax)+8).toFixed(1)+'" fill="#6c72ff" font-size="10">'+musd(cmax)+'</text>');
   o.push('<text x="'+(W-padR+4)+'" y="'+cy(cmin).toFixed(1)+'" fill="#6c72ff" font-size="10">'+musd(cmin)+'</text>');
   var ix=[0,Math.floor(n/2),n-1];
   for(var m=0;m<3;m++){var dt=(sel[ix[m]][0]||'').slice(2),an=m===0?'start':(m===2?'end':'middle');
     o.push('<text x="'+bx(ix[m]).toFixed(1)+'" y="'+(H-6)+'" fill="#8d969e" font-size="9" text-anchor="'+an+'">'+dt+'</text>');}
   o.push('</svg>');el.innerHTML=o.join('');}
 function drawAll(){hl();Object.keys(D).forEach(draw);}
 document.addEventListener('click',function(e){var t=e.target.closest&&e.target.closest('.etftf');if(!t)return;
   TF=t.getAttribute('data-etf');try{localStorage.setItem('ct_etf_tf',TF);}catch(_e){}drawAll();});
 if(window.ResizeObserver){Object.keys(D).forEach(function(sym){var el=document.getElementById('etf-'+sym);
   if(el)new ResizeObserver(function(){draw(sym);}).observe(el);});}
 window.CT_drawEtf=drawAll;   // 소프트 자동갱신이 리서치 탭을 교체한 뒤 재렌더용
 drawAll();
})();
</script>"""


def _etf_section(data: dict) -> str:
    """리서치 탭: BTC·ETH·SOL·XRP 스팟 ETF 일별 순유입(막대)+누적(선). 시계열 구간 선택(클라이언트)."""
    assets = (data or {}).get("assets") or {}
    order = [s for s in ("BTC", "ETH", "SOL", "XRP") if assets.get(s)]
    if not order:
        return ""
    ts = kst_display((data or {}).get("ts"), "%m-%d %H:%M")
    unit = html.escape(str((data or {}).get("unit", "USD millions")))
    source = str((data or {}).get("source", ""))
    src_html = (f"<a href='{html.escape(source)}' target='_blank' rel='noopener' style='color:var(--muted-2)'>"
                f"{html.escape(source[:60])}</a>" if source.startswith("http")
                else f"<span class='muted'>{html.escape(source[:70])}</span>")
    tfs = [("1주", "7"), ("1달", "30"), ("3달", "90"), ("6달", "180"), ("1년", "365"), ("ALL", "all")]
    tfbtns = "".join(f'<button class="etftf" data-etf="{v}">{lbl}</button>' for lbl, v in tfs)
    cards = []
    for sym in order:
        cards.append(
            f"<div class='card' style='flex:1;min-width:340px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:baseline;gap:8px'>"
            f"<b>{sym} 스팟 ETF</b>"
            f"<span class='muted' style='font-size:11px'>막대=일별 · <span style='color:#6c72ff'>선=누적</span></span></div>"
            f"<div id='etfv-{sym}' class='muted' style='font-size:13px;margin:4px 0 6px'>로딩…</div>"
            f"<div id='etf-{sym}' class='minichart' style='height:200px'></div></div>")
    js_data = {s: [[str(r["date"]), float(r["flow"])]
                   for r in (assets[s] or []) if r.get("flow") is not None and r.get("date")]
               for s in order}
    cfg = "<script>window.ETFDATA=" + json.dumps({"assets": js_data}) + ";</script>"
    return f"""
  <h2>🏦 BTC·ETH·SOL·XRP 스팟 ETF 순유입 <span class="muted">({ts} KST · 단위 {unit})</span>
    <span style="margin-left:8px;white-space:nowrap">{tfbtns}</span></h2>
  <div style="display:flex;gap:14px;flex-wrap:wrap">{"".join(cards)}</div>
  <div class="muted" style="margin-top:8px">출처: {src_html} · 누적선은 <b>선택 구간 내</b> 누적. 일 단위 발표(실시간 아님), 지연·정정 가능. 투자조언 아님.</div>
  {cfg}{_ETF_JS}
"""


def render_html(journal: TradeJournal, equity: float | None = None,
                events: list | None = None, refresh_sec: int = 0,
                start_equity: float | None = None,
                btc_series: list | None = None,
                market_extra: dict | None = None,
                tickers: list | None = None,
                equity_history: list | None = None) -> str:
    st = journal.stats()
    # 헤드라인 누적수익률·총실현손익: 실제 잔고(caller 가 넘긴 equity) 우선 —
    # 수수료·펀딩 등 저널이 못 담는 비용까지 포함해 실잔고와 일치. 없으면 저널 합산.
    if equity is not None and start_equity and start_equity > 0:
        head_pnl = equity - start_equity
        head_ret = (equity / start_equity - 1.0) * 100.0
    else:
        head_pnl = st["total_pnl"]
        head_ret = None  # 아래 final_pct 로 대체
    pnl_color = "#16a34a" if head_pnl >= 0 else "#e23b4a"
    # 헤드라인 '누적 손익'(실잔고 기준)과 저널 청산손익 합이 다를 수 있음(수수료·펀딩·
    # 슬리피지·미실현). 두 수치가 벌어지면 거래 실현합을 부제로 함께 노출해 혼동 방지.
    realized_pnl = float(st["total_pnl"])
    head_sub = (f"<span class='muted' style='font-size:10px'>거래실현 {realized_pnl:+,.2f}</span>"
                if abs(head_pnl - realized_pnl) > 0.01 else "")
    events = events or []
    # 전체 페이지 리로드(meta refresh) 대신 JS 부드러운 갱신에 쓸 주기(초)만 주입.
    refresh_tag = f'<script>window.CT_REFRESH={int(refresh_sec)};</script>'
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")
    now_file = datetime.now(KST).strftime("%Y%m%d_%H%M")
    trades_csv_js = json.dumps(_trades_csv(journal))  # 전체 거래 CSV(JS 임베드용)

    # --- 포트폴리오 차트 데이터 ---
    # 실잔고 이력이 '청산거래가 있는 모든 날짜'를 커버할 때만 실잔고 기준(수수료·펀딩 포함)을
    # 쓴다. 이력이 짧으면(봇 재시작 직후 등) 과거 거래가 통째로 차트에서 빠지므로,
    # 그 경우엔 저널(거래실현) 기준으로 폴백해 모든 거래가 올바른 날짜에 표시되게 한다.
    _eqb = _return_series_equity(equity_history or [], start_equity or 0.0)
    use_equity = bool(_eqb)
    if _eqb:
        trade_days = {datetime.fromtimestamp(e, KST).strftime("%m-%d")
                      for e in (_epoch(t.closed_at) for t in journal.closed_trades()
                                if t.closed_at) if e}
        eq_days = {datetime.fromtimestamp(float(ts), KST).strftime("%m-%d")
                   for ts, _ in (equity_history or [])}
        if trade_days and not trade_days.issubset(eq_days):
            use_equity = False   # 실잔고 이력이 일부 거래일을 못 덮음 → 저널 기준으로
    if use_equity:
        ret_pts, daily_bars, final_pct = _eqb
        series_basis = "실잔고 기준"
    else:
        ret_pts, daily_bars, final_pct = _return_series(journal, start_equity or 0.0)
        series_basis = "거래실현 기준"
    port_color = "#6c72ff"   # 코발트 바이올렛(브랜드 액센트)
    line_series = [{"label": "포트폴리오 수익률", "color": port_color, "points": ret_pts}]
    if btc_series and len(btc_series) >= 2:
        line_series.append({"label": "BTC 매수후보유", "color": "#f7931a",
                            "points": [(x, y) for x, y in btc_series]})
    if head_ret is None:      # 실잔고 없으면 저널 곡선 최종값 사용
        head_ret = final_pct
    ret_color = "#16a34a" if head_ret >= 0 else "#e23b4a"
    m = _strategy_metrics(journal, start_equity)
    btc_final = btc_series[-1][1] if btc_series else None
    btc_cmp = (f" · BTC {btc_final:+.1f}%" if btc_final is not None else "")

    chart_section = f"""
  <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:stretch">
    <div style="flex:1;min-width:340px;display:flex;flex-direction:column">
      <h2>📈 포트폴리오 추이 (수익률 vs BTC 매수후보유) <span class="muted" style="font-size:11px">· {series_basis}</span></h2>
      <div class="card" style="flex:1;display:flex;align-items:center">{charts.line_chart(line_series, width=560, height=240)}</div>
    </div>
    <div style="flex:1;min-width:340px;display:flex;flex-direction:column">
      <h2>📊 일별 손익 (USDT) <span class="muted" style="font-size:11px">· {series_basis}</span></h2>
      <div class="card" style="flex:1;display:flex;align-items:center">{charts.bar_chart(daily_bars, width=560, height=240, unit="")}</div>
    </div>
  </div>
"""

    # --- 알트 상대강도 + 시총 TOP10 + 매크로 괴리 ---
    me = market_extra or {}
    alt = me.get("alt_strength") or {}
    mcap = me.get("mcap_top") or []
    macro = me.get("macro") or []
    strength_section = f"""
  <h2>💪 BTC 대비 강도 (스테이블 제외)</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;align-items:start">
    {_strength_table("상대강도 1일", alt.get("1d", []))}
    {_strength_table("상대강도 7일", alt.get("7d", []))}
    {_strength_table("상대강도 30일", alt.get("30d", []))}
    {_mcap_table(mcap)}
    {_watchlist_card()}
  </div>
""" if (alt or mcap) else ""
    macro_section = _macro_view(macro)

    brief_section = _brief_section(load_market_brief())
    kol_section = _kol_section(load_kol_watch())
    chartists_section = _chartists_section(load_chartist_views())
    etf_section = _etf_section(load_etf_flows())

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
                c = "#16a34a" if pnl >= 0 else "#e23b4a"
                notional_c = (t.entry_price or 0.0) * (t.quantity or 0.0)
                out.append(
                    f"<tr><td>{html.escape(t.symbol)}</td>"
                    f"<td>{t.direction.upper()}</td>"
                    f"<td>{t.quantity:g}</td>"
                    f"<td>{notional_c:,.2f}</td>"
                    f"<td>{t.entry_price:.4f}</td>"
                    f"<td>{(t.exit_price or 0):.4f}</td>"
                    f"<td class='muted' style='font-size:11px'>{html.escape(_short_time(t.opened_at))}</td>"
                    f"<td class='muted' style='font-size:11px'>{html.escape(_short_time(t.closed_at))}</td>"
                    f"<td class='muted'>{html.escape(t.holding_human())}</td>"
                    f"<td style='color:{c}'>{pnl:+.2f}</td>"
                    f"<td>{html.escape(t.exit_reason)}</td></tr>"
                )
            else:
                notional = (t.entry_price or 0.0) * (t.quantity or 0.0)  # 진입 명목가(포지션 사이즈)
                out.append(
                    f"<tr class='pos-row' data-sym='{html.escape(t.symbol)}' "
                    f"data-dir='{html.escape(t.direction)}' data-entry='{t.entry_price}' "
                    f"data-qty='{t.quantity}'>"
                    f"<td>{html.escape(t.symbol)}</td>"
                    f"<td>{t.direction.upper()}</td>"
                    f"<td>{t.quantity:g}</td>"
                    f"<td>{notional:,.2f}</td>"
                    f"<td>{t.entry_price:.4f}</td>"
                    f"<td class='pos-cur muted'>-</td>"
                    f"<td class='pos-pct muted'>-</td>"
                    f"<td class='pos-pnl muted'>-</td>"
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
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<title>crypto-trader 대시보드</title>
<style>
  /* 디자인 토큰 — Revolut 영감 (revolut/DESIGN.md): 트루블랙 캔버스 + 코발트 바이올렛 */
  :root {{
    --bg:#000000; --surface:#16181a; --surface-2:#0a0a0a; --border:rgba(255,255,255,0.12);
    --text:#ffffff; --muted:rgba(255,255,255,0.72); --muted-2:#8d969e;
    --pos:#16a34a; --neg:#e23b4a; --accent:#6c72ff; --brand:#494fdf; --btc:#f7931a; --gold:#eab308;
    --radius:20px; --radius-sm:12px; --pad:20px; --gap:14px;
  }}
  body {{ font-family: 'Pretendard', 'Inter', 'Malgun Gothic', 'Apple SD Gothic Neo', -apple-system, system-ui, sans-serif; background:var(--bg); color:var(--text); margin:0; padding:28px; letter-spacing:0.2px; -webkit-font-smoothing:antialiased; }}
  h1 {{ font-size:20px; }} h2 {{ font-size:15px; color:var(--muted); margin-top:28px; }}
  h3 {{ font-size:14px; color:var(--muted); }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(126px,1fr)); gap:10px; margin:16px 0; }}
  .stat {{ background:var(--surface); border-radius:var(--radius-sm); padding:13px 14px; display:flex; flex-direction:column; gap:5px; }}
  .stat span {{ font-size:11px; color:var(--muted); }} .stat b {{ font-size:18px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ text-align:left; padding:8px 10px; border-bottom:1px solid var(--border); }}
  /* 강도·시총 등 컴팩트 표: 셀 여백을 줄여 좁은 카드에서도 가로 스크롤 없이 맞춤 */
  .mtbl {{ font-size:12px; }}
  .mtbl th, .mtbl td {{ padding:5px 6px; font-variant-numeric:tabular-nums; }}
  th {{ color:var(--muted); font-weight:600; }}
  .card {{ background:var(--surface); border-radius:var(--radius); padding:var(--pad); margin:10px 0; overflow-x:auto; }}
  .muted {{ color:var(--muted-2); font-size:12px; }}
  details.events {{ background:var(--surface); border-radius:var(--radius); padding:8px 14px; margin-top:28px; }}
  details.events summary {{ cursor:pointer; color:var(--muted); font-size:14px; padding:6px 0; }}
  .futsearch {{ width:100%; box-sizing:border-box; background:var(--surface-2); color:var(--text); border:1px solid var(--border); border-radius:12px; padding:9px 12px; font-size:13px; }}
  .futsearch::placeholder {{ color:var(--muted-2); }}
  .tkname {{ background:transparent; color:var(--text); border:none; font-size:18px; font-weight:700; cursor:pointer; padding:2px 0; }}
  .tkname:hover {{ color:var(--accent); }}
  .tklist {{ max-height:240px; overflow-y:auto; margin-top:6px; display:grid; grid-template-columns:repeat(auto-fill,minmax(80px,1fr)); gap:4px; }}
  .symlink {{ cursor:pointer; }}
  b.symlink:hover {{ color:var(--brand); text-decoration:underline; }}
  .card.symlink:hover {{ border-color:var(--brand); }}
  .tkopt {{ padding:6px 8px; border:1px solid var(--border); border-radius:9999px; font-size:12px; text-align:center; cursor:pointer; }}
  .tkopt:hover {{ background:var(--brand); color:#fff; }}
  .tfbtn, .oitf, .cvdtf, .etftf {{ background:transparent; color:var(--muted); border:1px solid var(--border); border-radius:9999px; padding:3px 9px; margin-left:4px; font-size:12px; cursor:pointer; }}
  .tfbtn-active {{ background:var(--brand); color:#fff; border-color:var(--brand); }}
  /* 차트: 세로 리사이즈 가능(모서리 드래그), 하단 20%는 거래량 막대 */
  .mkt-chartcard {{ display:flex; flex-direction:column; padding:14px 16px; }}
  .chartarea {{ margin-top:8px; height:260px; min-height:150px; max-height:720px; resize:vertical; overflow:hidden; }}
  .mkt-derivcard {{ display:flex; flex-direction:column; padding:14px 16px; }}
  /* OI·CVD 미니 라인차트 */
  .minichart {{ margin-top:8px; height:180px; min-height:130px; }}
  /* 파생 요약: 펀딩 행(펀딩/APR/24h) + 포지셔닝 박스(넷롱/상위넷롱/스마트머니갭) */
  .dfrow {{ display:flex; gap:10px; margin-bottom:12px; }}
  .dfcell {{ flex:1; min-width:0; display:flex; flex-direction:column; gap:2px; }}
  .dfcell b {{ font-size:15px; font-weight:700; }}
  .dbox {{ border:1px solid var(--border); border-radius:12px; padding:8px 11px; }}
  .dboxh {{ color:var(--muted-2); font-size:11px; margin-bottom:4px; }}
  .prow {{ display:flex; justify-content:space-between; align-items:baseline; gap:8px; padding:6px 0; border-bottom:1px solid var(--border); }}
  .prow:last-child {{ border-bottom:none; }}
  .prow b {{ font-size:15px; font-weight:700; }}
  .dlab {{ color:var(--muted-2); font-size:12px; }}
  .dsub {{ color:var(--muted-2); font-size:11px; }}
  .tabs {{ display:flex; gap:6px; margin:18px 0 4px; border-bottom:1px solid var(--border); }}
  .tab {{ background:transparent; color:var(--muted); border:none; border-bottom:2px solid transparent; padding:9px 16px; font-size:14px; font-weight:600; cursor:pointer; }}
  .tab-active {{ color:var(--text); border-bottom-color:var(--brand); }}
</style></head>
<body>
  <h1>🤖 crypto-trader 대시보드</h1>
  <div class="muted" id="gen-time">생성 {now_kst}</div>
  <div id="ticker-strip">{_ticker_strip(tickers or [])}</div>

  <div class="tabs">
    <button class="tab tab-active" data-tab="perf">📊 성과</button>
    <button class="tab" data-tab="market">🌐 시장</button>
    <button class="tab" data-tab="research">📰 리서치</button>
    <button class="tab" data-tab="leaderboard">🏆 리더보드</button>
  </div>

  <div class="tabpane" data-pane="perf">
    <div class="grid">
      {equity_row}
      <div class="stat"><span>누적 수익률</span><b style="color:{ret_color}">{head_ret:+.2f}%</b><span class="muted">{btc_cmp}</span></div>
      <div class="stat"><span>누적 손익 (USDT)</span><b style="color:{pnl_color}">{head_pnl:+,.2f}</b>{head_sub}</div>
      <div class="stat"><span>승률</span><b>{st['win_rate']:.1f}%</b></div>
      <div class="stat"><span>손익비 (PF)</span><b>{st['profit_factor']:.2f}</b></div>
      <div class="stat"><span>샤프 (거래)</span><b>{m['sharpe']:.2f}</b></div>
      <div class="stat"><span>소르티노</span><b>{m['sortino']:.2f}</b></div>
      <div class="stat"><span>최대낙폭 (MDD)</span><b style="color:#e23b4a">{m['mdd_pct']:.1f}%</b></div>
      <div class="stat"><span>기대값/거래</span><b>{m['expectancy_pct']:+.2f}%</b></div>
      <div class="stat"><span>손익크기비</span><b>{m['payoff']:.2f}</b></div>
      <div class="stat"><span>청산 거래</span><b>{st['total_trades']} <small style="font-size:12px;color:#94a3b8">(승 {st['wins']}/패 {st['losses']})</small></b></div>
      <div class="stat"><span>평균 유지시간</span><b>{st['avg_holding_human']}</b></div>
      <div class="stat"><span>열린 포지션</span><b>{st['open_trades']}</b></div>
    </div>
    <div class="muted" style="margin:4px 0 8px">지표는 청산 {m['n']}건 기준 — 거래가 쌓일수록 안정적입니다.
    누적 손익·수익률은 <b>실잔고 기준</b>(수수료·펀딩·슬리피지 포함), 손익비·기대값은 거래기록 실현손익 기준이라 서로 다를 수 있습니다.</div>
    {chart_section}
    <h2>열린 포지션</h2>
    <table><thead><tr><th>심볼</th><th>방향</th><th>수량</th><th>포지션(USDT)</th><th>진입가</th><th>현재가</th><th>손익률</th><th>PnL(USDT)</th><th>손절</th><th>익절</th><th>모드</th></tr></thead>
    <tbody>{rows(journal.open_trades(), False) or "<tr><td colspan=11>없음</td></tr>"}</tbody></table>
    <div class="muted" style="margin-top:4px;font-size:11px">현재가·손익률·PnL 은 serve_dashboard 서버 모드에서 실시간 표시(명목가 기준, 수수료 제외).</div>
    <h2>최근 청산 (최대 20건)
      <button id="dl-trades" class="tfbtn" style="margin-left:10px">⬇ 전체 거래 CSV</button></h2>
    <table><thead><tr><th>심볼</th><th>방향</th><th>수량</th><th>포지션(USDT)</th><th>진입</th><th>청산</th><th>오픈시각</th><th>종료시각</th><th>거래시간</th><th>손익</th><th>사유</th></tr></thead>
    <tbody>{rows(sorted(journal.closed_trades(), key=lambda t: t.closed_at or "", reverse=True)[:20], True) or "<tr><td colspan=11>없음</td></tr>"}</tbody></table>
  </div>

  <div class="tabpane" data-pane="market" style="display:none">
    <h2>📈 차트 · 파생 지표</h2>
    {_market_view(tickers or [])}
    {strength_section}
    {macro_section}
  </div>

  <div class="tabpane" data-pane="research" style="display:none">
    {chartists_section}
    {etf_section}
    {brief_section}
    {kol_section}
    {event_section}
  </div>

  <div class="tabpane" data-pane="leaderboard" style="display:none">
    <h2>🏆 리더보드 — 상위 트레이더 / 라이징스타</h2>
    <div style="margin-bottom:8px">
      <button class="tfbtn lbsrc tfbtn-on" data-src="hyperliquid">Hyperliquid</button>
      <button class="tfbtn lbsrc" data-src="binance">Binance</button>
    </div>
    <div class="muted" style="margin-bottom:8px">좌 <b>상위 트레이더</b>(통산 PnL·ROI 상위 · 현재 포지션) · 우 <b>라이징스타</b>(최근 한 달 수익·거래빈도 상위).
    5대 메이저(BTC/ETH/SOL/XRP/BNB) · 양방향/고배율 제외 · 10분 캐시. <b>정보용, 매매권유 아님.</b>
    (Binance는 지역차단으로 로컬 전용 + 포지션은 로그인 필요라 실적·PnL곡선만 표시)</div>
    <div id="lb-root" class="muted">시장 탭처럼 서버 모드(serve_dashboard)에서 로드됩니다 — 리더보드 탭을 열면 불러옵니다.</div>
  </div>

  <script>
   function _showTab(tab){{
     var found=false;
     document.querySelectorAll('.tab').forEach(function(b){{var on=b.getAttribute('data-tab')===tab;b.classList.toggle('tab-active',on);if(on)found=true;}});
     if(!found)tab='perf';
     document.querySelectorAll('.tab').forEach(function(b){{b.classList.toggle('tab-active',b.getAttribute('data-tab')===tab);}});
     document.querySelectorAll('.tabpane').forEach(function(p){{p.style.display=p.getAttribute('data-pane')===tab?'block':'none';}});
     return tab;}}
   window.__showTab=_showTab;   // 상단 티커 심볼 클릭 시 차트 IIFE가 시장 탭으로 전환하도록 노출
   document.addEventListener('click',function(e){{var t=e.target.closest&&e.target.closest('.tab');if(!t)return;
     var tab=_showTab(t.getAttribute('data-tab'));
     try{{localStorage.setItem('ct_tab',tab);}}catch(_e){{}} }});
   // 자동 새로고침 후에도 마지막으로 보던 탭 유지
   (function(){{var saved;try{{saved=localStorage.getItem('ct_tab');}}catch(_e){{}}if(saved)_showTab(saved);}})();
   // 리더보드 탭: 처음 열릴 때 1회 /api/leaderboard 로드(무거워서 지연) + 소스 토글(HL/Binance)
   (function(){{
     var curSrc='hyperliquid', cache={{}};
     function usd(n){{n=Number(n)||0;var a=Math.abs(n);
       if(a>=1e9)return (n/1e9).toFixed(2)+'B';if(a>=1e6)return (n/1e6).toFixed(2)+'M';
       if(a>=1e3)return (n/1e3).toFixed(1)+'K';return n.toFixed(0);}}
     function fmtT(ms){{if(!ms)return '<span class="muted">장기</span>';var d=new Date(ms);
       return (d.getUTCFullYear()%100)+'/'+(d.getUTCMonth()+1)+'/'+d.getUTCDate();}}
     function px(v){{if(v==null)return '-';return v>=100?Math.round(v).toLocaleString():v.toFixed(4);}}
     function spark(hist){{  // 역대 누적 PnL 미니차트(시간축 x · PnL값축 y)
       if(!hist||hist.length<2)return '';
       var vs=hist.map(function(p){{return p[1];}});
       var mn=Math.min.apply(null,vs),mx=Math.max.apply(null,vs);
       if(mn>0)mn=0;if(mx<0)mx=0;                 // 0 포함해 부호 보이게
       var rng=(mx-mn)||1;
       var W=290,H=100,PL=54,PB=16,PT=6,PR=8,pw=W-PL-PR,ph=H-PT-PB;
       var t0=hist[0][0],t1=hist[hist.length-1][0],tr=(t1-t0)||1;
       var pts=hist.map(function(p){{
         var x=PL+((p[0]-t0)/tr)*pw;var y=PT+(1-(p[1]-mn)/rng)*ph;
         return x.toFixed(1)+','+y.toFixed(1);}}).join(' ');
       var last=vs[vs.length-1],col=(last>=0)?'#16c784':'#e23b4a';
       var zy=PT+(1-(0-mn)/rng)*ph;
       function yl(v){{var y=PT+(1-(v-mn)/rng)*ph;
         return '<text x="'+(PL-4)+'" y="'+(y+3).toFixed(1)+'" font-size="9" fill="#8a94a6" text-anchor="end">$'+usd(v)+'</text>';}}
       function xl(ms,x,an){{var d=new Date(ms);
         return '<text x="'+x+'" y="'+(H-4)+'" font-size="9" fill="#8a94a6" text-anchor="'+an+'">'+(d.getUTCFullYear()%100)+'/'+(d.getUTCMonth()+1)+'</text>';}}
       return '<svg width="'+W+'" height="'+H+'" style="display:block" title="역대 누적 PnL">'
         +'<line x1="'+PL+'" y1="'+(PT).toFixed(1)+'" x2="'+PL+'" y2="'+(PT+ph).toFixed(1)+'" stroke="#334" stroke-width="0.5"/>'
         +'<line x1="'+PL+'" y1="'+zy.toFixed(1)+'" x2="'+(W-PR)+'" y2="'+zy.toFixed(1)+'" stroke="#556" stroke-width="0.5" stroke-dasharray="2,2"/>'
         +yl(mx)+yl(mn)+(mn<0&&mx>0?yl(0):'')
         +xl(t0,PL,'start')+xl(t1,W-PR,'end')
         +'<polyline points="'+pts+'" fill="none" stroke="'+col+'" stroke-width="1.5"/></svg>';
     }}
     function sumCards(s){{  // 코인별 집계 카드
       if(!s||!s.length)return '';
       function rng(r){{return r?('$'+usd(r[0])+'~$'+usd(r[1])):'-';}}
       var cards=s.map(function(c){{
         return '<div style="flex:1;min-width:150px;padding:8px;border:1px solid var(--line,#233);border-radius:8px">'
           +'<div style="font-weight:700;margin-bottom:3px">'+c.coin+'</div>'
           +'<div style="font-size:13px"><span style="color:#16c784">롱 '+c.long_count+'</span> · <span style="color:#e23b4a">숏 '+c.short_count+'</span></div>'
           +'<div style="font-size:11px" class="muted">롱 $'+usd(c.long_notional)+' / 숏 $'+usd(c.short_notional)+'</div>'
           +'<div style="font-size:11px" class="muted">청산 롱 '+rng(c.liq_long_range)+'</div>'
           +'<div style="font-size:11px" class="muted">청산 숏 '+rng(c.liq_short_range)+'</div></div>';
       }}).join('');
       return '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">'+cards+'</div>';
     }}
     function esc(s){{return String(s==null?'':s).replace(/[<>&]/g,function(c){{return c==='<'?'&lt;':c==='>'?'&gt;':'&amp;';}});}}
     function card(t){{
       var addr=t.addr||'';
       var nm=t.name?esc(t.name):(addr.slice(0,6)+'…'+addr.slice(-4));
       var head;
       if(t.profile_url)head='<a href="'+t.profile_url+'" target="_blank" style="font-weight:700">'+nm+'</a>';
       else if(addr.indexOf('0x')===0)head='<a href="https://hypurrscan.io/address/'+addr+'" target="_blank" style="font-weight:700">'+nm+'</a>';
       else head='<b>'+nm+'</b>';
       var m='<span>PnL <b style="color:#16c784">$'+usd(t.pnl)+'</b></span>'
         +'<span>ROI <b>'+Math.round((t.roi||0)*100)+'%</b></span>';
       if(t.month_pnl!=null)m+='<span class="muted">한달 <b style="color:'+((t.month_pnl>=0)?'#16c784':'#e23b4a')+'">$'+usd(t.month_pnl)+'</b></span>';
       if(t.turnover!=null)m+='<span class="muted">회전 '+t.turnover.toFixed(1)+'x</span>';
       if(t.recent_pnl!=null)m+='<span class="muted">90일 <b style="color:'+((t.recent_pnl>=0)?'#16c784':'#e23b4a')+'">$'+usd(t.recent_pnl)+'</b></span>';
       if(t.account_value)m+='<span class="muted">계좌 $'+usd(t.account_value)+'</span>';
       if(t.mdd!=null)m+='<span class="muted">MDD '+Math.round((t.mdd||0)*100)+'%</span>';
       if(t.subscribers!=null)m+='<span class="muted">구독 '+usd(t.subscribers)+'</span>';
       if(t.net_side)m+='<span>순방향 '+((t.net_side==='long')?'<span style="color:#16c784">롱</span>':'<span style="color:#e23b4a">숏</span>')+'</span>';
       if(t.max_lev)m+='<span class="muted">최대'+t.max_lev+'x</span>';
       var ps=t.positions||[],body;
       if(ps.length){{
         var rows=ps.map(function(p){{
           var uc=(p.upnl>=0)?'#16c784':'#e23b4a';var sd=(p.side==='long')?'롱':'숏';
           var sc=(p.side==='long')?'#16c784':'#e23b4a';
           return '<tr><td style="color:'+sc+'">'+p.coin+' '+sd+'</td><td>$'+usd(p.notional)+'</td><td>'+px(p.entry)+'</td>'
             +'<td style="color:#e0964a">'+px(p.liquidation)+'</td><td>'+fmtT(p.entry_ts)+'</td>'
             +'<td style="color:'+uc+'">$'+usd(p.upnl)+'</td><td class="muted">'+(p.leverage||'-')+'x</td></tr>';
         }}).join('');
         body='<table style="width:100%;font-size:12px"><thead><tr><th>종목/방향</th><th>명목</th><th>진입</th><th>청산</th><th>진입시각</th><th>미실현</th><th>lev</th></tr></thead><tbody>'+rows+'</tbody></table>';
       }}else{{
         var st=(t.position_status==='HAS_POSITION')?'보유중':(t.position_status==='NO_POSITION')?'무포지션':(t.position_status||'비공개');
         body='<div class="muted" style="font-size:12px">현재 포지션: '+st+' <span style="opacity:.7">(바이낸스 포지션 상세는 로그인 필요)</span></div>';
       }}
       return '<div style="margin:8px 0;padding:8px;border:1px solid var(--line,#233);border-radius:8px">'
         +'<div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:4px">'+head+m+'</div>'
         +'<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-start">'
         +'<div><div class="muted" style="font-size:11px">역대 누적 PnL</div>'+spark(t.pnl_history)+'</div>'
         +'<div style="flex:1;min-width:300px">'+body+'</div></div></div>';
     }}
     function col(title,sub,list){{
       var cards=((list||[]).map(card).join(''))||'<div class="muted" style="font-size:12px">해당 트레이더 없음</div>';
       return '<div style="flex:1;min-width:340px">'
         +'<h3 style="margin:4px 0 2px">'+title+'</h3>'
         +'<div class="muted" style="font-size:11px;margin-bottom:6px">'+sub+'</div>'+cards+'</div>';
     }}
     function render(d){{
       var root=document.getElementById('lb-root');if(!root)return;
       var top=(d&&d.top)||(d&&d.traders)||[];var rising=(d&&d.rising)||[];
       if(!top.length&&!rising.length){{
         var msg=(d&&d.source==='binance')
           ?'Binance 스마트머니는 지역차단으로 <b>로컬 대시보드</b>에서만 동작합니다(개발서버는 빈 결과).'
           :'데이터 없음 — 서버 모드에서만 동작하며, 첫 로드는 리더보드 대량행 조회로 다소 걸립니다.';
         root.innerHTML='<span class="muted">'+msg+'</span>';return;}}
       var h=sumCards(d.summary||[]);
       h+='<div style="display:flex;gap:16px;flex-wrap:wrap">'
         +col('🏆 상위 트레이더','통산 PnL·ROI 상위 · 현재 포지션',top)
         +col('🚀 라이징스타','최근 한 달 수익·거래빈도 상위'+((d&&d.source==='binance')?' (ROI 상위 대체)':''),rising)
         +'</div>';
       root.innerHTML=h;
     }}
     function load(src){{
       src=src||curSrc;
       var root=document.getElementById('lb-root');if(!root)return;
       if(cache[src]){{if(curSrc===src)render(cache[src]);return;}}
       root.innerHTML='<span class="muted">불러오는 중… (첫 로드는 수십 초 걸릴 수 있습니다)</span>';
       fetch('/api/leaderboard?source='+src,{{cache:'no-store'}}).then(function(r){{return r.json();}})
         .then(function(d){{
           if(d&&d.loading){{ if(curSrc===src){{root.innerHTML='<span class="muted">불러오는 중… 리더보드 집계(백그라운드) 최대 1~2분 — 잠시만요…</span>';setTimeout(function(){{load(src);}},5000);}} return; }}
           cache[src]=d;if(curSrc===src)render(d);
         }})
         .catch(function(){{if(curSrc===src)root.innerHTML='<span class="muted">불러오기 실패 — serve_dashboard 서버 모드에서만 동작합니다.</span>';}});
     }}
     function setSrc(src){{curSrc=src;
       document.querySelectorAll('.lbsrc').forEach(function(b){{b.classList.toggle('tfbtn-on',b.getAttribute('data-src')===src);}});
       load(src);}}
     document.addEventListener('click',function(e){{
       var s=e.target.closest&&e.target.closest('.lbsrc');
       if(s){{setSrc(s.getAttribute('data-src'));return;}}
       var t=e.target.closest&&e.target.closest('.tab');
       if(t&&t.getAttribute('data-tab')==='leaderboard')load(curSrc);}});
     try{{if(localStorage.getItem('ct_tab')==='leaderboard')load(curSrc);}}catch(_e){{}}
   }})();
   // 열린 포지션 현재가·손익률·PnL 실시간 채우기(서버 모드) — 갱신 후 재호출 가능하게 함수화
   function fillPositions(){{
     var rws=document.querySelectorAll('.pos-row');if(!rws.length)return;
     var syms=[];rws.forEach(function(r){{var s=r.getAttribute('data-sym');if(s&&syms.indexOf(s)<0)syms.push(s);}});
     function fmt(v){{if(v>=1000)return v.toLocaleString('en-US',{{maximumFractionDigits:2}});
       if(v>=1)return v.toFixed(4); if(v>=0.01)return v.toFixed(5); return v.toFixed(7);}}
     fetch('/api/prices?symbols='+encodeURIComponent(syms.join(',')))
      .then(function(r){{return r.json();}}).then(function(px){{
       rws.forEach(function(r){{
        var base=(r.getAttribute('data-sym')||'').split('/')[0].toUpperCase();
        var cur=px[base];if(cur==null)return;
        var entry=parseFloat(r.getAttribute('data-entry')),qty=parseFloat(r.getAttribute('data-qty'));
        var sign=r.getAttribute('data-dir')==='short'?-1:1;
        var pnl=(cur-entry)*qty*sign, pct=entry>0?((cur-entry)/entry*100*sign):0;
        var col=pnl>=0?'#16a34a':'#e23b4a';
        var cc=r.querySelector('.pos-cur'),pc=r.querySelector('.pos-pct'),pp=r.querySelector('.pos-pnl');
        if(cc){{cc.textContent='$'+fmt(cur);cc.classList.remove('muted');}}
        if(pc){{pc.textContent=(pct>=0?'+':'')+pct.toFixed(2)+'%';pc.style.color=col;pc.classList.remove('muted');}}
        if(pp){{pp.textContent=(pnl>=0?'+':'')+pnl.toFixed(2);pp.style.color=col;pp.classList.remove('muted');}}
       }});
      }}).catch(function(){{}});
   }}
   fillPositions();
   // 부드러운 자동 갱신 — 전체 리로드 없이 서버렌더 영역(성과·리서치·티커·생성시각)만 교체.
   // 차트(시장 탭)는 자체 API 타이머로 갱신되므로 건드리지 않아 스크롤·차트 상태 보존.
   (function(){{
     var SEC=window.CT_REFRESH||0; if(!SEC||SEC<5)return;
     // file:// 로 연 정적 파일은 fetch가 CORS로 막히므로 옛 방식(전체 리로드)로 폴백.
     if(location.protocol==='file:'){{setInterval(function(){{location.reload();}},SEC*1000);return;}}
     setInterval(function(){{
       fetch(location.pathname+location.search,{{cache:'no-store'}}).then(function(r){{return r.text();}}).then(function(html){{
         var doc=new DOMParser().parseFromString(html,'text/html');
         ['perf','research'].forEach(function(pane){{
           var cur=document.querySelector('.tabpane[data-pane="'+pane+'"]');
           var nw=doc.querySelector('.tabpane[data-pane="'+pane+'"]');
           if(cur&&nw)cur.innerHTML=nw.innerHTML;   // display(활성탭 여부)는 요소에 남아 보존
         }});
         // 리서치 탭 innerHTML 교체 시 JS로 그리던 ETF 차트가 리셋되므로 재렌더
         if(window.CT_drawEtf)window.CT_drawEtf();
         var g=doc.getElementById('gen-time'),gc=document.getElementById('gen-time');
         if(g&&gc)gc.textContent=g.textContent;
         var t=doc.getElementById('ticker-strip'),tc=document.getElementById('ticker-strip');
         if(t&&tc){{if(window.CT_WL&&window.CT_WL.length){{if(window.CT_renderTopStrip)window.CT_renderTopStrip();}}
           else{{tc.innerHTML=t.innerHTML;}}}}
         fillPositions();   // 새 pos-row 실시간 가격 재주입
       }}).catch(function(){{}});
     }},SEC*1000);
   }})();
   // 전체 거래내역 CSV 다운로드
   document.addEventListener('click',function(e){{
     var b=e.target.closest&&e.target.closest('#dl-trades'); if(!b)return;
     var csv=window.TRADESCSV||''; if(!csv){{alert('거래내역이 없습니다.');return;}}
     var blob=new Blob(['\\ufeff'+csv],{{type:'text/csv;charset=utf-8'}});
     var url=URL.createObjectURL(blob),a=document.createElement('a');
     a.href=url; a.download='crypto_trades_{now_file}.csv'; document.body.appendChild(a);
     a.click(); document.body.removeChild(a); setTimeout(function(){{URL.revokeObjectURL(url);}},1000);
   }});
  </script>
  <script>window.TRADESCSV={trades_csv_js};</script>
</body></html>"""
