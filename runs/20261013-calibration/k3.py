#!/usr/bin/env python3
"""k3.py — calibration K3 (COO, run 20261013-requirements-evaluator D5). Script-only, no model calls.

A doctored copy of the INDEX.md spec:
- **planted:** group B9 with id B9.1 and no Fails if. It must come back UNKNOWN (untestable), never PASS (EV-R1.3).
- **deleted:** group C2, with ids C2.1 and C2.2. Those ids must be absent from the manifest and the verdict.

It runs the real spec_parse.py and verdict.py over the given evaluation run's other recorded results.

  k3.py SOURCE_RUN
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

src = Path(sys.argv[1])
k3 = Path("runs/20261013-eval-k3")
if k3.exists():
    shutil.rmtree(k3)
k3.mkdir(parents=True)
for name in ("classify.json", "matrix.json", "confirm.json", "judged.json"):
    if (src / name).exists():
        shutil.copy2(src / name, k3 / name)
spec_src = Path("runs/20261013-calibration/raw/product-21b2597/docs/index-md")
spec = k3 / "spec"
spec.mkdir()
shutil.copy2(spec_src / "VISION.md", spec / "VISION.md")
text = (spec_src / "REQUIREMENTS.md").read_text(encoding="utf-8")
c2 = re.search(r"\*\*C2 — .*?(?=\n\*\*G1 — |\n## )", text, re.S)
assert c2, "C2 block not found"
text = text.replace(c2.group(0), "")
planted = "\n**B9 — Pleasant output** (planted by the COO for K3)\n- **B9.1** The output must be pleasant to read.\n"
text = text.replace("\n## C — ", planted + "\n## C — ", 1)
assert "B9.1" in text and "C2.1" not in text
(spec / "REQUIREMENTS.md").write_text(text, encoding="utf-8")

r = subprocess.run([sys.executable, "tools/evaluator/spec_parse.py", "--requirements", str(spec / "REQUIREMENTS.md"),
                    "--vision", str(spec / "VISION.md"), "--out", str(k3 / "requirements.json")],
                   capture_output=True, text=True)
assert r.returncode == 0, r.stderr
r = subprocess.run([sys.executable, "tools/evaluator/verdict.py", "--run", str(k3)], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
v = json.loads((k3 / "verdict.json").read_text())
rows = {row["id"]: row for row in v["requirements"]}
checks = {
    "B9.1 present and UNKNOWN": rows.get("B9.1", {}).get("verdict") == "UNKNOWN",
    "B9.1 reason says untestable": "untestable" in rows.get("B9.1", {}).get("reason", ""),
    "C2.1, C2.2 absent from the manifest": not {"C2.1", "C2.2"} & set(v["manifest"]),
    "C2.1, C2.2 absent from the verdict": not {"C2.1", "C2.2"} & set(rows),
    "not MEETS": v["meets"] is False,
}
for name, ok in checks.items():
    print(("PASS " if ok else "FAIL ") + name)
print("B9.1 row:", rows.get("B9.1"))
sys.exit(0 if all(checks.values()) else 1)
