"""최우선 점검 — ApEn(펀딩ΔF)이 "이미 진행 중인 추세"의 증상(동어반복)인지.

BTC ADX(4h,14)·EMA괴리율(추세강도 프록시)·실현변동성(20봉)·펀딩절대수준·펀딩변화stdev 와
ApEn(raw)·apen_pctile 의 상관을 ①전체구간 ②트리거 시점(게이트 활성, apen_pctile<=30) 한정
둘 다 pandas.corr()(pairwise) 로 계산. 사전 폐기조건 (b): |r|>=0.6 이면 대조군(ADX게이트) 필수,
구분 불가면 재포장으로 폐기.

병기: 펀딩레이트 CUSUM 체인지포인트 스펙과의 상관(전체구간+트리거시점) — 동어반복 점검 항목.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pandas as pd

from signals import build_btc_apen, build_btc_price_regime

CUSUM_DIR = Path(__file__).resolve().parents[1] / "funding-rate-cusum-changepoint-regime-swing"


def _load_cusum_events_module():
    """모듈명이 우리 events.py 와 겹치므로 파일 경로로 직접 로드(sys.modules 캐시 충돌 회피)."""
    spec = importlib.util.spec_from_file_location("cusum_events_mod", CUSUM_DIR / "events.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def map_bar_to_settlement(bar_series: pd.Series, settlement_index: pd.DatetimeIndex) -> pd.Series:
    """봉(4h) 인덱스 시리즈를 정산시각 그리드에 backward asof 매핑."""
    s = bar_series.dropna().sort_index()
    left = pd.DataFrame({"t": settlement_index})
    right = pd.DataFrame({"t": s.index, "v": s.values})
    out = pd.merge_asof(left, right, on="t", direction="backward")
    out = out.set_index("t")["v"]
    out.index.name = None
    return out


def main() -> dict:
    apen_d = build_btc_apen()
    reg = build_btc_price_regime()

    idx = apen_d["apen"].index
    adx_settle = map_bar_to_settlement(reg["adx"], idx)
    slope_settle = map_bar_to_settlement(reg["ema_slope"], idx)
    rv_settle = map_bar_to_settlement(reg["rv20"], idx)
    funding_abs_level = apen_d["funding_8h"]["rate"].abs().rolling(30).mean()
    funding_chg_std = apen_d["delta"].rolling(30).std()

    df = pd.DataFrame({
        "apen": apen_d["apen"], "apen_pctile": apen_d["apen_pctile"],
        "adx": adx_settle, "ema_slope": slope_settle, "rv20": rv_settle,
        "funding_abs_level": funding_abs_level, "funding_chg_std": funding_chg_std,
    }, index=idx)

    full_corr = {}
    trig_corr = {}
    trig_mask = df["apen_pctile"] <= 30
    for col in ["adx", "ema_slope", "rv20", "funding_abs_level", "funding_chg_std"]:
        full_corr[col] = {
            "apen_vs": df["apen"].corr(df[col]),
            "apen_pctile_vs": df["apen_pctile"].corr(df[col]),
        }
        sub = df[trig_mask]
        trig_corr[col] = {
            "apen_vs": sub["apen"].corr(sub[col]),
            "apen_pctile_vs": sub["apen_pctile"].corr(sub[col]),
        }

    # CUSUM 비교(펀딩ΔF ApEn vs 펀딩레벨 CUSUM 체인지포인트) — CUSUM 스펙 repro의 events.py 재사용
    cusum_mod = _load_cusum_events_module()
    cusum_events, cusum_diag = cusum_mod.detect_events(
        apen_d["funding_8h"].assign(interval_hours=8), baseline_window=60, k=0.5, h=4.0)
    cusum_e = cusum_diag["e"].reindex(idx)
    full_corr["cusum_e"] = {
        "apen_vs": df["apen"].corr(cusum_e), "apen_pctile_vs": df["apen_pctile"].corr(cusum_e)}
    sub_e = cusum_e[trig_mask]
    trig_corr["cusum_e"] = {
        "apen_vs": df.loc[trig_mask, "apen"].corr(sub_e),
        "apen_pctile_vs": df.loc[trig_mask, "apen_pctile"].corr(sub_e)}
    n_cusum_events_during_gate = 0
    if len(cusum_events):
        gate_times = set(idx[trig_mask.to_numpy()])
        n_cusum_events_during_gate = cusum_events["event_time"].isin(gate_times).sum()

    out = {
        "n_settlements": int(len(df)), "n_trigger": int(trig_mask.sum()),
        "full_corr": full_corr, "trig_corr": trig_corr,
        "n_cusum_events": int(len(cusum_events)),
        "n_cusum_events_during_gate": int(n_cusum_events_during_gate),
    }
    print(json.dumps(out, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
