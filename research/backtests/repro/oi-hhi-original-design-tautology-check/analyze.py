"""원본 스펙(동적 20종목·365일 백분위) 재현 진단 — 폐기조건 (b) 판정.

산출: 동적 유니버스 요약, 전체구간/트리거시점 상관, 부분집합 비율, (b) 판정.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/home/user/study/research/backtests/repro/oi-hhi-original-design-tautology-check")
import common  # noqa: E402
from crypto_trader.signals import indicators as ind  # noqa: E402


def main() -> None:
    print("=== 1) 동적 20종목 유니버스 구축 ===")
    univ = common.build_dynamic_universe()
    print(f"후보 풀: {len(common.CANDIDATE_POOL)}종목, top20 한 번이라도 진입: "
         f"{len(univ.members_ever)}종목")
    print(f"데이터 범위: {univ.qv.index.min().date()} ~ {univ.qv.index.max().date()} "
         f"({len(univ.qv.index)}일)")
    print("일자별 유효 유니버스 크기(top20_mask 합계) 분포:")
    print(univ.universe_size.describe())

    # 시점별 구성 변화 스냅샷(연초 기준)
    print()
    print("--- 연초 스냅샷별 top20 구성 ---")
    for year in [2022, 2023, 2024, 2025, 2026]:
        ts = pd.Timestamp(f"{year}-01-01", tz="UTC")
        if ts not in univ.top20_mask.index:
            ts = univ.top20_mask.index[univ.top20_mask.index >= ts][0]
        members = sorted(univ.top20_mask.columns[univ.top20_mask.loc[ts]].tolist())
        print(f"{ts.date()}: n={len(members)} {members}")

    print()
    print("=== 2) HHI·BTC 점유율 신호 구축(롤링 365일 백분위) ===")
    sig = common.build_hhi_signals(univ)
    valid_hhi = sig.hhi.notna().sum()
    valid_pct = sig.hhi_pctile.notna().sum()
    print(f"HHI 계산 가능일수: {valid_hhi} / {len(sig.hhi)}, 백분위(365일 워밍업 후) 유효일수: "
         f"{valid_pct}")
    print("day별 HHI 계산에 실제 사용된 멤버 수(n_members_used) 분포:")
    print(sig.n_members_used[sig.n_members_used > 0].describe())
    miss_ratio = 1 - (sig.n_members_used / univ.universe_size.replace(0, np.nan))
    print(f"평균 결측 비율(유니버스 대비 OI 미확보): {miss_ratio.mean():.4f}")

    print()
    print("=== 3) 전체구간 상관 (pandas.corr, pairwise) ===")
    df_full = pd.DataFrame({
        "hhi_pctile": sig.hhi_pctile,
        "btc_share_pctile": sig.btc_oi_share_pctile,
        "hhi_raw": sig.hhi,
        "btc_share_raw": sig.btc_oi_share,
    }).dropna()
    print(f"n={len(df_full)}")
    print(df_full.corr())
    r_full_pctile = df_full["hhi_pctile"].corr(df_full["btc_share_pctile"])
    r_full_raw = df_full["hhi_raw"].corr(df_full["btc_share_raw"])
    print(f"\n[핵심] 전체구간 상관(백분위 기준): r={r_full_pctile:.4f}")
    print(f"[핵심] 전체구간 상관(원값 기준): r={r_full_raw:.4f}")

    print()
    print("=== 4) BTC 4h EMA20/50 크로스 트리거 시점 한정 상관 ===")
    btc4h = common.load_klines_4h("BTCUSDT")
    ema_fast = ind.ema(btc4h["close"], common.EMA_FAST)
    ema_slow = ind.ema(btc4h["close"], common.EMA_SLOW)
    fast = ema_fast.to_numpy(float)
    slow = ema_slow.to_numpy(float)
    prev_above = fast[:-1] > slow[:-1]
    curr_above = fast[1:] > slow[1:]
    valid = (np.isfinite(fast[:-1]) & np.isfinite(slow[:-1]) & np.isfinite(fast[1:])
            & np.isfinite(slow[1:]))
    golden = valid & (~prev_above) & curr_above
    death = valid & prev_above & (~curr_above)
    cross_idx = np.where(golden | death)[0] + 1  # 크로스 확정 봉 인덱스
    cross_times = btc4h.index[cross_idx]
    print(f"BTC 4h EMA{common.EMA_FAST}/{common.EMA_SLOW} 크로스 이벤트 수: {len(cross_times)} "
         f"(golden={golden.sum()}, death={death.sum()})")

    # 인과적 게이트일 = 크로스가 속한 캘린더일의 하루 전날(전일 종료 시점 OI 스냅샷이 그 날
    # 00:00부터 적용된다는 common.oi_1d_from_5m 라벨 규약과 일치).
    gate_days = (cross_times.floor("1D") - pd.Timedelta(days=1)).as_unit("ns")
    hz = sig.hhi_pctile.reindex(gate_days).to_numpy(float)
    sz = sig.btc_oi_share_pctile.reindex(gate_days).to_numpy(float)
    hraw = sig.hhi.reindex(gate_days).to_numpy(float)
    sraw = sig.btc_oi_share.reindex(gate_days).to_numpy(float)
    dtrig = pd.DataFrame({"hhi_pctile": hz, "btc_share_pctile": sz,
                          "hhi_raw": hraw, "btc_share_raw": sraw})
    dtrig_valid = dtrig.dropna()
    print(f"트리거 시점 대응 게이트일 유효표본 n={len(dtrig_valid)} / 전체 크로스 {len(cross_times)}")
    print(dtrig_valid.corr())
    r_trig_pctile = dtrig_valid["hhi_pctile"].corr(dtrig_valid["btc_share_pctile"])
    r_trig_raw = dtrig_valid["hhi_raw"].corr(dtrig_valid["btc_share_raw"])
    print(f"\n[핵심] 트리거 시점 상관(백분위 기준): r={r_trig_pctile:.4f}")
    print(f"[핵심] 트리거 시점 상관(원값 기준): r={r_trig_raw:.4f}")

    print()
    print("=== 5) 게이트 발화 시점 부분집합 비율 ===")
    hhi_disperse = set(df_full.index[df_full["hhi_pctile"] <= common.LO_TH])
    share_disperse = set(df_full.index[df_full["btc_share_pctile"] <= common.LO_TH])
    hhi_concentrated = set(df_full.index[df_full["hhi_pctile"] >= common.HI_TH])
    share_concentrated = set(df_full.index[df_full["btc_share_pctile"] >= common.HI_TH])

    def subset_ratio(a: set, b: set) -> float:
        return len(a & b) / len(a) if a else float("nan")

    print(f"HHI 분산레짐(<= {common.LO_TH}%ile) 발화일: {len(hhi_disperse)}, "
         f"BTC점유율 분산레짐 발화일: {len(share_disperse)}")
    print(f"HHI 분산레짐 ⊆ BTC점유율 분산레짐 비율: {subset_ratio(hhi_disperse, share_disperse):.4f}")
    print(f"BTC점유율 분산레짐 ⊆ HHI 분산레짐 비율: {subset_ratio(share_disperse, hhi_disperse):.4f}")
    print(f"HHI 집중레짐(>= {common.HI_TH}%ile) 발화일: {len(hhi_concentrated)}, "
         f"BTC점유율 집중레짐 발화일: {len(share_concentrated)}")
    print(f"HHI 집중레짐 ⊆ BTC점유율 집중레짐 비율: "
         f"{subset_ratio(hhi_concentrated, share_concentrated):.4f}")
    print(f"BTC점유율 집중레짐 ⊆ HHI 집중레짐 비율: "
         f"{subset_ratio(share_concentrated, hhi_concentrated):.4f}")
    both_extreme_hhi = hhi_disperse | hhi_concentrated
    both_extreme_share = share_disperse | share_concentrated
    print(f"HHI 극단(양쪽 합) ⊆ BTC점유율 극단(양쪽 합) 비율: "
         f"{subset_ratio(both_extreme_hhi, both_extreme_share):.4f}")
    print(f"BTC점유율 극단 ⊆ HHI 극단 비율: "
         f"{subset_ratio(both_extreme_share, both_extreme_hhi):.4f}")

    print()
    print("=== 6) 사전 등록 폐기조건 (b) 판정 ===")
    print("(b) HHI와 BTC 단독 점유율의 상관 |r| > 0.8 이면 재포장으로 폐기(동어반복)")
    verdict_full = "충족(폐기)" if abs(r_full_pctile) > 0.8 else "미충족"
    verdict_trig = "충족(폐기)" if abs(r_trig_pctile) > 0.8 else "미충족"
    print(f"전체구간(백분위) |r|={abs(r_full_pctile):.4f} -> (b) {verdict_full}")
    print(f"트리거시점(백분위) |r|={abs(r_trig_pctile):.4f} -> (b) {verdict_trig}")

    # 결과를 파일로도 저장(리포트 인용용)
    out = {
        "n_candidates": len(common.CANDIDATE_POOL),
        "n_members_ever": len(univ.members_ever),
        "n_full": len(df_full),
        "n_trigger_valid": len(dtrig_valid),
        "n_trigger_total": len(cross_times),
        "r_full_pctile": r_full_pctile,
        "r_full_raw": r_full_raw,
        "r_trigger_pctile": r_trig_pctile,
        "r_trigger_raw": r_trig_raw,
        "hhi_disperse_n": len(hhi_disperse),
        "share_disperse_n": len(share_disperse),
        "subset_hhi_in_share_disperse": subset_ratio(hhi_disperse, share_disperse),
        "subset_share_in_hhi_disperse": subset_ratio(share_disperse, hhi_disperse),
        "hhi_concentrated_n": len(hhi_concentrated),
        "share_concentrated_n": len(share_concentrated),
        "subset_hhi_in_share_concentrated": subset_ratio(hhi_concentrated, share_concentrated),
        "subset_share_in_hhi_concentrated": subset_ratio(share_concentrated, hhi_concentrated),
        "subset_hhi_extreme_in_share_extreme": subset_ratio(both_extreme_hhi, both_extreme_share),
        "subset_share_extreme_in_hhi_extreme": subset_ratio(both_extreme_share, both_extreme_hhi),
        "verdict_b_full": verdict_full,
        "verdict_b_trigger": verdict_trig,
    }
    import json
    with open("/tmp/oi_hhi_orig_result.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\n결과 저장: /tmp/oi_hhi_orig_result.json")


if __name__ == "__main__":
    main()
