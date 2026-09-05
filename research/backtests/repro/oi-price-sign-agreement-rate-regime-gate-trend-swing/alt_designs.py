"""설계판단 대안 실행 — 인접 파라미터 스윕과는 다른 '해석 대안'을 실제로 돌려 편향 여부를 검증.

(A) 헤더의 "1d(EMA20/50 추세확인)"을 문자 그대로 따른 대안: EMA20/50을 1d에서 계산하고 크로스
    확정일의 다음 4h봉(00:00 UTC 경계)에 진입 — 채택안(4h EMA)과 달리 여기서만 1d→4h 정렬이
    필요하므로 ms→us 업캐스트 함정 사정권. ns 명시로 회피.
(B) zero-diff(ΔOI==0 또는 ΔPrice==0) 처리 대안: 채택안은 "일치 아님"으로 세지만, 대안은 그런
    봉을 분모에서 제외(부호가 정의되는 봉만으로 일치율 계산).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "OISIGN_REPO_SRC", "/home/user/study/.claude/worktrees/agent-a64cdc714957bee50/src"))
from crypto_trader.signals import indicators as ind  # noqa: E402
from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common
import engine
import stats_utils as su

KLINES_1D_DIR = common.DATA / "klines_1d"


def _load_klines_1d() -> pd.DataFrame:
    files = sorted(KLINES_1D_DIR.glob("BTCUSDT-1d-*.csv"))
    parts = []
    for p in files:
        with open(p) as f:
            first = f.readline()
        has_header = "open_time" in first
        df = pd.read_csv(p, header=0 if has_header else None,
                         names=common._KLINE_COLS if not has_header else None)
        df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
        if df.empty:
            continue
        df["open_time"] = df["open_time"].astype("int64")
        parts.append(df)
    out = pd.concat(parts, ignore_index=True)
    ot = out["open_time"]
    is_us = ot.abs() > 10**14
    if is_us.any():
        out.loc[is_us, "open_time"] = out.loc[is_us, "open_time"] // 1000
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume", "quote_volume"]]
    out.index = out.index.as_unit("ns")   # ⚠️ms→us 업캐스트 함정 회피(ns 명시)
    return out


def _map_1d_idx_to_4h(df1d_index: pd.DatetimeIndex, df4h_index: pd.DatetimeIndex) -> np.ndarray:
    boundary = df1d_index + pd.Timedelta(days=1)   # ns 인덱스 + Timedelta → ns 유지 확인 필요
    assert boundary.dtype == df1d_index.dtype, f"단위 업캐스트 발생: {boundary.dtype} vs {df1d_index.dtype}"
    idx4h = df4h_index.to_numpy()
    pos = np.searchsorted(idx4h, boundary.to_numpy(), side="left")
    return pos


def run_alt_1d_ema():
    print("--- (A) 1d EMA20/50 확인 매핑판 ---")
    df1d = _load_klines_1d()
    df1d = df1d.copy()
    df1d.index = df1d.index.as_unit("ns")
    sig4h = common.build_signals()   # agree/agree_pctile 는 4h 그대로 재사용
    df4h = sig4h.df4h

    ema_f_1d = ind.ema(df1d["close"], common.EMA_FAST)
    ema_s_1d = ind.ema(df1d["close"], common.EMA_SLOW)
    ema_f = ema_f_1d.to_numpy(float)
    ema_s = ema_s_1d.to_numpy(float)
    n1d = len(df1d)
    prev_above = ema_f[:-1] > ema_s[:-1]
    curr_above = ema_f[1:] > ema_s[1:]
    valid = (np.isfinite(ema_f[:-1]) & np.isfinite(ema_s[:-1]) &
             np.isfinite(ema_f[1:]) & np.isfinite(ema_s[1:]))
    golden = valid & (~prev_above) & curr_above
    death = valid & prev_above & (~curr_above)
    golden_days = np.where(golden)[0] + 1
    death_days = np.where(death)[0] + 1
    events = [(t, "long") for t in golden_days] + [(t, "short") for t in death_days]
    events.sort()

    entry_pos = _map_1d_idx_to_4h(df1d.index, df4h.index)

    o4 = df4h["open"].to_numpy(float); h4 = df4h["high"].to_numpy(float)
    l4 = df4h["low"].to_numpy(float); c4 = df4h["close"].to_numpy(float)
    atr20 = sig4h.atr20.to_numpy(float)
    agree_pctile = sig4h.agree_pctile.to_numpy(float)
    n4h = len(df4h)

    settings = get_settings(); risk = RiskManager(settings)
    lev = settings.leverage_for("BTC/USDT")
    trades = []
    equity = 10_000.0
    next_avail = -1

    # 1d 크로스에도 4h EMA와 동일한 death/golden 배열이 필요(반대방향 청산 판정용) — 4h EMA 배열 재사용
    ema4_f = sig4h.ema_fast.to_numpy(float); ema4_s = sig4h.ema_slow.to_numpy(float)
    golden4, death4 = engine._ema_cross_events(ema4_f, ema4_s)
    # 1d 대안판은 "반대방향 EMA20/50 크로스"도 1d 기준으로 판정해야 일관 — 1d death/golden을
    # 4h 인덱스에 매핑(각 1d 크로스일의 진입위치를 그대로 재사용해 "그 4h봉에서 이벤트 발생"으로 표시)
    opp_at_4h_death = np.zeros(n4h, dtype=bool)
    opp_at_4h_golden = np.zeros(n4h, dtype=bool)
    for d in death_days:
        pos = entry_pos[d]
        if 0 <= pos < n4h:
            opp_at_4h_death[pos] = True
    for d in golden_days:
        pos = entry_pos[d]
        if 0 <= pos < n4h:
            opp_at_4h_golden[pos] = True

    for t, direction in events:
        gm = agree_pctile[entry_pos[t] - 1] if 0 <= entry_pos[t] - 1 < n4h else np.nan
        if not (np.isfinite(gm) and gm >= common.HI_TH):
            continue
        entry_i = int(entry_pos[t])
        if entry_i <= next_avail or entry_i >= n4h - 1:
            continue
        entry_raw = o4[entry_i]
        atr_v = atr20[entry_i - 1] if entry_i - 1 >= 0 else np.nan
        if not (np.isfinite(atr_v) and atr_v > 0 and entry_raw > 0):
            continue
        sl_dist = common.ATR_STOP_MULT * atr_v
        fill_px = engine._fill(entry_raw, direction, closing=False, fee_on=True)
        is_long = direction == "long"
        fixed_stop = fill_px - sl_dist if is_long else fill_px + sl_dist
        dirn = Direction.LONG if is_long else Direction.SHORT
        plan = risk.build_plan_with_stop("BTCUSDT", dirn, fill_px, fixed_stop, fill_px, equity, leverage=lev)
        if plan is None or plan.quantity <= 0:
            continue
        fee_entry = engine._fee(fill_px * plan.quantity, True)
        equity -= fee_entry
        opp = opp_at_4h_death if is_long else opp_at_4h_golden
        exit_i = None; exit_px = None
        j = entry_i
        while j < n4h:
            hh, ll, cl = h4[j], l4[j], c4[j]
            hit = (ll <= fixed_stop) if is_long else (hh >= fixed_stop)
            if hit:
                exit_i = j; exit_px = fixed_stop; break
            if opp[j]:
                exit_i = j; exit_px = cl; break
            j += 1
        if exit_i is None:
            exit_i = n4h - 1; exit_px = c4[exit_i]
        fill_exit = engine._fill(exit_px, direction, closing=True, fee_on=True)
        fee_exit = engine._fee(fill_exit * plan.quantity, True)
        raw = ((fill_exit - fill_px) if is_long else (fill_px - fill_exit)) * plan.quantity
        pnl = raw - fee_entry - fee_exit
        r = pnl / plan.risk_amount if plan.risk_amount > 0 else 0.0
        trades.append(dict(direction=direction, entry_time=df4h.index[entry_i], r=r))
        equity += pnl
        next_avail = exit_i

    df = pd.DataFrame(trades)
    if df.empty:
        print("1d EMA 대안판: 트레이드 0건")
        return
    is_df, oos_df, full_df = su.split_is_oos(df)
    for sub, name in [(is_df, "IS"), (oos_df, "OOS"), (full_df, "FULL")]:
        t, p, n = su.t_stat(sub)
        print(f"1d EMA대안 {name:4s} n={n:4d} PF(R)={su.pf_r(sub):.3f} t={t:+.3f}")


def run_alt_zero_diff():
    print("--- (B) zero-diff 분모제외 대안 ---")
    df4h = common.load_klines_4h()
    m5 = common.load_metrics_5m()
    oi_4h = common.oi_4h_from_5m(m5, df4h.index)
    d_price = df4h["close"].diff()
    d_oi = oi_4h.diff()
    sign_price = np.sign(d_price)
    sign_oi = np.sign(d_oi)
    valid_nonzero = d_price.notna() & d_oi.notna() & (sign_price != 0) & (sign_oi != 0)
    same = (sign_price == sign_oi) & valid_nonzero
    same_f = same.astype(float)
    same_f[~valid_nonzero] = np.nan   # NaN인 봉은 분모에서 자동 제외(rolling mean 이 skipna)
    agree_b = same_f.rolling(common.AGREE_WINDOW, min_periods=max(5, common.AGREE_WINDOW // 2)).mean()
    norm_bars = common.AGREE_NORM_DAYS * 6
    agree_pctile_b = common.rolling_pctile(agree_b, norm_bars)

    sig_base = common.build_signals()
    sig_alt = common.Signals(**{**sig_base.__dict__, "agree": agree_b, "agree_pctile": agree_pctile_b})
    df_alt = None
    cfg = engine.RunConfig(gate="base", fee_on=True)
    trades = engine.run_config(sig_alt, cfg)
    df_alt = su.trades_df(trades)
    if df_alt.empty:
        print("zero-diff 대안판: 트레이드 0건")
        return
    is_df, oos_df, full_df = su.split_is_oos(df_alt)
    for sub, name in [(is_df, "IS"), (oos_df, "OOS"), (full_df, "FULL")]:
        t, p, n = su.t_stat(sub)
        print(f"zero-diff대안 {name:4s} n={n:4d} PF(R)={su.pf_r(sub):.3f} t={t:+.3f}")
