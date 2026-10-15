# Brief — m3-gap, attempt 1

You are working in a git worktree; the current folder is the repository root. Work only inside it.

## Task (one deliverable)

Add tests to `tools/harness-guard/test/insight.test.ts` for two M3 behaviours SPEC.md states that the current tests do
not pin. M3's code and tests were both written by one engine (opencode); you are the independent engine. The COO
planted wrong versions of `src/insight.ts`: one that **accepts an unknown option kind** such as `[policy]` survived
every test, and one that accepts an extra, made-up **source** word survived too.

## Context

- `tools/harness-guard/SPEC.md`, section **M3** (read it in full): an option kind outside `[rule]`, `[check]`,
  `[tool]`, `[config-advice]` (e.g. `[policy]`) is `R12.3-option-kind`; `Source:` must be one of `instruction`,
  `check`, `tool`, `config`.
- `tools/harness-guard/src/types.ts` (fixed). Do not read `src/insight.ts` — the tests come from SPEC.md.

## Standard

- New tests: an option `[policy] … evidence: x` → `checkSection` has a fail finding with rule `R12.3-option-kind`, and
  a failure answered only by such a section stays open in `openFailures`; at least two made-up source words (e.g.
  `person`, `luck`) → `R12.3-source`; the four valid kinds and four valid sources each pass (positive controls).
- Keep every existing test unchanged. Use temporary folders as the existing tests do.
- Check: `cd tools/harness-guard && bun test test/insight.test.ts` — report the counts. If a new test fails against the
  current implementation, that is a finding, not a reason to weaken the test: report it.

## Limits

- May change: `tools/harness-guard/test/insight.test.ts` only; plus the result and evidence files below.
- Must not change: anything else. Do not commit. Do not start any other AI engine or agent.

## Write the result to

`runs/20261015-ts-hybrid/nodes/m3-gap-1.result.md` (write `m3-gap-1.result.tmp` first, then rename), header:

```
---
node: m3-gap
attempt: 1
engine: codex
model: <as your tool reports it>
status: ok | fail | partial
started: <UTC>
ended: <UTC>
evidence: runs/20261015-ts-hybrid/nodes/m3-gap-1.evidence.txt
---
<one sentence>
- Files written: …
- Check: <command and counts>
- New tests failing on the current implementation: <names, or none>
```
