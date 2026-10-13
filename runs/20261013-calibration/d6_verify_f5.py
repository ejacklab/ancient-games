#!/usr/bin/env python3
"""d6_verify_f5.py — F5 after R1, on the shapes probe_matrix now writes (COO)."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("verdict_f5", ROOT / "tools/evaluator/verdict.py")
vd = importlib.util.module_from_spec(spec)
sys.modules["verdict_f5"] = vd
spec.loader.exec_module(vd)

def case(matrix):
    return vd._decide_case("X1-F1", {"kind": "executable", "reason": "r"}, matrix, [], {})["verdict"]

base = {"citations": {"t::a": ["X1-F1"], "t::b": ["X2-F1"]}, "product": {"t::a": "pass", "t::b": "pass"},
        "restored": True}
timeout = dict(base, mutants={"X1-F1": {"status": "applied", "results": {"t::a": "fail", "t::b": "fail"}}},
               runs={"X1-F1": {"status": "timeout", "errors": []}})
all_red_two = dict(base, mutants={"X1-F1": {"status": "applied", "results": {"t::a": "fail", "t::b": "fail"}}})
error_only = dict(base, mutants={"X1-F1": {"status": "applied", "results": {"t::a": "fail", "t::b": "pass"}}},
                  runs={"X1-F1": {"status": "ok", "errors": ["t::a"]}})
healthy = dict(base, mutants={"X1-F1": {"status": "applied", "results": {"t::a": "fail", "t::b": "pass"}}})
print("timeout recorded       ->", case(timeout), "(want UNKNOWN)")
print("all red, 2 probes      ->", case(all_red_two), "(want UNKNOWN)")
print("red only by a JUnit error ->", case(error_only), "(want UNKNOWN)")
print("healthy kill           ->", case(healthy), "(want PASS)")
