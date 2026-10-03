# Exploration — dispatch.py, where an engine's working folder is decided
Produced 2026-10-03 by the COO (small area, whale rule). Question asked: where does the dispatcher set the folder an
engine runs in, and what else resolves against that folder? Commit explored: db1fad2.

| id | Claim | Kind | Source | Quote | Evidence |
|---|---|---|---|---|---|
| X1 | Engine processes run with the repo root as their folder | read | .claude/skills/workflow-design/scripts/dispatch.py:209 | `code, stdout, stderr = run_group(cmd, node["outer_timeout_s"], base)` | — |
| X2 | run_group starts the process with that folder as cwd | read | .claude/skills/workflow-design/scripts/dispatch.py:166 | `def run_group(cmd: list[str], timeout: float, cwd: Path)` | — |
| X3 | The Codex adapter also passes the folder as `-C` | read | .claude/skills/workflow-design/scripts/dispatch.py:135 | `"-C", str(cwd), "-o", str(out_file)]` | — |
| X4 | build_command receives the repo root as that folder | read | .claude/skills/workflow-design/scripts/dispatch.py:197 | `cmd = build_command(node, engine, model, prompt, out_file, base, attempt)` | — |
| X5 | The brief is read relative to the repo root | read | .claude/skills/workflow-design/scripts/dispatch.py:192 | `prompt = (base / node["brief"]).read_text()` | — |
| X6 | Check commands run from the repo root | read | .claude/skills/workflow-design/scripts/dispatch.py:257 | `cwd=base)` | — |
| X7 | A fallback copies the node and overrides it with the fallback's fields | read | .claude/skills/workflow-design/scripts/dispatch.py:292 | `target = {**target, **fb, "id": node["id"], "fallback": None}` | — |
| X8 | qwen run from the repo root loaded the project's context: about 198k tokens for a one-line answer | ran | runs/20261003-dispatch-canary/README.md:25 | `run from the repo root, qwen loads the project's context` | runs/20261003-dispatch-canary-qwen/raw/canary-qwen-1-qwen.stdout (usage.total_tokens 197871) |

## Impact map (4 items, TASK_TYPES case C)
- **Where the change goes:** the engine's cwd at X1/X2/X4 and Codex's `-C` at X3 — one new node field.
- **What calls it / what it calls:** `call()` → `build_command()` and `run_group()`; `run_node()` builds fallbacks (X7).
- **Nearby conventions:** plan fields validated in `check_plan`; paths relative to the repo root; tests drive fake engines.
- **Must not change:** briefs (X5), result files and check commands (X6) keep resolving against the repo root; a node
  without the new field behaves exactly as before; other scripts and `ancient_games/`.

## Gaps
X8 is the only `ran` claim; X1–X7 are `read`, and the build will run them through the verifier's cases.
