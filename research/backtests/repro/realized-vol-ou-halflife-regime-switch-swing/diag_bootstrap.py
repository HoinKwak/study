"""사전 폐기조건 (d): 게이트없음(gate_none) 대비 표본수 맞춤 부트스트랩.
base(OOS n) 의 평균 net_R 이 gate_none/simple_alt(OOS n' >> n) 풀에서 무작위로 n개씩 뽑은
표본 평균 분포 중 몇 백분위인지 계산. 60백분위 미만이면 부가가치 없음으로 폐기."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import OOS_START, OOS_END

RNG = np.random.default_rng(20260907)
N_BOOT = 20000


def percentile_test(base_r: np.ndarray, pool_r: np.ndarray) -> dict:
    n = len(base_r)
    base_mean = float(base_r.mean())
    boot_means = np.array([RNG.choice(pool_r, size=n, replace=True).mean() for _ in range(N_BOOT)])
    pct = float((boot_means <= base_mean).mean() * 100)
    return {"n": int(n), "base_mean": base_mean, "percentile": pct,
            "boot_mean": float(boot_means.mean()), "boot_std": float(boot_means.std())}


def main():
    out = {}
    for mode in ["breakout", "fade"]:
        base = pd.read_csv(f"out_trades_{mode}_base.csv", parse_dates=["entry_time"])
        none_ = pd.read_csv(f"out_trades_{mode}_gate_none.csv", parse_dates=["entry_time"])
        alt = pd.read_csv(f"out_trades_{mode}_simple_alt.csv", parse_dates=["entry_time"])

        def oos(df):
            if len(df) == 0:
                return df
            return df[(df["entry_time"] >= OOS_START) & (df["entry_time"] <= OOS_END)]

        base_oos = oos(base)
        none_oos = oos(none_)
        alt_oos = oos(alt)

        r_base = base_oos["net_R"].to_numpy()
        r_none = none_oos["net_R"].to_numpy()
        r_alt = alt_oos["net_R"].to_numpy()

        res_none = percentile_test(r_base, r_none)
        res_alt = percentile_test(r_base, r_alt)
        out[mode] = {"vs_gate_none": res_none, "vs_simple_alt": res_alt}
        print(mode, "vs gate_none:", res_none)
        print(mode, "vs simple_alt:", res_alt)

    with open("out_diag_bootstrap.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
