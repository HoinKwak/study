"""진단: wick_asym>=0.4 나이브 발생률, 결합조건 실측확률(나이브/직관 추정 대조), 8h 정산
오프셋(00/08/16 UTC 근접 위상)별 wick_asym 분포 — 사전 폐기조건 (e) 판정용."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import SYMBOLS, load_symbol, wick_asym
from engine import build_frame, find_signals


def main() -> None:
    naive_rates = []
    freq_rows = []
    offset_rows = []

    for sym in SYMBOLS:
        data = load_symbol(sym)
        prem = data["prem_4h"]
        wa = wick_asym(prem)
        valid = wa.dropna()
        p_upper = float((valid >= 0.4).mean())
        p_lower = float((valid <= -0.4).mean())
        naive_rates.append({"symbol": sym, "n": len(valid), "p_wick_upper>=0.4": p_upper,
                             "p_wick_lower<=-0.4": p_lower})

        # 4h 봉의 UTC 시(hour)로 8h 정산 위상 분류: 정산시각 자체(00/08/16)=offset0,
        # +4h(04/12/20)=offset1(정산 직전 봉)
        hours = valid.index.hour
        offset = np.where(np.isin(hours, [0, 8, 16]), "at_settlement(00/08/16h)",
                          "pre_settlement(04/12/20h)")
        odf = pd.DataFrame({"wick_asym": valid.values, "offset": offset}, index=valid.index)
        for off_label, sub in odf.groupby("offset"):
            offset_rows.append({
                "symbol": sym, "offset": off_label, "n": len(sub),
                "p_upper": float((sub["wick_asym"] >= 0.4).mean()),
                "p_lower": float((sub["wick_asym"] <= -0.4).mean()),
                "mean_wick_asym": float(sub["wick_asym"].mean()),
            })

        # 결합조건 실측: 최종 진입조건 전체(consec>=4/6 AND premium 부호 AND ext>=5%)
        frame = build_frame(sym)
        n_total = len(frame["prem"].dropna(subset=["consec_upper", "ext_pct"]))
        signals = find_signals(frame)
        n_short = sum(1 for s in signals if s[1] == -1)
        n_long = sum(1 for s in signals if s[1] == 1)
        years = n_total * 4 / 24 / 365.25
        freq_rows.append({
            "symbol": sym, "n_bars_valid": n_total, "years_approx": round(years, 2),
            "n_signals_short": n_short, "n_signals_long": n_long,
            "signals_per_year": round((n_short + n_long) / years, 2) if years > 0 else None,
        })

    naive_df = pd.DataFrame(naive_rates)
    freq_df = pd.DataFrame(freq_rows)
    offset_df = pd.DataFrame(offset_rows)

    print("=== wick_asym 나이브 발생률(>=0.4 / <=-0.4) ===")
    print(naive_df.to_string(index=False))
    print("\n=== 8h 정산 오프셋별 분포(사전 폐기조건 e 판정용) ===")
    print(offset_df.to_string(index=False))
    print("\n=== 최종 결합조건 실측 신호 빈도(종목당 연간) ===")
    print(freq_df.to_string(index=False))

    # 폐기조건 (e): 오프셋 조건화 없이 재집계했을 때 특정 오프셋에 신호 70% 이상 쏠리는지
    # -> "신호"(결합조건 전체가 아니라 wick_asym>=th 원재료 자체)의 오프셋 쏠림을 본다.
    at_settle = offset_df[offset_df["offset"] == "at_settlement(00/08/16h)"]
    pre_settle = offset_df[offset_df["offset"] == "pre_settlement(04/12/20h)"]
    tot_upper_at = (at_settle["n"] * at_settle["p_upper"]).sum()
    tot_upper_pre = (pre_settle["n"] * pre_settle["p_upper"]).sum()
    frac_at = tot_upper_at / (tot_upper_at + tot_upper_pre) if (tot_upper_at + tot_upper_pre) > 0 else float("nan")
    print(f"\n정산시각(00/08/16h) 봉에 몰린 upper-wick 이벤트 비율: {frac_at:.3f} "
          f"(폐기조건 (e): >=0.70 이면 정산 아티팩트로 폐기)")

    out = {"naive_rates": naive_rates, "offset_rows": offset_rows, "freq_rows": freq_rows,
           "frac_upper_at_settlement_hours": frac_at}
    with open("out_diag_freq.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\n저장: out_diag_freq.json")


if __name__ == "__main__":
    main()
