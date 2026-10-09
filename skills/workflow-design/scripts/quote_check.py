#!/usr/bin/env python3
"""quote_check.py — check an explorer's findings against the code they cite (method 3.8 item 10).
Stdlib only, no model calls.

Every finding names a source `path:LINE` or `path:START-END` and a short verbatim quote. The check: the file
exists under --root, the lines exist, and the quote (whitespace-normalised) is inside those lines. It kills
invented sources and wrong locations; it cannot tell whether the explorer's reading of the code is right — that is
what `ran` claims are for.

Input, either form (docs/workflow-templates/explorer-file.md):
  markdown  a table whose header has the columns  id | ... | Kind | Source | Quote | Evidence
  jsonl     one object per line: {"id", "source", "quote", "kind", "evidence"}
Kind is `read` (inferred from the code) or `ran` (confirmed by running it); a `ran` finding must name its evidence.

Usage: quote_check.py FILE [--root DIR] [--slack N] [--min-quote N]
  --slack N   accept a quote found up to N lines outside the cited range, reported as `moved` with the real line
Exit: 0 every finding ok, 1 any finding failed, 2 usage error (no findings found, unreadable input).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SRC_RE = re.compile(r"^`?(?P<path>[^`:\s]+):(?P<a>\d+)(?:-(?P<b>\d+))?`?$")
KINDS = {"read", "ran"}


def norm(s: str) -> str:
    return " ".join(s.split())


def strip_code(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == "`" and s[-1] == "`":
        s = s[1:-1]
    return s.strip()


def split_row(line: str) -> list[str]:
    cells = re.split(r"(?<!\\)\|", line.strip())[1:-1]
    return [c.replace("\\|", "|").strip() for c in cells]


def parse_markdown(text: str) -> list[dict]:
    rows, cols, fenced = [], None, False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):              # a table inside a code fence is a placeholder, not findings
            fenced, cols = not fenced, None
            continue
        if fenced:
            continue
        if not s.startswith("|"):
            cols = None                      # a table ended; the next one needs its own header
            continue
        cells = split_row(s)
        low = [c.lower() for c in cells]
        if cols is None:
            if "source" in low and "quote" in low:
                cols = low
            continue
        if set(s) <= set("|-: "):
            continue
        rec = dict(zip(cols, cells))
        rows.append({"id": rec.get("id", "?"), "source": strip_code(rec.get("source", "")),
                     "quote": strip_code(rec.get("quote", "")), "kind": rec.get("kind", "").strip().lower(),
                     "evidence": rec.get("evidence", "").strip(), "has_kind": "kind" in cols})
    return rows


def parse_jsonl(text: str) -> list[dict]:
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip():
            e = json.loads(line)
            out.append({"id": str(e.get("id", n)), "source": str(e.get("source", "")), "quote": str(e.get("quote", "")),
                        "kind": str(e.get("kind", "")).lower(), "evidence": str(e.get("evidence", "") or ""),
                        "has_kind": "kind" in e})
    return out


def check(f: dict, root: Path, slack: int, min_quote: int, cache: dict) -> tuple[str, str]:
    problems = []
    if f["has_kind"]:
        if f["kind"] not in KINDS:
            problems.append(f"kind {f['kind']!r} is not read or ran")
        elif f["kind"] == "ran" and f["evidence"] in ("", "—", "-"):
            problems.append("a ran claim names no evidence")
    m = SRC_RE.match(f["source"])
    if not m:
        return "bad", "; ".join(problems + [f"source {f['source']!r} is not path:LINE or path:START-END"])
    q = norm(f["quote"])
    if len(q) < min_quote:
        return "bad", "; ".join(problems + [f"quote shorter than {min_quote} characters"])
    path = root / m["path"]
    if not path.is_file():
        return "missing", "; ".join(problems + [f"file {m['path']} does not exist"])
    if path not in cache:
        cache[path] = path.read_text(errors="replace").splitlines()
    lines = cache[path]
    a, b = int(m["a"]), int(m["b"] or m["a"])
    if a < 1 or b < a or b > len(lines):
        return "bad", "; ".join(problems + [f"lines {a}-{b} outside the file (1-{len(lines)})"])
    if q in norm(" ".join(lines[a - 1:b])):
        return ("bad", "; ".join(problems)) if problems else ("ok", "")
    width = b - a
    for d in range(1, slack + 1):
        for start in (a - d, a + d):
            if 1 <= start and start + width <= len(lines) and q in norm(" ".join(lines[start - 1:start + width])):
                where = f"{m['path']}:{start}" + (f"-{start + width}" if width else "")
                return ("bad" if problems else "moved"), "; ".join(problems + [f"quote is at {where}"])
    return "missing", "; ".join(problems + [f"quote not found at {m['path']}:{a}" + (f"-{b}" if b != a else "")])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file")
    ap.add_argument("--root", default=".", help="the repo the sources are relative to")
    ap.add_argument("--slack", type=int, default=0)
    ap.add_argument("--min-quote", type=int, default=8)
    a = ap.parse_args(argv)
    p = Path(a.file)
    try:
        text = p.read_text()
        findings = parse_jsonl(text) if p.suffix == ".jsonl" else parse_markdown(text)
    except (OSError, ValueError) as e:
        print(f"quote_check: cannot read {a.file}: {e}", file=sys.stderr)
        return 2
    if not findings:
        print(f"quote_check: no findings with Source and Quote columns in {a.file}", file=sys.stderr)
        return 2
    cache: dict = {}
    counts: dict[str, int] = {}
    for f in findings:
        verdict, why = check(f, Path(a.root), a.slack, a.min_quote, cache)
        counts[verdict] = counts.get(verdict, 0) + 1
        if verdict != "ok":
            print(f"{verdict:7} {f['id']}: {why}")
    ran = sum(1 for f in findings if f["kind"] == "ran")
    print(f"{len(findings)} findings: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
          + f"; kind ran {ran}, read {sum(1 for f in findings if f['kind'] == 'read')}")
    return 0 if counts.get("ok", 0) + counts.get("moved", 0) == len(findings) else 1


if __name__ == "__main__":
    sys.exit(main())
