# mc-fix-a — result

Date: 2026-10-18 · brief: `runs/20261018-finish-everything/briefs/mc-fix-a.md` · findings: `runs/20261018-finish-everything/red/mc-findings-red.md`
(accepted set from `mc-reproduce-red/result.md`)

## What was changed

12 pieces, 12 findings — 7 TypeScript (`memory_check/src/`), 3 Python (`tools/memory_index.py`), 2 in both.
Nothing was committed; nothing outside `memory_check/src/`, `tools/memory_index.py` and this run's `nodes/`
folder was touched.

| Piece | Fix | Where |
| --- | --- | --- |
| C2 | `projectMemory` is now also true when the staged diff *removes* memory (`git diff --cached -M --name-status --diff-filter=DR`), so a staged `git rm` of all of `project-memory/` reaches `checkK41` instead of being read as "not applicable" | `gitchecks.ts` `stagedMemoryRemovals` (new), `checks.ts` |
| C3 | `versionsOf`'s baseline is the entry's text at the head of the range when the range holds no commit of that entry, so the HEAD→staged change is compared instead of passing over 0 transitions | `gitrequirements.ts` |
| C4+A3 | A `.claude/settings.json` hook registered under `hooks.SessionStart` is read as a session-start read whatever its command says; its `command` strings are parsed out of the JSON and judged with `atStart` forced true | `cachechecks.ts` `sessionStartHookCommands` (new) |
| C5 | `checkRd1` reads each session-start file from the **staging area** (`stagedFiles`, new: one `ls-files -s` + one `cat-file --batch`). A file in no staged version (untracked, or a hook under `.git/`) is read from the working tree, and the evidence says which was read | `gitchecks.ts` `stagedFiles` (new), `cachechecks.ts`, `checks.ts` |
| C6 | A `memory_index.py` warning naming W1.1a is a break; every other warning stays a note. `tools/memory_index.py` was **not** touched (brief: B2.5 keeps inactive entries non-blocking there) | `indextool.ts` |
| C7+A1 | The unborn-HEAD early return applies only to a revision; `git ls-files -s` reads the staging area with no commit | `tools/memory_index.py` `check_index` |
| C8 | `is_object_id` accepts 40- and 64-character hex ids | `tools/memory_index.py` |
| C9 | `headerDelimiters` keeps only `---` pairs whose lines between them hold a top-level `key:` line, so two thematic breaks in a body are not a second header block | `entry.ts` |
| C11 | `agentMemory` lists child folders only; a file in `<home>/.claude/agent-memory/` is not a location | `locations.ts` |
| C12+A5 | The warning names entry files from the parsed staged paths (`CheckRun.stagedEntries`) instead of matching them out of the evidence with a pattern, so a bare name from `memory_index.py` and a name with a space are both named whole | `checks.ts`, `warn.ts` |
| A2 | `check_index` reports the over-limit failure beside a mismatch instead of returning on the mismatch first | `tools/memory_index.py` |
| A4 | `linksNothing` reads a bare `-` as no link, so an empty indented bullet under `superseded_by` breaks K4.1 | `gitrequirements.ts` |

## Checks run (the brief's standard)

| Check | Before | After |
| --- | --- | --- |
| `cd memory_check && bun test` | 87 pass / **10 fail** | **97 pass / 0 fail** |
| `python3 -m pytest -q tests/test_memory_index.py tests/test_memory_index_unit.py tests/test_memory_index_review2.py` | 465 pass / **3 fail** | **468 passed** |
| `cd memory_check && ./node_modules/.bin/tsgo --noEmit -p .` | clean | clean |

Baseline numbers are from the first run of each suite in this session, before any edit.

## What each check does not establish

- The 10 new `review2.test.ts` cases and the 3 new `review2.py` cases are the *only* thing that shows each fix
  works; each was checked against the fixture it ships with, on the engine the fixture runs (bun / CPython).
- A clean typecheck is not a review. `commandsUnder` and `sessionStartHookCommands` assume Claude Code's settings
  shape `hooks.<Event>[].hooks[].command`; the walker also finds `command` keys nested deeper, which is wider than
  that shape and not tested against a settings file that is not shaped like it.
- The report row for Rd1 changed shape: it now reads `<file>, the staged state:1-N` or
  `<file>, the working tree (in no staged version):1-N` where it read `<file>:1-N`. Nothing asserts on that text;
  it was eyeballed on a scratch repo, not asserted.
- I ran the tool against **this** repository once (`bun src/cli.ts --project .. --home ~`): it exits cleanly, but
  this repository has no `project-memory/`, so every record reads "not applicable" and the run exercised almost
  none of the changed paths. A scratch repo under `/tmp` (with a cache, a SessionStart hook, a staged-only
  instruction and one entry) was used to eyeball the Rd1 evidence; both new breaks appear with the paths above.

## Deliberately not changed

- `checks.ts:270`'s Rd3.1a workaround (`mismatch && !overLimit && over-limit size` → "could not run"). After the A2
  fix in `memory_index.py` an over-limit render always prints the over-limit message, so the branch cannot be
  reached any more. I left it in place: it is a guard against reporting a pass for a check that never ran, and
  removing it is not part of any accepted finding.
- `tools/memory_index.py` for C6 — the brief forbids it (B2.5), and the reproduce step flagged
  `test_active_problems_are_errors_and_inactive_ones_are_warnings` as the unit test that a py-side fix would
  break. That test exercises `parse_entry` only, so the memory-check-side fix leaves it green (it passes).