# Method changelog

History of `docs/WORKFLOW_DESIGN_METHOD.md` (and the skill that packages it): when each rule was added, and every
rule that was removed or changed. The method states the rules as they stand; this file keeps how they got there.
Moved here on 2026-10-08 from inline text (`runs/20261008-optimize/`). One line per item, oldest first; quotes are
verbatim from the text they replaced.

## Added

- 2026-09-20 — The method agreed between EJ and Claude; every number in it from one session (n=1).
- 2026-09-22 — 3.5: the tier rule (attempts start on the cheapest tier) and the tier exit (a fresh node on a stronger tier, never a switch inside the session), at EJ's request; n=0.
- 2026-09-25 — 3.1: the blueprint check, added after EJ found that several projects never ended: their workflows built without a fixed target, so every verify or review step could find more to do; n=0.
- 2026-10-01 — 3.0: understand the challenge, at EJ's request; extended the same day with the six whys and categorization; n=0. The note "not yet encoded in `intake.js`; see `TODO.md`" was stale by 2026-10-08: `intake.js` checks a restatement (`checkRestatement`).
- 2026-10-01 — 3.4: default-first design (category lookup, ≥20% challenger rule, ledger), at EJ's request; n=0.
- 2026-10-02 — 3.2: label the pieces, at EJ's request; n=0.
- 2026-10-02 — 3.8: running a node (executors are tools, timers, pass-back, no polling), at EJ's request; n=0; at the time "not yet encoded in `design_gate.py` or `intake.js`" (much of it is now in `scripts/dispatch.py`).
- 2026-10-02 — 3.8 item 8: the brief carries a template, an example and a standard (EJ: "this is the COO's real work").
- 2026-10-02 — 3.8 item 11: every run leaves a feedback record; n=0.
- 2026-10-02 — §4: project memory for software work (`decisions.md`, `changelog.md`, `lessons.md`), at EJ's request; n=0.
- 2026-10-03 — 3.8 item 10: exploring existing code is its own role (EJ); n=0.
- 2026-10-03 — 3.8 item 12: design decisions cite their evidence (EJ); n=0.
- 2026-10-05 — 3.1: `git` is not a requirement (EJ).
- 2026-10-05 — 3.4: health is a reason to split (EJ); n=0.
- 2026-10-05 — 3.4: size from an estimate, never one huge prompt (EJ); n=0. EJ's words: *"When we design the workflow, we don't ask a subagent to give a HUGE prompt that runs like 10 hours to Codex. Since an LLM can already estimate the workload, better to divide into like 6 or more pieces of prompts that are logical."*
- 2026-10-05 — 3.6: the design and the runnable plan are two artifacts, and the COO writes both (EJ).
- 2026-10-05 — 3.8 item 2: no single call runs past the 8-hour ceiling (EJ); n=0.
- 2026-10-05 — 3.7: concurrency "name the unit" (EJ: *"how many running in parallel is even more weird"*); the table moved to Appendix C on 2026-10-08.
- 2026-10-11 — Appendix A: `accepted` defined as *traceable and internally consistent*, not *true*, and added to the word list on line 11 (EJ: *"please add these to your memory"*, after the agent-memory run was reported as accepted when the item-6 check was a script the COO wrote and the different-kind verifiers had not run); n=1. The three presentation rules that came with it live in `CLAUDE.md`, with their own basis.

- 2026-10-12 — 3.0: the vision and requirements a task serves, named at the end of 3.0 for every task except a tiny one (research, design and documentation included); requirements drafted by the agent when missing, and work does not start until EJ confirms them (EJ: *"I notice you perform better when I give you a vision and requirements"*; then *"b, apply to every task except tiny ones"*); n=1 (runs `20261012-memory-caches`, `-caches-routing`, `-caches-merge`).
- 2026-10-13 — 3.3 and 3.5: ask the experts (the `four-experts` skill) — at 3.3 Linus, 孫子, 老子 and Dave once the unclear-spot list is written; at 3.5 Linus, 范蠡, 孫子 and Dave on each loop's check before it runs; advice only, a "drop it" goes to EJ, never silently (EJ: *"ok, put them to the 3.3 and 3.5, update the algorithm and skills"*, after the experts' own placement run `runs/20261013-four-experts-where-in-ej-s-workflow/`); n=0. The state template gained a *Raised by* column and an *Experts asked* line; the design template a per-piece *Experts on the check* line.

## Removed or changed

