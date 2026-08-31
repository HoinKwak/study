"""룩어헤드 점검: 데이터를 임의 시점에서 절단해도 절단 이전 구간의 신호(JR pctile·트리거)가
전구간 계산과 동일한지 확인(미래 데이터 참조 시 절단 시 값이 달라짐)."""
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oibv")
import common
import engine

CUTS = {"BTCUSDT": 900, "ETHUSDT": 700, "ADAUSDT": 400, "XRPUSDT": 250}

cfg = engine.RunConfig()
all_ok = True
for sym, cut in CUTS.items():
    sd = common.build_symbol_data(sym)
    if sd is None:
        print(f"{sym}: 데이터 없음, 스킵")
        continue
    oi_p_full, px_p_full, ret_full, atr_full = engine._build_trigger_arrays(sd, cfg)

    # 절단: d1 을 cut 이후로 자르고, oi_jr/px_jr 도 해당 날짜 이후 제거해 재계산
    cut_time = sd.d1.index[cut]
    sd_cut = common.SymbolData(
        d1=sd.d1.iloc[:cut + 1],
        oi_jr=sd.oi_jr[sd.oi_jr.index <= cut_time],
        px_jr=sd.px_jr[sd.px_jr.index <= cut_time],
        day_ret_pct=sd.day_ret_pct[sd.day_ret_pct.index <= cut_time],
        atr14_1d=sd.atr14_1d[sd.atr14_1d.index <= cut_time],
    )
    oi_p_cut, px_p_cut, ret_cut, atr_cut = engine._build_trigger_arrays(sd_cut, cfg)

    n_check = min(len(oi_p_cut), cut - 5)
    check_from = max(0, n_check - 200)  # 절단점 근처 최근 200개만 비교(워밍업 이후)
    diffs_oi = np.nansum(np.abs(oi_p_full[check_from:n_check] - oi_p_cut[check_from:n_check]) > 1e-6)
    diffs_px = np.nansum(np.abs(px_p_full[check_from:n_check] - px_p_cut[check_from:n_check]) > 1e-6)
    diffs_atr = np.nansum(np.abs(atr_full[check_from:n_check] - atr_cut[check_from:n_check]) > 1e-6)
    ok = diffs_oi == 0 and diffs_px == 0 and diffs_atr == 0
    all_ok &= ok
    print(f"{sym} cut={cut}({cut_time.date()}) 비교구간 n={n_check-check_from} "
         f"oi_pctile 불일치={diffs_oi} px_pctile 불일치={diffs_px} atr 불일치={diffs_atr} "
         f"{'OK' if ok else 'FAIL'}")

print(f"\n전체 결과: {'룩어헤드 없음 확인' if all_ok else '불일치 발견 — 룩어헤드 의심'}")
