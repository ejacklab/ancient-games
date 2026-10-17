# P2 evaluator repair verification and coverage

Checker author: P2 Codex. The acceptance and mutation checks below were written by the evaluator's author. They test the evaluator and canned fixture answers, not the future builder's correctness on real repositories.

The repair adds 15 cases (52 total), source-backed text and call-site checks, chain/test endpoint checks, independent safety verdicts, and a seeded held-out generator. Changes are confined to `eval/` and `test/eval/`; no package was added. All ten fixture tsconfigs type-check in the generated copies for seeds 0, 1 and 49271. Tests independently compare identifier tokens and relocated lines with the written files, then check transformed witnesses against each rewritten case. Witness and case rewriting share generator helpers, so passing them alone is not independent evidence; type checking and source/AST observations provide additional checks.

New cases by requirement:

| Requirement | Cases |
|---|---|
| R1 | R1-where, R1-find, R1-callees, R1-tests-file, R1-top-level-throws |
| R2 | R2-type-not-name-source, R2-type-not-name-test, R2-no-tests-pattern |
| A1 | A1-shared-and-varies |
| A2 | A2-computed-member |
| A3 | A3-user-pattern-outside-test-folder, A3-same-name-helper-not-counted |
| A5 | A5-default-text |
| L1 | L1-computed-member, L1-no-blanket-limit |

Negative tests reject each of the five relationship failures in the repair brief using contract/source checks alone, without relying on an unrelated case equality: sibling text, flow text, chain endpoints, test paths/call sites, and command-inappropriate sections. Additional cases reject an `unclear` classification for known sibling rows, missing dynamic limits, same-name helper false positives, and blanket limits. Integration checks use malformed stdout for R1/R3 to establish that answer content does not influence those verdicts, and compare every other requirement's status after a marker, exit or filesystem fault. Raw filesystem changes remain available; the deliberate R1 marker is counted only in R1.

Reports show `MET (tool part)` beside the unchecked parts for R3, A2, A3 and A5. R1 runtime marker observations remain **bundled only**; held-out R1 cases do not claim a marker check. The ambient test-API renaming conflict and existing interface questions are in [SPEC_QUESTIONS.md](SPEC_QUESTIONS.md).

Final required command results (2026-10-15), run serially from `code_map/`:

```text
bun test
 131 pass
 0 fail
 2365 expect() calls
Ran 131 tests across 5 files. [24.30s]

bunx tsgo --noEmit
(no output; exit 0)

bun eval/run.ts --tool "bun eval/stub/stub.ts" --cases eval/cases/fixtures.json --out /tmp/cm-eval2
Requirements: {"MET":8,"NOT MET":0,"NOT CHECKED":2}
Fails-if lines: {"MET":18,"NOT MET":0,"NOT CHECKED":2}
Cases: {"MET":52,"NOT MET":0,"NOT CHECKED":0}
Report: /tmp/cm-eval2/report.json
```

## Fixture-checkable Fails-if lines — MET

- **R1** — mapping a fixture whose top level writes a marker creates that marker.
  Cases: R1-map, R1-chain, R1-tests, R1-callers, R1-where, R1-find, R1-callees, R1-tests-file, R1-top-level-throws.
- **R2** — an implementation the lookup finds has no link.
  Cases: R2-all-implementations, R2-type-not-name-source.
- **R2** — a declaration is presented as proof of an implementation.
  Cases: R2-declaration.
- **R2** — a test fake is unlabelled or presented as the real implementation.
  Cases: R2-test-fake.
- **R2** — an unresolved or ambiguous target is unmarked.
  Cases: R2-ambiguous, R2-unresolved, R2-type-not-name-test, R2-no-tests-pattern.
- **R3** — protected content leaves the machine or enters git.
  Cases: R3-offline.
- **A1** — a claim lacks its location or contradicts the code, or a checked example misses a known item.
  Cases: A1-module-siblings, A1-no-sibling-rule, A1-map-link-flow, A1-known-callers, A1-known-callees, A1-shared-and-varies.
