# Backtest — Bollinger squeeze → volatility-expansion breakout (swing)

- **Spec**: `research/strategies/bollinger-squeeze-breakout-daily.md`
- **Implementation**: `research/impl/swing_strategies.py` → `BollingerSqueezeBreakoutStrategy`
- **Runner / engine**: `research/impl/swing_runner.py` (`squeeze`, `sens_squeeze`)
- **Verdict**: **FAIL as specced** (base with shorts is net-negative on BTC/ETH, PF 0.79/1.02).
  **HOLD for the long-only 4h variant** — net-positive on all three symbols (PF 1.35/1.11/1.80),
  BTC & SOL consistent across halves. Not a clean PASS (ETH PF 1.11 < 1.3 and its 2nd half collapses;
  heavy fee drag; 1d dead). Best-looking of the three but needs a dedicated OOS retest before promotion.

## Method / reproducibility

- Same **custom replay engine** as the golden-cross report (framework-identical fees/slippage:
  0.05%/side + 0.02% slippage; stop-priority intra-bar SL/TP; `CLOSE` at bar close). Indicators reused
  read-only, **no production code modified.**
- **Squeeze tag**: `BandWidth=(upper−lower)/mid` with BB(20, 2σ). Squeeze threshold =
  `min(0.05, rolling 20th-pctile of BW over trailing 126 bars)` — computed on closed bars only, **no
  lookahead**. A bar is "recently squeezed" if any of the **6 bars before** the breakout bar were ≤ threshold.
- **Entry**: recently-squeezed **and** close breaks the band (long: close > upper; short: close < lower)
  **and** breakout-bar volume ≥ 1.2× mean(prior 20) **and** (EMA200 trend gate) breakout direction
  agrees with price-vs-EMA200.
- **Exit**: trailing **midline** (SMA20) — close back through it ⇒ `CLOSE`. Hard SL = entry ∓ 2×ATR(14).
- **Sizing**: full allocation (100% notional, 1×). **Data**: mirror spot, 1d ~1100 d, 4h ~760 d
  (BTC/ETH/SOL). Commands: `python research/impl/swing_runner.py squeeze` · `... sens_squeeze`

## Results — base (long+short), full allocation

| period/symbol       |  ret%  |   PF  | win% | #tr | MDD% | fees(%eq) |
|---------------------|-------:|------:|-----:|----:|-----:|----------:|
| **1d ~3yr** — squeeze on daily is too rare (0–1 trades/symbol → n/a) |||||||
| BTC full            |  −8.88 |  0.00 |   0.0 |  1 |  8.9 | 0.1 |
| **4h ~2yr** |||||||
| BTC full            | −20.55 |  0.79 |  29.5 | 78 | 34.1 | 7.0 |
| BTC 1st / 2nd half  | −13.76 / −10.64 | 0.72 / 0.79 || 34 / 42 | 21.6 / 24.9 ||
| ETH full            |  +1.75 |  1.02 |  31.7 | 63 | 34.0 | 6.6 |
| ETH 1st / 2nd half  | +4.68 / −12.01 | 1.10 / 0.78 || 29 / 32 | 11.9 / 34.0 ||
| SOL full            | +56.41 |  1.83 |  44.7 | 38 | 21.3 | 4.6 |
| SOL 1st / 2nd half  | +19.48 / +27.16 | 1.89 / 1.79 || 15 / 20 | 9.5 / 21.3 ||

Base is carried entirely by SOL; BTC is a clear loser (PF 0.79) and ETH is breakeven. **Short trades
are the poison** (see sensitivity).

## Results — LONG-ONLY variant, full allocation (the promising cut)

| period/symbol       |  ret%  |   PF  | win% | #tr | MDD% | fees(%eq) |
|---------------------|-------:|------:|-----:|----:|-----:|----------:|
| BTC 4h full         | +16.52 |  1.35 |  33.3 | 42 |  7.0 | 4.7 |
| BTC 1st / 2nd half  | +11.83 / +1.06 | 1.47 / 1.06 || 21 / 19 | 6.1 / 6.9 ||
| ETH 4h full         |  +6.32 |  1.11 |  33.3 | 33 | 19.8 | 3.9 |
| ETH 1st / 2nd half  | +16.18 / −17.15 | 1.94 / **0.40** || 14 / 17 | 5.6 / 19.8 ||
| SOL 4h full         | +28.05 |  1.80 |  47.6 | 21 | 14.1 | 2.5 |
| SOL 1st / 2nd half  | +20.39 / +3.33 | 5.21 / 1.16 || 7 / 11 | 2.7 / 14.1 ||
| 1d (all symbols)    | 0 trades — squeeze+breakout+vol never coincides on daily in-window |||||

## Sensitivity (BTC/USDT 4h full)

| variant                 | ret%   |  PF  | #tr | MDD% |
|-------------------------|-------:|-----:|----:|-----:|
| base pct20 vol1.2 gateON| −20.55 | 0.79 |  78 | 34.1 |
| squeeze_pct 0.10        | −18.40 | 0.71 |  51 | 30.8 |
| squeeze_pct 0.30        | −22.21 | 0.78 |  84 | 32.6 |
| vol_mult 1.0            | −22.55 | 0.78 |  82 | 34.0 |
| trend gate OFF          | −33.49 | 0.73 | 104 | 47.8 |
| atr_sl 3.0              | −23.33 | 0.76 |  78 | 36.4 |
| **long-only**           | **+16.52** | **1.35** | 42 | 7.0 |

- **Long-only is the single decisive axis.** Every other knob (squeeze percentile, vol multiplier,
  trend gate, ATR stop) leaves the base net-negative; removing shorts flips BTC from −20.5% to +16.5%.
  The EMA200 gate matters (turning it off is the worst, −33%).

## Verdict — FAIL (base) / HOLD (long-only 4h)

- **As specced (long+short): FAIL.** BTC PF 0.79, ETH PF 1.02 — below breakeven/1.3; only SOL clears
  the bar. Crypto false-breakouts + short losses dominate; ~40–80 trades × 0.14% round-trip burns
  4–7% of equity in fees.
- **Long-only 4h: net-positive on all three symbols** (+16.5 / +6.3 / +28.0; PF 1.35 / 1.11 / 1.80),
  with BTC and SOL **positive in both halves** — the most consistent result in this batch. But it is
  **not a clean PASS**: ETH sits at PF 1.11 with a losing 2nd half (PF 0.40), the win rate is low
  (33%) so it leans on rare runners, fee drag is high, and "drop shorts" is a post-hoc choice (albeit
  a defensible prior in a net-bullish 2 yr window). **Daily produces no trades** — the "1d is the most
  robust TF" premise from the source does not reproduce; the tradeable edge is a 4h phenomenon.
- **Recommendation**: keep long-only-4h as a **candidate for a dedicated forward/OOS retest** (fresh
  window + a fee-aware exit to cut the 33% win-rate churn) rather than passing it now. It is the
  closest thing to an edge found in this batch.
