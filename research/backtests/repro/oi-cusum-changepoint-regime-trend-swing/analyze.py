"""메인 분석: BTC 단일종목, OI CUSUM 체인지포인트 레짐전환 추세추종.
IS/OOS/FULL, gross/net PF(R)·t, 대조군 4+종, 사전 폐기조건 판정."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import pf_r, t_stat, win_rate, IS_START, IS_END, OOS_START, OOS_END
from signals import build_signals
from events import raw_cp_events, gated_entries
from engine import simulate_trades, trades_to_df, DEFAULT_DIRECTION_MAP
from control import gate_none_entries, build_oi_zspike_entries, price_cusum, price_cusum_entries

BASE_PARAMS = dict(z_window_days=90, k=0.5, h=5.0, ema_fast_n=20, ema_slow_n=50)
STOP_MULT = 1.5
ATR_TRAIL_MULT = 2.5
MAX_HOLD = 30
CONFIRM_BARS = 2


def split_stats(df: pd.DataFrame, tcol: str = "entry_time") -> dict:
    if len(df) == 0:
        return {"n": 0}
    is_df = df[(df[tcol] >= IS_START) & (df[tcol] <= IS_END)]
    oos_df = df[(df[tcol] >= OOS_START) & (df[tcol] <= OOS_END)]
    full_df = df[(df[tcol] >= IS_START) & (df[tcol] <= OOS_END)]
    out = {}
    for name, d in [("is", is_df), ("oos", oos_df), ("full", full_df)]:
        out[name] = {
            "n": len(d),
            "pf_net": pf_r(d["net_R"]) if len(d) else float("nan"),
            "t_net": t_stat(d["net_R"]) if len(d) else float("nan"),
            "pf_gross": pf_r(d["gross_R"]) if len(d) else float("nan"),
            "t_gross": t_stat(d["gross_R"]) if len(d) else float("nan"),
            "win_rate": win_rate(d["net_R"]) if len(d) else float("nan"),
        }
    return out


def main():
    sig = build_signals("BTCUSDT", **BASE_PARAMS)
    raw_cp = raw_cp_events(sig)
    entries = gated_entries(sig, confirm_bars=CONFIRM_BARS)
    entries.to_csv("out_entries_base.csv", index=False)
    raw_cp.to_csv("out_raw_cp_btc.csv", index=False)

    results = {}

    # --- base (스펙 문언 그대로: up=롱, down=숏 추세추종) ---
    trades_base = simulate_trades(sig, entries, DEFAULT_DIRECTION_MAP, stop_mult=STOP_MULT,
                                   atr_trail_mult=ATR_TRAIL_MULT, max_hold_bars=MAX_HOLD,
                                   raw_cp=raw_cp)
    df_base = trades_to_df(trades_base)
    df_base.to_csv("out_trades_base.csv", index=False)
    results["base"] = split_stats(df_base)

    # --- 반전 대조군 (④, 원신호 기준 대칭재배치 + 청산조건도 방향에 맞게 반전) ---
    trades_rev = simulate_trades(sig, entries, DEFAULT_DIRECTION_MAP, stop_mult=STOP_MULT,
                                  atr_trail_mult=ATR_TRAIL_MULT, max_hold_bars=MAX_HOLD,
                                  reverse=True, raw_cp=raw_cp)
    df_rev = trades_to_df(trades_rev)
    df_rev.to_csv("out_trades_reverse.csv", index=False)
    results["reverse"] = split_stats(df_rev)
    # 신호 중첩률(반전은 같은 entries 를 그대로 반대방향으로 매매하므로 100% — 명시)
    results["reverse_signal_overlap_frac"] = 1.0  # 동일 entries 를 재사용(방향만 반전)

    # --- 컨트래리언 방향 대안 (스펙이 우려한 "하방CP=청산캐스케이드->컨트래리언 롱") ---
    contra_map = {"up": 1, "down": 1}
    trades_contra = simulate_trades(sig, entries, contra_map, stop_mult=STOP_MULT,
                                     atr_trail_mult=ATR_TRAIL_MULT, max_hold_bars=MAX_HOLD,
                                     raw_cp=raw_cp)
    df_contra = trades_to_df(trades_contra)
    df_contra.to_csv("out_trades_contrarian_down.csv", index=False)
    results["contrarian_down_long"] = split_stats(df_contra)

    # --- ① 게이트없음(순수 EMA20/50 크로스) ---
    entries_none = gate_none_entries(sig)
    entries_none.to_csv("out_entries_gate_none.csv", index=False)
    trades_none = simulate_trades(sig, entries_none, DEFAULT_DIRECTION_MAP, stop_mult=STOP_MULT,
                                   atr_trail_mult=ATR_TRAIL_MULT, max_hold_bars=MAX_HOLD,
                                   raw_cp=entries_none.rename(columns={})[["cp_bar", "cp_time", "cp_type"]]
                                   if len(entries_none) else None)
    df_none = trades_to_df(trades_none)
    df_none.to_csv("out_trades_gate_none.csv", index=False)
    results["gate_none"] = split_stats(df_none)

    # --- ② OI 단순 z-score 스파이크 게이트 ---
    entries_zsp = build_oi_zspike_entries(sig, z_thresh=2.0, confirm_bars=CONFIRM_BARS)
    entries_zsp.to_csv("out_entries_oi_zspike.csv", index=False)
    zsp_raw = entries_zsp[["cp_bar", "cp_time", "cp_type"]].drop_duplicates() if len(entries_zsp) else None
    trades_zsp = simulate_trades(sig, entries_zsp, DEFAULT_DIRECTION_MAP, stop_mult=STOP_MULT,
                                  atr_trail_mult=ATR_TRAIL_MULT, max_hold_bars=MAX_HOLD,
                                  raw_cp=zsp_raw)
    df_zsp = trades_to_df(trades_zsp)
    df_zsp.to_csv("out_trades_oi_zspike.csv", index=False)
    results["oi_zspike_gate"] = split_stats(df_zsp)

    # --- ③ 가격 CUSUM 신호원 교체 ---
    price_cp = price_cusum(sig, **{k: v for k, v in BASE_PARAMS.items() if k in ("z_window_days", "k", "h")})
    price_cp.to_csv("out_price_cusum_btc.csv", index=False)
    entries_pc = price_cusum_entries(sig, price_cp, confirm_bars=CONFIRM_BARS)
    entries_pc.to_csv("out_entries_price_cusum.csv", index=False)
    pc_raw = price_cp if len(price_cp) else None
    trades_pc = simulate_trades(sig, entries_pc, DEFAULT_DIRECTION_MAP, stop_mult=STOP_MULT,
                                 atr_trail_mult=ATR_TRAIL_MULT, max_hold_bars=MAX_HOLD,
                                 raw_cp=pc_raw)
    df_pc = trades_to_df(trades_pc)
    df_pc.to_csv("out_trades_price_cusum.csv", index=False)
    results["price_cusum_gate"] = split_stats(df_pc)

    # --- 빈도 요약 ---
    results["freq"] = {
        "raw_cp_full": len(raw_cp),
        "gated_entries_full": len(entries),
        "gated_is": int(((entries["entry_time"] >= IS_START) & (entries["entry_time"] <= IS_END)).sum()),
        "gated_oos": int(((entries["entry_time"] >= OOS_START) & (entries["entry_time"] <= OOS_END)).sum()),
    }

    with open("out_summary.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
