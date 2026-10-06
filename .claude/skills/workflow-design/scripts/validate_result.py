#!/usr/bin/env python3
"""validate_result.py — the script that checks a pass-back file (method 3.8). No model, stdlib only.

  result  a node's result file: a header between two `---` lines, then the body (docs/workflow-templates/result-file.md)
  digest  a research digest (docs/workflow-templates/research-file.md): capped length, required headings

Usage:
  validate_result.py FILE [--kind result|digest] [--node N] [--attempt K] [--model M] [--root DIR]
                     [--max-lines N] [--summary N]
Prints `ok <file>` or `fail <file>: <reason>; ...`, and with --summary N the first N body lines of a valid result
(what the COO reads). Exit: 0 valid, 1 findings, 2 usage error.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

RESULT_KEYS = ["node", "attempt", "engine", "model", "status", "started", "ended", "evidence"]
STATUSES = {"ok", "fail", "partial"}
DIGEST_HEADINGS = ["Answer", "Confidence", "Decision it triggers"]


def split_header(text: str):
    """The header is the first `---`…`---` block, wherever it is.

    A strict "header at byte 0" contract failed a real run (2026-10-05): claude printed one sentence of context
    before the header, and the whole node blocked on "no header". LLMs will keep adding a prelude, and the prelude
    is harmless — the header and body are still well-formed. Discard whatever precedes the first `---`; require the
    block itself to be well-formed.
    """
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip() == "---"), None)
    if start is None:
        return None, text
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == "---":
            hdr = {}
            for ln in lines[start + 1:i]:
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    hdr[k.strip()] = v.strip()
            return hdr, "\n".join(lines[i + 1:])
    return None, text


def check_result(text: str, node=None, attempt=None, model=None, root: Path | None = None):
    f = []
    hdr, body = split_header(text)
    if hdr is None:
        return ["no header between two '---' lines"], "", {}
    for k in RESULT_KEYS:
        if not hdr.get(k):
            f.append(f"header is missing {k!r}")
    if hdr.get("status") and hdr["status"] not in STATUSES:
        f.append(f"status {hdr['status']!r} is not one of {sorted(STATUSES)}")
    if node and hdr.get("node") and hdr["node"] != node:
        f.append(f"node {hdr['node']!r} != contract {node!r}")
    if attempt and hdr.get("attempt") and hdr["attempt"] != str(attempt):
        f.append(f"attempt {hdr['attempt']!r} != {attempt}")
    if model and hdr.get("model") and hdr["model"] != model:
        f.append(f"model {hdr['model']!r} != contract {model!r}")
    if hdr.get("status") == "ok":
        if not body.strip():
            f.append("status ok but the body is empty")
        ev = hdr.get("evidence")
        if ev and root is not None and not (root / ev).exists():
            f.append(f"evidence path {ev!r} does not exist")
    return f, body, hdr


def check_digest(text: str, max_lines: int):
    f = []
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) > max_lines:
        f.append(f"digest has {len(lines)} non-empty lines, cap is {max_lines}")
    for h in DIGEST_HEADINGS:
        if f"**{h}" not in text:
            f.append(f"digest has no '**{h}' part")
    return f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--kind", choices=["result", "digest"], default="result")
    ap.add_argument("--node"); ap.add_argument("--attempt"); ap.add_argument("--model")
    ap.add_argument("--root"); ap.add_argument("--max-lines", type=int, default=20)
    ap.add_argument("--summary", type=int, default=0)
    a = ap.parse_args()
    p = Path(a.file)
    if not p.is_file():
        print(f"fail {a.file}: file does not exist")
        return 1
    text = p.read_text(errors="replace")
    if not text.strip():
        print(f"fail {a.file}: file is empty")
        return 1
    if a.kind == "digest":
        f = check_digest(text, a.max_lines); body = ""
    else:
        f, body, _ = check_result(text, a.node, a.attempt, a.model, Path(a.root) if a.root else None)
    if f:
        print(f"fail {a.file}: " + "; ".join(f))
        return 1
    print(f"ok {a.file}")
    if a.summary and body:
        print("\n".join(body.splitlines()[: a.summary]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
