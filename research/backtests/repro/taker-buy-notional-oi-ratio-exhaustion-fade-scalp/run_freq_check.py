"""최우선 검증: 개별조건 발생률 vs 결합조건 발생률 — 독립기대 대비 배수.
스펙의 핵심 의심점(체결건수 흡수 스퀴즈 건과 동일 유형 — 유량z 극단과 흡수형 캔들이
상호배타적일 위험)을 최종 진입조건 전체(z_th=3.0 AND body_ratio<=0.40, 1h 확인 포함/미포함
둘 다)를 대상으로 실측한다."""
import pickle

import numpy as np

import common
from scipy import stats as sstats

with open(common.SP / "sigs_200.pkl", "rb") as f:
    sigs = pickle.load(f)

Z_TH = 3.0
BODY_TH = 0.40

# 정규분포 근사 독립기대(단측 z>=3.0)
p_z_normal = float(sstats.norm.sf(Z_TH))
print(f"정규분포 근사 P(z>=3.0) (단측) = {p_z_normal:.6f} ({p_z_normal*100:.4f}%)")
print(f"  15m봉 연간 개수 ≈ 35,040 → 정규 근사 기준 연 {p_z_normal*35040:.1f}회/방향, "
     f"양방향 합 {2*p_z_normal*35040:.1f}회/종목/년\n")

print(f"{'심볼':10s} {'n':>8s} {'z_buy>=3':>10s} {'z_sell>=3':>10s} {'body<=.4':>10s} "
     f"{'joint_buy':>10s} {'joint_sell':>10s} {'indep기대(buy)':>14s} {'실측/기대':>10s}")
tot_n = 0
tot_joint = 0
tot_indep_expect = 0.0
for sym, sig in sigs.items():
    zb = sig.z_buy
    zs = sig.z_sell
    body = sig.body_ratio.to_numpy(float)
    valid = np.isfinite(zb) & np.isfinite(zs) & np.isfinite(body)
    n = int(valid.sum())
    fb = np.isfinite(zb) & (zb >= Z_TH)
    fs = np.isfinite(zs) & (zs >= Z_TH)
    fbody = np.isfinite(body) & (body <= BODY_TH)
    p_b = fb[valid].mean()
    p_s = fs[valid].mean()
    p_body = fbody[valid].mean()
    joint_b = (fb & fbody & valid).sum()
    joint_s = (fs & fbody & valid).sum()
    indep_expect_b = p_b * p_body * n
    ratio = (joint_b / indep_expect_b) if indep_expect_b > 0 else float("nan")
    print(f"{sym:10s} {n:8d} {p_b*100:9.4f}% {p_s*100:9.4f}% {p_body*100:9.4f}% "
         f"{joint_b:10d} {joint_s:10d} {indep_expect_b:14.2f} {ratio:10.3f}")
    tot_n += n
    tot_joint += joint_b + joint_s
    tot_indep_expect += indep_expect_b + p_s * p_body * n

years = tot_n / 4 / 35040 * 4  # n(15m bars) -> years, 15m*35040/yr per symbol; tot_n sums 7 symbols
print(f"\n합계: 결합발생(양방향) = {tot_joint}, 독립기대 합 = {tot_indep_expect:.1f}, "
     f"실측/기대 = {tot_joint/tot_indep_expect:.3f}")
print(f"7종목 합산 연평균(결합, 양방향, 4.5년 환산 근사) ≈ {tot_joint/4.5:.1f}건/년(7종목 합)"
     f" ≈ {tot_joint/4.5/7:.2f}건/년/종목")
print("스펙 사전 예상: 연 90~100회/종목(정규근사, 3배 이상 벗어나면 재점검 지시)")
