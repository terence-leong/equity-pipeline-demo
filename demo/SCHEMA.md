# Company Scoring Engine — Public I/O Schema & Module Map

> ⚠️ **PUBLIC DEMO SCHEMA.** This documents the input/output structure used by the demo artifacts in this repo ([`DEMO-A_scorecard.md`](DEMO-A_scorecard.md), [`DEMO-A_report.md`](DEMO-A_report.md)). It mirrors the *structure* of the production schema; the production schema is a **superset** containing additional private columns (see §7). All example values are placeholders. **Weights, thresholds, score-to-state mappings, and gate-trigger logic are private** and appear only as `[private]`.

## Pipeline shape

```
INPUTS (provenance-tagged)
   → 8 SCORING MODULES (sub-scores 0–10)
        → TOTAL_SCORE (0–100; module→total mapping private)
   → NON-TOTAL LAYERS (momentum · headroom · reward/risk · tape gate)
   → FINAL STATE BLOCK (machine-parseable verdict)
```

Two design rules govern everything downstream: every input carries exactly one provenance tag, and a missing driver propagates as MISSING instead of being estimated.

## 1. Input schema

| Field | Type / unit | Allowed status | Provenance rule |
|---|---|---|---|
| `AS_OF` | ISO date | required | run timestamp or USER_PROVIDED_OVERRIDE |
| `LISTING` | text | required | fixes listing / currency basis for all ratios |
| `PRICE` | number, listing currency | OK / MISSING / WEIRD | DIRECT_FROM_SOURCE only |
| `REVENUE_TTM` | number, reporting currency (millions) | OK / MISSING / WEIRD | DIRECT_FROM_SOURCE |
| `GROSS_PROFIT_TTM` | number (millions) | OK / MISSING / WEIRD | DIRECT_FROM_SOURCE |
| `GROSS_MARGIN` | percent | OK / MISSING | COMPUTED_FROM_SOURCE (formula shown inline) |
| `SHARES_OUT` | number (millions) | OK / MISSING | DIRECT_FROM_SOURCE or USER_PROVIDED_OVERRIDE |
| `NET_DEBT` | number (millions) | OK / MISSING | DIRECT_FROM_SOURCE |
| `EV` | number (millions) | OK / MISSING | COMPUTED; **blocked** if any driver MISSING |
| `EV_SALES` | ratio | OK / MISSING | COMPUTED; **blocked** if `EV` MISSING |

Input-layer rules:
- **One tag per value** — `DIRECT_FROM_SOURCE`, `COMPUTED_FROM_SOURCE: <formula>`, `USER_PROVIDED_OVERRIDE`, or `MISSING — NOT VERIFIED`. Untagged numbers are invalid.
- **Dependency closure** — a derived ratio may not print OK unless its drivers are OK; see the `NET_DEBT → EV → EV_SALES` chain in the scorecard for MISSING propagating honestly.
- **Basis alignment** — ratios compute only when listing/currency basis is provable; otherwise status `WEIRD` and no computation.

## 2. Module map (Layer 2 core)

Eight modules, each emitting a sub-score 0–10 (or `FLAGGED`). Module→total weighting is `[private]`.

| # | Module | Question it answers | Primary consumes | Emits |
|---|---|---|---|---|
| 1 | Why-Now / catalyst timing | Why does this re-rate now? | catalysts, guidance, tape context | 0–10 |
| 2 | Bottleneck / moat | Is the position defensible? | competitive set, switching friction | 0–10 + moat class |
| 3 | Survival / balance-sheet durability | Can it self-fund through a downturn? | cash, debt, FCF | 0–10 |
| 4 | Financing / dilution risk | Who pays for growth? | SBC, share-count trend | 0–10 |
| 5 | Growth trajectory | Is the top line compounding? | revenue trend, margin trend | 0–10 |
| 6 | Tradability / liquidity | Can size move in and out? | volume, spread | 0–10 |
| 7 | Consensus / positioning | What does the crowd already believe? | coverage, positioning proxies | 0–10 |
| 8 | Valuation | Is the price defensible? | multiple bands vs peers/history | 0–10 **or `FLAGGED`** |

Module rules:
- A module whose core driver is MISSING emits **`FLAGGED`**, never a guessed score (scorecard: Valuation `FLAGGED` because `EV_SALES` was MISSING).
- Moat class vocabulary: `WIDE / NARROW / NONE` (assignment criteria `[private]`).

## 3. Non-total layers

Computed independently of TOTAL; always emitted, never silently dropped.

| Field | Scale | Meaning | Notes |
|---|---|---|---|
| `MOMENTUM_SCORE` | 0–100 | trend pressure | distinct scale from module sub-scores |
| `HEADROOM_SCORE` | 0–100 | room before structural resistance | |
| `RR_RATIO` | ratio (e.g. `2.1:1`) | price-structure asymmetry | prints with authority label (see §6, queued fix) |
| `ENGINE_TAPE_GATE` | enum | timing veto | illustrative values: `CLEAR / WAIT_FOR_RESET / NO_TRADE` — production enum `[private]` |

The gate outranks the total: a passable TOTAL with `WAIT_FOR_RESET` still resolves to `Watch` (see scorecard §4).

## 4. Final state block (canonical output)

Key spelling and order are locked; drift is a hard stop (see [`llm-reliability-patterns`](https://github.com/terence-leong/llm-reliability-patterns), pattern 05).

```
BEGIN_SCORECARD
TICKER=<text>
AS_OF=<ISO date>
TOTAL_SCORE=<0-100>/100
MOMENTUM_SCORE=<0-100>/100
HEADROOM_SCORE=<0-100>/100
RR_RATIO=<x.y:1 | MISSING>
ENGINE_TAPE_GATE=<enum>
VALUATION_MODULE=<0-10 | FLAGGED (reason)>
FINAL_STATE=<Asymmetry | Starter | Watch | Avoid>
FINAL_STATE_REASON=<one line>
SYNTHETIC=<TRUE for demo runs>
END_SCORECARD
```

`FINAL_STATE` is a fixed four-word vocabulary — `Asymmetry / Starter / Watch / Avoid` — mapped from scores, layers, and gates by rules that are `[private]`.

## 5. Status & provenance vocabulary

| Token | Meaning |
|---|---|
| `OK` | verified and usable downstream |
| `MISSING` | not verified this run; blocks dependents |
| `WEIRD` | retrieved but fails a sanity/basis check; unusable |
| `PARTIAL` | some required lookback/coverage retrieved, not all |
| `FLAGGED` | module-level: core driver missing, score withheld |

Provenance tags are listed in §1 and documented generically in [`llm-reliability-patterns`](https://github.com/terence-leong/llm-reliability-patterns), pattern 02.

## 6. Propagation rules (public-safe)

1. MISSING driver → every dependent value MISSING (never estimated).
2. Module missing a core driver → `FLAGGED`, excluded from confident scoring.
3. Gate verdicts outrank the total in final-state resolution.
4. Non-total layers are always computed and emitted — a layer silently absent is a run failure, not a blank.
5. Queued hardening (from the demo report §13): totals print with a `FULL / PARTIAL(n dark)` quality companion; momentum and RR print authority labels.

## 7. What the production schema adds (private)

The production output is a superset of this document. Additional column families, named at category level only: theme-taxonomy fields, conviction/sizing tiers, gate internals and trigger telemetry, execution-history lookback columns, and all weights/thresholds. None of those columns, names, or values appear in this repo.
