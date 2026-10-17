# Code-map evaluation

P2 Codex evaluator; authored independently of the future tool builder

MET records the fixture/case checks assigned to this evaluator, not a proof for all repositories. Canned-stub results test the evaluator, not a real code-map tool.

| Requirement | Status |
|---|---|
| R1 | MET |
| R2 | MET |
| R3 | MET |
| A1 | MET |
| A2 | MET |
| A3 | MET |
| A5 | MET |
| A6 | NOT CHECKED |
| L1 | MET |
| L2 | NOT CHECKED |

## Fails-if lines

- **R1 MET** — mapping a fixture whose top level writes a marker creates that marker. Cases: R1-map, R1-chain, R1-tests, R1-callers.
- **R2 MET** — an implementation the lookup finds has no link. Cases: R2-all-implementations.
- **R2 MET** — a declaration is presented as proof of an implementation. Cases: R2-declaration.
- **R2 MET** — a test fake is unlabelled or presented as the real implementation. Cases: R2-test-fake.
- **R2 MET** — an unresolved or ambiguous target is unmarked. Cases: R2-ambiguous, R2-unresolved.
- **R3 MET** — protected content leaves the machine or enters git. Cases: R3-offline.
- **A1 MET** — a claim lacks its location or contradicts the code, or a checked example misses a known item. Cases: A1-module-siblings, A1-no-sibling-rule, A1-map-link-flow, A1-known-callers, A1-known-callees.
- **A2 MET** — a known place is not found. Cases: A2-find-known.
- **A2 MET** — an ambiguous match is treated as certain, or a candidate not built is not named. Cases: A2-ambiguous-find, A2-ambiguous-callers.
- **A2 MET** — a known link within the depth is missing, or a shown link contradicts the code. Cases: A2-known-chain, A2-default-six-down, A2-default-six-up, A2-explicit-depth.
- **A2 MET** — a link lacks its kind or location. Cases: A2-link-kind-location.
- **A2 MET** — a function reached twice is shown twice. Cases: A2-shared-once, A2-recursion.
- **A3 MET** — the count differs from the list, or a link lacks its evidence. Cases: A3-count-evidence.
- **A3 MET** — a test with a known path is missing. Cases: A3-known-path, A3-fake-unset, A3-fake-count, A3-fake-exclude.
- **A3 MET** — static links are called coverage. Cases: A3-static-label.
- **A3 MET** — the per-function file report runs without the user's request. Cases: A3-no-file-report.
- **A5 MET** — an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked. Cases: A5-specific-answer.
- **A6 NOT CHECKED** — fewer than three modules are mapped, or a map fails A1. Cases: none.
  - No opencode case files for the three modules were supplied.
- **L1 MET** — a branch stops early without a reason, or an empty result is presented as proof of absence. Cases: L1-empty, L1-dynamic, L1-outside-repository, L1-depth-zero.
- **L2 NOT CHECKED** — it leaves out correctness, the build cost, the reading tokens or the time, or hides a worse result. Cases: none.
  - P5 measures cost against reading; this evaluator does not measure L2.

## Failures

## Parts not checked

- **A2 NOT CHECKED** — P6 checks the agent's selection and naming of candidates it did not build.
- **A3 NOT CHECKED** — P6 checks whether the agent asks the user before requesting a per-function file report.
- **A5 NOT CHECKED** — P6 checks whether the agent requests a whole map without being asked.
- **R3 NOT CHECKED** — Network isolation and filesystem snapshots do not establish absence of caught connection attempts, transmission by other processes, or downstream training use.

## Totals

```json
{
  "requirements": {
    "MET": 8,
    "NOT MET": 0,
    "NOT CHECKED": 2
  },
  "lines": {
    "MET": 18,
    "NOT MET": 0,
    "NOT CHECKED": 2
  },
  "cases": {
    "MET": 37,
    "NOT MET": 0,
    "NOT CHECKED": 0
  }
}
```
