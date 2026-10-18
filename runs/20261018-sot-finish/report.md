# Report — 20261018-sot-finish

EJ, 2026-10-18: *"can you get 6 experts help to auto finish everything within 6 hours via a well plan and design
workflow execution?"* A time-boxed run: the COO applied the experts' majority provisionally; EJ accepts or overrules.
Started 04:54 (after EJ's 100-minute timer), deadline 10:54; finished about 09:15.

## Done

| TODO item | Outcome | Where |
|---|---|---|
| 14 — limits file | `project-memory/start-limits.json`, JSON, one row per agent and unit; the tool reads it; merged | `docs/index-md/` B4.1, B4.2, B4.5; `tools/memory_index.py` |
| 14 — open rules | per unit the smallest row, a unit with no row keeps the example; both sides' new `covers` paths kept, the old removed, reported | YAML Rd3.1a, W6.3a |
| 14 — measure agy | not now: S1 tied 3 to 3; item 11's "later" (4 of 6) stands | `s1b/compare.md` |
| 6 — secret scanner | built into the tool: fixed-prefix forms, every status, both modes, never printed; reviewer for the rest | `docs/index-md/` B2.8; YAML `checks` |
| 5 — the COO's 10-14 wording | all six CHANGE: K1.1, K5.1, Rd5.2, W5.2 changed; W1.2a, W6.1a stand | `s2/compare.md`, YAML |

Out by design: item 12 (EJ: "not now"), item 9 (EJ skipped the test), item 7 (the ledger still has another
session's uncommitted edits), the `CACHES.md` correction (another design's document; a request).

## How the build was checked (S4)

| Check | Result | Who wrote it; what it does not establish |
|---|---|---|
| Tests written blind (Codex, code-free workspace), two rounds | 27 new acceptance tests; red on the code before, every older test green | Codex; the tests show what they test, no more |
| Code (opencode), two attempts + the COO's small fixes | 3917 tests pass on the branch; 4111 on master after the merge | the gate (`feature_gate.py`): tests, baseline, scope, must-not, tamper — PASS three times |
| Mutants | 29 new: 28 killed by the acceptance file, 1 by a unit test; 3 size mutants killed; old control mutants unchanged wherever they apply; rerun on the merged code, same | the COO wrote the mutants; they show the tests can fail, not that every behaviour is covered |
| Blind review (Sonnet), with a plant | found the plant (a fenced-code-block skip) and 13 real findings, all fixed or answered in the spec | the reviewer's probes are its own |
| Review of the repairs | all fixed except O1 (no requirement covers it); three small new problems, fixed by the COO | as above |

The merge met another session's change to the same function (`7020438`, memory-check fixes); the conflict was
resolved keeping both, then the suite and the check-mode mutants were rerun.

## Picks the COO made where the experts had no majority (EJ may overrule)

- The file's name `start-limits.json` (3 of 6 used it); per-unit "smallest row, else the example" (row by row 3, the
  file as a whole 2); an empty `limits` list is an error; units `lines`, `bytes`, `characters`; no waiver for B2.8.
- The review's spec questions: whole tokens (gitleaks' word boundaries), BEGIN/END lines contain the markers, line
  breaks not counted toward the 64, a BEGIN with no END is not a block, `limit` a JSON integer, text fields
  non-empty, the BEGIN line is the reported line.
- W5.2's new `fails_if` words (5 of 6 asked for a change, no common words).

## Incident

Another session started its own six-hour run at the same minute, and the guard's `deadline start` gave it this run's
deadline; this session's hook then said "time is up" and the first expert round's agents stopped. Fixed by hand in
the two deadline records; reported in the TODO (item 15). A permission check refused the relaunch once; EJ's timer
and later relaunch went through.

## Open (TODO item 15 in `runs/20261014-sot-yaml-review/state.md`)

Credential in a file name or a stale `INDEX.md` diff still printed; a flattened private key not caught; O1; O2; no
acceptance test for a folder at the limits path in check mode; the guard's deadline claim.
