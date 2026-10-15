status: done

Round 5 S3 is implemented in a new `src/paths.ts`: `PathError`, `findPathFiles(root)`, `loadPath(file)`, `checkPath(root, file)`, `skeleton(root, session, out?)` and `parents(root, category)`, with the shape SPEC S3 gives (lines 382–412) — no other export was added, and `src/types.ts` was not touched.

## Files written

- `.claude/skills/workflow-design/guard/src/paths.ts` (new, only file my Limits allow)
- `runs/20261015-learn-success/nodes/code-paths.result.md` (this file)

## Commands run and their last lines

1. `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` → no output, exit 0 (re-run after `src/hooks.ts` began importing `paths.ts`: still clean).
2. `cd .claude/skills/workflow-design/guard && bun test` → `Ran 962 tests across 14 files. 1.75s` — `937 pass`, `25 fail`.
   - **Round-5 path tests: 0 exist.** `test/round5-paths.test.ts` is not written yet (`grep -c round5-paths` → 0), so none of the counts below are S3 tests.
   - Baseline when I started, before the other workers' files changed: `922 pass`, `3 fail`, `Ran 925 tests across 13 files` — all 3 were `C17 (R9)` tests that throw `C17 needs a machine with no other opencode run process (found 3)` (this machine runs opencode; environmental, unrelated to S3).
   - The 25 failures now are **not mine**: nothing in the repo imports `paths.ts` except `src/hooks.ts` (S5 worker), and none of the failing test names touch paths. Running only the 13 pre-existing files: `900 pass`, `25 fail` — `D1 test runs that fail > D1 control` (19, e.g. `passing {"command":"bun test"} stays quiet`), `C2 …`, `PostToolUse > a successful file answer writes no record` (2) and the 3 environmental `C17`. These appeared while `src/hooks.ts` and `src/journal.ts` were being rewritten for S1/S5 (`git status`: those two plus `src/insight.ts` modified, `src/rates.ts` and `test/round5-insight.test.ts` new). Note for the S1/S5 worker: S1 says a passing engine call and a green test run **do** write a `success` record, while the Round-4 D1 control tests still assert "writes no record" / "stays quiet" — those controls need to count `kind: "success"` as an expected record.
3. Scratch check in `/tmp/opencode` (deleted afterwards; nothing written into the guard): parent+child files, `bun run` of the module → `findPathFiles` → `["runs/r1/success-path-child.yaml","runs/r1/success-path.yaml"]`; child 1% better → `better: true`, `gainPercent: 1`, findings `["warn:R12.7-aim-report"]`; repeated `R12.2-test-failed` listed in `repeatedFailures`; no `change` → `R12.7-copied`; wrong `aim.parent_value` → `R12.7-aim-mismatch`; absent parent → `R12.7-parent-missing`; parent value 0 → `gainPercent: null`; `great.evidence` missing → `R12.7-great-evidence`; empty `steps`/`measures` → 2 × `R12.7-path-missing`; `path: 2` → `PathError`; `skeleton(root, "s1", "../escape.yaml")` → `PathError: out: a path file is only written inside the root`; a session id with a colon survives `Bun.YAML.parse` of the skeleton.

## Decisions where SPEC left room

- **`measures` in `skeleton`** (SPEC line 402–404 reads "`measures` filled from the journal (`failures`: this session's failure records, `successes`: its success records) and `failures` (their check ids)"): `measures: { failures: <count>, successes: <count> }` plus a top-level `failures:` list of the distinct check ids, in journal order. Counts and ids only — no command or output text.
- **Message of `R12.7-aim-report`** is exactly `gain <n.n>% against a 2% aim` (SPEC line 398 quotes it in full, so nothing is appended; the measure and parent value are in `fix`). SPEC line 398 writes the negative example with a typographic minus (`−4.0%`); I emit ASCII `-4.0%`, since the message is machine-readable output and the sign is the same gain. If a test copies the doc's minus verbatim it will differ in that one character.
- **A child with a parent and no `aim`** is not a finding: SPEC line 395 makes `gainPercent`/`better` null "with no parent or aim", so a missing aim is a legitimate state and only `R12.7-aim-missing` (an `aim` whose `measure` is not in both files, or no measure at all) fails.
- **A path file that does not parse or lacks `path: 1`** is reported by `checkPath` as `R12.7-path-missing` rather than throwing (SPEC gives `PathError` to `loadPath`; `path check` should not crash on a bad file). Round 3's C8 principle (validation never throws on any YAML shape) is applied throughout: every field is read defensively, so no YAML shape makes `checkPath` or `parents` throw.
- **`parents()`** returns each matching file with its numeric `measures` and its own `checkPath(...).better`, in `findPathFiles` order (ascending, so the most recent file name is last).
- **Skeleton placeholders for the optional blocks** (`parent`, `change`, `aim`, `great`) are written as commented lines: a written-but-empty `aim.measure` would fail `R12.7-aim-missing`, and a fresh skeleton must not fail its own check for fields the agent has not filled yet.

## CONTRADICTS

- None in SPEC S3 itself. One SPEC conflict outside my node, found while running the suite and reported for the S1/S5 worker above: SPEC line 373 (S1) makes a green `test-run` and a clean engine call write a `success` record, while the Round-4 D1 control tests (`test/round4.test.ts`, "passing … stays quiet", "writes no record") still assert that nothing is written; the two cannot both hold as written.