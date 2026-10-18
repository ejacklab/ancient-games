#!/usr/bin/env python3
"""summarise.py RUN_DIR — the COO's one-screen summary of an evaluator run (calibration, D5)."""
import json
import sys
from collections import Counter
from pathlib import Path

K = Path(sys.argv[1])
print((K / "verdict.md").read_text(encoding="utf-8").splitlines()[0])
v = json.loads((K / "verdict.json").read_text())
c = json.loads((K / "classify.json").read_text()) if (K / "classify.json").exists() else {"cases": []}
print("kinds:", dict(Counter(x["kind"] for x in c["cases"])))
print("case verdicts:", dict(Counter(x["verdict"] for x in v["cases"])))
print("non-PASS reasons:", dict(Counter(x["reason"] for x in v["cases"] if x["verdict"] != "PASS")))
for x in v["cases"]:
    if x["verdict"] == "FAIL":
        print("  FAIL", x["case"], x["kind"], "|", x["repro"][:170])
print("requirements:", dict(Counter(r["verdict"] for r in v["requirements"])), "out_of_scope:", v["out_of_scope"])
m = json.loads((K / "matrix.json").read_text())
print("probes:", len(m["product"]), "red on product:", sum(1 for r in m["product"].values() if r == "fail"),
      "mutants:", len(m["mutants"]), dict(Counter(x["status"] for x in m["mutants"].values())), "restored:", m["restored"])
if (K / "judged.json").exists():
    j = json.loads((K / "judged.json").read_text())
    print("judged: plant_case", j.get("plant_case"), "plant_found", j.get("plant_found"), "n", len(j.get("cases", [])))
