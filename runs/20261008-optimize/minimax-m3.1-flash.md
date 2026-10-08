I'll read the method doc first.
Read both files (`references/method.md` is a symlink to `docs/WORKFLOW_DESIGN_METHOD.md`, so they are one doc, 579 + 219 lines).

**Verdict: not lean.** §3.1 + §3.8 alone are 205 lines (35%); running-the-node detail, rule archaeology and provenance bookkeeping are roughly a third of the file. ~248 lines can go without touching the method's core.

## Cuts, highest value first

1. **§3.8 whole (lines 425–526, ~80 lines savable).** A *design* method carrying100 lines of executor operating contract (timers, no-polling, pass-back headers, `harvest_run.py`) — all of it already stated in SKILL.md step 7 (lines 127–138) and enforced by `dispatch.py`, `validate_result.py`, `node-brief.md`. Keep the framing (COO leads, executors are tools) + item 8 (template/example/standard, which is genuinely the designer's job); point the rest at `docs/DISPATCHER_DESIGN.md` and `docs/EXECUTOR_KINDS.md`.

2. **Skill duplicates the method's hardest rules verbatim (~45 lines in SKILL.md).** The loop's five conditions: method 281–292 vs SKILL 108–118 — including the cache-voiding rationale. The three-part stop: method 329–341 vs SKILL 139–143, **158**, and **179–181** (three copies inside one file). Check-that-can-fail: method 292, 489, 579 vs SKILL 179. The backlog rule: method 343–346 vs SKILL 145–147. SKILL.md:9-10 says the method holds the reasons — so the skill should hold the rule in one clause and cite a §-number, not re-teach it. Biggest cost of this one is not lines: a reader following "read the method once" hits each rule twice and cannot tell which is current.

3. **Provenance bookkeeping: ~22 tags, ~30 lines.** `(Added 2026-10-02 at EJ's request; n=0)` / `(EJ, 2026-10-05; n=0)` at lines 43, 120, 153, 197, 247, 249, 270, 291, 301, 351, 356, 410, 427, 451, 485, 499, 513, 521, 551 — plus three block-quoted EJ sentences (215–217, 250–253) and two "not yet encoded in `intake.js`" TODOs (44, 428). Lines 3–7 already say the whole file is n=1/n=0. Move to one dated appendix table: rule → added → measured n.

4. **Tombstones: dead rules documented in place (~30 lines).** 395–408 (14 lines explaining the deleted caps rule, twice), 476–479 (deleted fallback), 153 (`was "all eight settled"`), 272–274 (archaeology for the number 3), 85–91 (7 lines explaining a `git` rule that no longer exists),451–459 (ceiling rationale restating §3.4's health rule at 247–248). A removed rule leaves one clause ("no caps rule — the spike rule in TASK_TYPES.md is about approaches, not roles"); why you removed it belongs in one appendix or nowhere.

5. **§4's memory table (535–545) and closing cautions (562–571), ~20 lines.** "Claude Code auto-memory: only Claude Code reads it", "Run records: nobody reads them unless asked" are tooling lore, not design method. §4's live content is the state file (530–533) and the three product files (551–560). The "no store without a query" rule also appears at 554 — once is enough.

6. **§3.7 concurrency-unit table (410–423, 14 lines).** `maxActiveSubagents=8` vs `MAX_ENGINE_PROCESSES` is dispatcher knowledge. Keep §3.7's job — sequential first, the five parallel conditions (384–390), verifier independence (393) — plus the one live line at 423 ("never write 'running in parallel' without saying which of the three"); point the rest at `DISPATCHER_DESIGN.md`.

7. **§3.1 blueprint's 8-section × "whose decision" table (132–144, 13 lines).** Line 130 already sends layout and headings to `docs/workflow-templates/blueprint.md`, which exists and holds it. The method needs only what a blueprint *is* (123–125), which sections a task needs (147–153), and status → effect (159–183).

8. **One-word-one-job table (11–20, 10 lines) → appendix.** A glossary placed *before* §1 as a gate, for words the doc then uses correctly anyway. `checklist = the judged fixed list` has no consequence anywhere in the doc. Keep it as a lookup next to `TASK_TYPES.md`, not as a reader's first hurdle.

9. **Tiny test 3×, blueprint exception 3× (~8 lines).** Tiny test: §2 34–37, restated §3.0 73–75, and SKILL 32–36 — §3.0's is §2 with one extra clause. Blueprint confirmations not answered by silence: §3.1 177–183 (full version, with the build/research split) and §3.3 233–235 (cross-reference sentence) and SKILL 72–75. Keep §3.1's; delete the other two.

10. **§5 three qualities (573–579) → 3-line gate with citations.**7 lines that restate §3.5 (a check per piece), §3.6 (three-part stop), §3.1 (acceptance criteria). Its only unique content is the pre-run cost/agent-count estimate and "skipped or unrun checks reported" — and a checklist of three lines belongs in `docs/workflow-templates/workflow-design.md`, which already exists.

If you want one only: **cut 1**. If you want two: add **cut 2**, because that duplicate ownership is the thing that will make the next edit land wrong.
