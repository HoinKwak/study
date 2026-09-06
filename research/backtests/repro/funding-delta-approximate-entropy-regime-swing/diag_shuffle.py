"""부호 무작위화 셔플(나이브 50/50) + 승률고정 대안검정 병행 — OOS net_R, 100회.

나이브 50/50 셔플은 승률 50%를 암묵 귀무가설로 깔아 실제 승률과 다르면 왜곡된다(CLAUDE.md
축적 교훈) — 실제 관측 승률을 유지한 채 |R| 배정만 무작위 순열하는 승률고정 검정을 병행."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import split_is_oos, win_rate
from events import build_universe
from engine import run_variant, trades_to_df


def naive_sign_shuffle(r: np.ndarray, n: int = 100, seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    obs_mean = r.mean()
    means = []
    for _ in range(n):
        signs = rng.choice([-1, 1], size=len(r))
        means.append((np.abs(r) * signs).mean())
    means = np.array(means)
    pctile = 100.0 * (means < obs_mean).mean()
    return {"obs_mean": float(obs_mean), "shuffle_pctile": float(pctile)}


def winrate_fixed_shuffle(r: np.ndarray, n: int = 100, seed: int = 7) -> dict:
    """실제 부호(승/패 여부)는 그대로 두고 |R| 값들을 트레이드 간에 무작위 재배정(페어링만 섞음)."""
    rng = np.random.default_rng(seed)
    signs = np.sign(r)
    signs[signs == 0] = 1
    abs_r = np.abs(r)
    obs_mean = r.mean()
    means = []
    for _ in range(n):
        perm = rng.permutation(abs_r)
        means.append((perm * signs).mean())
    means = np.array(means)
    pctile = 100.0 * (means < obs_mean).mean()
    return {"obs_mean": float(obs_mean), "shuffle_pctile": float(pctile),
            "win_rate": float((signs > 0).mean())}


def main() -> dict:
    uni = build_universe()
    trades = trades_to_df(run_variant(uni))
    _, oos, _ = split_is_oos(trades)
    r = oos["net_R"].to_numpy()
    out = {
        "n": len(r), "observed_win_rate": win_rate(oos["net_R"]),
        "naive_5050": naive_sign_shuffle(r),
        "winrate_fixed": winrate_fixed_shuffle(r),
    }
    print(json.dumps(out, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
