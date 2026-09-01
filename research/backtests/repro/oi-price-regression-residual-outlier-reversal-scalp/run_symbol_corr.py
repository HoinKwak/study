"""종목 간 신호(트리거) 상관 — 평시 vs 위기국면(2024-08, 2025-02, 2025-10)."""
import pickle
import sys

import pandas as pd

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiresid")
import common

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

df = results[("resid", "A", True)]
df = df[(df["entry_time"] >= common.IS_START) & (df["entry_time"] <= common.OOS_END)]
df["cal_day"] = df["entry_time"].dt.floor("D")

by_day_sym = df.groupby("cal_day")["symbol"].nunique()
print("=== 동시발화(같은 캘린더일, 여러 종목) 분포 (FULL) ===")
print(by_day_sym.value_counts().sort_index())
print(f"총 고유일수={by_day_sym.shape[0]}, 3종목 이상 동시={  (by_day_sym>=3).sum()}, "
     f"7종목 전부 동시={(by_day_sym==7).sum()}")

CRISIS_WINDOWS = [
    ("2024-08 엔캐리 청산", "2024-08-01", "2024-08-10"),
    ("2025-02 Bybit 해킹", "2025-02-01", "2025-02-10"),
    ("2025-10 청산캐스케이드", "2025-10-01", "2025-10-15"),
]

print("\n=== 위기구간 집중도 ===")
total_n = len(df)
for name, s, e in CRISIS_WINDOWS:
    sub = df[(df["entry_time"] >= pd.Timestamp(s, tz="UTC")) & (df["entry_time"] <= pd.Timestamp(e, tz="UTC"))]
    day_sym = sub.groupby(sub["entry_time"].dt.floor("D"))["symbol"].nunique()
    max_sym_day = day_sym.max() if len(day_sym) else 0
    print(f"  {name} ({s}~{e}): n={len(sub)} ({len(sub)/total_n*100:.1f}% of FULL), "
         f"최대 동시종목수/일={max_sym_day}, sum(R)={sub['r'].sum():+.2f}")

print("\n=== 평시(위기구간 제외) vs 전체 최대동시발화 비교 ===")
mask_crisis = pd.Series(False, index=df.index)
for name, s, e in CRISIS_WINDOWS:
    mask_crisis |= (df["entry_time"] >= pd.Timestamp(s, tz="UTC")) & (df["entry_time"] <= pd.Timestamp(e, tz="UTC"))
quiet = df[~mask_crisis]
qday = quiet.groupby(quiet["entry_time"].dt.floor("D"))["symbol"].nunique()
print(f"평시 고유일={qday.shape[0]}, 3종목+ 동시={ (qday>=3).sum()} ({(qday>=3).sum()/qday.shape[0]*100:.2f}%)")
