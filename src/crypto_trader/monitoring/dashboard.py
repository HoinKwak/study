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
            f"<tr><td>{i + 1}</td><td><b>{html.escape(sym)}</b></td>"
            f"<td style='color:{c}'>{rel:+.2f}%</td>"
            f"<td class='muted'>{r.get('alt', 0.0):+.1f}%</td></tr>"
        )
    inner = "".join(body) or "<tr><td colspan=4 class='muted'>데이터 없음</td></tr>"
    return (f"<div class='card' style='flex:1;min-width:200px'>"
            f"<div class='muted' style='margin-bottom:6px'>{title}</div>"
            f"<table><thead><tr><th>#</th><th>심볼</th><th>BTC대비</th><th>수익률</th>"
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
        body.append(
            f"<tr><td>{i + 1}</td><td><b>{html.escape(str(r.get('symbol', '')))}</b></td>"
            f"{cell(r.get('r1'))}{cell(r.get('r7'))}{cell(r.get('r30'))}</tr>"
        )
    inner = "".join(body) or "<tr><td colspan=5 class='muted'>데이터 없음</td></tr>"
    return (f"<div class='card' style='flex:1;min-width:300px'>"
            f"<div class='muted' style='margin-bottom:6px'>시총 TOP10 · BTC 대비 수익률</div>"
            f"<table><thead><tr><th>#</th><th>심볼</th><th>1일</th><th>7일</th><th>30일</th>"
            f"</tr></thead><tbody>{inner}</tbody></table></div>")


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
            f"<div class='card' style='margin:0;padding:9px 11px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:baseline'>"
            f"<b style='font-size:14px'>{sym}</b><span style='color:{c};font-size:11px'>{pct_txt}</span></div>"
            f"<div class='muted' style='font-size:11px;margin-bottom:2px'>{_fmt_px(t.get('price'))}</div>"
            f"{spark}</div>")
    return (f"<div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));"
            f"gap:8px;margin:12px 0'>{''.join(minis)}</div>")


