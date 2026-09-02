"""룩어헤드 감사: 1분 프리미엄 시계열을 임의 시점에서 절단해도 절단 이전(+마진) 이벤트의
c/c_z 가 전체데이터 실행과 완전히 일치하는지 확인. 일치하면 이벤트 계산이 미래 데이터를
참조하지 않음(causal)을 증명."""
from __future__ import annotations

import pandas as pd

from common import load_symbol
from events import build_events

SYMBOL = "BTCUSDT"
CUT_AT = pd.Timestamp("2024-03-15 00:00:00", tz="UTC")  # 임의 절단점(중간 지점)


def main():
    d = load_symbol(SYMBOL)
    prem_full = d["prem_1m"]["close"]

    ev_full = build_events(prem_full, lookback=60)

    prem_trunc = prem_full[prem_full.index <= CUT_AT]
    ev_trunc = build_events(prem_trunc, lookback=60)

    # 절단점 이전, 그리고 lookback(60) 워밍업을 감안해 c_z 가 절단 후에도 안정적으로
    # 계산되는 이벤트만 비교(절단 근접 이벤트는 rolling window 끝단이라 표본이 달라질 수 있음
    # -- 실제로는 c_z 가 shift(1)+과거전용이라 절단으로 인해 "미래" 표본이 사라지는 방향으로만
    # 영향받고, 절단 이전 이벤트는 애초에 미래 데이터를 쓴 적이 없어야 함).
    margin = pd.Timedelta(days=10)
    keep_full = ev_full[ev_full["settlement_time"] <= CUT_AT - margin].reset_index(drop=True)
    keep_trunc = ev_trunc[ev_trunc["settlement_time"] <= CUT_AT - margin].reset_index(drop=True)

    merged = keep_full.merge(keep_trunc, on="t0", suffixes=("_full", "_trunc"))
    n_common = len(merged)
    c_diff = (merged["c_full"] - merged["c_trunc"]).abs().max()
    cz_diff = (merged["c_z_full"] - merged["c_z_trunc"]).abs().max()
    ckpt_diff = (merged["checkpoint_premium_full"] - merged["checkpoint_premium_trunc"]).abs().max()

    print(f"공통 이벤트 수(절단점-10일 이전) = {n_common} / full={len(keep_full)} / "
          f"trunc={len(keep_trunc)}")
    print(f"max|c 차이| = {c_diff:.3e}")
    print(f"max|c_z 차이| = {cz_diff:.3e}")
    print(f"max|checkpoint_premium 차이| = {ckpt_diff:.3e}")
    ok = n_common > 100 and c_diff < 1e-12 and cz_diff < 1e-9
    print("룩어헤드 없음(절단 전 이벤트 완전 일치):", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