- **A2** — a known place is not found.
  Cases: A2-find-known.
- **A2** — an ambiguous match is treated as certain, or a candidate not built is not named.
  Cases: A2-ambiguous-find, A2-ambiguous-callers, A2-effect-step-ambiguous.
- **A2** — a known link within the depth is missing, or a shown link contradicts the code.
  Cases: A2-known-chain, A2-default-six-down, A2-default-six-up, A2-explicit-depth, A2-computed-member, A2-inline-generator-owner, A2-same-name-helper-fake, A2-shorter-route-down, A2-shorter-route-down-reversed, A2-shorter-route-up, A2-shorter-route-up-reversed.
- **A2** — a link lacks its kind or location.
  Cases: A2-link-kind-location.
- **A2** — a function reached twice is shown twice.
  Cases: A2-shared-once, A2-recursion.
- **A3** — the count differs from the list, or a link lacks its evidence.
  Cases: A3-count-evidence, A3-same-name-helper-not-counted.
- **A3** — a test with a known path is missing.
  Cases: A3-known-path, A3-fake-unset, A3-fake-count, A3-fake-exclude, A3-user-pattern-outside-test-folder.
- **A3** — static links are called coverage.
  Cases: A3-static-label.
- **A3** — the per-function file report runs without the user's request.
  Cases: A3-no-file-report.
- **A5** — an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked.
  Cases: A5-specific-answer, A5-default-text, A5-exact-callees, A5-exact-not-found, A5-exact-depth-stop.
- **L1** — a branch stops early without a reason, or an empty result is presented as proof of absence.
  Cases: L1-empty, L1-dynamic, L1-outside-repository, L1-depth-zero, L1-computed-member, L1-no-blanket-limit.

## Fails-if lines — NOT CHECKED

- **A6:** fewer than three modules are mapped, or a map fails A1. No opencode module case files were supplied.
- **L2:** it leaves out correctness, the build cost, the reading tokens or the time, or hides a worse result. P5 performs the cost comparison; this evaluator does not measure it.

## Parts outside these tool checks — NOT CHECKED

- **A2:** the agent selecting a candidate and naming the others belongs to P6.
- **A3:** the agent asking the user before a per-function report belongs to P6.
- **A5:** whether the agent requested an unasked whole map belongs to P6.
- **R3:** isolation and file snapshots do not prove absence of caught connection attempts, transmissions by other processes, downstream training use, or changes outside the observed trees. `unshare -rn` worked for this run. If unavailable, the evaluator reports R3 NOT CHECKED.

The fixture test sources use `*.testcase.ts` and `*.specimen.ts`, named explicitly by `--tests`, so Bun does not discover or execute them as evaluator tests. The marker source is deliberately imported only by the negative integration check, which asserts detection and removal.

## P2R2 — functions held in constants (2026-10-15)

Eight new cases (60 total): `A2-const-chain`, `A2-const-chain-through`, `A2-const-callers`,
`A2-const-callees`, `A3-const-tests`, `A1-const-map`, `A2-const-find-comment`,
`A2-const-find-string`.

`const-held/` includes constant arrows, a constant function expression, an Effect-like `fn` generator wrapper,
an object property arrow and `Service.of({ get })`. The chain is
`start → submit → compute → get → svc.get → deepest`; the single test reaches `deepest` through all six links.
Only `submit` is an exported entry called from outside the mapped `module/` folder. Its map expectations check
the decision and return steps in source order. Separate description queries match only a comment or a string
inside `deepest`.

The new helper exposed a held-out renaming defect: the local parameter `value` caused the generator to rename
`IteratorResult.value`. The generator now consults TypeScript symbols when transforming source property accesses
and preserves members declared in declaration files. All eleven fixture tsconfigs type-check for held-out seeds
0, 1 and 49271. Checks also verify the rewritten shorthand binding, Effect wrapper, search words, locations and
canned witnesses. Eighteen new mutation checks reject omissions, anonymous holder names, lost/reordered entry
steps, and false caller attribution to the shorthand. Checker author: P2 Codex; these checks validate the
evaluator and its canned answers, not an independent implementation or correctness on opencode.

