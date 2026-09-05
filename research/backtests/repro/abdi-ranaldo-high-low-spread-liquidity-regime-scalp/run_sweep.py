"""파라미터 스윕: ar_window·pctile_window·pctile_entry(lo/hi)·burst_mult·trail_mult·stop_mult.
⚠️"설계판단을 스윕에서 점검했다"고 쓰려면 그 스윕이 실제로 그 판단의 대안을 돌렸는지 확인할 것
(인접 파라미터 스윕은 해석 대안의 검증이 아니다) — 본 스윕은 파라미터 민감도만 확인하며, 해석적
설계판단(예: 15m 단일확인봉 원칙, 서브모드 게이트 배타성)의 대안 검증은 run_design_alt.py 참조."""
from __future__ import annotations

from dataclasses import replace as dc_replace

import common
import engine
import run_main as rm
import stats_utils as su
from crypto_trader.config import get_settings
from crypto_trader.risk import RiskManager


def run_variant(sigs, cfg: engine.RunConfig, label: str):
    settings = get_settings()
    risk = RiskManager(settings)
    all_trades = []
    for sym, sig in sigs.items():
        all_trades.extend(engine.run_symbol(sym, sig, cfg, settings, risk))
    df = su.trades_df(all_trades)
    _, oos_df, _ = su.split_is_oos(df)
    s = su.summary(oos_df, label)
    print(" ", su.print_summary(s))
    return s


def main():
    sigs = rm.get_signals()
    print("===== 기준(baseline) =====")
    run_variant(sigs, engine.RunConfig(), "baseline")

    print("\n===== ar_window 스윕 =====")
    for w in (10, 15, 20, 30, 40):
        sigs_w = {sym: common.with_ar_window(sig, w) for sym, sig in sigs.items()}
        run_variant(sigs_w, engine.RunConfig(ar_window=w), f"ar_window={w}")

    print("\n===== pctile_window(일) 스윕 =====")
    for d in (10, 15, 20, 25, 30):
        sigs_d = {sym: common.with_pctile_window(sig, d) for sym, sig in sigs.items()}
        run_variant(sigs_d, engine.RunConfig(), f"pctile_window={d}d")

    print("\n===== pctile_entry(lo/hi) 스윕 =====")
    for lo, hi in ((0.15, 0.85), (0.20, 0.80), (0.25, 0.75), (0.30, 0.70)):
        cfg = engine.RunConfig(pctile_entry_lo=lo, pctile_entry_hi=hi)
        run_variant(sigs, cfg, f"pctile_lo={lo}/hi={hi}")

    print("\n===== burst_mult 스윕 =====")
    for m in (1.2, 1.5, 1.8, 2.0):
        cfg = engine.RunConfig(burst_mult=m)
        run_variant(sigs, cfg, f"burst_mult={m}")

    print("\n===== trail_mult 스윕 =====")
    for m in (1.2, 1.6, 2.0, 2.2):
        cfg = engine.RunConfig(trail_mult=m)
        run_variant(sigs, cfg, f"trail_mult={m}")

    print("\n===== stop_mult 스윕 =====")
    for m in (0.8, 1.0, 1.2, 1.5):
        cfg = engine.RunConfig(stop_mult=m)
        run_variant(sigs, cfg, f"stop_mult={m}")

    print("\n===== max_hold_bars 스윕 =====")
    for m in (8, 12, 16, 24):
        cfg = engine.RunConfig(max_hold_bars=m)
        run_variant(sigs, cfg, f"max_hold_bars={m}")


if __name__ == "__main__":
    main()
