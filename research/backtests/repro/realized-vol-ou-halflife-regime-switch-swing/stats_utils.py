from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def pf(r: pd.Series) -> float:
    r = r.dropna()
    pos = r[r > 0].sum()
    neg = -r[r < 0].sum()
    if neg == 0:
        return float("inf") if pos > 0 else float("nan")
    return float(pos / neg)


def t_stat(r: pd.Series) -> float:
    r = r.dropna()
    if len(r) < 2:
        return float("nan")
    return float(stats.ttest_1samp(r, 0.0).statistic)


def summarize(r: pd.Series) -> dict:
    r = r.dropna()
    n = len(r)
    if n == 0:
        return {"n": 0, "PF": float("nan"), "t": float("nan"), "mean": float("nan"),
                "winrate": float("nan")}
    return {
        "n": n, "PF": pf(r), "t": t_stat(r), "mean": float(r.mean()),
        "winrate": float((r > 0).mean()),
    }


def declustered_t(trades: pd.DataFrame, r_col: str, time_col: str = "entry_time",
                   freq: str = "1D") -> dict:
    """캘린더일(또는 임의 freq) 단위로 R 을 합산해 t-검정 — 표본 부풀림 방지."""
    if len(trades) == 0:
        return {"n": 0, "t": float("nan"), "PF": float("nan")}
    g = trades.copy()
    g["_key"] = g[time_col].dt.floor(freq)
    agg = g.groupby("_key")[r_col].sum()
    return {"n": len(agg), "t": t_stat(agg), "PF": pf(agg), "mean": float(agg.mean())}


def rolling_window_declustered_t(trades: pd.DataFrame, r_col: str, time_col: str = "entry_time",
                                   window_days: int = 5) -> dict:
    """N일 롤링(고정 블록) 윈도우로 클러스터링 — 종목별 진입 타이밍이 어긋나는 경우 대비."""
    if len(trades) == 0:
        return {"n": 0, "t": float("nan"), "PF": float("nan")}
    g = trades.copy().sort_values(time_col)
    t0 = g[time_col].min().normalize()
    block = ((g[time_col] - t0).dt.days // window_days)
    agg = g.groupby(block)[r_col].sum()
    return {"n": len(agg), "t": t_stat(agg), "PF": pf(agg), "mean": float(agg.mean())}
