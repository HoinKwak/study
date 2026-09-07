"""1차 진단: 신호빈도 실측 — lag×p_sig 3×3 스윕(사전 등록 최우선 확인 지점 ①②).

base(gc_window=60,gc_lag=4,p_sig=0.05,p_insig=0.10)의 문자 그대로의 전환 정의
(직전 봉 대비 'OI 선행'→'거래대금 선행')이 7종목 전체·4.5년에 걸쳐 몇 건이나 발생하는지
실측한다. 스카우트 예상(종목당 연 15~40건)과 비교."""
from __future__ import annotations

import json
from pathlib import Path

from common import SYMBOLS
from signals import build_signals

HERE = Path(__file__).resolve().parent


def main():
    results = []
    for lag in (2, 4, 8):
        for psig in (0.01, 0.05, 0.10):
            total = 0
            per_sym = {}
            for sym in SYMBOLS:
                sig = build_signals(sym, gc_lag=lag, p_sig=psig)
                n = int(sig.transition_qv.sum())
                per_sym[sym] = n
                total += n
            results.append({"lag": lag, "p_sig": psig, "total": total, "per_symbol": per_sym})
            print(lag, psig, total, per_sym)
    (HERE / "out_diag_freq.json").write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
