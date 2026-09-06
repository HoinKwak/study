"""사전 폐기조건 (e) — 게이트 없는 순수 EMA20/50 눌림목 대조군 대비 부가가치 부트스트랩.
+ ADX(4h,14) 게이트 대조군(사전 폐기조건 (b), |r|<0.6 확인됐으나 완전성 위해 병행)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import pf_r, t_stat, split_is_oos
from events import build_universe
from engine import run_variant, trades_to_df
from signals import build_btc_price_regime


def bootstrap_diff(a: np.ndarray, b: np.ndarray, n_boot: int = 2000, seed: int = 42) -> dict:
    """a,b: 두 변형의 OOS net_R 배열(길이가 다를 수 있음 — 각자 리샘플). 평균(R) 차이의 부트스트랩."""
    rng = np.random.default_rng(seed)
    diffs = np.empty(n_boot)
    for i in range(n_boot):
        sa = rng.choice(a, size=len(a), replace=True)
        sb = rng.choice(b, size=len(b), replace=True)
        diffs[i] = sa.mean() - sb.mean()
    pct_gt0 = float((diffs > 0).mean() * 100)
    return {"mean_diff": float(diffs.mean()), "pct_a_gt_b": pct_gt0,
            "ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))]}


def main() -> dict:
    uni = build_universe()
    base = trades_to_df(run_variant(uni))
    _, base_oos, _ = split_is_oos(base)

    nogate = trades_to_df(run_variant(uni, no_gate=True))
    _, nogate_oos, _ = split_is_oos(nogate)

    # ADX 게이트 대조군: BTC ADX(4h,14) 상위 백분위(<=30퍼센타일, ApEn 저값과 유사 발생률 맞춤)
    # 를 apen_pctile 대신 사용 — "저ApEn=규칙적"의 대안으로 "저ADX=무추세"가 아니라 스펙 취지상
    # ApEn 저값(규칙적 변화)과 개념적으로 가장 가까운 대조는 "고ADX=추세뚜렷"이므로 ADX 상위
    # 백분위를 게이트로 사용(추세 강도 자체가 만드는 재포장 여부 점검).
    btc_reg = build_btc_price_regime()
    # ⚠️룩어헤드 수정(리뷰어 감사 2026-09-06): 전체 구간을 한 번에 rank하면 각 시점이
    #   미래 데이터까지 포함한 백분위를 쓰게 된다(ApEn 쪽은 causal 트레일링 백분위인데
    #   이 대조군만 전체구간 rank였다). causal 확장윈도우로 교체 — 리뷰어 재실행에서
    #   게이트 발화 일치율 98.9%·PF/t 거의 동일(1.256/1.386 vs 원본 1.265/1.429)로
    #   실질 영향은 없었으나 코드 위생상 수정한다.
    adx_pctile = btc_reg["adx"].expanding().rank(pct=True) * 100
    adx_gate = (adx_pctile >= 70)  # 발생률 30%대 맞춤(저ApEn 게이트와 유사 발화율)
    gate_override = {sym: adx_gate for sym in uni["universe"]}
    adxgate = trades_to_df(run_variant(uni, gate_override=gate_override))
    _, adxgate_oos, _ = split_is_oos(adxgate)

    out = {
        "base_oos": {"n": len(base_oos), "pf_net": pf_r(base_oos["net_R"]),
                     "t_net": t_stat(base_oos["net_R"])},
        "nogate_oos": {"n": len(nogate_oos), "pf_net": pf_r(nogate_oos["net_R"]),
                       "t_net": t_stat(nogate_oos["net_R"])},
        "adxgate_oos": {"n": len(adxgate_oos), "pf_net": pf_r(adxgate_oos["net_R"]),
                        "t_net": t_stat(adxgate_oos["net_R"])},
        "bootstrap_base_vs_nogate": bootstrap_diff(base_oos["net_R"].to_numpy(),
                                                    nogate_oos["net_R"].to_numpy()),
        "bootstrap_base_vs_adxgate": bootstrap_diff(base_oos["net_R"].to_numpy(),
                                                     adxgate_oos["net_R"].to_numpy()),
    }
    print(json.dumps(out, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
