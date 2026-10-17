# bridge-3 — result

**Status: done.** "V7, by case" (the last bullet of SPEC Round 19) is implemented; every test in
`.claude/skills/workflow-design/guard/test/round19-evaluation.test.ts` passes, including the one that was red,
"V7: a new FAIL case in a group that already failed in the baseline is still a failure".

One sentence: `--baseline` now holds a group back only when the group failed before **and** every one of its FAIL cases was
FAIL in the baseline too, so a FAIL case the baseline did not fail makes the group a new failure instead of a note.

## Files changed

- `.claude/skills/workflow-design/guard/src/evaluation.ts` — new `failingCaseIds(cases, group)` (a group's FAIL case ids,
  the group read by the id prefix through the existing `casesOfGroup`) and `heldBackGroups(verdict, baseline)`; the baseline
  branch of `ingestVerdict()` calls `heldBackGroups()` instead of `failingGroupNames()` on the baseline's requirements alone;
  the file header and the two V7 comments now name the case-level rule. `failingGroupNames()` is kept and used inside
  `heldBackGroups()` for the requirement half.
- `.claude/skills/workflow-design/guard/src/cli.ts` — one usage line: "`--baseline F` holds back the groups F already
  failed, case by case". The flag itself was already wired by bridge-2 and is unchanged.

Nothing else was touched: no test, no `SPEC.md`. Nothing staged, nothing committed (`git status` shows `src/cli.ts`
modified and `src/evaluation.ts` untracked; every other entry in that output was already there before this brief).

## Commands

- `cd .claude/skills/workflow-design/guard && bun test` → last line: `Ran 1527 tests across 37 files. [14.46s]`
  (1527 pass, 0 fail, 7891 expect() calls).
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` → last line: no output, exit 0 (clean).

## The reading I chose where SPEC leaves a case open

SPEC: "a group FAIL in the baseline too is a note only when every one of its FAIL cases was FAIL in the baseline; a FAIL case
the baseline did not fail makes it a failure." Two edges are not pinned by that sentence or by a test — decided, not measured:

- **A case the baseline says nothing about was not failed by the baseline**, so it counts as new. A baseline written by an
  older run that carried no `cases` array at all therefore holds back nothing for a group that has FAIL cases (it still holds
  back a group whose verdict has no FAIL cases — vacuously "every one of its FAIL cases", which is how V7's own test passes).
  The alternative, treating a missing `cases` array as "the baseline cannot speak about cases", would silently re-record
  every old group as new; the literal reading errs toward recording a failure, and a note is still left in the owner's file
  for the group it does hold back.
- **Both rows are asked.** The group must have failed in the baseline's `requirements` *and* have no new FAIL case. A verdict
  whose requirements fail where the baseline's passed is a failure even if its case ids happen to appear in the baseline's
  cases.

Checked by hand in a scratch root (`/tmp`, since it is scratch and not a refer-back artifact), each with its own bytes so the
V3 same-bytes return could not mask the run:

| baseline | verdict | result |
|---|---|---|
| no `cases` array; B1 FAIL before | B1 fails, FAIL case `B1-F1` | `evaluator:B1` recorded — the case is new |
| `B1-F1` judged PASS in the baseline | B1 fails, FAIL case `B1-F1` | `evaluator:B1` recorded |
| `B1-F2` FAIL in the baseline | B1 fails, FAIL case `B1-F2` | no record; note `- B1 · FAIL in the baseline too · B1.1` |
| absent file | any | `- evaluation · could not run · no such verdict file: …`, exit 1, no record |
| `--baseline` with no value | any | exit 2 (`--baseline needs a value`) |

## CONTRADICTS

None. The one item bridge-2's result listed as decided — "group matching is by group name, and the note lists the ids the
verdict itself failed" — is unchanged here: `baselineLine()` still carries the verdict's ids, not the baseline's subset.
Round 19's last bullet refines only *which groups are held back*, which is what this brief was asked to implement; SPEC and
the test file agree on the narrower rule, and the test file pins both halves of it.