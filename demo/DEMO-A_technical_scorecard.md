# DEMO-A — Entry Quality Engine — Sample Technical Scorecard

> ⚠️ **SYNTHETIC ILLUSTRATION.** `DEMO-A` is a fictional ticker. Every value on this page is a placeholder. This is the Layer-3 (Entry Quality Engine) companion to the Layer-2 artifacts — [`DEMO-A_scorecard.md`](DEMO-A_scorecard.md) and [`DEMO-A_report.md`](DEMO-A_report.md) — showing the engine-eye view that produced the `WAIT_FOR_RESET` gate in that same fake run. Production **scoring bands, component weights, structure-phase logic, and gate-trigger thresholds are private** and appear only as `[private]`.

## What this file demonstrates

- Timing is scored in a layer separate from fundamentals — and the gate can veto a passable fundamental score.
- Reward/risk comes from price-structure bands, shown with its arithmetic.
- A missing tape input degrades data quality **honestly** instead of being back-filled from memory.

## 1. Tape inputs (provenance layer)

All values synthetic; tags show a live run's format.

```
FIELD            VALUE          PROVENANCE
AS_OF            2026-06-30     USER_PROVIDED_OVERRIDE
PRICE            18.40          DIRECT_FROM_SOURCE
MA50D            17.92          DIRECT_FROM_SOURCE   [DEMO_PLACEHOLDER]
MA200D           16.10          DIRECT_FROM_SOURCE   [DEMO_PLACEHOLDER]
MA20D            MISSING        MISSING — NOT VERIFIED (not published by source)
VOL_20D_AVG      1.8M sh        DIRECT_FROM_SOURCE   [DEMO_PLACEHOLDER]
VOL_TREND        contracting    COMPUTED_FROM_SOURCE [DEMO_PLACEHOLDER]
HIGH_52W         21.00          DIRECT_FROM_SOURCE   [DEMO_PLACEHOLDER]
DATA_QUALITY     PARTIAL        (MA20D missing)
```

The MISSING line is deliberate: short moving averages are genuinely absent from some data sources, and the honest handling is a `DATA_QUALITY=PARTIAL` downgrade — never a value recalled "from memory."

## 2. Structure read (phase vocabulary illustrative)

- **Phase:** consolidation following an advance — price above MA50D and MA200D [placeholders], below the overhead supply band.
- **Support band:** 17.20–17.90 (prior breakout shelf + MA50D confluence) [placeholders]
- **Resistance band:** 19.80–21.00 (prior congestion + 52-week high) [placeholders]

## 3. Component read (0–100 each; aggregation weights private)

| Component | Score [all DEMO_PLACEHOLDER] |
|---|---|
| Trend alignment | 72 |
| Structure quality | 61 |
| Volume behavior | 44 |
| Volatility posture | 55 |
| Relative strength | 51 |

→ `MOMENTUM_SCORE=58/100` (matches the Layer-2 block), authority **LOW** because `DATA_QUALITY=PARTIAL`. Aggregation is weighted `[private]` — a simple average of these placeholders will not reproduce the printed score, by design.

→ `HEADROOM_SCORE=41/100`: the overhead band sits close above; the upside runway before structural resistance is short.

## 4. Reward/risk (price-structure bands)

```
ENTRY_REF    18.40
STOP_REF     17.20   (below support band)
TARGET_REF   20.92   (measured objective inside overhead band)
RISK         18.40 − 17.20 = 1.20
REWARD       20.92 − 18.40 = 2.52
RR_RATIO     2.52 / 1.20 = 2.1 : 1   [COMPUTED_FROM_SOURCE — placeholder inputs]
```

The 2.1:1 in the Layer-2 final block is this computation.

## 5. Gate resolution

Gate states (illustrative enum): `CLEAR / WAIT_FOR_RESET / NO_TRADE` — production enum and trigger thresholds `[private]`.

```
ENGINE_TAPE_GATE=WAIT_FOR_RESET
GATE_REASON=price below overhead supply on contracting volume; DATA_QUALITY=PARTIAL
RE-OPEN (illustrative): reclaim resistance band on expanding volume, OR retreat into support band with stabilization
```

Two rules demonstrated (both illustrative; production criteria private): the gate does not print `CLEAR` while `DATA_QUALITY=PARTIAL`, and in production this layer additionally requires an independent human chart-reader's score as a required input before the gate can clear.

## 6. Handoff to final state

Layer 3 emits momentum, headroom, RR, and the gate. Layer 2's published resolution: `FINAL_STATE=Watch`, reason "tape gate WAIT_FOR_RESET overrides total." Timing authority outranked a passable fundamental 63 — the separation working as designed.

## Appendix — layer output block

```
BEGIN_TECH_SCORECARD
TICKER=DEMO-A
AS_OF=2026-06-30
MOMENTUM_SCORE=58/100 [DEMO_PLACEHOLDER]
MOMENTUM_AUTHORITY=LOW (DATA_QUALITY=PARTIAL)
HEADROOM_SCORE=41/100 [DEMO_PLACEHOLDER]
RR_RATIO=2.1:1 [DEMO_PLACEHOLDER]
ENGINE_TAPE_GATE=WAIT_FOR_RESET
DATA_QUALITY=PARTIAL (MA20D MISSING)
SYNTHETIC=TRUE — placeholder demo, not a live run
END_TECH_SCORECARD
```

Note the coherence detail: `MOMENTUM_AUTHORITY` exists at this layer but did not surface in the Layer-2 final block — exactly the gap the demo report's self-audit flagged (§10) and queued for fix (§13).
