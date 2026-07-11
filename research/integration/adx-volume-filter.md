# Integration review — EMA 9/21, Donchian+ADX+Vol, and the ADX/volume filter idea

- **Inputs**: `research/backtests/ema-9-21-crossover.md`, `research/backtests/donchian-adx-breakout.md`
  (both **FAIL**), scout's top-2 candidates.
- **Reviewed our code**: `strategy/scalp.py`, `strategy/mid.py`, `strategy/swing.py`, `strategy/regime.py`,
  `signals/indicators.py` (`adx`, `bollinger_bands`, `atr`), `portfolio/sleeve.py`, `portfolio/worker.py`.
- **Scope**: proposal only, no production code changed.

---

## 1. EMA 9/21 crossover — **REJECT (d)**

Direct adoption rejected. Not adoptable in any form on our sleeves.

- Net-negative on **all 18** symbol×TF×period cells. PF 0.32–0.74, never near the 1.3 bar.
- Fees are the executioner: **40–55% of starting equity** paid in fees/slippage on full runs; a
  crossover fires far too often for taker costs at 5m/15m.
- Consistent across BTC/ETH/SOL and both sub-periods (not overfit) and parameter-insensitive
  (every variant PF 0.49–0.62) → the edge is *absent* at our TFs, not mis-tuned.
- No complementary use either: we have **no MACD/EMA-cross entry** to reinforce, and `regime.py`
  already derives trend direction from ADX/DI far more robustly than a raw EMA cross would.
- Would only be worth revisiting on 4h/1d with maker fills — outside our short-TF sleeves.

## 2. Donchian breakout + ADX>20 + Volume — **REJECT standalone (d)**

Direct adoption as an intraday entry engine rejected.

- Every full-history run loses money (PF 0.47–0.84; best full run ETH 15m −30% / PF 0.84).
- The only green cells are **1st-half** sub-periods (ETH 5m +6.6%, SOL 5m +3.5%, ETH 15m +5.3%) and
  the **same symbol's 2nd half collapses** every time (PF 0.37–0.60) — textbook in/out-of-sample flip.
- 24–31% win rate on a trailing exit needs rare large runners; at 5m/15m they don't cover
  ~0.14% round-trip × 180–390 trades (fees alone 15–42% of equity).
- **The one salvageable observation**: the ADX+volume filters are *directionally* useful.
  Turning ADX off is the worst cell (−77.9%, 548 trades); ADX + a wider N=55 channel roughly
  halves trades and cuts losses to −18% (PF 0.83, best of the sweep). The filters **soften the
  collapse but never eliminate it.** Assessed on its own below.

---

## 3. The salvageable idea: add an ADX + volume gate to `ScalpStrategy`?

### Verdict: **REJECT for redundancy (d)** — the gate is already present in our scalp, and stricter.

This is the important part, so the reasoning is spelled out. The proposed filter is
"**ADX(14) ≥ 20** on the signal bar **AND** breakout-bar volume **≥ 1.0× mean(prior 10)**".
Both halves are already enforced by `ScalpStrategy` today — more tightly.

**(a) The ADX gate already exists, at a higher threshold, with direction.**
`worker.py:272` computes `confirm_regime = detect_regime(confirm_df)[0]` on the scalp confirm TF (15m)
and passes it to `ScalpStrategy.decide`. `regime.detect_regime` *is* an ADX(14)+DI classifier
(`trend_th=25`, `range_th=20`). In `scalp.py:129-130`:

```python
long_regime_ok  = confirm_regime is None or confirm_regime is Regime.TREND_UP
short_regime_ok = confirm_regime is None or confirm_regime is Regime.TREND_DOWN
```

A long only fires when the regime is `TREND_UP`, which requires **ADX ≥ 25 AND +DI > −DI**. `RANGE`
(ADX < 20) is blocked, and so is `NEUTRAL` (20 ≤ ADX < 25). So the scalp already demands a **stricter
ADX floor (25 vs 20)** *plus* DI directional agreement — information the Donchian filter's bare
`ADX ≥ 20` does not even carry. The proposed gate is a weaker subset of what ships today.

**(b) The volume gate already exists, ~4× stronger.**
`scalp.py:109-110` requires `bar.volume ≥ vol_spike_mult(4.0) × mean(prior 20)`. The Donchian filter
asks for `≥ 1.0× mean(prior 10)` — i.e. merely above-average. Our 4× spike is a far tighter screen.
Adding a 1× floor changes nothing; it never binds when a 4× floor already passed.

