# Readiness — 20260920-readme-test-count

Anything marked missing becomes a preparation piece at the front of the flow.

All commands below were run in this session on 2026-09-20 at HEAD `4a0c94b`, from `/home/smoke01/dev/ancient-games`.

## Tools

Run each one; do not assume.

| Tool | Needed for | Command that proved it works | Result (works / missing) |
|---|---|---|---|
| python3 | Running the suite the way README.md:33 says to | `python3 --version` → `Python 3.12.3` (`/usr/bin/python3`; no `.venv` or `venv` in the repo) | works |
| pytest | Getting the real count | `python3 -m pytest --version` → `pytest 9.0.2`; `python3 -m pytest --collect-only -q` → `379 tests collected in 0.09s`; `python3 -m pytest -q -p no:cacheprovider` → `379 passed in 6.90s` (7.5 s wall clock) | works |
| grep | Finding every place README.md states the count | `grep -n -i "passed\|xfail\|pytest" README.md` → lines 20, 26, 33, 36; `grep -rn "68 passed"` over `*.md *.py *.toml *.cfg` → only `README.md:33` | works |
| git | Baseline, confirming only README.md changes, the diff for review | `git status --short` (baseline in state.md); `git log -1 --format='%h %ad %s' --date=short -- README.md` → `61d4cc9 2026-09-07 …`; `git --version` → `2.43.0` | works |
| date | State log lines | `date +%F` → `2026-09-20` | works |

Side effect check: `git status --short` after the full pytest run was identical to the baseline (`__pycache__/` and
`.pytest_cache/` are in `.gitignore`).

Present but not needed: `uv` (`/home/smoke01/.local/bin/uv`, located with `which` only, not run).

## Skills that apply

| Skill | What it covers here |
|---|---|
| challenge-mediation | Typing the challenge and its cost of being wrong before work starts; it is the source of "Split iff it changes the route" that method §3.4 uses for the size decision |

Looked at and not applicable: `enhance-ancient-games` (plans enhancements from `20260919-state.md`, not a doc
correction), `verify-extraction` (the README line can be read in full in under a minute), `agent-loop` (no
`agent-loop.json` in this repo), `formalization` (the problem is already precisely stated).

## Information

| What is needed | Where it is | Structure (state file / map / md hierarchy / memory folder / journal or index / graph / web / none) | Verified against the source? | Which agents and tools can read it |
|---|---|---|---|---|
| The stale claim and its exact text | `README.md:33` — `python3 -m pytest -q          # 68 passed, 0 xfailed` | md file, one line, tracked, unmodified in the working tree | Yes — read in this session; `grep -rn "68 passed"` finds no other occurrence | Any agent or tool that can read repo files |
| Other README sentences about the suite | `README.md:26` — "No test is xfailed."; `README.md:19-21` — "eight trace test cases … nine lints run as a pytest suite" | md file | Line 26: yes — the full run printed `379 passed` with no xfailed, skipped or failed figure; the only `xfail` hit in `tests/` and `ancient_games/` is a docstring (`tests/test_interface_fixes.py:4`). Lines 19-21: not checked (not a count of pytest tests) | Any agent or tool that can read repo files |
| The real current count | Not stored anywhere reliable; produced by `python3 -m pytest -q` | none — a command result | Yes, for this session and this environment: `379 passed in 6.90s` at `4a0c94b` with the untracked files in the baseline present | Any agent with Bash, python3 and pytest 9.0.2 (installed at user level in `~/.local/bin`, so not tied to a venv) |
| What pytest collects | `pyproject.toml` — `testpaths = ["tests"]`; 25 `test_*.py` files in `tests/` (`ls tests/test_*.py | wc -l`); untracked `tests/workflows/` holds only `intake_harness.mjs` | config file | Yes — read `pyproject.toml`, listed `tests/` and `tests/workflows/`; the `.mjs` file is not collected | Any agent or tool that can read repo files |
| Environment sensitivity of the count | `PROJECT_OVERVIEW.md:403-410` — with `NO_COLOR` set: `378 passed, 1 failed`; with `env -u NO_COLOR`: `379 passed` | md file | Partly — `NO_COLOR` is unset in this session and 379 passed; the 378/1 case was not reproduced here | Any agent or tool that can read repo files |
| Earlier recorded baselines | `20260919-plan-critic-issues.md:8` (379 passed, 0 failed, 0 skipped); Claude Code auto-memory `ancient-games-house-rules.md` (379 passed at `4a0c94b`) | md file; memory folder | Yes — both agree with this session's run | The md file: any agent. The auto-memory: Claude Code only |
| Dated counts in other docs (282, 318, 351, 363, 370) | `docs/AUTONOMY_REVIEW.md:3`, `docs/AUTONOMY_DESIGN.md:242`, `docs/INTERFACE_FIXES_IMPL.md:6`, `docs/DKIND_MIRROR_RESEARCH.md:3`, `docs/ABLATION_4_IMPL.md:6`, `docs/ABLATION_4.md:3`, `docs/ABLATION_4_DESIGN.md:4`, `docs/research/INTERFACE_CONTRARIAN.md:3` | md hierarchy, no index | Located by grep only; each is tied to a named commit, and the challenge names README.md only | Any agent or tool that can read repo files |
| House rule on running the suite | Claude Code auto-memory `ancient-games-house-rules.md`: run the suite and commit as separate steps | memory folder | Read in this session; not written in any repo file | Claude Code only |

## Missing or unverified

| Item | Effect on the flow (organise piece / verify piece / research piece / export to a file) |
|---|---|
| The count is a command result, not stored knowledge: it changes with every added test and with the `NO_COLOR` environment variable, so the 379 recorded here is dated 2026-09-20 / `4a0c94b` and must be taken again by whoever edits the README, in the same session as the edit | verify piece |
| Whether the replacement keeps the `, 0 xfailed` suffix: pytest prints no xfailed figure when there are none (output was `379 passed in 6.90s`), so the suffix is README wording, not pytest output | ask EJ (decision; goes to step 2's question batch with a provisional assumption) |

No tool is missing. No information is missing or readable by one tool only, except the two auto-memory items above,
which are not required to do the task.
