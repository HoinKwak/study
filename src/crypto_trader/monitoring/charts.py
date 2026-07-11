"""의존성 없는 인라인 SVG 차트 — 대시보드용 (외부 JS/CDN 불필요).

라이브러리 없이 순수 SVG 문자열을 만들어 HTML 에 그대로 삽입한다.
line_chart(누적수익률·BTC 비교), bar_chart(일별 손익)를 제공한다.
"""
from __future__ import annotations

import html
from datetime import datetime, timedelta, timezone

_KST = timezone(timedelta(hours=9))


def _date_label(epoch: float) -> str:
    try:
        return datetime.fromtimestamp(epoch, _KST).strftime("%m-%d")
    except (ValueError, OSError, OverflowError):
        return ""

# Revolut 영감 다크 팔레트 (트루블랙 배경)
_AXIS = "rgba(255,255,255,0.20)"
_TEXT = "#8d969e"
_GRID = "rgba(255,255,255,0.06)"
_POS = "#16a34a"
_NEG = "#e23b4a"


def _empty(msg: str = "데이터 없음") -> str:
    return f"<div style='color:{_TEXT};padding:24px;text-align:center'>{html.escape(msg)}</div>"


def line_chart(series: list[dict], width: int = 720, height: int = 260,
               pad: int = 40, y_suffix: str = "%", x_dates: bool = True) -> str:
    """복수 시계열 라인차트.

    series: [{'label': str, 'color': str, 'points': [(x, y), ...]}]  (x 동일 도메인)
    x_dates=True 이면 x 값을 epoch초로 보고 하단에 날짜(KST MM-DD) 축을 표시.
    """
    pts = [p for s in series for p in s.get("points", [])]
    if len(pts) < 2:
        return _empty()
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys + [0.0]), max(ys + [0.0])
    if xmax == xmin:
        xmax = xmin + 1
    if ymax == ymin:
        ymax = ymin + 1
    yr = ymax - ymin
    bpad = pad + 16 if x_dates else pad   # 날짜축 공간

    def sx(x: float) -> float:
        return pad + (x - xmin) / (xmax - xmin) * (width - 2 * pad)

    def sy(y: float) -> float:
        return height - bpad - (y - ymin) / yr * (height - bpad - pad)

    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" '
             f'style="max-width:{width}px" xmlns="http://www.w3.org/2000/svg">']
    # 가로 그리드 + y 라벨 (5분할)
    for i in range(5):
        yv = ymin + yr * i / 4
        y = sy(yv)
        parts.append(f'<line x1="{pad}" y1="{y:.1f}" x2="{width - pad}" y2="{y:.1f}" '
                     f'stroke="{_GRID}" stroke-width="1"/>')
        parts.append(f'<text x="6" y="{y + 4:.1f}" fill="{_TEXT}" font-size="11">'
                     f'{yv:+.1f}{y_suffix}</text>')
    # 0 기준선 강조
    if ymin < 0 < ymax:
        y0 = sy(0.0)
        parts.append(f'<line x1="{pad}" y1="{y0:.1f}" x2="{width - pad}" y2="{y0:.1f}" '
                     f'stroke="{_AXIS}" stroke-width="1.5" stroke-dasharray="3 3"/>')
    # 시리즈
    for s in series:
        p = s.get("points", [])
        if len(p) < 2:
            continue
        d = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in p)
        parts.append(f'<polyline points="{d}" fill="none" '
                     f'stroke="{s["color"]}" stroke-width="2"/>')
    # x축 날짜 라벨 (KST) — 5등분
    if x_dates:
        for k in range(5):
            xv = xmin + (xmax - xmin) * k / 4
            anchor = "start" if k == 0 else ("end" if k == 4 else "middle")
            parts.append(
                f'<text x="{sx(xv):.1f}" y="{height - 4}" fill="{_TEXT}" font-size="10" '
                f'text-anchor="{anchor}">{_date_label(xv)}</text>')
    # 범례 (CJK 글자폭 반영해 겹침 방지)
    lx = pad + 6
    for s in series:
        parts.append(f'<rect x="{lx:.0f}" y="10" width="10" height="10" fill="{s["color"]}"/>')
        parts.append(f'<text x="{lx + 15:.0f}" y="19" fill="{_TEXT}" font-size="12">'
                     f'{html.escape(s["label"])}</text>')
        lx += 15 + _label_width(s["label"]) + 22
    parts.append("</svg>")
    return "".join(parts)


