#!/usr/bin/env python3
"""d6_verify.py — the COO runs the three most serious D6 claims instead of trusting a review that ran nothing."""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"tools/evaluator/{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


with tempfile.TemporaryDirectory() as tmp:
    run = Path(tmp)
    # F1: a spec with zero in-scope requirements
    (run / "requirements.json").write_text(json.dumps({"spec": {}, "groups": [], "vision": [], "manifest": []}))
    r = subprocess.run([sys.executable, str(ROOT / "tools/evaluator/verdict.py"), "--run", str(run)],
                       capture_output=True, text=True)
    print("F1 zero requirements ->", r.stdout.splitlines()[0] if r.stdout else r.stderr.strip())

# F3: citations of hyphenated case ids
pm = load("probe_matrix")
for doc in ('"""EV-P1-F2 — x"""', '"""B1-F1 — x"""'):
    m = pm.CITATION.match(doc.strip('"').split(" — ")[0])
    print("F3 citation of", doc, "->", m.group(1) if m else None)

# F5: a mutant whose run left no report counts as proof
vd = load("verdict")
row = vd._decide_case("X1-F1", {"kind": "executable", "reason": "r"},
                      {"citations": {"t::a": ["X1-F1"]}, "product": {"t::a": "pass"},
                       "mutants": {"X1-F1": {"status": "applied", "results": {"t::a": "fail"}}}, "restored": True},
                      [], {})
print("F5 an 'all red' mutant run (what a timeout produces) ->", row["verdict"])
