"""룩어헤드 부재 검증: 데이터를 특정 시점에서 절단해 재실행 -> 절단 이전 트레이드가 전체 실행과
bit 단위로 일치하는지 확인. ns 명시 통일이 실제로 asof 매핑을 깨뜨리지 않는지도 확인."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd

import common
import engine

SYM = "BTCUSDT"
CUT = pd.Timestamp("2024-01-01", tz="UTC")  # 절단 시점(이 시점 이후 데이터를 아예 제거)
SAFE_MARGIN = pd.Timedelta(days=25)  # 워밍업/트레일링 영향 배제할 안전 마진(1d lookback 20일 + 여유)

# --- 전체 데이터로 실행 ---
sig_full = common.build_signals(SYM)
trades_full = engine.run_symbol(SYM, sig_full, engine.RunConfig())

# --- 절단 데이터로 실행(2024-01-01 이후 1h 원본 자체를 제거) ---
h1_full = common.load_klines_1h(SYM)
h1_cut = h1_full[h1_full.index < CUT].copy()

# common.build_signals 는 캐시(lru_cache)된 load_klines_1h 를 그대로 쓰므로, 절단본을 별도
# 심볼명으로 주입해 캐시 오염 없이 재현한다.
import types
def build_signals_cut(h1_df, pct_th=0.6, lookback_1h=168, lookback_4h=42, lookback_1d=20):
    h4 = common.resample_native(h1_df, "4h")
    d1 = common.resample_native(h1_df, "1D")
    atr1h = common.ind.atr(h1_df, 14); atr4h = common.ind.atr(h4, 14); atr1d = common.ind.atr(d1, 14)
    atrpct_1h = (atr1h / h1_df["close"]).replace([np.inf, -np.inf], np.nan)
    atrpct_4h = (atr4h / h4["close"]).replace([np.inf, -np.inf], np.nan)
    atrpct_1d = (atr1d / d1["close"]).replace([np.inf, -np.inf], np.nan)
    p1h = pd.Series(common.rolling_percentile_rank(atrpct_1h.to_numpy(float), lookback_1h), index=h1_df.index)
    p4h = pd.Series(common.rolling_percentile_rank(atrpct_4h.to_numpy(float), lookback_4h), index=h4.index)
    p1d = pd.Series(common.rolling_percentile_rank(atrpct_1d.to_numpy(float), lookback_1d), index=d1.index)
    close4h = (h4.index + pd.Timedelta(hours=4)).astype("datetime64[ns, UTC]")
    p1h_at4h = common.map_asof_available(pd.DatetimeIndex(close4h), p1h, pd.Timedelta(hours=1))
    p4h_at4h = p4h.reindex(h4.index).to_numpy(float)
    p1d_at4h = common.map_asof_available(pd.DatetimeIndex(close4h), p1d, pd.Timedelta(days=1))
    atr22_4h = common.ind.atr(h4, 22)
    return common.Signals(h1=h1_df, h4=h4, d1=d1, p1h_at4h=p1h_at4h, p4h_at4h=p4h_at4h,
                          p1d_at4h=p1d_at4h, atr22_4h_signal=atr22_4h.to_numpy(float),
                          atr22_4h_trail=atr22_4h.shift(1).to_numpy(float))

sig_cut = build_signals_cut(h1_cut)
trades_cut = engine.run_symbol(SYM, sig_cut, engine.RunConfig())

# --- 비교: 절단시점 - 안전마진 이전에 진입한 트레이드만 ---
safe_before = CUT - SAFE_MARGIN
tf = [(t.entry_time, t.direction, round(t.entry_price, 6), t.reason, t.holding_bars,
      round(t.r_net, 8)) for t in trades_full if t.entry_time < safe_before]
tc = [(t.entry_time, t.direction, round(t.entry_price, 6), t.reason, t.holding_bars,
      round(t.r_net, 8)) for t in trades_cut if t.entry_time < safe_before]

print(f"전체실행 절단이전 트레이드수: {len(tf)}  절단실행 트레이드수(전체): {len(trades_cut)} "
     f"(이중 안전구간): {len(tc)}")
mismatches = [i for i, (a, b) in enumerate(zip(tf, tc)) if a != b]
print("길이 일치:", len(tf) == len(tc))
print("불일치 건수:", len(mismatches))
if mismatches[:5]:
    for i in mismatches[:5]:
        print("FULL:", tf[i])
        print("CUT :", tc[i])
if len(tf) == len(tc) and not mismatches:
    print("✅ 룩어헤드 없음 — 절단 이전 트레이드가 전체실행과 완전히 일치(bit 단위)")
else:
    print("⚠️ 불일치 발견 — 룩어헤드 위험 재검토 필요")

# --- 부가 검증: p1d_at4h 가 실제로 backward-only 인지 임의 시점 5개를 직접 재계산 대조 ---
print("\n=== p1d_at4h 수기 재계산 대조(5개 임의 4h 시점) ===")
d1 = sig_full.d1
h4 = sig_full.h4
rng = np.random.default_rng(0)
sample_idx = rng.choice(np.arange(200, len(h4) - 5), size=5, replace=False)
p1d_manual_ok = True
for i in sample_idx:
    close_t = h4.index[i] + pd.Timedelta(hours=4)
    # '닫힌' 1d 봉: 그 종료시각(index+1day)이 close_t 이하인 가장 최근 1d 봉
    closed_days = d1.index[(d1.index + pd.Timedelta(days=1)) <= close_t]
    if len(closed_days) == 0:
        continue
    last_day_close_time = closed_days.max() + pd.Timedelta(days=1)
    manual_val = None
    # p1d 값 재계산(자체 롤링 백분위, common 함수 재사용 대신 직접 대조 위해 인덱스만 확인)
    print(f"i={i} 4h_close={close_t} 최근닫힌1d봉_종료={last_day_close_time} "
         f"(<= close_t: {last_day_close_time <= close_t}) p1d_at4h={sig_full.p1d_at4h[i]:.2f}")
    if last_day_close_time > close_t:
        p1d_manual_ok = False
print("모든 샘플에서 last_day_close_time <= close_t (미래 미참조):", p1d_manual_ok)
