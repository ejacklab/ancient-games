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

## Restructured

- 2026-10-08 — Optimization pass (`runs/20261008-optimize/`): the provenance tags above taken out of the method's text; the glossary, the memory-kinds table and the concurrency table moved to the method's Appendix; §3.8's twelve items compressed to one line each (numbers kept, because code and docs cite them); duplicated definitions merged (baseline → 3.1, "not answered by silence" → 3.1, tiny test → §2, tier escalation → 3.5 item 4); §5 collapsed to pointers. The matching `SKILL.md` change (a summary that links to the method instead of a second
  copy) is proposed in `runs/20261008-optimize/SKILL.proposed.md` and not yet applied.
