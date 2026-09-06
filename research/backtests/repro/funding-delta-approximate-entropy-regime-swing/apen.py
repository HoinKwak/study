"""근사 엔트로피(Approximate Entropy, ApEn) — Pincus(1991) 원 정의 그대로 구현.

정의(길이 N 시계열 x_1..x_N, 패턴길이 m, 허용오차 r):
  1) 벡터 X_i = [x_i, ..., x_{i+m-1}], i=1..N-m+1
  2) C_i^m(r) = #{ j in 1..N-m+1 : d(X_i, X_j) <= r } / (N-m+1)
     d(X_i,X_j) = max_k |x_{i+k-1} - x_{j+k-1}| (체비셰프 거리, 자기자신(j=i) 포함 — Pincus 원 정의)
  3) Phi^m(r) = (1/(N-m+1)) * sum_i ln(C_i^m(r))
  4) ApEn(m,r,N) = Phi^m(r) - Phi^{m+1}(r)

낮을수록 시계열이 규칙적(반복 패턴이 m→m+1로 늘어나도 여전히 비슷하게 남음), 높을수록 불규칙.
"""
from __future__ import annotations

import numpy as np


def _phi(x: np.ndarray, m: int, r: float) -> float:
    n = len(x)
    nm = n - m + 1
    if nm <= 0:
        return float("nan")
    # X_i 벡터들 (nm, m)
    X = np.array([x[i:i + m] for i in range(nm)])
    # 체비셰프 거리 행렬 (nm, nm) — N=30 수준이라 O(N^2) 브루트포스로 충분(스펙 §코딩난이도 명시)
    diff = np.abs(X[:, None, :] - X[None, :, :]).max(axis=2)
    C = (diff <= r).sum(axis=1) / nm
    # C_i 는 항상 자기자신 포함이라 최소 1/nm > 0 이므로 log(0) 위험 없음
    return float(np.mean(np.log(C)))


def apen(x: np.ndarray, m: int = 2, r: float | None = None) -> float:
    """단일 윈도우에 대한 ApEn(m,r). r 미지정 시 0.2*std(x, ddof=0) 사용(Pincus 관행)."""
    x = np.asarray(x, dtype=float)
    if r is None:
        r = 0.2 * x.std(ddof=0)
    if r == 0 or not np.isfinite(r):
        return float("nan")
    phi_m = _phi(x, m, r)
    phi_m1 = _phi(x, m + 1, r)
    return phi_m - phi_m1


def apen_ref_naive(x: np.ndarray, m: int, r: float) -> float:
    """완전 순수파이썬 중첩루프 참조 구현(벡터화 버전과 독립적으로 재작성 — 교차검증용).

    apen()의 numpy 벡터화 로직과 알고리즘적으로 동일한 수식을 그대로 이중 for 문으로 옮긴 것.
    벡터화 버전에 실수(축 방향·자기포함 여부 등)가 있었다면 여기서 다른 값이 나온다.
    """
    x = list(map(float, x))
    n = len(x)

    def phi_naive(mm: int) -> float:
        nm = n - mm + 1
        if nm <= 0:
            return float("nan")
        logs = []
        for i in range(nm):
            Xi = x[i:i + mm]
            cnt = 0
            for j in range(nm):
                Xj = x[j:j + mm]
                d = max(abs(a - b) for a, b in zip(Xi, Xj))
                if d <= r:
                    cnt += 1
            C = cnt / nm
            logs.append(np.log(C))
        return sum(logs) / nm

    return phi_naive(m) - phi_naive(m + 1)


def rolling_apen(series: np.ndarray, window: int, m: int = 2, r_mult: float = 0.2) -> np.ndarray:
    """길이 len(series) 배열에 대해 매 시점 t 의 [t-window+1, t] 트레일링 윈도우 ApEn 계산.

    r = r_mult * std(윈도우 내 값, ddof=0)(윈도우별 상대값 — 데미닝, 스펙 §코딩난이도 주의사항).
    워밍업(윈도우 미달) 구간은 NaN.
    """
    n = len(series)
    out = np.full(n, np.nan)
    for t in range(window - 1, n):
        w = series[t - window + 1:t + 1]
        if np.any(~np.isfinite(w)):
            continue
        out[t] = apen(w, m=m, r=r_mult * w.std(ddof=0))
    return out


