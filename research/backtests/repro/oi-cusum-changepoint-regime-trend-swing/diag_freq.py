"""§전제 일관성 사전검토(스펙 필수): h·k(·z_window) 조합별 체인지포인트 빈도 스윕.
빈도가 파라미터에 과도하게 민감(2배 변화에 10배 이상 요동)한지 확인 — 사전 폐기조건 (c)."""
from __future__ import annotations

import itertools
import pandas as pd

from signals import build_signals
from events import raw_cp_events, gated_entries
from common import IS_START, IS_END, OOS_START, OOS_END

Z_WINDOWS = [60, 90, 120]
KS = [0.3, 0.5, 0.7, 1.0]
HS = [3.0, 4.0, 5.0, 6.0, 8.0]


def main():
    rows = []
    for zw, k, h in itertools.product(Z_WINDOWS, KS, HS):
        sig = build_signals("BTCUSDT", z_window_days=zw, k=k, h=h)
        cp = raw_cp_events(sig)
        ge = gated_entries(sig, confirm_bars=2)
        n_oos = len(ge[(ge["entry_time"] >= OOS_START) & (ge["entry_time"] <= OOS_END)])
        n_is = len(ge[(ge["entry_time"] >= IS_START) & (ge["entry_time"] <= IS_END)])
        rows.append({"z_window": zw, "k": k, "h": h, "raw_cp": len(cp),
                     "gated_is": n_is, "gated_oos": n_oos, "gated_full": n_is + n_oos})
    df = pd.DataFrame(rows)
    df.to_csv("out_diag_freq.csv", index=False)
    print(df.to_string(index=False))

    # 민감도 점검: base(90,0.5,5.0) 근방에서 k 또는 h 를 2배 변경했을 때 빈도 배율
    base = df[(df.z_window == 90) & (df.k == 0.5) & (df.h == 5.0)]["gated_full"].iloc[0]
    print("\nbase(z90,k0.5,h5.0) gated_full =", base)
    for zw, k, h in [(90, 1.0, 5.0), (90, 0.3, 5.0), (90, 0.5, 8.0), (90, 0.5, 3.0)]:
        row = df[(df.z_window == zw) & (df.k == k) & (df.h == h)]
        if len(row):
            v = row["gated_full"].iloc[0]
            ratio = v / base if base > 0 else float("nan")
            print(f"  z{zw} k{k} h{h}: gated_full={v} ratio_vs_base={ratio:.2f}")


if __name__ == "__main__":
    main()
