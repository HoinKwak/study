"""룩어헤드 점검 — 절단(truncation) 재실행. 주전략 신호 + 대조군(gate_none·simple_alt) 둘 다 확인.

BTC 데이터를 임의 지점(cutoff)에서 잘라 그 전 구간만으로 신호를 재계산했을 때, 절단 전
구간의 신호가 전체데이터 계산과 완전히 일치해야 한다(미래 데이터가 과거 신호에 영향 없음).
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
from common import load_klines_4h
from signals import build_signals
import control_signals as cs

CUTOFF = 4000  # 임의 절단점(약 1.83년 지점, 여유있게 OU/EMA/ATR 워밍업 이후)


def compare_series(full: pd.Series, trunc: pd.Series, name: str) -> tuple[int, int]:
    n = len(trunc)
    common_idx = full.index[:n]
    a = full.loc[common_idx]
    b = trunc
    # 부동소수 비교(0 근접 오차 허용), NaN 은 둘 다 NaN 이어야 일치
    both_nan = a.isna() & b.isna()
    diff = (~both_nan) & (~np.isclose(a.fillna(1e18), b.fillna(1e18), rtol=1e-9, atol=1e-9))
    mismatches = int(diff.sum())
    if mismatches:
        print(f"  [{name}] 불일치 {mismatches}건, 첫 불일치 idx: {a.index[diff][:3].tolist()}")
    else:
        print(f"  [{name}] 완전 일치 (n={n})")
    return mismatches, n


def main():
    df = load_klines_4h("BTCUSDT")
    full_ind = build_signals(df)
    trunc_df = df.iloc[:CUTOFF].copy()
    trunc_ind = build_signals(trunc_df)

    print("=== 주신호(breakout/fade dev, half_life) 절단검증 ===")
    total_mm = 0
    for col in ["dev", "half_life", "raw_breakout_dir", "raw_fade_dir", "ema20", "atr14"]:
        mm, n = compare_series(full_ind[col], trunc_ind[col], col)
        total_mm += mm

    print("=== 대조군(gate_none/simple_alt) 절단검증 ===")
    for mode in ["breakout", "fade"]:
        full_none = (cs.gate_none_breakout(full_ind) if mode == "breakout"
                     else cs.gate_none_fade(full_ind))
        trunc_none = (cs.gate_none_breakout(trunc_ind) if mode == "breakout"
                      else cs.gate_none_fade(trunc_ind))
        mm, n = compare_series(full_none, trunc_none, f"gate_none_{mode}")
        total_mm += mm

        full_alt = (cs.simple_alt_breakout(df, full_ind) if mode == "breakout"
                    else cs.simple_alt_fade(df, full_ind))
        trunc_alt = (cs.simple_alt_breakout(trunc_df, trunc_ind) if mode == "breakout"
                     else cs.simple_alt_fade(trunc_df, trunc_ind))
        mm, n = compare_series(full_alt, trunc_alt, f"simple_alt_{mode}")
        total_mm += mm

    print("총 불일치 건수:", total_mm)
    with open("out_diag_lookahead.txt", "w") as f:
        f.write(f"total_mismatches={total_mm}\ncutoff={CUTOFF}\n")


if __name__ == "__main__":
    main()
