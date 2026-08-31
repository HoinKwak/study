"""count(t) 방향(상승/하락) lag-1 자기상관 + 실측 스트릭 길이 분포 vs 이론적 이항 기저율(0.5^n*2)."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import common

print("=== count 원시값 lag-1 자기상관 + up/down 방향(이진) lag-1 자기상관 ===")
for sym in common.SYMBOLS:
    sig = common.build_signals(sym)
    cnt = pd.Series(sig.count)
    raw_ac1 = cnt.autocorr(1)
    up = (cnt.diff() > 0).astype(float)
    up[cnt.diff() == 0] = np.nan  # 동률은 제외
    up_ac1 = up.dropna().autocorr(1)
    print(f"{sym}: count_raw_lag1_autocorr={raw_ac1:.4f}  up_binary_lag1_autocorr={up_ac1:.4f}")

print("\n=== 실측 스트릭 길이(>=n) 발생률 vs 이론적 이항 기저율(0.5^n) ===")
print(f"{'n':>3s} {'theory':>10s}", end="")
for sym in common.SYMBOLS:
    print(f" {sym[:3]:>10s}", end="")
print()
for n in range(1, 9):
    theory = 0.5 ** n
    row = f"{n:>3d} {theory:>10.4f}"
    for sym in common.SYMBOLS:
        sig = common.build_signals(sym)
        su_ = sig.streak_up
        valid = np.isfinite(su_)
        rate = (su_[valid] >= n).mean()
        row += f" {rate:>10.4f}"
    print(row)
