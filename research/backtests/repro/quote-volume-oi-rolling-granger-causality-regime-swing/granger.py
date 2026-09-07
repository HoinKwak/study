"""롤링 양방향 그레인저 인과성(F-검정) — 거래대금(quote_volume) ↔ OI(sum_open_interest).

VAR(lag) 두 방향:
  qv->oi: doi_t ~ const + doi_{t-1..t-lag} + dqv_{t-1..t-lag}  vs 제약모형(dqv 항 제외)
  oi->qv: 대칭

각 시점 t 에서 창(window, 기본 60봉)의 **과거~현재(t 포함)** 데이터만 사용(룩어헤드 없음).
window 내 시차 관측치까지 전부 그 window 안에서만 가져온다(창 밖 데이터 참조 없음).
NaN 이 창 안에 하나라도 있으면 그 시점은 계산 불가(NaN) 처리.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import f as f_dist


def _lag_matrix(w: np.ndarray, lag: int, n_obs: int) -> np.ndarray:
    """w(길이=window)에서 시차 lag 라그 행렬(n_obs x lag) 구성.
    row r(0..n_obs-1)의 col j(0..lag-1) = w[lag-j-1+r] (즉 목표시점 lag+r 의 (j+1)차 과거값)."""
    cols = [w[lag - j - 1: lag - j - 1 + n_obs] for j in range(lag)]
    return np.column_stack(cols)


def _ols_rss(y: np.ndarray, X: np.ndarray) -> float:
    # 정규방정식으로 소형 시스템 직접 풀이(빠름). 특이행렬이면 lstsq 폴백.
    XtX = X.T @ X
    Xty = X.T @ y
    try:
        beta = np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    return float(resid @ resid)


def _granger_p(y: np.ndarray, own_lags: np.ndarray, other_lags: np.ndarray, lag: int) -> float:
    n = len(y)
    const = np.ones((n, 1))
    Xr = np.hstack([const, own_lags])
    Xu = np.hstack([const, own_lags, other_lags])
    rss_r = _ols_rss(y, Xr)
    rss_u = _ols_rss(y, Xu)
    k_u = Xu.shape[1]
    df_u = n - k_u
    if df_u <= 0 or rss_u <= 0:
        return float("nan")
    f_val = ((rss_r - rss_u) / lag) / (rss_u / df_u)
    if f_val < 0:
        f_val = 0.0
    return float(f_dist.sf(f_val, lag, df_u))


def rolling_granger_pvalues(doi: np.ndarray, dqv: np.ndarray,
                            window: int = 60, lag: int = 4):
    """causal 롤링 양방향 그레인저 F-검정 p-value 배열 반환 (p_qv2oi, p_oi2qv).

    t 위치의 값은 doi[t-window+1 : t+1], dqv[t-window+1 : t+1] (길이 window, t 포함)만 사용.
    """
    n = len(doi)
    assert len(dqv) == n
    n_obs = window - lag
    k_u = 1 + 2 * lag
    if n_obs <= k_u:
        raise ValueError(f"window={window} 이 lag={lag} 대비 너무 작음(n_obs={n_obs}<=k_u={k_u})")
    p_qv2oi = np.full(n, np.nan)
    p_oi2qv = np.full(n, np.nan)
    for t in range(window - 1, n):
        w_doi = doi[t - window + 1: t + 1]
        w_dqv = dqv[t - window + 1: t + 1]
        if not (np.all(np.isfinite(w_doi)) and np.all(np.isfinite(w_dqv))):
            continue
        y_oi = w_doi[lag:window]
        y_qv = w_dqv[lag:window]
        lag_doi = _lag_matrix(w_doi, lag, n_obs)
        lag_dqv = _lag_matrix(w_dqv, lag, n_obs)
        p_qv2oi[t] = _granger_p(y_oi, lag_doi, lag_dqv, lag)
        p_oi2qv[t] = _granger_p(y_qv, lag_dqv, lag_doi, lag)
    return p_qv2oi, p_oi2qv


def classify_regime(p_qv2oi: np.ndarray, p_oi2qv: np.ndarray,
                    p_sig: float = 0.05, p_insig: float = 0.10) -> np.ndarray:
    """레짐 분류: 'qv_lead' / 'oi_lead' / 'none'(무레짐, NaN 포함)."""
    n = len(p_qv2oi)
    out = np.full(n, "none", dtype=object)
    valid = np.isfinite(p_qv2oi) & np.isfinite(p_oi2qv)
    qv_lead = valid & (p_qv2oi < p_sig) & (p_oi2qv >= p_insig)
    oi_lead = valid & (p_oi2qv < p_sig) & (p_qv2oi >= p_insig)
    out[qv_lead] = "qv_lead"
    out[oi_lead] = "oi_lead"
    return out
