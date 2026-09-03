"""metrics create_time 정시정렬(지터) 실측 — 직전 라운드 fundingRate calc_time +0~31ms 지터
사고 재발 여부 확인."""
from __future__ import annotations

import pandas as pd

import common as c


def main():
    for sym in ["BTCUSDT", "DOGEUSDT", "ADAUSDT"]:
        m5 = c.load_metrics_5m(sym)
        idx = m5.index
        # 초/마이크로초 성분이 전부 0인지 확인(지터가 있으면 0이 아닌 값이 섞임)
        sec = idx.second
        micro = idx.microsecond
        minute_mod5 = idx.minute % 5
        n_bad_sec = int((sec != 0).sum())
        n_bad_micro = int((micro != 0).sum())
        n_bad_minute = int((minute_mod5 != 0).sum())
        print(f"{sym}: n={len(idx)} 초!=0 인 행={n_bad_sec} 마이크로초!=0={n_bad_micro} "
             f"5분경계아님={n_bad_minute}")
    print("\n결론: 전부 0이면 metrics create_time 은 정시(5분배수, 초=00) 정렬 확정 — "
         "funding calc_time 과 달리 지터 없음. floor/merge_asof 대신 정확일치 resample 사용해도 무방.")


if __name__ == "__main__":
    main()
