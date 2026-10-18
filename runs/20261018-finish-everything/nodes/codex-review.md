## Findings

1. **SessionStart cache reads can incorrectly pass.** `memory_check/src/cachechecks.ts:145` applies prose negation rules to executable commands. Contract: “a start hook or instruction opens any file under `project-memory/.cache/`” fails Rd1. Input: a SessionStart command `cat project-memory/.cache/index.sqlite || echo not found`. The word `not` exempts the command; my probe returned clean despite the cache read. The C4+A3 test uses only a bare `cat`, so it misses this defect.

2. **The header fix both misses entries and rejects valid prose.** At `memory_check/src/entry.ts:84`, encountering thematic breaks without a colon stops scanning all later headers. Contract W6.1a fails when “an entry file holds more than one entry.” Input: a valid entry followed by `---\nSee below.\n---`, then a second entry header. My probe reported one header and no break. Conversely, `---\nNote: keep UTC timestamps.\n---` falsely fails W6.1a, contrary to U2’s requirement to report exactly the planted breaks. The C9 test covers neither case.

3. **Deletion warnings lose the deleted filename.** `memory_check/src/warn.ts:55` resolves entry filenames exclusively through surviving staged entries. Contract R2 requires warnings “with ids and file names.” Input: stage deletion of the only entry, update the index, then run `--warn`. The K4.1 warning contains no filename because the deleted entry is absent from `stagedEntries`; my renderer probe reproduced this. C2 checks the report, while C12+A5 tests only surviving entries.

4. **Compound test commands escape the timeout.** `.claude/workflows/crossed-build-check.js:71` prefixes the command without enclosing its shell expression. Contract XB1: timeout “is the limit of every engine call and test command.” With `timeout: 60` and `test_cmd: "true && sleep 61"`, the generated command is `timeout 60 true && sleep 61`; only `true` is bounded. My shortened timing probe confirmed this behavior. The harness checks prompt substrings using simple commands, so it passes with this defect.

5. **C17 still depends on unrelated process names.** `.claude/skills/workflow-design/guard/test/round3.test.ts:858` preserves every process containing `second task`, regardless of the test’s unique marker. Contract: remove “every other process’s `opencode run` line,” retaining the tests’ marked lines. Input: another session running `opencode run "second task"`. The filter retains it, causing the test expecting no parallel-process trap to fail. My filter probe confirmed retention; the tests do not introduce this external collision.

6. **Explicit null timeout bypasses validation.** `.claude/workflows/crossed-build-check.js:54` turns `timeout: null` into 580. Contract XB1 permits “a whole number from 60 to 3600” and rejects anything else. My workflow probe with null reached four stubbed agent calls instead of returning an error. Invalid-input tests cover `30`, `4000`, and `"x"`, but omit null.

## Checked

These findings are my reading of the quoted contracts, supported by read-only probes I wrote.

No additional issues found on inspection in the remaining memory-check fixes, deadline selection and ambiguity handling, criteria deferral, or evaluator cleanup paths and symlink protection.

The parser recognized one complete F3 case and all four vision cases. The existing crossed-build-check harness passed; it stubs agents and does not establish that generated shell commands enforce their limits.

Fixture-writing suites were inspected rather than run, honoring the read-only brief. No files were intentionally changed.