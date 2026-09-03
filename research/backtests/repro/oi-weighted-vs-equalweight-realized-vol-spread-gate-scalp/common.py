"""OI가중 vs 등가중 실현변동성 스프레드 레짐 게이트 스캘프 — 공통 데이터 로더·지표 계산.

스펙: research/strategies/oi-weighted-vs-equalweight-realized-vol-spread-gate-scalp.md

데이터 소스:
  - klines 1h/15m: 기존 정기 루틴이 이미 받아 캐시해둔 pickle(monthly, raw Binance klines 컬럼)을
    재사용한다(`klines_qv_cache`=1h, `klines_cache`=15m, 스크래치패드 공용 캐시 — "캐시 재사용
    타당성" 선례에 따라 기간·유니버스·필드 대조 후 사용, 부재 시 download.py 로 재다운로드).
  - metrics(5분 OI): 이전 라운드(oiskew)가 이미 전 구간·7종목 CSV 로 추출해둔 것을 읽기전용으로
    재사용(`sum_open_interest_value` 컬럼, 7종목×1642일 = 11,494개 파일, 미싱 2건만).

⚠️ 시간 단위 함정: pandas 3.0.x 는 `to_datetime(unit="ms")` 가 `datetime64[ms]` 를 유지하고 여기에
`pd.Timedelta` 를 더하면 조용히 `datetime64[us]` 로 업캐스트되어 merge_asof 정렬이 깨진다. 모든
DatetimeIndex 는 파싱 직후 `.astype("datetime64[ns, UTC]")` 로 명시 통일한다.
⚠️ metrics `create_time` 은 날짜 문자열이라 unit 미지정 파싱이 pandas 3.0.5 에서 us 로 추론되고
klines 는 ms 라 병합이 조용히 전부 NaN 이 될 수 있음 — 여기서는 애초에 정수 epoch 파싱이 아니라
명시적 `format="%Y-%m-%d %H:%M:%S"` 문자열 파싱을 쓰므로 이 함정 자체가 발생하지 않으나, 병합 후
NaN 비율을 반드시 출력해 확인한다(아래 diag 스크립트).
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
    "OIWEQ_REPO_SRC", str(Path(__file__).resolve().parents[4] / "src"))
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "OIWEQ_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiweq"))
DATA = SP / "data"
DATA.mkdir(parents=True, exist_ok=True)

# 기존 정기 루틴의 공용 캐시(읽기전용 재사용)
KLINES_1H_CACHE = Path(os.environ.get(
    "OIWEQ_KLINES_1H",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/klines_qv_cache"))
KLINES_15M_CACHE = Path(os.environ.get(
    "OIWEQ_KLINES_15M",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/klines_cache"))
METRICS_DIR = Path(os.environ.get(
    "OIWEQ_METRICS_DIR",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiskew/data/metrics"))

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
BTC = "BTCUSDT"
TRADE_SYMBOL = BTC

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = (TAKER_FEE + SLIPPAGE) * 2  # 0.14%

# 스펙 기본 파라미터
RV_WINDOW = 24            # 1h 봉, 24시간 윈도우
SPREAD_Z_WINDOW = 90      # 1h 봉, 90시간 롤링
SPREAD_Z_SHORT_TH = 1.5
SPREAD_Z_LONG_TH = -1.0
DONCHIAN_LOOKBACK = 20    # 15m 봉
ATR_TRAIL_MULT = 1.4
ATR_STOP_MULT = 1.0
MAX_HOLD = 10             # 15m 봉


# ------------------------------------------------------------------ klines 로더(pickle 캐시)

def _load_klines_pkl_cache(symbol: str, tf: str, cache_dir: Path) -> pd.DataFrame:
    import pickle
    files = sorted(cache_dir.glob(f"{symbol}_{tf}_*.pkl"))
    if not files:
        return pd.DataFrame()
    parts = []
    for p in files:
        with open(p, "rb") as f:
            parts.append(pickle.load(f))
    out = pd.concat(parts, ignore_index=True)
    out["open_time"] = out["open_time"].astype("int64")
    dt = pd.to_datetime(out["open_time"], unit="ms", utc=True).astype("datetime64[ns, UTC]")
    out["dt"] = dt
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    return out[["open", "high", "low", "close", "volume", "quote_volume"]]


@lru_cache(maxsize=None)
def load_klines_1h(symbol: str) -> pd.DataFrame:
    return _load_klines_pkl_cache(symbol, "1h", KLINES_1H_CACHE)


@lru_cache(maxsize=None)
def load_klines_15m(symbol: str) -> pd.DataFrame:
    return _load_klines_pkl_cache(symbol, "15m", KLINES_15M_CACHE)


# ------------------------------------------------------------------ metrics(OI) 로더

@lru_cache(maxsize=None)
def load_metrics_5m(symbol: str) -> pd.DataFrame:
    """metrics 5분 원본 로드. create_time 은 날짜 문자열 → 명시적 format 파싱(us/ms 단위사고 회피).
    ⚠️0-fill 결측 처리: sum_open_interest_value<=0 은 명백한 결측 placeholder(실제 OI 는 0이
    될 수 없음) → NaN 처리(이전 라운드 선례와 동일)."""
    files = sorted(METRICS_DIR.glob(f"{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "symbol", "sum_open_interest_value"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce").astype("datetime64[ns, UTC]")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out["sum_open_interest_value"] = pd.to_numeric(out["sum_open_interest_value"], errors="coerce")
    out.loc[out["sum_open_interest_value"] <= 0, "sum_open_interest_value"] = np.nan
    return out[["sum_open_interest_value"]]


def oi_value_1h_from_5m(m5: pd.DataFrame) -> pd.DataFrame:
    """5분 OI 명목가치 → 1h 봉 마감시점 값(resample('1h').last() 는 빈 bin 에 NaN, 명시적 ffill).
    ffill 이 적용된 bar 수를 oi_5m_count==0 으로 추적."""
    if m5.empty:
        return pd.DataFrame()
    s = m5["sum_open_interest_value"]
    last = s.resample("1h", label="left", closed="left").last()
    cnt = s.resample("1h", label="left", closed="left").count()
    filled = last.ffill()
    return pd.DataFrame({"oi_value": filled, "oi_raw_nan": last.isna(), "oi_5m_count": cnt})


# ------------------------------------------------------------------ 실현변동성·OI가중 스프레드

def realized_vol_1h(df1h: pd.DataFrame, window: int = RV_WINDOW) -> pd.Series:
    ret = np.log(df1h["close"] / df1h["close"].shift(1))
    return ret.rolling(window).std()


@dataclass
class UniverseData:
    rv: pd.DataFrame          # 1h 인덱스 × 7종목 실현변동성
    oi_value: pd.DataFrame    # 1h 인덱스 × 7종목 OI 명목가치
    oi_5m_count: pd.DataFrame


def build_universe_data(symbols: list[str] = SYMBOLS, rv_window: int = RV_WINDOW) -> UniverseData:
    rv_cols, oi_cols, cnt_cols = {}, {}, {}
    for sym in symbols:
        k1h = load_klines_1h(sym)
        if k1h.empty:
            continue
        rv_cols[sym] = realized_vol_1h(k1h, rv_window)
        m5 = load_metrics_5m(sym)
        oi1h = oi_value_1h_from_5m(m5)
        if not oi1h.empty:
            oi_cols[sym] = oi1h["oi_value"]
            cnt_cols[sym] = oi1h["oi_5m_count"]
    rv = pd.DataFrame(rv_cols).sort_index()
    oi_value = pd.DataFrame(oi_cols).sort_index()
    oi_5m_count = pd.DataFrame(cnt_cols).sort_index()
    return UniverseData(rv=rv, oi_value=oi_value, oi_5m_count=oi_5m_count)


def compute_spread(udata: UniverseData, symbols: list[str] = SYMBOLS,
                    spread_z_window: int = SPREAD_Z_WINDOW) -> pd.DataFrame:
    """rv_ow(OI가중)·rv_ew(등가중)·spread·spread_z·btc_oi_weight(진단용) 계산.

    OI가중치는 그 시점 OI 값이 있는 종목들만으로 재정규화(결측 종목 제외, 전부 결측이면 NaN).
    RV 가 결측인 종목은 해당 시점 두 가중 평균 모두에서 자연 제외(pandas NaN 전파 + dropna 방식
    대신 명시적 마스킹으로 어느 종목이 실제로 집계에 들어갔는지 추적 가능하게 함)."""
    idx = udata.rv.index.union(udata.oi_value.index)
    rv = udata.rv.reindex(idx)[symbols]
    oi = udata.oi_value.reindex(idx)[symbols]

    valid = rv.notna() & oi.notna()
    oi_masked = oi.where(valid)
    rv_masked = rv.where(valid)

    oi_sum = oi_masked.sum(axis=1, skipna=True)
    n_valid = valid.sum(axis=1)
    w = oi_masked.div(oi_sum, axis=0)

    rv_ow = (w * rv_masked).sum(axis=1, skipna=True)
    rv_ow = rv_ow.where(n_valid > 0)
    rv_ew = rv_masked.mean(axis=1, skipna=True)
    rv_ew = rv_ew.where(n_valid > 0)

    spread = rv_ow - rv_ew
    z_mean = spread.rolling(spread_z_window).mean()
    z_std = spread.rolling(spread_z_window).std(ddof=0)
    spread_z = (spread - z_mean) / z_std
    spread_z = spread_z.where(z_std > 1e-12)

    btc_w = w[BTC] if BTC in w.columns else pd.Series(np.nan, index=idx)

    out = pd.DataFrame({
        "rv_ow": rv_ow, "rv_ew": rv_ew, "spread": spread, "spread_z": spread_z,
        "btc_oi_weight": btc_w, "n_valid": n_valid,
    })
    return out


def gate_from_spread_z(spread_z: pd.Series, short_th: float = SPREAD_Z_SHORT_TH,
                        long_th: float = SPREAD_Z_LONG_TH) -> pd.Series:
    """'short_only'/'long_only'/'neutral'/NaN(워밍업)."""
    out = pd.Series(index=spread_z.index, dtype=object)
    valid = spread_z.notna()
    out[valid & (spread_z >= short_th)] = "short_only"
    out[valid & (spread_z <= long_th)] = "long_only"
    out[valid & (spread_z < short_th) & (spread_z > long_th)] = "neutral"
    return out


def known_at_shifted_1h(df_1h: pd.DataFrame) -> pd.DataFrame:
    """1h 인덱스(open_time)를 +1h 해 '이 값이 알려지는 시점(봉 마감)'으로 재색인."""
    out = df_1h.copy()
    out.index = out.index + pd.Timedelta(hours=1)
    return out


def align_1h_to_15m(df15: pd.DataFrame, data_1h: pd.DataFrame) -> pd.DataFrame:
    """15m 각 봉의 종가시각(open_time+15m)에 '그 시점까지 알려진' 가장 최근 1h 값을
    backward merge_asof 로 매핑(룩어헤드 방지: 미확정 1h 봉 참조 불가)."""
    known = known_at_shifted_1h(data_1h).sort_index()
    close_times = (df15.index + pd.Timedelta(minutes=15)).astype("datetime64[ns, UTC]")
    left = pd.DataFrame({"close_time": close_times, "bar_time": df15.index})
    right = known.reset_index().rename(columns={known.index.name or "index": "close_time"})
    merged = pd.merge_asof(left, right, on="close_time", direction="backward")
    merged = merged.set_index("bar_time")
    return merged.drop(columns=["close_time"])


# ------------------------------------------------------------------ BTC 15m 지표

def donchian(df: pd.DataFrame, period: int = DONCHIAN_LOOKBACK) -> tuple[np.ndarray, np.ndarray]:
    """직전(shift 1봉) period봉 고점/저점(현재봉 미포함, 룩어헤드/자기참조 방지)."""
    hi = df["high"].rolling(period).max().shift(1).to_numpy(float)
    lo = df["low"].rolling(period).min().shift(1).to_numpy(float)
    return hi, lo


@dataclass
class BtcSignals:
    df15: pd.DataFrame
    don_hi: np.ndarray
    don_lo: np.ndarray
    atr14: pd.Series


def build_btc_signals(donchian_period: int = DONCHIAN_LOOKBACK) -> BtcSignals:
    df15 = load_klines_15m(TRADE_SYMBOL)
    don_hi, don_lo = donchian(df15, donchian_period)
    atr14 = ind.atr(df15, 14)
    return BtcSignals(df15=df15, don_hi=don_hi, don_lo=don_lo, atr14=atr14)
