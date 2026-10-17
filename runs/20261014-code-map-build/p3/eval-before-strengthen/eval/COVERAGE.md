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
  Cases: A2-ambiguous-find, A2-ambiguous-callers.
- **A2** — a known link within the depth is missing, or a shown link contradicts the code.
  Cases: A2-known-chain, A2-default-six-down, A2-default-six-up, A2-explicit-depth, A2-computed-member.
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
  Cases: A5-specific-answer, A5-default-text.
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
