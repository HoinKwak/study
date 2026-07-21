"""KOSPI vs BTC 최근 2년 가격 상관 분석 (정보용, 매매신호 아님).

가설 점검: "코인 수급이 국장(KOSPI)으로 빨려 크립토 하락장이 왔다."
- 레벨(가격) 상관은 둘 다 추세라 착시 → **로그수익률 상관**과 **롤링 상관**으로 본다.
- 상관≠인과: 수급 이동이 하락을 '유발'했는지는 상관으로 증명 불가(전역 위험선호·환율 등 교란).

데이터: Yahoo Finance 일봉 종가(^KS11 KOSPI, BTC-USD, KRW=X 환율 참고). 2년.
출력: research/macro/kospi-btc-correlation.{json,md} + kospi_btc_overlay.svg.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "macro"
_YH = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=2y&interval=1d"


def fetch(symbol: str) -> pd.Series:
    """Yahoo 일봉 종가 → 날짜(UTC date) 인덱스 Series."""
    url = _YH.format(sym=urllib.parse.quote(symbol))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:  # noqa: S310
        d = json.load(r)
    res = d["chart"]["result"][0]
    ts = res["timestamp"]
    cl = res["indicators"]["quote"][0]["close"]
    idx = pd.to_datetime(ts, unit="s", utc=True).date
    s = pd.Series(cl, index=idx, name=symbol).astype(float).dropna()
    s = s[~s.index.duplicated(keep="last")]
    return s


import urllib.parse  # noqa: E402


def main() -> None:
    kospi = fetch("^KS11")
    btc = fetch("BTC-USD")
    try:
        usdkrw = fetch("KRW=X")
    except Exception:  # noqa: BLE001
        usdkrw = None

    # KOSPI 거래일 기준 정렬(내부조인)
    df = pd.DataFrame({"kospi": kospi, "btc": btc}).dropna()
    df = df.sort_index()
    span = f"{df.index[0]} ~ {df.index[-1]}"
    n = len(df)

    # 로그수익률
    r = np.log(df / df.shift(1)).dropna()
    # 주간 수익률(금요일 기준 리샘플)
    dfi = df.copy(); dfi.index = pd.to_datetime(dfi.index)
    wk = np.log(dfi.resample("W-FRI").last() / dfi.resample("W-FRI").last().shift(1)).dropna()

    def corr(a, b):
        # Spearman = 순위의 Pearson (scipy 불필요)
        return {"pearson": round(float(a.corr(b)), 3),
                "spearman": round(float(a.rank().corr(b.rank())), 3)}

    daily_c = corr(r["kospi"], r["btc"])
    weekly_c = corr(wk["kospi"], wk["btc"])

    # 롤링 60일 상관
    roll = r["kospi"].rolling(60).corr(r["btc"]).dropna()
    roll_recent = float(roll.iloc[-1])
    roll_min = float(roll.min()); roll_max = float(roll.max())
    roll_min_date = str(roll.idxmin()); roll_max_date = str(roll.idxmax())
    neg_frac = float((roll < 0).mean())   # 롤링상관이 음(-)이던 기간 비중

    # 반기별(전반/후반) 상관 — 시간에 따른 변화
    half = n // 2
    r1, r2 = r.iloc[:half], r.iloc[half:]
    first_c = round(float(r1["kospi"].corr(r1["btc"])), 3)
    second_c = round(float(r2["kospi"].corr(r2["btc"])), 3)

    # 최근 3·6개월 상관
    def last_days_corr(days):
        rr = r.iloc[-days:]
        return round(float(rr["kospi"].corr(rr["btc"])), 3)
    c_3m, c_6m = last_days_corr(63), last_days_corr(126)

    # 방향 분해: KOSPI↑&BTC↓ (수급 로테이션 정황) 등 4분면 빈도
    up_k = r["kospi"] > 0; up_b = r["btc"] > 0
    quad = {
        "kospi↑_btc↑": round(float((up_k & up_b).mean()), 3),
        "kospi↑_btc↓": round(float((up_k & ~up_b).mean()), 3),
        "kospi↓_btc↑": round(float((~up_k & up_b).mean()), 3),
        "kospi↓_btc↓": round(float((~up_k & ~up_b).mean()), 3),
    }

    # 리드-래그: corr(KOSPI_ret[t], BTC_ret[t+k])
    lead = {}
    for k in range(-5, 6):
        if k >= 0:
            a, b = r["kospi"].iloc[:len(r) - k], r["btc"].iloc[k:]
        else:
            a, b = r["kospi"].iloc[-k:], r["btc"].iloc[:len(r) + k]
        lead[k] = round(float(np.corrcoef(a.values, b.values)[0, 1]), 3)
    best_k = max(lead, key=lambda k: abs(lead[k]))

    # 2년 누적 수익률(정규화)
    ret_kospi = float(df["kospi"].iloc[-1] / df["kospi"].iloc[0] - 1)
    ret_btc = float(df["btc"].iloc[-1] / df["btc"].iloc[0] - 1)
    fx_note = None
    if usdkrw is not None:
        u = usdkrw.reindex(df.index).ffill()
        fx_note = {"usdkrw_start": round(float(u.iloc[0]), 1), "usdkrw_end": round(float(u.iloc[-1]), 1),
                   "usdkrw_chg": round(float(u.iloc[-1] / u.iloc[0] - 1), 3)}

    result = {
        "asset_pair": "KOSPI(^KS11) vs BTC-USD", "span": span, "trading_days": n,
        "source": "Yahoo Finance daily close",
        "cumret_2y": {"kospi": round(ret_kospi, 3), "btc": round(ret_btc, 3)},
        "return_corr": {"daily": daily_c, "weekly": weekly_c},
        "rolling60_corr": {"recent": round(roll_recent, 3), "min": round(roll_min, 3),
                           "min_date": roll_min_date, "max": round(roll_max, 3),
                           "max_date": roll_max_date, "neg_fraction": round(neg_frac, 3)},
        "half_corr": {"first_half": first_c, "second_half": second_c},
        "recent_corr": {"3m": c_3m, "6m": c_6m},
        "sign_quadrants": quad,
        "lead_lag": {"corr_by_lag": lead, "best_lag": best_k,
                     "note": "k>0: KOSPI가 BTC를 k일 선행(양이면 동행 선행)"},
        "fx": fx_note,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "kospi-btc-correlation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))

    # SVG: 정규화 오버레이 + 롤링상관
    _svg(df, roll, OUT / "kospi_btc_overlay.svg")

    # 마크다운
    _md(result, OUT / "kospi-btc-correlation.md")
    print("저장:", OUT / "kospi-btc-correlation.md")
    print(f"기간 {span} · {n}일")
    print(f"2년 누적: KOSPI {ret_kospi*100:+.0f}% · BTC {ret_btc*100:+.0f}%")
    print(f"일간수익률 상관 {daily_c['pearson']} · 주간 {weekly_c['pearson']}")
    print(f"롤링60 상관 최근 {roll_recent:.2f} (범위 {roll_min:.2f}~{roll_max:.2f}, 음(-) 기간 {neg_frac*100:.0f}%)")
    print(f"반기: 전반 {first_c} → 후반 {second_c}")


def _svg(df, roll, path):
    """정규화(시작=100) KOSPI·BTC 오버레이 + 하단 롤링60 상관 미니패널."""
    W, H, m = 900, 460, 50
    pw, ph = W - 2 * m, 240
    kn = df["kospi"] / df["kospi"].iloc[0] * 100
    bn = df["btc"] / df["btc"].iloc[0] * 100
    lo = min(kn.min(), bn.min()); hi = max(kn.max(), bn.max())
    xs = np.linspace(m, m + pw, len(df))

    def yv(v, top, height):
        return top + height - (v - lo) / (hi - lo + 1e-9) * height

    def poly(series, top, height, color):
        pts = " ".join(f"{x:.1f},{yv(v, top, height):.1f}" for x, v in zip(xs, series.values))
        return f'<polyline fill="none" stroke="{color}" stroke-width="1.8" points="{pts}"/>'

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="sans-serif">']
    p.append(f'<rect width="{W}" height="{H}" fill="#0b0e14"/>')
    p.append(f'<text x="{m}" y="24" fill="#e6e6e6" font-size="15">KOSPI vs BTC — 정규화(시작=100), 최근 2년</text>')
    # 상단 오버레이
    p.append(poly(kn, 40, ph, "#e879f9"))   # KOSPI
    p.append(poly(bn, 40, ph, "#f7931a"))   # BTC
    p.append(f'<text x="{m}" y="{40+14}" fill="#e879f9" font-size="12">KOSPI {kn.iloc[-1]:.0f}</text>')
    p.append(f'<text x="{m+90}" y="{40+14}" fill="#f7931a" font-size="12">BTC {bn.iloc[-1]:.0f}</text>')
    # 하단 롤링상관 패널
    ct, chh = 330, 90
    r0 = roll.reindex(df.index).values
    zero = ct + chh - (0 - (-1)) / 2 * chh
    p.append(f'<line x1="{m}" y1="{zero:.0f}" x2="{m+pw}" y2="{zero:.0f}" stroke="#333"/>')
    p.append(f'<text x="{m}" y="{ct-6}" fill="#9aa" font-size="12">롤링 60일 수익률 상관 (−1 ~ +1)</text>')
    pts = []
    for x, v in zip(xs, r0):
        if v == v:  # not nan
            y = ct + chh - (v - (-1)) / 2 * chh
            pts.append(f"{x:.1f},{y:.1f}")
    p.append(f'<polyline fill="none" stroke="#38bdf8" stroke-width="1.6" points="{" ".join(pts)}"/>')
    p.append(f'<text x="{m}" y="{H-14}" fill="#9aa" font-size="11">{df.index[0]}</text>')
    p.append(f'<text x="{m+pw-70}" y="{H-14}" fill="#9aa" font-size="11">{df.index[-1]}</text>')
    p.append("</svg>")
    path.write_text("\n".join(p))


def _md(res, path):
    q = res["sign_quadrants"]; rc = res["rolling60_corr"]
    lines = [
        "# KOSPI vs BTC 가격 상관 분석 (최근 2년)", "",
        f"> 정보 분석용, **매매신호 아님**. 기간 {res['span']} · 거래일 {res['trading_days']} · 출처 {res['source']}.",
        "> 가설 점검: \"코인 수급이 국장으로 빨려 크립토 하락장.\" **상관≠인과** — 상관은 동행/역행을 보여줄 뿐",
        "> 수급 이동이 하락을 유발했는지는 증명 못 함(전역 위험선호·미 금리·환율 등 교란요인).", "",
        "## 2년 누적 수익률", "",
        f"- **KOSPI {res['cumret_2y']['kospi']*100:+.0f}%** vs **BTC {res['cumret_2y']['btc']*100:+.0f}%** "
        "(KOSPI는 KRW, BTC는 USD 기준).",
    ]
    if res.get("fx"):
        f = res["fx"]
        lines.append(f"- 환율 USDKRW {f['usdkrw_start']}→{f['usdkrw_end']} ({f['usdkrw_chg']*100:+.0f}%) — "
                     "BTC를 원화로 보면 이만큼 가산(참고).")
    lines += [
        "", "## 수익률 상관 (레벨 아닌 수익률 — 착시 제거)", "",
        f"- **일간**: Pearson {res['return_corr']['daily']['pearson']} · Spearman {res['return_corr']['daily']['spearman']}",
        f"- **주간**: Pearson {res['return_corr']['weekly']['pearson']} · Spearman {res['return_corr']['weekly']['spearman']}",
        f"- 반기별: 전반 {res['half_corr']['first_half']} → 후반 {res['half_corr']['second_half']}",
        f"- 최근: 3개월 {res['recent_corr']['3m']} · 6개월 {res['recent_corr']['6m']}",
        "", "## 롤링 60일 상관 (시간에 따른 변화)", "",
        f"- 최근값 **{rc['recent']}**, 범위 {rc['min']}({rc['min_date']}) ~ {rc['max']}({rc['max_date']}).",
        f"- 롤링상관이 **음(-)이던 기간 비중 {rc['neg_fraction']*100:.0f}%** — 음이 잦을수록 역행(로테이션 정황).",
        "", "## 방향 4분면 (일간)", "",
        f"- 동반상승 {q['kospi↑_btc↑']*100:.0f}% · 동반하락 {q['kospi↓_btc↓']*100:.0f}% · "
        f"**KOSPI↑·BTC↓ {q['kospi↑_btc↓']*100:.0f}%** · KOSPI↓·BTC↑ {q['kospi↓_btc↑']*100:.0f}%",
        f"- 'KOSPI↑·BTC↓'가 동반상승보다 크면 역행(수급 로테이션 가설에 부합하는 정황).",
        "", "## 리드-래그", "",
        f"- 최대 상관 시차 k={res['lead_lag']['best_lag']}일 ({res['lead_lag']['corr_by_lag'][str(res['lead_lag']['best_lag'])] if isinstance(list(res['lead_lag']['corr_by_lag'].keys())[0],str) else res['lead_lag']['corr_by_lag'][res['lead_lag']['best_lag']]}). "
        "k>0=KOSPI 선행. 절대값 작으면 뚜렷한 선행관계 없음.",
        "", "## 해석 (정직)", "",
        "- 위 수치로 **동행/역행의 정도와 시간 변화**를 판단하되, '수급이 국장으로 빨려 하락'이라는 인과는",
        "  이 분석만으로 확정 못 한다. 더 직접적 검증은 **김치프리미엄**(한국 BTC가 글로벌 대비 할인이면 한국",
        "  수급 이탈 정황)·한국 거래소 거래대금·스테이블 유출입인데, 데이터 확보가 어려워 여기선 제외.",
        "- 차트: `kospi_btc_overlay.svg`(정규화 오버레이 + 롤링60 상관).",
    ]
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
