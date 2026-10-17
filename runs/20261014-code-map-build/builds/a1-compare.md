# Round A1, round 1 — opencode against dsh, same brief, same base

Both builders started at the same time from the same base: the A2 code plus the 29 A1 tests. Each worked in its own
copy and had 35 minutes. The checks below are the same for both. Script: `scripts/compare_build.py`, written by the
COO. Raw output: `compare-opencode.json`, `compare-dsh.json`.

| Measure | opencode (MiniMax-M3.1-Flash-Preview) | dsh (headless profile, default model) |
|---|---|---|
| Wall time | 1,117 s | 1,123 s |
| Files changed in `src/` | 4 | 4 |
| Lines added to `src/` (base 1,944) | +69 | +114 |
| Ran git | no | no |
| Wrote outside its `src/` | its evaluator output, under `node_modules/.cm-round-opencode` (the brief allowed it) | the same, `.cm-round-dsh` |
| `bun test` | 293 pass, 0 fail | 293 pass, 0 fail |
| `tsgo` | exit 0 | exit 0 |
| Evaluator, bundled cases | all MET (A6, L2 not checked) | the same |
| Held-out copy (renamed) | no NOT MET, 61 of 70 cases MET | the same |
| Private opencode core set | 6 of 8 cases MET; A1 and A2 NOT MET | the same 6 of 8 |
| Private opencode ai set | 2 of 2 | 2 of 2 |
| Its own report | done at 16:08Z, with its own held-out copies | done at 16:03Z, then a final line at 16:08Z; it flagged the two test-file type errors as not its own |

## Real opencode maps (`probe-*.json`)

| Module | Measure | A5 tool | opencode | dsh |
|---|---|---|---|---|
| session | links resolved | 1,084 | 1,267 | **1,327** |
| session | unresolved, not "outside" | 169 | 103 | **10** |
| tool | links resolved | 410 | **437** | 436 |
| ai | links resolved | 3,049 | **3,617** | 3,478 |
| ai | ambiguous | 31 | 72 | 75 |

- **The links the P4 judges found wrong:** both builds now resolve all four checked ones (steps.attempt,
  StepFailedError, DeclinedError, Auth.header).
- **Still open in both:**
  - `transport.prepare` is now ambiguous with 2 candidates, where the judge found 3;
  - the sibling tables still have 0 rows on the real tool and ai modules.
- More links resolved does not mean more correct. No one checked the extra links.

## Pick (the COO's, provisional)

**opencode.** On every check that can fail, the two builds are level. opencode resolves more links in total (5,321
against 5,241) with a smaller change. opencode also has build priority by EJ's rule of 2026-10-04. dsh's build is
kept in `builds/a1-dsh/` for round 2.

## Found while comparing

- **A private case was wrong — the COO's error, not either builder's.** `OC-M1-callees-attempt` expected the call at
  step.ts:94 among `attempt`'s direct callees. That call sits inside the arrow `executeTool` (step.ts:91), and the spec
  names the nearest enclosing function. So it is a level below. The case now expects step.ts:126, where `attempt`
  calls `executeTool`. The old file is kept as `core.v2.json`.
- **Still failing on both: `where Permission.assert`.** It returns two unrelated object properties named
  `….permission.assert`, and not the service's implementation. This is A1's "a checked example misses a known item",
  and the feedback for round 2.
