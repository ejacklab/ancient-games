# bridge-2 — result

**Status: done.** V6 and V7 of SPEC Round 19 are implemented; every test in
`.claude/skills/workflow-design/guard/test/round19-evaluation.test.ts` passes, including V1, which failed only because it
expected the per-id shape V6 replaces.

One sentence: the ingest now groups the FAIL requirements by their `group` field and writes one failure record per group
(`evaluator:<group>`, input the group's ids joined by `, `), and `--baseline <verdict.json>` turns a group that the baseline
also held as failing into an owner's note instead of a failure.

## Files changed

- `.claude/skills/workflow-design/guard/src/evaluation.ts` — `failingGroups()` / `failingGroupNames()`, `readVerdict()` (the
  verdict reader factored out, so the baseline is read by the same rules), `count(rows, heldBack)` (fails = records written,
  one per group; a group held back by the baseline is in none of the three numbers), the group loop, `baselineLine()`, and
  `ingestVerdict(…, baseline: string | null = null)`.
- `.claude/skills/workflow-design/guard/src/cli.ts` — `evaluation ingest` reads `--baseline` and resolves it against the
  cwd; the usage text names the flag.

Nothing else was touched: no test, no `SPEC.md`. Nothing staged, nothing committed (`git status` shows both files
unstaged; the other entries in that output were already there).

## Commands

- `cd .claude/skills/workflow-design/guard && bun test` → last line: `Ran 1526 tests across 37 files. [17.34s]` (1526 pass,
  0 fail, 37 files, 7890 expect() calls).
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` → last line: no output, exit 0 (clean).

## What no test pins, and how it behaves (checked by hand)

The lesson for this edit: the new `--baseline` cases enter an existing path, so that path's early returns were listed before
the change and each was exercised. A verdict's early returns (run outside the root, missing file, not JSON, no
`requirements`, an unnamed requirement, already-ingested bytes, UNKNOWN, non-FAIL) are unchanged, so V1–V5 still pass.

The baseline's own early returns are new and no test covers them — decided, not measured:

- **A baseline that cannot be read is a blocked run**: the note `- evaluation · could not run · <reason>`, exit 1, and no
  failure record at all — the same path as V4's blocked verdict. Reason: without the baseline a group that failed before
  the change would be recorded as a new failure, and the guard does not log a failure it cannot justify (Round 8). Verified
  by hand for all three shapes (absent file, `{oops`, `{"meets": false}`): exit 1, note, 0 records.
- **`--baseline` with no value** → `--baseline needs a value`, exit 2, from the shared `flagValue`.
- **A FAIL requirement with no `group`** is a group of one, named by its id — the old per-id behaviour in that case.
- **The summary line** counts records written, not requirement verdicts: with a baseline holding back one group of two
  ids and one other group failing, it prints `evaluation ingest: 1 FAIL recorded, 0 UNKNOWN noted, 1 PASS`. V5's line is
  unchanged (its single FAIL requirement is a single group). The line has three fixed buckets, so a group held back by the
  baseline is deliberately in none of them rather than miscounted as a PASS.
- **Group matching is by group name**, and the note lists the ids the verdict itself failed, not the subset the baseline
  holds: SPEC V7 suppresses at the group level ("a group that is FAIL in the baseline too").

## CONTRADICTS

None. SPEC Round 19 says V6 replaces V1's per-requirement record, and the test file pins V1's `evaluator:G1` / `input:
"R1.1"` shape, which V6 reproduces for a group of one id — the two agree.