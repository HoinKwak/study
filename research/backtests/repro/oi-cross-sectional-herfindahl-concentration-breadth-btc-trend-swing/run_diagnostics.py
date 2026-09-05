"""동어반복·대조군·de-clustering·룩어헤드 절단·부호 무작위화 진단 일괄 실행.

리포트 §4~§8 근거 수치를 재현한다.
"""
from __future__ import annotations
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi")

import numpy as np
import pandas as pd

import common
import engine
import stats_utils as su

univ = common.build_universe()
sig = common.build_signals(univ)

print("=== §4.2 동어반복 점검(전체 구간) ===")
oi_growth7 = sig.oi_total_growth7
df = pd.DataFrame({"hhi_z": sig.hhi_z, "share_z": sig.btc_oi_share_z, "oi_g7": oi_growth7}).dropna()
print(f"n={len(df)}")
print(df.corr())

print()
print("=== §4.2 동어반복 점검(트리거 시점 한정 — EMA50 크로스 이벤트일) ===")
close1d = sig.df1d["close"].to_numpy(float)
ema50 = sig.ema50_1d.to_numpy(float)
prev_above = close1d[:-1] > ema50[:-1]
curr_above = close1d[1:] > ema50[1:]
valid = (np.isfinite(ema50[:-1]) & np.isfinite(ema50[1:]) & np.isfinite(close1d[:-1])
        & np.isfinite(close1d[1:]))
golden = valid & (~prev_above) & curr_above
death = valid & prev_above & (~curr_above)
cross_days = np.where(golden | death)[0] + 1
gate_days = cross_days - 1
hz = sig.hhi_z.to_numpy(float)[gate_days]
sz = sig.btc_oi_share_z.to_numpy(float)[gate_days]
oi7 = sig.oi_total_growth7.to_numpy(float)[gate_days]
dtrig = pd.DataFrame({"hhi_z": hz, "share_z": sz, "oi_g7": oi7}).dropna()
print(f"n={len(dtrig)} (EMA50 크로스 이벤트 전체 — 게이트 통과 여부와 무관)")
print(dtrig.corr())

print()
print("=== §4.2 거래대금 집중도(HHI, 종목축) 와의 상관 ===")
qv = {s: common.load_klines_1d(s)["quote_volume"] for s in common.SYMBOLS}
qvdf = pd.DataFrame(qv)
complete = qvdf.notna().all(axis=1)
total = qvdf.sum(axis=1)
shares = qvdf.div(total, axis=0)
hhi_vol = (shares ** 2).sum(axis=1).where(complete)
hhi_vol_z = common.rolling_zscore(hhi_vol, 60)
dvol = pd.DataFrame({"hhi_oi_z": sig.hhi_z, "hhi_vol_z": hhi_vol_z}).dropna()
print(f"n={len(dvol)}")
print(dvol.corr())

print()
print("=== §5 대조군 실행(gate=none/hhi/btcshare/reverse, fee on/off) ===")
for gate in ["none", "hhi", "btcshare", "reverse"]:
    for fee_on in [True, False]:
        cfg = engine.RunConfig(gate=gate, fee_on=fee_on)
        trades = engine.run_config(sig, cfg)
        tdf = su.trades_df(trades)
        is_df, oos_df, full_df = su.split_is_oos(tdf)
        label = f"{gate:10s} fee={'on ' if fee_on else 'off'}"
        print(su.print_summary(su.summary(full_df, label + " FULL")))
        print(su.print_summary(su.summary(is_df, label + " IS  ")))
        print(su.print_summary(su.summary(oos_df, label + " OOS ")))
        assert len(is_df) + len(oos_df) == len(full_df), "IS+OOS != FULL"

print()
print("=== §5 base⊆pool 중복률 + 부트스트랩 ===")


def get(gate):
    cfg = engine.RunConfig(gate=gate, fee_on=True)
    trades = engine.run_config(sig, cfg)
    return su.trades_df(trades)


df_none = get("none"); df_hhi = get("hhi"); df_share = get("btcshare"); df_rev = get("reverse")
is_h, oos_h, full_h = su.split_is_oos(df_hhi)
is_n, oos_n, full_n = su.split_is_oos(df_none)
is_s, oos_s, full_s = su.split_is_oos(df_share)

