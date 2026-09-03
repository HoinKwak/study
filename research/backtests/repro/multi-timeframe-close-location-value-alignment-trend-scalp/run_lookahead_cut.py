"""룩어헤드 검증: 특정 시점 이후 데이터를 완전 삭제하고 재실행해, 안전마진 이전 트레이드가
전체실행과 완전 일치하는지 확인(15m/1h/4h 세 TF 모두 절단, >=3 종목)."""
from __future__ import annotations
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine

SYMS = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]
CUTOFF = pd.Timestamp("2024-01-01", tz="UTC")
SAFETY_MARGIN_DAYS = 30


def run_full(sym):
    common.load_klines.cache_clear()
    cfg = engine.RunConfig()
    sig = engine.build_signals(sym, cfg)
    return engine.run_symbol(sym, sig, cfg)


def truncate_and_run(sym):
    tmp_data = common.SP / f"data_trunc_{sym}"
    if tmp_data.exists():
        shutil.rmtree(tmp_data)
    shutil.copytree(common.DATA, tmp_data)
    orig_data = common.DATA
    common.DATA = tmp_data
    for tf in ["15m", "1h", "4h"]:
        d = tmp_data / f"klines_{tf}"
        for f in sorted(d.glob(f"{sym}-{tf}-*.csv")):
            df = pd.read_csv(f)
            df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
            df["open_time"] = df["open_time"].astype("int64")
            dt = pd.to_datetime(df["open_time"], unit="ms", utc=True)
            keep = dt < CUTOFF
            if keep.all():
                continue
            df = df[keep]
            if df.empty:
                f.unlink()
            else:
                df.to_csv(f, index=False)
    common.load_klines.cache_clear()
    cfg = engine.RunConfig()
    sig = engine.build_signals(sym, cfg)
    trades = engine.run_symbol(sym, sig, cfg)
    common.DATA = orig_data
    common.load_klines.cache_clear()
    shutil.rmtree(tmp_data)
    return trades


if __name__ == "__main__":
    safety_cut = CUTOFF - pd.Timedelta(days=SAFETY_MARGIN_DAYS)
    for sym in SYMS:
        full_trades = run_full(sym)
        trunc_trades = truncate_and_run(sym)

        full_safe = [t for t in full_trades if t.entry_time < safety_cut]
        trunc_safe = [t for t in trunc_trades if t.entry_time < safety_cut]

        n = min(len(full_safe), len(trunc_safe))
        mismatches = 0
        for i in range(n):
            a, b = full_safe[i], trunc_safe[i]
            if (a.entry_time != b.entry_time or a.direction != b.direction or
                abs(a.entry_price - b.entry_price) > 1e-6 or
                a.reason != b.reason or a.holding_bars != b.holding_bars or
                abs(a.r_net - b.r_net) > 1e-6):
                mismatches += 1
                if mismatches <= 5:
                    print(f"MISMATCH {sym} idx={i}: full={a} trunc={b}")
        print(f"{sym}: 전체실행 안전마진이전={len(full_safe)} 절단실행={len(trunc_safe)} "
              f"비교됨={n} 불일치={mismatches} 개수차이={len(full_safe)-len(trunc_safe)}")
