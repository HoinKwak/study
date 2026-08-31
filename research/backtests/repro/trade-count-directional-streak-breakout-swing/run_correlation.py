"""동어반복 점검: streak_up 과 거래대금z/ROC/ATR 상관 — 전체구간 vs 트리거시점 한정, pandas.corr() 사용."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import common

print(f"{'symbol':10s} {'r_qv_full':>10s} {'r_qv_trig':>10s} {'r_roc_full':>10s} {'r_roc_trig':>10s} "
     f"{'r_atr_full':>10s} {'r_atr_trig':>10s}  trig_n")
for sym in common.SYMBOLS:
    sig = common.build_signals(sym)
    streak_up = pd.Series(sig.streak_up, index=sig.df.index)
    qv = sig.quote_volume
    qv_z = (qv - qv.rolling(60).mean()) / qv.rolling(60).std()
    roc = sig.roc
    atr_norm = sig.atr14 / sig.df["close"]  # 정규화 변동성

    d = pd.DataFrame({"streak_up": streak_up, "qv_z": qv_z, "roc": roc, "atr_norm": atr_norm}).dropna()
    r_qv_full = d["streak_up"].corr(d["qv_z"])
    r_roc_full = d["streak_up"].corr(d["roc"])
    r_atr_full = d["streak_up"].corr(d["atr_norm"])

    # 트리거 시점 한정: streak_up>=5 인 봉만 (실제 게이트가 발화하는 시점)
    trig = d[d["streak_up"] >= 5]
    if len(trig) >= 3:
        r_qv_trig = trig["streak_up"].corr(trig["qv_z"])
        r_roc_trig = trig["streak_up"].corr(trig["roc"])
        r_atr_trig = trig["streak_up"].corr(trig["atr_norm"])
    else:
        r_qv_trig = r_roc_trig = r_atr_trig = float("nan")

    print(f"{sym:10s} {r_qv_full:>10.3f} {r_qv_trig:>10.3f} {r_roc_full:>10.3f} {r_roc_trig:>10.3f} "
         f"{r_atr_full:>10.3f} {r_atr_trig:>10.3f}  {len(trig)}")

print("\n(참고) streak_up 은 정수 카운터라 트리거 시점(streak_up>=5)에서는 값이 5~7 사이로 좁게")
print("분포해 트리거 시점 상관은 표본이 얇고(n=7~63) 분산이 작아 해석에 주의가 필요함을 명시.")