ov_share = su.independent_pair_diff(full_h, full_s)
print("hhi vs btcshare 중복(entry_time 기준):", ov_share)
sh = set(df_hhi["signal_day_idx"]); ss = set(df_share["signal_day_idx"])
print("hhi ⊆ btcshare (signal_day_idx 기준):", sh.issubset(ss), len(sh), "/", len(ss))

r_hhi_oos = oos_h["r"].to_numpy(); r_none_oos = oos_n["r"].to_numpy(); r_share_oos = oos_s["r"].to_numpy()
print("matched-N: hhi(OOS) vs none(OOS)pool:", su.bootstrap_matched_n_diff(r_none_oos, r_hhi_oos))
print("matched-N: hhi(OOS) vs btcshare(OOS)pool:", su.bootstrap_matched_n_diff(r_share_oos, r_hhi_oos))
print("diff test: hhi vs btcshare(OOS):", su.bootstrap_diff_test(r_hhi_oos, r_share_oos))
print("diff test: hhi vs none(OOS):", su.bootstrap_diff_test(r_hhi_oos, r_none_oos))

print()
print("=== §6 부호 무작위화 vs 승률고정 대안 검정 ===")
print("sign-shuffle FULL:", su.sign_shuffle_test(full_h["r"].to_numpy()))
print("winrate-fixed FULL:", su.winrate_fixed_shuffle_test(full_h["r"].to_numpy()))
print("sign-shuffle OOS:", su.sign_shuffle_test(oos_h["r"].to_numpy()))
print("winrate-fixed OOS:", su.winrate_fixed_shuffle_test(oos_h["r"].to_numpy()))

print()
print("=== §7 de-clustering(캘린더일/5일 롤링) ===")
cal = su.decluster_calendar_day(full_h)
roll = su.decluster_rolling_days(full_h, 5)
print(f"원 표본 n={len(full_h)}, 캘린더일 n={len(cal)}, 5일롤링 클러스터 n={len(roll)}")
print("5일 롤링 클러스터 크기 분포:\n", roll["n"].describe())

print()
print("=== §7 top-N 제거 민감도(FULL/OOS) ===")
sorted_full = full_h.sort_values("r", ascending=False)
for k in [1, 2, 3]:
    rest = sorted_full.iloc[k:]
    print(f"FULL top-{k} 제거: n={len(rest)} PF={su.pf_r(rest):.3f} sum_r={rest['r'].sum():.3f}")
sorted_oos = oos_h.sort_values("r", ascending=False)
for k in [1, 2]:
    rest = sorted_oos.iloc[k:]
    print(f"OOS top-{k} 제거: n={len(rest)} PF={su.pf_r(rest):.3f} sum_r={rest['r'].sum():.3f}")

print()
print("=== §8 룩어헤드 절단 검증(전 7종목 데이터 2024-01-01 절단) ===")
cutoff = pd.Timestamp("2024-01-01", tz="UTC")
orig_load_1d = common.load_klines_1d
orig_load_metrics = common.load_metrics_5m
common.load_klines_1d.cache_clear()
common.load_metrics_5m.cache_clear()
from functools import lru_cache


@lru_cache(maxsize=None)
def trunc_klines_1d(sym):
    d = orig_load_1d.__wrapped__(sym)
    return d[d.index < cutoff]


@lru_cache(maxsize=None)
def trunc_metrics(sym):
    d = orig_load_metrics.__wrapped__(sym)
    return d[d.index < cutoff]


common.load_klines_1d = trunc_klines_1d
common.load_metrics_5m = trunc_metrics
univ_cut = common.build_universe()
sig_cut = common.build_signals(univ_cut)
common_idx = sig.hhi_z.index.intersection(sig_cut.hhi_z.index)
common_idx = common_idx[common_idx < cutoff - pd.Timedelta(days=5)]
diff_hhi = (sig.hhi_z.reindex(common_idx) - sig_cut.hhi_z.reindex(common_idx)).abs()
diff_ema = (sig.ema50_1d.reindex(common_idx) - sig_cut.ema50_1d.reindex(common_idx)).abs()
print(f"비교표본 n={len(common_idx)}  hhi_z 최대차={diff_hhi.max()}  ema50 최대차={diff_ema.max()}")
print("(0.0 이어야 정상 — 미래 데이터 절단 후에도 절단시점 이전 신호가 완전히 동일해야 룩어헤드 없음)")
