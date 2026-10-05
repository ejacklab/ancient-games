# FIX_SPEC — the 13 programming bugs

Scope: the 13 programming bugs from `runs/20261004-defect-register.md`. Of the 13, **9 have a test that fails
against the current code and passes after the fix**; **2 are Blocked** (1.5, 7.2); **2 are already corrected or
fixed and get no builder action** (2.5, 7.4).

The readiness family (3.1–3.5) follows the verifier's ready set in
`runs/20261004-domain-fix-review/VERIFICATION.md` §1, which names the test that flips for each. For 1.4/1.6/7.1/7.3
the check is designed here, because that is what the verifier said was missing.

---

## 1.4 + 1.6 — the gate must require a `loop` object on every node whose category's default pattern is a loop, and it must read that from the parsed `pattern` column (one change fixes both)

- **Intended behaviour**: `docs/TASK_TYPES.md:86` gives every category a "Default pattern"; the rows whose pattern
  text contains "loop" — `code generation`, `ui/ux dev`, `debugging`, `test script gen` — describe loop work, and
  `docs/TASK_TYPES.md:28-29` ("Default-first") makes that pattern the default the gate enforces. Method 3.5
  (`docs/WORKFLOW_DESIGN_METHOD.md:243-256`) makes the loop's limit, exit and feedback mandatory. After the fix,
  `design_gate.py` must (a) derive loop-ness from the parsed `pattern` cell, not from any hardcoded category-name
  list, and (b) fire G3 when a node of such a category carries **no** `loop` object — not only when a `loop` object
  already exists, which is today's `if lp is not None` gate (`design_gate.py:165-172`). Every node whose category
  row is loop-pattern must carry `loop` with integer `limit` ≥ 1, non-empty `exit`, non-empty `feedback`. A node of
  a non-loop category may still opt into a loop and is then validated by the same three field checks.

- **The edit**: In `parse_types` (`design_gate.py:86-102`), store `"loop": "loop" in r[2].lower()` on each category
  row, keeping `"pattern": r[2]` as-is. In `validate_design`'s node loop (`design_gate.py:165-172`), replace the
  `lp = n.get("loop")` / `if lp is not None` gate so that a node whose category row has `loop` true and no `loop`
  object appends one G3 finding (e.g. `G3: node <id> is a loop-pattern category but carries no loop`) and skips the
  field checks; validate `limit`/`exit`/`feedback` whenever a `loop` object is present or the category is
  loop-pattern. Do **not** add a hardcoded loop-category list to `design_gate.py`.

