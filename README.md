# Equity Research Pipeline — Public Demo

A working, sanitized demonstration of an LLM-native systematic equity research stack. **Architecture, schemas, and audit discipline are fully visible here. Production weights, prompts, theme taxonomy, and thresholds are private.**

Philosophy: inspired by classic macro-trading discipline — three questions in sequence: **what** to buy (theme + company quality), **when** to buy (entry quality), and **how much** risk to carry (macro regime).

## The four layers

| Layer | Public name | Question answered | What's in this repo |
|---|---|---|---|
| 1 | Theme Rotation Engine | Where is capital rotating? | Schema + demo run on a historical theme |
| 2 | Company Scoring Engine | Is this the best house on the street? | Full I/O schema, module map, demo scorecard on fake ticker `DEMO-A` |
| 3 | Entry Quality Engine | Is the entry safe *now*? | Demo technical scorecard |
| 4 | Macro Risk Overlay | Aggressive or defensive? | Sample dashboard outputs |

## Demo run

Every value in this demo is either from a public historical example or a placeholder. The output schema is real; the numbers are not live. Demo scorecard files will be added under `demo/`.

## The engineering problem: making an LLM honest

The hard part wasn't scoring logic — it was verifiability. Every number must be echoed verbatim from an opened source or labeled MISSING. No training-memory market data. Provenance tags on every value, schema locks, copy-forward baseline integrity, regression diff guards, atomic step execution, self-check gates that halt rather than guess.

Generalized versions of every technique: [`llm-reliability-patterns`](https://github.com/terence-leong/llm-reliability-patterns).

## Reproducibility claim (worded precisely)

Designed for **repeatability and auditability**: locked schemas, verbatim source echoes, validation gates, halt-over-guess protocols. This is not a claim of bitwise LLM determinism — it is a claim that every output value is traceable to an echoed source or explicitly labeled as missing.

## What is deliberately NOT here

**Public:** architecture, schemas, fake/historical examples, audit principles, redacted outputs, delayed case studies.
**Private:** prompts, scoring weights, rubrics, theme taxonomy, ticker universe, live outputs, decision thresholds, gate logic.

## Status

Iterated across **66+ versions** in live daily use across US, HK, China A-share, and Japan markets. This repository is research-process documentation. It is not investment advice, not a performance record, and not an offer of any kind.

Collaboration inquiries: terence@tripcanvas.co


## Run the toy pipeline

A runnable, dependency-free demonstration of the audit shell — receipt echo → provenance tags → MISSING propagation → gates → locked output schema. Synthetic data only; every weight and constant is a labeled fake.

```
python demo/demo_pipeline.py
python -m unittest discover demo -v
```

`demo_pipeline.py` reproduces the published DEMO-A scorecard block **byte-for-byte** from `sample_source.json`, printing the full audit trail (receipt echoes, provenance tags, blocked computations) along the way — and asserts the match itself (`BYTE_MATCH_PUBLISHED_ARTIFACT=True`). `test_demo_pipeline.py` is eleven passing tests, each a documented failure mode: schema drift halts, MISSING propagates instead of being estimated, untagged numbers are rejected, the regression guard trips on out-of-scope changes, and the tape gate cannot clear on partial data. There is deliberately no LLM call here: this is the deterministic enforcement shell that wraps the LLM in production, which is exactly the layer that is safe to publish.

