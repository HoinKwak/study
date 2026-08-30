"""서브캔들 거래대금 균일성(CV) TWAP 흔적 추종 — 전체 진단 파이프라인."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from subbarcv_strat import (  # noqa: E402
    pf, tstat, split, summarize, run_all, run_symbol,
    SYMBOLS, IS_START_TS, IS_END_TS, OOS_START_TS, OOS_END_TS,
    _raw5, _raw15,
)
from subbarcv_engine import ROUNDTRIP_COST  # noqa: E402
from subbarcv_signals import compute_signal_frame, build_hourly_from_5m  # noqa: E402

pd.set_option("display.width", 180)
pd.set_option("display.max_columns", 25)
pd.set_option("display.max_rows", 200)


def section(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def print_table(rows):
    print(pd.DataFrame(rows).to_string(index=False))


# ---------------------------------------------------------------------------
section("0. 데이터 커버리지 (5m/15m, 심볼별)")
cov_rows = []
for sym in SYMBOLS:
    d5 = _raw5(sym)
    d15 = _raw15(sym)
    cov_rows.append(dict(symbol=sym, n5m=len(d5), start5m=d5.index.min(), end5m=d5.index.max(),
                          n15m=len(d15), start15m=d15.index.min(), end15m=d15.index.max()))
print_table(cov_rows)

# ---------------------------------------------------------------------------
section("1. 기본 파라미터 FULL/IS/OOS (pctile_cv<=30, consist>=8/12, range/ATR>=0.5, "
        "trail_mult=1.5, sl_atr_mult=1.2, max_hold=8h)")
base_trades = run_all()
is_t, oos_t, full_t = split(base_trades)
print(f"IS건수={len(is_t)}  OOS건수={len(oos_t)}  FULL건수={len(full_t)}  "
      f"IS+OOS==FULL? {len(is_t) + len(oos_t) == len(full_t)} (IS+OOS={len(is_t) + len(oos_t)})")
print_table([summarize(full_t, "FULL"), summarize(is_t, "IS"), summarize(oos_t, "OOS")])
print("\n종목별 OOS:")
print_table([summarize(oos_t[oos_t["symbol"] == s], s) for s in SYMBOLS])

section("1b. 회계 정합 (raw_pnl_accum - fees == pnl), 종목별 독립계좌 $10,000 순차복리 1%리스크")


def account(df: pd.DataFrame, start_equity=10_000.0):
    df = df.sort_values("entry_time").copy()
    equity = start_equity
    raw_pnl_accum = fees_accum = pnl_accum = 0.0
    for _, row in df.iterrows():
        risk_dollar = equity * 0.01
        notional = risk_dollar / row["risk_frac"] if row["risk_frac"] > 0 else 0.0
        raw_pnl = notional * row["raw_ret"]
        fees = notional * ROUNDTRIP_COST
        net_pnl = notional * row["net_ret"]
        raw_pnl_accum += raw_pnl
        fees_accum += fees
        pnl_accum += net_pnl
        equity += net_pnl
        if equity <= 0:
            equity = 1.0
    return raw_pnl_accum, fees_accum, pnl_accum, equity


for sym in SYMBOLS:
    sub = full_t[full_t["symbol"] == sym]
    if len(sub) == 0:
        continue
    raw_acc, fees_acc, pnl_acc, final_eq = account(sub)
    ok = abs((raw_acc - fees_acc) - pnl_acc) < 1e-6
    print(f"{sym}: n={len(sub)} raw={raw_acc:.2f} fees={fees_acc:.2f} pnl={pnl_acc:.2f} "
          f"raw-fees={raw_acc - fees_acc:.2f} 일치?={ok} 최종equity={final_eq:.2f}")

section("1c. 무비용 진단 (fee=0, slippage=0) — 폐기조건 ③ (OOS gross PF(R)<1.0 이면 FAIL)")
fee0_trades = run_all(fee0=True)
is0, oos0, full0 = split(fee0_trades)
print_table([summarize(full0, "FULL(무비용)"), summarize(is0, "IS(무비용)"),
             summarize(oos0, "OOS(무비용)")])
oos_gross_pf_r = pf(oos_t["r_gross"])
print(f"\n[폐기조건③ 판정] OOS gross PF(R) = {oos_gross_pf_r:.4f} "
      f"({'FAIL: gross<1.0' if oos_gross_pf_r < 1.0 else 'gross>=1.0, 통과'})")

section("2. 청산사유/방향 분포 (FULL), zero_hold_frac")
print(full_t["exit_reason"].value_counts())
print(full_t["direction"].value_counts())
zero_hold = (full_t["exit_idx"] == full_t["entry_idx"]).mean()
print(f"zero_hold_frac(=exit_idx==entry_idx, 진입봉 자체에서 스톱 터치): {zero_hold:.4f}")
print("\n보유기간(15m봉수) 분포:")
print(full_t["bars_held"].describe())

section("3. 동어반복(tautology) 점검 — CV vs range/ATR, CV vs ATR%, CV vs 실현변동성 상관 "
        "(전체구간 vs 트리거 시점 한정)")


def tautology_check(symbol: str):
    df5 = _raw5(symbol)
    hourly = compute_signal_frame(df5)
    valid = hourly.dropna(subset=["cv", "range_atr"])
    corr_full_range = valid["cv"].corr(valid["range_atr"])
    # ATR% = ATR/close (변동성 국면 프록시), 실현변동성 = 로그수익률 24봉(1일) 표준편차
    atr_pct = (hourly["atr"] / hourly["close"])
    logret = np.log(hourly["close"]).diff()
    rvol = logret.rolling(24).std()
    valid2 = pd.DataFrame({"cv": hourly["cv"], "atr_pct": atr_pct, "rvol": rvol}).dropna()
    corr_full_atrpct = valid2["cv"].corr(valid2["atr_pct"])
    corr_full_rvol = valid2["cv"].corr(valid2["rvol"])

    trig = (hourly["long_trigger"] | hourly["short_trigger"]).fillna(False)
    trig_valid = hourly.loc[trig].dropna(subset=["cv", "range_atr"])
    corr_trig_range = trig_valid["cv"].corr(trig_valid["range_atr"]) if len(trig_valid) > 5 else np.nan
    trig_valid2 = valid2.loc[valid2.index.isin(hourly.index[trig])]
    corr_trig_atrpct = trig_valid2["cv"].corr(trig_valid2["atr_pct"]) if len(trig_valid2) > 5 else np.nan
    corr_trig_rvol = trig_valid2["cv"].corr(trig_valid2["rvol"]) if len(trig_valid2) > 5 else np.nan

    return dict(symbol=symbol, n_trig=int(trig.sum()),
                corr_full_cv_rangeatr=corr_full_range, corr_trig_cv_rangeatr=corr_trig_range,
                corr_full_cv_atrpct=corr_full_atrpct, corr_trig_cv_atrpct=corr_trig_atrpct,
                corr_full_cv_rvol=corr_full_rvol, corr_trig_cv_rvol=corr_trig_rvol)


taut_rows = [tautology_check(s) for s in SYMBOLS]
print_table(taut_rows)
print("\n판정 기준: |상관|>=0.3(스펙 사전점검 기준) 또는 트리거시점 한정 상관이 전체구간 대비 "
      "크게 벌어지면(예: 함정사례 0.246→0.928) 동어반복(저변동성 재포장) 의심.")

section("4. 전제의 내적 일관성 — 결합확률 실측 vs 독립가정 곱 (FULL, 종목별)")


def consistency_check(symbol: str):
    df5 = _raw5(symbol)
    hourly = compute_signal_frame(df5)
    valid = hourly.dropna(subset=["pctile_cv", "consist", "range_atr"])
    n = len(valid)
    rate_cv = (valid["pctile_cv"] <= 30.0).mean()
    rate_consist = (valid["consist"] >= 8 / 12 - 1e-9).mean()
    rate_range = (valid["range_atr"] >= 0.5).mean()
    combined_rate = ((valid["pctile_cv"] <= 30.0) & (valid["consist"] >= 8 / 12 - 1e-9)
                      & (valid["range_atr"] >= 0.5)).mean()
    indep_expect = rate_cv * rate_consist * rate_range
    ratio = combined_rate / indep_expect if indep_expect > 0 else np.nan
    return dict(symbol=symbol, n=n, rate_cv=rate_cv, rate_consist=rate_consist,
                rate_range=rate_range, combined_rate=combined_rate,
                indep_expect=indep_expect, 실제_기대_비=ratio,
                n_trig_bars=int(((valid["pctile_cv"] <= 30.0) & (valid["consist"] >= 8/12-1e-9)
                                  & (valid["range_atr"] >= 0.5)).sum()))


print_table([consistency_check(s) for s in SYMBOLS])

section("5. 종목 간 신호 상관 (OOS 진입시점 기준) — 캘린더일 + 3~5일 롤링 + 위기국면(꼬리) 상관")
oos_daily = oos_t.copy()
oos_daily["entry_date"] = oos_daily["entry_time"].dt.date
per_day_syms = oos_daily.groupby("entry_date")["symbol"].apply(lambda s: set(s))
n_days_with_signal = len(per_day_syms)
co_counts = per_day_syms.apply(len).value_counts().sort_index()
print("하루에 동시진입한 종목수 분포(고유일 기준):")
print(co_counts)
print(f"고유 신호일수: {n_days_with_signal}, 7종목 전부 동시진입일수: "
      f"{(per_day_syms.apply(len) == 7).sum()} "
      f"({(per_day_syms.apply(len) == 7).sum() / max(n_days_with_signal,1):.2%})")

# 3~5일 롤링 윈도우 동시진입(블록 단위)
oos_daily["entry_ts"] = pd.to_datetime(oos_daily["entry_date"])
for win in (3, 5):
    oos_daily[f"block{win}"] = (oos_daily["entry_ts"] - pd.Timestamp("2024-07-01")).dt.days // win
    per_blk = oos_daily.groupby(f"block{win}")["symbol"].apply(lambda s: set(s))
    n_blk = len(per_blk)
    full7 = (per_blk.apply(len) == 7).sum()
    print(f"{win}일 롤링블록: 고유블록수={n_blk}, 7종목 전부 동시(블록내)={full7} "
          f"({full7 / max(n_blk,1):.2%})")

pvt = oos_daily.pivot_table(index="entry_date", columns="symbol", values="r_net", aggfunc="mean")
corr_mat = pvt.corr()
print("\n종목간 R-배수 상관행렬(OOS, 일별 평균, 평시):")
print(corr_mat.round(3))
offdiag = corr_mat.to_numpy()[np.triu_indices(len(SYMBOLS), k=1)]
print(f"오프대각 평균={np.nanmean(offdiag):.3f}, 최소={np.nanmin(offdiag):.3f}, "
      f"최대={np.nanmax(offdiag):.3f}")

# 위기국면(꼬리) 상관: BTC 절대수익률 상위 5% 일자만 필터링
btc15 = _raw15("BTCUSDT")
btc_daily_ret = btc15["close"].resample("1D").last().pct_change().dropna()
thr = btc_daily_ret.abs().quantile(0.95)
crisis_days = set(btc_daily_ret[btc_daily_ret.abs() >= thr].index.date)
print(f"\nBTC 절대일수익률 상위5% 임계={thr:.4f}, 위기일수={len(crisis_days)}")
oos_daily_crisis = oos_daily[oos_daily["entry_date"].isin(crisis_days)]
if len(oos_daily_crisis) >= 10:
    pvt_c = oos_daily_crisis.pivot_table(index="entry_date", columns="symbol", values="r_net",
                                          aggfunc="mean")
    corr_c = pvt_c.corr()
    offdiag_c = corr_c.to_numpy()[np.triu_indices(len(SYMBOLS), k=1)]
    print("위기국면 상관행렬:")
    print(corr_c.round(3))
    print(f"위기국면 오프대각 평균={np.nanmean(offdiag_c):.3f} vs 평시 {np.nanmean(offdiag):.3f}")
else:
    print(f"위기국면 표본 부족(n={len(oos_daily_crisis)}) — 상관 계산 생략")

section("6. 정보원 무력화 대조군 — CV 종목별 랜덤 셔플 20회")
shuffle_rows = []
for seed in range(20):
    st = run_all(mode="cv_shuffle", shuffle_seed=1000 + seed)
    _, oos_s, full_s = split(st)
    shuffle_rows.append(dict(seed=seed, n_full=len(full_s), n_oos=len(oos_s),
                              pf_r_gross_oos=pf(oos_s["r_gross"]) if len(oos_s) else np.nan,
                              pf_r_net_oos=pf(oos_s["r_net"]) if len(oos_s) else np.nan))
shuf_df = pd.DataFrame(shuffle_rows)
print(shuf_df.to_string(index=False))
base_pfr_oos = pf(oos_t["r_net"])
pct = (shuf_df["pf_r_net_oos"] < base_pfr_oos).mean()
print(f"\nbase OOS PF(R)_net={base_pfr_oos:.3f}, 셔플20회 평균={shuf_df['pf_r_net_oos'].mean():.3f}, "
      f"base보다 낮은 셔플비율={pct:.2%}(백분위={pct*100:.1f}/100)")
rank = 1 + int((shuf_df["pf_r_net_oos"] >= base_pfr_oos).sum())
print(f"순열검정: base가 (base+20셔플) 21개 중 순위 {rank}위 → p≈{rank/21:.4f}")

section("7. 게이트 없음 대조군 — 순수 15m Donchian(20) 브레이크아웃 (폐기조건① 최우선)")
donch_trades = run_all(mode="donchian")
is_d, oos_d, full_d = split(donch_trades)
print(f"donchian n: FULL={len(full_d)} IS={len(is_d)} OOS={len(oos_d)} "
      f"(base n: FULL={len(full_t)} IS={len(is_t)} OOS={len(oos_t)}, "
      f"빈도비={len(full_d)/max(len(full_t),1):.2f}x)")
print_table([summarize(full_d, "donchian FULL"), summarize(oos_d, "donchian OOS")])
print_table([summarize(full_t, "base(CV) FULL"), summarize(oos_t, "base(CV) OOS")])

# 표본수 맞춘 부트스트랩 검정(폐기조건① 판정 방식): donchian OOS R_net 풀에서 base와
# 같은 표본수로 복원추출 반복, base PF(R)_net 이 그 분포에서 유의하게 우수한지.
rng = np.random.default_rng(42)


def bootstrap_p_better(base_r, pool_r, n_boot=5000):
    base_arr = np.asarray(base_r, dtype=float)
    pool_arr = np.asarray(pool_r, dtype=float)
    n = len(base_arr)
    base_pf = pf(base_arr)
    boots = []
    for _ in range(n_boot):
        samp = rng.choice(pool_arr, size=n, replace=True)
        boots.append(pf(samp))
    boots = np.array(boots)
    p_not_better = float((boots >= base_pf).mean())  # base 가 우수하지 않을(같거나 낮을) 확률
    return base_pf, boots, p_not_better


if len(oos_d) >= 10 and len(oos_t) >= 5:
    base_pf_r, boots_d, p_val = bootstrap_p_better(oos_t["r_net"], oos_d["r_net"])
    print(f"\n[폐기조건① 부트스트랩] base OOS PF(R)_net={base_pf_r:.3f}, "
          f"donchian 풀에서 표본수({len(oos_t)}) 맞춰 5000회 복원추출한 PF(R) 분포: "
          f"mean={boots_d.mean():.3f} median={np.median(boots_d):.3f}")
    print(f"p(donchian 부트스트랩 PF(R) >= base PF(R)) = {p_val:.4f} "
          f"({'p>0.1 → 비유의 → 폐기조건① 충족(FAIL)' if p_val > 0.1 else 'p<=0.1 → base가 유의하게 우수'})")
else:
    print("donchian 또는 base OOS 표본 부족 — 부트스트랩 생략")

section("8. 방향반전(REV) 대조군 — SL/TP 대칭 재배치 + 청산조건 방향분기, zero_hold_frac")
rev_trades = run_all(mode="reverse")
is_r, oos_r, full_r = split(rev_trades)
print_table([summarize(full_r, "REV FULL"), summarize(is_r, "REV IS"), summarize(oos_r, "REV OOS")])
zero_hold_rev = (rev_trades["exit_idx"] == rev_trades["entry_idx"]).mean() if len(rev_trades) else np.nan
print(f"\nzero_hold_frac(REV)={zero_hold_rev:.4f}  zero_hold_frac(base)={zero_hold:.4f}")
print("\nREV 청산사유 분포:")
print(rev_trades["exit_reason"].value_counts())
print("\nREV 보유기간 분포:")
print(rev_trades["bars_held"].describe())
print(f"\n방향비교(OOS): base PF(R)_net={pf(oos_t['r_net']):.3f}  REV PF(R)_net={pf(oos_r['r_net']):.3f}")

section("9. LOO(Leave-One-Out) — 종목 1개씩 제외 (OOS)")
loo_rows = []
for sym in SYMBOLS:
    sub = oos_t[oos_t["symbol"] != sym]
    loo_rows.append(dict(제외종목=sym, n=len(sub), pf_gross=pf(sub["raw_ret"]),
                          pf_net=pf(sub["net_ret"]), pf_r_net=pf(sub["r_net"]),
                          t_r_net=tstat(sub["r_net"])))
print_table(loo_rows)

section("10. top-N 트레이드 제거 (OOS, net_ret 상위 N건 제거)")
topn_rows = []
for N in (0, 3, 5, 10, 20):
    sub = oos_t.sort_values("net_ret", ascending=False).iloc[N:]
    topn_rows.append(dict(N=N, n=len(sub), pf_net=pf(sub["net_ret"]), pf_r_net=pf(sub["r_net"]),
                           t_r_net=tstat(sub["r_net"])))
print_table(topn_rows)

section("11. 분기별 손익 분해 (OOS, net_ret 합계 비중)")
oos_q = oos_t.copy()
oos_q["quarter"] = oos_q["entry_time"].dt.to_period("Q").astype(str)
q_pnl = oos_q.groupby("quarter")["net_ret"].sum().sort_values(ascending=False)
total_net = oos_q["net_ret"].sum()
print(q_pnl)
if total_net != 0 and len(q_pnl):
    top_q = q_pnl.index[0]
    print(f"\n최대기여분기={top_q}, 비중={q_pnl.iloc[0] / total_net:.2%}")
    sub_ex_top = oos_q[oos_q["quarter"] != top_q]
    print(f"최대기여분기 제외 시: n={len(sub_ex_top)}, pf_net={pf(sub_ex_top['net_ret']):.3f}, "
          f"t_r_net={tstat(sub_ex_top['r_net']):.3f}")

section("12. 파라미터 스윕 (OOS)")
sweep_rows = []
for th in (15, 20, 25, 30, 35, 40):
    t = run_all(pctile_cv_th=th)
    _, o, _ = split(t)
    sweep_rows.append(dict(param="pctile_cv_th", value=th, n=len(o), pf_net=pf(o["net_ret"]),
                            pf_r_net=pf(o["r_net"]), t_r_net=tstat(o["r_net"])))
for cn in (7, 8, 9, 10):
    t = run_all(consist_th_num=cn)
    _, o, _ = split(t)
    sweep_rows.append(dict(param="consist_th_num", value=cn, n=len(o), pf_net=pf(o["net_ret"]),
                            pf_r_net=pf(o["r_net"]), t_r_net=tstat(o["r_net"])))
for ra in (0.3, 0.4, 0.5, 0.6, 0.8):
    t = run_all(range_atr_th=ra)
    _, o, _ = split(t)
    sweep_rows.append(dict(param="range_atr_th", value=ra, n=len(o), pf_net=pf(o["net_ret"]),
                            pf_r_net=pf(o["r_net"]), t_r_net=tstat(o["r_net"])))
for tm in (1.0, 1.25, 1.5, 2.0):
    t = run_all(trail_mult=tm)
    _, o, _ = split(t)
    sweep_rows.append(dict(param="trail_mult", value=tm, n=len(o), pf_net=pf(o["net_ret"]),
                            pf_r_net=pf(o["r_net"]), t_r_net=tstat(o["r_net"])))
for mh in (4, 6, 8, 12, 16):
    t = run_all(max_hold_hours=mh)
    _, o, _ = split(t)
    sweep_rows.append(dict(param="max_hold_hours", value=mh, n=len(o), pf_net=pf(o["net_ret"]),
                            pf_r_net=pf(o["r_net"]), t_r_net=tstat(o["r_net"])))
print_table(sweep_rows)
n_pass = sum(1 for r in sweep_rows if r["pf_net"] >= 1.3 and r["n"] >= 20)
print(f"\n스윕 {len(sweep_rows)}변형 중 OOS net PF>=1.3(n>=20) 통과: {n_pass}건")

section("13. de-clustering (트레이드/캘린더일/3~5일 롤링 재검정, net & gross 동일 적용)")
oos_dc = oos_t.copy()
oos_dc["entry_date"] = oos_dc["entry_time"].dt.date
daily_net = oos_dc.groupby("entry_date")["net_ret"].mean()
daily_gross = oos_dc.groupby("entry_date")["raw_ret"].mean()
oos_dc["entry_ts"] = pd.to_datetime(oos_dc["entry_date"])
oos_dc["block3"] = (oos_dc["entry_ts"] - pd.Timestamp("2024-07-01")).dt.days // 3
oos_dc["block5"] = (oos_dc["entry_ts"] - pd.Timestamp("2024-07-01")).dt.days // 5
blk3_net = oos_dc.groupby("block3")["net_ret"].mean()
blk3_gross = oos_dc.groupby("block3")["raw_ret"].mean()
blk5_net = oos_dc.groupby("block5")["net_ret"].mean()
blk5_gross = oos_dc.groupby("block5")["raw_ret"].mean()

print(f"명목 트레이드 t(R_net)={tstat(oos_t['r_net']):.3f} (n={len(oos_t)})  "
      f"t(gross r)={tstat(oos_t['r_gross']):.3f}")
print(f"캘린더일 단위(중복종목 평균): n={len(daily_net)} PF_net={pf(daily_net):.3f} "
      f"t_net={tstat(daily_net):.3f}  PF_gross={pf(daily_gross):.3f} t_gross={tstat(daily_gross):.3f}")
print(f"3일 롤링블록 단위: n={len(blk3_net)} PF_net={pf(blk3_net):.3f} t_net={tstat(blk3_net):.3f}  "
      f"PF_gross={pf(blk3_gross):.3f} t_gross={tstat(blk3_gross):.3f}")
print(f"5일 롤링블록 단위: n={len(blk5_net)} PF_net={pf(blk5_net):.3f} t_net={tstat(blk5_net):.3f}  "
      f"PF_gross={pf(blk5_gross):.3f} t_gross={tstat(blk5_gross):.3f}")

section("14. 룩어헤드 절단 테스트 (여러 종목)")
lookahead_rows = []
for sym in SYMBOLS[:4]:
    df5 = _raw5(sym)
    full_hourly = compute_signal_frame(df5)
    cut_ts = pd.Timestamp("2024-01-01")
    df5_cut = df5[df5.index < cut_ts + pd.Timedelta(hours=1)]  # 절단 시점 이후 데이터 제거
    cut_hourly = compute_signal_frame(df5_cut)
    common_idx = full_hourly.index.intersection(cut_hourly.index)
    common_idx = common_idx[common_idx < cut_ts - pd.Timedelta(days=61)]  # 절단 경계 근접 제외
    diffs = 0
    checked = 0
    for t in common_idx[-500:]:
        a = full_hourly.loc[t, "pctile_cv"]
        b = cut_hourly.loc[t, "pctile_cv"]
        checked += 1
        if pd.notna(a) and pd.notna(b) and abs(a - b) > 1e-6:
            diffs += 1
        elif pd.isna(a) != pd.isna(b):
            diffs += 1
    lookahead_rows.append(dict(symbol=sym, cut=str(cut_ts), checked=checked, diffs=diffs))
print_table(lookahead_rows)
print("판정: diffs=0 이면 절단 이후 데이터가 절단 이전 신호값에 영향을 주지 않음(룩어헤드 없음).")

section("15. 사전 등록 폐기조건 종합 판정")
print(f"① 게이트없음(Donchian) 대비: 위 7절 부트스트랩 결과 참조")
print(f"② OOS 표본 n={len(oos_t)} < 20 이면 판단불가: "
      f"{'해당(판단불가)' if len(oos_t) < 20 else '표본 충분'}")
print(f"③ 무비용 OOS gross PF(R) = {oos_gross_pf_r:.4f} "
      f"{'< 1.0 → FAIL' if oos_gross_pf_r < 1.0 else '>= 1.0 → 통과'}")

print("\n완료.")