**(c) Plus gates the Donchian idea doesn't have at all**: Bollinger **squeeze** pre-filter
(`squeeze_pctile=30`, the only filter that gave consistent 3-symbol×2-period improvement per the
inline note), a strong-body/`min_body_atr` screen, and an **OI-increase** confirm. Our scalp is
already a heavily-gated, *different* engine (squeeze BB breakout, ~68% win rate per `sleeve.py`),
not the bare Donchian breakout the filter was measured on.

**(d) The backtest evidence argues against it even on its own terms.** In the Donchian sweep ADX is a
*loss-reducer on a losing engine*, not an edge-creator — best filtered cell is still −18%. There is no
result anywhere showing ADX turning a profitable engine more profitable. Bolting a redundant,
looser copy of it onto a scalp that already passed backtest has no positive mechanism and a real
cost: **it can only cut signal frequency.** `sleeve.py:36-39` notes frequency is already a concern
(the universe was widened to $50M/`dynamic_universe` specifically to recover signals the squeeze
filter removes). Another gate that removes trades works directly against that.

### The one honest orthogonal nuance (and why it's still not worth a cycle)

The scalp's ADX gate lives on the **confirm TF (15m)**; the Donchian ADX was on the **signal TF**.
So a *strictly* new variable would be a **same-TF (5m) ADX floor** on the signal itself — "don't take
the 5m breakout unless the 5m bar is itself in a strong-trend state, even if 15m says TREND." That is
not literally identical to what we have. But it is a thin edge case: (i) 5m ADX and 15m regime are
highly correlated, so it will rarely disagree; (ii) when it does disagree it mostly just deletes
trades → frequency cost above; (iii) the sweep gives no reason to expect it flips sign of expectancy.
Low expected value, real downside. **Recommend not spending a build/backtest cycle on it.**

---

## Optional A/B (only if the team wants to spend one cycle to close the question)

If, despite the above, we want an empirical nail in the coffin, run the **cheapest** discriminating
test and **pre-register** the kill criteria so it can't turn into a tuning expedition.

- **Variant**: in `scalp.py`, after the squeeze filter and before the entry checks (around line 118,
  i.e. after `bar`/`atr_val` are computed), add one guard:
  `adx_now, _, _ = ind.adx(df, 14); if adx_now.iloc[-1] < ADX_MIN: HOLD("adx 약함")`.
  This is the *signal-TF* floor (the only non-redundant version). One threshold only: **ADX_MIN = 20**.
  Do **not** also loosen or touch volume/squeeze/OI — those already dominate.
- **Baseline**: current `ScalpStrategy` unchanged.
- **Universe / TF**: BTC, ETH, SOL on **5m** (scalp signal TF; confirm 15m), reuse the existing
  `SleeveBacktester(sleeve_kind="scalp")` harness, framework fees (0.05%/side + 0.02% slip),
  same warmup/cooldown. Split 1st/2nd half for consistency, exactly as the two reports did.
- **Metric**: net return, PF, #trades, MDD per cell, plus **trades removed vs baseline**.

### Success / rollback criteria (pre-registered)

- **ADOPT (b — entry filter)** only if the ADX floor improves **net return AND PF in ≥ 5 of 6**
  symbol×half cells, the improvement holds in **both** halves of each symbol (no in/out flip like the
  Donchian green cells), and it removes **< 40%** of baseline trades. Anything less → do not ship.
- **ROLLBACK / DROP** if PF or return degrades in the majority of cells, if gains live in only one
  half (overfit signature), or if trade count drops so far that scalp frequency materially falls
  (the exact problem `sleeve.py` engineered around). Given §3, this is the expected outcome.

---

## Priority summary

| Idea | Recommendation | Priority |
|------|----------------|----------|
| EMA 9/21 crossover (adopt) | **REJECT (d)** — net-negative everywhere, fee-killed | — |
| Donchian+ADX+Vol standalone | **REJECT (d)** — net-losing intraday, overfit green cells | — |
| ADX+vol filter → scalp | **REJECT (d)** — redundant with existing ADX≥25 regime gate + 4× vol spike | drop; optional 1-cycle A/B above only to formally close it |

**Bottom line:** both scout strategies are correctly failed and neither should be adopted, as-is or as
a filter. The "add an ADX + volume gate" idea is already implemented in `ScalpStrategy` — at a tighter
ADX threshold (25 vs 20, with DI direction) and a ~4× tighter volume threshold — so it adds no
orthogonal information and only risks cutting an already-scarce signal rate. Recommend **dropping it**;
if empirical closure is wanted, run the single pre-registered signal-TF-ADX A/B and expect a rollback.
