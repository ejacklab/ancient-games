# Brief — m5-code, attempt 1

You are working in a git worktree; the current folder is the repository root. Work only inside it.

## Task (one deliverable)

Implement module M5 (hook adapters, install, doctor, CLI) in `tools/harness-guard/src/hooks.ts, src/plugins/opencode.ts, src/install.ts, src/doctor.ts, src/cli.ts` so that its acceptance tests pass. The tests in
`tools/harness-guard/test/hooks.test.ts, test/cli.test.ts, test/doctor.test.ts, test/plugin.test.ts` were written by a different engine from SPEC.md and are frozen: you must not change them.

## Context (only what this task needs)

- `tools/harness-guard/SPEC.md` — the specification. Read the **Common** section and the **M5** section in full.
- `tools/harness-guard/src/types.ts` — the shared types. Fixed: import them, never redefine or change them.
- `tools/harness-guard/data/traps.yaml`, `tools/harness-guard/data/engines.yaml` — the catalogues (read-only).
- Runtime: bun 1.4.3, TypeScript, **no npm dependencies** (`bun:test`, `Bun.YAML.parse`, `node:*` modules only).
- Style: match `tools/harness-guard/src/types.ts` — short comments, plain names.
- Already built and tested: `src/traps.ts`, `src/journal.ts`, `src/insight.ts`, `src/register.ts` (M1–M4, done). Use it; do not change it.
- Withheld on purpose: nothing — but the tests' author's reasoning is not given; the tests and SPEC.md are the whole contract.

## Standard (how it will be judged)

- `cd tools/harness-guard && bun test` — every test passes (all modules built so far, not only yours).
- `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` — exit 0, no type errors.
- Behaviour follows SPEC.md, not only the tests: where a test and SPEC.md disagree, do not bend the code to the test —
  stop and report it under CONTRADICTS with the test name and the SPEC line.
- No secret or raw command/prompt text in anything the module writes or prints (the tests plant `SECRET-PLANT-7f3a9c`).
- No new dependency; no change to `package.json`, `tsconfig.json`, `SPEC.md`, `src/types.ts`, `data/`, or any test.

The COO will re-run every check you report, and will plant wrong inputs of its own.

## Limits

- May change: `tools/harness-guard/src/hooks.ts, src/plugins/opencode.ts, src/install.ts, src/doctor.ts, src/cli.ts` only (and new helper files under `src/`); plus the result and evidence files below.
- Must not change: anything else. Do not commit; do not run `git` commands that change the repository.
- Do not start any other AI engine or agent. Do not read or print files outside the repository.

## Write the result to

Write the result file `runs/20261015-ts-hybrid/nodes/m5-code-1.result.md` (write to `m5-code-1.result.tmp` first, then
rename it). It starts with this header, then the body:

```
---
node: m5-code
attempt: 1
engine: opencode
model: <the model as your tool reports it>
status: ok | fail | partial
started: <UTC time>
ended: <UTC time>
evidence: runs/20261015-ts-hybrid/nodes/m5-code-1.evidence.txt
---
<first line: the answer in one sentence>
- Files written: <paths>
- Check: <the command you ran and its last lines, e.g. "12 pass, 0 fail">
- CONTRADICTS: <each place SPEC.md or src/types.ts contradicts itself or cannot be met, with the line; or "none">
```

Put the full output of every check you ran in the evidence file. No reasoning in the body.
