status: complete

Wrote 49 K1 acceptance tests from SPEC.md, covering every K1 Fails-if with planted files plus discovery, loading, register conversion, skeletons and secret handling, without reading src/criteria.ts.

files: .claude/skills/workflow-design/guard/test/round6-criteria.test.ts; runs/20261015-score/nodes/tests-criteria.result.md

commands and last lines (working directory: .claude/skills/workflow-design/guard):

- `bun test test/round6-criteria.test.ts` — exit 0; `49 pass`, `0 fail`, `72 expect() calls`; `Ran 49 tests across 1 file. [25.00ms]`.
- `./node_modules/.bin/tsgo --noEmit -p .` — exit 0; no output, no errors in this file or others.

Checks authored by this worker against SPEC.md; passing establishes the planted cases, not independent verification or untested hook/CLI behavior. No commits made.

CONTRADICTS: none.
