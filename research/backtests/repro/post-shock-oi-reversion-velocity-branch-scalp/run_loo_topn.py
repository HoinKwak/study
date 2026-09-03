"""LOO(종목별 제외) + top-N 트레이드 제거 — 기본 파라미터, OOS net R-배수 기준."""
from __future__ import annotations

import pandas as pd

import common as c
import engine
import stats_utils as su


def main():
    data = c.load_all()
    cfg = engine.Config()
    df, _ = engine.run(c.SYMBOLS, data, cfg)
    _, oos, _ = su.split_is_oos(df)
    print("=== 기준(전 종목) ===")
    print(su.print_summary(su.summary(oos, "all")))

    print("\n=== LOO(종목별 제외) ===")
    for sym in c.SYMBOLS:
        d = oos[oos["symbol"] != sym]
        print(su.print_summary(su.summary(d, f"excl-{sym}")))

    print("\n=== top-N 제거(승리 트레이드 상위 N건 제외) ===")
    oos_sorted = oos.sort_values("r_multiple", ascending=False)
    for n in [1, 3, 5, 10, 20]:
        d = oos_sorted.iloc[n:]
        print(su.print_summary(su.summary(d, f"top-{n}제거")))

    print("\n=== 최대 손실 트레이드 상위 N건 제거(대칭점검) ===")
    oos_sorted2 = oos.sort_values("r_multiple", ascending=True)
    for n in [1, 3, 5, 10, 20]:
        d = oos_sorted2.iloc[n:]
        print(su.print_summary(su.summary(d, f"worst-{n}제거")))


if __name__ == "__main__":
    main()
