status: complete

Wrote 49 SPEC-derived acceptance tests for Round 5 S1/S2/S5, covering every Fails-if with planted inputs; the final run has 45 passes and 4 failures, and TypeScript passes.

Files written:
- `.claude/skills/workflow-design/guard/test/round5-hooks.test.ts`
- `runs/20261015-learn-success/nodes/tests-hooks.result.md`

Commands and last lines (verification run from `.claude/skills/workflow-design/guard`):
- `bun test test/round5-hooks.test.ts` — initial: `44 pass`, `4 fail`, `Ran 48 tests across 1 file. [230.00ms]`; final: `45 pass`, `4 fail`, `601 expect() calls`, `Ran 49 tests across 1 file. [222.00ms]` (exit 1).
- `./node_modules/.bin/tsgo --noEmit -p .` — initial last line: `Type 'PathReport' has no call signatures.` at `src/cli.ts(285,16)` (another worker's file); final: no output (exit 0), no errors in the test file or other files.
- Each fixture runs `git init --quiet` in its temporary `hg-` repository (no output); CLI tests run `bun <absolute guard>/src/cli.ts rates` with and without `--session round5-session` (both return exit 0 with empty stdout/stderr).

Remaining failures:
- S2: both CLI tests receive empty stdout instead of the Markdown rates table (SPEC.md line 380).
- S5: missing/invalid great sections block once, but the recorded raised ids are `["great:runs/success-path.yaml"]` rather than `["path"]` (SPEC.md lines 425–426).

Check author: Codex wrote these tests from SPEC.md; these synthetic payloads check the handler and CLI behavior, not which hooks a live harness emits. Tests retain the spec expectations rather than modifying implementation files. Secret-planted checks cover hook output and guard-owned files, rates rows, and CLI output.

CONTRADICTS: none.
