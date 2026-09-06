"""§LOO — BTC 단일종목 진입이라 '종목 제외'가 성립하지 않으므로, 연도별 leave-one-year-out
으로 대체(연도 하나씩 제외하고 나머지 FULL 재계산 — 특정 연도 의존 여부 확인)."""
from __future__ import annotations

import json
import pandas as pd

from common import pf_r, t_stat


def main():
    df = pd.read_csv("out_trades_base.csv", parse_dates=["entry_time"])
    df["year"] = df["entry_time"].dt.year
    years = sorted(df["year"].unique())
    out = {"years_present": years, "n_by_year": df["year"].value_counts().sort_index().to_dict()}
    for y in years:
        rest = df[df["year"] != y]
        out[f"exclude_{y}"] = {
            "n": len(rest), "net_pf": pf_r(rest["net_R"]), "net_t": t_stat(rest["net_R"])}
    print(json.dumps(out, indent=2, default=str))
    with open("out_diag_loo_year.json", "w") as f:
        json.dump(out, f, indent=2, default=str)


if __name__ == "__main__":
    main()
