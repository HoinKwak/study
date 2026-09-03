"""빈도 실측 — 스펙 예상(종목당 연 8~25건, 7종목 합산 OOS 35~175건) 대비 CUSUM 원시 이벤트·
EMA게이트 통과 신호·실제 체결 트레이드 수를 단계별로 기록."""
from __future__ import annotations

import json

import pandas as pd

from common import SYMBOLS
from engine import build_frame, find_signals


def main() -> None:
    out = {}
    for sym in SYMBOLS:
        f = build_frame(sym)
        ev = f["events"]
        sig = find_signals(f)
        out[sym] = {
            "funding_rows_total": int(len(f["funding"])),
            "excluded_non_8h_frac": f["excluded_frac"],
            "cusum_events_raw": int(len(ev)),
            "ema_gated_signals": int(len(sig)),
        }
    with open("out_diag_freq.json", "w") as fp:
        json.dump(out, fp, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
