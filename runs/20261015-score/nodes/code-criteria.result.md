status: done

Implemented Round 6 K1 in a new `src/criteria.ts` with exactly the SPEC K1 exports (`isCriteriaFile`, `findCriteriaFiles`, `loadCriteria`, `CriteriaError`, `checkCriteria`, `score`, `fromRegister`, `skeleton`); K2/K3 wiring is the other worker's file.

files: `.claude/skills/workflow-design/guard/src/criteria.ts` (new); `runs/20261015-score/nodes/code-criteria.result.md`. No other file touched, nothing committed.

commands and last lines:
- `bun test` (in `.claude/skills/workflow-design/guard`): `1075 pass / 3 fail / Ran 1078 tests across 16 files`. The 3 failures are the C17 tests (`round3.test.ts` "the CLI drops only its own process and its parent from running") that throw `needs a machine with no other opencode run process (found 3)` — this session itself is an opencode run. Verified as baseline: the same 3 fail with `src/criteria.ts` moved out of the tree, so they are environmental, not caused by this file. No round-6 criteria test file exists yet (`test/round6-criteria.test.ts` is still unwritten), so no round-6 count to report.
- `./node_modules/.bin/tsgo --noEmit -p .`: exit 0, no output — no error anywhere, mine or others'.
- Behaviour probe (temp file under `/tmp`, importing the module): every K1 fails-if holds — met-without-evidence → `R12.7-criterion-evidence`; repeated id → `R12.7-criterion-text`; no items → `R12.7-criteria-empty`; 2 of 3 met → `66.7`; an unmarked item counts as neither (lands in `unmarked`). `loadCriteria` throws `CriteriaError` on unparseable YAML and on a file without `criteria: 1`; `findCriteriaFiles` returns `.harness-guard/criteria/score.yaml` and `runs/2026/criteria.yaml` sorted, skipping `runs/2026/other.yaml`; `fromRegister` gives one unmarked item per `units(r)` (the deduped variant drops out); `skeleton` round-trips through `Bun.YAML.parse` and cuts the request to 120 characters.

decisions worth knowing (SPEC-consistent, but not spelled out):
- `isCriteriaFile` is exactly SPEC's `criteria*.yaml` (any folder); `findCriteriaFiles` follows SPEC's two locations — under `.harness-guard/criteria/` every `*.yaml` counts (as S3/S5 do for path files), under `runs/**` only `criteria*.yaml`.
- An item that is not a mapping, or has no id, is read as id `""` and text `""`: it counts in `total`, raises `R12.7-criterion-text` and appears in `unmarked` as `items[<n>]` (position, no item text). SPEC has no `R12.7-criteria-malformed` rule, so no new rule id was invented; the point is that no YAML shape makes `checkCriteria` or `score` throw (round 3, C8).
- `findings.message`/`fix` carry ids and positions only — no criterion text, no request text, nothing planted.

CONTRADICTS: none. SPEC lines followed as written for all of Round 6 K1.