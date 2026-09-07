"""표본수 맞춘 부트스트랩: base(그레인저 레짐) vs 대조군(게이트없음·z-score 게이트) 비교.
base 표본수만큼 대조군 풀에서 복원추출을 반복해 평균 net_R 백분위를 계산."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(20260907)


def bootstrap_percentile(base_mean: float, pool: np.ndarray, n_base: int, n_iter: int = 2000) -> float:
    if len(pool) == 0 or n_base == 0:
        return float("nan")
    means = np.array([RNG.choice(pool, size=n_base, replace=True).mean() for _ in range(n_iter)])
    return float((means < base_mean).mean() * 100.0)


def main():
    base = pd.read_csv(HERE / "out_trades_base.csv", parse_dates=["entry_time"]) \
        if (HERE / "out_trades_base.csv").exists() else pd.DataFrame()
    out = {}
    for control_name in ("gate_none", "zscore_gate"):
        fn = HERE / f"out_trades_{control_name}.csv"
        if not fn.exists():
            continue
        pool_df = pd.read_csv(fn, parse_dates=["entry_time"])
        for col in ("gross_R", "net_R"):
            if len(base) == 0 or len(pool_df) == 0:
                out[f"{control_name}_{col}"] = {"note": "표본 없음"}
                continue
            base_mean = float(base[col].mean())
            pct = bootstrap_percentile(base_mean, pool_df[col].to_numpy(), len(base))
            out[f"{control_name}_{col}"] = {"n_base": int(len(base)), "n_pool": int(len(pool_df)),
                                            "base_mean": base_mean, "percentile_of_base_in_pool": pct}
    print(json.dumps(out, indent=2))
    (HERE / "out_diag_bootstrap.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
