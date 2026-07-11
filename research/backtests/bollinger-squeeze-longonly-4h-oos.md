# OOS Validation — Bollinger squeeze→breakout, LONG-ONLY, 4h

- **Candidate**: `BollingerSqueezeBreakoutStrategy(allow_short=False)`, 4h, full allocation.
  Prior report `research/backtests/bollinger-squeeze-breakout-daily.md` marked it **HOLD**
  (only cut net-positive on BTC/ETH/SOL: +16.5/+6.3/+28.0%, PF 1.35/1.11/1.80) and asked for a
  dedicated OOS retest before promotion. This is that retest.
- **Impl / runner**: `research/impl/swing_oos.py` (windowed engine reusing
  `research/impl/swing_strategies.py`); data + costs reused from `research/impl/swing_runner.py`.
- **Costs (identical to framework mid-path)**: taker 0.05%/side + 0.02% slippage, stop-priority
  intrabar SL/TP, CLOSE at bar close. No production code modified.
- **Data**: data-api.binance.vision spot mirror, 4h, ~760 days (≈4560 bars/symbol), warmup 210 bars.
  Sanity check: the windowed engine reproduces the prior report's BTC/ETH/SOL full-window numbers
  to the decimal (+16.52 / +6.32 / +28.05), so any differences below are method, not engine.
- **Reproduce**: `SCRATCH=… python research/impl/swing_oos.py {folds|wf|robust|longonly|multi|all}`

## VERDICT: **REJECT** (fragile / overfit; the "long-only" cut is not structurally defensible)

The edge is a property of the **favorable 2023–early-2024 window**, not a durable signal. Three
independent tests each fail the bar for real money, and the one axis that made it look good
("drop shorts") is a BTC-specific curve-fit that reverses on most alts.

---

## 1) Walk-forward / sequential folds — does the edge persist OOS?

### 1a. Sequential folds (fixed base params, long-only, 4 contiguous folds)

Per-fold trade counts are small (2–14), so any single PF is noisy — but the **sign of the most
recent fold is the signal**, and it is unanimous.

| symbol | fold1 ret%(PF) | fold2 ret%(PF) | fold3 ret%(PF) | **fold4 (most recent) ret%(PF)** | full |
|--------|---------------:|---------------:|---------------:|---------------------------------:|-----:|
| BTC  | +14.0 (1.96) | +2.7 (1.25) | +6.0 (1.86) | **−4.6 (0.55)** | +16.5 |
| ETH  | +18.7 (3.40) | +9.5 (1.95) | −3.1 (0.73) | **−17.5 (0.13)** | +6.3 |
| SOL  | +5.8 (3.00) | +14.3 (8.70) | +10.2 (2.00) | **−3.9 (0.71)** | +28.1 |
| BNB  | −8.4 (0.41) | −6.5 (0.31) | +21.5 (5.02) | **−5.4 (0.32)** | −1.8 |
| XRP  | −8.7 (0.35) | −14.0 (0.02) | +13.0 (10.3) | **−7.2 (0.33)** | −17.6 |
| DOGE | +1.8 (1.19) | 0.0 (n/a) | +22.9 (∞) | **−5.7 (0.51)** | +18.1 |
| ADA  | −3.9 (0.73) | +25.7 (6.87) | +3.4 (2.43) | **−4.5 (0.28)** | +15.0 |
| AVAX | −8.7 (0.33) | +27.0 (8.22) | +18.1 (17.8) | **−18.5 (0.00)** | +6.7 |

**The most-recent fold is net-negative on all 8 symbols (8/8), PF ≤ 0.71 everywhere.** Eight
independent instruments turning negative in the same trailing ~6-month window is not sampling noise
— it is regime decay. The full-window profits are earned in folds 1–3 and given back in fold 4.

### 1b. Anchored walk-forward WITH honest parameter optimization

For each test fold, a 54-combo grid (bb∈{14,20,26} × sqz_pct∈{.10,.20,.30} × vol_mult∈{1.0,1.2,1.5}
× atr_sl∈{2.0,3.0}) is optimized (best PF, ≥5 train trades) on all prior bars, then the winner is
applied **blind** to the next fold. This is the test that matters for money.