def sparkline(closes: list[float], width: int = 130, height: int = 36,
              color: str = "#6c72ff") -> str:
    """축·라벨 없는 미니 추세선(가격 티커용)."""
    ys = [c for c in (closes or []) if c is not None]
    if len(ys) < 2:
        return ""
    ymin, ymax = min(ys), max(ys)
    if ymax == ymin:
        ymax = ymin + 1
    n = len(ys)
    pts = " ".join(
        f"{i / (n - 1) * (width - 2) + 1:.1f},"
        f"{height - 2 - (v - ymin) / (ymax - ymin) * (height - 4):.1f}"
        for i, v in enumerate(ys))
    return (f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'xmlns="http://www.w3.org/2000/svg"><polyline points="{pts}" fill="none" '
            f'stroke="{color}" stroke-width="1.5"/></svg>')


def _label_width(text: str) -> float:
    """대략적 글자폭(px) — 한글/CJK 는 넓게 잡아 범례 겹침 방지."""
    return sum(14.0 if ord(c) > 0x2E00 else 7.0 for c in text)


def bar_chart(bars: list[tuple[str, float]], width: int = 720, height: int = 200,
              pad: int = 40, unit: str = "") -> str:
    """일별 손익 등 막대차트. bars: [(label, value)]. 양수=녹색, 음수=적색."""
    if not bars:
        return _empty()
    vals = [v for _, v in bars]
    vmax = max([abs(v) for v in vals] + [1e-9])
    n = len(bars)
    bw = (width - 2 * pad) / n
    midy = height - pad - (0 - (-vmax)) / (2 * vmax) * (height - 2 * pad)  # 0 위치(중앙)
    zero_y = pad + (height - 2 * pad) / 2

    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" '
             f'style="max-width:{width}px" xmlns="http://www.w3.org/2000/svg">']
    parts.append(f'<line x1="{pad}" y1="{zero_y:.1f}" x2="{width - pad}" y2="{zero_y:.1f}" '
                 f'stroke="{_AXIS}" stroke-width="1"/>')
    half = (height - 2 * pad) / 2
    show_val = n <= 15   # 막대 적을 때만 값 라벨(겹침 방지)
    for i, (label, v) in enumerate(bars):
        x = pad + i * bw + bw * 0.15
        h = abs(v) / vmax * half
        y = zero_y - h if v >= 0 else zero_y
        color = _POS if v >= 0 else _NEG
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw * 0.7:.1f}" '
                     f'height="{max(h, 0.5):.1f}" fill="{color}"/>')
        if show_val:
            vy = (y - 4) if v >= 0 else (y + h + 12)
            parts.append(f'<text x="{x + bw * 0.35:.1f}" y="{vy:.1f}" fill="{color}" '
                         f'font-size="11" text-anchor="middle">{v:+.1f}</text>')
    # x 라벨 (양끝 + 중앙만 — 겹침 방지)
    idxs = {0, n - 1, n // 2}
    for i in idxs:
        if 0 <= i < n:
            lx = pad + i * bw + bw * 0.5
            parts.append(f'<text x="{lx:.1f}" y="{height - 12}" fill="{_TEXT}" '
                         f'font-size="11" text-anchor="middle">{html.escape(bars[i][0])}</text>')
    parts.append(f'<text x="6" y="{pad}" fill="{_TEXT}" font-size="11">+{vmax:.0f}{unit}</text>')
    parts.append(f'<text x="6" y="{height - pad}" fill="{_TEXT}" font-size="11">-{vmax:.0f}{unit}</text>')
    parts.append("</svg>")
    return "".join(parts)
