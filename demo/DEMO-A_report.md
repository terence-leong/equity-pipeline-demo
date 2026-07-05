# DEMO-A — Company Scoring Engine — Sample Narrative Report

> ⚠️ **SYNTHETIC ILLUSTRATION.** `DEMO-A` is a fictional company. Every number in this document is a placeholder invented to show the *report format* the Company Scoring Engine emits alongside its scorecard. This is the companion narrative to [`demo/DEMO-A_scorecard.md`](DEMO-A_scorecard.md) — same fake run, same values. Scoring **weights, thresholds, score deltas, sizing tiers, and gate-trigger logic are private** and appear here only as `[private]`. Nothing on this page is a live run, market data, or a call.

**ticker:** DEMO-A (fictional)
**what do they do:** Fictional designer of power-management components for industrial automation equipment.

## 1. Bottom line — how's the setup?

A solid mid-tier operator blocked at the door by its own tape gate.

```
Total score (fundamental):   63 / 100   [DEMO_PLACEHOLDER]
Momentum score:              58 / 100   [DEMO_PLACEHOLDER]
Headroom score:              41 / 100   [DEMO_PLACEHOLDER]
Reward/risk:                 2.1 : 1    [DEMO_PLACEHOLDER]
Leadership edge (overlay):   6.5 / 10   [DEMO_PLACEHOLDER] | delta applied: [private]
Dilution / SBC:              SBC ≈ 38% of trailing net income; share count +4.2%/yr [DEMO_PLACEHOLDER]
Moat:                        NARROW     [DEMO_PLACEHOLDER]
Tape gate:                   WAIT_FOR_RESET
Final state:                 Watch
```

The engine drafted a provisional high-conviction layout of 8% [DEMO_PLACEHOLDER], then compressed actionable size to zero: the tape gate reads WAIT_FOR_RESET and a core valuation driver is unverified. The fundamental score is respectable; the entry is not available. That divergence — good house, closed door — is exactly what the layered design is supposed to surface.

## 2. Bull case

Steady share gains in a niche where qualification cycles run long and switching is expensive. Revenue growth in the mid-teens [DEMO_PLACEHOLDER] with gross margin at 44.0% [DEMO_PLACEHOLDER], self-funded operations, and a customer base that re-orders on multi-year design cycles. If the consolidation phase resolves upward, the growth and tradability sub-scores (8 and 7) suggest the setup re-opens quickly.

## 3. Bear case

Dilution is the structural leak: stock-based compensation consuming roughly 38% of trailing net income [DEMO_PLACEHOLDER] and a share count compounding at +4.2%/yr [DEMO_PLACEHOLDER] tax every thesis. Three larger diversified incumbents (unnamed, fictional) can bundle adjacent product lines. And the valuation module is dark — net debt was never verified, so the EV chain is uncomputable and the engine literally cannot say whether the price is defensible.

## 4. Reward/risk view

RR prints 2.1 : 1 [DEMO_PLACEHOLDER], computed from price-structure bands independent of the valuation chain. It clears the actionability bar [threshold private] on its face — but headroom at 41 says the upside band is short, and the RR figure was produced while one module was dark. A ratio that clean deserves a companion authority label; this run didn't attach one. See §10.

## 5. Leadership view

Founder-led since inception [DEMO_PLACEHOLDER], stable product roadmap, no unexplained executive turnover in the lookback window. The overlay applied its delta [private] on continuity evidence alone: direct equity holdings and compensation tables were not parsed in this run, so alignment is asserted from ownership continuity, not verified skin-in-the-game. Score stands at 6.5 [DEMO_PLACEHOLDER] with that caveat attached.

## 6. Opportunity edge view

The niche is real: power-management content per automation cell is rising [DEMO_PLACEHOLDER trend], and DEMO-A's parts sit at a genuine integration chokepoint. The edge module applied its boost [private] but the valuation cap kept theme enthusiasm from overrunning a structurally narrow-moat merchant supplier — the cap doing its job.

## 7. Execution capability view

Only two of four lookback quarters were retrievable in this run [DEMO_PLACEHOLDER], so the module printed PARTIAL and granted **zero** delta. Guidance-only claims received no credit. Freezing the adjustment rather than extrapolating from half a record is correct behavior; the missing quarters are a data-pack failure, not a scoring one.

## 8. Moat + competitive landscape view

Moat class NARROW [DEMO_PLACEHOLDER]. Qualification lock-in and design-cycle friction are genuine but pricing power is contested, and the dilution leak partially converts moat economics into employee compensation rather than shareholder return. Competitive threat marked elevated: the unnamed incumbents have distribution scale DEMO-A cannot match.

## 9. My honest view

I agree with the machine's restraint. A 63 total with an 8-and-7 core is a name worth tracking, but you do not open a position through a WAIT_FOR_RESET gate with the valuation chain dark. Watchlist it; re-run when net debt is verified and the tape resets. The most useful thing this run produced is not the score — it's the two flaws it exposed in its own process (§10).

## 10. What looks wrong or fragile in this run (self-audit)

- **Dark module, clean total.** NET_DEBT=MISSING blacked out the EV chain and the Valuation module printed FLAGGED — yet TOTAL_SCORE=63 printed with no companion quality tag saying one module was dark. A reader of the scorecard alone could miss it.
- **Sizing ran before the gate.** The provisional 8% layout [DEMO_PLACEHOLDER] was drafted *before* the missing-driver check executed. The cap caught it downstream, but order-of-operations meant an uninformed size existed at all.
- **Non-total layers printed without authority labels.** Momentum (58) and RR (2.1:1) used inputs of uneven completeness and printed bare, with no LOW/FULL authority marker.

## 11. What the engine got right

- **MISSING propagated.** No silent estimate for net debt; the EV chain went dark honestly instead of plausibly.
- **The gate outranked the score.** Watch despite a passable 63 — timing authority beat fundamental enthusiasm.
- **Dilution was priced, not narrated.** The SBC leak landed in the Financing sub-score (5) instead of living only in prose.

## 12. What the engine got wrong

- Provisional sizing computed ahead of the data-completeness gate (caught late, should never exist).
- Total printed without a quality companion while a module was FLAGGED.
- Momentum/RR printed without authority tags.

## 13. Needle-moving fixes queued (thresholds and deltas private)

1. **Missing-driver abort:** any MISSING core valuation driver caps provisional size at the starter tier [tier value private] *before* any cap audit runs.
2. **TOTAL_QUALITY companion tag:** every total prints with FULL or PARTIAL(n modules dark) beside it.
3. **Authority labels on non-total layers:** momentum and RR must print FULL/LOW authority based on input completeness [criteria private].

## Appendix — final state block (matches the scorecard)

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
