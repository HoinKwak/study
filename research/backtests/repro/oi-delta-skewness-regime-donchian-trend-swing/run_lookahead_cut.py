"""룩어헤드 절단 테스트: 데이터를 임의 시점에서 잘라 신호를 다시 계산해도 절단 이전 구간의
skew_oi/pctile_skew/donchian 값이 전체 데이터로 계산한 값과 동일한지 확인 (여러 종목)."""
import sys

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiskew")
import numpy as np
import pandas as pd
import common

CUT = pd.Timestamp("2024-03-15", tz="UTC")

for sym in ["BTCUSDT", "ETHUSDT", "XRPUSDT"]:
    full = common.build_signals(sym)
    # 절단판: klines/metrics 를 CUT 이전까지만 남기고 다시 신호 생성
    df_full = common.load_klines_4h(sym)
    m5_full = common.load_metrics_5m(sym)
    df_cut = df_full[df_full.index < CUT]
    m5_cut = m5_full[m5_full.index < CUT]

    oi4h = common.oi_4h_from_5m(m5_cut)
    dfj = df_cut.join(oi4h, how="left")
    delta_oi = dfj["oi"].diff()
    skew_arr = common.rolling_skew_biased(delta_oi.to_numpy(float), 60)
    pctile_arr = common.rolling_percentile_rank(skew_arr, 180 * 6)
    don_hi, don_lo = common.donchian(dfj, 20)

    # 절단 이전 구간(워밍업 이후, 절단 시점에서 좀 더 여유) 비교
    n_cut = len(dfj)
    check_upto = n_cut - 5   # 절단 경계 바로 앞 5봉 정도는 제외(여유), 그 이전은 완전 동일해야 함
    full_skew = full.skew_oi.to_numpy()[:check_upto]
    full_pctile = full.pctile_skew.to_numpy()[:check_upto]
    full_don_hi = full.don_hi[:check_upto]

    ok_skew = np.allclose(full_skew, skew_arr[:check_upto], equal_nan=True)
    ok_pctile = np.allclose(full_pctile, pctile_arr[:check_upto], equal_nan=True)
    ok_don = np.allclose(full_don_hi, don_hi[:check_upto], equal_nan=True)
    print(f"{sym}: skew 일치={ok_skew} pctile 일치={ok_pctile} donchian_hi 일치={ok_don} "
         f"(절단전 bars={check_upto})")
    if not (ok_skew and ok_pctile and ok_don):
        # 어디서 차이나는지
        diff_idx = np.where(~np.isclose(full_skew, skew_arr[:check_upto], equal_nan=True))[0]
        print("  차이 인덱스 예시:", diff_idx[:5])