Required commands, run serially from `code_map/`:

```text
bun test test/eval
 157 pass
 0 fail
 2896 expect() calls
Ran 157 tests across 5 files. [16.75s]

bunx tsgo --noEmit
(no output; exit 0)

bun eval/run.ts --tool "bun eval/stub/stub.ts" --cases eval/cases/fixtures.json --out eval/.const-held-check
Requirements: {"MET":8,"NOT MET":0,"NOT CHECKED":2}
Fails-if lines: {"MET":18,"NOT MET":0,"NOT CHECKED":2}
Cases: {"MET":60,"NOT MET":0,"NOT CHECKED":0}
```

The temporary report directory was removed after checking the totals. Results are recorded here because the
brief restricts writes to `eval/` and `test/eval/`. A6 and L2 remain NOT CHECKED; the existing tool/agent/privacy
limits still apply. No package was added, and edits are confined to those two directories.

## P3 — A5/A2 evaluator strengthening (2026-10-16)

Checker author: P3 Codex. Ten new cases (70 total) and their canned witnesses were written from fixture source and the unchanged requirements/spec. These tests check evaluator discrimination and stub consistency; they do not establish the builder's correctness on real projects. No existing fixture was edited. The only changes to existing case expectations are the requested text exclusion and exact empty-link equality.

The exact Fails-if lines used below are:

- **A5:** “an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked”
- **A2 links:** “a known link within the depth is missing, or a shown link contradicts the code”
- **A2 ambiguity:** “an ambiguous match is treated as certain, or a candidate not built is not named”

| New case | Requirement / Fails-if above | Wrong answer rejected |
|---|---|---|
| A5-exact-callees | A5 | Wrong caller, site or target; extra links; unasked map, chain, tests or matches section; missing limits. |
| A5-exact-not-found | A5 | Not-found accompanied by an extra reason, or replaced/omitted. |
| A5-exact-depth-stop | A5 | Wrong or missing depth stop, expansion beyond down one, or an upward branch despite up zero. |
| A2-inline-generator-owner | A2 links | Service call inside the unheld generator attributed to the surrounding named function, or evidence split across links. |
| A2-same-name-helper-fake | A2 links | Unrelated same-named helper or test fake presented as the real target; helper added to candidates. |
| A2-effect-step-ambiguous | A2 ambiguity | One same-named Effect.fn step selected as certain, or a candidate/location omitted. |
| A2-shorter-route-down | A2 links | Long-first discovery suppresses the tail reachable at down depth three through the shorter route. |
| A2-shorter-route-down-reversed | A2 links | Same missing tail with the root's call order reversed in source. |
| A2-shorter-route-up | A2 links | Long-first discovery suppresses the tail reachable at up depth three through the shorter route. |
| A2-shorter-route-up-reversed | A2 links | Same missing tail with caller declarations reversed in source. |

Each new case has an integration test requiring MET from the actual bundled stub process and NOT MET from a process printing its targeted changed witness. The four missing-tail mutations retain valid sites, connected links, levels and seen references and pass the general contract; the new expectations reject them. After the repair below, link shapes keep each caller/site/target together while allowing optional fields and unordered candidate lists. The depth-three link shape is independent of output sibling order; positive checks reverse each canned tree's siblings. The contract indexes shown functions before checking seen references, rejects duplicate full occurrences and dangling references, and permits a shared function's full expansion later in the serialized tree.

`A2-computed-member` now rejects an invented, contract-valid link while retaining its dynamic limit. `A5-default-text` excludes `chain/logic.ts:4` (`recursive`, unrelated to `leaf`). Matcher tests cover present and absent locations for both includes and excludes, path suffixes, escaped filenames and line-number prefixes. Text paths select no JSON section; the check searches the stdout place.

