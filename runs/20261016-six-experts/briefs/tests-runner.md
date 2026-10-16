# Brief — tests-runner

You work in a git worktree; the current folder is the repository root. Work only inside it.

## Task
Write tests for the six-experts runner in `tests/test_six_experts.py` (pytest), from
`.claude/skills/six-experts/SKILL.md` and `runs/20261016-six-experts/plan.md` (and `state.md` decisions D1, D2). Load
the script as `tests/test_six_experts_codex_quota.py` does (importlib from
`.claude/skills/six-experts/scripts/six_experts.py`). Mock every engine: never start a real AI engine; replace
`start`/`subprocess.Popen` or put fake executables on PATH. Do not change the script.

What the skill promises, each a test:
- The Claude command keeps the prompt as its last argument and passes the tools as one `--allowedTools=...` argument.
- Dave and Dario run on the same model, `claude-sonnet-5-5`.
- Dario's brief holds the question and the five answer sections, and no list, identity, "Load first" or insight path.
- Dave's brief has "Load first: what was learned", the index path and the categories named with `--insights`; with
  none named it says he chooses from the index; the index and sections files are written into the run's `seats/`
  (mock the guard call: `guard_text`).
- `check`: Dario passes on the five sections alone; Dave fails when he cites an `F-xxxxxxxx` id not in his index, and
  when he cites none without "No insight applies"; he passes when he cites an id from the index.
- Two experts on opencode are never running at the same time (the second waits for the first).

## Pieces and progress (first)
Before starting, append one `planned` line per piece to `runs/20261016-six-experts/nodes/tests-runner.progress.md`,
then a line as each starts and ends: `- <ISO time from date -Iseconds> · <piece id> · <planned|start|done|fail> · <note>`

## Standard
`env -u NO_COLOR python3 -m pytest -q tests/test_six_experts.py` — report the counts.

## Limits
May change: the test file, the progress file and your result file only. Do not commit. No other AI engine.
Stop by 15:45 +0800.

## Result
`runs/20261016-six-experts/nodes/tests-runner.result.md`: `status: done|partial|fail`, one sentence; files; commands and
last lines; CONTRADICTS (with the line in SKILL.md or plan.md) or none.
