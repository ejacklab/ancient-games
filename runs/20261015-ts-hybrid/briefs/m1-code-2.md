# Brief — m1-code, attempt 2

You are working in a git worktree; the current folder is the repository root. Work only inside it.

## Task (one deliverable)

Implement module M1 (traps, engine-call recognition, result check) in `tools/harness-guard/src/traps.ts` so that its acceptance tests pass. The tests in
`tools/harness-guard/test/traps.test.ts` were written by a different engine from SPEC.md and are frozen: you must not change them.

## Context (only what this task needs)

- `tools/harness-guard/SPEC.md` — the specification. Read the **Common** section and the **M1** section in full.
- `tools/harness-guard/src/types.ts` — the shared types. Fixed: import them, never redefine or change them.
- `tools/harness-guard/data/traps.yaml`, `tools/harness-guard/data/engines.yaml` — the catalogues (read-only).
- Runtime: bun 1.4.3, TypeScript, **no npm dependencies** (`bun:test`, `Bun.YAML.parse`, `node:*` modules only).
- Style: match `tools/harness-guard/src/types.ts` — short comments, plain names.
- Withheld on purpose: nothing — but the tests' author's reasoning is not given; the tests and SPEC.md are the whole contract.

## Feedback from the previous attempt (the check's real output)

This is a **repair round** caused by a measurement, not by your tests being wrong. The COO replayed 3,677 past Bash
commands from this project through M1 as first built: 37 denies, **31 false**. The lint read the whole Bash string, so
it fired on `codex exec --help`, on `pgrep -f "codex exec"`, on `grep` patterns and `echo` text naming an engine, on
heredoc bodies that mention `opencode run`, and on absolute paths belonging to another command on the same line
(e.g. `python3 …/runlog.py --runs-root /abs/runs exec … -- opencode run "…"`). Six denies were real: `codex exec`
with no stdin redirect, two inside a backgrounded `( … ) &` group.

SPEC.md's M1 section now has a **Segments** part (read it in full) and new Fails-if lines; `data/*.yaml` regexes are
now anchored to the command word (`^(?:\S*/)?codex…`). Also still missing from the first tests: a **proposed result
trap** must produce no finding in `checkResult` (SPEC: "each approved **result** trap").

For the test writer: keep every existing test that still matches SPEC.md; change only tests the new SPEC contradicts
(say which, and why, in the result); add tests for every new Fails-if line and for `segments()` (heredoc removal,
quotes, `2>&1` not a separator, background of a `( … ) &` group, wrapper stripping incl. `runlog.py … --`, `--help`).
Use planted command strings shaped like the false denies above — never real paths from this machine.


## Standard (how it will be judged)

- `cd tools/harness-guard && bun test` — every test passes (all modules built so far, not only yours).
- `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` — exit 0, no type errors.
- Behaviour follows SPEC.md, not only the tests: where a test and SPEC.md disagree, do not bend the code to the test —
  stop and report it under CONTRADICTS with the test name and the SPEC line.
- No secret or raw command/prompt text in anything the module writes or prints (the tests plant `SECRET-PLANT-7f3a9c`).
- No new dependency; no change to `package.json`, `tsconfig.json`, `SPEC.md`, `src/types.ts`, `data/`, or any test.

The COO will re-run every check you report, and will plant wrong inputs of its own.

## Limits

- May change: `tools/harness-guard/src/traps.ts` only (and new helper files under `src/` that only it imports); plus the result and evidence files below.
- Must not change: anything else. Do not commit; do not run `git` commands that change the repository.
- Do not start any other AI engine or agent. Do not read or print files outside the repository.

## Write the result to

Write the result file `runs/20261015-ts-hybrid/nodes/m1-code-2.result.md` (write to `m1-code-2.result.tmp` first, then
rename it). It starts with this header, then the body:

```
---
node: m1-code
attempt: 2
engine: opencode
model: <the model as your tool reports it>
status: ok | fail | partial
started: <UTC time>
ended: <UTC time>
evidence: runs/20261015-ts-hybrid/nodes/m1-code-2.evidence.txt
---
<first line: the answer in one sentence>
- Files written: <paths>
- Check: <the command you ran and its last lines, e.g. "12 pass, 0 fail">
- CONTRADICTS: <each place SPEC.md or src/types.ts contradicts itself or cannot be met, with the line; or "none">
```

Put the full output of every check you ran in the evidence file. No reasoning in the body.