Held-out tests use temporary directories outside the repository, remove them afterward, type-check all sixteen generated fixture projects for seeds 0, 1 and 49271, and compare renamed identifier tokens/relocated lines with written sources. Explicit checks cover the new exact query, text/JSON exclusions, duplicate Effect.fn names, and all four route fixtures. Both generated case expectations and transformed witnesses use generator helpers; their agreement alone is not independent evidence.

Files changed (relative to `code_map/`):

- Existing evaluator files: `eval/matcher.ts`, `eval/contract.ts`, `eval/holdout.ts`, `eval/cases/fixtures.json`, `eval/README.md`, `eval/COVERAGE.md`.
- Tests: `test/eval/matcher.test.ts`, `test/eval/holdout.test.ts`, new `test/eval/strengthen.test.ts`.
- `eval/fixtures/answer-scope/`: `logic.ts`, `tsconfig.json`.
- `eval/fixtures/effect-inline/`: `api.ts`, `effect.ts`, `live.ts`, `use.ts`, `tsconfig.json`.
- `eval/fixtures/effect-shadow/`: `api.ts`, `effect.ts`, `fake.testcase.ts`, `helper.ts`, `live.ts`, `use.ts`, `tsconfig.json`.
- `eval/fixtures/effect-twins/`: `effect.ts`, `one.ts`, `two.ts`, `tsconfig.json`.
- `eval/fixtures/route-depth/`: `down.ts`, `down-reversed.ts`, `up.ts`, `up-reversed.ts`, `tsconfig.json`.
- Ten new `eval/stub/answers/<case-id>.json` files, one for each new case in the table. Existing canned files are unchanged.

Original strengthening checks from `code_map/` (before the repair below):

```text
bun test test/eval
 183 pass
 0 fail
 4209 expect() calls
Ran 183 tests across 6 files. [24.24s]

./node_modules/.bin/tsgo --noEmit
(no output; exit 0)

bun eval/run.ts --tool "bun eval/stub/stub.ts" --out /tmp/cm-strengthen-eval-20261016
Requirements: {"MET":8,"NOT MET":0,"NOT CHECKED":2}
Fails-if lines: {"MET":18,"NOT MET":0,"NOT CHECKED":2}
Cases: {"MET":70,"NOT MET":0,"NOT CHECKED":0}
Report: /tmp/cm-strengthen-eval-20261016/report.json
```

The scratch report was removed after its results were recorded here. Hash comparisons with the pre-change files confirmed unchanged `src/`, existing fixture files and tests outside `test/eval/`. A structural comparison of all sixty existing cases confirmed exactly the two authorized expectation additions. No package was installed and no held-out copy was written in the repository. A6/L2 and the documented agent/privacy portions remain NOT CHECKED.

## P3 — repair spec-allowed answer rejection (2026-10-16)

Checker author: Codex. Nine of the ten P3 cases now use `expect.shapes` for links, chains or matches. This pins each link's caller, site, target, resolution, kind, via and complete candidate list together, while permitting extra object fields and any array order. Loc's `endLine` and Link's `declaration` are optional in the spec; neither is required by these shapes. The unheld generator's name is omitted from its caller shape because the spec defines holder names but leaves unheld-body names open. Its location and kind remain fixed. `equals` retains its original behavior, and all sixty earlier cases and all canned witnesses are unchanged.

The depth-one case requires its branch stop to have reason `depth` and no children, and its upward list to be empty. `exactLimitReasons: ["depth"]` rejects any other reason across stops and top-level limits, permitting the depth reason to appear only at the required branch stop or also in a top-level summary. The spec requires the branch stop but does not prescribe repetition in the summary. The not-found case is unchanged: `limits[].reason` still equals exactly `["not-found"]`.

Each new case has an integration check for the bundled stub, a source/spec-derived permitted variant, and a targeted wrong answer. Variants add optional locations/declarations and node metadata, reorder candidates/matches and chain siblings, annotate depth stops, and change the unheld-body name. Additional checks reject missing/extra links or candidates, evidence split over links, changed endpoints/sites/holder names, missing/wrong/extra limit reasons, deeper children, upward branches and missing tails. The missing-tail mutations still pass the general contract, so their NOT MET verdict tests the case expectations. Matcher tests exercise one-to-one unordered matching even with overlapping shapes. Held-out tests relocate the new shapes and check all transformed witnesses for the existing three seeds. These are checks written by Codex; stub consistency and fixture tests do not establish correctness on other projects or provide independent validation of the evaluator.

