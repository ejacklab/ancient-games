# 孫子 (Sun Tzu) — can our engines, the task, and the ground carry it?

## Answer

Of the three knowings my #4 asks for, only one is whole: **the task as posed can be done** — by my reading of the code, `parse_entry` already receives every line of every entry and is reached by both write and check mode, so the id check is one pattern and the marker check one line scan on the same always-error path as `empty id`. The **ground is half known**: the blueprint is a draft (Q2), the base ref is EJ's (Q1), and two ground facts are already wrong in the design — the pinned spec will not be in the worktree the workers use, and the reused `trace_check.py` cannot see B2.7. The **engines are the least known**: all three are installed, but none has been called this run, the Codex model id comes from a cache the readiness itself calls possibly stale, and the quota reset is a report. Do not dispatch N1 or N2 until the two canaries fire; if Codex does not answer, take the design's own exit path rather than reading the reset as proof.

Only half known, in order of danger: (1) the engines' ability to run *today* — a canary fact; (2) the ground where the workers stand — the spec and the script; (3) the blueprint — not yet accepted, so it does not yet permit the build. New spots below are written `N… (new)` to keep them apart from the design's node ids.

**Per piece, against the three knowings** (my #4: our side, their side, the ground):

| Piece | Our engines/tools | The task as posed | The ground |
|---|---|---|---|
| prep (N0) | half — canaries unrun; a worktree outside the repo untested | whole | half — Q1 base, Q2 spec, evaluator not on master |
| tests (N1) | half — Codex unrun; model id from a stale cache | half — fixture inventory unknown | half — spec edits not in the worktree; trace_check lacks B2.7 |
| code (N2) | half — opencode unrun; `--variant high` effect unknown | whole — one pattern, one line scan (my reading) | whole once N1 freezes the tests |
| sabotage (N3) | whole — `mutate.py` and `mutants.json` exist | whole — one mutant per new clause | whole, with old mutants listed, not counted |
| review (N4) | half — a `claude-sonnet-5-5` subagent is not proven this run | half — a plant the tests cannot catch is assumed | whole |
| close (N5) | half — the evaluator branch is not on master (so skipped) | whole | half — the SoT K6 sentence needs EJ's approval with the merge |

**Spot list, with my verdict for each.**

| Id | Piece | Which knowing | Verdict |
|---|---|---|---|
| Q1 | prep (N0) | ground: base ref | **Half, EJ's.** Git settles the fact: `d990dab` is on `fix/index-drop-runbooks` only, not in master. If yes, N0 must merge before the worktree — an action the design's own defaults otherwise reserve for EJ's word. If no, start from `d990dab`; the existing worktree `../ancient-games-index-r` already sits there. Cheap and reversible either way. |
| Q2 | all (N0–N5) | ground: blueprint | **Not permitted.** By the design's own rule, nothing builds until the spec says it. The spec is draft, so the ground does not yet allow N1–N5. EJ's. |
| D1 | tests/code (N1, N2) | task/blueprint | **Whole.** W1.1 gives the form and the SoT's own example `13-10-k3f7a2-2026`; form-only is a fair reading of "the shape", and a calendar check would add a false-error surface for no stated requirement. |
| D2 | tests/code (N1, N2) | task | **Whole, placement-sensitive (my reading).** The always-error path is `parse_entry`; `check_content` splits active-error from inactive-warning. Both new checks must sit on the `parse_entry` path; the active-and-retired tests are what prove it. |
| D3 | tests/code (N1, N2) | task/blueprint | **Whole.** K6.3 names exactly `<<<<<<<` and `>>>>>>>`, and does not name `=======`; excluding it also avoids a false error on a Markdown underline. |
| D4 | all | scope | **Whole, EJ's.** Not every road is taken, and the design says which are not. Its price: the blank id `" "` is closed as a side effect — say so in the report. |
| D5 | close (N5) | ground | **Half, and the condition is already false.** `build/evaluator` is not on master (it contains only itself), so the default skips the evaluator and says so. Also the design's `tools/evaluator/` does not exist; the tree is `docs/evaluator/` and the worktree `../ancient-games-evaluator`. |
| N1 (new) | tests (N1) | our means | **Half — the danger spot.** Codex is installed, but no call was made; the `gpt-6.1-sol` id is reported from a cache the readiness calls possibly stale; the quota reset is reported; readiness marks "codex executes a task: unknown". Probe: N0's canary, `</dev/null`, output naming model and effort. |
| N2 (new) | code (N2) | our means | **Half.** opencode is installed; the earlier `--variant high` was "accepted" but whether it changes anything is unknown (U4). Probe: the opencode canary, naming the model and the variant. |
| N3 (new) | tests/code (N1, N2) | ground: files | **Half — the sharpest ground defect.** `docs/index-md/` is tracked and clean on master, so a worktree from `<start>` holds the *old* B2.3/G4.2 and no B2.7; N0's Q2 edits stay uncommitted in the main tree. The design never says how the workers get the pinned spec, and N1's worktree removes the script while the red-against-old check needs it. Name where each file lives — e.g. copy the pinned spec into the worktree's `raw/inputs/`, as the earlier run did (my #16: an unclear order is the commander's fault). |
| N4 (new) | tests/sabotage/close (N1, N3, N5) | our means | **Half — one check cannot fire as written.** `runs/20261012-index-md-build/checks/trace_check.py` hard-codes its in-scope ids and has no `B2.7`, so the design's own sabotage (remove the B2.7 citation, expect failure) cannot work. N1 may change only the test file, so the COO must extend the check. Paths too: `checks/…` is under the old run folder; `feature_gate.py` is under `skills/workflow-design/scripts/`; `baseline` needs `--junit` and `--out`. |
| N5 (new) | tests (N1) | task: information | **Half.** The fixture inventory is not given: which ids exist, which tests depend on an id's shape (duplicate, prefix/kind, sort), and which bad ids are intentional (`id: ""`) and must not be "converted". "Change every fixture id" is over-broad as written; N1's red-against-old run is the check. |
| N6 (new) | review (N4) | our means/task | **Half.** This run's readiness never proves a `claude-sonnet-5-5` subagent; the earlier run's success is reported. And "a plant the tests cannot catch" is assumed, not shown — for two simple checks the plant may have to sit outside the criteria, which is a different review. Probe: a trivial read-only Sonnet call; write the plant only after N2's code exists. |
| N7 (new) | prep (N0) | ground: the machine | **Half.** The design puts the worktree at `../ancient-games-index-clean`, outside the repo. The earlier `../ancient-games-index-md` exists, but that is another session's precedent, not a test now, and my reading of this session's file policy is workspace-write to the repo root. Probe: the `git worktree add` itself; on refusal, use an in-repo path. |

