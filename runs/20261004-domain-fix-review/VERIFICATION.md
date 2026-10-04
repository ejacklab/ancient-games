# VERIFICATION — a blind re-read of FIX_PLAN.md

Verifier: claude-opus-5-5, a fresh session. I did not write the surveys or the plan. Note that the engine is the same
as one survey's and the chair's, so the self-preference check (2) is the one to read most sceptically.

**How this was checked.** Everything below comes from reading. Running Python, `node` and `git log` needed an
approval this session did not have, so **no test, script or mutation was run**. The exceptions are `grep` counts and two
`git grep` calls on a past commit. Where a conclusion depends on how code would behave, the lines it rests on are cited
so it can be re-run.

---

## 1. Is every `DIRECT` checkable? — **FAIL (7 of 13)**

| fix | verdict | why |
|---|---|---|
| 1.4 | **FAIL** | The check (strip `loop` → CAUGHT) is the same as 1.6's. A gate that hardcodes a loop list, like `corpus_check.py:37` `LOOP_CATS`, passes it without ever reading `pattern`. So the check cannot show that the 1.4 defect ("pattern used 0 times") is gone. The parts of minimax's check that could show it were dropped: `grep -c LOOP_CATS` = 0, and a step-kind row that carries a loop. |
| 1.6 | PASS | Today, loop rules fire only inside `if lp is not None` (`design_gate.py:163-170`). No other rule reads `loop`, so stripping it is currently uncaught, and the mutation can fail. |
| 2.2 | **FAIL** | "Lower the threshold to 0.05 → the 10% row reports MISSED" works only if **both** 0.20 constants are lowered: `:185` (claim) and `:193` (recomputed). Lowering `:185` alone leaves a `claim_margin: 0.10` row CAUGHT through another G5 clause: `:193` if the estimates are consistent, `:196` (arithmetic) if not, `:198` if they are absent. The matrix scores only the prefix `G5` (`mutation_matrix.py:173,178`). The alternative check, "a challenger **ledger row** reaches **G5** arithmetic", mixes two rules: ledger rows go to `validate_ledger_row` (G7, `:258`), not G5. The plan names two checks joined by "or" for two different fixes, and does not commit to one. |
| 2.6 | **FAIL** | "Re-emit through the gate → zero new G3 findings" passes whether or not `corpus_check.py` emits `pattern`. Under the plan's 1.4 fix, the gate reads the pattern from the TASK_TYPES row by category, not from the node. The "+ the 1.4 mutation" part tests the gate on `p050.json`, not the emitter. deepseek's check would fail if the edit were absent (each emitted design carries the row's `pattern`), and it was dropped. |
| 3.1 | PASS | `tests/test_readiness.py:413-419` (`test_rt_15`) asserts `verified` for a mapless blueprint, so it must flip. |
| 3.2 | PASS, scope understated | `test_rt_16` (`:422-426`) asserts `verified` for an empty directory. `tests/test_readiness.py:138` also asserts `verified … absent (…)` for absent directories, so more than the one named test flips. |
| 3.3 | **FAIL** | "`test_rt_13` flips" has no expected value, and the plan itself says the count is unsettled: claude says "0 of 8", minimax says "1, map only". Any change to the string makes the test flip, including a wrong count. It also interacts with 3.1. Under claude's 3.1 rule ("MISSING when no section file exists"), the `test_rt_13` fixture (README.md, a.md, b.md, none of them template names) becomes MISSING, and `exit_code` makes the run exit 1 (`readiness.py:~330`). That breaks the test's `returncode == 0` assertion (`:376`), and the plan does not say which outcome is right. |
| 3.4 | PASS | `test_rt_07_WART_require_accepts_present_broken_tool` (`:255-258`) records the current behaviour. A `--require` on an UNKNOWN tool exiting 1 fails on today's code. |
| 3.5 | PASS for the half it covers | `readiness.py:157-163` calls `model.get(...)` on whatever `d.get("model")` returns, so `{"model":"x"}` raises today. The other half is lost; see check 3. |
| 7.1 | **FAIL: the fix cannot pass its own check** | The fix is "a required `restatement` in READY_SCHEMA". The check is an `intake_harness.mjs` sabotage case. The harness stub returns canned objects and never enforces a schema's `required` (`intake_harness.mjs:58-71`). A schema field alone cannot make that case fail. The fix also needs a code-side check in `intake.js`, the way `checkBlueprint` is called at `:624`, and the plan does not name one. |
| 7.2 | **FAIL as DIRECT** | It is checkable, but the plan itself says it depends on 5.1, a DECISION, and claude's vote says it waits on 1.2, a SCHEMA. A fix that cannot start until a decision lands is not direct. |
| 7.3 | **FAIL: passes either way** | The "passes" case, "fresh node on a stronger tier, then the unclear list", contains "unclear". The current regex `/unclear\|EJ/` (`intake.js:381`) already accepts it. The "another round" case already fails today (`intake_harness.mjs:339`). So both halves pass on the unfixed code. The plan's fix text (claude's: accept the first exit "provided the same text also names" unclear/EJ) is behaviourally the current code. A check that could fail: an exit naming **only** a fresh node on a stronger tier is accepted. Whether that should be accepted is exactly where deepseek ("without requiring unclear or EJ") and claude disagree, and the 3/3 label hides it. |
| 8.2 | PASS | `workload.py:166-169` compares `engines[v]` only with `engines[n.id]`. A codex worker with a claude verifier and no plan fallback is not flagged today. |