Files changed by this repair, relative to `code_map/`:

- `eval/matcher.ts`, `eval/case-file.ts`, `eval/run.ts`, `eval/holdout.ts`: optional shape/reason matching, validation, exercised-case detection and shape relocation.
- `eval/cases/fixtures.json`: nine new case expectations; `A5-exact-not-found` and the sixty earlier cases are unchanged.
- `test/eval/matcher.test.ts`, `test/eval/strengthen.test.ts`, `test/eval/holdout.test.ts`.
- `eval/README.md`, `eval/COVERAGE.md`.

Final verification from `code_map/`:

```text
bun test test/eval
 190 pass
 0 fail
 4291 expect() calls
Ran 190 tests across 6 files. [24.88s]

./node_modules/.bin/tsgo --noEmit
(no output; exit 0)

bun eval/run.ts --tool "bun eval/stub/stub.ts" --out /tmp/cm-strengthen-eval-fix-stub-20261016
Requirements: {"MET":8,"NOT MET":0,"NOT CHECKED":2}
Fails-if lines: {"MET":18,"NOT MET":0,"NOT CHECKED":2}
Cases: {"MET":70,"NOT MET":0,"NOT CHECKED":0}
(exit 0)

bun eval/run.ts --tool "bun src/cli.ts" --out /tmp/cm-strengthen-eval-fix-real-20261016
Requirements: {"MET":7,"NOT MET":1,"NOT CHECKED":2}
Fails-if lines: {"MET":17,"NOT MET":1,"NOT CHECKED":2}
Cases: {"MET":68,"NOT MET":2,"NOT CHECKED":0}
(exit 1: A2's missing-link line fails)
```

The real CLI's results for the ten new cases:

| Case | Verdict | Mismatch |
|---|---|---|
| A5-exact-callees | MET | None. |
| A5-exact-not-found | MET | None. |
| A5-exact-depth-stop | MET | None. |
| A2-inline-generator-owner | MET | None. |
| A2-same-name-helper-fake | MET | None. |
| A2-effect-step-ambiguous | MET | None. |
| A2-shorter-route-down | NOT MET | Tail at `route-depth/down.ts:8` is absent from `chain.down[].children[].link.to`; the selected depth-three link is `routeShared` (line 6, site 6) → `routeLeaf` (line 7), instead of `routeLeaf` (line 7, site 7) → `routeTail` (line 8). |
| A2-shorter-route-down-reversed | MET | None. |
| A2-shorter-route-up | NOT MET | Tail at `route-depth/up.ts:5` is absent from `chain.up[].children[].link.from`; the selected depth-three link is `routeLeaf` (line 4, site 4) → `routeShared` (line 3), instead of `routeTail` (line 5, site 5) → `routeLeaf` (line 4). |
| A2-shorter-route-up-reversed | MET | None. |

Why those two answers violate the unchanged spec (source/spec reading by Codex): down depth three includes `routeRoot` → `routeShared` → `routeLeaf` → `routeTail`; up depth three includes the callers `routeRoot` ← `routeShared` ← `routeLeaf` ← `routeTail`. The CLI first expands the longer route through `routeA`, then stops at `routeShared` on the shorter route with `seen`. That omits the tail link within the requested depth, triggering A2's exact Fails-if line above. The check remains strict on that missing link; accepting optional metadata cannot supply it.

Both scratch reports were removed after these results were recorded. A before/after content-hash comparison found changes only in the ten repair files listed above: no `src/`, fixture source, canned answer, package, or other test changed. The sixty earlier case objects also compare equal structurally. No package was installed and no held-out copy was left in the repository. A6/L2 and the documented agent/privacy portions remain NOT CHECKED.
