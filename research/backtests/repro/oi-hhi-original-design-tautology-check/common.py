"""원본 스펙(동적 20종목 유니버스 + 롤링 365일 백분위) 재현 — 로더/유니버스 구축.

스펙: research/strategies/oi-cross-sectional-herfindahl-concentration-breadth-btc-trend-swing.md (9ea4001)
목적: 사전 등록 폐기조건 (b) [HHI와 BTC 단독 점유율 상관 |r|>0.8 → 재포장 폐기]가
원본 설계(고정 7종목·60일 z-score가 아니라 동적 20종목·365일 백분위)에서도 성립하는지 확인.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

_repo_src = os.environ.get(
    "OIHHI_REPO_SRC",
    "/home/user/study/.claude/worktrees/agent-a25eed216f42f1e6d/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "OIHHI_ORIG_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi_orig"))
DATA = SP / "data"
KLINES_1D_DIR = DATA / "klines_1d"
KLINES_4H_DIR = DATA / "klines_4h"
METRICS_DIR = DATA / "metrics"

# 원본 스펙 기본값
UNIVERSE_SIZE = 20
MIN_QV_USD = 10_000_000.0  # 24h 거래대금 $10M 이상 (봇 동적 유니버스 정의와 동일)
HHI_WINDOW_DAYS = 365
LO_TH = 30  # percentile
HI_TH = 70  # percentile
EMA_FAST, EMA_SLOW = 20, 50  # BTC 4h

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

_KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
               "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]

# 후보 풀: 기존 7종목 + 대형·중형 알트 + 밈코인(1000x 계약명 보정) — 실제 데이터 존재 여부는
# HTTP 200/404 실측으로 확인(다운로드 로그: klines_pool_missing.log).
CANDIDATE_POOL = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT",
    "MATICUSDT", "DOTUSDT", "LTCUSDT", "LINKUSDT", "AVAXUSDT", "ATOMUSDT", "UNIUSDT",
    "FILUSDT", "ETCUSDT", "XLMUSDT", "ICPUSDT", "NEARUSDT", "TRXUSDT", "BCHUSDT",
    "1000SHIBUSDT", "VETUSDT", "ALGOUSDT", "AAVEUSDT", "SANDUSDT", "MANAUSDT", "AXSUSDT",
    "FTMUSDT", "GRTUSDT", "EOSUSDT", "XTZUSDT", "THETAUSDT", "EGLDUSDT", "GALAUSDT",
    "CHZUSDT", "DYDXUSDT", "RUNEUSDT", "LDOUSDT", "INJUSDT",
    "APTUSDT", "ARBUSDT", "OPUSDT", "SUIUSDT", "WLDUSDT", "SEIUSDT", "TIAUSDT",
    "ORDIUSDT", "1000PEPEUSDT", "WIFUSDT", "1000BONKUSDT", "JUPUSDT", "RENDERUSDT",
    "FETUSDT", "ONDOUSDT", "PYTHUSDT", "HBARUSDT", "TONUSDT",
]

CORE7 = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]


# ------------------------------------------------------------------ 로더

def _load_klines(dirpath: Path, symbol: str, tf: str) -> pd.DataFrame:
    files = sorted(dirpath.glob(f"{symbol}-{tf}-*.csv"))
    parts = []
    for p in files:
        with open(p) as f:
            first = f.readline()
        has_header = "open_time" in first
        df = pd.read_csv(p, header=0 if has_header else None,
                         names=_KLINE_COLS if not has_header else None)
        df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
        if df.empty:
            continue
        df["open_time"] = df["open_time"].astype("int64")
        parts.append(df)
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    ot = out["open_time"]
    is_us = ot.abs() > 10**14
    if is_us.any():
        out.loc[is_us, "open_time"] = out.loc[is_us, "open_time"] // 1000
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume", "quote_volume"]]
    out.index = out.index.as_unit("ns")
    return out


@lru_cache(maxsize=None)
def load_klines_1d(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_1D_DIR, symbol, "1d")


@lru_cache(maxsize=None)
def load_klines_4h(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_4H_DIR, symbol, "4h")


@lru_cache(maxsize=None)
def load_metrics_5m(symbol: str) -> pd.DataFrame:
    """metrics 5분 원본 로드. create_time 은 날짜 문자열 → 명시적 format 파싱(us/ms 단위사고 회피)."""
    files = sorted(METRICS_DIR.glob(f"{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "symbol", "sum_open_interest"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out.index = out.index.as_unit("ns")
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    out.loc[out["sum_open_interest"] <= 0, "sum_open_interest"] = np.nan
    return out


def oi_1d_from_5m(m5: pd.DataFrame) -> pd.Series:
    """5분 OI → 1d 마지막값(그날 00:00~24:00 UTC 구간 마지막 관측치, label=left/closed=left).
    즉 day D 라벨의 값은 'day D 종료 시점(약 23:55 UTC)까지의 정보'를 담는다 — day D+1 부터 사용
    가능(원본 스펙의 "1d 경계(00:00 UTC)에서 산출"과 일관: 자정 스냅샷은 직전일 마감 데이터)."""
    if m5.empty:
        return pd.Series(dtype=float)
    s = m5["sum_open_interest"]
    last = s.resample("1D", label="left", closed="left").last()
    return last


def rolling_pctile(x: pd.Series, window: int) -> pd.Series:
    """롤링 window일 창 기준 각 시점 값의 백분위(0~100). 마지막 관측치가 자기 자신을 포함한
    창 내에서 몇 %ile 인지(오름차순 순위 비율)."""
    def _pct(arr):
        if len(arr) < 2 or not np.isfinite(arr[-1]):
            return np.nan
        valid = arr[np.isfinite(arr)]
        if len(valid) < 2:
            return np.nan
        rank = (valid < arr[-1]).sum()
        return 100.0 * rank / (len(valid) - 1) if len(valid) > 1 else np.nan
    return x.rolling(window, min_periods=max(30, window // 4)).apply(_pct, raw=True)


# ------------------------------------------------------------- 동적 유니버스 구축

@dataclass
class DynUniverse:
    qv: pd.DataFrame            # 1d, 컬럼=심볼, 값=quote_volume(당일)
    top20_mask: pd.DataFrame    # 1d, 불리언 — 그 날 causal 선정된 top20 여부(전일 qv 기준)
    members_ever: list[str]     # top20에 한 번이라도 든 심볼 전체
    universe_size: pd.Series    # 유효 유니버스 크기(top20_mask.sum(axis=1)) — 데이터 결측 감안


def build_dynamic_universe(min_qv_usd: float = MIN_QV_USD,
                           universe_size: int = UNIVERSE_SIZE) -> DynUniverse:
    """룩어헤드 방지: day D의 유니버스는 day D-1의 quote_volume(전일 24h 거래대금)으로 선정.
    (day D 1d 봉 자체는 D의 거래 중에만 확정되므로 D 시작 시점엔 미지 — 반드시 D-1 값을 써야 함)"""
    qv_cols = {}
    for sym in CANDIDATE_POOL:
        k = load_klines_1d(sym)
        if k.empty:
            continue
        qv_cols[sym] = k["quote_volume"]
    qv = pd.DataFrame(qv_cols).sort_index()

    qv_prev = qv.shift(1)  # causal: 전일 값
    eligible = qv_prev >= min_qv_usd

    top20_mask = pd.DataFrame(False, index=qv.index, columns=qv.columns)
    for dt in qv.index:
        row = qv_prev.loc[dt].where(eligible.loc[dt])
        row = row.dropna()
        if row.empty:
            continue
        top = row.sort_values(ascending=False).head(universe_size).index
        top20_mask.loc[dt, top] = True

    members_ever = sorted(top20_mask.columns[top20_mask.any(axis=0)].tolist())
    usize = top20_mask.sum(axis=1)
    return DynUniverse(qv=qv, top20_mask=top20_mask, members_ever=members_ever,
                       universe_size=usize)


@dataclass
class HHISignals:
    oi_notional: pd.DataFrame   # 1d, 컬럼=members_ever, 값=OI 명목가치(USDT), 결측=NaN
    hhi: pd.Series              # 그 날 top20_mask 멤버만으로 계산한 HHI(t)
    hhi_pctile: pd.Series       # 롤링 365일 백분위
    btc_oi_share: pd.Series     # BTC 명목가치 / (그 날 top20 멤버 합계)
    btc_oi_share_pctile: pd.Series
    n_members_used: pd.Series   # 그 날 HHI 계산에 실제 사용된(OI 데이터 존재) 멤버 수


def build_hhi_signals(univ: DynUniverse, window: int = HHI_WINDOW_DAYS) -> HHISignals:
    oi_cols = {}
    for sym in univ.members_ever:
        k1d = load_klines_1d(sym)
        m5 = load_metrics_5m(sym)
        if k1d.empty or m5.empty:
            continue
        oi1d = oi_1d_from_5m(m5)
        oi1d.index = oi1d.index.as_unit("ns")
        k1d = k1d.copy()
        k1d.index = k1d.index.as_unit("ns")
        joined = pd.DataFrame({"oi": oi1d}).join(k1d[["close"]], how="inner")
        oi_cols[sym] = joined["oi"] * joined["close"]
    oi_notional = pd.DataFrame(oi_cols).reindex(univ.top20_mask.index)

    hhi = pd.Series(np.nan, index=univ.top20_mask.index)
    btc_share = pd.Series(np.nan, index=univ.top20_mask.index)
    n_used = pd.Series(0, index=univ.top20_mask.index)

    for dt in univ.top20_mask.index:
        members = univ.top20_mask.columns[univ.top20_mask.loc[dt]]
        if len(members) == 0:
            continue
        vals = oi_notional.loc[dt, members].dropna()
        n_used.loc[dt] = len(vals)
        if len(vals) < max(5, int(0.5 * len(members))):
            continue  # 유니버스 절반 미만만 OI 확보되면 그 날은 왜곡 위험 → 제외
        total = vals.sum()
        if total <= 0:
            continue
        shares = vals / total
        hhi.loc[dt] = float((shares ** 2).sum())
        if "BTCUSDT" in vals.index:
            btc_share.loc[dt] = float(vals["BTCUSDT"] / total)

    hhi_pctile = rolling_pctile(hhi, window)
    btc_share_pctile = rolling_pctile(btc_share, window)

    return HHISignals(oi_notional=oi_notional, hhi=hhi, hhi_pctile=hhi_pctile,
                      btc_oi_share=btc_share, btc_oi_share_pctile=btc_share_pctile,
                      n_members_used=n_used)