- **The test**: two, each failing before and passing after.
  1. `tests/workflows/mutation_matrix.py`: add a mutation row `("loop object missing", m_loop_missing, "G3", "")`
     where `m_loop_missing(d)` does `del d["nodes"][0]["loop"]`. The matrix's base design `p050.json` node `n1` is
     `code generation` with a loop, and `d["nodes"][0]` is that node. Today the stripped design returns no findings
     (confirmed: `validate_design` returns `[]`), so the matrix reports MISSED and exits 1; after the fix it reports
     CAUGHT and exits 0. `python3 tests/workflows/mutation_matrix.py --self-check` then also reports MISSED for it
     (the matrix's neuter pass already does this generically).
  2. New unit test in `tests/test_task_types.py`, e.g. `test_parse_types_marks_loop_from_the_pattern_column`: write a
     minimal TASK_TYPES.md to a `tmp_path` with a `| Category | Touches product | Default pattern | Default engine |
     Default check | Sabotage (proof the check can fail) |` table carrying one row whose Default pattern contains
     `loop` and one whose does not, call `dg.parse_types(p)`, and assert the loop row has `loop` is `True` and the
     step row has `loop` is `False`. Before the fix the `loop` key does not exist (KeyError); after it does. This is
     the check that pins "reads `pattern`" rather than a hardcoded list.

- **Risk**: `debugging` is a loop-pattern **mixed** category, but a diagnosis-only debugging run is read-only
  research (`docs/TASK_TYPES.md:91`). This spec requires a loop on every loop-pattern node regardless of `builds`,
  which is consistent with the corpus (zero loop-pattern nodes lack a loop, confirmed) and with
  `tests/test_task_types.py:24` `LOOP_CATS` / `design_for` (which always attach a loop) and
  `test_mixed_category_semantics`. If EJ instead wants read-only mixed nodes exempted, the rule changes to "require a
  loop only when the category product is `yes` or the design builds" — that variant is a separate decision and is
  not specified here. Regression nets: `test_gate_accepts_every_corpus_design`, `test_gate_self_test_cli`,
  `test_mixed_category_semantics`.

---

## 3.1 — `check_blueprint` must be able to fail: a directory with no map (or no section file) is MISSING, not VERIFIED

- **Intended behaviour**: the blueprint check's whole job is separating a fixed target from its absence
  (`docs/WORKFLOW_DESIGN_METHOD.md:99-110`); "verified" means the target is there. An existing directory whose own
  detail says "map MISSING" or "0 sections" must not be VERIFIED (`runs/20261004-defect-register.md` 3.1). The
  script's own contract (`readiness.py:21`) says an explicit `--blueprint` dir that is MISSING exits 1.

- **The edit**: rewrite `check_blueprint` (`readiness.py:197-205`). Add
  `SECTION_FILES = {"01-vision.md", "02-requirements.md", "03-domain-model.md", "04-business-logic.md",
  "05-architecture.md", "06-data-model.md", "07-ui-ux.md", "08-non-functional.md"}` (the blueprint's section
  filenames, `docs/workflow-templates/blueprint.md:8-18`). Count only the files in `SECTION_FILES`. Return MISSING
  with detail `f"map MISSING, {len(sections)} sections: {', '.join(sections) or 'none'}"` when `README.md` is
  absent; MISSING with detail `"map present, 0 sections"` when no section file exists; otherwise VERIFIED with
  `f"{len(sections)} sections, map present: {', '.join(sections)}"` (sections sorted).

- **The test**: `test_rt_15` flips (`tests/test_readiness.py:413-419`). Change the run to
  `json_checks(sandbox.run("--blueprint", bp, "--json"), code=1)` and the assertion to
  `assert_row(checks, f"blueprint ({bp})", "MISSING", "map MISSING, 0 sections: none", bp, "Skills and workflows")`.
  Today the code reports `verified` with rc 0, so the flipped test fails; after the fix it passes.

- **Risk**: `exit_code` (`readiness.py:328-330`) already returns 1 for a MISSING blueprint, so a mapless `--blueprint`
  dir now fails the run — that is the intended "can fail" behaviour, and `test_rt_13`'s existing absent-dir case
  (`--blueprint nope`, rc 1) already documents it. Nothing else calls `check_blueprint` except `gather` under
  `--blueprint`.

---

## 3.2 — absent and empty directories must not report `verified`

- **Intended behaviour**: readiness separates verified from unknown/missing
  (`docs/WORKFLOW_DESIGN_METHOD.md:72-94`); "verified" means a command proved something. An absent or empty skills or
  workflows directory proves nothing, so it must not be `verified` (`runs/20261004-defect-register.md` 3.2). The
  verifier's accepted fix is to default `absent_status` to MISSING.

- **The edit**: in `check_dir_listing` (`readiness.py:184`), change the default parameter
  `absent_status: str = VERIFIED` to `absent_status: str = MISSING`. The two early returns already use
  `absent_status` for the absent and empty cases, so both become MISSING; the detail strings `absent ({p})` and
  `empty ({p})` are unchanged.

- **The test**: `test_rt_16` flips (`tests/test_readiness.py:422-426`) to
  `assert_row(..., "claude skills (user)", "MISSING", f"empty ({skills})", skills, "Skills and workflows")`, and
  `test_rt_01`'s directory loop (`tests/test_readiness.py:137-138`) flips its six absent-dir assertions from
  `"verified"` to `"MISSING"` (detail stays `f"absent ({path})"`). Both currently pass with `verified`; both pass with
  `MISSING` after.

- **Risk**: marking an optionally-absent directory (e.g. a user with no codex skills) MISSING is a semantic
  overstatement; if EJ objects, the fallback is minimax's per-call-site statuses (absent skills UNKNOWN, only a
  required item MISSING). `exit_code` (`readiness.py:322-331`) only fails on `--require`d tools and explicit
  blueprints, not skill dirs, so exit codes do not change; `test_rt_08`'s markdown-versus-json comparison still holds
  because both modes report the same status.

---

## 3.3 — "N sections" must count the blueprint's sections, not every `.md`

- **Intended behaviour**: the count is the blueprint's sections — exactly the eight section files — not arbitrary
  `.md` files in the directory (`runs/20261004-defect-register.md` 3.3;
  `docs/workflow-templates/blueprint.md:8-18` lists the eight).

