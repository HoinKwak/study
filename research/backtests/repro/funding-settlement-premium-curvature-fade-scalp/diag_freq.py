"""신호빈도 실측 — 스펙의 [추정] 연 50건/심볼(정규근사)과 실측 비교."""
from __future__ import annotations

import json

import pandas as pd

from common import SYMBOLS, load_symbol
from events import build_events

Z_THRESHOLD = 2.0


def main():
    rows = []
    for sym in SYMBOLS:
        d = load_symbol(sym)
        prem = d["prem_1m"]["close"]
        ev = build_events(prem, lookback=60)
        valid = ev[ev["c_z"].notna()]
        years = (valid["t0"].max() - valid["t0"].min()).days / 365.25 if len(valid) else float("nan")
        trig = valid[valid["c_z"].abs() >= Z_THRESHOLD]
        per_year = len(trig) / years if years else float("nan")
        long_frac = (trig["c_z"] <= -Z_THRESHOLD).mean() if len(trig) else float("nan")
        rows.append({"symbol": sym, "n_windows_total": len(ev), "n_valid_cz": len(valid),
                     "n_trigger": len(trig), "trigger_rate_pct": len(trig) / len(valid) * 100
                     if len(valid) else float("nan"), "years": years,
                     "trigger_per_year": per_year, "long_frac_of_trigger": long_frac})
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    print(f"\n스펙 [추정]: 연 ~50건/심볼(정규근사 4.55% × 연 1,095 체크포인트)")
    print(f"실측 평균 발생률: {df['trigger_rate_pct'].mean():.2f}% "
          f"(정규근사 기대 4.55%p 대비 {df['trigger_rate_pct'].mean()/4.55:.2f}배)")
    print(f"실측 평균 연간 발생건수: {df['trigger_per_year'].mean():.1f}건/종목/년")
    with open("out_diag_freq.json", "w") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2, default=str)


if __name__ == "__main__":
    main()
