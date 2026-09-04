"""대조군③: taker-aggressor-price-premium-absorption-scalp(기존 리포트, 8/13)와 신호 시점
중복률 실측. 그 스펙의 impl 이 커밋돼있지 않아(research/.gitignore 가 impl/ 제외) 리포트에
명시된 정의를 이 스크립트에서 독립적으로 재구현한다(리포트 §1 인용):
  buyer_avg = taker_buy_quote_volume/taker_buy_volume
  seller_avg = (quote_volume-taker_buy_quote_volume)/(volume-taker_buy_volume)
  premium_bps = (buyer_avg-seller_avg)/close*10000
  premium_z = 최근 100봉(자기포함) 롤링 z-score
  body_ratio = |close-open|/(high-low)
  숏: premium_z>=+2.5 AND body_ratio<=0.35 / 롱: premium_z<=-2.5 AND body_ratio<=0.35
사전 폐기조건 (c): 중복률>=70% 이면 중복전략으로 폐기.
"""
import pickle

import numpy as np
import pandas as pd

import common
import engine
import stats_utils as su

with open(common.SP / "sigs_200.pkl", "rb") as f:
    sigs = pickle.load(f)

Z_TH = 3.0
BODY_TH = 0.40


def base_trigger_times(sig: common.Signals) -> set:
    """본 스펙의 원시(raw) 트리거 시점 — 1h확인·쿨다운 등 엔진 필터 이전, 순수 신호조건만."""
    zb, zs = sig.z_buy, sig.z_sell
    body = sig.body_ratio.to_numpy(float)
    trig = (np.isfinite(body) & (body <= BODY_TH)
           & ((np.isfinite(zb) & (zb >= Z_TH)) | (np.isfinite(zs) & (zs >= Z_TH))))
    return set(sig.df15m.index[trig])


def taker_aggressor_trigger_times(sig: common.Signals) -> pd.DataFrame:
    df = sig.df15m
    tb_vol = df["taker_buy_volume"]
    sell_vol = df["volume"] - tb_vol
    buyer_avg = (df["taker_buy_quote_volume"] / tb_vol.replace(0.0, np.nan))
    seller_avg = ((df["quote_volume"] - df["taker_buy_quote_volume"])
                  / sell_vol.replace(0.0, np.nan))
    premium_bps = (buyer_avg - seller_avg) / df["close"] * 10000.0
    m = premium_bps.rolling(100).mean()
    sd = premium_bps.rolling(100).std(ddof=0)
    premium_z = (premium_bps - m) / sd.replace(0.0, np.nan)
    body_ratio = sig.body_ratio
    short_trig = (premium_z >= 2.5) & (body_ratio <= 0.35)
    long_trig = (premium_z <= -2.5) & (body_ratio <= 0.35)
    idx = df.index[(short_trig | long_trig).fillna(False)]
    return pd.DataFrame({"entry_time": idx})


overlap_rows = []
for sym, sig in sigs.items():
    ta = taker_aggressor_trigger_times(sig)
    ta_times = set(ta["entry_time"])
    base_sig_times = base_trigger_times(sig)
    overlap = base_sig_times & ta_times
    frac = len(overlap) / len(base_sig_times) if base_sig_times else float("nan")
    overlap_rows.append((sym, len(base_sig_times), len(ta_times), len(overlap), frac))
    print(f"{sym:10s} base트리거={len(base_sig_times):5d} taker-aggressor트리거={len(ta_times):6d} "
         f"중복={len(overlap):5d} 중복률(base기준)={frac:.2%}")

tot_base = sum(r[1] for r in overlap_rows)
tot_overlap = sum(r[3] for r in overlap_rows)
print(f"\n합계 중복률(base 기준) = {tot_overlap}/{tot_base} = {tot_overlap/tot_base:.2%}")
print("사전 폐기조건 (c): 중복률>=70% 이면 중복전략으로 폐기")
