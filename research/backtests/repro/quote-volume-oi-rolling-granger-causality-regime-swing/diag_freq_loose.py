"""보조 진단: 완화된 전환 정의(events_loose.py)의 신호빈도를 lookback 값별로 실측."""
from __future__ import annotations

import json
from pathlib import Path

from common import SYMBOLS
from signals import build_signals
from events_loose import loose_gated_entries

HERE = Path(__file__).resolve().parent


def main():
    out = {}
    for lookback in (3, 5, 10):
        total = 0
        per_sym = {}
        for sym in SYMBOLS:
            sig = build_signals(sym)  # base gc params
            ent = loose_gated_entries(sig, lookback=lookback)
            per_sym[sym] = int(len(ent))
            total += len(ent)
        out[lookback] = {"total": total, "per_symbol": per_sym}
        print(lookback, total, per_sym)
    (HERE / "out_diag_freq_loose.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