## 2. Is the plan faithful to the surveys? — **PASS on the votes, FAIL on the fix text and §5**

**The votes are right.** I rebuilt all 135 verdicts (45 × 3) from the three surveys. All 19 rows in the §1 table match
on each expert's vote and on the count. The seven 3/3 rows (1.4, 2.2, 3.1, 3.2, 3.3, 3.5, 7.3) and the three-way
splits (5.2, 6.4, 8.1) are correct. No DIRECT vote is missing from the table: the union of DIRECT votes is exactly
those 19 rows.

**The failure the brief asked about is present, in the fix text rather than the votes.** Where the experts proposed
different fixes, the plan flags the disagreement three times (1.4, 2.2, 3.3). In four other cases it silently adopts
the claude survey's fix:

- **3.2**: the plan uses claude's "default `absent_status` to MISSING". minimax proposed something else: set the status
  per call site, with absent skills UNKNOWN and only a required item MISSING. This is not flagged.
- **7.3**: the plan uses claude's check verbatim. deepseek's fix drops the unclear/EJ requirement, and minimax's
  accepts "the three documented exits". The result is the check that cannot fail (check 1).
- **8.2**: the plan uses claude's `workload.py` edit and lists only minimax as a dissent. deepseek also voted DIRECT,
  for a different edit: `engines.py` `DEFAULT_FALLBACKS`.
- **3.5**: the plan narrows the fix to claude's and minimax's model guard. It drops the rc==0 half, which claude and
  deepseek both fixed.

**§5 point 4 is not supported by the files.**
- "All three lead with the gate/test/readiness families the register itself calls 'where to start'": the register's
  "Where to start" (`defect-register.md:143-148`) names the gate family, the test family, the mutation run and 5.1. It
  does not name readiness. claude's first fix is 4.5, minimax's is readiness, and only deepseek leads with the gate.
- "The one expert (claude) who re-read the code": minimax's survey cites code correctly and specifically.
  `corpus_check.py:113` does hardcode `design_source: "default"`, `corpus_check.py:37` does define `LOOP_CATS`, and
  `test_rt_13`/`15`/`16` do assert the strings minimax quotes, including "3 sections". minimax read code.
- "broke rank on … 6.4": on 6.4 all three disagreed (DOC / LATER / DECISION), so there was no rank to break.

