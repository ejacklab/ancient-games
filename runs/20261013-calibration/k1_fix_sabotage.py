#!/usr/bin/env python3
"""Undo each K1 repair in turn; the named tests must go red. COO, run 20261013-requirements-evaluator D5."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PM, MI = ROOT / "tools/evaluator/probe_matrix.py", ROOT / "tools/evaluator/model_io.py"
TESTS = ["tests/test_evaluator_probe_matrix.py", "tests/test_evaluator_k1_regressions.py"]
UNDO = [
    ("absolute paths", PM, "    product, probes = product.resolve(), probes.resolve()\n", ""),
    ("failure output recorded", PM, "    if output:  # optional", "    if False:  # optional"),
    ("no-output void", MI, "        if not str(context.get(\"output\") or \"\").strip():", "        if False:"),
    ("confirm file required", MI, "        _require_model_file(run / \"confirm.json\", \"confirm\")", "        pass"),
    ("judge file required", MI, "        _require_model_file(run / \"judge-1.json\", \"first judge\")", "        pass"),
    ("run-folder path accepted", MI, "            relative = relative[len(prefix):]", "            pass"),
    ("K1b: removed-file void", MI, "        elif any(path in str(context.get(\"output\")) for path in removed):",
     "        elif False:"),
    ("K1b: absolute repro path", ROOT / "tools/evaluator/verdict.py", "EVAL_PRODUCT=\"$PWD\"/{", "EVAL_PRODUCT={"),
]
env = {k: v for k, v in os.environ.items() if k != "NO_COLOR"}
bad = 0
for name, path, old, new in UNDO:
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, (name, text.count(old))
    try:
        path.write_text(text.replace(old, new), encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                           cwd=ROOT, capture_output=True, text=True, env=env, timeout=600)
    finally:
        path.write_text(text, encoding="utf-8")
    caught = r.returncode != 0
    bad += not caught
    print(f"{name}: {'caught' if caught else 'NOT CAUGHT'} — {r.stdout.strip().splitlines()[-1]}")
print("all caught" if not bad else f"{bad} not caught")
sys.exit(1 if bad else 0)
