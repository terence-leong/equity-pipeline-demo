#!/usr/bin/env python3
"""Tests for demo_pipeline.py — each test is a documented failure mode.

The suite proves the gates fire: the pipeline reproduces the published
artifact, MISSING propagates, untagged numbers are rejected, schema drift
halts, the regression guard trips, receipts gate DIRECT values, and the
tape gate cannot clear on partial data.
"""
import unittest

from demo_pipeline import (
    AuditLog, Value, DIRECT, MISSING, PUBLISHED_BLOCK,
    UntaggedValueError, SchemaError, RegressionError,
    compute, extract_direct, render_block, diff_guard,
    resolve_gate, run_pipeline,
)


class TestPipelineReproducesArtifact(unittest.TestCase):
    def test_block_matches_published_demo_artifact_byte_for_byte(self):
        _, block = run_pipeline()
        self.assertEqual(block, PUBLISHED_BLOCK)


class TestMissingPropagation(unittest.TestCase):
    def test_missing_driver_blocks_dependents_instead_of_estimating(self):
        log = AuditLog()
        a = Value("A", 10.0, DIRECT)
        b = Value("B", None, MISSING)
        out = compute("A_PLUS_B", "A + B", lambda x, y: x + y, log, a, b)
        self.assertFalse(out.ok)
        self.assertEqual(out.provenance, MISSING)

    def test_pipeline_flags_valuation_when_net_debt_absent(self):
        _, block = run_pipeline()
        self.assertIn("VALUATION_MODULE=FLAGGED (EV/Sales MISSING)", block)


class TestProvenanceEnforcement(unittest.TestCase):
    def test_untagged_raw_number_is_rejected(self):
        log = AuditLog()
        a = Value("A", 10.0, DIRECT)
        with self.assertRaises(UntaggedValueError):
            compute("BAD", "A + 5", lambda x, y: x + y, log, a, 5.0)

    def test_direct_value_requires_echoable_source_line(self):
        log = AuditLog()
        doc = {"source_name": "s", "as_of": "d", "lines": []}
        v = extract_direct(doc, "Absent label", "X", log)
        self.assertEqual(v.provenance, MISSING)
        self.assertFalse(any("RECEIPT_ECHO" in ln for ln in log.lines))


class TestSchemaLock(unittest.TestCase):
    def test_non_canonical_key_halts(self):
        with self.assertRaises(SchemaError):
            render_block([("TICKER", "X"), ("Ticker_Typo", "Y")])

    def test_key_order_drift_halts(self):
        # correct keys, wrong order -> hard stop
        pairs = [("AS_OF", "d"), ("TICKER", "X")]
        with self.assertRaises(SchemaError):
            render_block(pairs)


class TestRegressionGuard(unittest.TestCase):
    def test_out_of_scope_change_raises(self):
        anchor = {"A": "1", "B": "2"}
        candidate = {"A": "1", "B": "3"}
        with self.assertRaises(RegressionError):
            diff_guard(anchor, candidate, updated_keys={"A"})

    def test_declared_change_passes(self):
        anchor = {"A": "1", "B": "2"}
        candidate = {"A": "1", "B": "3"}
        self.assertEqual(diff_guard(anchor, candidate, {"B"}), ["B"])


class TestTapeGate(unittest.TestCase):
    def test_gate_cannot_clear_on_partial_data_even_with_bullish_tape(self):
        price = Value("PRICE", 25.0, DIRECT)           # above resistance
        resistance = Value("RESISTANCE_LOW", 19.8, DIRECT)
        gate, _ = resolve_gate(price, resistance, "expanding", "PARTIAL")
        self.assertEqual(gate, "WAIT_FOR_RESET")

    def test_gate_clears_only_on_full_data_and_demo_conditions(self):
        price = Value("PRICE", 25.0, DIRECT)
        resistance = Value("RESISTANCE_LOW", 19.8, DIRECT)
        gate, _ = resolve_gate(price, resistance, "expanding", "FULL")
        self.assertEqual(gate, "CLEAR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