def _market_view(tickers) -> str:
    """시장 탭: 캔들차트(좌) + 파생지표 패널(우) — 티커·타임프레임 연동."""
    top = _tickers_of(tickers)
    if not top:
        return ""
    tfs = [("1일", "1d"), ("7일", "7d"), ("30일", "30d"),
           ("6개월", "6m"), ("1년", "1y"), ("YTD", "ytd")]
    tfbtns = "".join(f'<button class="tfbtn" data-tf="{v}">{lbl}</button>' for lbl, v in tfs)
    dtfs = [("5분", "5m"), ("1시간", "1h"), ("4시간", "4h"), ("1일", "1d")]
    dtfbtns = "".join(f'<button class="dtfbtn" data-dtf="{v}">{lbl}</button>' for lbl, v in dtfs)
    d1 = str(top[0].get("symbol", "BTC"))
    chart = (
        f'<div class="card mkt-chartcard" style="flex:2;min-width:340px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'
        f'<button class="tkname" id="mkt-name"><span id="mkt-sym">{html.escape(d1)}</span> ▾</button>'
        f'<span>{tfbtns}</span></div>'
        f'<div id="mkt-search" style="display:none;margin:8px 0">'
        f'<input class="futsearch" id="mkt-input" placeholder="심볼 검색…">'
        f'<div class="tklist" id="mkt-list"></div></div>'
        f'<div id="mkt-chart" class="chartarea"><div class="muted">로딩…</div></div>'
        f'<div class="muted" style="text-align:right;font-size:10px;margin-top:2px">↕ 아래 모서리를 끌어 높이 조절</div></div>')
    derivs = (
        f'<div class="card mkt-derivcard" style="flex:1;min-width:250px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:6px">'
        f'<span class="muted">파생 지표 · <b id="mkt-dsym">{html.escape(d1)}</b></span>'
        f'<span>{dtfbtns}</span></div>'
        f'<div id="mkt-derivs"><div class="muted">로딩…</div></div></div>')
    cfg = ("<script>window.MKTCFG=" + json.dumps(
        {"syms": [str(t.get("symbol", "")) for t in top], "d1": d1}) + ";</script>")
    return (f'<div style="display:flex;flex-wrap:wrap;gap:14px;align-items:stretch">{chart}{derivs}</div>{cfg}{_CHART_JS}')


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
 var SEL={s:cfg.d1,tf:'7d',dtf:'1h'};
 var LAST=null;               // 마지막 캔들 데이터(리사이즈 재렌더용)
 var root=document.getElementById('mkt-chart');
 if(!root)return;
 var card=root.closest('.card');
 var dcard=document.querySelector('.mkt-derivcard');
 function hlTf(){card.querySelectorAll('.tfbtn').forEach(function(b){
   b.classList.toggle('tfbtn-active', b.getAttribute('data-tf')===SEL.tf);});}
 function hlDtf(){if(!dcard)return;dcard.querySelectorAll('.dtfbtn').forEach(function(b){
   b.classList.toggle('tfbtn-active', b.getAttribute('data-dtf')===SEL.dtf);});}
 function fmtPx(v){if(v>=1000)return '$'+v.toLocaleString('en-US',{maximumFractionDigits:0});
   if(v>=1)return '$'+v.toFixed(2); if(v>=0.01)return '$'+v.toFixed(4); return '$'+v.toFixed(6);}
 function usd(v){if(v==null)return '-'; if(v>=1e9)return '$'+(v/1e9).toFixed(2)+'B';
   if(v>=1e6)return '$'+(v/1e6).toFixed(1)+'M'; if(v>=1e3)return '$'+(v/1e3).toFixed(0)+'K'; return '$'+v.toFixed(0);}
 // ---- 캔들 차트 (컨테이너 실제 크기에 맞춰 렌더 → 세로 리사이즈 대응) ----
 function drawCandles(d){LAST=d;var p=(d&&d.points)||[];
   if(p.length<2){root.innerHTML='<div class="muted">데이터 없음</div>';return;}
   var W=Math.max(320,root.clientWidth||680),H=Math.max(160,root.clientHeight||320);
   var padL=64,padR=12,padT=12,padB=26;
   var xs=p.map(function(a){return a[0];});
   var lows=p.map(function(a){return a[3];}),highs=p.map(function(a){return a[2];});
   var xmin=Math.min.apply(null,xs),xmax=Math.max.apply(null,xs);
   var ymin=Math.min.apply(null,lows),ymax=Math.max.apply(null,highs);
   if(xmax===xmin)xmax+=1; if(ymax===ymin)ymax+=1; var yr=ymax-ymin;
   function sx(x){return padL+(x-xmin)/(xmax-xmin)*(W-padL-padR);}
   function sy(v){return H-padB-(v-ymin)/yr*(H-padB-padT);}
   var cw=Math.max(1.4,(W-padL-padR)/p.length*0.62);
   var o=['<svg viewBox="0 0 '+W+' '+H+'" width="100%" height="100%" style="display:block" preserveAspectRatio="none">'];
   for(var i=0;i<5;i++){var yv=ymin+yr*i/4,y=sy(yv);
     o.push('<line x1="'+padL+'" y1="'+y+'" x2="'+(W-padR)+'" y2="'+y+'" stroke="rgba(255,255,255,0.06)"/>');
     o.push('<text x="6" y="'+(y+4)+'" fill="#8d969e" font-size="11">'+fmtPx(yv)+'</text>');}
   for(var j=0;j<p.length;j++){var op=p[j][1],hi=p[j][2],lo=p[j][3],cl=p[j][4];
     var x=sx(xs[j]),up=cl>=op,col=up?'#16a34a':'#e23b4a';
     o.push('<line x1="'+x.toFixed(1)+'" y1="'+sy(hi).toFixed(1)+'" x2="'+x.toFixed(1)+'" y2="'+sy(lo).toFixed(1)+'" stroke="'+col+'" stroke-width="1"/>');
     var yo=sy(op),yc=sy(cl),top=Math.min(yo,yc),bh=Math.max(1,Math.abs(yc-yo));
     o.push('<rect x="'+(x-cw/2).toFixed(1)+'" y="'+top.toFixed(1)+'" width="'+cw.toFixed(1)+'" height="'+bh.toFixed(1)+'" fill="'+col+'"/>');}
   for(var k=0;k<5;k++){var xv=xmin+(xmax-xmin)*k/4,dt=new Date(xv);
     var lab=('0'+(dt.getMonth()+1)).slice(-2)+'-'+('0'+dt.getDate()).slice(-2);
     var an=k===0?'start':(k===4?'end':'middle');
     o.push('<text x="'+sx(xv).toFixed(1)+'" y="'+(H-6)+'" fill="#8d969e" font-size="10" text-anchor="'+an+'">'+lab+'</text>');}
   o.push('</svg>');root.innerHTML=o.join('');}
 function loadChart(){
   fetch('/api/klines?symbol='+encodeURIComponent(SEL.s)+'&tf='+SEL.tf)
   .then(function(r){return r.json();}).then(function(d){drawCandles(d);})
   .catch(function(){LAST=null;root.innerHTML='<div class="muted">차트는 serve_dashboard 서버 모드에서 표시됩니다.</div>';});
   hlTf();}
 // 컨테이너 세로 리사이즈 시 마지막 데이터로 재렌더
 if(window.ResizeObserver){var ro=new ResizeObserver(function(){if(LAST)drawCandles(LAST);});ro.observe(root);}
 // ---- 파생 지표 패널 ----
 function tile(lab,val,col,sub){return '<div class="dtile"><span class="dlab">'+lab+'</span>'+
   '<b style="color:'+(col||'#e6e8ea')+'">'+val+'</b>'+(sub?'<span class="dsub">'+sub+'</span>':'')+'</div>';}
 function renderDerivs(d){var el=document.getElementById('mkt-derivs');
   if(!d){el.innerHTML='<div class="muted">파생 데이터는 serve_dashboard 서버 모드에서 표시됩니다.</div>';return;}
   var g='#16a34a',r='#e23b4a',n='#8d969e',per=d.period||SEL.dtf;
   var fr=d.funding_rate,frp=(fr==null)?null:fr*100;
   var apr=(frp==null)?null:frp*3*365;    // 8h 펀딩 × 하루3회 × 365 = 연환산
   var gl=d.global_ls_ratio,tt=d.top_trader_ls_ratio,tk=d.taker_buy_sell_ratio;
   var netLong=(gl==null)?null:gl/(1+gl)*100, ttNet=(tt==null)?null:tt/(1+tt)*100;
   var gap=(netLong==null||ttNet==null)?null:(ttNet-netLong);   // 상위−전체 넷롱(스마트머니 갭)
   var o=[];
   o.push(tile('펀딩비 (funding)', frp==null?'-':(frp>=0?'+':'')+frp.toFixed(4)+'%',
     frp==null?n:(frp>=0?g:r), frp==null?'':(frp>=0?'롱 → 숏 지불':'숏 → 롱 지불')));
   o.push(tile('연환산 펀딩 (APR)', apr==null?'-':(apr>=0?'+':'')+apr.toFixed(1)+'%',
     apr==null?n:(apr>=0?g:r), '펀딩 8h × 3 × 365'));
   o.push(tile('OI 변화 ('+per+')', d.oi_change_pct==null?'-':(d.oi_change_pct>=0?'+':'')+d.oi_change_pct.toFixed(2)+'%',
     d.oi_change_pct==null?n:(d.oi_change_pct>=0?g:r), d.oi_notional?('미결제약정 '+usd(d.oi_notional)):''));
   o.push(tile('넷 롱 비중', netLong==null?'-':netLong.toFixed(1)+'%',
     netLong==null?n:(netLong>=50?g:r), '롱/숏 계좌 '+(gl==null?'-':gl.toFixed(2))));
   o.push(tile('상위 트레이더 넷롱', ttNet==null?'-':ttNet.toFixed(1)+'%',
     ttNet==null?n:(ttNet>=50?g:r), 'L/S '+(tt==null?'-':tt.toFixed(2))));
   o.push(tile('스마트머니 갭', gap==null?'-':(gap>=0?'+':'')+gap.toFixed(1)+'p',
     gap==null?n:(gap>=0?g:r), '상위−전체 넷롱 (양수=고래 낙관)'));
   o.push(tile('테이커 매수/매도 (CVD)', tk==null?'-':tk.toFixed(2),
     tk==null?n:(tk>=1?g:r), tk==null?'':(tk>=1?'시장가 매수 우세':'시장가 매도 우세')));
   o.push(tile('24h 거래량', usd(d.vol24),
     d.chg24==null?n:(d.chg24>=0?g:r), d.chg24==null?'':('24h '+(d.chg24>=0?'+':'')+d.chg24.toFixed(2)+'%')));
   el.innerHTML=o.join('');}
 function loadDerivs(){document.getElementById('mkt-dsym').textContent=SEL.s;
   document.getElementById('mkt-derivs').innerHTML='<div class="muted">로딩…</div>';
   fetch('/api/derivs?symbol='+encodeURIComponent(SEL.s)+'&period='+encodeURIComponent(SEL.dtf))
   .then(function(r){return r.json();}).then(function(d){renderDerivs(d);})
   .catch(function(){renderDerivs(null);});
   hlDtf();}
 // ---- 심볼 검색 ----
 function renderSyms(q){q=(q||'').toUpperCase();var box=document.getElementById('mkt-list');
   box.innerHTML=SYMS.filter(function(x){return x.toUpperCase().indexOf(q)>=0;}).slice(0,150)
   .map(function(x){return '<div class="tkopt" data-s="'+x+'">'+x+'</div>';}).join('');}
 document.addEventListener('click',function(e){var t=e.target;if(!t.closest)return;
   var tf=t.closest('.tfbtn');if(tf){SEL.tf=tf.getAttribute('data-tf');loadChart();return;}
   var dtf=t.closest('.dtfbtn');if(dtf){SEL.dtf=dtf.getAttribute('data-dtf');loadDerivs();return;}
   var nm=t.closest('#mkt-name');if(nm){var s=document.getElementById('mkt-search');
     s.style.display=s.style.display==='none'?'block':'none';if(s.style.display==='block')renderSyms('');return;}
   var op=t.closest('.tkopt');if(op){SEL.s=op.getAttribute('data-s');
     document.getElementById('mkt-sym').textContent=SEL.s;
     document.getElementById('mkt-search').style.display='none';loadChart();loadDerivs();}});
 document.addEventListener('input',function(e){var t=e.target;
   if(t.id==='mkt-input')renderSyms(t.value);});
 fetch('/api/symbols').then(function(r){return r.json();}).then(function(a){if(a&&a.length)SYMS=a;}).catch(function(){});
 loadChart();loadDerivs();
})();
</script>"""


_STAGE_COLOR = {"조기": "#22c55e", "확산": "#eab308", "뒷북": "#94a3b8"}


def _kol_section(kol: dict) -> str:
    tokens = (kol or {}).get("tokens") or []
    if not tokens:
        return ""
    ts = kst_display((kol or {}).get("ts"), "%m-%d %H:%M")
    body = []
    for t in tokens[:15]:
        stage = str(t.get("stage", ""))
        sc = next((c for k, c in _STAGE_COLOR.items() if k in stage), "#e2e8f0")
        body.append(
            f"<tr><td><b>{html.escape(str(t.get('token', '')))}</b></td>"
            f"<td class='muted'>{html.escape(str(t.get('chain', '')))}</td>"
            f"<td style='color:{sc}'>{html.escape(stage)}</td>"
            f"<td>{html.escape(str(t.get('kols', '')))}</td>"
            f"<td>{html.escape(str(t.get('thesis', ''))[:70])}</td>"
            f"<td class='muted'>{html.escape(str(t.get('risk', ''))[:40])}</td></tr>"
        )
    return f"""
  <h2>🐦 KOL 하이프 토큰 <span class="muted">({ts} KST)</span></h2>
  <div class="card" style="overflow-x:auto"><table>
  <thead><tr><th>토큰</th><th>체인</th><th>단계</th><th>KOL</th><th>서사</th><th>리스크</th></tr></thead>
  <tbody>{"".join(body)}</tbody></table>
  <div class="muted" style="margin-top:8px">⚠️ 아이디어·조기경보용, 투자조언 아님. 자체 검증 필수.</div></div>
