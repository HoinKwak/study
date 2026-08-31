"""룩어헤드 절단 테스트: 데이터를 임의 시점에서 잘라 신호를 다시 계산해도 절단 이전 구간의
streak_up/streak_down/donchian/ema1d 값이 전체 데이터로 계산한 값과 동일한지 확인(여러 종목)."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import common

CUT = pd.Timestamp("2024-03-15", tz="UTC")

for sym in ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT"]:
    full = common.build_signals(sym)
    df4h_full = common.load_klines_4h(sym)
    df1d_full = common.load_klines_1d(sym)
    df4h_cut = df4h_full[df4h_full.index < CUT]
    df1d_cut = df1d_full[df1d_full.index < CUT]

    count_cut = df4h_cut["count"].to_numpy(float)
    su_cut, sd_cut = common.count_streak(count_cut)
    don_hi_cut, don_lo_cut = common.donchian(df4h_cut, 20)
    ema1d_cut = common.ema1d_on_4h(df4h_cut, df1d_cut, 50)

    n_cut = len(df4h_cut)
    check_upto = n_cut - 5   # 절단 경계 바로 앞 5봉은 여유로 제외

    full_su = full.streak_up[:check_upto]
    full_sd = full.streak_down[:check_upto]
    full_don_hi = full.don_hi[:check_upto]
    full_ema = full.ema1d.to_numpy()[:check_upto]

    ok_su = np.allclose(full_su, su_cut[:check_upto], equal_nan=True)
    ok_sd = np.allclose(full_sd, sd_cut[:check_upto], equal_nan=True)
    ok_don = np.allclose(full_don_hi, don_hi_cut[:check_upto], equal_nan=True)
    ok_ema = np.allclose(full_ema, ema1d_cut.to_numpy()[:check_upto], equal_nan=True)
    print(f"{sym}: streak_up 일치={ok_su} streak_down 일치={ok_sd} donchian_hi 일치={ok_don} "
         f"ema1d 일치={ok_ema} (절단전 bars={check_upto})")
    if not (ok_su and ok_sd and ok_don and ok_ema):
        for name, a, b in [("su", full_su, su_cut[:check_upto]), ("sd", full_sd, sd_cut[:check_upto]),
                           ("don", full_don_hi, don_hi_cut[:check_upto]),
                           ("ema", full_ema, ema1d_cut.to_numpy()[:check_upto])]:
            diff_idx = np.where(~np.isclose(a, b, equal_nan=True))[0]
            if len(diff_idx):
                print(f"  [{name}] 차이 인덱스 예시:", diff_idx[:5])
