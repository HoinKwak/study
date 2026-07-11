# Backtest — EMA 9/21 Crossover (ATR stop + fixed R:R)

- **Spec**: `research/strategies/ema-9-21-crossover.md`
- **Implementation**: `research/impl/strategies.py` → `EmaCrossStrategy`
- **Runner**: `research/impl/runner.py` (`ema`, `sens_ema`)
- **Verdict**: **FAIL** (net-negative on every symbol / TF / sub-period; no parameter rescues it)

## Method / reproducibility

- Driven through `SleeveBacktester(sleeve_kind="mid")` with our custom Strategy injected
  (`bt.strategy = EmaCrossStrategy(...)`). This reuses the framework's fee + slippage +
  intra-bar SL/TP (stop-first) + CLOSE-signal exit logic — **no production code modified**.
- **Fees/slippage = framework defaults**: taker 0.05%/side + slippage 0.02% (≈0.14% round trip).
- Rules: long on EMA9 crossing above EMA21 on the last **closed** bar, short on cross-down.
  SL = entry ± 1.5×ATR(14); TP = entry ± 2.0×stop_dist (fixed 1:2 R:R). Reverse-cross closes
  the position (spec option, default ON). Position sizing = risk 1%/trade (framework RiskManager),
  notional capped at 100% equity. Warmup 60 bars, cooldown 0.
- No look-ahead: signals use only closed bars; entry fill = signal-bar close + slippage.
- Data: `data-api.binance.vision` spot mirror. **5m capped to ~30 days** (whipsaw-heavy TF, our
  scalp signal TF); **15m over ~180 days** (our mid signal TF). Each run also split into
  1st/2nd half for a crude in/out-of-sample consistency check.
- Commands:
  ```
  python research/impl/runner.py ema
  python research/impl/runner.py sens_ema
  ```

## Results — 5m signal, ~30 days

| symbol / period    |  ret%  |  PF  | win% | #tr | MDD%  | fees (% of start) |
|--------------------|-------:|-----:|-----:|----:|------:|------------------:|
| BTC full           | -71.74 | 0.37 | 27.0 | 293 | 71.74 | 49.3% |
| BTC 1st half       | -41.58 | 0.39 | 29.4 | 136 | 42.69 | 30.4% |
| BTC 2nd half       | -52.86 | 0.32 | 24.4 | 156 | 52.86 | 31.3% |
| ETH full           | -75.54 | 0.42 | 28.1 | 320 | 75.55 | 48.5% |
| ETH 1st half       | -47.41 | 0.42 | 27.2 | 151 | 48.14 | 31.7% |
| ETH 2nd half       | -54.78 | 0.39 | 28.1 | 167 | 55.00 | 30.7% |
| SOL full           | -67.60 | 0.51 | 28.6 | 280 | 67.60 | 41.5% |
| SOL 1st half       | -36.92 | 0.54 | 30.8 | 133 | 40.80 | 25.2% |
| SOL 2nd half       | -49.85 | 0.44 | 26.0 | 146 | 49.85 | 25.2% |

## Results — 15m signal, ~180 days

| symbol / period    |  ret%  |  PF  | win% | #tr | MDD%  | fees (% of start) |
|--------------------|-------:|-----:|-----:|----:|------:|------------------:|
| BTC full           | -85.20 | 0.55 | 29.2 | 559 | 85.20 | 55.1% |
| BTC 1st half       | -55.64 | 0.58 | 30.0 | 277 | 56.74 | 36.7% |
| BTC 2nd half       | -66.22 | 0.51 | 28.5 | 281 | 66.44 | 41.7% |
| ETH full           | -72.24 | 0.64 | 30.1 | 539 | 76.20 | 50.9% |
| ETH 1st half       | -51.67 | 0.61 | 28.3 | 269 | 55.89 | 30.6% |
| ETH 2nd half       | -41.79 | 0.71 | 32.0 | 269 | 46.83 | 42.5% |
| SOL full           | -68.03 | 0.71 | 29.9 | 536 | 69.62 | 52.9% |
| SOL 1st half       | -36.86 | 0.74 | 31.7 | 265 | 42.00 | 30.4% |
| SOL 2nd half       | -48.70 | 0.66 | 28.1 | 270 | 51.44 | 35.8% |

## Sensitivity (BTC/USDT 15m, 180d)

| variant                | ret%   |  PF  | win% | #tr | MDD%  |
|------------------------|-------:|-----:|-----:|----:|------:|
| base (9/21, sl1.5, rr2)| -85.20 | 0.55 | 29.2 | 559 | 85.20 |
| fast/slow 5/13         | -93.99 | 0.52 | 25.4 | 826 | 93.99 |
| fast/slow 12/26        | -85.97 | 0.49 | 28.0 | 475 | 86.00 |
| rr 3.0                 | -85.55 | 0.54 | 23.4 | 530 | 85.55 |
| no reverse-exit        | -79.27 | 0.62 | 32.3 | 465 | 79.27 |

Every variant is deeply negative (PF 0.49–0.62). Faster EMAs make it worse (more whipsaw);
slower EMAs and disabling the reverse-exit reduce trade count and losses marginally but come
nowhere near break-even. The edge is not parameter-dependent — it is simply absent at these TFs.

## Verdict — FAIL

- **Net-negative after fees everywhere.** All 18 symbol×period cells lose money; PF ranges 0.32–0.74,
  never approaching the 1.3 bar. Win rate ~27–32% is by design (low-win / high-R trend-follow),
  but the realized average R does not clear the ~0.14% round-trip cost at 5m/15m.
- **Sample size is fine** (280–560 trades) — the loss is statistically real, not noise.
- **Fees are the executioner**: 40–55% of starting equity is paid in fees/slippage across the
  full runs. A crossover system fires far too often at intraday TFs for taker costs to survive.
- **Consistent, not overfit** — it fails uniformly across BTC/ETH/SOL and both sub-periods, so no
  cherry-picking could salvage it.
- This matches the scout's own caution: the source's edge was concentrated on **D1** (and even H1
  crypto was PF≈1). At our scalp/mid TFs (5m/15m) there is no edge. Not viable as-is; would only be
  worth revisiting on 4h/1d with maker fills — outside our short-timeframe sleeves.
