#!/usr/bin/env python3
"""k2_score.py — K2's score: for each variant, its fault group's case verdicts against the clean K1c."""
import json
from pathlib import Path

faults = json.loads(Path("/tmp/claude-1000/-home-smoke01-dev-ancient-games/cf13332d-7485-4348-b877-808de8ee85c2/plants/k2-faults.json").read_text())
base = {c["case"]: c["verdict"] for c in json.loads(Path("runs/20261013-eval-k1c/verdict.json").read_text())["cases"]}
own = {r["variant"]: r["own_tests"] for r in json.loads(Path("runs/20261013-calibration/k2-prepare.json").read_text())}
rows = []
for n, fault in enumerate(faults, 1):
    v = json.loads(Path(f"runs/20261013-eval-k2-{n}/verdict.json").read_text())
    cases = {c["case"]: c["verdict"] for c in v["cases"]}
    changed = {c: (base.get(c), cases[c]) for c in cases if c.startswith(fault["group"] + "-F") and base.get(c) != cases[c]}
    new_fail = [c for c, (b, a) in changed.items() if a == "FAIL"]
    strong = "FAIL (new)" if new_fail else ("changed" if changed else "no change")
    rows.append((n, fault["id"], fault["group"], fault["what"], strong, changed, own[n]))
    print(f"variant {n} {fault['id']} [{fault['group']}] {fault['what']}: evaluator {strong} {changed}; product's own tests: {own[n]}")
caught = sum(1 for r in rows if r[4] == "FAIL (new)")
print(f"evaluator: {caught}/{len(rows)} faults turned their group's case to a new FAIL; "
      f"own tests: {sum(1 for r in rows if r[6] == 'caught')}/{len(rows)} caught")
