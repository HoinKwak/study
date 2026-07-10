"""파라미터 그리드 스윕 — 슬리브 전략의 핵심 파라미터 조합을 백테스트로 비교.

    python -m scripts.sweep_params --sleeve scalp --symbol BTC/USDT --days 14
    python -m scripts.sweep_params --sleeve mid --symbol BTC/USDT --days 90
    python -m scripts.sweep_params --sleeve swing --symbol BTC/USDT --days 365

결과는 수익률/PF/승률/거래수/MDD 표로 출력. 과최적화 주의 — 조합 수를 작게 유지하고,
최종 선택은 다른 심볼/기간으로 재검증할 것.
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.backtest import SleeveBacktester  # noqa: E402
from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.data import ohlcv_to_df  # noqa: E402
from crypto_trader.strategy import MidStrategy, ScalpStrategy, SwingStrategy  # noqa: E402
from crypto_trader.utils import get_logger  # noqa: E402

from scripts.run_backtest import SLEEVE_TF, fetch_history  # noqa: E402

log = get_logger("sweep")

# 슬리브별 그리드 (작게 유지 — 과최적화 방지)
GRIDS = {
    "scalp": {
        "vol_spike_mult": [3.0, 4.0],
        "reward_risk_ratio": [1.5, 2.0, 2.5],
    },
    "mid": {
        "min_hist_frac": [0.0003, 0.0006, 0.001],
        "st_mult": [3.0, 4.0],
    },
    "swing": {
        "rsi_os": [20.0, 25.0],
        "sl_buffer_atr": [1.0, 1.5, 2.0],
    },
}

STRATEGY_CLS = {"scalp": ScalpStrategy, "mid": MidStrategy, "swing": SwingStrategy}


def main() -> None:
    parser = argparse.ArgumentParser(description="파라미터 스윕")
    parser.add_argument("--sleeve", required=True, choices=["scalp", "mid", "swing"])
    parser.add_argument("--symbol", default="BTC/USDT")
    parser.add_argument("--days", type=int, default=None)
    args = parser.parse_args()

    settings = get_settings()
    signal_tf, confirm_tf = SLEEVE_TF[args.sleeve]
    default_days = {"swing": 365, "mid": 90, "scalp": 14}
    days = args.days or default_days[args.sleeve]

    log.info("데이터 수집: %s %s %d일", args.symbol, signal_tf, days)
    df = ohlcv_to_df(fetch_history(args.symbol, signal_tf, days))
    log.info("%d 캔들", len(df))

    grid = GRIDS[args.sleeve]
    keys = list(grid.keys())
    rows = []
    for combo in itertools.product(*grid.values()):
        params = dict(zip(keys, combo))
        # swing 의 rsi_ob 는 rsi_os 와 대칭으로
        if args.sleeve == "swing" and "rsi_os" in params:
            params["rsi_ob"] = 100.0 - params["rsi_os"]
        bt = SleeveBacktester(settings, args.sleeve, confirm_tf=confirm_tf)
        bt.strategy = STRATEGY_CLS[args.sleeve](settings, **params)
        res = bt.run(args.symbol, df)
        rows.append((params, res))
        log.info("%s → %+.2f%% (PF %.2f, %d회)", params, res.total_return_pct,
                 res.profit_factor, res.num_trades)

    rows.sort(key=lambda r: r[1].total_return_pct, reverse=True)
    print(f"\n===== 스윕 결과: {args.sleeve} {args.symbol} {days}일 =====")
    print(f"{'파라미터':<52} {'수익률':>8} {'PF':>6} {'승률':>6} {'횟수':>4} {'MDD':>7} {'수수료':>9}")
    for params, res in rows:
        pstr = ", ".join(f"{k}={v}" for k, v in params.items())
        print(f"{pstr:<52} {res.total_return_pct:>+7.2f}% {res.profit_factor:>6.2f} "
              f"{res.win_rate:>5.1f}% {res.num_trades:>4} {res.max_drawdown_pct:>6.2f}% "
              f"{res.total_fees:>8.2f}")


if __name__ == "__main__":
    main()
