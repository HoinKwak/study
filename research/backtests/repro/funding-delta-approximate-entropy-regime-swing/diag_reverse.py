"""반전 대조군 — SL/TP 대칭 재배치(engine.py 가 risk_distance 기준 대칭, direction 뒤집기만)
+ 레짐붕괴 청산은 방향 미참조 스칼라라 반전에도 불변(§engine.py 주석). 신호 중첩률 실측."""
from __future__ import annotations

import json

import pandas as pd

from common import pf_r, t_stat, split_is_oos
from events import build_universe
from engine import run_variant, trades_to_df


def main() -> dict:
    uni = build_universe()
    fwd = trades_to_df(run_variant(uni, reverse=False))
    rev = trades_to_df(run_variant(uni, reverse=True))

    _, fwd_oos, _ = split_is_oos(fwd)
    _, rev_oos, _ = split_is_oos(rev)

    # 신호 중첩 — 반전은 동일 signal_time 후보군에 trade_dir 만 뒤집는 구조이나, 순차체결(단일
    # 포지션) 특성상 포지션 보유상태가 방향별로 달라 실제 "체결된" entry_time 집합은 달라질 수
    # 있음(9/5 12:06Z 라운드 발견 구조) — 실현 entry_time 교집합으로 중첩률 실측.
    fwd_entries = set(zip(fwd_oos["symbol"], fwd_oos["entry_time"]))
    rev_entries = set(zip(rev_oos["symbol"], rev_oos["entry_time"]))
    overlap = len(fwd_entries & rev_entries)
    overlap_frac_fwd = overlap / len(fwd_entries) if fwd_entries else float("nan")
    overlap_frac_rev = overlap / len(rev_entries) if rev_entries else float("nan")

    out = {
        "fwd": {"n": len(fwd_oos), "pf_net": pf_r(fwd_oos["net_R"]), "t_net": t_stat(fwd_oos["net_R"]),
                "pf_gross": pf_r(fwd_oos["gross_R"]), "t_gross": t_stat(fwd_oos["gross_R"])},
        "rev": {"n": len(rev_oos), "pf_net": pf_r(rev_oos["net_R"]), "t_net": t_stat(rev_oos["net_R"]),
                "pf_gross": pf_r(rev_oos["gross_R"]), "t_gross": t_stat(rev_oos["gross_R"])},
        "overlap_n": overlap, "overlap_frac_of_fwd": overlap_frac_fwd,
        "overlap_frac_of_rev": overlap_frac_rev,
    }
    print(json.dumps(out, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
