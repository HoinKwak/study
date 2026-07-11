# Backtest — Bollinger touch + RSI divergence + centerline-cross confirmation (reversal, swing)

- **Spec**: `research/strategies/bollinger-rsi-divergence-reversal.md`
  (source: YouTube CominiTV `rEsf7aTVXos`, strategy #9 — the one novel idea)
- **Implementation**: `research/impl/swing_strategies.py` → `BollingerRsiDivergenceStrategy`
- **Runner / engine**: `research/impl/swing_runner.py` (`divergence`, `sens_divergence`)
- **Verdict**: **FAIL.** No net tradeable edge on 4h (all symbols PF ≤ 1.03) and every 2nd half is
  negative. 1d shows a positive tilt (PF 1.30, 75% win) but on a **4-trade** sample — not decision-grade.
  **Silver lining, honestly reported**: the video's central claim is *directionally validated* —
  removing the centerline-cross confirmation destroys the strategy (PF 0.44 on 1d, −36%). The filter
  works; it just isn't enough to produce a positive-expectancy standalone system after fees.

## Method / reproducibility

- Same **custom replay engine** (framework-identical fees/slippage; stop-priority intra-bar SL/TP;
  `CLOSE` at bar close; final liquidation). Indicators reused read-only, **no production code modified.**
- **Look-ahead guard on pivots (the critical part)**: a swing low/high at bar *p* is a local extremum
  over `[p−pivot_win, p+pivot_win]` and is **only confirmed once `pivot_win` later bars exist**
  (`confirmed_pivot_*(...)` requires `p + pivot_win ≤ last_closed_bar`). The last `pivot_win` bars can
  never be pivots — so divergence is detected on the confirmation delay the spec demands, never with
  future knowledge.
- **Long entry**: (1) a confirmed swing low pierced the lower band; (2) **bullish divergence** — that
  low is a lower-low in price but a higher-low in RSI(14) vs a prior confirmed low within `div_lookback`;
  (3) **confirmation** — current close freshly crosses **above** the midline (SMA20). Short = mirror.
- **Regime gate**: skip if ADX(14) ≥ 25 (divergences fail in strong trends). **Exit**: opposite band,
  or RR 1.5 TP, or `max_hold=20` bars; SL = `min(signal swing low, entry−1.5×ATR)` (tighter side).
- **Sizing**: full allocation (100% notional, 1×). **Data**: mirror spot, 1d ~1100 d, 4h ~760 d
  (BTC/ETH/SOL). Commands: `python research/impl/swing_runner.py divergence` · `... sens_divergence`

## Results — base, full allocation

| period/symbol       |  ret%  |   PF  | win% | #tr | MDD% | fees(%eq) |
|---------------------|-------:|------:|-----:|----:|-----:|----------:|
| **1d ~3yr** (tiny samples — n/a for a verdict) |||||||
| BTC full            |  +3.24 |  1.30 |  75.0 |  4 | 10.9 | 0.4 |
| ETH full            |  −7.28 |  0.70 |  50.0 |  4 | 21.1 | 0.4 |
| SOL full            | +13.85 |   inf | 100.0 |  1 |  0.0 | 0.1 |
| **4h ~2yr** |||||||
| BTC full            | −15.58 |  0.54 |  50.0 | 28 | 18.7 | 2.6 |
| BTC 1st / 2nd half  | −7.28 / −7.48 | 0.36 / 0.67 || 9 / 16 | 8.7 / 12.5 ||
| ETH full            |  +1.44 |  1.03 |  57.1 | 28 | 16.9 | 3.0 |
| ETH 1st / 2nd half  | +11.74 / −6.29 | 1.62 / 0.76 || 15 / 12 | 9.0 / 16.9 ||
| SOL full            |  +0.60 |  1.01 |  59.4 | 32 | 21.9 | 3.5 |
| SOL 1st / 2nd half  | +8.32 / −7.13 | 1.28 / 0.79 || 17 / 15 | 8.9 / 21.9 ||

Win rates are respectably high (50–59%) but net is breakeven-to-negative: losers outsize winners, and
**all three 2nd halves are negative** — the edge (if any) decays out of sample.

## Sensitivity (BTC/USDT)

| variant                 | 1d ret% / PF (#tr) | 4h ret% / PF (#tr) |
|-------------------------|-------------------:|-------------------:|
| base pw3 adx25 conf rr1.5| +3.24 / 1.30 (4)  | −15.58 / 0.54 (28) |
| pivot_win 2             | +8.00 / 1.70 (5)   | −6.10 / 0.86 (37)  |
| pivot_win 5             | −6.15 / 0.40 (2)   | −17.10 / 0.51 (28) |
| ADX gate OFF            | +21.97 / 2.18 (11) | −2.16 / 0.96 (60)  |
| **no centerline confirm** | **−36.06 / 0.44 (13)** | +2.21 / 1.02 (84) |
| rr_target 2.5           | +2.54 / 1.23 (4)   | −15.58 / 0.54 (28) |
| div_lookback 60         | +24.10 / 3.11 (7)  | −21.21 / 0.55 (37) |

- **The confirmation filter is validated (the report's real finding).** On 1d, dropping the
  centerline-cross confirmation collapses the strategy from +3.2%/PF1.30 to −36%/PF0.44 — exactly the
  "don't catch the knife; wait for confirmation" thesis of the video. The mechanism does what it claims.
- On 1d, looser pivots / no-ADX / longer lookback push PF to 2–3 — but always on **≤ 11 trades**, so
  this is noise-grade, not evidence.
- **On 4h nothing rescues it**: every variant is net-negative or a rounding-error positive (PF ≤ 1.02).

## Verdict — FAIL

- **No positive-expectancy standalone system after fees.** 4h — the only TF with a usable sample
  (28–32 trades/symbol) — is net-negative/breakeven on all three symbols (PF 0.54 / 1.03 / 1.01) and
  negative in every 2nd half. 1d has the right *shape* (PF 1.30, 75% win) but 1–4 trades/symbol can't
  support a verdict.
- **But the novel mechanism is not junk.** The centerline-cross confirmation demonstrably raises win
  rate / PF (removing it is catastrophic), and the ADX regime gate helps on 4h. The scout's stated
  worry is confirmed: honestly modelling the pivot-confirmation delay makes signals late and rare, and
  the surviving trades don't clear the fee hurdle. As a **standalone reversal engine: FAIL.** As a
  **confirmation overlay** (a divergence+centerline gate bolted onto an existing entry) the component
  has demonstrated value and could be worth reusing — but that is a different artifact than this spec.
