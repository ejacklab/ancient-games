#!/usr/bin/env python3
"""k2_diff.py — for each K2 variant, the probes that turned red against K1c, and the case groups they cite."""
import json
from pathlib import Path

base = json.loads(Path("runs/20261013-eval-k1c/matrix.json").read_text())
faults = json.loads(Path("/tmp/claude-1000/-home-smoke01-dev-ancient-games/cf13332d-7485-4348-b877-808de8ee85c2/plants/k2-faults.json").read_text())
for n, fault in enumerate(faults, 1):
    m = json.loads(Path(f"runs/20261013-eval-k2-{n}/matrix.json").read_text())
    new_red = [k for k, v in m["product"].items() if v == "fail" and base["product"].get(k) != "fail"]
    groups = sorted({c.rsplit("-F", 1)[0] for k in new_red for c in m["citations"].get(k, [])})
    hit = fault["group"] in groups
    print(f"variant {n} {fault['id']} [{fault['group']}] {fault['what']}: {len(new_red)} newly red; groups {groups}; "
          f"{'HIT' if hit else 'MISS'}")
