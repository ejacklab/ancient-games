# Optimize the workflow-design method — claude (Opus 5.5), blind

Read: `docs/WORKFLOW_DESIGN_METHOD.md` (579 lines), `.claude/skills/workflow-design/SKILL.md`. Did not read the
other engines' files. Line numbers are the method doc's at commit 8431d26.

**Verdict: not lean.** The core (3.0–3.6 steps, five node fields, state file, three-part stop) holds up. The
weight is (a) the history of deleted or revisited rules kept inline, and (b) the same rule restated in every
section it touches. The ten cuts below remove roughly 150 lines (~25%) without losing a rule.

## The cuts, by value

| # | Kind | Where | Cut / merge | Why |
|---|---|---|---|---|
| 1 | optional | 3.7 L395–423 | Replace the deleted-caps story and the three-row concurrency table with one line: *"No caps rule. Never write 'parallel' without naming the unit — `docs/EXECUTOR_KINDS.md`."* | ~29 lines describing a rule that no longer exists; the unit distinction already lives at `EXECUTOR_KINDS.md:327`. |
| 2 | optional | 3.6 L353–370 | Keep 3 lines: design and plan are two artifacts; `dispatch.py validate --design` compares; the plan may add, may not lose. The "C, then C revisited" story goes to `DECISIONS.md` / the register. | Decision history, not method; a first reader needs the rule, not how it was reached. |
| 3 | duplicate | 3.3 L232–235, 3.4 L243–244, 3.6 L337–341 (source: 3.1 L177–183) | Replace each restatement of "blueprint questions are not answered by silence / builders wait for settled sections" with "(3.1)". | Same rule four times, each slightly re-worded, so a reader has to check they agree. |
| 4 | duplicate | §1 L26–28, 3.2 L211–217, 3.4 L245–259, 3.8 item 1 L440–443, 3.8 L451–459 | One "how big is a piece" paragraph in 3.4: floor (hand-off has a fixed cost; a label is not a node) and ceiling (hours of work → split into 6+; 8 h per call). 3.2 and 3.8 point there. | Split cost and "segments are healthier" are each stated three times; 3.4 even says "it does not remove 3.2's warning". L457 is also mis-indented. |
| 5 | duplicate | 3.8 items 9–12 L493–526, bundled-runtime L434–438, default-first L263–270 | Move the researcher/explorer contracts, `runlog`/`harvest` tooling and evidence-citing rule to `EXECUTOR_KINDS.md` (which has the roles); bundled-runtime is already at `EXECUTOR_KINDS.md:90`; the 20% rule is already at `TASK_TYPES.md:31`. Leave one pointer line each. | ~45 lines that are the single copy elsewhere, or should be — they specify how to *run* roles, not how to *design*. |
| 6 | optional | 19 inline "(Added 2026-… at EJ's request; n=0)" tags | Collapse into one provenance table at the end: section · added · source · n. Fix L4–7, which names only 3.0 and 3.5 as n=0 while about ten sections are. | Provenance matters (house rule) but inline it interrupts every rule; the header summary is already stale. |
| 7 | duplicate | 3.0 L73–75 (and L65) | Delete; §2 L34–37 already says the tiny test reads the restatement. | Tiny test stated three times in two adjacent sections. |
| 8 | duplicate | 3.5 item 4 L288–291 and L297–301 | Merge into item 4 with one sentence of why (cache voided, cheap tier's wrong turns anchor the strong one). | Tier escalation stated twice inside one section. |
| 9 | low-priority | 3.1 L85–91 (git), 3.4 L272–274 (anchors for 3) | Git paragraph → one line ("git not required; the baseline is the test command, 3.6"). Anchors → appendix (also fix "the the"). | Readiness opens with an incident report; the anchors are evidence footnotes. |
| 10 | optional | "One word, one job" L11–20; §4 L535–545 memory-kinds table, L569–571 graph caution | Glossary and background tables → appendix at the end. | A glossary of function names (`probe_binary`, `compare_plan_to_design`) before the reader knows what a node is; the memory table is general background. |

## Checked and *not* duplicated (the brief's candidates)

- **Who fills it** — not in the method at all (only in `CLAUDE.md`); nothing to merge. §4's "Written by" column is its only trace.
- **One word, one job** — one copy; misplaced (cut 10), not duplicated.
- **Loop's five conditions** (3.5) and **parallel's five** (3.7) — different lists. Not a dup, but both say "all five", which invites the confusion.
- **Three-part stop** — stated once (3.6); §5 points at it. Fine.
- **Check-that-can-fail** — 3.5 item 5 is the rule; §5 and 3.8 item 8 are short references. Fine.
- **Baseline** — two copies (3.1 L88–89, 3.6 L332–333); the 3.1 copy goes with cut 9.

## Low-priority candidates I would keep

The nine steps, the five node fields, the state file and the acceptance criteria are the core. §5 (three qualities)
restates rules from 3.x by design — it is the finish-line checklist; keep it, but L577 "fixed bounds on …
concurrency" now points at a rule that cut 1 shows was deleted — re-word or drop that word.
