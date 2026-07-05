#!/usr/bin/env python3
"""
demo_pipeline.py — Runnable toy of an auditable LLM-research pipeline shell.

SYNTHETIC DEMO. Every number here is fake. All weights and constants are
arbitrary demo values, chosen only so this toy reproduces the published
DEMO-A artifacts in this repo byte-for-byte. Production weights, thresholds,
and gate logic are private and different.

Stdlib only. No network. No API key.

Run:   python demo_pipeline.py
Tests: python -m unittest discover demo -v   (from repo root)

What this demonstrates (the enforcement shell around an LLM, minus the LLM):
  1. Receipt-echo gate  — a DIRECT value exists only if its raw source line
                          is echoed into the audit log first.
  2. Provenance tags    — every number carries exactly one origin tag.
  3. MISSING propagation— an unverified driver blocks every dependent value;
                          nothing is silently estimated.
  4. Gates over scores  — the tape gate vetoes a passable fundamental total.
  5. Schema lock        — locked key order/spelling; drift is a hard stop.
  6. Regression guard   — out-of-scope key changes raise, never ship.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

# ----------------------------- errors (the gates) ---------------------------

class UntaggedValueError(Exception):
    """A raw, untagged number tried to enter a computation."""

class SchemaError(Exception):
    """Output schema drifted from the canonical key set/order."""

class RegressionError(Exception):
    """A key outside the declared update set changed."""

# ----------------------------- provenance vocab -----------------------------

DIRECT = "DIRECT_FROM_SOURCE"
COMPUTED = "COMPUTED_FROM_SOURCE"
OVERRIDE = "USER_PROVIDED_OVERRIDE"
MISSING = "MISSING — NOT VERIFIED"


@dataclass
class Value:
    """A number plus its mandatory provenance. Untagged numbers cannot exist."""
    name: str
    number: Optional[float]
    provenance: str
    formula: str = ""
    receipt: str = ""

    @property
    def ok(self) -> bool:
        return self.provenance != MISSING and self.number is not None

    def tag(self) -> str:
        if self.provenance == COMPUTED:
            return f"[{COMPUTED}: {self.formula}]"
        return f"[{self.provenance}]"


class AuditLog:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def add(self, line: str) -> None:
        self.lines.append(line)

    def dump(self) -> str:
        return "\n".join(self.lines)


# ----------------------------- ingest layer --------------------------------

def open_source(path: Path, log: AuditLog) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    log.add(f'OPENED source: {doc["source_name"]} (as-of {doc["as_of"]})')
    return doc


def extract_direct(doc: dict, label: str, name: str, log: AuditLog) -> Value:
    """Receipt-echo gate: a DIRECT value exists only if its raw line is echoed."""
    for line in doc["lines"]:
        if line["label"] == label:
            raw = f'{line["label"]}: {line["value"]}'
            log.add(f'RECEIPT_ECHO="{raw}" — {doc["source_name"]}, as-of {doc["as_of"]}')
            number = float(str(line["value"]).replace(",", ""))
            return Value(name, number, DIRECT, receipt=raw)
    log.add(f"{name}: label '{label}' not present in source -> {MISSING}")
    return Value(name, None, MISSING)


def analyst_override(doc: dict, key: str, name: str, log: AuditLog) -> Value:
    """Analyst chart inputs enter as USER_PROVIDED_OVERRIDE, never as DIRECT."""
    inputs = doc.get("analyst_inputs", {})
    if key in inputs:
        log.add(f"{name}={inputs[key]} [{OVERRIDE}] (analyst chart input)")
        return Value(name, float(inputs[key]), OVERRIDE)
    log.add(f"{name}: no analyst input -> {MISSING}")
    return Value(name, None, MISSING)


def compute(name: str, formula: str, fn: Callable[..., float],
            log: AuditLog, *inputs: Value) -> Value:
    """Computation gate: only tagged Values may enter; MISSING propagates."""
    for v in inputs:
        if not isinstance(v, Value):
            raise UntaggedValueError(f"untagged raw number passed into {name}")
    dead = [v.name for v in inputs if not v.ok]
    if dead:
        log.add(f"{name}: blocked, missing driver(s): {', '.join(dead)} -> {MISSING}")
        return Value(name, None, MISSING, formula=formula)
    result = fn(*[v.number for v in inputs])
    out = Value(name, result, COMPUTED, formula=formula)
    log.add(f"{name}={result:g} {out.tag()}")
    return out


# --------------------- demo scoring constants (ALL FAKE) --------------------
# Chosen so the toy reproduces the published DEMO-A artifacts exactly.
# These are NOT the production weights. Production weighting is private.

DEMO_SUBSCORES = {"whynow": 7, "moat": 8, "survival": 6, "financing": 5,
                  "growth": 8, "tradability": 7, "consensus": 6}
DEMO_WEIGHTS = {"whynow": 1.0, "moat": 1.0, "survival": 2.0, "financing": 3.0,
                "growth": 1.0, "tradability": 1.0, "consensus": 1.0}  # sums to 10

MOM_COMPONENTS = {"trend": 72, "structure": 61, "volume": 44,
                  "volatility": 55, "rel_strength": 51}
MOM_WEIGHTS = {"trend": 0.25, "structure": 0.20, "volume": 0.15,
               "volatility": 0.20, "rel_strength": 0.20}  # sums to 1.0

DEMO_HEADROOM_MULT = 2.9  # fake demo constant


# ----------------------------- gate + final state ---------------------------

def resolve_gate(price: Value, resistance_low: Value, volume_trend: str,
                 data_quality: str) -> tuple[str, str]:
    """Illustrative demo gate. Enum CLEAR / WAIT_FOR_RESET / NO_TRADE.
    Production trigger logic is private. Rule demonstrated: the gate can
    never print CLEAR while data quality is PARTIAL."""
    if data_quality != "FULL":
        return "WAIT_FOR_RESET", "data quality PARTIAL blocks CLEAR"
    if price.ok and resistance_low.ok and price.number < resistance_low.number \
            and volume_trend == "contracting":
        return "WAIT_FOR_RESET", "below overhead supply on contracting volume"
    return "CLEAR", "demo conditions met"


def resolve_final_state(gate: str) -> tuple[str, str]:
    """Illustrative demo mapping: timing authority outranks the total."""
    if gate != "CLEAR":
        return "Watch", f"tape gate {gate} overrides total"
    return "Starter", "demo mapping"


# ----------------------------- output schema lock ---------------------------

SCHEMA_KEYS = ["TICKER", "AS_OF", "TOTAL_SCORE", "MOMENTUM_SCORE",
               "HEADROOM_SCORE", "RR_RATIO", "ENGINE_TAPE_GATE",
               "VALUATION_MODULE", "FINAL_STATE", "FINAL_STATE_REASON",
               "SYNTHETIC"]


def validate_schema(pairs: list[tuple[str, str]]) -> None:
    keys = [k for k, _ in pairs]
    for k in keys:
        if k not in SCHEMA_KEYS:
            raise SchemaError(f"SCHEMA_ERROR — KEY NAME NOT CANONICAL: {k}")
    if keys != SCHEMA_KEYS:
        raise SchemaError("HALT — FORMAT DRIFT (SCHEMA_LOCK)")


def render_block(pairs: list[tuple[str, str]]) -> str:
    validate_schema(pairs)
    body = [f"{k}={v}" for k, v in pairs]
    return "\n".join(["BEGIN_SCORECARD"] + body + ["END_SCORECARD"])


def diff_guard(anchor: dict, candidate: dict, updated_keys: set) -> list:
    """Regression guard: any change outside declared keys raises."""
    changed = [k for k in anchor if candidate.get(k) != anchor[k]]
    illegal = [k for k in changed if k not in updated_keys]
    if illegal:
        raise RegressionError(
            "REGRESSION_ERROR — NON-UPDATED KEY CHANGED: " + ",".join(illegal))
    return changed


# ----------------------------- the pipeline --------------------------------

PUBLISHED_BLOCK = """BEGIN_SCORECARD
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
END_SCORECARD"""


def run_pipeline(source_path: Path | None = None) -> tuple[AuditLog, str]:
    log = AuditLog()
    path = source_path or Path(__file__).resolve().parent / "sample_source.json"
    doc = open_source(path, log)

    # 1) Ingest with receipt echoes -----------------------------------------
    price = extract_direct(doc, "Price", "PRICE", log)
    revenue = extract_direct(doc, "Revenue (TTM)", "REVENUE_TTM", log)
    gross_profit = extract_direct(doc, "Gross profit (TTM)", "GROSS_PROFIT_TTM", log)
    shares = extract_direct(doc, "Shares outstanding", "SHARES_OUT", log)
    ma50 = extract_direct(doc, "50-day moving average", "MA50D", log)
    ma200 = extract_direct(doc, "200-day moving average", "MA200D", log)
    ma20 = extract_direct(doc, "20-day moving average", "MA20D", log)      # absent
    high52 = extract_direct(doc, "52-week high", "HIGH_52W", log)
    net_debt = extract_direct(doc, "Net debt", "NET_DEBT", log)            # absent

    data_quality = "FULL" if ma20.ok else "PARTIAL (MA20D MISSING)"
    log.add(f"DATA_QUALITY={data_quality}")

    # 2) Computations — MISSING propagates, nothing estimated ---------------
    compute("GROSS_MARGIN_PCT", "GROSS_PROFIT_TTM / REVENUE_TTM * 100",
            lambda gp, r: gp / r * 100, log, gross_profit, revenue)
    ev = compute("EV", "PRICE * SHARES_OUT + NET_DEBT",
                 lambda p, s, nd: p * s + nd, log, price, shares, net_debt)
    ev_sales = compute("EV_SALES", "EV / REVENUE_TTM",
                       lambda e, r: e / r, log, ev, revenue)

    # 3) Module layer (fake demo weights) ------------------------------------
    total = sum(DEMO_WEIGHTS[m] * DEMO_SUBSCORES[m] for m in DEMO_SUBSCORES)
    log.add(f"TOTAL_SCORE={total:g} (fake demo weights; production weighting private)")
    valuation_module = ("FLAGGED (EV/Sales MISSING)" if not ev_sales.ok
                        else "scored")
    log.add(f"VALUATION_MODULE={valuation_module}")

    # 4) Non-total layers -----------------------------------------------------
    momentum = round(sum(MOM_WEIGHTS[c] * MOM_COMPONENTS[c] for c in MOM_COMPONENTS))
    authority = "LOW" if not ma20.ok else "FULL"
    log.add(f"MOMENTUM_SCORE={momentum} authority={authority} ({data_quality})")

    upside_pct = compute("UPSIDE_PCT", "(HIGH_52W - PRICE) / PRICE * 100",
                         lambda h, p: (h - p) / p * 100, log, high52, price)
    headroom = round(upside_pct.number * DEMO_HEADROOM_MULT) if upside_pct.ok else None
    log.add(f"HEADROOM_SCORE={headroom} (demo multiplier {DEMO_HEADROOM_MULT}, fake)")

    stop = analyst_override(doc, "support_band_low", "STOP_REF", log)
    target = analyst_override(doc, "measured_objective", "TARGET_REF", log)
    risk = compute("RISK", "PRICE - STOP_REF", lambda p, s: p - s, log, price, stop)
    reward = compute("REWARD", "TARGET_REF - PRICE", lambda t, p: t - p, log, target, price)
    rr = compute("RR_RATIO", "REWARD / RISK",
                 lambda rw, rk: round(rw / rk, 2), log, reward, risk)

    # 5) Gate + final state ---------------------------------------------------
    resistance_low = analyst_override(doc, "resistance_band_low", "RESISTANCE_LOW", log)
    gate, gate_reason = resolve_gate(price, resistance_low,
                                     doc.get("volume_trend", ""), 
                                     "FULL" if ma20.ok else "PARTIAL")
    log.add(f"ENGINE_TAPE_GATE={gate} ({gate_reason})")
    final_state, reason = resolve_final_state(gate)

    # 6) Locked output block --------------------------------------------------
    pairs = [
        ("TICKER", doc["ticker"]),
        ("AS_OF", doc["as_of"]),
        ("TOTAL_SCORE", f"{int(total)}/100 [DEMO_PLACEHOLDER]"),
        ("MOMENTUM_SCORE", f"{momentum}/100 [DEMO_PLACEHOLDER]"),
        ("HEADROOM_SCORE", f"{headroom}/100 [DEMO_PLACEHOLDER]"),
        ("RR_RATIO", f"{rr.number:g}:1 [DEMO_PLACEHOLDER]"),
        ("ENGINE_TAPE_GATE", gate),
        ("VALUATION_MODULE", valuation_module),
        ("FINAL_STATE", final_state),
        ("FINAL_STATE_REASON", reason),
        ("SYNTHETIC", "TRUE — placeholder demo, not a live run"),
    ]
    return log, render_block(pairs)


def main() -> int:
    log, block = run_pipeline()
    print("=" * 72)
    print("AUDIT TRAIL (receipt echoes, provenance tags, blocked computations)")
    print("=" * 72)
    print(log.dump())
    print("=" * 72)
    print("FINAL BLOCK (schema-locked)")
    print("=" * 72)
    print(block)
    print("=" * 72)
    print(f"BYTE_MATCH_PUBLISHED_ARTIFACT={block == PUBLISHED_BLOCK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