"""


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
            f"<div style='font-size:13px;margin-top:6px'>{html.escape(str(a.get('summary', ''))[:240])}</div>"
            f"<div class='muted' style='margin-top:6px'>레벨: {html.escape(str(a.get('levels', '')))}</div>"
            f"<div class='muted'>촉매: {html.escape(str(a.get('catalysts', ''))[:120])}</div></div>"
        )
    notable = brief.get("notable", [])
    nrows = "".join(
        f"<tr><td><b>{html.escape(str(n.get('token', '')))}</b></td>"
        f"<td class='muted'>{html.escape(str(n.get('status', '')))}</td>"
        f"<td>{html.escape(str(n.get('summary', ''))[:120])}</td></tr>"
        for n in notable[:12]
    )
    notable_html = (f"<h3 style='margin-top:14px'>주목 프로젝트/토큰</h3>"
                    f"<div class='card' style='overflow-x:auto'><table><thead><tr>"
                    f"<th>토큰</th><th>상태</th><th>요약</th></tr></thead>"
                    f"<tbody>{nrows}</tbody></table></div>") if nrows else ""
    market_html = (f"<div class='card'>{html.escape(str(market)[:400])}</div>"
                   if market else "")
    return f"""
  <h2>📰 시장 분석 요약 <span class="muted">({ts} KST)</span></h2>
  {market_html}
  <div style="display:flex;gap:12px;flex-wrap:wrap">{"".join(cards)}</div>
  {notable_html}
