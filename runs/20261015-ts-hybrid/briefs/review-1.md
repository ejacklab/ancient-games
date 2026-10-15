# Brief — independent review, round 1 (read-only)

You are reviewing a build you did not write the code of. The current folder is a git worktree on branch
`feat/ts-hybrid`. Read only; change nothing; do not run git commands that change the repository.

## What was built

`tools/harness-guard/` — a bun TypeScript package, the code half of a "harness health" hybrid: checks that need no
judgment run at fixed points (Claude Code hooks, an opencode plugin, a CLI), so an agent cannot skip them once
installed. Spec: `tools/harness-guard/SPEC.md`. Shared types: `src/types.ts`. Catalogues: `data/*.yaml`. Modules:
`src/traps.ts` (M1), `src/journal.ts` (M2), `src/insight.ts` (M3), `src/register.ts` (M4), `src/hooks.ts`,
`src/plugins/opencode.ts`, `src/install.ts`, `src/doctor.ts`, `src/cli.ts` (M5). Tests in `test/`. Code by opencode
(MiniMax), tests mostly by Codex, M3's first tests by opencode. Also one Python fix:
`.claude/skills/workflow-design/scripts/dispatch.py` (a result whose own header says `status: fail` or `partial` now
blocks the node) with its test in `tests/test_dispatch.py`.

The requirements it serves are in `runs/20261015-ts-hybrid/requirements-context.md` (R11–R13). The design and its
acceptance criteria AC1–AC8: `runs/20261015-ts-hybrid/workflow-design-context.md`.

## Task

Find **defects**: places where the code does not do what SPEC.md, R11–R13 or AC1–AC8 say, where a check cannot fail,
where a secret or raw command/prompt text can leak into output, the journal or evidence, where a hook could freeze the
agent (exit 2 from a crash, an endless block with no way out but the harness cap), where a hook could block correct work
(false deny), where a payload of an unexpected shape crashes the handler, and where a test passes for the wrong reason.
Read the code and tests. Your sandbox is read-only, so you cannot run the tests: the COO's run of the full suite and
the typecheck is in `runs/20261015-ts-hybrid/nodes/review-context-tests.txt`.

Not wanted: style, naming, refactors, "could also" features.

## Template — the body of your result

First line: the verdict in one sentence. Then a table, most severe first:

| # | Severity (high/medium/low) | File:line | Defect (what is wrong) | Failing input (concrete) | Requirement / AC it breaks |
|---|---|---|---|---|---|

Then: "Checked and fine:" — one line per area you checked and found no defect in. Then: "Not checked:" — what you
could not check and why.

## Standard

Each defect names a concrete input that shows it (a payload, a command string, a file) and the line responsible. A
defect you could not show with an input is listed as "suspected" with its reason. No invented requirements.

## Your final message is the result

It is saved as `runs/20261015-ts-hybrid/nodes/review-1.result.md`. Start it with this header:

```
---
node: review
attempt: 1
engine: codex
model: <as reported>
status: ok
started: <UTC>
ended: <UTC>
evidence: runs/20261015-ts-hybrid/nodes/review-context-tests.txt
---
```
