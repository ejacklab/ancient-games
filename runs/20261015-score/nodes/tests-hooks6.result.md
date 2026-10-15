status: complete

Wrote 40 SPEC-derived K2 hook and K3 path-score acceptance tests; the latest run has 34 passing and 6 failing tests, all remaining failures asserting missing path-skeleton scores in the concurrently changing implementation.

files:
- .claude/skills/workflow-design/guard/test/round6-hooks.test.ts
- runs/20261015-score/nodes/tests-hooks6.result.md

commands and last lines (run from .claude/skills/workflow-design/guard):
- `bun test test/round6-hooks.test.ts` — exit 1; `34 pass`, `6 fail`, `836 expect() calls`, `Ran 40 tests across 1 file. [233.00ms]`.
- `./node_modules/.bin/tsgo --noEmit -p .` — exit 0; no output, no errors in this file or others.
- Two earlier test invocations from the repository root matched no files; the reported counts are from the guard package directory.

Coverage: reminder context and once-per-session marker; Write/Edit/MultiEdit touches; session isolation; invalid/unmarked criteria once per file state; changed/deleted files; unmet-item failure fields and deduplication; open-failure/raise/path ordering and D6; late criteria after success or failure, per-file deduplication, first-touch timing and exclusion of criteria-generated failures; skeleton score, percentage mean, zero/absent scores, session discovery, and written skeleton. Secret planting covers request, criterion, command, and tool output; assertions scan hook output and guard-owned state for leakage.

These acceptance checks were authored by Codex from SPEC.md, independently of the implementation; passing them does not establish behavior outside these fixtures. No implementation files changed and no commit made.

CONTRADICTS: SPEC.md:478 says `criteria written first leave no late record` in the Fails-if list, while K2's late-criteria rule at lines 464–467 creates a late failure only when the first touch follows a checked result. The test asserts that criteria touched first produce no late failure, following that operative rule.