| symbol | fold train-best PF | **OOS ret% per fold** | **stitched OOS PF** | OOS #tr |
|--------|-------------------:|-----------------------|--------------------:|--------:|
| BTC | 3.50 / 2.20 / 1.91 | −3.6 / −0.3 / −4.2 | **0.77** (loses) | 32 |
| ETH | 3.54 / 4.04 / 2.55 | +15.8 / −3.1 / −17.6 | **0.87** (loses) | 24 |
| SOL | 4.64 / 6.28 / 9.89 | +14.3 / +10.2 / −3.1 | **1.90** (wins) | 15 |
| **Pooled (BTC+ETH+SOL)** | — | net **+839** on 3×10k | **1.09** | 71 |

- Train PFs looked spectacular (1.9–9.9); **OOS PFs collapse to 0.77 / 0.87 / 1.90.** Two of three
  core symbols **lose money out of sample**; the pooled OOS PF **1.09 is below the 1.3 bar** and is
  carried entirely by SOL.
- The optimizer repeatedly chose the **loosest** squeeze (bb14 / sqz_pct 0.30) because it maximized
  in-sample PF — and that choice failed OOS on BTC. Textbook overfitting: in-sample selection does
  not generalize.

---

## 2) Parameter robustness

Full-window (in-sample) net PnL of each of the 54 combos, summed across BTC/ETH/SOL (each starts 10k).

- **Positive combos: 47/54 (87%).** Distribution: min −759, median +2019, mean +2231, max +8064.
- Base (bb20/sqz.20/vm1.2/atr2) ranks **7/54, PF 1.37** — comfortably inside the plateau.
- The only losers are the **tightest squeeze (sqz_pct 0.10)**, which starves the strategy of trades.

| rank | bb | sqz | vol | atr | net PnL(3sym) | PF | #tr |
|-----:|---:|----:|----:|----:|--------------:|---:|----:|
| 1 | 14 | .30 | 1.5 | 2.0 | +8064 | 1.41 | 123 |
| 6 | 20 | .20 | 1.5 | 2.0 | +5166 | 1.40 | 89 |
| 7 (base) | 20 | .20 | 1.2 | 2.0 | +5090 | 1.37 | 96 |
| 53 | 14 | .10 | 1.2 | 2.0 | −569 | 0.96 | 96 |
| 54 | 20 | .10 | 1.5 | 3.0 | −759 | 0.92 | 68 |

**Read honestly:** this is a broad plateau, but it is a plateau *over the favorable full window*.
Section 1 shows the same params are negative in the trailing fold and lose OOS under blind
optimization. A wide in-sample plateau that does not survive walk-forward is **robust curve-fitting,
not a robust edge**. It rules out "we got lucky on one knob"; it does **not** establish a live edge.

---

## 3) "Long-only" justification — is dropping shorts defensible?

Full-window, base params. If long-only were structural ("shorts structurally lose in crypto"),
short-only should lose everywhere and long+short should always be worse than long-only.

| symbol | long+short ret%(PF) | **long-only ret%(PF)** | short-only ret%(PF) | B&H% | long-only helps? |
|--------|--------------------:|-----------------------:|--------------------:|-----:|:----------------:|
| BTC  | −20.5 (0.79) | **+16.5 (1.35)** | −31.8 (0.38) | +1  | YES (decisive) |
| BNB  | −29.7 (0.57) | **−1.8 (0.95)** | −28.4 (0.29) | +1  | YES |
| ETH  | +1.7 (1.02) | **+6.3 (1.11)** | −2.5 (0.96) | −47 | mild |
| SOL  | +56.4 (1.83) | **+28.1 (1.80)** | +22.1 (1.80) | −51 | **NO — worse** |
| DOGE | +49.3 (1.60) | **+18.1 (1.74)** | +28.4 (1.58) | −39 | **NO — worse** |
| ADA  | +21.6 (1.35) | **+15.0 (1.52)** | +6.8 (1.22) | −61 | **NO — worse** |
| AVAX | +36.9 (1.49) | **+6.7 (1.16)** | +28.4 (2.01) | −75 | **NO — worse** |
| XRP  | +16.2 (1.19) | **−17.6 (0.52)** | +41.1 (1.82) | +103| **NO — inverted** |