- **The edit**: the same `check_blueprint` rewrite as 3.1 — count only the eight `SECTION_FILES`, not every `.md`.
  Fix this in the same edit as 3.1 (one function, two defects).

- **The test**: `test_rt_13` flips (`tests/test_readiness.py:369-378`). Change its blueprint fixture to
  `README.md` plus all eight section files plus `a.md`, `b.md` (and keep `notes.txt`), and change the assertion to
  `assert_row(..., f"blueprint ({bp})", "verified", "8 sections, map present: 01-vision.md, 02-requirements.md,
  03-domain-model.md, 04-business-logic.md, 05-architecture.md, 06-data-model.md, 07-ui-ux.md, 08-non-functional.md",
  bp)`. Today the code counts every `.md` and reports `11 sections, map present: 01-vision.md, 02-requirements.md,
  03-domain-model.md, 04-business-logic.md, 05-architecture.md, 06-data-model.md, 07-ui-ux.md, 08-non-functional.md`
  (11 files, truncated to the first 8), so the flipped assertion fails; after the fix it passes.

- **Risk**: the same rewrite makes a directory with `README.md` but no section file report MISSING (rc 1) — that is
  3.1's behaviour, not a regression, and no remaining test uses such a fixture. `test_rt_15` covers the map-missing
  side; the rewritten `test_rt_13` covers the counting side.

---

## 3.4 — `--require` must fail on a tool that is not verified, not only on MISSING

- **Intended behaviour**: `--require TOOL` means "tool that must be verified present; exit 1 if MISSING"
  (`readiness.py:369`). A tool that is present but whose `--version` times out or exits non-zero is UNKNOWN — not
  verified — so a `--require` on it must also exit 1 (`runs/20261004-defect-register.md` 3.4).

- **The edit**: in `exit_code` (`readiness.py:322-331`), replace the `missing`/`known` set logic with: for each
  required tool, return 1 unless there is a check for that tool with `status == VERIFIED`. Keep the separate
  `--blueprint` MISSING hard-fail loop (`readiness.py:328-330`) unchanged. Update the docstring at `readiness.py:21`
  to "1 a --require'd tool that is not verified, or an explicit --blueprint dir that is MISSING".

- **The test**: `test_rt_07` flips (`tests/test_readiness.py:255-258`). Change to
  `json_checks(sandbox.run("--require", "broken", "--json"), code=1)` and keep the row assertion
  `assert_row(checks, "broken", "unknown", "exit 3: boom on stderr", "`broken --version`", "Tools")`. Today the run
  exits 0 (confirmed), so the flipped test fails; after the fix it exits 1. Also update `test_rt_10`
  (`tests/test_readiness.py:317-332`): its hanging-binary run currently uses `--require claude` and asserts rc 0; a
  hanging `claude` is UNKNOWN, so after this fix `--require claude` would exit 1. Drop the `--require` there (run
  `sandbox.run("--json")`) so the test keeps asserting the timeout bound and the UNKNOWN row with rc 0.

- **Risk**: `--require` on any tool that cannot be verified now fails the run, which is the documented contract;
  `test_rt_06` (verified `git`, missing `nope`) is the regression net for the still-correct cases, and `test_rt_14` /
  `--self-test` is unaffected (its fake tool is MISSING, which is still a failure).

---

## 3.5 — a rc-0 non-model-list output must not count as verified models; a non-object `model` must not raise

- **Intended behaviour** (two halves of register 3.5):
  1. `check_agy_login` (`readiness.py:126-142`): an `agy models` run that exits 0 but prints an error line is not a
     verified model list. VERIFIED must require rc 0 **and** at least one line that is a model id.
  2. `check_qwen_config` (`readiness.py:145-167`): a `settings.json` whose `model` value is not an object must report
     UNKNOWN, not raise an uncaught `AttributeError` at `model.get(...)`.

- **The edit**:
  1. In `check_agy_login`, filter the id list to drop label lines:
     `ids = [l.split()[0] for l in out.splitlines() if l.split() and not l.lower().startswith("fetching")
     and not l.split()[0].endswith(":")]`. The existing `rc == 0 and ids` then reports VERIFIED only when a model line
     remains, and the existing fall-through reports UNKNOWN (`exit 0: <first line>`) otherwise.
  2. In `check_qwen_config`, after `d` is confirmed a dict and before `model.get(...)`: if `d.get("model")` is not
     None and not a dict, return `Check("Models and logins", item, UNKNOWN, "unreadable: settings.model is not an
     object", str(p))`. `modelProviders`, `env` and `security` hit the same `.values()`/`.get()` pattern on the same
     file and should get the same non-object guard (not separately tested).

