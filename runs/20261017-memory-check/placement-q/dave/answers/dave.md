# Dave — where memory-check belongs in the method

## Answer
Put memory-check in **3.1 Readiness** as one more read-only tool, beside `readiness.py`, `harness_health.py` and `doctor`. It runs once before the run, and its report is saved in `runs/<id>/` as the run's memory baseline. Then, **only at the stop of a node that writes to `project-memory/`**, run `--warn` again and compare it with that baseline, as part of a check the node already runs (3.6 stop part 2, or §4's State-row check). A MUST that newly fails there counts as a failed attempt. This adds no step and runs at no other node. The session-start hook stays a separate harness decision, and the method does not rely on it.

## How I decided
1. **What would settle it (my #1).** The question is settled by one observation: a memory break that memory-check catches at a given moment and that nothing in the method catches now. If, on a product with `project-memory/`, the node-stop comparison catches nothing that the node's own check, the verifier or EJ had not already caught, I drop that part and keep only the 3.1 line.

2. **What is already measured (my #5).**
   - On this repo the tool reports "Counts: 0 fail, 3 pass, 3 needs a reviewer, 72 not applicable, 0 could not run" (`runs/20261017-memory-check/nodes/smoke-report.md` line 128). The reason is that there is no `project-memory/` (line 120).
   - The same report says "Not calibrated on a real project" (line 127).
   - The hook was tried by hand. It printed nothing in this repo and one line in a repo without `AGENTS.md` (`settings-diff.md` lines 30–32).
   - "70 tests pass" comes from the brief. My own `bun test` was refused permission, so I have **not** rechecked it.
   - A Glob over `~/dev` found no `project-memory/INDEX.md`. Listing other projects was refused, so I treat other products as *unknown*, not as absent.
   - What none of this shows: whether any real run breaks memory in a way the tool catches.

3. **Control: the method as it is now (my #4).** For each candidate moment I compared the tool with what already runs there.
   - **Before the run.** 3.1 already lists read-only checks (`docs/WORKFLOW_DESIGN_METHOD.md` lines 102–110). Its information table says "There, but not verified | Add a small piece that checks it against the source" (line 125). For project memory, no command does that check today: neither `memory_index` nor `memory-check` appears in the method (my grep found no match). A tool line here replaces a judgement with a command and adds no step.
   - **At the stop of a node that writes memory.** 3.6 already re-checks "the baseline recorded in 3.1 still passes" at each building node's stop (line 373). §4's State row gives a memory-writing node only one check: whether "a required one is missing" (line 610). That check does not cover the index, format or history MUSTs, and memory-check does. So this is a moment where the tool catches something new, and it can run inside a check that already exists.
   - **At every node.** §4's Contract row already covers what a node reads (line 609). Rd5.1 is `check: reviewer` (`SOURCE_OF_TRUTH_REQUIREMENTS.yaml` line 811), so the tool cannot decide it anyway. A node that writes no memory cannot break memory, so running the tool there adds a step that catches nothing, which the owner's aim rules out.

4. **Session start is the wrong unit.** Insight `runs/20261016-integrate-r11-r13/insight.md#F-8392b4ce`: a check that treated the session as the task boundary gave false failures, and that session spanned "2026-10-15 to 2026-10-16 and seven requests".
   - What it changed: a session-start warning can be a day old when a run starts, so it cannot stand in for 3.1.
   - The hook is also set only in `~/.claude/settings.json` (`settings-diff.md` line 3), while a run's nodes may be Codex, agy or opencode. §4 says a rule a node must follow lives in repo files, not in one engine's setup (lines 613–615). *My reading:* the same holds for a check.
   - The hook serves the vision's second user, "Every agent starting a session" (`memory_check/VISION.md` line 11). It is EJ's separate yes.

5. **Read the states, not the exit code.** Insight `runs/20261015-long-session/insight.md#F-f09b058d`: a check that read "cannot resolve" as "missing" logged a false failure. memory-check exits 1 both when a MUST fails and when a MUST could not run (`memory_check/REQUIREMENTS.md` R3, line 73).
   - What it changed: the step reads the counts and the per-id states, and "could not run" is never treated as "fail".

6. **Other sessions' changes.** Insight `runs/20261015-long-session/insight.md#F-8712e9fc`: a whole-tree test failed on another session's uncommitted edit. memory-check reads the staged state (C5, line 50), and another session can change that during a run.
   - What it changed: a new fail is charged to a node only if its file is one the node lists as written ("The node's return lists the entries it wrote", line 610). Otherwise it is reported and not charged.

7. **What each result state does** (*my reading*, tied to the method's own rules):

| State | At 3.1, before the run | At the stop of a node that writes `project-memory/` |
|---|---|---|
| pass | Carry on; this is the memory baseline. | Carry on. |
| not applicable | Carry on with one readiness line. Do not add a piece to create `project-memory/`: "the first node that writes an entry creates the folder" (lines 603–604). | Carry on. If this node created the folder, everything now reported is new and is judged as in the rows below. |
| fail (MUST) | Report it; do not fix it unless the task is memory work. A mismatch is "reported in the state file and to EJ, not settled" (line 609). A node that reads the failing memory becomes an unclear spot (3.3): the experts settle it in a time-boxed run, and EJ after three failed trials (3.8 item 14). Every other piece carries on, because stopping them is a listed failure (lines 571–572). A missing `AGENTS.md` goes to EJ in the same batch. | Already failing in the baseline: not this node's fault; stays reported. New, on a file the node wrote: a failed attempt, which goes into the node's bounded repair loop (line 376). New, on a file the node did not write: reported, not charged (step 6). |
| needs a reviewer | Listed once for EJ in the readiness file. It never stops the run and is not asked again each run. On this repo it is always the same three: W3.5a, W3.5b, Rd1.1 (smoke report lines 114–116). | Ignored: the stop is "all objective" (line 370). |
| could not run | Marked unknown, the way `readiness.py` leaves "what it cannot prove" (line 104). Carry on and say so. | That id is "not checked", never "still passes". It is reported: "skipped or unrun checks reported" (line 632). |

8. **Nature (my #6, #7), *recall*; this point does not decide.** A cell checks its DNA at checkpoints: before it copies the DNA and before it divides, not continuously.
   - What is the same: a memory break is copied forward into later runs and sessions. So the two moments that matter are before a run builds on memory (3.1) and before a node's written memory is passed on (its stop).
   - What is different: a checkpoint repairs the damage or halts the cell. memory-check only reads (F3), and the method reports rather than settles. So I borrow the timing and drop the halt.

9. **Is anything redundant, or forbidden? (decision 3; my #4 and my reading)**
   - **Nothing in the method becomes redundant.**
     - No line of the method runs `memory_index.py`.
     - §4's "a required one is missing" is a method rule that the tool will not add: "The tool adds no rule of its own" (`VISION.md` line 18).
     - Rd5.1 stays a reviewer check.
   - **What does change:** for memory structure, 3.1's "add a small piece that checks it" is now a built tool, so a design no longer writes its own memory-checking piece.
   - **The tool must not:**
     - become a step of its own;
     - run at nodes that write no memory;
     - fix or regenerate anything;
     - stop a run on "needs a reviewer" or "not applicable";
     - be judged by its exit code alone;
     - be replaced by the session-start hook.

10. **Small first, then scale (my #8, #2).** The 3.1 line costs one command and is removed by deleting one line, so it can go in now. The node-stop comparison has never run on real memory (n=0). It should be tried on one run of the first product that has `project-memory/` before it becomes a rule for every run. That one-run trial costs less than arguing per-node against end-of-run.

11. **How sure I am (my #10).** The tool has not yet caught a real break anywhere: 0 fail, and n=0 projects with memory. The arguments against session-start-only and against every-node rest on the method's text and on n=1 insights. Treat this as a hint for a trial, not a law.

No category was named. I chose three insights from **check** and none of them was the wrong category.

## What I need to know
1. Does any of EJ's products have `project-memory/` now, or which one will have it first? If none does, write only the 3.1 line now. The node-stop part would then be a rule with nothing to apply to, and it waits for that product.
2. When is the node-stop trial judged: a date or a set of runs? Under my #3 this is fixed in writing before the trial, and choosing it is EJ's decision.

## Costs and risks
- **Noise in readiness (my #5).** On this repo the report says "not applicable" 72 times. The readiness file should carry the counts line and the path to the report, not the report itself.
- **Time at each memory-writing node (my #4).** Not measured. History checks cover every commit since the first one that touches `project-memory/` (C5), so the run time grows as the memory ages.
- **Wrong charges (F-8712e9fc, my #9).** The file-ownership rule depends on each node listing the entries it wrote. If a node's list is wrong, the result is either a false charge or a missed break.
- **Exit-code misreading (F-f09b058d).** Anything that stops on exit 1 will stop runs on shallow clones, because C5 makes history checks "could not run" there.
- **No compare tool (my reading).** Comparing two `--warn` outputs covers only MUSTs and `AGENTS.md` (R2). A new SHOULD fail shows up only in the full report.
- **The hook's own cost, if EJ approves it.** It prints one line per session in every git project without `AGENTS.md` (`settings-diff.md` lines 34–35).
- **n=0 (my #9, #10).** The node-stop part may catch nothing. If so, that null result is reported as a result and the part is removed.

## How we would know I was right
- **Planted test, prediction written first (my #3, #4).** Take a scratch copy of a project with `project-memory/`. Run one small workflow whose memory-writing node plants one MUST break of a kind the tool's own fixtures cover.
  - Prediction: the node-stop comparison names that id as newly failing and the attempt fails. The control, today's method (the "required one is missing" check alone), lets it pass.
  - If the control also catches it, the node-stop part adds nothing and is dropped.
- **Real trial (my #1, #9).** On the first product with `project-memory/`, over the trial EJ sets, count the new MUST fails caught at node stops that nothing else caught.
  - Zero: remove the part and report the null result.
  - One or more: keep it and write it into 3.6.
- **The 3.1 line.** Count how often it changes a design, by adding an unclear spot or a note to EJ. On a product without memory it should produce one "not applicable" line and nothing more.

**Recommendation:**
1. **3.1:** add memory-check to the readiness tools; save the report in `runs/<id>/` as the memory baseline; read the states, never the exit code alone.
2. **Fail before a run:** report it, don't fix it. Only nodes that read the failing memory wait, as an unclear spot. List "needs a reviewer" items once for EJ.
3. **Nodes that write `project-memory/`:** rerun `--warn` at the stop (3.6 part 2, or the §4 State check). A MUST that newly fails on the node's own file is a failed attempt. Try this on one product first and drop it if it catches nothing.
4. **Session start:** the hook is EJ's separate yes, and the method never relies on it.
