# Report — memory-check (run 20261017-memory-check)

**A TypeScript tool that checks a project's memory against the source-of-truth and caches guidelines, built through
research, implementation, tests, review and an enhance round, each by a different engine; 74 tests pass. The method
runs it once in 3.1 Readiness.**

## The project — `memory_check/`
`AGENTS.md`, `VISION.md`, `USE_CASES.md` (U1–U6), `REQUIREMENTS.md` (find, check, report, tests), `src/` (12 modules,
`cli.ts` a launcher that keeps bun's cache off), `guidelines/` (the tool's own copy), `test/` (74 tests).
Run: `bun memory_check/src/cli.ts --project <repo root> [--out FILE] [--warn] [--home DIR] [--since REV]`.

## How it was made
| Phase | Who | Result |
|---|---|---|
| Research | six experts (`research-q/`) | 16 open questions, the main agent's picks applied (`design-decisions.md`) |
| Implement | opencode (`nodes/implement.*`) | v1, tsgo clean |
| Test | Codex, from the spec only (`test/acceptance.test.ts`) | 55 tests: 3 showed the spec wrong (corrected), 8 tool bugs fixed by opencode (`fix-1`) |
| Review | Codex, read only (`nodes/review.codex.md`; dsh returned nothing) | 14 findings, each a test red first (`test/review.test.ts`), fixed by opencode (`fix-2`, attempt 2) |
| Enhance | six experts (`enhance-q/`) | picks applied: could-not-run MUSTs in the warning, unstaged count, final Not applicable section (`test/enhance.test.ts`, `fix-3`); the hook speaks only where `project-memory/` exists |
| Placement | six experts (`placement-q/`) | unanimous: once in 3.1 Readiness, not per node — written into the method |

## On this repo
`nodes/smoke-report.md`: 0 fail, 3 pass, 3 needs a reviewer, 72 not applicable (no `project-memory/`), 0 could not run;
the warning is empty; exit 0. Fixtures only: no real project with `project-memory/` has been checked.

## Open for EJ
- The session-start hook: `settings-diff.md`, waiting for your yes.
- A real project with `project-memory/` to calibrate on, if there is one.
- Claude Code's `~/.claude/projects/*/memory/` is not the guidelines' agent memory (`~/.claude/agent-memory/`): a
  guideline question, reported, not changed.
- The experts' proposed method change (a question trials cannot answer goes to you at once): yours, not applied.
- The crossed-check workflow's fixed 580 s per engine call was too short for Codex writing 55 tests.

## Failures along the way (evidence, R12.2)
opencode stopped twice on an auto-rejected absolute path (the opencode lesson now says so); dsh returned no review;
the experts' first ask ran before its question file existed (launched in the same step as the write).
