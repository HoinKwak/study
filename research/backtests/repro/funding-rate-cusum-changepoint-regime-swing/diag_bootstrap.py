"""대조군 우열 검정 — 표본수 맞춘 부트스트랩(base vs reverse, base vs nogate), OOS net_R."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import SYMBOLS
from engine import load_all, run_variant, trades_to_df


def oos_slice(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["entry_time"] >= "2024-07-01") & (df["entry_time"] <= "2026-06-30 23:59:59")]


def bootstrap_diff(a: np.ndarray, b: np.ndarray, n_iter: int = 2000, seed: int = 7) -> dict:
    """a, b 독립 표본. 표본수를 min(len(a),len(b))으로 맞춰 재표집(복원추출) 후 평균차 분포."""
    rng = np.random.default_rng(seed)
    n = min(len(a), len(b))
    diffs = []
    for _ in range(n_iter):
        sa = rng.choice(a, size=n, replace=True)
        sb = rng.choice(b, size=n, replace=True)
        diffs.append(sa.mean() - sb.mean())
    diffs = np.array(diffs)
    obs = a[:n].mean() - b[:n].mean() if False else (np.mean(a) - np.mean(b))
    p_le_0 = float((diffs <= 0).mean())
    p_ge_0 = float((diffs >= 0).mean())
    return {"n_a": len(a), "n_b": len(b), "n_matched": n, "observed_diff": float(obs),
            "boot_diff_mean": float(diffs.mean()), "boot_diff_std": float(diffs.std()),
            "p_a_le_b": p_le_0, "p_a_ge_b": p_ge_0}


def main() -> None:
    univ = load_all()
    base = trades_to_df(run_variant(univ))
    reverse = trades_to_df(run_variant(univ, reverse=True))
    nogate = trades_to_df(run_variant(univ, no_ema_gate=True))

    base_oos = oos_slice(base)["net_R"].to_numpy()
    rev_oos = oos_slice(reverse)["net_R"].to_numpy()
    nogate_oos = oos_slice(nogate)["net_R"].to_numpy()

    out = {
        "base_vs_reverse": bootstrap_diff(base_oos, rev_oos),
        "base_vs_nogate": bootstrap_diff(base_oos, nogate_oos),
    }
    with open("out_diag_bootstrap.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
