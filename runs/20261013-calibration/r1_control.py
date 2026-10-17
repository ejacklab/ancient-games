#!/usr/bin/env python3
"""r1_control.py — Dave's control: re-decide the recorded runs with the R1 verdict.py and list every case change."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("verdict_r1", ROOT / "tools/evaluator/verdict.py")
vd = importlib.util.module_from_spec(spec)
sys.modules["verdict_r1"] = vd
spec.loader.exec_module(vd)
for name in ["20261013-eval-k1c"] + [f"20261013-eval-k2-{n}" for n in range(1, 7)]:
    run = ROOT / "runs" / name
    old = json.loads((run / "verdict.json").read_text())
    new = vd.decide(run)
    before = {c["case"]: c["verdict"] for c in old["cases"]}
    after = {c["case"]: (c["verdict"], c["reason"]) for c in new["cases"]}
    changes = {k: (before.get(k), v) for k, v in after.items() if before.get(k) != v[0]}
    print(f"{name}: meets {old['meets']}→{new['meets']}; {len(changes)} case changes {changes}; "
          f"input_problems {len(new.get('input_problems', []))}; orphans {len(new.get('orphan_probes', []))}")
