"""폐기조건(b): 즉시진입 대조군 vs 지연(delayed) 설계 — gross 기준, 표본수 맞춘 부트스트랩 +
base⊆pool 중첩 시 비중첩 표본만의 독립 Welch."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as c
import engine
import stats_utils as su


def main():
    data = c.load_all()
    cfg = engine.Config(fee_on=False)  # gross 기준(스펙 지시)

    # 지연(delayed) persistence 확정 트레이드 — gross
    delayed_rows = []
    for sym, sd in data.items():
        events = engine.detect_events(sym, sd, cfg)
        trades = engine.simulate_symbol(sym, sd, events, cfg)
        delayed_rows.extend(trades)
    delayed_df = engine.trades_to_df(delayed_rows)
    delayed_pers = delayed_df[delayed_df["branch"] == "persistence"]
    is_d, oos_d, full_d = su.split_is_oos(delayed_pers)

    # 즉시진입 대조군(persistence 프레임: 충격방향 그대로) — 모든 원시충격에 적용, gross
    imm_rows = []
    for sym, sd in data.items():
        shocks = engine.detect_raw_shocks(sym, sd, cfg)
        trades = engine.simulate_immediate(sym, sd, shocks, cfg, frame="persistence")
        imm_rows.extend(trades)
    imm_df = engine.trades_to_df(imm_rows)
    is_i, oos_i, full_i = su.split_is_oos(imm_df)

    print("=== 지연(delayed, persistence branch, gross) ===")
    for label, d in [("IS", is_d), ("OOS", oos_d), ("FULL", full_d)]:
        print(su.print_summary(su.summary(d, f"delayed-{label}")))

    print("\n=== 즉시진입(persistence frame, gross) ===")
    for label, d in [("IS", is_i), ("OOS", oos_i), ("FULL", full_i)]:
        print(su.print_summary(su.summary(d, f"immediate-{label}")))

    # 표본수 맞춘 부트스트랩: pool=즉시진입(더 큰 표본), base=지연(delayed)
    boot = su.bootstrap_matched_n_diff(oos_i["r_multiple"].to_numpy(),
                                       oos_d["r_multiple"].to_numpy())
    print(f"\nOOS 표본수맞춘 부트스트랩(pool=즉시진입, base=지연): {boot}")
    print("→ 지연 base 의 mean(R) 이 즉시진입 분포에서 백분위", f"{boot['pctile']:.1f}",
         "(50 근방이면 지연이 부가가치 없음)")

    # base ⊆ pool 중첩 확인: (symbol, shock_time) 기준
    key_d = set(zip(oos_d["symbol"], oos_d["shock_time"]))
    key_i = set(zip(oos_i["symbol"], oos_i["shock_time"]))
    overlap = key_d & key_i
    print(f"\nOOS 지연 트레이드 수={len(key_d)}, 즉시진입 트레이드 수={len(key_i)}, "
         f"(symbol,shock_time) 중첩={len(overlap)} ({100*len(overlap)/max(len(key_d),1):.1f}% of base)")

    # base⊆pool(99%대 중첩) — pool 쪽 잔여분(overlap 아닌 즉시진입 트레이드)만으로 base 전체와
    # 비교하는 것이 검정력을 보존하는 올바른 비중첩 독립비교(직전 라운드 "0건 중첩 잔여분만 비교"
    # 관행과 동일 원리: base 를 깎지 않고 pool 에서 base 와 겹치는 근원사건만 제외).
    mask_i_nonoverlap = ~oos_i.apply(lambda row: (row["symbol"], row["shock_time"]) in overlap, axis=1)
    i_no = oos_i[mask_i_nonoverlap]
    w = su.welch_test(oos_d["r_multiple"].to_numpy(), i_no["r_multiple"].to_numpy())
    print(f"\n비중첩 독립 Welch(지연 base 전체 vs 즉시진입 pool 잔여분, OOS gross R): "
         f"n_base={len(oos_d)} n_pool_residual={len(i_no)} "
         f"mean_base={w.get('mean_a', float('nan')):.4f} mean_pool_resid={w.get('mean_b', float('nan')):.4f} "
         f"t={w['t']:.3f} p={w['p']:.4f}")

    # 참고: 즉시진입 reversion 프레임도 병행 실행(정보용, reversion branch 표본희소 참고)
    imm_rows_r = []
    for sym, sd in data.items():
        shocks = engine.detect_raw_shocks(sym, sd, cfg)
        trades = engine.simulate_immediate(sym, sd, shocks, cfg, frame="reversion")
        imm_rows_r.extend(trades)
    imm_df_r = engine.trades_to_df(imm_rows_r)
    is_ir, oos_ir, full_ir = su.split_is_oos(imm_df_r)
    print("\n=== 즉시진입(reversion frame, gross) — 참고용 ===")
    for label, d in [("IS", is_ir), ("OOS", oos_ir), ("FULL", full_ir)]:
        print(su.print_summary(su.summary(d, f"immediate-rev-{label}")))

    delayed_df.to_parquet(str(c.SP / "delayed_gross.parquet"))
    imm_df.to_parquet(str(c.SP / "immediate_persistence_gross.parquet"))
    imm_df_r.to_parquet(str(c.SP / "immediate_reversion_gross.parquet"))


if __name__ == "__main__":
    main()
