# Report — 20261014-memory-index-cleanup

EJ, 2026-10-14: *"run it, go ahead to start the cleanup"*. Run by the COO (`claude-opus-5-5`). State: `state.md`.

## Result

`tools/memory_index.py` now rejects an id not in W1.1's form `DD-MM-xxxxxx-YYYY` (B2.3) and an entry with a line
starting `<<<<<<<` or `>>>>>>>` (B2.7). Both are errors in every status, in write and check mode.

- **Where:** branch `fix/index-id-and-markers`, worktree `../ancient-games-index-clean`, 7 commits on master
  `ca8e043`. **Not merged and not pushed.**
- **Tests:** 994 pass, the full suite (*ran* at `6126804`). The baseline was 686.

## The three-part stop (method 3.6)

| Part | Result | Who wrote the check, and what it does not establish |
|---|---|---|
| New criteria pass and can fail | B2.3, B2.7 and G4.2 tests pass. 13 of 14 new mutants are killed by the acceptance file. N14 is killed by the unit file only. | The COO wrote the mutants. The mutants show the tests can fail; they do not show every behaviour is covered (see the backlog). |
| Baseline still passes | 994 pass. The gate reports 57 baseline cases "missing": they are renamed parametrizations whose names held the old ids, and all pass under their new names. The old 32 mutants match N0's control mutant by mutant. | `feature_gate.py` was written in an earlier session. The renaming was judged by the COO. |
| Must not change | `core.hooksPath` is empty. There is no `project-memory/`. The coder changed only the two allowed files (gate: scope, must-not, tamper ok). | The gate checks paths, not intent. |

## Workers

| Node | Engine | Result |
|---|---|---|
| N1 | codex `gpt-6.1-sol` high, in a code-free workspace | 1 attempt (68k tokens) plus 1 repair round (37k). Raised 3 CONTRADICTS: two were real, fixed in the spec (below); one was expected (SoT K6.3). |
| N2 | opencode `MiniMax-M3.1-Flash-Preview` high | Green on attempt 1, no CONTRADICTS. |
| N4 | Claude subagent `claude-sonnet-5-5` | Found the plant (*a marker scan cut off at 40 lines*), verified with its own probes. 8 findings in criteria, 3 outside. |

Worker calls: 4 of the 11 allowed, plus 3 canaries.

## What the COO changed that EJ has not seen

1. **The spec, `9acec67`.** B2.5 ("a problem in an inactive entry beyond B2.3 is a warning") and B2's Fails if ("a
   broken retired entry stops the build") contradicted B2.7's "an error in every status", as N1 found. Both now say
   "beyond B2.3 and B2.7". This is *the COO's wording*.
2. **SoT K6.3's Fails if, `6126804`.** It now reads "In an entry, the tool's check catches it (`docs/index-md/`
   B2.7); in `INDEX.md`, the comparison in K6.2 does." This is *proposed in the design*, for EJ to approve with the
   merge.
3. **Review fixes, `48162f0`:**
   - F3: the id error says what `x` is.
   - F4: markers are matched with `startswith`, and the comment is plain.
   - F5: every marker line is reported.
   - F6: three unit-test fixture ids are now in the form.
   
   Not done, with reasons:
   - F7: unit tests pin this script's own messages, as its older unit tests do.
   - F8 and F2: these went to the backlog.
4. **A reference patch** at N1: the old script plus the two checks. All of N1's tests passed against it. It is not
   in the design. It catches a test masked by a computed id, which the fixture lint cannot see.

## Not done

- **The requirements evaluator** did not run, because `tools/evaluator/` is not on master.
- **The ledger row** in `docs/TASK_TYPES_LEDGER.md` is not written. That file has uncommitted changes from another
  session in the main tree, so it waits for the merge.
- **Backlog:** five items, in `docs/index-md/BACKLOG.md` on the branch. Item 5 of the earlier list (a blank id) is
  closed by B2.3.

## Files

- `nodes/`: each worker's result and diff.
- `sabotage/`:
  - `control-n0.md`, `old-mutants-final.md`;
  - `new-mutants-final.json`, `n3-new-final.md`;
  - `plant-review-1.txt`, `reference-patch.json`.
- `gate-1.txt`, `gate-2.txt`, `baseline.json`, `plan.json`, `traceability.md`.
- `checks/`: `trace_check.py` (B2.7 added), `fixture_ids.py` (new), `mutate.py` (copied).
