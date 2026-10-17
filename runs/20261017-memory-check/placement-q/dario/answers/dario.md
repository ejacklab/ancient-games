# Answer — where memory-check belongs in the workflow-design method

## Answer
Run it in step 3.1 (Readiness) as one more read-only check, once before the first node, beside `readiness.py`, `harness_health.py` and `doctor`. Run it a second time at the end of a run (step 3.6 / skill step 8), and only if a node wrote memory entries. Don't add a per-node step. A failing MUST goes to EJ as a decision spot (3.3) and the run carries on without the pieces that depend on it. The other result states never stop a run.

## How I decided
1. **Does the method already check memory?** No. I searched `docs/WORKFLOW_DESIGN_METHOD.md`, the skill's `SKILL.md`, its `scripts/*.py` and `guard/src/*.ts` for `memory_index` and found nothing. I searched `docs/*.md`, the skill's `.md` files, `CLAUDE.md` and `AGENTS.md` for `memory-check` and `memory_check` and found one unrelated hit. §4 (lines 592–611) says what each node does with memory. The only check it names is the method's own "its check fails if a required one is missing" (line 610, marked n=0). Nothing in the method checks that entries are never deleted (K4.1) or never rewritten (K4.3), that the index is regenerated (K6.2), or that `AGENTS.md` exists (F1). The tool is the only thing that does. So this placement adds a check without overlapping another.
2. **Where it fits without a new step.** Lines 100–110 of the method already list the read-only checks run before work. The Information check names "a memory folder" as a structure, and its table has the row "There, but not verified → a small piece that checks it" (lines 114–125). One command in that list adds no step and no row. `--warn` prints nothing when nothing fails (`settings-diff.md`: nothing printed in this repo).
3. **Why not per node.** §4 already gives each node its memory duties in its five fields. The tool judges the whole memory folder from the staged state and git history (REQUIREMENTS C5), not one node's work. A run per node would be a new step per node, which is the opposite of your aim.
4. **Why not session start only.** §4 says "nothing is left to a reminder the agent may skip" (lines 594–595), and a hook warning is a reminder. The hook also waits for EJ's yes (`settings-diff.md`), so the method can't depend on it.
5. **Why the end-of-run use.** *My reading:* K4.1 and K4.3 are "must not change" rules, and 3.6's stop condition has a "must not change holds" part (lines 370–376). Comparing the end result with the 3.1 result means a failure that was already there is not charged to the run. A new MUST failure is then a failed attempt of the node that wrote the entry, bounded by 3.5 (3.6: "A failure of any of the three is a failed attempt").
6. **What the step does with each result state** (my reading, built on 3.3, 3.1 and SoT Rd5.3):

   | State | What the step does |
   |---|---|
   | pass | Carry on. Write the tool's counts line to `state.md`. |
   | fail (MUST) | At 3.1 it becomes an unclear spot of kind decision, in the one batch to EJ. The provisional assumption is to carry on with pieces that don't touch the failing entries. No agent edits memory to make it pass (SoT Rd5.3: the reader reports, the owner decides). At the end of a run it is a failed attempt of the writing node. A fail on a SHOULD is a line in the report only. |
   | needs a reviewer | Carry on and list it in `state.md` and the final report. It is never counted as a pass. A reviewer item that is a node's own check (Rd5.1) stays in that node's Contract (§4 line 609). |
   | not applicable | Carry on with one line, "no project-memory/". It must not trigger the 3.1 "Missing → research piece" row. §4 lines 600–604 already say what happens before a product has `project-memory/`. In the smoke report, 72 of 78 results here were not applicable. |
   | could not run | Mark it *unknown* in the readiness list (3.1: what can't be proved stays unknown) and carry on. Never treat it as a pass. Read the counts line, not the exit code, because REQUIREMENTS R3 says exit 0 for "no MUST fails *or could not run*". |

7. **Q3, what becomes redundant.** Nothing in the method does, except a hand-built "check the memory folder" preparation piece in the 3.1 information row, which one command replaces. The Contract checks (Rd5.1/Rd5.3: check an entry against the code) and the method's own "required entry written" check stay. The tool never judges whether an entry is true. By my count of the `check:` lines in `SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, of the 64 records about 33 are reviewer-only, 11 are "none", 14 are tool or git alone, and 6 mix tool or git with a reviewer. SoT Rd5.5 says the same: checking against code finds only gaps between entry and code.
8. **Q3, what it must not do.** It must not be a step per node. It must not stop a whole run. It must not edit memory. It must not be read as proof that an entry is true. It must not be the only enforcement, so the hook stays an owner-decided extra.

## What I need to know
- **A stop or an ask for a failing MUST at run start?** I assumed ask-and-carry-on, since that is the 3.3 default for decisions. If EJ wants a hard stop, the answer changes to treating it like a blueprint question (3.1: not answered by silence).
- **Has the tool been run on a real project with `project-memory/`?** The smoke report says "Not calibrated on a real project". If it hasn't, I would keep the end-of-run use report-only until it has.
- **Do nodes stage or commit their entries before the end check?** The tool reads the staged state (C5). If they don't, the end check can't see what they wrote.

## Costs and risks
- **Not tested on a real project:** the method has no real project with `project-memory/` to test against, and the tool is uncalibrated. False fails are possible, and each one is a question to EJ. On this repo, which has no `project-memory/` (I checked), 3.1 gets almost no evidence.
- **Staging blindness:** an unstaged node write is invisible, so a clean end-of-run report can be wrong about what the node wrote.
- **Exit-code trap:** a script that trusts the exit code treats "could not run" as a pass (R3).
- **A pass reads stronger than it is:** it says structure and history follow the guidelines, nothing about truth. I did not re-run `bun test`. The 70 passing tests are from the brief.
- **Hook tension (not part of the placement):** the method says "a start hook carries only the four session-start reads" (§4 line 608). The `--warn` line is not a memory file (my reading, and Rd2.1's fails-if is about loading memory files), but a reviewer could read it either way. That is EJ's call with the settings diff.
- **Cost:** one command and one `state.md` line per run, plus one added line in 3.1 and one in 3.6 or step 8. They go in as bullets, not new numbered items, so no cited item number moves.

## How we would know I was right
- **Planted test:** on a copy of a project with `project-memory/`, delete one entry (K4.1) and leave the index stale (K6.2). Run a designed workflow that calls memory-check at 3.1 and at the end. The end report should show a new MUST fail naming those ids, `state.md` should hold both counts lines, and EJ should have been asked once, with no stop.
- **Control run:** a run on this repo should add no node, no question, and a counts line of 0 fail.
- **Exit-code trap:** on a shallow-clone fixture, the exit code is 0, the counts line shows "could not run", and the readiness list shows *unknown*.
- **Calibration measure:** over the first runs on real projects, compare the fails EJ confirms with the fails EJ overrules as false. If EJ overrules most, the check stays report-only.
