#!/usr/bin/env python3
"""check_r1_tests.py — the COO's check of the R1 test node: collect, how many fail today, findings cited, harness runs."""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
env = {k: v for k, v in os.environ.items() if k != "NO_COLOR"}
for test_file, ids in [("tests/test_evaluator_r1.py",
                        "F1 F2 F4 F5 F6 F7 F8 F9 F10 F11 F12 F13 F14 F15 F16 F17 F18 F19 F20".split()),
                       ("tests/test_evaluator_r1_matrix_spec.py", "F1 F3 F4 F5 F14".split())]:
    path = ROOT / test_file
    if not path.exists():
        print(f"{test_file}: absent")
        continue
    text = path.read_text(encoding="utf-8")
    missing = [i for i in ids if not re.search(rf"R1-{i}\b", text)]
    col = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", test_file],
                         cwd=ROOT, capture_output=True, text=True, env=env)
    run = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test_file],
                         cwd=ROOT, capture_output=True, text=True, env=env, timeout=900)
    print(f"{test_file}: collect: {col.stdout.strip().splitlines()[-1]} | today: {run.stdout.strip().splitlines()[-1]}"
          f" | missing ids: {missing or 'none'}")
h = subprocess.run(["node", "tests/workflows/evaluate_harness.mjs"], cwd=ROOT, capture_output=True, text=True)
print("harness:", (h.stdout.strip().splitlines() or ["(no output)"])[-1], "| exit", h.returncode,
      "| crashed" if "Error" in h.stderr else "")
