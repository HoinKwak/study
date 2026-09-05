"""진입수수료 pnl 반영 확인 — 최근 2라운드 연속 나온 버그(진입fee 미차감)를 이 구현이
회피했는지 수치로 증명. engine.py의 pnl = raw - fee_entry - fee_exit 를 fee_entry 미차감
버전과 대조해 실제로 그 항이 결과에 영향을 주는지(=코드가 실제로 그 값을 쓰는지) 확인."""
from __future__ import annotations

import stats_utils as su
import engine


def check_entry_fee(sig):
    cfg = engine.RunConfig(gate="base", fee_on=True)
    trades = engine.run_config(sig, cfg)
    df_with = su.trades_df(trades)

    # 버그판 재현: pnl 에서 fee_entry 를 빼지 않는 버전(과거 버그 패턴)으로 R 재계산
    df_bug = df_with.copy()
    df_bug["pnl_bug"] = df_bug["pnl"] + df_bug["fee_entry"]  # fee_entry 를 되돌려줌(버그 재현)
    df_bug["r_bug"] = df_bug["pnl_bug"] / df_bug["risk_amount"]

    is_c, oos_c, full_c = su.split_is_oos(df_with)
    df_bug_full = df_bug[(df_bug["entry_time"] >= __import__("common").IS_START) &
                         (df_bug["entry_time"] <= __import__("common").OOS_END)]

    print(f"수정판(진입fee 반영) FULL PF(R)={su.pf_r(full_c):.4f}  sum(R)={full_c['r'].sum():+.3f}")
    pf_bug = (df_bug_full.loc[df_bug_full['r_bug'] > 0, 'r_bug'].sum() /
             -df_bug_full.loc[df_bug_full['r_bug'] < 0, 'r_bug'].sum())
    print(f"버그판(진입fee 미반영) FULL PF(R)={pf_bug:.4f}  sum(R)={df_bug_full['r_bug'].sum():+.3f}")
    print(f"진입fee 총액(FULL)={full_c['fee_entry'].sum():.2f} "
         f"(0이 아니면 실제로 pnl 계산에 영향을 주는 값 — 코드가 그 값을 쓰고 있음을 확인)")
