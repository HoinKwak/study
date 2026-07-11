# Backtest — Donchian Channel Breakout + ADX>20 + Volume filter

- **Spec**: `research/strategies/donchian-adx-breakout.md`
- **Implementation**: `research/impl/strategies.py` → `DonchianAdxStrategy` (+ `donchian_channel` helper)
- **Runner**: `research/impl/runner.py` (`donchian`, `sens_donchian`)
- **Verdict**: **FAIL** (net-negative on every full run; the two positive sub-periods do not persist
  out-of-sample — overfitting signature)

## Method / reproducibility

- Driven through `SleeveBacktester(sleeve_kind="mid")` with the custom Strategy injected — reuses the
  framework fee + slippage + intra-bar SL/TP (stop-first) + CLOSE-signal exit. **No production code
  modified.**
- **Fees/slippage = framework defaults**: taker 0.05%/side + slippage 0.02% (≈0.14% round trip).
- Rules: **long** when close > highest-high of the prior N=20 bars (channel `shift(1)`, no look-ahead)
  **AND** ADX(14) ≥ 20 **AND** breakout-bar volume ≥ 1.0× mean(prior 10 bars). Short is the mirror.
  Hard SL = channel **midline** at entry; exit = trailing midline cross (CLOSE emitted each bar when
  close falls back through the recomputed midline). TP left far (trend runner). Sizing = risk 1%/trade,
  notional capped at 100% equity. Warmup 60, cooldown 3 bars.
- Added helpers (indicators.py had no Donchian): `donchian_channel()` pure function. ADX/ATR reused
  from `indicators.py`. **No OI/derivatives needed** — spec is fully OHLCV, so nothing was approximated.
- Data: `data-api.binance.vision` spot mirror. **5m ~30 days**, **15m ~180 days**; each split 1st/2nd
  half for consistency.
- Commands:
  ```
  python research/impl/runner.py donchian
  python research/impl/runner.py sens_donchian
  ```

## Results — 5m signal, ~30 days

| symbol / period    |  ret%  |  PF  | win% | #tr | MDD%  | fees (% of start) |
|--------------------|-------:|-----:|-----:|----:|------:|------------------:|
| BTC full           | -43.88 | 0.47 | 25.9 | 185 | 43.88 | 33.6% |
| BTC 1st half       | -21.65 | 0.53 | 25.0 |  92 | 25.77 | 19.1% |
| BTC 2nd half       | -28.21 | 0.41 | 27.2 |  92 | 28.54 | 18.4% |
| ETH full           | -26.52 | 0.74 | 28.0 | 182 | 33.29 | 34.8% |
| ETH 1st half       |  +6.62 | 1.14 | 32.2 |  87 | 12.13 | 18.2% |
| ETH 2nd half       | -30.90 | 0.38 | 23.7 |  93 | 31.16 | 15.5% |
| SOL full           | -28.26 | 0.70 | 30.8 | 185 | 31.14 | 27.3% |
| SOL 1st half       |  +3.52 | 1.08 | 37.1 |  89 |  8.51 | 14.1% |
| SOL 2nd half       | -31.14 | 0.37 | 24.2 |  95 | 31.14 | 12.6% |

## Results — 15m signal, ~180 days

| symbol / period    |  ret%  |  PF  | win% | #tr | MDD%  | fees (% of start) |
|--------------------|-------:|-----:|-----:|----:|------:|------------------:|
| BTC full           | -61.75 | 0.63 | 24.0 | 391 | 65.00 | 41.9% |
| BTC 1st half       | -22.33 | 0.77 | 27.3 | 194 | 29.17 | 23.5% |
| BTC 2nd half       | -51.17 | 0.40 | 20.9 | 196 | 51.38 | 23.2% |
| ETH full           | -29.97 | 0.84 | 29.7 | 380 | 41.21 | 41.0% |
| ETH 1st half       |  +5.31 | 1.05 | 30.9 | 191 | 13.14 | 20.1% |
| ETH 2nd half       | -33.71 | 0.60 | 28.2 | 188 | 35.42 | 19.6% |
| SOL full           | -44.11 | 0.71 | 29.2 | 384 | 45.10 | 30.2% |
| SOL 1st half       | -16.87 | 0.80 | 28.3 | 191 | 23.60 | 15.1% |
| SOL 2nd half       | -32.22 | 0.62 | 30.2 | 192 | 32.56 | 18.2% |

## Sensitivity (BTC/USDT 15m, 180d)

| variant                 | ret%   |  PF  | win% | #tr | MDD%  |
|-------------------------|-------:|-----:|-----:|----:|------:|
| base (N20, adx20, vol1.0)| -61.75 | 0.63 | 24.0 | 391 | 65.00 |
| N=55                    | -17.99 | 0.83 | 29.4 | 201 | 30.40 |
| adx_min 25              | -49.28 | 0.64 | 22.6 | 287 | 54.45 |
| adx_min 0 (filter off)  | -77.90 | 0.64 | 23.4 | 548 | 78.46 |
| vol_mult 1.5            | -57.97 | 0.60 | 23.7 | 350 | 62.25 |

**The filters do exactly what the source claimed — directionally.** Turning the ADX filter *off*
is the worst result (-77.9%, 548 trades); tightening the channel to N=55 roughly halves the trade
count and cuts losses to -18% (PF 0.83, best of the sweep). So ADX + a wider channel genuinely
reduce the number of bad breakouts. But none of it reaches break-even, let alone PF ≥ 1.3.

## Verdict — FAIL

- **Every full-history run loses money** (PF 0.47–0.84). Best full run is ETH 15m at -30% / PF 0.84.
- **The only green cells are 1st-half sub-periods** (ETH 5m +6.6%, SOL 5m +3.5%, ETH 15m +5.3%) — and
  in every case the *same symbol's* 2nd half collapses (PF 0.37–0.60). That in/out-of-sample flip is
  the textbook signature of a fragile, regime-dependent edge, **not** a durable one. Flagged as
  overfitting risk; not passable.
- **Win rate 24–31% with a trailing exit** means the strategy relies on rare large trend runners to
  pay for many small losers, but at 5m/15m the runners are too small/infrequent to cover ~0.14%
  round-trip cost × 180–390 trades (fees alone are 15–42% of equity).
- **Better than EMA, and the filters clearly help** (consistent with the source's 52→58→63% win-rate
  claim as *directional* evidence), so the concept has some merit — but on our intraday TFs it is still
  net-losing. The scout's note that pure breakouts "collapse quickly in range regimes" is confirmed:
  the ADX/volume filters soften the collapse without eliminating it.
- **Where it might work**: N=55 wide-channel + ADX filter on higher TFs (4h/1d) and/or maker entries,
  or as a *filter/confirmation signal* bolted onto an existing sleeve (ADX regime gate for
  `regime.py`) rather than a standalone intraday entry engine. Not viable standalone as specced.
