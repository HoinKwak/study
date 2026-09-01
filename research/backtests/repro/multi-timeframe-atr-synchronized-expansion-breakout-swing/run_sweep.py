"""파라미터 민감도 스윕: pct_th, lookback_1h/4h/1d, atr_mult_tp/sl 각각 base 대비 단독 변경."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su

t0 = time.time()

variants = []
# pct_th 스윕 (신호 재계산 불요 -> 캐시된 기본 lookback 시그널 재사용)
base_sig = engine.load_all_signals()
for th in [50.0, 55.0, 60.0, 65.0, 70.0]:
    cfg = engine.RunConfig(pct_th=th)
    trades = engine.run_all(base_sig, cfg)
    df = su.trades_df([t for lst in trades.values() for t in lst])
    _is, oos, _full = su.split_is_oos(df)
    variants.append((f"pct_th={th}", su.summary(oos, f"pct_th={th}")))

# atr_mult_sl / atr_mult_tp 스윕 (신호 재계산 불요)
for sl in [1.0, 1.5, 2.0]:
    cfg = engine.RunConfig(atr_mult_sl=sl)
    trades = engine.run_all(base_sig, cfg)
    df = su.trades_df([t for lst in trades.values() for t in lst])
    _is, oos, _full = su.split_is_oos(df)
    variants.append((f"atr_mult_sl={sl}", su.summary(oos, f"atr_mult_sl={sl}")))

for tp in [2.5, 3.5, 4.5]:
    cfg = engine.RunConfig(atr_mult_tp=tp)
    trades = engine.run_all(base_sig, cfg)
    df = su.trades_df([t for lst in trades.values() for t in lst])
    _is, oos, _full = su.split_is_oos(df)
    variants.append((f"atr_mult_tp={tp}", su.summary(oos, f"atr_mult_tp={tp}")))

for te in [10, 15, 20]:
    cfg = engine.RunConfig(time_exit_bars=te)
    trades = engine.run_all(base_sig, cfg)
    df = su.trades_df([t for lst in trades.values() for t in lst])
    _is, oos, _full = su.split_is_oos(df)
    variants.append((f"time_exit_bars={te}", su.summary(oos, f"time_exit_bars={te}")))

# lookback 스윕 (신호 재계산 필요)
for lb1h in [120, 168, 240]:
    sig = engine.load_all_signals(lookback_1h=lb1h)
    cfg = engine.RunConfig()
    trades = engine.run_all(sig, cfg)
    df = su.trades_df([t for lst in trades.values() for t in lst])
    _is, oos, _full = su.split_is_oos(df)
    variants.append((f"lookback_1h={lb1h}", su.summary(oos, f"lookback_1h={lb1h}")))

for lb4h in [30, 42, 60]:
    sig = engine.load_all_signals(lookback_4h=lb4h)
    cfg = engine.RunConfig()
    trades = engine.run_all(sig, cfg)
    df = su.trades_df([t for lst in trades.values() for t in lst])
    _is, oos, _full = su.split_is_oos(df)
    variants.append((f"lookback_4h={lb4h}", su.summary(oos, f"lookback_4h={lb4h}")))

for lb1d in [15, 20, 30]:
    sig = engine.load_all_signals(lookback_1d=lb1d)
    cfg = engine.RunConfig()
    trades = engine.run_all(sig, cfg)
    df = su.trades_df([t for lst in trades.values() for t in lst])
    _is, oos, _full = su.split_is_oos(df)
    variants.append((f"lookback_1d={lb1d}", su.summary(oos, f"lookback_1d={lb1d}")))

print(f"\n=== 파라미터 스윕 요약 (OOS net, {len(variants)}개 변형) ===")
n_pass = 0
for name, s in variants:
    ok = (s["pf_r"] >= 1.3 and s["t"] >= 1.96)
    n_pass += ok
    print(su.fmt(s), " PASS" if ok else "")
print(f"\n통과(PF>=1.3 AND t>=1.96) 변형: {n_pass}/{len(variants)}")
print(f"소요 {time.time()-t0:.1f}s")
