"""룩어헤드 절단 재실행 감사: 임의 시점에서 데이터를 절단해 squeeze_pctile·donchian 을
재계산하고, 절단 이전 시점 값이 전체이력 계산값과 bit 단위(허용오차) 일치하는지 확인."""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import load_symbol, build_daily_frame

CUTOFFS = {
    "BTCUSDT": 400,
    "ETHUSDT": 700,
    "ADAUSDT": 900,
    "XRPUSDT": 250,
    "BNBUSDT": 500,
    "SOLUSDT": 1100,
    "DOGEUSDT": 1300,
}


def main() -> None:
    all_ok = True
    for sym, cut in CUTOFFS.items():
        data = load_symbol(sym)
        full_daily = build_daily_frame(sym, data, squeeze_window=60, donchian_len=15)

        # 절단: prem_1d, price_1d 를 cut 번째 행까지만 사용(그 시점까지의 정보만)
        cut_time = full_daily.index[cut]
        data_cut = {
            "price_1d": data["price_1d"].loc[:cut_time],
            "price_4h": data["price_4h"].loc[:cut_time],
            "prem_1d": data["prem_1d"].loc[:cut_time],
        }
        cut_daily = build_daily_frame(sym, data_cut, squeeze_window=60, donchian_len=15)

        # 비교 구간: cut_daily 의 마지막 부분(윈도우 워밍업 이후) vs full_daily 동일 인덱스
        common_idx = cut_daily.index.intersection(full_daily.index)
        # 워밍업 이후만 비교(squeeze_pctile 이 non-null 인 구간)
        cmp_idx = common_idx[cut_daily.loc[common_idx, "squeeze_pctile"].notna()]
        a = cut_daily.loc[cmp_idx, "squeeze_pctile"]
        b = full_daily.loc[cmp_idx, "squeeze_pctile"]
        match = np.allclose(a.values, b.values, atol=1e-9, equal_nan=True)
        dh_a, dh_b = cut_daily.loc[cmp_idx, "donchian_high"], full_daily.loc[cmp_idx, "donchian_high"]
        dl_a, dl_b = cut_daily.loc[cmp_idx, "donchian_low"], full_daily.loc[cmp_idx, "donchian_low"]
        dh_match = np.allclose(dh_a.values, dh_b.values, atol=1e-9, equal_nan=True)
        dl_match = np.allclose(dl_a.values, dl_b.values, atol=1e-9, equal_nan=True)
        ok = match and dh_match and dl_match
        all_ok = all_ok and ok
        print(f"{sym}: cut={cut}({cut_time.date()}) 비교표본={len(cmp_idx)} "
              f"squeeze_pctile일치={match} donchian_high일치={dh_match} donchian_low일치={dl_match}")
        if not match:
            diff = (a - b).abs()
            print("  최대 오차:", diff.max())
    print("\n전체 결과:", "PASS(룩어헤드 없음)" if all_ok else "FAIL(불일치 발견 — 조사 필요)")


if __name__ == "__main__":
    main()
