"""필수 진단 일괄 실행: 무비용 gross · de-clustering(캘린더일 + 3~5일 롤링) · 종목간 상관(연간+꼬리)
· 반전 대조군 · 베타 무력화 대조군(z_oi_raw) · 신호빈도 대조 · 몸통/꼬리 구간 분해."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sstats

import common
import engine
import stats_utils as su


def run_cfg(bundles, cfg, label):
    trades = engine.run_all(bundles, cfg)
    rows = [su.trades_df(trades.get(s, [])) for s in common.ALT_SYMBOLS]
    pooled = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    is_p, oos_p, full_p = su.split_is_oos(pooled)
    print(f"\n### {label} ###")
    print(" ", su.print_summary(su.summary(is_p, "IS")))
    print(" ", su.print_summary(su.summary(oos_p, "OOS")))
    print(" ", su.print_summary(su.summary(full_p, "FULL")))
    return pooled, is_p, oos_p, full_p


def section(title):
    print("\n" + "=" * 20 + f" {title} " + "=" * 20)


def main():
    bundles = engine.load_all_bundles()
    base_cfg = engine.RunConfig()
    pooled_base, is_base, oos_base, full_base = run_cfg(bundles, base_cfg, "1) 채택안(base, net)")

    # ------------------------------------------------------------ 1) 무비용 gross 진단
    section("무비용(gross) 진단: fee=0, slippage=0")
    gross_cfg = engine.RunConfig(fee_on=False, taker_fee=0.0, slippage=0.0)
    pooled_gross, is_g, oos_g, full_g = run_cfg(bundles, gross_cfg, "gross(fee=0,slip=0)")

    # ------------------------------------------------------------ 2) de-clustering
    section("de-clustering (OOS, 채택안)")
    cal = su.decluster_calendar_day(oos_base)
    print(" 캘린더일 단위  :", su.print_summary(su.summary(cal, "OOS cal-day")))
    for w in (3, 4, 5):
        roll = su.decluster_rolling_days(oos_base, window_days=w)
        print(f" {w}일 롤링클러스터:", su.print_summary(su.summary(roll, f"OOS roll{w}d")))
    # gross 도 동일 de-clustering(폐기조건 근거로 gross t 인용시 병행 요건)
    cal_g = su.decluster_calendar_day(oos_g)
    print(" [gross] 캘린더일:", su.print_summary(su.summary(cal_g, "OOS(gross) cal-day")))

    # ------------------------------------------------------------ 3) 종목간 신호 상관
    section("종목간 신호 상관(잔차 z-score 일봉 시계열)")
    daily_z = {}
    for sym in common.ALT_SYMBOLS:
        d = common.build_daily_signals(sym)
        daily_z[sym] = pd.Series(d.z_resid, index=d.idx)
    zdf = pd.DataFrame(daily_z).dropna(how="any")
    corr = zdf.corr()
    print(corr.round(3))
    # 위기국면(BTC 절대일수익률 상위 5%) 꼬리 상관
    btc = common.load_klines(common.BTC, "1d")
    btc_ret = btc["close"].pct_change()
    btc_ret = btc_ret.reindex(zdf.index)
    thresh = btc_ret.abs().quantile(0.95)
    crisis_mask = btc_ret.abs() >= thresh
    corr_crisis = zdf[crisis_mask].corr()
    print(f"\n위기국면(|BTC 일수익률|>={thresh*100:.2f}%, n={crisis_mask.sum()}) 상관:")
    print(corr_crisis.round(3))
    avg_off_diag = (corr.values[np.triu_indices(len(corr), 1)]).mean()
    avg_off_diag_crisis = (corr_crisis.values[np.triu_indices(len(corr_crisis), 1)]).mean()
    print(f"\n평균 쌍상관: 연간 전체={avg_off_diag:.3f}  위기국면={avg_off_diag_crisis:.3f}")

    # ------------------------------------------------------------ 4) 반전 대조군
    section("반전 대조군(신호 이벤트 동일, 체결방향만 반대)")
    rev_cfg = engine.RunConfig(reverse=True)
    pooled_rev, is_r, oos_r, full_r = run_cfg(bundles, rev_cfg, "reverse")
    print(" zero_hold_frac(반전, OOS):",
         f"{(oos_r['holding_bars']==0).mean()*100:.2f}%" if len(oos_r) else "n/a")
    print(" zero_hold_frac(base, OOS):",
         f"{(oos_base['holding_bars']==0).mean()*100:.2f}%" if len(oos_base) else "n/a")
    print(" 청산사유 분포(반전, OOS):"); print(oos_r["reason"].value_counts())

    # ------------------------------------------------------------ 5) 베타 무력화 대조군
    section("베타 무력화 대조군(회귀 잔차 대신 원 OI성장률 z-score, 회귀 미사용)")
    oi_cfg = engine.RunConfig(signal_source="oi_zscore")
    pooled_oi, is_oi, oos_oi, full_oi = run_cfg(bundles, oi_cfg, "z_oi_raw(대조군)")

    # ------------------------------------------------------------ 6) 신호빈도 대조
    section("신호빈도 대조: 일봉 임계돌파 일수 vs 실제 체결")
    total_signal_days = 0
    for sym in common.ALT_SYMBOLS:
        d = common.build_daily_signals(sym)
        z = d.z_resid
        finite = np.isfinite(z)
        n_days = ((z >= 2.0) | (z <= -2.0))[finite].sum()
        n_trades = len(pooled_base[pooled_base["symbol"] == sym])
        total_signal_days += n_days
        print(f"  {sym}: 임계돌파 일수={n_days}  실제 체결={n_trades}  배수={n_trades/n_days:.2f}"
             if n_days else f"  {sym}: 임계돌파 일수=0")
    print(f"  합계: 임계돌파 일수={total_signal_days}  실제 체결={len(pooled_base)}  "
         f"배수={len(pooled_base)/total_signal_days:.2f}")

    # ------------------------------------------------------------ 7) 몸통/꼬리 구간 분해
    section("몸통(|z| 1.0~2.0)/꼬리(|z|>=2.0) 성과 분해 — z_th=1.0 완화판으로 트레이드 재수집")
    tail_cfg = engine.RunConfig(z_th=1.0)
    trades_tail = engine.run_all(bundles, tail_cfg)
    rows = [su.trades_df(trades_tail.get(s, [])) for s in common.ALT_SYMBOLS]
    pooled_lowz = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    _, oos_lowz, _ = su.split_is_oos(pooled_lowz)
    bins = [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0), (3.0, np.inf)]
    for lo, hi in bins:
        sub = oos_lowz[(oos_lowz["z_at_signal"].abs() >= lo) & (oos_lowz["z_at_signal"].abs() < hi)]
        print(f"  |z| in [{lo},{hi}): ", su.print_summary(su.summary(sub, f"[{lo},{hi})")))

    # 저장(공유 캐시 — run_sweep/run_loo 에서 재사용)
    pooled_base.to_pickle(common.SP / "trades_base.pkl")
    pooled_gross.to_pickle(common.SP / "trades_gross.pkl")
    pooled_rev.to_pickle(common.SP / "trades_reverse.pkl")
    pooled_oi.to_pickle(common.SP / "trades_oi_control.pkl")
    pooled_lowz.to_pickle(common.SP / "trades_lowz.pkl")


if __name__ == "__main__":
    main()
