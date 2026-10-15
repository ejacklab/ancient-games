# Brief — r3-code, attempt 1

You are working in a git worktree; the current folder is the repository root. Work only inside it.

## Task (one deliverable)

Change `tools/harness-guard/src/` so that the package meets the section **"Round 3 — changes from the review and the
measurements"** at the end of `tools/harness-guard/SPEC.md` (items C1–C24) and every test passes. The new tests are in
`tools/harness-guard/test/round3.test.ts` (written by a different engine, from SPEC.md); four older test rows were
updated to match Round 3. Tests are frozen: do not change any file under `test/`.

## Context

- `tools/harness-guard/SPEC.md` — read the Round 3 section in full, and the parts of M1–M5 each item refers to.
- `runs/20261015-ts-hybrid/nodes/review-1.result.md` — the review behind C1–C22, with the exact failing inputs.
- `tools/harness-guard/src/types.ts` — fixed. If a Round 3 item needs a type change, report it under CONTRADICTS
  instead of changing the file.
- C24 has no test: implement it as SPEC says; the COO will probe it.
- Runtime: bun 1.4.3, TypeScript, no npm dependencies.

## Standard

- `cd tools/harness-guard && bun test` — every test passes (796 now; 111 fail before your change).
- `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` — exit 0.
- Where a test and SPEC.md disagree, do not bend the code to the test: report it under CONTRADICTS.
- No secret or raw command/prompt text in anything the guard writes or prints (tests plant `SECRET-PLANT-7f3a9c`).

## Limits

- May change: files under `tools/harness-guard/src/` only (new helper files there are allowed); plus the result and
  evidence files below.
- Must not change: `test/`, `SPEC.md`, `src/types.ts`, `data/`, `package.json`, `tsconfig.json`, anything else.
- Do not commit. Do not start any other AI engine or agent. Run checks in the foreground; nothing in the background.

## Write the result to

`runs/20261015-ts-hybrid/nodes/r3-code-1.result.md` (write `r3-code-1.result.tmp` first, then rename). **Write it even
if you stop early** — with `status: partial` and what remains. Header:

```
---
node: r3-code
attempt: 1
engine: opencode
model: <as your tool reports it>
status: ok | fail | partial
started: <UTC>
ended: <UTC>
evidence: runs/20261015-ts-hybrid/nodes/r3-code-1.evidence.txt
---
<one sentence>
- Files written: …
- Check: <the two commands and their last lines>
- CONTRADICTS: <each, or none>
```
