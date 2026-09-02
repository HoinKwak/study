"""메인 실행 — base(gated) + 무조건부 대조군 3종(always_mr/always_mom/no_gate_both) + 반전.
net(비용반영)·gross(fee=0·slip=0) 둘 다, IS/OOS/FULL 및 서브모드(MR/MOM) 분리 집계.
결과를 CSV(trades)로 저장해 후속 진단 스크립트가 재사용.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
import stats_utils as su

OUT = common.SP / "out"
OUT.mkdir(parents=True, exist_ok=True)

VARIANTS = {
    "base_gated": dict(signal_mode="gated", direction_mode="normal"),
    "base_gated_reverse": dict(signal_mode="gated", direction_mode="reverse"),
    "always_mr": dict(signal_mode="mr_only_ungated", direction_mode="normal"),
    "always_mom": dict(signal_mode="mom_only_ungated", direction_mode="normal"),
    "no_gate_both": dict(signal_mode="no_gate_both", direction_mode="normal"),
}


def run_variant(name: str, kw: dict, cost_on: bool) -> pd.DataFrame:
    cfg = engine.RunConfig(cost_on=cost_on, **kw)
    sigs = engine.load_all_signals(common.SYMBOLS, cfg)
    trades = engine.run_all(sigs, cfg)
    all_trades = [t for tl in trades.values() for t in tl]
    df = su.trades_df(all_trades, rcol="r_net" if cost_on else "r_gross")
    tag = "net" if cost_on else "gross"
    df.to_csv(OUT / f"trades_{name}_{tag}.csv", index=False)
    return df


def report_block(df: pd.DataFrame, label: str) -> None:
    is_df, oos_df, full_df = su.split_is_oos(df)
    print(su.fmt(su.summary(is_df, f"{label} IS")))
    print(su.fmt(su.summary(oos_df, f"{label} OOS")))
    print(su.fmt(su.summary(full_df, f"{label} FULL")))


def main() -> None:
    print("### 데이터 로드/신호 계산 캐시 워밍업 (base_gated) ###")
    for cost_on in (True, False):
        tag = "net" if cost_on else "gross"
        print(f"\n===== 비용 {'ON(net)' if cost_on else 'OFF(gross)'} =====")
        dfs = {}
        for name, kw in VARIANTS.items():
            df = run_variant(name, kw, cost_on)
            dfs[name] = df
            print(f"\n--- {name} ({tag}) 합산 ---")
            report_block(df, name)
            if name in ("base_gated", "base_gated_reverse", "no_gate_both"):
                for mode in ("MR", "MOM"):
                    sub = df[df["mode"] == mode]
                    if len(sub) == 0:
                        print(f"   [{mode}] n=0")
                        continue
                    report_block(sub, f"{name}/{mode}")

        if cost_on:
            # base ⊆ no_gate_both 중첩 비율 계산 (net 기준)
            base = dfs["base_gated"]
            pool = dfs["no_gate_both"]
            base_keys = set(zip(base["symbol"], base["mode"], base["entry_idx"]))
            pool_keys = set(zip(pool["symbol"], pool["mode"], pool["entry_idx"]))
            overlap = base_keys & pool_keys
            print(f"\n### base_gated ⊆ no_gate_both 중첩 점검 ###")
            print(f"   base n={len(base_keys)}, pool n={len(pool_keys)}, "
                 f"overlap={len(overlap)} ({100*len(overlap)/max(1,len(base_keys)):.1f}% of base)")


if __name__ == "__main__":
    main()