"""


def render_html(journal: TradeJournal, equity: float | None = None,
                events: list | None = None, refresh_sec: int = 0,
                start_equity: float | None = None,
                btc_series: list | None = None,
                market_extra: dict | None = None,
                tickers: list | None = None) -> str:
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
    events = events or []
    refresh_tag = (f'<meta http-equiv="refresh" content="{refresh_sec}">'
                   if refresh_sec > 0 else "")
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")

    # --- 포트폴리오 차트 데이터 ---
    ret_pts, daily_bars, final_pct = _return_series(journal, start_equity or 0.0)
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
  <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start">
    <div style="flex:1;min-width:340px">
      <h2>📈 포트폴리오 추이 (수익률 vs BTC 매수후보유)</h2>
      <div class="card">{charts.line_chart(line_series, width=560)}</div>
    </div>
    <div style="flex:1;min-width:340px">
      <h2>📊 일별 손익 (USDT)</h2>
      <div class="card">{charts.bar_chart(daily_bars, width=560, unit="")}</div>
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
  <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start">
    <div style="flex:2;display:flex;gap:12px;flex-wrap:wrap;min-width:320px">
      {_strength_table("상대강도 1일", alt.get("1d", []))}
      {_strength_table("상대강도 7일", alt.get("7d", []))}
      {_strength_table("상대강도 30일", alt.get("30d", []))}
    </div>
    <div style="flex:1;min-width:300px">
      {_mcap_table(mcap)}
    </div>
  </div>
""" if (alt or mcap) else ""
    macro_section = f"""
  <h2>🌐 BTC vs 나스닥·금 괴리 (시작=0%)</h2>
  <div class="card">{charts.line_chart(macro, y_suffix="%")}</div>
""" if macro else ""

    brief_section = _brief_section(load_market_brief())
    kol_section = _kol_section(load_kol_watch())

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
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:var(--gap); margin:16px 0; }}
  .stat {{ background:var(--surface); border-radius:var(--radius); padding:var(--pad); display:flex; flex-direction:column; gap:6px; }}
  .stat span {{ font-size:12px; color:var(--muted); }} .stat b {{ font-size:20px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ text-align:left; padding:8px 10px; border-bottom:1px solid var(--border); }}
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
  .tkopt {{ padding:6px 8px; border:1px solid var(--border); border-radius:9999px; font-size:12px; text-align:center; cursor:pointer; }}
  .tkopt:hover {{ background:var(--brand); color:#fff; }}
  .tfbtn, .dtfbtn {{ background:transparent; color:var(--muted); border:1px solid var(--border); border-radius:9999px; padding:3px 9px; margin-left:4px; font-size:12px; cursor:pointer; }}
  .tfbtn-active {{ background:var(--brand); color:#fff; border-color:var(--brand); }}
  /* 차트: 세로 리사이즈 가능(모서리 드래그) — 파생 패널은 flex-stretch 로 높이 추종 */
  .mkt-chartcard {{ display:flex; flex-direction:column; }}
  .chartarea {{ margin-top:8px; height:300px; min-height:180px; max-height:720px; resize:vertical; overflow:hidden; }}
  .mkt-derivcard {{ display:flex; flex-direction:column; }}
  #mkt-derivs {{ flex:1; display:flex; flex-direction:column; }}
  .dtile {{ flex:1; display:flex; flex-direction:column; gap:2px; justify-content:center; padding:9px 4px; border-bottom:1px solid var(--border); }}
  .dtile:last-child {{ border-bottom:none; }}
  .dtile b {{ font-size:17px; font-weight:700; }}
  .dlab {{ color:var(--muted-2); font-size:12px; }}
  .dsub {{ color:var(--muted-2); font-size:11px; }}
  .tabs {{ display:flex; gap:6px; margin:18px 0 4px; border-bottom:1px solid var(--border); }}
  .tab {{ background:transparent; color:var(--muted); border:none; border-bottom:2px solid transparent; padding:9px 16px; font-size:14px; font-weight:600; cursor:pointer; }}
  .tab-active {{ color:var(--text); border-bottom-color:var(--brand); }}
</style></head>
<body>
  <h1>🤖 crypto-trader 대시보드</h1>
  <div class="muted">생성 {now_kst}</div>
  {_ticker_strip(tickers or [])}

  <div class="tabs">
    <button class="tab tab-active" data-tab="perf">📊 성과</button>
    <button class="tab" data-tab="market">🌐 시장</button>
    <button class="tab" data-tab="research">📰 리서치</button>
  </div>

  <div class="tabpane" data-pane="perf">
    <div class="grid">
      {equity_row}
      <div class="stat"><span>누적 수익률</span><b style="color:{ret_color}">{head_ret:+.2f}%</b><span class="muted">{btc_cmp}</span></div>
      <div class="stat"><span>총 실현손익 (USDT)</span><b style="color:{pnl_color}">{head_pnl:+,.2f}</b></div>
      <div class="stat"><span>승률</span><b>{st['win_rate']:.1f}%</b></div>
      <div class="stat"><span>손익비 (PF)</span><b>{st['profit_factor']:.2f}</b></div>
      <div class="stat"><span>샤프 (거래)</span><b>{m['sharpe']:.2f}</b></div>
      <div class="stat"><span>소르티노</span><b>{m['sortino']:.2f}</b></div>
      <div class="stat"><span>최대낙폭 (MDD)</span><b style="color:#e23b4a">{m['mdd_pct']:.1f}%</b></div>
      <div class="stat"><span>기대값/거래</span><b>{m['expectancy_pct']:+.2f}%</b></div>
      <div class="stat"><span>손익크기비</span><b>{m['payoff']:.2f}</b></div>
      <div class="stat"><span>청산 거래</span><b>{st['total_trades']} <small style="font-size:12px;color:#94a3b8">(승 {st['wins']}/패 {st['losses']})</small></b></div>
      <div class="stat"><span>열린 포지션</span><b>{st['open_trades']}</b></div>
    </div>
    <div class="muted" style="margin:4px 0 8px">지표는 청산 {m['n']}건 기준 — 거래가 쌓일수록 안정적입니다.</div>
    {chart_section}
    <h2>열린 포지션</h2>
    <table><thead><tr><th>심볼</th><th>방향</th><th>진입가</th><th>손절</th><th>익절</th><th>모드</th></tr></thead>
    <tbody>{rows(journal.open_trades(), False) or "<tr><td colspan=6>없음</td></tr>"}</tbody></table>
    <h2>최근 청산 (최대 20건)</h2>
    <table><thead><tr><th>심볼</th><th>방향</th><th>진입</th><th>청산</th><th>손익</th><th>사유</th></tr></thead>
    <tbody>{rows(journal.closed_trades()[-20:][::-1], True) or "<tr><td colspan=6>없음</td></tr>"}</tbody></table>
  </div>

  <div class="tabpane" data-pane="market" style="display:none">
    <h2>📈 차트 · 파생 지표</h2>
    {_market_view(tickers or [])}
    {strength_section}
    {macro_section}
  </div>

  <div class="tabpane" data-pane="research" style="display:none">
    {brief_section}
    {kol_section}
    {event_section}
  </div>

  <script>
   function _showTab(tab){{
     var found=false;
     document.querySelectorAll('.tab').forEach(function(b){{var on=b.getAttribute('data-tab')===tab;b.classList.toggle('tab-active',on);if(on)found=true;}});
     if(!found)tab='perf';
     document.querySelectorAll('.tab').forEach(function(b){{b.classList.toggle('tab-active',b.getAttribute('data-tab')===tab);}});
     document.querySelectorAll('.tabpane').forEach(function(p){{p.style.display=p.getAttribute('data-pane')===tab?'block':'none';}});
     return tab;}}
   document.addEventListener('click',function(e){{var t=e.target.closest&&e.target.closest('.tab');if(!t)return;
     var tab=_showTab(t.getAttribute('data-tab'));
     try{{localStorage.setItem('ct_tab',tab);}}catch(_e){{}} }});
   // 자동 새로고침 후에도 마지막으로 보던 탭 유지
   (function(){{var saved;try{{saved=localStorage.getItem('ct_tab');}}catch(_e){{}}if(saved)_showTab(saved);}})();
  </script>
</body></html>"""
