# Brief — m2-tests, attempt 2

You are working in a git worktree; the current folder is the repository root. Work only inside it.

## Task (one deliverable)

Write the acceptance tests for module M2 (failure journal) in `tools/harness-guard/test/journal.test.ts`, from SPEC.md alone. The
implementation (`tools/harness-guard/src/journal.ts`) does not exist yet and is written afterwards by a different engine to pass your tests,
so your tests are the standard it is judged by. Do not write the implementation.

## Context (only what this task needs)

- `tools/harness-guard/SPEC.md` — the specification. Read the **Common** section and the **M2** section in full.
- `tools/harness-guard/src/types.ts` — the shared types. Fixed: import them, never redefine or change them.
- `tools/harness-guard/data/traps.yaml`, `tools/harness-guard/data/engines.yaml` — the catalogues (read-only).
- Runtime: bun 1.4.3, TypeScript, **no npm dependencies** (`bun:test`, `Bun.YAML.parse`, `node:*` modules only).
- Style: match `tools/harness-guard/src/types.ts` — short comments, plain names.
- Withheld on purpose: the implementation (it does not exist).

## Feedback from the previous attempt (the check's real output)

Repair after the code node ran your tests (89 of 90 pass against the M2 implementation).

1. **A test bug, reproduced by the COO** (`/tmp/bunbug`): `test.each([null, undefined, 7, "failure", [], {}])` — bun
   spreads an array element into arguments, so the `[]` case calls the callback with **zero** arguments; the callback
   declares one parameter, and bun then treats that parameter as a `done` callback and waits 5 s:
   "this test timed out after 5000ms, before its done callback was called". Wrap every element of that table in its
   own array (`[[null], [undefined], [7], ["failure"], [[]], [{}]]`) or use `test.each` with objects, and check no
   other `test.each` table in the file has an array element that is not wrapped.
2. SPEC M2 now says `writeEvidence` and `appendRecord` drop raw-content keys (your tests already expect that) and
   `appendFailure` stores the strings it is given. Check your tests agree; change only a test that contradicts it.

Change nothing else. Run `bun test test/journal.test.ts` — the implementation now exists in `src/journal.ts` (do not
read or change it); report the pass/fail count.


## Standard (how it will be judged)

- Every **Fails-if** line of the M2 section is pinned by at least one test that plants the wrong input and
  asserts the right outcome; every export listed in M2 is called by at least one test with the exact signature
  SPEC.md gives. Name each test after the behaviour (e.g. `"lint: codex exec without a stdin redirect is a trap"`).
- Tests build their own fixtures in a temporary folder (`fs.mkdtempSync(path.join(os.tmpdir(), "hg-"))`), never in the
  repository; a test that needs a git repository creates one with `git init` in the temp folder.
- Import from the module path exactly as SPEC.md names it (e.g. `import { lintCommand } from "../src/traps.ts"`).
- A test may not depend on the machine (user name, home folder, installed engines, running processes) — pass
  everything through the function arguments SPEC.md defines (`LintContext.running`, `HookEnv`, …).
- Planted secrets: where a function writes or prints anything, one test plants the string `SECRET-PLANT-7f3a9c` in the
  input and asserts it never appears in the output, the journal or an evidence file.
- Check you run: `cd tools/harness-guard && bun test test/journal.test.ts` — it must run (load) and fail **only** because `src/journal.ts` is missing
  (report the exact error). Also `./node_modules/.bin/tsgo --noEmit -p .` will report the missing module; any other
  type error in your test file must be fixed.

The COO will re-run every check you report, and will plant wrong inputs of its own.

## Limits

- May change: `tools/harness-guard/test/journal.test.ts` and new files under `tools/harness-guard/test/fixtures/` only; plus the result and evidence files below.
- Must not change: anything else. Do not commit; do not run `git` commands that change the repository.
- Do not start any other AI engine or agent. Do not read or print files outside the repository.

## Write the result to

Write the result file `runs/20261015-ts-hybrid/nodes/m2-tests-2.result.md` (write to `m2-tests-2.result.tmp` first, then
rename it). It starts with this header, then the body:

```
---
node: m2-tests
attempt: 2
engine: codex
model: <the model as your tool reports it>
status: ok | fail | partial
started: <UTC time>
ended: <UTC time>
evidence: runs/20261015-ts-hybrid/nodes/m2-tests-2.evidence.txt
---
<first line: the answer in one sentence>
- Files written: <paths>
- Check: <the command you ran and its last lines, e.g. "12 pass, 0 fail">
- CONTRADICTS: <each place SPEC.md or src/types.ts contradicts itself or cannot be met, with the line; or "none">
```

Put the full output of every check you ran in the evidence file. No reasoning in the body.
