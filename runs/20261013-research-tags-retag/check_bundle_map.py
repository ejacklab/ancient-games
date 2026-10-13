#!/usr/bin/env python3
"""check_bundle_map.py — piece B's check (written by the COO, Claude): every bundle path named in the README's
`docs/X` is `Y` mapping exists under skills/, and every docs/ source it names exists in the repo.
Usage: check_bundle_map.py [README]   exit 1 on any missing path."""
import re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
readme = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "skills/README.md"
text = " ".join(readme.read_text().split())
pairs = re.findall(r"`(docs/[^`]+)` is `(workflow-design/[^`]+)`", text)
bad = [f"no mapping line found in {readme}"] if not pairs else []
for src, dst in pairs:
    if not (REPO / src).exists(): bad.append(f"source missing: {src}")
    if not (REPO / "skills" / dst).exists(): bad.append(f"bundle path missing: skills/{dst}")
print("\n".join(bad) if bad else f"B check: PASS — {len(pairs)} mappings, every source and bundle path exists")
sys.exit(1 if bad else 0)
