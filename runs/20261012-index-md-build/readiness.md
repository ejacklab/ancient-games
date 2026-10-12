# Readiness — 20261012-index-md-build

Run 2026-10-12 by the COO. Anything marked missing becomes a preparation piece at the front of the flow (N0).

## Tools

| Tool | Needed for | Command that proved it works | Result |
|---|---|---|---|
| python3 3.12.3 | the script, the tests | `readiness.py` → `python3 --version` | works |
| git 2.43.0 | `ls-files -z`, `cat-file --batch`, worktree, hooks | `readiness.py` → `git --version` | works |
| pytest | baseline, N1–N5 checks | `env -u NO_COLOR python3 -m pytest -q` → 529 passed in 31.61 s | works |
| codex-cli 0.160.0 | N1 (and N2's exit) | `codex --version` | installed; **canary not run** → N0 |
| opencode 1.18.34 | N2 | `opencode --version` | installed; **canary not run** → N0; effort flag unknown (U4) |
| claude 2.1.296 | N4 subagent | `readiness.py` → `claude --version` | works (this session) |
| `feature_gate.py` | N2's check | read its docstring; `baseline`/`check` subcommands | present; **not run yet** → N0 |
| `workload.py` | engine split | ran on 1- and 2-module plans | works; result → Q2 |
| `runlog.py`, `harvest_run.py` | feedback record | `runlog.py --help` | present |

## Skills that apply

| Skill | What it covers here |
|---|---|
| workflow-design | this design |
| requirement-check | any rule written into the spec while building (none planned) |
| meaningful-names | names in the script, judged at N4 item 7 |

## Information

| What is needed | Where it is | Structure | Verified against the source? | Who can read it |
|---|---|---|---|---|
| Vision, requirements, design | `docs/index-md/*.md` (untracked) | md hierarchy, ids B/C/G | read in full by the COO, 2026-10-12 | every engine, by absolute path |
| Why each fix exists | `runs/20261012-index-md-algorithm/reviews/` | reviews + summary | summary read | COO only (not given to workers) |
| Entry format | `docs/memory-system/SOURCE_OF_TRUTH.md` W1.1–W1.3 | md | lines read | COO; workers get it through REQUIREMENTS B2 |
| Size example | `docs/memory-system/CACHES.md:519` | md table | quoted | COO |
| House style for a tool | `tools/export_skills.py`, `tests/test_skills_export.py` | code | read | every engine |

## Blueprint

- Product: the INDEX.md generator. Map: none; spec in `docs/index-md/`.
- Kind of task: **feature**, because it adds a tool and tests to the repo.

| Section | Needed? | Status for this task | File | Effect |
|---|---|---|---|---|
| vision | yes | draft | `docs/index-md/VISION.md` | question for EJ (Q1) |
| requirements | yes | draft | `docs/index-md/REQUIREMENTS.md` | question for EJ (Q1) |
| domain model | no | — | — | none: the entry format is in requirements B2 |
| business logic | yes | draft | `docs/index-md/DESIGN.md` (the algorithm) | Q1 |
| architecture | yes | draft | `docs/index-md/DESIGN.md` (files, hooks) | Q1 |
| data model | no | — | — | none: no store |
| ui/ux | no | — | — | none: CLI output is in C1.2 |
| non-functional | yes | draft, one part open | `REQUIREMENTS.md` B4 | Q1; the limits stay example constants |

## Missing or unverified

| Item | Effect on the flow |
|---|---|
| codex and opencode canaries | N0 runs one each |
| opencode effort flag (U4) | N0 canary |
| `docs/index-md/` is untracked, so a worktree from HEAD lacks it | briefs use main-tree paths; hashes pinned |
| another session is still reviewing the requirements | pinned hashes; recheck at N5; a change is a stop |