**Smaller items.** The §4 rows decided 2/3 omit the dissent for 5.4 (claude DOC), 5.5 (minimax DOC), 6.1 (claude
SCHEMA) and 6.3 (claude LATER; the plan quotes claude's reason but not its vote). The chair's four overrides split
two to claude (6.4, and 7.4 against a 2/3 DIRECT) and two to deepseek (5.2, 8.1). That split is not one-sided. But the
7.4 override adopts the chair-engine's own 1/3 verdict, and the plan does not say so.

## 3. Did anything get lost? — **FAIL (one issue in limbo, one half-issue dropped)**

All 45 ids appear in the plan. I checked the register's rows; its own header says "44 distinct", but the rows and the
totals table give 45.

- **8.1 has no home.** §3 rules it DIRECT, but it is not in the 13-fix direct set (§2), and it is not among the non-DIRECT
  verdicts (§4 excludes it explicitly). It has neither a fix slot nor a blocking reason. 4.1 is blocked on it, so 4.1
  inherits the limbo.
- **3.5's second half is dropped.** The register's 3.5 has two defects (`readiness.py:139,163`): "any rc==0 with output
  counts as a verified model list", and the AttributeError. The plan carries only the AttributeError. claude's survey
  has a check for the dropped half (a stub `agy` printing an error with rc 0 → UNKNOWN), and deepseek's has one too.
- **Blocking reasons are missing for most of §4.** SCHEMA rows 1.1, 1.2, 1.3 and 8.3 name the field but not what blocks
  adding it; only 4.5 says "EJ picks". Most DOC rows (4.2, 4.3, 4.4, 4.6, 4.7, 5.7, 6.5, 7.4) name the files but not why
  they are not simply done. The DECISION rows do state the choice EJ faces.
- **Header arithmetic.** Line 7 says "Two fixes already…" and then lists three (1.7, 2.5, 2.3). Line 8 says "Two
  further items are demoted"; only one (7.4) is demoted anywhere in the plan.

## 4. Are the plan's three corrections true?

**(a) 7.4 was misfiled; the emitter was `corpus_check.py`, and it is already fixed: RIGHT.**
- `git grep` at `45b9c37` (before the gate commit) finds `"default check for {c} (TASK_TYPES.md)"` in
  `tests/workflows/corpus_check.py:68` **and** `tests/test_task_types.py:44`. `intake.js` has no `TASK_TYPES` reference
  at that commit or at `2a075cf~5`, and has none now.
- Today `corpus_check.py:69` emits `known[c].get("check")`, `test_task_types.py:45` does the same, and 0 of 300 emitted
  designs contain `TASK_TYPES`.
- `testlog.md:5` names `corpus_check.py` as the source of the logged designs.
- One omission: there were two emitters, not one, and the plan names only `corpus_check.py`. Both are fixed.

**(b) The 5.7 caps are enforced in `dispatch.py`: RIGHT about the code, OVERSTATED about minimax.**
- The code: `dispatch.py:41` (`DEFAULT_BUDGET` max_roles 5, max_parallel 3), `:62-64` (roles cap) and `:107-109`
  (parallel-group cap) say what the plan says. `:326` (`ThreadPoolExecutor(max_workers=max_parallel)`) also enforces the
  cap at run time.
- The limit: this binds a **dispatch plan**, not a **design**. `design_gate.py` has no cap rule, and a design that never
  goes through `dispatch.py run` (an `intake.js` output, a Workflow script) is not capped.
- So minimax's "no G-rule enforces either, so nothing would catch a design running six at once" is true of the gate and
  false of a dispatched plan. The plan calls it simply false.
- The register's "exist only in the method" is wrong as written, and the plan is right to correct it.

**(c) The SCHEMA verdict on 1.1/1.3/8.3 overstates the work, because `intake.js` already has the fields: PARTLY RIGHT.**
- What it gets right: `DESIGN_SCHEMA` (`intake.js:165-201`) carries every field the plan lists (`stop`, `intent`,
  `returns`, `files_touched`, `must_not_change`, `evidence`, `evidence_file`, `state_reads/writes`,
  `brief_given/withheld`). That gives four of the five things content. There is no `tools`, `category`, `engine` or
  `sabotage`.
- What is wrong for **1.3**: `stop` is **one free-text string** (`:190`). 1.3 is about the stop's three parts as
  separately checkable values. Today those are checked only by a judged verifier (`V7`, `:248`). Adopting intake's piece
  does not close 1.3 without a further format change.
- **There is no baseline in any intake schema.** "baseline" appears only in prompt text (`:501,507,584`) and the
  verifier items `V4`/`V6`. The plan does not claim a baseline field, and rightly leaves 1.2 out of the group. The
  brief's paraphrase of the correction ("carries `stop` and a baseline") would be false.
- §5.1 then cites "94 of 300 designs" as the cost of the grouped decision, but that projection belongs to 1.2's baseline
  (`open-defects.md:46`), which the group excludes.
- §4 still lists 1.1, 1.3 and 8.3 as separate SCHEMA rows, which contradicts §5.1's "one decision, not four field
  inventions".

## 5. What did the plan miss?

1. **The 8.1 "DIRECT" fix turns a large part of the corpus red.** `corpus_check.py:97-98` assigns a `codex` reviewer to
   every opencode-led build group. 92 of 300 emitted designs carry a "+ Codex" engine cell. The register's own 8.1
   example (`testlog.md:105`) is reviewed by `codex gpt-6.1-sol` (`testlog.md:~124`). A set-valued `engine_kind` makes
   those designs fail G6 until a third-kind reviewer default is chosen. That choice is claude's DECISION, which the
   chair filed as a "follow-up". The plan calls the 1.1-1.3 projection "a decision, not a field name" and should treat
   this one the same way.
2. **13 fixes are fewer edits than that.** 1.4, 1.6 and 2.6 are one gate rule plus one emitter line. 3.1 and 3.3
   collide on `test_rt_13`. 7.2 waits on 5.1/1.2. The plan gives no order or grouping.
3. **1.7 is accepted as FIXED although only half of it is.** The register's defect is "non-empty, not executable".
   What was fixed is the table-pointer form. claude's survey records the residue ("executable" needs `check_kind`, which
   comes with 4.5), and the plan drops it.
