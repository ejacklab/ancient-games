# 孫子 (Sun Tzu) — where memory-check belongs in the workflow-design method

## Answer

Run memory-check **once, in 3.1 Readiness** (the skill's step 1), before any piece starts — not on every node, not as a separate end-of-run pass, and not at session start only. It fills the checkable part of the memory line 3.1 already asks about; its result says what memory the run may stand on, and it should hold only the pieces that rely on broken or unjudged memory, not the run.

## How I decided

1. **The moment is the reckoning before the march (my #1, quoted).** 「多算勝，少算不勝，而況於無算乎？」 The method already gathers its read-only proofs at 3.1 — `readiness.py` for tools, `harness_health.py` for harness setup, `doctor` for hooks (`docs/WORKFLOW_DESIGN_METHOD.md` lines 102–110). A run that starts on memory nothing has counted is the "no count" case; the check belongs before 3.2, not after the work.

2. **Fix the half you own (my #2, quoted).** 「先為不可勝，以待敵之可勝。」 A run cannot make a project's memory correct by starting, but it can know before it starts which part is safe to stand on. That is why the result belongs in readiness, not in a worker's good character later.

3. **Name the empty half of 3.1 (my #4, quoted; my reading of the method).** 「知彼知己，百戰不殆」 — yet 3.1 proves the tools, the harness and the hooks, and asks about "a memory folder" in prose with no script (`docs/WORKFLOW_DESIGN_METHOD.md` lines 113–129). memory-check is that script for the part it covers: the locations, the guidelines' checkable requirements, `AGENTS.md`. It does not answer whether the knowledge *this task* needs is there; that judgement stays in 3.1. One line made checkable, not a new step.

4. **Make the addition pay for itself (my #5, quoted).** 「合於利而動，不合於利而止。」 It pays only if it adds no step and does not gate every run. So: one run, one readiness line, and the **report** is the result, not the exit code. On this repo the report is 0 fail, 3 pass (the tool's own F1–F3), 3 need a reviewer, 72 not applicable, 0 could not run (`runs/20261017-memory-check/nodes/smoke-report.md` line 128); a cache break would not even change the exit code, because `CACHES.md` gives its requirements no level (same file, line 129; `memory_check/REQUIREMENTS.md` line 73, R3). A green line here is a count, not a pass.

5. **Map each of the five states to a decision, not to a stop (my reading, from C2 and the method's 3.1/3.3/3.6).**

| result state | what 3.1 does | who acts |
|---|---|---|
| **pass** | one readiness line with the counts; carry on | readiness |
| **fail (a MUST)** | a decision spot in the 3.3 batch; provisional: carry on, name the break in the state and the report, and hold only the pieces that read or write that memory (or add a preparation piece to repair it) | EJ; in a time-boxed run, the 3.3 experts (3.8 item 14) |
| **needs a reviewer** | never counted as a pass; the ids go in the readiness line; a reviewer item a piece depends on holds that piece until the owner, or the person they name, judges it; the rest are owner questions | the owner / their named reviewer |
| **not applicable** | carry on; no `project-memory/` is not a failure (C4) and is not a reason to create it | none |
| **could not run** | record "unknown" with the reason (a shallow clone; or not a git root, where the tool exits 2 before checking); no stop; a piece that needs that memory reads the entry or gets a small check | readiness, then the piece |

6. **Do not repeat a project-level fact per node (my #8, quoted).** 「兵貴勝，不貴久。」 The snapshot is the staged state (C5, `memory_check/REQUIREMENTS.md` lines 50–53), so between nodes the memory the tool sees does not change unless a node stages memory; a per-node run buys duration, not a new fact. A separate end-of-run pass has the same problem: it can pass on the memory as it was, not as a node wrote it. The one exception is the node that commits `project-memory/`; it runs the tool on its own commit as its check (3.6/§4), not as a sixth step.

7. **Use 勢, not a reminder (my #12, quoted).** 「故善戰者，求之於勢，不責於人，故能擇人而任勢。」 A sentence in every brief asking the node to check memory is 責於人; the `--warn` hook is 勢. But the hook is a harness setting and waits for EJ's yes (`runs/20261017-memory-check/settings-diff.md` line 37: "Yes recorded: (not yet)"), and it never fails a session (`|| true` in the proposed command, line 22). A method step cannot rest on an unapproved harness setting; the method's placement stays 3.1, and the hook is how sessions outside a designed run get the same warning.

8. **Not every road is the run's road (my #13, quoted; my reading of its application).** 「途有所不由」 — a break in memory the run never reads is not a reason to stop the run. Only the dependent piece waits; the report carries the rest. This is also what keeps the placement from adding the repair step the owner did not ask for.

9. **Name the fault the check can hide (my #15, quoted; my reading).** 「凡此五者，將之過也」 — a clean result read as a pass is the general's fault, not the ground's. On this repo the tool can exit 0 with 72 not applicable and 3 reviewer items. The readiness line must carry the counts and the reviewer ids; "memory OK" is never written.

10. **A checked thing must be able to fail (my #17, quoted).** 「策之而知得失之計，作之而知動靜之理」 — probe it by planting a break. The test at the end is that probe; the placement is right only if the break shows at 3.1 and the run changes only where it must.

**What is redundant, and what it must not do.** Nothing is fully redundant. The closest is 3.1's row "There, but not verified → add a small piece that checks it against the source" (lines 121–126): for project memory the tool now does the checkable part, so that piece shrinks to reading the entry and judging the reviewer items. §4's per-node application is not redundant — the tool checks the repository's memory, not which entries a node reads or writes — and the blueprint check is untouched. The tool must not judge the "needs a reviewer" items (`memory_check/VISION.md` lines 14–18; C1), replace `memory_index.py` (VISION, last bullet), or write memory (F3). The method must not make the tool's git root a requirement of every run (F2; method 3.1 line 94), require `project-memory/` to exist before work (C4; §4), add a second memory check beside it, rest a node on a "needs a reviewer" or "could not run" line, or turn the tool's exit code into the run's stop.

## What I need to know

1. **Fail policy:** should a failing MUST stop the run, or only hold the pieces that need that memory? I assumed the second; a gate changes step 5's handling, not the step number.
2. **Hook:** will EJ install the session-start `--warn` hook? It changes the coverage and the cost, not the method placement.
3. **Projects:** will the method run on git repositories with `project-memory/`, or on plain directories and projects without it? This repo has none (72 not applicable); on a plain directory the tool exits 2 (`memory_check/REQUIREMENTS.md` F2). If most projects are like this, 3.1 records "not applicable" and the hook is the only real value.
4. **Reviewer:** who reviews the "needs a reviewer" items, and before which pieces? With no one named, those items are ids only and cannot hold a piece.
5. **Memory commits:** will a run commit the `project-memory/` entries it writes? If yes, the writing node's check is cheap and worth it; if no, an end check reads the old snapshot and must not run.

## Costs and risks

**My #6 says the wise mix benefit and harm (quoted: 「是故智者之慮，必雜於利害」); this is the harm side, priced.**

- **A green that is not coverage (my #4, half-known; smoke-report lines 128–129).** On this repo 72 requirements are not applicable and 3 need a reviewer, yet the run looks clean. *Price:* the method records a check it did not get; the fix is the counts and the reviewer ids in the line, never "memory OK".
- **A gate by the back door (my #5, quoted).** If a fail stops the run, every project with a memory break pays a repair before any work — a step the owner did not ask for. *Price:* the method gets slower exactly where memory is imperfect.
- **The wrong snapshot (my reading; C5, lines 50–53).** The tool reads the staged state, not the working tree. A per-node or end-of-run run can pass on the memory as it was, not as the node wrote it. *Price:* false assurance; this is why 3.1 is the safe moment.
- **A tool that cannot run where the method must (F2; method 3.1 line 94).** The method must work in a plain directory; the tool exits 2 outside a git root. *Price:* a usage error read as a memory failure, adding a requirement the method rejects.
- **Noise at session start (settings-diff; my #8).** The proposed hook prints one line in every git project without `AGENTS.md`, at each session, and its output becomes context. *Price:* warning fatigue, and the owner's yes is not recorded yet.
- **The reviewer's three (my #15; VISION, C1/C6).** Three items need a person; the tool cannot judge them by design. *Price:* if nobody reviews them, the memory the run relied on may have been among the unjudged items; the check catches the need, not the judgement.

## How we would know I was right

A planted-break test (my #17): a fixture project with `project-memory/` and one planted break per checkable requirement (U2's minimum acceptance, `memory_check/USE_CASES.md` lines 14–20), plus a second run whose pieces never read the broken entry. The placement is right if:

- the break shows in the 3.1 readiness line and the run's report;
- the pieces that do not read it finish, and no new node is added;
- the pieces that do read it wait (or get a preparation piece), and only they do;
- on this repo the line says "not applicable" with the counts, and the run is not stopped; the hook prints nothing (I ran `bun memory_check/src/cli.ts --project "$(git rev-parse --show-toplevel)" --warn`: exit 0, no output);
- on a plain directory (no git) the tool is skipped with a note, not counted as a fail;
- over the first three designs: steps added = 0, checks added = 1 readiness line, false passes = 0, time added ≤ the hook's 20 s timeout (`settings-diff.md`). The method already sets this three-design review for the 3.3 experts (`docs/WORKFLOW_DESIGN_METHOD.md` lines 266–268); use the same review here.

If after three designs it caught no break the method would have missed and added a COO turn, the placement is wrong: keep the session-start hook only. If it caught a break in memory a node read and the node proceeded anyway, the "hold the dependent piece" rule failed.

**Recommendation (four lines).**
1. Run memory-check **once in 3.1 Readiness**, before any piece, and record its counts and reviewer ids in the readiness row.
2. pass / not applicable → carry on; fail → a decision that holds only the pieces relying on that memory; needs a reviewer → only the dependent piece waits; could not run → unknown, read the entry.
3. Not on every node, not a separate end pass; only the node that commits memory runs it again, as its check; the `--warn` hook is session delivery, pending EJ's yes.
4. Nothing is fully redundant: the "not verified" memory piece shrinks to reading the entry; the method must not gate the run on the exit code, use the tool to judge reviewer items, let it replace `memory_index.py`, or make its git requirement a precondition.
