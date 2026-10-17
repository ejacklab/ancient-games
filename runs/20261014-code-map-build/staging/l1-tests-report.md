# L1 staged CLI tests — results

My reading: the copied tool has four reproducible failures in 29 tests (25 pass). Exit status: 1.

Codex wrote these checks. They exercise the CLI on controlled source fixtures; passing them is not independent evidence of L1 compliance on every repository or stopping path. The failures below are observed output from the copied tool.

## Deliverable and reproduction

- Tests: `test-l1/limits.test.ts` and `test-l1/walk-budget.test.ts`, with inputs under `test-l1/fixtures/`.
- Runnable package snapshot: `cm-copy-l1/`, copied from `code_map/` at the start of this task without node_modules. Its node_modules symlink is `../../../../code_map/node_modules`.
- Run from `cm-copy-l1/`: `bun test test/l1`.
- Complete output: `l1-run.log`. Group outputs: `l1-search.log`, `l1-stops.log`, `l1-empty.log`, `l1-walk.log`.
- All 15 deliverable files match the runnable copy byte for byte. Generated fixture directories are removed in finally blocks and none remain after the run.
- Four fixture projects: `service-search`, `service-stops`, `direct-stops`, and `service-long-walk`. `service-stops` and `service-long-walk` use Context.Service, injected yield* service calls, and Effect.fn implementations (half of the fixture projects). `service-search` also uses Effect.fn.
- The generated walk fixtures use 450 functions in both a long chain and a wide queue, plus a short control. No target-project code is executed.

## Fails-if coverage and exact test names

Each name quotes the applicable part of L1: "a branch stops early without a reason" and/or "an empty result is presented as proof of absence". Empty-result tests run both JSON and default text. Positive scoped wording checks allow denials such as "this is not proof of absence".

| Result | Exact test name |
|---|---|
| FAIL | L1 find ranked names retain comment/string matches or explain omissions — Fails if: "a branch stops early without a reason" |
| PASS | L1 find delayed vault control reads service comments/strings — Fails if: "a branch stops early without a reason" |
| PASS | L1 find retention ledger control reads service comments/strings — Fails if: "a branch stops early without a reason" |
| PASS | L1 callees applyCallback locates its dynamic stop — Fails if: "a branch stops early without a reason" |
| PASS | L1 callees chooseRoute locates its dynamic stop — Fails if: "a branch stops early without a reason" |
| PASS | L1 callees roundInvoice locates its outside-repo stop — Fails if: "a branch stops early without a reason" |
| PASS | L1 callees missingReceipt locates its not-found stop — Fails if: "a branch stops early without a reason" |
| FAIL | L1 map keeps the computed service call's dynamic limit — Fails if: "a branch stops early without a reason" |
| PASS | L1 chain locates an unresolved service branch — Fails if: "a branch stops early without a reason" |
| PASS | L1 chain service down-depth marks the truncated branch — Fails if: "a branch stops early without a reason" |
| PASS | L1 chain direct up-depth marks the truncated branch — Fails if: "a branch stops early without a reason" |
| PASS | L1 chain zero-depth locates the stop at the selected service — Fails if: "a branch stops early without a reason" |
| PASS | L1 chain up cycle names the previously shown location — Fails if: "a branch stops early without a reason" |
| PASS | L1 chain down cycle names the previously shown location — Fails if: "a branch stops early without a reason" |
| PASS | L1 find missing query names not-found and qualifies emptiness — Fails if: "a branch stops early without a reason"; "an empty result is presented as proof of absence" |
| PASS | L1 where missing query names not-found and qualifies emptiness — Fails if: "a branch stops early without a reason"; "an empty result is presented as proof of absence" |
| PASS | L1 callers missing query names not-found and qualifies emptiness — Fails if: "a branch stops early without a reason"; "an empty result is presented as proof of absence" |
| PASS | L1 callees missing query names not-found and qualifies emptiness — Fails if: "a branch stops early without a reason"; "an empty result is presented as proof of absence" |
| PASS | L1 chain missing query names not-found and qualifies emptiness — Fails if: "a branch stops early without a reason"; "an empty result is presented as proof of absence" |
| PASS | L1 tests missing query names not-found and qualifies emptiness — Fails if: "a branch stops early without a reason"; "an empty result is presented as proof of absence" |
| PASS | L1 map missing query names not-found and qualifies emptiness — Fails if: "a branch stops early without a reason"; "an empty result is presented as proof of absence" |
| PASS | L1 callers existing idle service scopes its empty result in JSON and text — Fails if: "an empty result is presented as proof of absence" |
| PASS | L1 callees existing idle service scopes its empty result in JSON and text — Fails if: "an empty result is presented as proof of absence" |
| PASS | L1 chain existing idle service scopes its empty result in JSON and text — Fails if: "an empty result is presented as proof of absence" |
| PASS | L1 tests existing idle service scopes its empty result in JSON and text — Fails if: "an empty result is presented as proof of absence" |
| PASS | L1 tests short generated service graph control reaches the target — Fails if: "a branch stops early without a reason" |
| FAIL | L1 tests 450-function linear service walk finds the test or locates its budget stop — Fails if: "a branch stops early without a reason" |
| FAIL | L1 tests 450-function wide service walk finds the test or locates its budget stop — Fails if: "a branch stops early without a reason" |
| PASS | L1 chain default depth marks a longer generated service route — Fails if: "a branch stops early without a reason" |

## Observed failures

- **L1 find ranked names retain comment/string matches or explain omissions — Fails if: "a branch stops early without a reason"**: Only archiveParcel is returned. queuedDispatch and auditDispatch match the same description in a comment and a string; limits is empty. Their individual description controls pass.
- **L1 map keeps the computed service call's dynamic limit — Fails if: "a branch stops early without a reason"**: map workflow.ts has no dynamic limit at workflow.ts:15 (routes[key]()). The corresponding callees test passes. Limits for other sites and the missing sibling rule do not explain this omitted call.
- **L1 tests 450-function linear service walk finds the test or locates its budget stop — Fails if: "a branch stops early without a reason"**: The generated linear graph has a static test-to-target route. tests ledgerTarget reports zero tests and limits is empty. The copied reachableFrom implementation stops after 400 visits. The short generated service graph control passes.
- **L1 tests 450-function wide service walk finds the test or locates its budget stop — Fails if: "a branch stops early without a reason"**: The generated wide graph has a static test-to-target route. tests ledgerTarget reports zero tests and limits is empty. The copied reachableFrom implementation stops after 400 visits. The short generated service graph control passes.

## Last lines of the full run

```text

 25 pass
 4 fail
 255 expect() calls
Ran 29 tests across 2 files. [20.22s]
```