4. **2.2's G7 half has no check in the plan.** G7 is covered by the gate's `--self-test` (`design_gate.py:348-353`), but
   the register's point is that the **corpus** never reaches it, and no named check makes it do so.
5. **The register's ✓ marks are not carried forward.** Five DIRECT fixes rest on issues the register marks
   engine-only, not independently confirmed: 1.6, 3.4, 3.5, 7.2, 7.3. I confirmed four of them by reading: 1.6 at
   `design_gate.py:163`, 3.4 via `test_rt_07`, 3.5 at `readiness.py:157-163`, 7.3 at `intake.js:381`. I did not check
   7.2's claim that the baseline is only a git snapshot beyond `intake.js:507`. The plan does not say which of its fixes
   rest on unconfirmed premises.

---

## The plan's weakest claim

**§3: "8.1 — the chair rules: DIRECT."** The plan says the data is already in the cell, so the fix is a code edit and
the consequence "follows from the fix rather than blocking it". But the edit cannot land green. Every opencode-led
build reviewed by codex, the corpus default at `corpus_check.py:98`, becomes a G6 failure. The repair requires choosing
which kind reviews a split build (claude, deepseek, or the per-module plan after `workload.py --write`). That is the
EJ decision claude named.

What would settle it:
- In a worktree, make `engine_kind` return the set of kinds a cell names, re-run the gate over
  `runs/20261004-corpus-fulltest/designs/*.json`, and count the new G6 findings. My upper bound from grep is 92.
- Get EJ's answer on the reviewer kind for a split build.

If the count is near zero, DIRECT holds. If it is near 92, 8.1 is a DECISION with a ready mutation.

(Runner-up: **7.3 at 3/3.** It is the plan's most confident category, and its check cannot fail as written; see check 1.)

## What I did not check

- **Nothing was executed.** No pytest, no `mutation_matrix.py`, no `--self-test`, no `intake_harness.mjs`, no gate run;
  each needed an approval this session did not have. The 2.2 conclusion (one lowered constant stays CAUGHT) and the 7.3
  conclusion (both cases pass today) come from reading `design_gate.py:180-198`, `mutation_matrix.py:168-178` and
  `intake.js:381`. Both should be confirmed by a run before anyone relies on them.
- **Git history** was searched at two commits only (`45b9c37`, `2a075cf~5`). The claim that `intake.js` "never"
  emitted a table pointer holds at those two points and in the working tree. I did not walk the full history.
- **"92 designs"** counts files containing "+ Codex". I did not confirm that each one pairs a codex reviewer with a
  split builder; I checked one (`testlog.md:105-124`).
- **DOC-row citations not re-read:** 4.1, 4.2, 4.4, 4.6, 4.7, 4.8, 5.7 (`METHOD.md:333,426`), 6.5. I checked only 4.3
  (`DIAGRAM.md:213`), 5.2 (`METHOD.md:306,482`, `SKILL.md:139`) and 6.4 (`METHOD.md:200,272`).
- **Not checked:** the 94/300 and 150-node projections in `open-defects.md`; the surveys' citations from
  `docs/research/20261004-sunzi/`. I did not open those four files.
- **Whether the chair's rulings on 5.2 and 6.4 are right on the merits.** I checked that their citations exist, not
  whether DECISION and DOC are the correct verdicts.
- **Things I noticed about the algorithm, outside this verification's scope:**
  - The register's header says "44 distinct issues", but its table has 45.
  - `debugging` is a `mixed`, loop-pattern category whose diagnosis-only run is read-only. A "loop-pattern building
    node must carry `loop`" rule (1.4/1.6) has to decide what that means for a mixed node, and no survey addresses it.
  - Folding the 3.0 restatement into the readiness agent (7.1) puts it in the same call as readiness, not before it.
