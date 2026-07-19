"""BTC 요일유형(주중/주말) × 시간대(UTC시간, KST 병기)별 강세/횡보/약세 확률.

정보 분석용(매매신호 아님). 시간별(1h) 종가-종가 수익률을 임계값 THR로 3분류:
  강세(bull) r > +THR · 약세(bear) r < -THR · 횡보(side) 그 사이.
버킷(요일유형×시간)마다 P(bull/side/bear)와 표본수 n, 평균수익률을 낸다. n으로 신뢰도 판단.

데이터: scratchpad/futdump100m/BTCUSDT.pkl (바이낸스 선물 15m, 2022~2026).
출력: research/seasonality/btc_hourly.{json,md}.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "scratchpad" / "futdump100m" / "BTCUSDT.pkl"
OUTDIR = REPO / "research" / "seasonality"
THR = 0.001   # ±0.1% 임계값(강세/약세 경계). BTC 1h 변동성 대비 완만한 3분류.


def load_1h() -> pd.DataFrame:
    raw = pd.read_pickle(DATA)
    df = pd.DataFrame(raw, columns=["ts", "open", "high", "low", "close", "volume"])
    df["dt"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    df = df.set_index("dt").sort_index()
    h = df["close"].astype(float).resample("1h").last().dropna()
    out = pd.DataFrame({"close": h})
    out["ret"] = out["close"].pct_change()
    out = out.dropna()
    out["hour"] = out.index.hour                       # UTC 시간(0~23)
    out["dow"] = out.index.dayofweek                   # 0=월 … 6=일
    out["is_weekend"] = out["dow"] >= 5                # 토·일
    out["cls"] = np.where(out["ret"] > THR, "bull",
                          np.where(out["ret"] < -THR, "bear", "side"))
    return out


def _probs(sub: pd.DataFrame) -> dict:
    n = len(sub)
    if n == 0:
        return {"n": 0, "p_bull": None, "p_side": None, "p_bear": None, "mean_ret_bps": None}
    vc = sub["cls"].value_counts()
    return {"n": int(n),
            "p_bull": round(vc.get("bull", 0) / n, 4),
            "p_side": round(vc.get("side", 0) / n, 4),
            "p_bear": round(vc.get("bear", 0) / n, 4),
            "mean_ret_bps": round(sub["ret"].mean() * 1e4, 2)}


def main() -> None:
    df = load_1h()
    span = f"{df.index[0].date()} ~ {df.index[-1].date()}"
    result: dict = {"asset": "BTC", "source": "binance futures 15m→1h",
                    "span": span, "threshold_pct": THR * 100, "total_hours": len(df),
                    "overall": _probs(df), "weekday_weekend": {}, "by_dow": {}}
    # 주중/주말 × 시간
    for wknd, label in [(False, "weekday"), (True, "weekend")]:
        rows = {}
        for hr in range(24):
            rows[hr] = _probs(df[(df["is_weekend"] == wknd) & (df["hour"] == hr)])
        result["weekday_weekend"][label] = rows
    # 요일별 × 시간(보너스)
    for d in range(7):
        rows = {hr: _probs(df[(df["dow"] == d) & (df["hour"] == hr)]) for hr in range(24)}
        result["by_dow"][["월", "화", "수", "목", "금", "토", "일"][d]] = rows

    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "btc_hourly.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))

    # 사람이 읽는 마크다운
    def kst(h): return (h + 9) % 24
    lines = [f"# BTC 요일·시간대별 강세/횡보/약세 확률", "",
             f"> 정보 분석용, **매매신호 아님**. 기간 {span} · 1h 종가수익률 임계 ±{THR*100:.2f}% 3분류 · 표본 {len(df):,}시간.",
             "", f"전체: 강세 {df['cls'].eq('bull').mean()*100:.1f}% · 횡보 {df['cls'].eq('side').mean()*100:.1f}% · 약세 {df['cls'].eq('bear').mean()*100:.1f}%", ""]
    for wknd, label in [(False, "주중(월~금)"), (True, "주말(토·일)")]:
        lines += [f"## {label}", "",
                  "| UTC | KST | 강세% | 횡보% | 약세% | 평균(bps) | n |", "|--:|--:|--:|--:|--:|--:|--:|"]
        for hr in range(24):
            p = _probs(df[(df["is_weekend"] == wknd) & (df["hour"] == hr)])
            lines.append(f"| {hr:02d} | {kst(hr):02d} | {p['p_bull']*100:.1f} | {p['p_side']*100:.1f} | "
                         f"{p['p_bear']*100:.1f} | {p['mean_ret_bps']:+.1f} | {p['n']} |")
        lines.append("")
    # 요약: 강세확률 상·하위 시간대(주중/주말)
    lines += ["## 강세확률 상·하위 시간대", ""]
    for wknd, label in [(False, "주중"), (True, "주말")]:
        cells = [(hr, _probs(df[(df["is_weekend"] == wknd) & (df["hour"] == hr)])) for hr in range(24)]
        cells = [(hr, p) for hr, p in cells if p["n"] > 0]
        top = sorted(cells, key=lambda x: -x[1]["p_bull"])[:3]
        bot = sorted(cells, key=lambda x: x[1]["p_bull"])[:3]
        lines.append(f"- **{label}** 강세↑: " + ", ".join(f"UTC{h:02d}(KST{kst(h):02d}) {p['p_bull']*100:.0f}%" for h, p in top)
                     + " · 강세↓: " + ", ".join(f"UTC{h:02d}(KST{kst(h):02d}) {p['p_bull']*100:.0f}%" for h, p in bot))
    (OUTDIR / "btc_hourly.md").write_text("\n".join(lines) + "\n")
    print(f"저장: {OUTDIR}/btc_hourly.(json|md) · 기간 {span} · {len(df):,}시간")
    print("전체: 강세 %.1f%% 횡보 %.1f%% 약세 %.1f%%" % (
        df["cls"].eq("bull").mean()*100, df["cls"].eq("side").mean()*100, df["cls"].eq("bear").mean()*100))


if __name__ == "__main__":
    main()
