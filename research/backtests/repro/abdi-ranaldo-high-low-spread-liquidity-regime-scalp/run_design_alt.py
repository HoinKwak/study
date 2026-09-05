"""설계판단 대안검증 — 인접 파라미터 스윕과 달리, 실제 해석적 설계판단의 '문자 그대로의 대안'을
직접 구현·실행한다(⚠️신규 규칙: 인접 파라미터 스윕은 해석 대안의 검증이 아니다).

1) 단일 확인봉 원칙 → 대안: 15m 확인봉을 최대 4봉까지 스캔(confirm_scan_bars=4).
2) 레짐 무효화 조기청산(기본 on) → 대안: 완전 비활성(invalidation_exit=False).
3) 볼린저 std(기본 2.0) → 스윕(1.8~2.5, bb_std는 sig 재계산 필요해 파라미터 스윕과 별도 취급).
"""
from __future__ import annotations

import common
import engine
import run_main as rm
import stats_utils as su
from run_sweep import run_variant


def main():
    sigs = rm.get_signals()
    print("===== 기준(baseline) =====")
    run_variant(sigs, engine.RunConfig(), "baseline")

    print("\n===== 대안①: 확인봉 스캔(단일→최대4봉) =====")
    run_variant(sigs, engine.RunConfig(confirm_scan_bars=4), "confirm_scan=4")

    print("\n===== 대안②: 레짐 무효화 조기청산 완전 비활성 =====")
    run_variant(sigs, engine.RunConfig(invalidation_exit=False), "invalidation_off")

    print("\n===== 대안③: 볼린저 std 스윕(평균회귀 서브모드) =====")
    for std in (1.8, 2.0, 2.2, 2.5):
        sigs_b = {sym: common.with_bb_std(sig, std) for sym, sig in sigs.items()}
        run_variant(sigs_b, engine.RunConfig(), f"bb_std={std}")

    print("\n===== 서브모드 단독(대안④: 모멘텀만/평균회귀만 — 서브모드 혼합 풀 분리비교) =====")
    run_variant(sigs, engine.RunConfig(modes=("M",)), "M-only")
    run_variant(sigs, engine.RunConfig(modes=("R",)), "R-only")


if __name__ == "__main__":
    main()
