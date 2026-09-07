"""동어반복 점검 — 레짐전환 지표와 거래량 z-score/OI ROC 의 상관을 전체구간·트리거 시점
양쪽에서 실측(사전 폐기조건 (e): |r|>0.85 트리거시점 기준이면 재포장 확정).

레짐전환 자체는 이산 이벤트라 연속 상관을 그대로 구할 수 없으므로, 그 대리 연속 지표로
'diff = p_oi2qv - p_qv2oi'(양수일수록 거래대금선행 우세)를 쓰고, 이를 거래량 z-score·OI ROC 와
비교한다. 트리거 시점 상관은 (loose 정의 포함) 실제 진입 신호가 발생한 봉들만 골라 비교한다."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import SYMBOLS
from signals import build_signals
from events import gated_entries
from events_loose import loose_gated_entries

HERE = Path(__file__).resolve().parent


def compute_proxies(sig) -> pd.DataFrame:
    df = sig.df
    qv = df["quote_volume"].astype(float)
    oi = sig.oi.astype(float)
    dqv = sig.dqv
    # 거래량 z-score(60봉 트레일링, shift(1)로 자기 자신 제외)
    mean = dqv.shift(1).rolling(60, min_periods=60).mean()
    std = dqv.shift(1).rolling(60, min_periods=60).std()
    vol_z = (dqv - mean) / std
    # OI ROC(전봉 대비 변화율)
    oi_roc = oi.pct_change()
    diff = sig.p_oi2qv - sig.p_qv2oi  # 양수: 거래대금선행 방향 우세
    return pd.DataFrame({"diff": diff, "vol_z": vol_z, "oi_roc": oi_roc})


def main():
    all_full = []
    trigger_rows = []
    for sym in SYMBOLS:
        sig = build_signals(sym)
        prox = compute_proxies(sig)
        all_full.append(prox)
        ent = gated_entries(sig)
        loose = loose_gated_entries(sig, lookback=3)
        for bar_set, tag in [(ent["signal_bar"].tolist(), "strict"),
                            (loose["signal_bar"].tolist(), "loose")]:
            for b in bar_set:
                if 0 <= b < len(prox):
                    row = prox.iloc[b]
                    trigger_rows.append({"symbol": sym, "tag": tag, **row.to_dict()})

    full_df = pd.concat(all_full, ignore_index=True).dropna()
    full_corr_vol = float(full_df["diff"].corr(full_df["vol_z"]))
    full_corr_oi = float(full_df["diff"].corr(full_df["oi_roc"]))

    trig_df = pd.DataFrame(trigger_rows).dropna()
    out = {"full_period": {"n": int(len(full_df)), "corr_diff_vol_z": full_corr_vol,
                           "corr_diff_oi_roc": full_corr_oi}}
    for tag in ("strict", "loose"):
        sub = trig_df[trig_df["tag"] == tag]
        if len(sub) >= 3:
            out[f"trigger_{tag}"] = {
                "n": int(len(sub)),
                "corr_diff_vol_z": float(sub["diff"].corr(sub["vol_z"])),
                "corr_diff_oi_roc": float(sub["diff"].corr(sub["oi_roc"])),
            }
        else:
            out[f"trigger_{tag}"] = {"n": int(len(sub)), "note": "표본부족(<3)으로 상관 계산 생략"}
    print(json.dumps(out, indent=2))
    (HERE / "out_diag_tautology.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
