# Result — tests-index

status: done

Wrote the Round 11 acceptance tests from SPEC.md "Round 11" (I1 index, I2 show, I3 categories) with a planted
temporary git root per test; all 14 pass and the typecheck is clean.

## Files

- `.claude/skills/workflow-design/guard/test/round11-insight-index.test.ts` (new, 14 tests)
- `runs/20261016-six-experts/nodes/tests-index.progress.md` (pieces P1–P6, planned → start → done)
- `runs/20261016-six-experts/nodes/tests-index.result.md` (this file)

No `src/` file, SPEC, or data file was touched.

## Commands and last lines

```
cd .claude/skills/workflow-design/guard && bun test test/round11-insight-index.test.ts
 14 pass
 0 fail
 67 expect() calls
Ran 14 tests across 1 file. [249.00ms]

./node_modules/.bin/tsgo --noEmit -p .
 (no output)

bun test                      # whole guard suite, for the record
 1275 pass
 3 fail
Ran 1278 tests across 24 files. [6.90s]
```

The 3 failures are the C17 ones in `test/round3.test.ts` (process list dropping); `bun test test/round3.test.ts`
alone gives 159 pass / 3 fail, so they are pre-existing and not from this file.

## Coverage against the Fails-if lines

| SPEC Fails-if | test |
|---|---|
| a section is missing from the index or listed twice | `P1 …every planted section appears once` (rows + `Set` size + one row per file), `P1 …no journal record still gets a row, with check -` |
| the index prints any whys, root-cause or option text | `P2 …the planted secret is in no row, JSON or table` (secret in whys, Source, root cause and option 1) |
| `show` prints a section that does not match, or misses one that does | `P3 --category prints only the matching` (tool category; the spec category and the great section absent; two `--category` flags print each once), `P3 a great section is printed whole` |
| a category rule with no matching section breaks the index | `P5 …every section is still listed` (a `never` rule with sources, titles and kinds that match nothing) |

Also covered: I2 `<file>#<id>` and a bare `<file>` ref, usage error 2 on stderr with nothing on stdout, "no matching
insight sections", I3 first matching rule and the condition that fails it, a section's own `Category: spec` line
overriding the rules while an unknown id falls back to the rules, `loadCategories` on the shipped
`data/insight-categories.yaml`, `insight index --json` keys, the markdown header and rows, and an empty root.

## CONTRADICTS

none.

Two things the tests pin that the SPEC does not say outright, so they are my reading, not the SPEC's words:
`insight show`'s usage error goes to **stderr** (exit 2) and leaves stdout empty, and `--json` wraps the rows as
`{"sections": [...]}`. If either is meant to be otherwise, those two assertions are where to change it.