"""스카우트 실측(BTC 2026-06-01~07-31, 삼중 동조 rising-edge 1건) 재현 시도.

스카우트는 1h 해상도에서 p1h/p4h/p1d 를 전부 1h 그리드에 정렬해 rising edge 를 봤을 가능성이
있다(우리 엔진은 4h 그리드에서 진입을 판단하므로 표본 빈도가 다를 수 있음) — 이 스크립트는 두 방식
모두로 확인한다.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import numpy as np
import pandas as pd

TH = 60.0
sym = "BTCUSDT"
sig = common.build_signals(sym)
h4 = sig.h4
h1 = sig.h1

start = pd.Timestamp("2026-06-01", tz="UTC")
end = pd.Timestamp("2026-07-31 23:59:59", tz="UTC")

# --- 방식 A: 우리 엔진(4h 그리드에서 판단) ---
close4h = h4.index + pd.Timedelta(hours=4)
mask4 = (sig.p1h_at4h >= TH) & (sig.p4h_at4h >= TH) & (sig.p1d_at4h >= TH)
mask4_s = pd.Series(mask4, index=h4.index)
rising4 = mask4_s & ~mask4_s.shift(1).fillna(False).astype(bool)
sel = (h4.index >= start) & (h4.index <= end)
print("A) 4h 그리드 rising-edge in window:", int(rising4[sel].sum()),
      "occupancy:", round(float(mask4_s[sel].mean()) * 100, 2), "%")

# --- 방식 B: 1h 그리드(각 1h 봉마다 p1h는 자기 값, p4h/p1d 는 asof 매핑해 1h 마다 평가) ---
p1h_full = pd.Series(common.rolling_percentile_rank(
    (common.ind.atr(h1, 14) / h1["close"]).to_numpy(float), 168), index=h1.index)
p4h_ts = h4.index + pd.Timedelta(hours=4)
p4h_at1h = common.map_asof_available(pd.DatetimeIndex(h1.index), pd.Series(sig.p4h_at4h, index=h4.index), pd.Timedelta(0))
p1d_at1h = common.map_asof_available(pd.DatetimeIndex(h1.index), pd.Series(sig.p1d_at4h, index=h4.index), pd.Timedelta(0))
mask1 = (p1h_full.to_numpy(float) >= TH) & (p4h_at1h >= TH) & (p1d_at1h >= TH)
mask1_s = pd.Series(mask1, index=h1.index)
rising1 = mask1_s & ~mask1_s.shift(1).fillna(False).astype(bool)
sel1 = (h1.index >= start) & (h1.index <= end)
print("B) 1h 그리드 rising-edge in window:", int(rising1[sel1].sum()),
      "occupancy:", round(float(mask1_s[sel1].mean()) * 100, 2), "%",
      "n_bars:", int(sel1.sum()))

print("\n개별 스케일 점유율(1h 그리드, 해당 윈도우):")
print("p1h>=60:", round(float((p1h_full[sel1] >= TH).mean()) * 100, 2), "%")
# ⚠️2026-09-01 리뷰어 적발: 괄호 위치 오류로 TypeError가 났다
#   (float(...)를 .mean() 바깥에 씌워 Series에 float()를 적용). 인용 수치는 그 전에
#   출력·확정돼 결론에는 영향이 없었으나 재실행이 끝까지 완주하도록 고친다.
print("p4h>=60:", round(float((p4h_at1h[sel1] >= TH).mean()) * 100, 2), "%")
print("p1d>=60:", round(float((p1d_at1h[sel1] >= TH)).mean() * 100, 2), "%")
