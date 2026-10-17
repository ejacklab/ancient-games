"""Write insight-triage.md from the insight-triage workflow's output file (item 13)."""
import json
import sys
from collections import Counter

data = json.load(open(sys.argv[1]))["result"]
rows = data["sections"]
marks = Counter(r["mark"] for r in rows)
applied = sum(1 for r in rows if r["fix_applied"] != "not found")
out = [
    "# Item 13 — the older insight sections marked under R12.2 (2026-10-17)",
    "",
    "Read by three Sonnet readers (workflow insight-triage, read-only); table written by the main agent from their",
    "returns. R12.2: a failure is the evaluator's judgment or the owner's correction; what a check saw is evidence.",
    "",
    f"- Sections: {len(rows)}; marks: " + ", ".join(f"{k} {v}" for k, v in sorted(marks.items())),
    f"- Top fix found applied: {applied}; not found: {len(rows) - applied}",
    f"- Reader groups missing: {data.get('groups_missing', 0)}",
    "",
    "| file | ids | mark | fix applied | note |",
    "|---|---|---|---|---|",
]
for r in rows:
    cell = lambda s: s.replace("|", "/").replace("\n", " ")
    out.append(f"| {cell(r['file'])} | {cell(r['ids'])} | {r['mark']} | {cell(r['fix_applied'])} | {cell(r['note'])} |")
open(sys.argv[2], "w").write("\n".join(out) + "\n")
print(len(rows), dict(marks), applied)
