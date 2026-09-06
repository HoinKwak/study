"""§사전 폐기조건 (f): 대조군①(게이트없음) 대비 표본수 맞춤 부트스트랩.
base(OOS n=14) 의 평균 net_R 이 gate_none(OOS n=79) 에서 무작위로 14개씩 뽑은 표본 평균들의
분포 중 몇 백분위에 해당하는지 계산."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import OOS_START, OOS_END

RNG = np.random.default_rng(20260906)
N_BOOT = 20000


def main():
    base = pd.read_csv("out_trades_base.csv", parse_dates=["entry_time"])
    none = pd.read_csv("out_trades_gate_none.csv", parse_dates=["entry_time"])
    base_oos = base[(base["entry_time"] >= OOS_START) & (base["entry_time"] <= OOS_END)]
    none_oos = none[(none["entry_time"] >= OOS_START) & (none["entry_time"] <= OOS_END)]

    n = len(base_oos)
    base_mean = base_oos["net_R"].mean()
    pool = none_oos["net_R"].to_numpy()

    boot_means = np.array([RNG.choice(pool, size=n, replace=True).mean() for _ in range(N_BOOT)])
    percentile = float((boot_means <= base_mean).mean() * 100)

    print(f"base OOS net_R 평균: {base_mean:.4f} (n={n})")
    print(f"gate_none 풀(OOS n={len(pool)})에서 표본수 맞춤 부트스트랩 {N_BOOT}회")
    print(f"base 평균이 위치한 백분위: {percentile:.2f}")
    print(f"부트스트랩 평균±표준편차: {boot_means.mean():.4f} ± {boot_means.std():.4f}")

    out = {"n": int(n), "base_mean_net_R": float(base_mean), "percentile": percentile,
          "boot_mean": float(boot_means.mean()), "boot_std": float(boot_means.std())}
    with open("out_diag_bootstrap.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