if __name__ == "__main__":
    # 소표본 손계산 대조 — N=6, m=2, r=1.0 을 사람이 직접 계산해 스크립트 출력과 대조.
    # 시계열: [1, 2, 1, 2, 1, 2] (완전 규칙적 진동 — ApEn≈0 기대)
    x_reg = np.array([1.0, 2.0, 1.0, 2.0, 1.0, 2.0])
    r = 1.0
    m = 2
    # X_i(m=2), i=1..5: [1,2],[2,1],[1,2],[2,1],[1,2]
    # 모든 쌍의 체비셰프거리가 0 or 1 이고 r=1.0 이라 전부 <=r → C_i=1 for all i → Phi^2=ln(1)=0
    # X_i(m=3), i=1..4: [1,2,1],[2,1,2],[1,2,1],[2,1,2] → 마찬가지로 전부 서로 거리<=1 → Phi^3=0
    # 손계산 기대값: ApEn = 0 - 0 = 0
    print("=== 손계산 대조 1: 완전 규칙적 [1,2,1,2,1,2], m=2, r=1.0 ===")
    print("손계산 기대: Phi^2=0.0, Phi^3=0.0, ApEn=0.0")
    print("apen() 결과:", apen(x_reg, m=m, r=r))
    print("apen_ref_naive() 결과:", apen_ref_naive(x_reg, m, r))

    # 손계산 대조 2: 좀 더 손으로 풀 수 있는 예 N=5, m=2, r=0.5, x=[1,1,2,1,3]
    print()
    print("=== 손계산 대조 2: [1,1,2,1,3], m=2, r=0.5 ===")
    x2 = np.array([1.0, 1.0, 2.0, 1.0, 3.0])
    r2 = 0.5
    # m=2: nm=4, X = [1,1],[1,2],[2,1],[1,3]  (i=1..4, 0-indexed 0..3)
    # 거리(체비셰프, m=2쌍 최대절대차):
    #  d(X0,X0)=0 d(X0,X1)=1 d(X0,X2)=1 d(X0,X3)=2  -> <=0.5: 자기자신만(1) -> C0=1/4
    #  d(X1,X1)=0 d(X1,X0)=1 d(X1,X2)=1 d(X1,X3)=1  -> <=0.5: 자기자신만(1) -> C1=1/4
    #  d(X2,X2)=0 d(X2,X0)=1 d(X2,X1)=1 d(X2,X3)=2  -> <=0.5: 자기자신만(1) -> C2=1/4
    #  d(X3,X3)=0 d(X3,X0)=2 d(X3,X1)=1 d(X3,X2)=2  -> <=0.5: 자기자신만(1) -> C3=1/4
    # Phi^2 = mean(ln(1/4)) = ln(0.25) = -1.386294
    # m=3: nm=3, X=[1,1,2],[1,2,1],[2,1,3]
    #  d(X0,X0)=0 d(X0,X1)=1 d(X0,X2)=2 -> C0=1/3
    #  d(X1,X1)=0 d(X1,X0)=1 d(X1,X2)=2 -> C1=1/3
    #  d(X2,X2)=0 d(X2,X0)=2 d(X2,X1)=2 -> C2=1/3
    # Phi^3 = ln(1/3) = -1.098612
    # ApEn = Phi^2 - Phi^3 = -1.386294 - (-1.098612) = -0.287682
    import math
    phi2_hand = math.log(0.25)
    phi3_hand = math.log(1 / 3)
    apen_hand = phi2_hand - phi3_hand
    print(f"손계산: Phi^2={phi2_hand:.6f}, Phi^3={phi3_hand:.6f}, ApEn={apen_hand:.6f}")
    print("apen() 결과:", apen(x2, m=2, r=r2))
    print("apen_ref_naive() 결과:", apen_ref_naive(x2, 2, r2))