## How I decided

1. I took the question as my #4's three tests — whether our troops can attack (engines and tools), whether the enemy can be attacked (the task as posed), and whether the ground permits battle (files, blueprint, information) — and looked for a piece missing each of the three, not for a single pass or fail.
2. I put our own side first (my #2): I separated what the run owns (the installed tools, the repo, the pinned hashes) from what depends on the other side (the model cache, the quota, another session's evaluator).
3. I counted before committing (my #1): the design counts steps, tests, mutants and cost, but not one *called* engine. By that rule more calculation wins and none is worst; the reckoning of means here is a report, not a count.
4. I separated foreknowledge from report (my #11): the quota reset and the model id come from a cache and a commit message — my list calls those likeness and measurement — and it says foreknowledge must come from the thing that knows. The canary is that thing.
5. I probed the ground rather than trusting the design's parentheses (my #17): I read the tracked files, the branches, the scripts and the code. Three ground assumptions are already false or loose: the evaluator is not on master; `trace_check.py` has no B2.7; the spec edits will not be in the worktree.
6. I checked the task against the code (my #4's second half): `parse_entry` receives every line in both modes and is the always-error path; the two checks are one pattern and one line scan. This is the one knowing I can call whole.
7. I mixed harm into the benefit of each default (my #6): the calendar check (D1), `=======` (D3), the blank id (D4). Each default's price is now named.
8. I did not drop a spot (my #13): not every road is taken, but a road is EJ's to leave, not mine.
9. I gave each recommendation a probe and a stop (my #8): the canary, the worktree command, the copy of the spec, the extended trace check — each cheap, reversible, and needing no new engine call.

## What I need to know

- **For EJ:** Q1 and Q2, the two the design already asks. My answer is conditional on both.
- **Not for EJ, for the COO — probes, not questions:** the Codex and opencode canary outputs; whether this session's file policy allows `git worktree add ../ancient-games-index-clean`; the fixture-id inventory in `tests/test_memory_index.py`.
- Nothing else. I was given the design, the spec status and the tool list; where I used the repo, I read it.

## Costs and risks

- Reading the reported reset as proof the engine is back: the run stalls at N1 and burns a prep attempt (my #2, my #11).
- The stale model cache: `gpt-6.1-sol` may not be offered; the canary's first line is the cheap exposure (my #1).
- The spec not in the worktree: N1 writes tests to the old B2.3 and the run is green and wrong (my #4 — the ground half; my #6).
- `trace_check.py` without B2.7: a criterion can be forgotten and the check still passes (my #4 — a check that cannot be shown failing is not a check).
- The worktree outside the repo: a denied command costs a prep attempt, not the run (my #8 — clumsy speed is heard of; a stalled start is not).
- The unknown `--variant high`: the coder may run at default effort while the record claims high (my #18 — manage strength; do not let the record overstate the worker).
- "Change every fixture id": it can change what a test asserts without changing its name (my #6).
- A plant that cannot exist: the review's only check disappears (my #4).

## How we would know I was right

- The two canaries exit 0, each naming its model — and `--variant high` for opencode.
- The pinned spec's sha256 inside the worktree equals N0's, and `trace_check.py` fails on a copy with the B2.7 citation removed.
- The red-against-old run shows exactly the new tests red and the baseline green (685 on master; 686 if `d990dab` is merged), and `feature_gate.py check` passes on N2's code.
- If instead the run stalls at N1, or N1's tests cite the old B2.3, then my verdict on the means and the ground was right and the design's was not.
