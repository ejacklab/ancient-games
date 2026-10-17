#!/usr/bin/env python3
"""k2_prepare.py — D5 calibration, K2 (COO, run 20261013-requirements-evaluator).

For each seeded fault, build runs/20261013-eval-k2-<n>/ from K1's run folder: the same requirements, classification,
probes, mutants and judging (EJ, 2026-10-13: "K2 ok", reuse K1's probes). The fault is applied to the workspace's
product copy. Then probe_matrix and model_io confirm-input are run. Separately, the product's own acceptance tests
(tests/test_memory_index.py at 21b2597) run against the same fault, for the comparison.

  k2_prepare.py FAULTS.json K1_RUN PRODUCT_DIR
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REUSED = ("requirements.json", "classify.json", "mutants.json", "plants.json", "judged.json", "confirm.json")


def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=1800)


def apply(root: Path, fault: dict) -> None:
    path = root / fault["file"]
    text = path.read_text(encoding="utf-8")
    assert text.count(fault["old"]) == 1, (fault["id"], path)
    path.write_text(text.replace(fault["old"], fault["new"]), encoding="utf-8")


def main(argv: list[str]) -> int:
    faults = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    k1, product = Path(argv[2]), Path(argv[3])
    rows = []
    for n, fault in enumerate(faults, 1):
        k2 = Path(f"runs/20261013-eval-k2-{n}")
        if k2.exists():
            shutil.rmtree(k2)
        k2.mkdir(parents=True)
        for name in REUSED:
            if (k1 / name).exists():
                shutil.copy2(k1 / name, k2 / name)
        shutil.copytree(k1 / "probes", k2 / "probes", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(k1 / "workspace", k2 / "workspace", symlinks=True)
        apply(k2 / "workspace" / "product", fault)
        matrix = run([sys.executable, "tools/evaluator/probe_matrix.py", "--run", str(k2)])
        confirm = run([sys.executable, "tools/evaluator/model_io.py", "confirm-input", "--run", str(k2)])
        # the product's own acceptance tests on the same fault
        own = Path(f"runs/20261013-calibration/raw/own-k2-{n}")
        if own.exists():
            shutil.rmtree(own)
        shutil.copytree(product, own, symlinks=True, ignore=shutil.ignore_patterns("runs", "__pycache__"))
        apply(own, fault)
        env = {k: v for k, v in os.environ.items() if k != "NO_COLOR"}
        tests = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-x",
                     "tests/test_memory_index.py"], cwd=own, env=env)
        last = (tests.stdout.strip().splitlines() or ["(no output)"])[-1]
        rows.append({"variant": n, "fault": fault["id"], "group": fault["group"],
                     "matrix_exit": matrix.returncode, "confirm_input": confirm.stdout.strip(),
                     "own_tests": "caught" if tests.returncode else "MISSED", "own_tests_summary": last})
        print(json.dumps(rows[-1]))
    Path("runs/20261013-calibration/k2-prepare.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