- **The test**: two new tests in `tests/test_readiness.py`.
  1. `test_rt_agy_models_rc0_error_is_unknown`: fake `agy` whose `--version` prints `agy-fake 0.1` and whose
     `models` prints `error: not logged in` to stdout and exits 0; run `--json --net` and assert
     `assert_row(checks, "agy login (model list)", "unknown", "exit 0: error: not logged in", "`agy models`
     (network)", "Models and logins")`. Today the code reports `verified | 1 models: error: …` (confirmed), so the
     test fails; after it passes.
  2. `test_rt_03d_non_object_model_field`: write `~/.qwen/settings.json` = `{"model": "x"}`; run `--json` and assert
     the row `qwen config (model, provider)` is `unknown`, proof `str(path)`, detail starting `unreadable:`. Today the
     process raises AttributeError (rc 1, traceback in stderr — confirmed), so `json_checks` fails; after it passes.

- **Risk**: `test_rt_12` (good `agy models` output) is the regression net for half 1 — its model lines
  (`gemini-9-pro`, `gemini-9-flash`, `gpt-oss-120b-medium`) have no trailing colon and still yield "3 models".
  `test_rt_21` (non-zero exit 3) still reports UNKNOWN via the unchanged fall-through. For half 2, `test_rt_03c`
  (non-object top-level settings) and `test_rt_05` (valid settings) are the regression nets.

---

## 7.1 — run method 3.0's restatement before readiness, and check it in code

- **Intended behaviour**: `docs/WORKFLOW_DESIGN_METHOD.md:30-70` ("3.0 Understand the challenge — before anything"):
  from the challenge text alone, state the objective, what is in scope, what is out of scope, and a provisional
  category, and put them beside the verbatim challenge "so EJ sees and can correct what the run understood before
  tokens are spent" (`:66-67`). `intake.js` today dispatches readiness first (`intake.js:620-623`) and never asks for
  or checks a restatement.

- **The edit**:
  1. Add a `restatement` object to `READY_SCHEMA` (`intake.js:55-95`) with string properties `objective`,
     `in_scope`, `out_of_scope`, `provisional_category`, all `required`, and add `'restatement'` to
     `READY_SCHEMA.required`.
  2. Add a code-side check beside `checkBlueprint`, e.g. `checkRestatement(ready)`, returning
     `['restatement: readiness did not report the 3.0 restatement']` when the field is absent and one named failure
     per empty string (`restatement: the objective is empty`, etc.). Call it in the readiness loop by changing
     `intake.js:625` to `failed = checkRestatement(ready).concat(checkBlueprint(ready.blueprint))`.
  3. In `readyPrompt` (`intake.js:504-524`), add a step 0 instructing the agent to restate the challenge (objective,
     in scope, out of scope, provisional category) before creating any file.

- **The test**: in `tests/workflows/intake_harness.mjs`, add a `RESTATEMENT` constant
  (`{ objective: '…', in_scope: '…', out_of_scope: '…', provisional_category: 'others' }`), add
  `restatement: RESTATEMENT` to the `READY` and `READY_FEATURE` canned answers (and every other canned readiness
  answer), and add a readiness-sabotage case: `'1-'` = `{ ...READY, restatement: { ...RESTATEMENT, objective: '' } }`
  → expect `result.status === 'unverified' && result.step === 1 && named(result, 'restatement: the objective is
  empty') && calls.length === 2`. Today there is no check, so the same ready answer reaches `verified` and the
  assertion fails; after the fix it stops at step 1. The harness stub enforces no schema `required`
  (`intake_harness.mjs:58-71`), which is why the code-side `checkRestatement` is the load-bearing part.

