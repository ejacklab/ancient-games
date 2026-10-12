#!/usr/bin/env python3
"""mutate.py — N3's check, written by the COO for run 20261012-index-md-build.

  mutate.py MUTANTS.json WORKTREE OUT.md

MUTANTS.json: [{"id": "M1", "fails_if": "B3.1 ...", "old": "<exact text>", "new": "<replacement>"}].
Each mutant replaces `old` (it must occur exactly once) in its `file` (default tools/memory_index.py), runs the acceptance file and the unit
file, and restores the original bytes. Killed = the acceptance file has at least one failure. The original's sha256
is checked at the end. What it does NOT establish: behaviour that no mutant breaks.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def run(wt: Path, test_file: str, env: dict) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-x", test_file],
                       cwd=wt, capture_output=True, text=True, env=env, timeout=600)
    return r.returncode, (r.stdout.strip().splitlines() or ["(no output)"])[-1]


def main(argv: list[str]) -> int:
    muts = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    wt, out = Path(argv[2]), Path(argv[3])
    files = {m.get("file", "tools/memory_index.py") for m in muts}
    origs = {f: (wt / f).read_bytes() for f in files}
    h0 = {f: hashlib.sha256(b).hexdigest() for f, b in origs.items()}
    env = {k: v for k, v in os.environ.items() if k != "NO_COLOR"}
    rows = []
    try:
        for m in muts:
            target = wt / m.get("file", "tools/memory_index.py")
            orig = origs[m.get("file", "tools/memory_index.py")]
            src = orig.decode("utf-8")
            n = src.count(m["old"])
            if n != 1:
                rows.append((m["id"], m["fails_if"], f"INVALID (old occurs {n}x)", "", ""))
                continue
            target.write_text(src.replace(m["old"], m["new"]), encoding="utf-8")
            acc_code, acc_last = run(wt, "tests/test_memory_index.py", env)
            unit_code, _ = run(wt, "tests/test_memory_index_unit.py", env)
            target.write_bytes(orig)
            rows.append((m["id"], m["fails_if"], "killed" if acc_code else "SURVIVED", acc_last,
                         "killed" if unit_code else "survived"))
    finally:
        for f, b in origs.items():
            (wt / f).write_bytes(b)
    assert all(hashlib.sha256((wt / f).read_bytes()).hexdigest() == h for f, h in h0.items()), "not restored"
    lines = ["| mutant | Fails if it breaks | acceptance file | acceptance summary | unit file (info) |",
             "|---|---|---|---|---|"] + [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in rows]
    bad = [r for r in rows if r[2] != "killed"]
    lines.append(f"\n{len(rows) - len(bad)}/{len(rows)} killed; originals restored ({len(h0)} file(s))")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
