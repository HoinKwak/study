"""리뷰어 추가 검증 — 스펙 헤더 "1d 확인" 게이트를 문자 그대로 구현해 재실행.

설계: 1d 종가가 causal 1d EMA20(전일 확정치만 사용, merge_asof backward, "가용시각"=
daily open_time+1일으로 lookahead 원천 차단) 위/아래에 있어야 그 방향 신호를 채택.
브레이크아웃(추세추종): 롱은 1d close > 1d ema20, 숏은 1d close < 1d ema20.
페이드(평균회귀): "1d 확인"의 자연스러운 해석은 동일(추세방향 필터)로 두되, 반대해석
(과열이므로 1d 추세 반대일 때만 채택)도 별도 실행해 설계판단 편향 여부를 확인한다.
"""
from __future__ import annotations
import json
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, ".")
from common import SYMBOLS, IS_START, IS_END, OOS_START, OOS_END, load_klines_4h, ema
from signals import build_signals
from engine import simulate_symbol, trades_to_df
from stats_utils import summarize, declustered_t, rolling_window_declustered_t
from analyze import split_is_oos, report_mode


def daily_ema20_causal(df4h: pd.DataFrame) -> pd.Series:
    """4h 데이터에서 1d 리샘플 후 EMA20(daily) 계산, 가용시각을 다음날 00:00으로 설정해
    merge_asof backward로 4h 인덱스에 causal 정렬."""
    daily = df4h["close"].resample("1D").last().dropna()
    daily_ema = ema(daily, 20)
    avail = daily_ema.index + pd.Timedelta(days=1)
    daily_df = pd.DataFrame({"avail": avail, "ema1d": daily_ema.values}).sort_values("avail")
    left = pd.DataFrame({"ts": df4h.index}).sort_values("ts")
    merged = pd.merge_asof(left, daily_df, left_on="ts", right_on="avail", direction="backward")
    merged = merged.set_index("ts").reindex(df4h.index)
    return merged["ema1d"]


def run_gated(mode: str, gate_mode: str = "trend_align"):
    all_trades = []
    for sym in SYMBOLS:
        df = load_klines_4h(sym)
        ind = build_signals(df)
        ema1d = daily_ema20_causal(df)
        close = ind["close"]
        dir_col = "raw_breakout_dir" if mode == "breakout" else "raw_fade_dir"
        directions = ind[dir_col].copy()
        trend_up = close > ema1d
        trend_dn = close < ema1d
        if gate_mode == "trend_align":
            ok_long = trend_up
            ok_short = trend_dn
        else:  # "trend_oppose" -- fade 반대해석
            ok_long = trend_dn
            ok_short = trend_up
        keep = pd.Series(0, index=directions.index, dtype="int64")
        keep = keep.where(~((directions == 1) & ok_long.fillna(False)), 1)
        keep = keep.where(~((directions == -1) & ok_short.fillna(False)), -1)
        trades = simulate_symbol(sym, mode, ind[["open", "high", "low", "close"]], ind["atr14"],
                                  ind["dev"], keep)
        all_trades.extend(trades)
    return trades_to_df(all_trades)


def main():
    results = {}
    for mode in ["breakout", "fade"]:
        trades = run_gated(mode, "trend_align")
        trades.to_csv(f"out_trades_{mode}_1dgate_align.csv", index=False)
        results[f"{mode}_align"] = report_mode(trades, f"{mode}_1dgate_align")
        splits = split_is_oos(trades)
        oos = splits["OOS"]
        if len(oos):
            dc = declustered_t(oos, "net_R")
            rw5 = rolling_window_declustered_t(oos, "net_R", window_days=5)
            results[f"{mode}_align"]["OOS_declustered_1d"] = dc
            results[f"{mode}_align"]["OOS_declustered_5d"] = rw5
            print(f"{mode} align OOS declustered 1d:", dc, "5d:", rw5)

    # fade 반대해석(과열 후 1d추세 반대일 때만)도 확인
    trades_f2 = run_gated("fade", "trend_oppose")
    results["fade_oppose"] = report_mode(trades_f2, "fade_1dgate_oppose")
    splits = split_is_oos(trades_f2)
    oos = splits["OOS"]
    if len(oos):
        dc = declustered_t(oos, "net_R")
        rw5 = rolling_window_declustered_t(oos, "net_R", window_days=5)
        results["fade_oppose"]["OOS_declustered_1d"] = dc
        results["fade_oppose"]["OOS_declustered_5d"] = rw5
        print("fade oppose OOS declustered 1d:", dc, "5d:", rw5)

    with open("out_diag_1dgate.json", "w") as f:
        json.dump(results, f, indent=2, default=str)


if __name__ == "__main__":
    main()
