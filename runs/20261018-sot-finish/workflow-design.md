# Workflow design — 20261018-sot-finish

Written 2026-10-18 02:18 by the COO (`claude-opus-5-5`) at EJ's request: *"can you get 6 experts help to auto finish
everything within 6 hours via a well plan and design workflow execution?"* A time-boxed run (method 3.8 item 14): EJ
gave 6 hours and is not asked until it ends; the COO decides from the experts' majority, provisionally, and EJ accepts
or overrules at the end. Deadline: 08:18 (`deadline start --minutes 360`). State: `state.md`.

## Scope

The open TODO items in `runs/20261014-sot-yaml-review/state.md`:

| Item | In? | Why |
|---|---|---|
| 14 — the tool reads the limits file; where it lives and its format; when the example stops; both sides change one `covers` path; measuring the engines | in | the open follow-ups of item 11 |
| 6 — secret scanner for W3.2 | in | the experts decide build or reviewer-only; a build joins the tool run |
| 5 — the COO's wording of 2026-10-14 | in | one approve-or-change round |
| 12 — W1.1b's rename check | out | EJ, 2026-10-15: "not now", until the harness-health work is solid |
| 9 — the agent test, YAML against Markdown | out | EJ chose to skip it |
| 7 — ledger row | out | `docs/TASK_TYPES_LEDGER.md` still has another session's uncommitted edits |
| `CACHES.md` correction | out | another design's document; stays a written request |

Defaults the COO set (EJ asked for full automation; said in the report): the tool change merges to master and is
pushed once its acceptance tests, the full suite, the mutants and the blind review all pass.

## Pieces, in order

| # | Piece | How | Check | Stop on failure |
|---|---|---|---|---|
| S1 | Decisions D1–D5 (below) | `experts-decide`, needsWeb (scanner tools), one round | each expert checked; `compare.md` | the majority, or "no majority" left as is |
| S2 | Item 5: approve or change the 10-14 wording | `experts-decide`, approveOrChange (card + vote) | as S1 | changes with a majority are applied |
| S3 | Apply S1 and S2 to the design | COO: `build_requirements.py`, prose, release notes | build script, `yaml_check.py`, `paths.py` | commit and push |
| S4 | Tool build (limits file; scanner if S1 says build) | worktree; spec lines in `docs/index-md/`; tests by Codex, blind; code by opencode; mutants; blind Sonnet review with a plant; merge | per node, as run `20261014-memory-index-cleanup` | two failed attempts of a node: stop that piece, report |
| S5 | Measure agy's limit, if S1 says now | sentinel files with a control, on the installed agy | the control's sentinels are all reported | report either result |
| S6 | Close | TODO, state, release notes, report to EJ | — | — |

## S1 decisions

- D1. Where the limits file lives, and its format (the tool is standard library only).
- D2. When the interim example stops applying.
- D3. Both sides change the same `covers` path: what the merge does.
- D4. Secret scanner: build (where, what it detects, standard library or an outside tool) or reviewer only.
- D5. Measure agy's start-file limit now, later, or never.

## Bounds and cost (not measured)

S1 about 20 minutes; S2 about 5; S3 10; S4 1–2 hours (the last tool run's shape); S5 15 minutes; S6 10. Total
about 2.5–3.5 hours of the 6. Agents: two expert rounds (6 + research + compare each), S4's 3–5 worker calls plus
canaries. One engine process at a time where they share a resource (opencode).

## Quality

Every decision is the experts' majority, recorded with its count; every build has a check shown able to fail;
nothing is merged that fails its tests or review; what stops is listed for EJ, never forced.
