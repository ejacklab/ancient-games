# Brief — m1-tests, attempt 3

You are working in a git worktree; the current folder is the repository root. Work only inside it.

## Task (one deliverable)

Write the acceptance tests for module M1 (traps, engine-call recognition, result check) in `tools/harness-guard/test/traps.test.ts`, from SPEC.md alone. The
implementation (`tools/harness-guard/src/traps.ts`) does not exist yet and is written afterwards by a different engine to pass your tests,
so your tests are the standard it is judged by. Do not write the implementation.

## Context (only what this task needs)

- `tools/harness-guard/SPEC.md` — the specification. Read the **Common** section and the **M1** section in full.
- `tools/harness-guard/src/types.ts` — the shared types. Fixed: import them, never redefine or change them.
- `tools/harness-guard/data/traps.yaml`, `tools/harness-guard/data/engines.yaml` — the catalogues (read-only).
- Runtime: bun 1.4.3, TypeScript, **no npm dependencies** (`bun:test`, `Bun.YAML.parse`, `node:*` modules only).
- Style: match `tools/harness-guard/src/types.ts` — short comments, plain names.
- Withheld on purpose: the implementation (it does not exist).

## Feedback from the previous attempt (the check's real output)

Small repair after your attempt 2. The COO resolved two points in SPEC.md (re-read the M1 section):

1. **A pipe into codex is fed stdin, so it is not the trap.** Your attempt-2 change made
   `lint: a pipe in another segment does not satisfy the codex stdin exception` expect `trap:codex-stdin` for
   `printf task | codex exec -`. That would block a correct command (a false deny — the very thing round 2 fixes).
   SPEC now gives `Segment` a `piped` field (true when the separator before it is `|`) and traps an `unless_piped`
   condition; `data/traps.yaml` sets `unless_piped: true` on `codex-stdin` and its `unless` regex no longer mentions
   the pipe. `src/types.ts` exports `Segment`. Change that test to expect **no** finding, and add tests for
   `segments(...).piped` (true after `|`, false after `||`, `;`, `&&`, and for the first segment) and for a planted
   trap with `unless_piped: true` against a piped and an unpiped segment.
2. SPEC line about recognition `background` now says it is the matching segment's `background` (your CONTRADICTS);
   no test change needed if yours already follow the Segments rules.

Change nothing else.


## Standard (how it will be judged)

- Every **Fails-if** line of the M1 section is pinned by at least one test that plants the wrong input and
  asserts the right outcome; every export listed in M1 is called by at least one test with the exact signature
  SPEC.md gives. Name each test after the behaviour (e.g. `"lint: codex exec without a stdin redirect is a trap"`).
- Tests build their own fixtures in a temporary folder (`fs.mkdtempSync(path.join(os.tmpdir(), "hg-"))`), never in the
  repository; a test that needs a git repository creates one with `git init` in the temp folder.
- Import from the module path exactly as SPEC.md names it (e.g. `import { lintCommand } from "../src/traps.ts"`).
- A test may not depend on the machine (user name, home folder, installed engines, running processes) — pass
  everything through the function arguments SPEC.md defines (`LintContext.running`, `HookEnv`, …).
- Planted secrets: where a function writes or prints anything, one test plants the string `SECRET-PLANT-7f3a9c` in the
  input and asserts it never appears in the output, the journal or an evidence file.
- Check you run: `cd tools/harness-guard && bun test test/traps.test.ts` — it must run (load) and fail **only** because `src/traps.ts` is missing
  (report the exact error). Also `./node_modules/.bin/tsgo --noEmit -p .` will report the missing module; any other
  type error in your test file must be fixed.

The COO will re-run every check you report, and will plant wrong inputs of its own.

## Limits

- May change: `tools/harness-guard/test/traps.test.ts` and new files under `tools/harness-guard/test/fixtures/` only; plus the result and evidence files below.
- Must not change: anything else. Do not commit; do not run `git` commands that change the repository.
- Do not start any other AI engine or agent. Do not read or print files outside the repository.

## Write the result to

Write the result file `runs/20261015-ts-hybrid/nodes/m1-tests-3.result.md` (write to `m1-tests-3.result.tmp` first, then
rename it). It starts with this header, then the body:

```
---
node: m1-tests
attempt: 3
engine: codex
model: <the model as your tool reports it>
status: ok | fail | partial
started: <UTC time>
ended: <UTC time>
evidence: runs/20261015-ts-hybrid/nodes/m1-tests-3.evidence.txt
---
<first line: the answer in one sentence>
- Files written: <paths>
- Check: <the command you ran and its last lines, e.g. "12 pass, 0 fail">
- CONTRADICTS: <each place SPEC.md or src/types.ts contradicts itself or cannot be met, with the line; or "none">
```

Put the full output of every check you ran in the evidence file. No reasoning in the body.