- **Risk**: every existing harness scenario uses a canned readiness answer, so each must gain a valid `restatement`
  or every "good" case starts failing at step 1 — the test edit above covers that in the same change as the code.
  `checkBlueprint` behaviour is unchanged; the two-attempt readiness repair path is already exercised by the existing
  `readySabotage` loop. (The loop's log line says "blueprint check(s) failed"; leaving or renaming it is cosmetic.)

---

## 7.3 — accept 3.5 item 4's first exit (a fresh node on a stronger tier), not only "unclear"/"EJ"

- **Intended behaviour**: `docs/WORKFLOW_DESIGN_METHOD.md:253-256` — when a loop hits its limit, its exit is one of
  three: a fresh node on a stronger tier (with a handoff note and its own limit), back to the unclear list, or to EJ.
  `intake.js:381` accepts only the last two (`/unclear|EJ/`), so a loop whose exit is the stronger-tier fresh node is
  wrongly rejected.

- **The edit**: at `intake.js:381`, change `if (!/unclear|EJ/.test(p.exit_on_limit))` to
  `if (!/unclear|EJ|stronger tier/.test(p.exit_on_limit))`. Keep it case-sensitive (do not add `/i`, which would make
  `EJ` match the `ej` in a word like `reject`). Leave the failure message as-is; if you extend it to name all three
  exits, update the harness's "another round" expected text in the same edit.

- **The test**: add one `intake_harness.mjs` pass case:
  `mutate(x => Object.assign(x.pieces[1], { exit_on_limit: 'a fresh node on a stronger tier with a handoff note' }))`
  run against the base design → expect `result.status === 'verified'`. Today the regex rejects that text (no
  `unclear`, no `EJ`), so the run is `unverified` and the assertion fails; after the fix it passes. The existing
  "another round" sabotage case (`intake_harness.mjs:339`, exit `start a fresh review round`) must still be
  `unverified` and named `goes back to the unclear list or to EJ` — it stays failing after the fix because
  `stronger tier` is absent from that text.

- **Risk**: the wider regex still rejects any non-tier "another round" exit (`start a fresh review round`) and the
  empty exit; the harness's `sabotage` / `designSabotage2` loops are the regression net. The design prompt prose
  (`intake.js:586-587`) still names only "unclear list or to EJ"; updating that prose is out of scope for this code
  bug, but it is why the three-exit vocabulary can drift again.

---

## Already corrected or fixed — no builder action

- **2.5** — published accuracies without a denominator: already corrected in prose (the README now states the
  denominators; `runs/20261004-domain-fix-review/FIX_PLAN.md` §4 marks it FIXED). No code edit and no test; the
  residue is a stale run record (`testlog.md:34`), not live code.
- **7.4** — the table-pointer check emitter was never `intake.js`; it was `tests/workflows/corpus_check.py:68-69`
  and `tests/test_task_types.py:44-45`, both already fixed (`runs/20261004-domain-fix-review/VERIFICATION.md` §4(a)).
  No code edit and no test.

---

## Blocked, and why

- **1.5** — G2 reads `builds` and `touched_paths` from the design itself (`design_gate.py:133-134`); the gate has no
  independent witness for them, and none exists at design time (the design has not run, so there is no `git diff`).
  Fixing the self-reference needs a post-run witness (`git diff --name-only`) or per-node file claims that no designed
  run produces. `runs/20261004-domain-fix-review/FIX_PLAN.md` §4 already routes this to LATER/DECISION — "EJ names the
  witness" (minimax: DECISION). Without that decision there is no edit whose test fails before the fix, so it is not
  checkable.

- **7.2** — depends on **5.1, a DECISION, not a programming bug**: which step records the product's test command and
  its output as the baseline before the first building node, and stop-versus-freeze when it is already red
  (`runs/20261004-domain-fix-review/FIX_PLAN.md` §4, DECISION). Until 5.1 is decided, "record the test command and its
  output" has no owner to attach a check to, so there is no test that fails on the current code without inventing a
  fix. Put it under Blocked and name the 5.1 decision.

---

## The order to build them in

1. **Readiness family first, one file** (`readiness.py` + `tests/test_readiness.py`): **3.1 and 3.3 together** (the
   same `check_blueprint` rewrite; 3.1's status semantics must land before 3.3's count is asserted), then **3.2**,
   **3.4**, **3.5**. The test edits must land in the same change as the code edits.
2. **Gate**: **1.4 + 1.6** (one change in `design_gate.py`; tests in `tests/workflows/mutation_matrix.py` and
   `tests/test_task_types.py`).
3. **`intake.js`**: **7.1** and **7.3** (distinct functions — `checkRestatement` / `READY_SCHEMA` / `readyPrompt`
   versus the loop-exit regex in `checkDesign`; either order, both before running the harness). 7.1's harness edit
   (add `RESTATEMENT` to every canned ready answer) must land in the same change as the code-side check, or the whole
   harness goes red.
4. **No build**: 1.5, 7.2 (Blocked); 2.5, 7.4 (already corrected/fixed).
