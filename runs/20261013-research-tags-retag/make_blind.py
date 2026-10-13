#!/usr/bin/env python3
"""make_blind.py — piece R1 of run 20261013-research-tags-retag (written by the COO, Claude).

Reads the five accepted r2 findings files, writes the blind sheet (no Label column, rows renumbered R001..R143 in a
fixed-seed shuffled order), the key (R-id -> section, original id, old label), the old definitions quoted from git
research-agent-memory.js (untracked; read before piece A), and a count of Finding texts that carry a tag-like word.

Usage: python3 make_blind.py            (writes blind/, key/)
       python3 make_blind.py --check    (checks what was written; exit 1 on any defect)
       python3 make_blind.py --check --sheet FILE  (check another sheet, for the sabotage test)
"""
import json, random, re, subprocess, sys
from collections import Counter
from pathlib import Path

RUN = Path(__file__).resolve().parent
REPO = RUN.parents[1]
SRC = sorted((REPO / "docs/research/20261011-agent-memory-graph-r2").glob("FINDINGS-s*.md"))
ROW = re.compile(r"^\|\s*(F\d+)\s*\|")
SEED = 20261013
EXPECTED = {"verified": 94, "reported": 44, "unproven": 3, "unknown": 2}
LEAK = re.compile(r"\b(verified|reported|unproven|unknown|primary|secondary)\b", re.I)


def read_rows():
    rows = []
    for f in SRC:
        sec = f.stem.split("FINDINGS-")[1]
        for line in f.read_text().splitlines():
            if not ROW.match(line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append({"section": sec, "orig": cells[0], "finding": cells[1], "label": cells[2],
                         "source": " | ".join(cells[3:])})
    return rows


def write():
    rows = read_rows()
    order = list(range(len(rows)))
    random.Random(SEED).shuffle(order)
    (RUN / "blind").mkdir(exist_ok=True); (RUN / "key").mkdir(exist_ok=True)
    key, out = {}, ["# Blind rows — 143 research findings", "",
                    "Each row: id · Finding · Source. Tag the Finding using only this row.", "",
                    "| id | Finding | Source |", "|---|---|---|"]
    for n, i in enumerate(order, 1):
        r = rows[i]; rid = f"R{n:03d}"
        key[rid] = {"section": r["section"], "orig": r["orig"], "old": r["label"]}
        out.append(f"| {rid} | {r['finding']} | {r['source']} |")
    (RUN / "blind/rows.md").write_text("\n".join(out) + "\n")
    (RUN / "key/old-labels.json").write_text(json.dumps(key, indent=1) + "\n")
    # the .js is untracked (no git HEAD copy); read it before piece A edits it, and record its checksum
    jsf = REPO / ".claude/workflows/research-agent-memory.js"
    sha = __import__("hashlib").sha256(jsf.read_bytes()).hexdigest()
    js = jsf.read_text().splitlines()
    i = next(k for k, l in enumerate(js) if l.strip().startswith("Labels: verified ="))
    quote = "\n".join(l.strip() for l in js[i:i + 2])
    (RUN / "blind/control-defs.md").write_text(
        f"Quoted verbatim from .claude/workflows/research-agent-memory.js (sha256 {sha}, before piece A), lines "
        f"{i + 1}-{i + 2} (the definitions the 143 rows were labelled under):\n\n{quote}\n")
    leaks = [rid for rid, n in zip(key, order) if LEAK.search(rows[n]["finding"])]
    (RUN / "blind/leaks.txt").write_text(f"{len(leaks)} of {len(rows)} Finding texts carry a tag-like word:\n"
                                         + " ".join(leaks) + "\n")
    print(f"wrote {len(rows)} rows; leaks {len(leaks)}")


def check(sheet):
    bad = []
    key = json.loads((RUN / "key/old-labels.json").read_text())
    lines = [l for l in Path(sheet).read_text().splitlines() if re.match(r"^\| R\d{3} \|", l)]
    ids = [l.split("|")[1].strip() for l in lines]
    if len(lines) != 143: bad.append(f"{len(lines)} rows, expected 143")
    if len(set(ids)) != len(ids): bad.append("duplicate ids: " + str([i for i, c in Counter(ids).items() if c > 1]))
    if set(ids) != set(key): bad.append(f"ids differ from the key: missing {sorted(set(key) - set(ids))[:5]}")
    counts = Counter(v["old"] for v in key.values())
    if dict(counts) != EXPECTED: bad.append(f"key label counts {dict(counts)} != {EXPECTED}")
    head = Path(sheet).read_text()
    if "| Label |" in head: bad.append("the sheet has a Label column")
    for l in lines:
        if re.search(r"\|\s*(verified|reported|unproven|unknown)\s*\|", l):
            bad.append(f"a bare tag cell in {l[:12]}")
    print("\n".join(bad) if bad else "R1 check: PASS — 143 rows, ids unique and equal to the key, counts 94/44/3/2, no Label column")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        s = sys.argv[sys.argv.index("--sheet") + 1] if "--sheet" in sys.argv else RUN / "blind/rows.md"
        sys.exit(check(s))
    write()
