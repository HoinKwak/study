"""§1단계(스펙 필수): 방향을 예단하지 말고 체인지포인트 발생 후 N봉 방향별 승률/평균수익률을
게이트 없이(EMA 확인 없이) 집계 — BTC 단독, IS+OOS 전체구간(FULL), IS 만 분리해서도 확인
(과최적화 방지 — 방향 결정은 IS 데이터만으로 내려야 하나, 참고용으로 FULL 도 병기).

CP 발생 시점(cp_bar 종가, 곧 그 다음 봉 시가)에서 N봉 뒤 종가까지 로그수익률을 계산해
CP 타입별(up/down) 평균·승률(롱 관점)을 본다. 평균이 양(+)이면 "롱"이 유리, 음(-)이면
"숏"(또는 반대: 하방 CP 뒤 롱=컨트래리언)이 유리하다는 뜻.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from signals import build_signals
from events import raw_cp_events
from common import IS_START, IS_END, OOS_START, OOS_END


def forward_returns(sig, cp_df: pd.DataFrame, horizons=(2, 6, 12, 30)) -> pd.DataFrame:
    n = len(sig.df)
    close = sig.df["close"].to_numpy()
    idx = sig.df.index
    rows = []
    for _, r in cp_df.iterrows():
        i = int(r["cp_bar"])
        entry_bar = i + 1
        if entry_bar >= n:
            continue
        entry_px = close[entry_bar - 1] if entry_bar - 1 >= 0 else np.nan  # 진입가 근사(직전종가)
        row = {"cp_bar": i, "cp_time": idx[i], "cp_type": r["cp_type"]}
        for hz in horizons:
            j = entry_bar + hz - 1
            if j >= n:
                row[f"ret_{hz}"] = np.nan
                continue
            row[f"ret_{hz}"] = float(np.log(close[j] / close[entry_bar]))
        rows.append(row)
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame, horizons=(2, 6, 12, 30)) -> pd.DataFrame:
    out = []
    for cp_type in ["up", "down"]:
        sub = df[df["cp_type"] == cp_type]
        for hz in horizons:
            col = f"ret_{hz}"
            s = sub[col].dropna()
            if len(s) == 0:
                continue
            out.append({
                "cp_type": cp_type, "horizon_bars": hz, "n": len(s),
                "mean_ret": s.mean(), "win_rate_long": float((s > 0).mean()),
                "t_stat": (s.mean() / (s.std(ddof=1) / np.sqrt(len(s)))) if len(s) > 1 and s.std(ddof=1) > 0 else np.nan,
            })
    return pd.DataFrame(out)


def main():
    sig = build_signals("BTCUSDT")
    cp_all = raw_cp_events(sig)
    print("BTC 원시 체인지포인트 수:", len(cp_all), "| up:", (cp_all["cp_type"] == "up").sum(),
          "down:", (cp_all["cp_type"] == "down").sum())

    fr = forward_returns(sig, cp_all)
    fr_full = fr[(fr["cp_time"] >= IS_START) & (fr["cp_time"] <= OOS_END)]
    fr_is = fr[(fr["cp_time"] >= IS_START) & (fr["cp_time"] <= IS_END)]

    print("\n=== FULL 구간(IS+OOS) ===")
    print(summarize(fr_full).to_string(index=False))
    print("\n=== IS 구간만(방향 결정은 이 표 기준) ===")
    print(summarize(fr_is).to_string(index=False))

    fr_full.to_csv("out_diag_direction_full.csv", index=False)
    fr_is.to_csv("out_diag_direction_is.csv", index=False)
    summarize(fr_full).to_csv("out_diag_direction_summary_full.csv", index=False)
    summarize(fr_is).to_csv("out_diag_direction_summary_is.csv", index=False)


if __name__ == "__main__":
    main()
