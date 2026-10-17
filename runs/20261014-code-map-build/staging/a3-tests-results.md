# A3 staged test handoff

Written and run by Codex. These are checks authored for this brief, not an independent evaluator verdict or a claim about all TypeScript projects.

## Artifacts

- Source suite: `test-a3/tests-reaching-functions.test.ts`, with `test-a3/fixtures/`.
- Run directory: `cm-copy/`; `node_modules` is the requested relative symlink.
- Command: `bun test test/a3`.
- The copied tool source was not edited or refreshed after the initial copy; `code_map/` was read only.
- One of the two fixture projects uses the Effect service style, with a real implementation and a fake in a test file. Fourteen of the eighteen checks use that project.
- Both fixture projects have zero TypeScript diagnostics using the existing TypeScript dependency.
- The staged suite and the suite run in the copy match byte for byte.

## Test names and Fails-if mapping

Every test name below includes the quoted Fails-if line at runtime. A failure means the copied tool violates that check; it is intentionally left failing for the next builder.

| Test name | Fails-if line | Copied tool |
|---|---|---|
| A3 direct count counts cases, not calls — Fails if: "the count differs from the list, or a link lacks its evidence;" | the count differs from the list, or a link lacks its evidence; | PASS |
| A3 counted Effect paths retain every link's evidence — Fails if: "the count differs from the list, or a link lacks its evidence;" | the count differs from the list, or a link lacks its evidence; | PASS |
| A3 undecided Effect paths retain evidence outside the count — Fails if: "the count differs from the list, or a link lacks its evidence;" | the count differs from the list, or a link lacks its evidence; | PASS |
| A3 fake-rule count includes the real Effect implementation — Fails if: "a test with a known path is missing;" | a test with a known path is missing; | PASS |
| A3 fake-rule exclude omits fake-only paths from both lists — Fails if: "a test with a known path is missing;" | a test with a known path is missing; | PASS |
| A3 unset fake rule preserves all known service paths as undecided — Fails if: "a test with a known path is missing;" | a test with a known path is missing; | PASS |
| A3 fake-rule exclude retains the direct path to the same leaf — Fails if: "a test with a known path is missing;" | a test with a known path is missing; | PASS |
| A3 no test pattern classifies no service-project files as tests — Fails if: "a test with a known path is missing;" | a test with a known path is missing; | PASS |
| A3 explicit and repeated patterns select the service project's test files — Fails if: "a test with a known path is missing;" | a test with a known path is missing; | PASS |
| A3 direct, aliased, it and describe-nested paths exclude a same-name decoy — Fails if: "a test with a known path is missing;" | a test with a known path is missing; | PASS |
| A3 JSON uses static-path labels and no execution-claim field in every fake mode — Fails if: "static links are called coverage;" | static links are called coverage; | PASS |
| A3 default text for counted Effect tests uses only static-path wording — Fails if: "static links are called coverage;" | static links are called coverage; | FAIL — default text contains `coverage` |
| A3 default text for undecided Effect tests uses only static-path wording — Fails if: "static links are called coverage;" | static links are called coverage; | FAIL — default text contains `coverage` |
| A3 default text for direct tests uses only static-path wording — Fails if: "static links are called coverage;" | static links are called coverage; | FAIL — default text contains `coverage` |
| A3 Effect file JSON requires explicit per-function permission — Fails if: "the per-function file report runs without the user's request." | the per-function file report runs without the user's request. | PASS |
| A3 direct file JSON requires explicit per-function permission — Fails if: "the per-function file report runs without the user's request." | the per-function file report runs without the user's request. | PASS |
| A3 default text also declines the unrequested Effect file report — Fails if: "the per-function file report runs without the user's request." | the per-function file report runs without the user's request. | PASS |
| A3 explicit per-function flag enables the Effect file answer — Fails if: "the per-function file report runs without the user's request." | the per-function file report runs without the user's request. | PASS |

## Failure reason

All three failing checks reach their final forbidden-word assertion. The CLI exits successfully and returns the expected static paths or fake-rule limit, but the default-text header is:

```text
static-call-path (static links, not execution coverage): … test(s)
```

The owner’s provisional wording rule in the brief says no default-text word says "coverage" or "covered", so even the negated phrase fails. JSON field names pass. No tool implementation change was made.

## What the passing checks establish

- Count equals list length, repeated calls count as one test case, and every expected path includes source locations, ordered links, concrete targets, and typed service declaration/candidate evidence.
- Direct, aliased, helper-mediated, `it`, describe-nested, and Effect service paths appear; a same-name decoy and ordinary setup functions are not tests reaching the target.
- All three fake-rule modes behave as specified, including mixed direct/fake paths and the exact missing-rule limit.
- Test-file classification has no default; explicit and repeated glob flags select the expected files.
- The whole-file answer is withheld without `--per-function` in JSON and text; the flag enables the requested file answer.

The brief assigns the agent’s act of asking the user to another check. These tests do not assess that behavior. The spec supplies no separate per-function JSON schema; the positive opt-in check uses the documented `TestsAnswer` payload and verifies paths terminate in the requested file.

## Last lines of the completed run

```text
 15 pass
 3 fail
 3895 expect() calls
Ran 18 tests across 1 file. [10.37s]
```

Exit status: 1 (the three expected wording failures).
