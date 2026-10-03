# Brief — verifier, phase 1: blind acceptance cases for the per-node working folder

You have not seen and must not read the implementation (`dispatch.py`) or its tests. Work from the criteria and the
interface below only. Do not use any tools; answer from this brief alone.

## Task (one deliverable)
Write a pytest file, `tests/test_dispatch_workdir.py`, with one or more tests per criterion R1–R7.

## Acceptance criteria (each with an example)
- R1 A node with `"workdir"` runs its engine with that folder as its working folder. Example: a script node whose
  command prints `os.getcwd()`, with `"workdir": "w/q"`, records a result containing `<root>/w/q`.
- R2 A relative `workdir` resolves against `--root`, and a missing folder is created. Example: `w/new` absent before
  the run exists after it.
- R3 A node without `workdir` runs in the repo root, as before. Example: the printed folder equals `<root>`.
- R4 The Codex adapter's `-C` names the node's working folder. Example: `--dry-run` on a codex node with
  `"workdir": "w"` prints `-C <root>/w`.
- R5 The brief, the result file and check commands still resolve against the repo root. Example: a node with
  `"workdir": "w"`, brief `brief.md` at the root and a check `python3 check.py {result}` with `check.py` at the root
  runs and passes; its result file is under `runs/<run_id>/nodes/`.
- R6 A fallback without its own `workdir` keeps the node's; a fallback with one uses it. Example: node `"a"`,
  fallback `"b"` → the fallback call runs in `<root>/b`.
- R7 `dispatch.py check` refuses a `workdir` that exists as a file. Example: `"workdir": "x.txt"` with `x.txt` a file →
  a refusal naming the node and saying it is not a folder.

## Context — the dispatcher's interface (this is all you need)
- Run it as `[sys.executable, str(SCRIPT), "--root", str(root), "run", str(plan_path)]` (or `"check"` instead of
  `"run"`; add `"--dry-run"` after the plan path for a dry run). In your file define
  `SCRIPT = Path(os.environ.get("DISPATCH_SCRIPT", str(Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts/dispatch.py")))`
  — the env var is required: the run checks your cases against the old version through it.
- Exit codes: `run` 0 all done, 1 stopped (a blocked node), 2 plan refused; `check` 0 ok, 1 refused, printing
  `plan refused:` and one line per problem naming the node id.
- Plan file (JSON): `{"run_id": "r1", "nodes": [ ... ]}`. A local-command node:
  `{"id": "n", "role": "worker", "engine": "script", "outer_timeout_s": 30, "passback": false, "cmd": [...], "workdir": "w"}`.
  With `"passback": false` the command's stdout becomes the node's result file, saved at
  `<root>/runs/<run_id>/nodes/<id>-<attempt>.result.md`; `<root>/runs/<run_id>/dispatch.json` holds
  `{"nodes": {"<id>": {"status": "done", "result": "<path>", ...}}}`.
- A check: `"check": {"name": "c", "cmd": [...]}` runs after the node; `{result}` in it is replaced by the result
  file's path; exit 0 passes.
- A fallback: `"fallback": {"engine": "script", "cmd": [...], "workdir": "b"}` replaces the node's call once when the
  first call fails (a non-zero exit is a failure).
- A Codex node (for `--dry-run` only, never really run): `{"id": "c", "role": "coder", "engine": "codex",
  "model": "m", "brief": "brief.md", "inner_timer": "60s", "outer_timeout_s": 70, "workdir": "w"}`; the brief file
  must exist and contain the headings `## Template`, `## Example` and `## Standard`. `--dry-run` prints one line
  per node: `[dry-run] <id> attempt 1: <the command line>`.
- Use pytest's `tmp_path` as the root. No network, no real engines.

## Template
Your body: one ```python code block holding the whole test file, and nothing else after it.

## Example
```python
import json, os, subprocess, sys
from pathlib import Path

SCRIPT = Path(os.environ.get("DISPATCH_SCRIPT", str(Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts/dispatch.py")))

def test_r3_no_workdir_runs_in_the_root(tmp_path):
    plan = {"run_id": "r1", "nodes": [{"id": "n", "role": "w", "engine": "script", "outer_timeout_s": 30,
            "passback": False, "cmd": [sys.executable, "-c", "import os; print(os.getcwd())"]}]}
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(tmp_path), "run", str(tmp_path / "plan.json")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    st = json.loads((tmp_path / "runs/r1/dispatch.json").read_text())
    assert Path(st["nodes"]["n"]["result"]).read_text().strip() == str(tmp_path)
```

## Standard
- Every criterion R1–R7 has at least one test whose name starts `test_r<N>_`.
- The cases must **fail** against the old dispatcher (which has no `workdir`) and pass against a correct one; the run
  checks the first automatically.
- Assert on observable behaviour only (exit codes, the result file, `dispatch.json`, printed lines), never on code.
