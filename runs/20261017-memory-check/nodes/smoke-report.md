# memory-check — snapshot: files: the staged state (git index, stage 0), the view `tools/memory_index.py --check` reads; history: no commits touch project-memory/: no history range to check — project: /home/smoke01/dev/ancient-games

Guidelines this report is checked against (the tool's own copy, C1): SOURCE_OF_TRUTH_REQUIREMENTS.yaml 26226965112c, CACHES.md 8eef3b46f3f2
Records: 64 from SOURCE_OF_TRUTH_REQUIREMENTS.yaml (SoT:), 11 Core requirements from CACHES.md (CACHES:).

## Memory locations (F1, F2)

| location | path | state |
|---|---|---|
| AGENTS.md | `/home/smoke01/dev/ancient-games/AGENTS.md` | present |
| CLAUDE.md | `/home/smoke01/dev/ancient-games/CLAUDE.md` | present |
| project-memory/INDEX.md | `/home/smoke01/dev/ancient-games/project-memory/INDEX.md` | absent |
| project-memory/entries/ | `/home/smoke01/dev/ancient-games/project-memory/entries` | absent |
| project-memory/work/ | `/home/smoke01/dev/ancient-games/project-memory/work` | absent |
| project-memory/journal/ | `/home/smoke01/dev/ancient-games/project-memory/journal` | absent |
| project-memory/.cache/ | `/home/smoke01/dev/ancient-games/project-memory/.cache` | absent |
| agent memory (<home>/.claude/agent-memory/<name>/) | `/home/smoke01/.claude/agent-memory` | absent |

## The tool's own requirements

- **F1** (MUST) — pass — /home/smoke01/dev/ancient-games/AGENTS.md exists; 2 of 8 named locations present, 6 absent
- **F2** (MUST) — pass — project /home/smoke01/dev/ancient-games is the root of a git repository (git rev-parse --show-toplevel in it)
- **F3** (MUST) — pass — this run created, changed and deleted nothing; it wrote only /home/smoke01/dev/ancient-games/runs/20261017-memory-check/nodes/smoke-report.md; every git call ran with GIT_OPTIONAL_LOCKS=0

## Results — MUST

- **SoT:K4.1** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:K4.3** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:K6.1a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:K6.2** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:K6.3a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd1.2** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd2.3a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd3.1a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd4.1** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd5.1** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd5.2** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd5.3** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd6.1** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W1.1a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W1.1b** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W1.2a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W1.3a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W3.2** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W3.3a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W3.5a** (MUST) — needs a reviewer — check: reviewer — whether the project holds user memory or agent memory is the owner's call (F1 reports the locations; it does not judge what is in them)
- **SoT:W4.1b** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W4.1c** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W5.3b** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W6.1a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W6.3a** (MUST) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)

## Results — SHOULD

- **SoT:K1.1** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:K5.1** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:K5.2** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:K6.1b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:K6.3b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd1.1** (SHOULD) — needs a reviewer — check: reviewer — user and agent memory live in the home folder, and whether that layout has a written reason is the owner's
- **SoT:Rd2.1** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd2.2** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd2.3b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd4.4** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd4.5b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W1.1c** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W1.2b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W1.3b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W2.1b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W2.2b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W3.1** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W3.3b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W3.4** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W3.5b** (SHOULD) — needs a reviewer — check: reviewer — where user and agent memory live, and whether a reason is written, is the owner's
- **SoT:W3.6** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W4.2** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W5.1** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W5.2** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W5.3a** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W6.1b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W6.2** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W6.3b** (SHOULD) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)

## Results — guidance

- **SoT:K4.2** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd3.1b** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd4.2** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd4.3** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd4.5a** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd5.4** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:Rd5.5** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W2.1a** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W2.2a** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W4.1a** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)
- **SoT:W4.3** (guidance) — not applicable — project-memory/ is absent (F1 reports it absent), so the memory this record is about is absent (C4)

## Results — CACHES.md Core requirements (no level in CACHES.md)

- **CACHES:B1** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:B2** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:B3** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:B4** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:B5** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:K1** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:K2** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:K3** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:Rd1** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:Rd2** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)
- **CACHES:Rd3** (not stated in CACHES.md) — not applicable — project-memory/.cache/ is absent (F1 reports it absent), so the cache requirements are not applicable (C4, C6)

## Needs a reviewer

- **SoT:W3.5a** (MUST) — fails if: the project holds user memory or agent memory. — why not the tool: check: reviewer — whether the project holds user memory or agent memory is the owner's call (F1 reports the locations; it does not judge what is in them)
- **SoT:W3.5b** (SHOULD) — fails if: they live elsewhere, with no written reason. — why not the tool: check: reviewer — where user and agent memory live, and whether a reason is written, is the owner's
- **SoT:Rd1.1** (SHOULD) — fails if: these live elsewhere or are laid out otherwise, with no written reason. — why not the tool: check: reviewer — user and agent memory live in the home folder, and whether that layout has a written reason is the owner's

## Notes from tools/memory_index.py

- `nothing to check: no project-memory/ in the staging area`

## This run

- Report written to /home/smoke01/dev/ancient-games/runs/20261017-memory-check/nodes/smoke-report.md
- Read only: nothing was created, changed or deleted except the report; every git call used GIT_OPTIONAL_LOCKS=0 (F3)
- The session-start hook is not installed: R2 leaves that harness change to the owner (R12.3)
- Not calibrated on a real project: no project has been named to calibrate against (design-decisions.md 15)
- Counts: 0 fail, 3 pass, 3 needs a reviewer, 72 not applicable, 0 could not run
- CACHES.md gives its requirements no level, so none of them gates the exit code (R3 counts MUSTs only)
