"""진단 전용 스크립트(본 백테스트 산출물 아님) — n=7 vs n=35 유니버스에서 rank_churn=0
빈도가 어떻게 달라지는지 확인. 결과는 리포트 본문에 인용."""
import os
from pathlib import Path

import pandas as pd

SP = Path(os.environ.get(
    "RANKCHURN_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/rankchurn"))

KCOLS = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume",
         "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


def load(sym, subdir):
    files = sorted((SP / "data" / subdir).glob(f"{sym}-1h-*.csv"))
    parts = []
    for p in files:
        with open(p) as f:
            first = f.readline()
        has_header = "open_time" in first
        df = pd.read_csv(p, header=0 if has_header else None,
                         names=KCOLS if not has_header else None)
        df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
        if df.empty:
            continue
        df["open_time"] = df["open_time"].astype("int64")
        parts.append(df)
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    out["quote_volume"] = out["quote_volume"].astype(float)
    return out[["quote_volume"]]


SYMS7 = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
EXT = ["LTCUSDT", "LINKUSDT", "TRXUSDT", "DOTUSDT", "AVAXUSDT", "UNIUSDT", "ATOMUSDT", "ETCUSDT",
       "FILUSDT", "NEARUSDT", "ALGOUSDT", "ICPUSDT", "FTMUSDT", "XLMUSDT", "THETAUSDT", "EGLDUSDT",
       "XTZUSDT", "ZECUSDT", "DASHUSDT", "WAVESUSDT", "ONEUSDT", "HBARUSDT", "KSMUSDT", "RUNEUSDT",
       "SANDUSDT", "MANAUSDT", "GRTUSDT", "AAVEUSDT"]


def build_vol24(syms, subdir_map):
    cols = {}
    for s in syms:
        df = load(s, subdir_map[s])
        if df.empty:
            print("EMPTY", s)
            continue
        cols[s] = df["quote_volume"].rolling(24, min_periods=24).sum()
    return pd.DataFrame(cols).sort_index()


def main():
    subdir_map = {s: "klines1h" for s in SYMS7}
    subdir_map.update({s: "klines1h_ext" for s in EXT})

    for n_label, syms in [("n=7", SYMS7), ("n=35", SYMS7 + EXT)]:
        vol24 = build_vol24(syms, subdir_map)
        vol24 = vol24.dropna()
        rank = vol24.rank(axis=1, method="average", ascending=False)
        churn = rank.diff(24).abs().mean(axis=1).dropna()
        print(n_label, "n_symbols=", len(syms), "obs=", len(churn),
              "range", churn.index.min(), churn.index.max())
        print("  zero frac:", (churn == 0).mean())
        print("  describe:\n", churn.describe())


if __name__ == "__main__":
    main()
