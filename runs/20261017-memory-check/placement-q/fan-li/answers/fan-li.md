# 范蠡 (Fan Li) — Placement of memory-check in the workflow-design method

## Answer
Run `memory-check` in step 3.1 (Readiness) as part of the pre-run Information check, never per node or as a new method step. If the result is `pass` or `not applicable`, carry on; if `needs a reviewer` or `could not run`, carry on with a note in `state.md`; if `fail`, stop and ask EJ only if the run depends on project memory, otherwise carry on with a note.

## How I decided
1. **Examine defensive preparations before acting, not during execution (my #18).** In 國語·吳語, my rule is `quoted`: 「審備則可以戰乎？」王曰：「巧。」 Defensive preparations must be examined before engaging. Step 3.1 (Readiness) already hosts pre-work read-only checks (`readiness.py`, `harness_health.py`, guard `doctor`; source: `docs/WORKFLOW_DESIGN_METHOD.md` lines 92–110). Memory inspection belongs inside step 3.1 under "Information", before any builder node runs. Running it per node would violate my #10 (`quoted`: 「臣聞古之善用兵者，贏縮以為常，四時以為紀，無過天極，究數而止。天道皇皇，日月以為常，明者以為法，微者則是行。陽至而陰，陰至而陽；日困而還，月盈而匡。古之善用兵者，因天地之常，與之俱行。」) by multiplying checks beyond necessity and exceeding limits.
2. **Do not force what is unready (my #3).** In 國語21:9, my rule is `quoted`: 「時不至，不可彊生；事不究，不可彊成。自若以處，以度天下，待其來者而正之，因時之所宜而定之。同男女之功，除民之害，以避天殃。田野開闢，府倉實，民眾殷。無曠其眾，以為亂梯。時將有反，事將有閒，必有以知天地之恆制，乃可以有天下之成利。事無閒，時無反，則撫民保教以須之。」 When a repository lacks `project-memory/` (source: `runs/20261017-memory-check/nodes/smoke-report.md`), the tool reports `not applicable`. The workflow must not halt or force memory creation; it continues using existing documentation fallbacks per §4 (source: `docs/WORKFLOW_DESIGN_METHOD.md` line 600).
3. **Contention is the last resort (my #13).** In 國語21:5, my rule is `quoted`: 「夫勇者，逆德也；兵者，凶器也；爭者，事之末也。陰謀逆德，好用凶器，始於人者，人之所卒也；淫佚之事，上帝之禁也，先行此者，不利。」 Unnecessary blocking of the user is contention. For `pass`, `not applicable`, `needs a reviewer`, or `could not run`, the workflow proceeds, logging non-fatal notices to `state.md`. Only a hard `fail` (violating a MUST in memory entries required by the upcoming task) justifies stopping the run to ask EJ.
4. **Distinguish tool duties from worker duties (my #14).** In 國語21:7, my rule is `quoted`: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 Automated verification replaces manual structure verification in step 3.1 ("There, but not verified; source: `docs/WORKFLOW_DESIGN_METHOD.md` line 125). But `memory-check` must not mutate files (it is read-only; source: `memory_check/VISION.md`) and must not replace human judgment on open questions (*my reading*).

## What I need to know
If EJ requires strict repository-wide memory compliance even for workflows that do not read or write `project-memory/`, then `fail` must stop all runs unconditionally; if not (the default), `fail` stops only runs whose nodes carry memory contracts.

## Costs and risks
- From my #18: Adding `memory-check` to 3.1 incurs a small runtime overhead on every run initialization, and risks cluttering logs with "not applicable" on legacy repositories.
- From my #13: Permitting runs to proceed with a note on `needs a reviewer` or non-dependent `fail` risks propagating latent memory defects if downstream nodes unexpectedly touch unchecked files.

## How we would know I was right
In future runs, step 3.1 executes `memory-check` without human intervention, zero runs in repositories lacking `project-memory/` are falsely blocked, and corrupted memory files are caught before dependent nodes run, with no additional steps added to the workflow graph.
