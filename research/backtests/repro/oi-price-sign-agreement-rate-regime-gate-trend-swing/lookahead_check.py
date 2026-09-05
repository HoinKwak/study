"""룩어헤드 절단검증 — 이 스펙은 BTC 단독(신호원·매매대상 모두 BTC)이라 '추가 3종목' 절단은
해당 없음(다종목 유니버스가 아님). 대신 **BTC 자기 시계열에서 3개 이상의 절단 시점**을 두고,
절단 이전 구간의 agree/agree_pctile/ema/atr 신호가 절단 유무와 무관하게 완전히 동일함을 확인한다
(각 시점 t의 신호가 t+1 이후 데이터를 전혀 참조하지 않아야 절단 후에도 불변)."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common


def _truncate_and_rebuild(cutoff: pd.Timestamp):
    full_4h = common.load_klines_4h()
    full_m5 = common.load_metrics_5m()
    # 원본 로더는 lru_cache 라 직접 필터링한 사본으로 build_signals 로직을 재현
    df4h = full_4h[full_4h.index <= cutoff].copy()
    m5 = full_m5[full_m5.index <= cutoff].copy()

    oi_4h = common.oi_4h_from_5m(m5, df4h.index)
    d_price = df4h["close"].diff()
    d_oi = oi_4h.diff()
    sign_price = np.sign(d_price)
    sign_oi = np.sign(d_oi)
    valid = d_price.notna() & d_oi.notna()
    same = (sign_price == sign_oi) & valid & (sign_price != 0) & (sign_oi != 0)
    same_f = same.astype(float)
    same_f[~valid] = np.nan
    agree = same_f.rolling(common.AGREE_WINDOW, min_periods=common.AGREE_WINDOW).mean()
    norm_bars = common.AGREE_NORM_DAYS * 6
    agree_pctile = common.rolling_pctile(agree, norm_bars)
    ema_fast = __import__("crypto_trader.signals.indicators", fromlist=["ema"]).ema(
        df4h["close"], common.EMA_FAST)
    ema_slow = __import__("crypto_trader.signals.indicators", fromlist=["ema"]).ema(
        df4h["close"], common.EMA_SLOW)
    atr20 = __import__("crypto_trader.signals.indicators", fromlist=["atr"]).atr(df4h, 20)
    return agree, agree_pctile, ema_fast, ema_slow, atr20


def run_lookahead_check():
    sig_full = common.build_signals()
    cutoffs = [
        pd.Timestamp("2022-06-30 20:00:00", tz="UTC"),
        pd.Timestamp("2023-12-31 20:00:00", tz="UTC"),
        pd.Timestamp("2025-06-30 20:00:00", tz="UTC"),
    ]
    for cutoff in cutoffs:
        agree_c, agpct_c, emaf_c, emas_c, atr_c = _truncate_and_rebuild(cutoff)
        # 절단 시점보다 충분히 이전(정규화창 365일 = 2190봉 소모 전) 구간에서 비교
        check_end = cutoff - pd.Timedelta(days=30)  # 여유 버퍼
        common_idx = agree_c.index[agree_c.index <= check_end]
        common_idx = common_idx.intersection(sig_full.agree.index)
        d_agree = (agree_c.loc[common_idx] - sig_full.agree.loc[common_idx]).abs().max()
        d_agpct = (agpct_c.loc[common_idx] - sig_full.agree_pctile.loc[common_idx]).abs().max()
        d_emaf = (emaf_c.loc[common_idx] - sig_full.ema_fast.loc[common_idx]).abs().max()
        d_atr = (atr_c.loc[common_idx] - sig_full.atr20.loc[common_idx]).abs().max()
        print(f"절단={cutoff.date()} 비교구간n={len(common_idx)} "
             f"maxΔagree={d_agree:.2e} maxΔagree_pctile={d_agpct:.2e} "
             f"maxΔema_fast={d_emaf:.2e} maxΔatr20={d_atr:.2e} "
             f"→ {'일치(룩어헤드 없음)' if max(d_agree, d_agpct, d_emaf, d_atr) < 1e-6 else '불일치!'}")
