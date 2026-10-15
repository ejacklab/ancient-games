status: done

Round 5 S4 is implemented in `src/insight.ts`. It adds `## great: <path file>` sections, `checkGreatSection`, `greatAnswered`, and a `parseInsight` that keeps great sections apart from failure sections. The existing M3 tests still pass, and the only failures in round3 come from C17's precondition about other processes on the machine.

## Files written

- `.claude/skills/workflow-design/guard/src/insight.ts`. This is the only source file changed. I made the edit with a python heredoc in the shell, not with the Edit tool; the resulting diff is the same.
- `runs/20261015-learn-success/nodes/code-insight.result.md` (this file).

## What was added (all in insight.ts)

- `export interface GreatSection extends InsightSection { great: string; comparison: string | null; cause: string | null }`, plus `isGreatSection(s)`.
- `parseInsight`: a `##` heading whose text **starts with** `great:` (case-insensitive) becomes a GreatSection. It has `ids: []`, `whys: []`, `source: null` and `rootCause: null`, and the path file has surrounding backticks and quotes removed. A heading that has an F-id and `great:` later in its text stays a failure section.
- `Comparison:` and `Cause:` are read on the same line or on the next non-empty line, the same way `Root cause:` is read. `Options:` uses the M3 list parser (C6).
- `checkGreatSection(s)` returns these fail findings:
  - `R12.7-great-comparison` when the comparison is missing or empty.
  - `R12.7-great-cause` when the cause is missing or empty.
  - `R12.7-great-options` when there are fewer than 1 or more than 3 options, when an option's kind is not `rule`, `check` or `tool` (so `[config-advice]` fails), or when an option has no evidence.
  - Messages hold only counts and positions, never the author's text.
- `greatAnswered(root): Set<string>` returns the path files named by great sections that have no fail finding. Each path is root-relative and normalised; an absolute path inside the root is made relative.
- M3 is unchanged. `isLabel`, `parseRootCause` (now a wrapper over a shared `labelValue`), `checkSection`, `answered` and `openFailures` behave the same. A great section has no ids, so `answered` and the CLI `insight` command never count it.

## Commands and last lines

- `bun test test/insight.test.ts test/round3.test.ts` → `244 pass / 3 fail / Ran 247 tests across 2 files`.
  - All 3 failures are C17 tests, and each one fails on its precondition: `C17 needs a machine with no other opencode run process (found 3)`. `ps` showed 3 `opencode run` processes, which are other workers' engines. This is not caused by insight.ts.
- `bun test test/insight.test.ts` → `85 pass / 0 fail / Ran 85 tests across 1 file`.
- `bun test test/round3.test.ts -t "C5|C6|C7"` (the insight items) → `0 fail / Ran 18 tests across 1 file`.
- `./node_modules/.bin/tsgo --noEmit -p .` → no output, `tsgo exit 0`. That covers the whole project as it stood, including the other workers' new `paths.ts` and `rates.ts`.
- Round-5 insight tests: `test/round5-insight.test.ts` **did not exist** when I finished, so the count is 0 run. It needs to be run once the tests worker is done.
- Smoke check: I wrote a throwaway script in /tmp and deleted it afterwards. On a file holding a failure section with `great:` in its heading, a valid great section and a bad one, I got:
  - The failure section stayed a failure section.
  - `greatAnswered` returned only the valid section's path.
  - The bad section (no cause, 4 options, `[config-advice]`) failed.
  - A planted `SECRET-PLANT-7f3a9c` in the comparison did not appear in any finding.

## CONTRADICTS

- **The types.ts gap (the fixed file has no place for great-section data).** SPEC line: "`parseInsight` keeps such sections apart from failure sections (`InsightSection.ids` empty)". `InsightSection` in the fixed `types.ts` has no field for the heading's path file, the comparison or the cause. Neither `checkGreatSection` nor `greatAnswered` can work from an `InsightSection` as typed. I added them as fields on a local `GreatSection extends InsightSection` in insight.ts. Tests written from SPEC and types.ts alone cannot name these fields, so they have to go through `parseInsight`. If a test builds an `InsightSection` literal and passes it to `checkGreatSection`, it gets the comparison and cause findings.
- **No rule for an option's kind or evidence (my choice, not in SPEC).** SPEC S4 lists only three rules: `R12.7-great-comparison`, `R12.7-great-cause` and `R12.7-great-options`. It names no rule for a wrong kind or a missing `evidence:` on an option, so I report both under `R12.7-great-options`.
- **What the heading's path is relative to (my reading).** SPEC does not say. I treat it as relative to the guard root, which matches `findPathFiles` returning root-relative paths.
