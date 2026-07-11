# Backtest — Golden/Dead cross 50/200 + gap≥1.2% + ADX>20 + volume (swing)

- **Spec**: `research/strategies/golden-cross-regime-adx-daily.md`
- **Implementation**: `research/impl/swing_strategies.py` → `GoldenCrossRegimeStrategy`
- **Runner / engine**: `research/impl/swing_runner.py` (`golden`, `sens_golden`)
- **Verdict**: **HOLD (inconclusive) — leaning FAIL.** Sample is far too small to validate
  (1d: 0–1 trades/symbol; 4h: 4–5 trades/symbol). What edge exists is entirely front-loaded
  (every 2nd-half is negative) and does not survive cross-symbol (SOL loses on every cut). Not a
  passing candidate as specced.

## Method / reproducibility

- **Custom replay engine** (not `SleeveBacktester`) because the framework hardcodes
  `SIGNAL_WINDOW=200`, one bar too short to detect a 50/200 SMA cross (needs two consecutive
  SMA200 values ⇒ 201 bars). The engine **mirrors the framework's mid-path economics exactly**:
  taker fee 0.05%/side, adverse slippage 0.02% (≈0.14% round-trip), intra-bar SL/TP with **stop
  priority**, strategy `CLOSE` at bar close, final position liquidated at last close. Indicators and
  `RiskManager` are reused read-only — **no production code modified.**
- **Entry (long-only base)**: the 50/200 spread `gap=(SMA50−SMA200)/SMA200` freshly rises through
  `+gap_min` (=1.2%). *Note:* at the raw cross bar the gap is ~0, so the spec's 1.2% filter is a
  **separation-confirmation** event, not the touch bar. Gates at that bar: **ADX(14) ≥ 20** and
  **volume** (mean of last 3 bars ≥ 1.2× mean(prior 20) — a sustained pickup, since a single-bar
  spike rarely coincides with the exact confirmation bar and would drop genuine crosses).
- **Exit**: opposite regime (spread flips sign / dead cross) **or** close < SMA200; catastrophic
  hard stop −10% (intra-bar).
- **Sizing**: **full allocation** — each entry = 100% equity notional, 1×, no leverage (natural
  benchmark for a fully-invested swing position; makes ret%/MDD comparable to buy&hold). A **risk-1%**
  cross-check is also reported; PF/win% are ~sizing-invariant so the edge conclusion is identical.
- **Data**: `data-api.binance.vision` spot mirror. **1d ~1100 d (~3 yr; ~2023-07→2026-07)**,
  **4h ~760 d (~2 yr; ~2024-06→2026-07)**. 200-bar SMA warmup consumes the first ~year, so the
  *usable* daily signal window is effectively ~2024→2026 — which contains very few cross events (as
  the spec itself warns: "초저빈도, 연 0~2회").
- Commands: `python research/impl/swing_runner.py golden` · `python research/impl/swing_runner.py sens_golden`

## Results — full allocation (1×)

| period/symbol       |  ret%  |   PF  | win% | #tr | MDD% | fees(%eq) |
|---------------------|-------:|------:|-----:|----:|-----:|----------:|
| **1d ~3yr** |||||||
| BTC full            | +11.45 |   inf | 100.0 |  1 |  0.0 | 0.1 |
| ETH full            | −10.13 |  0.00 |   0.0 |  1 | 10.1 | 0.1 |
| SOL full            |  +0.00 |    —  |   0.0 |  0 |  0.0 | 0.0 |
| **4h ~2yr** |||||||
| BTC full            |  +4.81 |  1.45 |  25.0 |  4 |  5.6 | 0.4 |
| BTC 1st half        |  +9.92 |  2.77 |  50.0 |  2 |  5.6 | 0.2 |
| BTC 2nd half        |  −4.64 |  0.00 |   0.0 |  2 |  4.6 | 0.2 |
| ETH full            | +68.02 |  2.91 |  40.0 |  5 | 11.5 | 0.8 |
| ETH 1st half        | +22.88 |  2.65 |  50.0 |  2 | 10.1 | 0.2 |
| ETH 2nd half        | −11.47 |  0.00 |   0.0 |  2 | 11.5 | 0.2 |
| SOL full            | −27.37 |  0.00 |   0.0 |  4 | 27.4 | 0.3 |
| SOL 1st half        | −10.13 |  0.00 |   0.0 |  1 | 10.1 | 0.1 |
| SOL 2nd half        | −19.18 |  0.00 |   0.0 |  3 | 19.2 | 0.3 |

Risk-1% sizing gives identical signs/PF at ~1/10 the magnitude (e.g. ETH 4h +7.7%, SOL 4h −2.7%) —
confirms the pattern is not a sizing artifact.

## Sensitivity (BTC/USDT full)

| variant                 | 1d ret% (#tr) | 4h ret% / PF (#tr) |
|-------------------------|--------------:|-------------------:|
| base gap1.2 adx20 vol1.2| +11.45 (1)    | +4.81 / 1.45 (4)   |
| gap 0.8%                | +10.85 (1)    | −8.88 / 0.14 (4)   |
| gap 2.0%                |  0.00 (0)     | −6.74 / 0.65 (5)   |
| adx_min 25              |  0.00 (0)     | −9.18 / 0.00 (2)   |
| vol_mult 1.0            | +11.45 (1)    | +15.43 / 1.94 (7)  |
| no-vol / no-adx (gap only)| +0.16 (2)   | +31.65 / 1.68 (13) |
| with dead-cross short   | +44.70 (2)    | +15.85 / 2.10 (7)  |

- The **specced filter thresholds are not robust**: loosening volume (1.0×) or dropping the vol/ADX
  gates entirely *improves* BTC 4h (gap-only: +31.6%, 13 trades, the only config with a double-digit
  sample). The 1.2×/ADX20 thresholds are on the wrong side of noise here.
- Adding the optional **dead-cross short** helps BTC in this window, but the scout flagged crypto
  short-squeeze risk and the sample is 7 trades — not evidence.

## Verdict — HOLD (inconclusive), leaning FAIL

- **Sample far below the bar for significance.** On 1d the usable post-warmup window holds essentially
  0–1 qualifying cross events per symbol; on 4h it is 4–5. The role guidance ("표본 <20 → 보류") applies
  directly. The eye-catching ETH 4h +68% is **5 trades**, front-loaded.
- **No cross-symbol consistency, no out-of-sample survival.** BTC/ETH are positive only via their
  1st halves; **every 2nd half is negative**, and **SOL loses on every cut** (full/1st/2nd). This is
  the textbook regime-dependent / front-loaded signature, not a durable edge.
- **The concept isn't refuted, it's under-powered.** Golden-cross regime is real but fires too rarely
  to validate standalone on 2–3 yr of data, and the specific gap/ADX/vol thresholds don't help (they
  hurt on the only symbol with a workable sample). 
- **Where it belongs**: as a **higher-TF regime *filter*** on an existing sleeve (e.g. "golden regime
  ⇒ longs only") — its natural role per the scout memo — **not** a standalone entry engine. Cannot be
  passed on this evidence.
