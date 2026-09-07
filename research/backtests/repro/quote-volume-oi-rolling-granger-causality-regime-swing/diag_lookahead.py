"""룩어헤드 절단 검증 — 주전략(그레인저 레짐)뿐 아니라 대조군(게이트없음·z-score 게이트)에도 적용.

각 심볼을 특정 컷오프 봉까지만 잘라(cut) 그 구간에서 다시 계산한 신호가, 전체 구간으로 계산한
신호를 cut 이전까지 잘랐을 때와 완전히 일치하는지 확인한다. 불일치가 있으면 미래 데이터를
참조하는 룩어헤드가 있다는 뜻이다."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import load_klines_4h, load_metrics_5m, oi_4h_from_5m, ema_4h, atr14_4h
from granger import rolling_granger_pvalues, classify_regime
from control import gate_none_entries, zscore_gate_entries
from signals import Signals, build_signals
from events import gated_entries

HERE = Path(__file__).resolve().parent


def build_signals_from_df(symbol: str, df_full: pd.DataFrame, cutoff: int | None,
                          gc_window=60, gc_lag=4, p_sig=0.05, p_insig=0.10) -> Signals:
    df = df_full.iloc[:cutoff].copy() if cutoff is not None else df_full.copy()
    qv = df["quote_volume"].astype(float)
    oi = df["oi"].astype(float)
    qv_safe = qv.where(qv > 0)
    oi_safe = oi.where(oi > 0)
    dqv = np.log(qv_safe).diff()
    doi = np.log(oi_safe).diff()
    p_qv2oi_arr, p_oi2qv_arr = rolling_granger_pvalues(doi.to_numpy(), dqv.to_numpy(),
                                                       window=gc_window, lag=gc_lag)
    p_qv2oi = pd.Series(p_qv2oi_arr, index=df.index)
    p_oi2qv = pd.Series(p_oi2qv_arr, index=df.index)
    regime_arr = classify_regime(p_qv2oi_arr, p_oi2qv_arr, p_sig=p_sig, p_insig=p_insig)
    regime = pd.Series(regime_arr, index=df.index)
    prev_regime = regime.shift(1)
    transition_qv = (prev_regime == "oi_lead") & (regime == "qv_lead")
    ret4h = np.log(df["close"]).diff()
    ema = ema_4h(df, 20, 50)
    atr14 = atr14_4h(df)
    return Signals(symbol=symbol, df=df[["open", "high", "low", "close", "volume", "quote_volume"]],
                   oi=df["oi"], oi_5m_count=df["oi_5m_count"], dqv=dqv, doi=doi,
                   p_qv2oi=p_qv2oi, p_oi2qv=p_oi2qv, regime=regime, transition_qv=transition_qv,
                   ret4h=ret4h, ema_fast=ema["ema_fast"], ema_slow=ema["ema_slow"], atr14=atr14)


def load_full_df(symbol: str) -> pd.DataFrame:
    df = load_klines_4h(symbol)
    m5 = load_metrics_5m(symbol)
    oi4h = oi_4h_from_5m(m5)
    return df.join(oi4h, how="left")


def check_symbol(symbol: str, cutoff: int) -> dict:
    df_full = load_full_df(symbol)
    sig_full = build_signals_from_df(symbol, df_full, cutoff=None)
    sig_cut = build_signals_from_df(symbol, df_full, cutoff=cutoff)

    n_cut = len(sig_cut.df)
    # 주신호(그레인저 레짐) 비교
    p_qv2oi_full = sig_full.p_qv2oi.iloc[:n_cut].to_numpy()
    p_qv2oi_cut = sig_cut.p_qv2oi.to_numpy()
    p_oi2qv_full = sig_full.p_oi2qv.iloc[:n_cut].to_numpy()
    p_oi2qv_cut = sig_cut.p_oi2qv.to_numpy()
    mismatch_p = int(np.sum(~np.isclose(np.nan_to_num(p_qv2oi_full, nan=-1.0),
                                        np.nan_to_num(p_qv2oi_cut, nan=-1.0), atol=1e-9)) +
                     np.sum(~np.isclose(np.nan_to_num(p_oi2qv_full, nan=-1.0),
                                        np.nan_to_num(p_oi2qv_cut, nan=-1.0), atol=1e-9)))
    regime_full = sig_full.regime.iloc[:n_cut].to_numpy()
    regime_cut = sig_cut.regime.to_numpy()
    mismatch_regime = int(np.sum(regime_full != regime_cut))
    trans_full = sig_full.transition_qv.iloc[:n_cut].to_numpy()
    trans_cut = sig_cut.transition_qv.to_numpy()
    mismatch_trans = int(np.sum(trans_full != trans_cut))

    # 대조군 신호도 절단 검증
    entries_full = gated_entries(sig_full)
    entries_full_in_cut = entries_full[entries_full["signal_bar"] < n_cut]
    entries_cut = gated_entries(sig_cut)
    mismatch_entries = abs(len(entries_full_in_cut) - len(entries_cut))

    gn_full = gate_none_entries(sig_full)
    gn_full_in_cut = gn_full[gn_full["signal_bar"] < n_cut]
    gn_cut = gate_none_entries(sig_cut)
    mismatch_gn = abs(len(gn_full_in_cut) - len(gn_cut))

    z_full = zscore_gate_entries(sig_full)
    z_full_in_cut = z_full[z_full["signal_bar"] < n_cut]
    z_cut = zscore_gate_entries(sig_cut)
    mismatch_z = abs(len(z_full_in_cut) - len(z_cut))

    return {"symbol": symbol, "cutoff": cutoff, "n_cut": n_cut,
            "mismatch_pvalue_count": mismatch_p, "mismatch_regime_count": mismatch_regime,
            "mismatch_transition_count": mismatch_trans,
            "entries_full_in_cut": int(len(entries_full_in_cut)), "entries_cut": int(len(entries_cut)),
            "mismatch_entries": int(mismatch_entries),
            "gate_none_full_in_cut": int(len(gn_full_in_cut)), "gate_none_cut": int(len(gn_cut)),
            "mismatch_gate_none": int(mismatch_gn),
            "zscore_full_in_cut": int(len(z_full_in_cut)), "zscore_cut": int(len(z_cut)),
            "mismatch_zscore": int(mismatch_z)}


if __name__ == "__main__":
    results = []
    for sym, cutoff in [("BTCUSDT", 5000), ("ETHUSDT", 4000), ("BNBUSDT", 6500),
                        ("SOLUSDT", 3000), ("XRPUSDT", 7000), ("DOGEUSDT", 2000),
                        ("ADAUSDT", 8000)]:
        r = check_symbol(sym, cutoff)
        print(r)
        results.append(r)
    (Path(__file__).resolve().parent / "out_diag_lookahead.json").write_text(
        json.dumps(results, indent=2))
