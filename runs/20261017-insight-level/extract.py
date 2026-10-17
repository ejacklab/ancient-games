"""List every insight section in runs/*/insight.md: id and title, its Source line and its Root cause line.

Run from the repository root: python3 runs/20261017-insight-level/extract.py > runs/20261017-insight-level/insights.md
"""
import glob
import re

print("# Every insight section (runs/*/insight.md), extracted by extract.py\n")
print("Each: the run, the heading, then the section's own `Source:` and `Root cause:` lines, verbatim.\n")
count = 0
for path in sorted(glob.glob("runs/*/insight.md")):
    run = path.split("/")[1]
    section = None
    fields = {}

    def flush():
        global count
        if section is None:
            return
        count += 1
        print(f"- **{run}** — {section}")
        for key in ("Source", "Root cause"):
            if key in fields:
                print(f"  - {key}: {fields[key]}")

    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("## "):
            flush()
            section = line[3:].strip()
            fields = {}
            continue
        match = re.match(r"^(Source|Root cause):\s*(.*)$", line)
        if match and section is not None and match.group(1) not in fields:
            fields[match.group(1)] = match.group(2)
    flush()
print(f"\n{count} sections.")