- 2026-09-20 — 3.4, first bullet changed after trial 1, where three decisions with obvious defaults helped push a one-line fix out of "small" (n=1): a spot of kind information or unknown always means a workflow design.
- 2026-10-02 — 3.0/3.2: the category used to be fixed in 3.0 and only checked against the facts; since then 3.2 relabels it from the algorithm.
- 2026-10-03 — 3.1, New product row: was "all eight settled"; now four settled before anything builds, the other four for the slice only (EJ; n=0).
- 2026-10-03 — 3.4 anchors: the corroboration cap of 3 corrected — it caps dispatches per plan, not agents running at once.
- 2026-10-05 — 3.1: before this date the runnable form ran `git status --short` unconditionally, and a plain directory died at the first step of every run (register 9.2); `git` made optional, and the baseline was stated as never depending on it.
- 2026-10-05 — 3.5 item 2 renamed: it read *"a limit on attempts"*, and EJ read it as a time bound, which is 3.8's business — two different rules wearing the same three words; now "a limit on the number of attempts — a count, not a time limit".
- 2026-10-05 — 3.7, caps deleted (EJ: "not logic at all"): the rule *"at most 5 subagent roles per run and at most 3 running at once"* re-labelled the spike rule's numbers in `docs/TASK_TYPES.md` (*"run at most 3 in parallel"*, *"up to 5 in a round"*, both about candidate approaches) as a rule about roles and concurrency; "5 roles" counted distinct `role` values (a property of a design), "3 running" counted engine processes alive (a property of the machine, now `MAX_ENGINE_PROCESSES` in `scripts/dispatch.py`); `validate_plan` no longer refuses a plan for many roles or a wide parallel group, and the pair survives only in the spike rule.
- 2026-10-05 — 3.8 item 5, fallback removed: one engine per node, and a failure blocks the node and reports rather than hopping to an engine nobody chose.
- 2026-10-05 — 3.6, design-vs-plan comparison: first decided as *"C — leave it"* (one author writes both and can see both, so a checker would guard against someone standing right there); revisited the same day after a traversal (`intake` → design → gate → plan → dispatch) in which the hand-written plan silently dropped two of three nodes' checks, plus `touched_paths`, the baseline, the categories and the estimate, while `validate_plan` said *"plan ok"* — so `dispatch.py validate PLAN --design DESIGN` now compares them. Moral recorded at the time: *"The first measurement of a decision's cost changed the decision. That is the argument for traversing a chain once rather than reasoning about it."*
- 2026-10-13 — §4: the three project-memory files in `docs/blueprint/` (*"A product keeps three small append-only files beside its blueprint"*: `decisions.md`, `changelog.md`, `lessons.md`) replaced by "Memory in a designed workflow": project memory follows `docs/memory-system/SOURCE_OF_TRUTH.md` and its caches `docs/memory-system/CACHES.md`, applied per node in the Context, Contract, State and Tools fields (memory delivered, never asked for). The blueprint template's memory files, the research-file template's pointer, 3.8 item 9's pointer and the skill's Context and State rows follow. EJ: *"we better enhance the workflow design algorithm to remind the ai agent when and how to use memory more effectively. both the source-of-truth and caches"*, after a four-expert run in sequence (`runs/20261013-memory-in-workflow-design/`: all four recommended the pointer and delivery by brief, import or hook); n=0.
- 2026-10-13 — §4, the same change after a four-expert review (`runs/20261013-memory-in-workflow-design/review/`, all four "accept with changes"; EJ: *"apply all"*): a transition paragraph (SEZA and `site/ancients` keep their three files under the rules above until EJ moves them); the Context row no longer lets a start hook carry entries (SoT Rd2.2) and keeps a words-only request as the stated fallback (SoT Rd2.1); Rd4.1 and the Rd5.4 exceptions added to Contract; State row citations corrected (K5.1, W5.2) with the logged journal read; the vector index's own trigger (B1.2) in Tools; *"Not verified: Codex's memory and subagent features beyond `AGENTS.md`."* merged into the built-in-memory sentence; a release-note sentence, *proposed*; `docs/TASK_TYPES.md`'s four `decisions.md` pointers now say "the product's decision record (method §4)"; the skill's Contract and Tools rows point to §4.
- 2026-10-14 — §4: the release note is kept, in the blueprint's `changelog.md`, written by the node whose work ships from the decisions' `done:` lines and the commits (EJ: *"yes want a release note"*); it was *proposed* and "when one is needed". The transition paragraph no longer names SEZA and `site/ancients` and says "its owner", not "EJ" (EJ: *"seza is another project, here we just use as an example"*).

## Restructured

- 2026-10-08 — Optimization pass (`runs/20261008-optimize/`): the provenance tags above taken out of the method's text; the glossary, the memory-kinds table and the concurrency table moved to the method's Appendix; §3.8's twelve items compressed to one line each (numbers kept, because code and docs cite them); duplicated definitions merged (baseline → 3.1, "not answered by silence" → 3.1, tiny test → §2, tier escalation → 3.5 item 4); §5 collapsed to pointers. The matching `SKILL.md` change (a summary that links to the method instead of a second
  copy) is proposed in `runs/20261008-optimize/SKILL.proposed.md` and not yet applied.
- 2026-10-12 — 3.0, first line: *"From the challenge text alone — no tools, no agents, no repository browsing — state three things"* now allows opening the vision and requirement files the new last step names; the cost guard gained the same exception (EJ, with the vision-and-requirements step above).
- 2026-10-12 — 3.1, blueprint table, row *Not a product change*: *"none; record why, and the check ends here. It carries no acceptance criteria"* replaced by *"none of the blueprint sections; its vision and requirements were settled in 3.0"* (EJ: the step applies to every task except a tiny one).
