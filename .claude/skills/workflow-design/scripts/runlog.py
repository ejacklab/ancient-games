#!/usr/bin/env python3
"""runlog.py — the run-written part of the feedback log (method 3.8; docs/research/20261002-workflow-feedback,
option B, minimal). Appends one JSON object per line to runs/<run>/events.jsonl. Stdlib only, no model calls.

Two commands:
  exec     wrap one engine call:  runlog.py exec --run R --node N --attempt K --engine codex -- codex exec ...
           Writes a start and an end event (exit code, duration, status ok|fail|timeout). The command's stdout and
           stderr go to runs/<run>/raw/ (gitignored), never into events.jsonl. The harvester later joins the
           engine's own records (e.g. a codex rollout) to this call by its time window and cwd.
  verdict  one line per node check: runlog.py verdict --run R --node N --round K --check NAME --pass yes|no

Public-repo rule: events carry ids, numbers, paths and status only, never prompt or response text.
Exit: exec returns the wrapped command's exit code (124 on --timeout); verdict 0; 2 on usage errors.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from engines import REGISTRY as _ADAPTERS   # same folder: a script run puts it on sys.path, and dispatch.py
                                            # inserts it there before importing this module

# The engines `--engine` may name are the CLI adapters dispatch.py can actually run, plus the two Claude Code
# provenance labels. Those two are not adapters: they say WHO ran a node (the COO herself or a subagent), and no
# command line builds them. Deriving the rest means a new adapter is never a second edit here.
ENGINES = ["claude-main", "claude-sub", *sorted(_ADAPTERS)]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def append(run_dir: Path, event: dict) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    with open(run_dir / "events.jsonl", "a") as f:   # one short line per write; one writer at a time (method 4)
        f.write(json.dumps(event, sort_keys=True) + "\n")


def cmd_exec(a) -> int:
    if not a.cmd:
        print("runlog exec: no command after --", file=sys.stderr)
        return 2
    run_dir = Path(a.runs_root) / a.run
    raw = run_dir / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    stem = f"{a.node}-{a.attempt}-{a.engine}"
    base = {"run_id": a.run, "node_id": a.node, "attempt": a.attempt, "engine": a.engine,
            "model": a.model, "cwd": os.getcwd(), "brief_variant": a.brief_variant}
    append(run_dir, {**base, "event": "start", "ts": now()})
    t0 = time.monotonic()
    status, code = "ok", 0
    with open(raw / f"{stem}.stdout", "w") as out, open(raw / f"{stem}.stderr", "w") as err:
        try:
            code = subprocess.run(a.cmd, stdout=out, stderr=err, timeout=a.timeout).returncode
            status = "ok" if code == 0 else "fail"
        except subprocess.TimeoutExpired:
            status, code = "timeout", 124
        except OSError as e:
            err.write(f"runlog: could not start command: {e}\n")
            status, code = "fail", 127
    append(run_dir, {**base, "event": "end", "ts": now(), "status": status, "exit_code": code,
                     "duration_ms": int((time.monotonic() - t0) * 1000),
                     "raw_stdout": str(raw / f"{stem}.stdout"), "raw_stderr": str(raw / f"{stem}.stderr")})
    return code


def cmd_verdict(a) -> int:
    append(Path(a.runs_root) / a.run, {"run_id": a.run, "node_id": a.node, "round": a.round, "event": "verdict",
                                       "ts": now(), "check": a.check, "pass": a.passed == "yes"})
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs-root", default="runs")
    sub = ap.add_subparsers(dest="command", required=True)
    e = sub.add_parser("exec")
    e.add_argument("--run", required=True); e.add_argument("--node", required=True)
    e.add_argument("--attempt", type=int, default=1); e.add_argument("--engine", required=True, choices=ENGINES)
    e.add_argument("--model"); e.add_argument("--brief-variant")
    e.add_argument("--timeout", type=float, help="outer timer in seconds (method 3.8)")
    e.add_argument("cmd", nargs=argparse.REMAINDER)
    v = sub.add_parser("verdict")
    v.add_argument("--run", required=True); v.add_argument("--node", required=True)
    v.add_argument("--round", type=int, default=1); v.add_argument("--check", required=True)
    v.add_argument("--pass", dest="passed", required=True, choices=["yes", "no"])
    a = ap.parse_args(argv)
    if a.command == "exec":
        if a.cmd and a.cmd[0] == "--":
            a.cmd = a.cmd[1:]
        return cmd_exec(a)
    return cmd_verdict(a)


if __name__ == "__main__":
    sys.exit(main())
