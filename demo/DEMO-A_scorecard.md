# DEMO-A — Company Scoring Engine — Sample Scorecard

> ⚠️ **SYNTHETIC ILLUSTRATION.** `DEMO-A` is a fake ticker. Every value on this page is a placeholder invented to show the *output format* of the Company Scoring Engine (Layer 2). Nothing here is a live run, market data, or a real call. No sources were opened to produce it.
>
> The provenance tags (`DIRECT_FROM_SOURCE`, `COMPUTED_FROM_SOURCE`, `USER_PROVIDED_OVERRIDE`, `MISSING`) show what a real run's tags look like in place. Scoring **weights, thresholds, theme codes, lane tables, and gate-trigger logic are private** and do not appear here.

## What this file demonstrates

- Every input carries a provenance tag, so an auditor can trace each number to its origin or see it marked missing.
- A MISSING input **propagates** instead of being silently filled.
- The module map rolls into separately-computed non-total layers and a single final state.
- The final state is drawn from a fixed four-word vocabulary: **Asymmetry / Starter / Watch / Avoid**.

## Section 1 — Inputs (provenance layer)

All values synthetic; tags illustrate a live run's format.

```
FIELD               VALUE        PROVENANCE
AS_OF               2026-06-30   USER_PROVIDED_OVERRIDE
LISTING             DEMO-A / primary
PRICE               18.40        DIRECT_FROM_SOURCE
REVENUE_TTM         1,240        DIRECT_FROM_SOURCE
GROSS_PROFIT_TTM    546          DIRECT_FROM_SOURCE
GROSS_MARGIN        44.0%        COMPUTED_FROM_SOURCE (546 / 1,240)
SHARES_OUT          210          USER_PROVIDED_OVERRIDE
NET_DEBT            MISSING      MISSING — NOT VERIFIED
EV                  MISSING      MISSING — NOT VERIFIED (depends on NET_DEBT)
EV_SALES           MISSING      MISSING — NOT VERIFIED (depends on EV)
```

The last three lines are the discipline in action: `NET_DEBT` was never verified, so `EV` and `EV/Sales` inherit MISSING rather than being estimated. A derived ratio may not print as OK while a driver is missing.

## Section 2 — Module map (sub-scores)

Sub-scores 0–10, synthetic. Weighting is private.

```
MODULE                                SUB-SCORE   NOTE
Why-Now / catalyst timing             7           demo
Bottleneck / moat                     8           demo
Survival / balance-sheet durability   6           demo
Financing / dilution risk             5           demo
Growth trajectory                     8           demo
Tradability / liquidity               7           demo
Consensus / positioning               6           demo
Valuation                             FLAGGED     valuation inputs incomplete (EV/Sales MISSING)
```

```
TOTAL_SCORE        63 / 100   [DEMO_PLACEHOLDER]
SCORING_LANE       [private]
MODULE_WEIGHTING   [private]
```

`TOTAL_SCORE` is an illustrative placeholder — **not** computed from the sub-scores above; the sub-score→total mapping is private. The Valuation module is FLAGGED, not scored, because a required input is MISSING. The engine does not guess past a missing driver.

## Section 3 — Non-total layers

Computed separately from TOTAL; synthetic values.

```
MOMENTUM_SCORE     58 / 100   [DEMO_PLACEHOLDER]
HEADROOM_SCORE     41 / 100   [DEMO_PLACEHOLDER]
RR_RATIO           2.1 : 1    [DEMO_PLACEHOLDER]
ENGINE_TAPE_GATE   WAIT_FOR_RESET
```

Momentum and Headroom are always on a 0–100 scale, distinct from the 0–10 module sub-scores. RR is always computed and never silently dropped. The tape gate can override the total — see Section 4.

## Section 4 — Final state block

```
BEGIN_SCORECARD
TICKER=DEMO-A
AS_OF=2026-06-30
TOTAL_SCORE=63/100 [DEMO_PLACEHOLDER]
MOMENTUM_SCORE=58/100 [DEMO_PLACEHOLDER]
HEADROOM_SCORE=41/100 [DEMO_PLACEHOLDER]
RR_RATIO=2.1:1 [DEMO_PLACEHOLDER]
ENGINE_TAPE_GATE=WAIT_FOR_RESET
VALUATION_MODULE=FLAGGED (EV/Sales MISSING)
FINAL_STATE=Watch
FINAL_STATE_REASON=tape gate WAIT_FOR_RESET overrides total
SYNTHETIC=TRUE — placeholder demo, not a live run
END_SCORECARD
```

The total alone might read as a Starter, but `ENGINE_TAPE_GATE=WAIT_FOR_RESET` forces `FINAL_STATE=Watch`. The gate's trigger conditions are private; what's public is that a gate exists and can veto the score.

## How to read this

- **Public here:** the output schema, the module map, the provenance discipline, the non-total layers, the final-state vocabulary.
- **Private, deliberately absent:** weights, thresholds, theme codes, lane tables, gate-trigger logic.
- Every number is synthetic. A real run replaces each placeholder with a source-echoed value carrying a real provenance tag, or an explicit MISSING.