- Dropping shorts is decisive **only for BTC** (and helps BNB/ETH). On **SOL, DOGE, ADA, AVAX, XRP
  the long+short version beats long-only**, and **short-only is net-positive on 5 of 8 symbols**
  (XRP +41, AVAX +28, DOGE +28, SOL +22, ADA +7). "Shorts are the poison" was a **BTC-specific
  artifact** of the prior 3-symbol sample, not a structural property.
- **Not a beta capture either** — it does not simply ride a bull market. Long-only is net-positive on
  SOL/ETH/ADA/AVAX whose buy-and-hold over this window was −47 to −75%, and it *loses* on XRP whose
  B&H was +103%. So the return is not "long crypto in an uptrend"; it is signal-specific, which cuts
  both ways: it removes the beta excuse but also removes the "secular uptrend ⇒ long-only" defense.
- **Conclusion: long-only is NOT defensible as a general prior.** It was chosen post-hoc because it
  rescued BTC. On the broader basket the profitable side is symbol-dependent, and forcing long-only
  actively *degrades* 5 of 8 symbols. This is exactly the post-hoc curve-fit the brief warned about.

---

## 4) Generalization — 8-symbol basket (full window, long-only, base params)

| symbol | ret% | PF | win% | #tr | MDD% | B&H% |
|--------|-----:|---:|-----:|----:|-----:|-----:|
| BTC  | +16.5 | 1.35 | 33.3 | 42 | 7.0 | +1 |
| ETH  | +6.3  | 1.11 | 33.3 | 33 | 19.8 | −47 |
| SOL  | +28.1 | 1.80 | 47.6 | 21 | 14.1 | −51 |
| BNB  | −1.8  | 0.95 | 28.1 | 32 | 17.3 | +1 |
| XRP  | −17.6 | 0.52 | 26.1 | 23 | 21.5 | +103 |
| DOGE | +18.1 | 1.74 | 41.7 | 12 | 8.1 | −39 |
| ADA  | +15.0 | 1.52 | 37.5 | 16 | 16.4 | −61 |
| AVAX | +6.7  | 1.16 | 31.6 | 19 | 18.6 | −75 |

**Basket: 6/8 net-positive, pooled PF 1.23.** On its own this looks tolerable — but it is the *same
favorable full window* that folds/WF already showed to be front-loaded. XRP (PF 0.52) is an outright
failure and BNB is flat, and every symbol's edge lives in folds 1–3. The basket does not rescue the
candidate; it inherits the same regime dependence.

---

## Reasoning for REJECT

| Test | Bar | Result | Pass? |
|------|-----|--------|:-----:|
| Sequential folds | edge persists across time | fold4 negative on **8/8** symbols | ✗ |
| Anchored walk-forward (optimize→OOS) | pooled OOS PF ≥ 1.3, consistent | **PF 1.09**, 2/3 core symbols lose OOS, carried by SOL | ✗ |
| Param robustness | broad plateau | 47/54 positive — but **in-sample only** | ~ |
| Long-only defensible | structural, not post-hoc | rescues BTC only; **degrades 5/8**, shorts profitable on 5/8 | ✗ |
| Multi-symbol | holds on broader basket | 6/8 full-window, but same front-loaded regime | ~ |

- The one decisive test for real money — **blind walk-forward** — fails: the honest OOS PF is 1.09,
  below the 1.3 threshold, and only SOL survives. BTC (the flagship) and ETH both lose out of sample.
- The **most recent 6 months are negative on every symbol tested**, so even if a promotion were made,
  it would be into a decaying regime.
- The result that earned the prior HOLD depended on a **long-only choice that is not structurally
  justified** — it is a BTC-specific fit; shorts are the profitable side on the majority of alts, and
  long-only *hurts* SOL/DOGE/ADA/AVAX/XRP. Remove that post-hoc choice and the base (long+short) is
  net-negative on BTC/BNB and mediocre elsewhere.
- The in-sample parameter plateau is genuine but only proves the fit is *smooth*, not *durable*.

**This does not clear the bar for touching real money.** If revisited later, the honest framing is a
**long+short** squeeze-breakout system (the short side is not poison outside BTC) re-validated on a
fresh forward window — not the long-only 4h cut, which is overfit to BTC in a now-expired regime.
Recommend **dropping it from the swing-sleeve promotion pipeline**; at most, keep the *long+short*
idea on the research backlog for a from-scratch OOS build.
