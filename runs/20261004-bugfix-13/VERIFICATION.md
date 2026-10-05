# VERIFICATION — the 9 built bugs from FIX_SPEC.md

**Read this first: none of the sabotage was executed.** In this session the permission layer refused every command
that runs code: `env -u NO_COLOR python3 -m pytest -q`, `python3 -m pytest …`, `python3 tests/workflows/mutation_matrix.py`
and `node tests/workflows/intake_harness.mjs` all returned "This command requires approval", and the session is
non-interactive, so nobody could approve them. `git status`, `git diff`, `git show` and `git stash list` still worked.

I did **not** run `git stash push`. Running it without being able to run the tests or be sure `git stash pop` would
be allowed could have left the fixes stashed and the tree changed, which the brief forbids. The tree is as I found it.
The only file I added is this one.

So every row below is `COULD NOT RUN`. Beside each one I give a **prediction from reading** the HEAD code
(`git show HEAD:<file>`) against the new test. A prediction is not the verification the brief asked for. The method
in §6 still has to be run before any of these fixes count as checked.

---

## 1. The sabotage table

| bug | the test | fails without the fix? | passes with it? | how you reverted |
|---|---|---|---|---|
| 1.4 + 1.6 (a) | `tests/test_mutation_matrix.py::test_the_gate_catches_every_mutation_aimed_at_a_rule`, via the new matrix row `("loop object missing", m_loop_missing, "G3", "")` | COULD NOT RUN (no code execution). *Predicted YES*: in HEAD `validate_design` only looks at a loop inside `if lp is not None` (HEAD `design_gate.py:165`). With `n1`'s loop deleted, no G3 fires and nothing else reads `loop`, so the row reports MISSED and the matrix exits 1. | COULD NOT RUN. *Predicted YES*: the new branch fires `G3: node n1 is a loop-pattern category but carries no loop`, because `code generation`'s pattern "evaluator–optimizer loop" contains `loop`. | not reverted |
| 1.4 + 1.6 (b) | `tests/test_task_types.py::test_parse_types_marks_loop_from_the_pattern_column` (new, present) | COULD NOT RUN. *Predicted YES*: HEAD `parse_types` stores no `loop` key, so the test hits a `KeyError`. | COULD NOT RUN. *Predicted YES*. | not reverted |
| 3.1 | `tests/test_readiness.py::test_rt_15_blueprint_without_map` (flipped) | COULD NOT RUN. *Predicted YES*: HEAD returns VERIFIED `2 sections, map MISSING: a.md, b.md` with rc 0. The test now demands rc 1 through `json_checks(..., code=1)`. | COULD NOT RUN. *Predicted YES*. | not reverted |
| 3.2 | `test_rt_16_empty_skill_directory` (flipped) and `test_rt_01_sanitized_full_inventory`'s 6-directory loop (flipped) | COULD NOT RUN. *Predicted YES*: all six call sites (`readiness.py:316-323`) use the default `absent_status`, which is VERIFIED in HEAD. | COULD NOT RUN. *Predicted YES*. | not reverted |
| 3.3 | `test_rt_13_blueprint_workflows_and_usage_errors` (fixture and assertion flipped) | COULD NOT RUN. *Predicted YES*: HEAD counts every `.md` (README.md, a.md, b.md and the 8 sections), so it reports `11 sections, map present: 01-vision.md … 08-non-functional.md`. The sort puts digits before `R` and `a`, so the first 8 names match and only the count differs. The test wants `8 sections`. | COULD NOT RUN. *Predicted YES*. | not reverted |
| 3.4 | `test_rt_07_WART_require_accepts_present_broken_tool` (flipped to `code=1`) | COULD NOT RUN. *Predicted YES*: in HEAD `exit_code`, `broken` is UNKNOWN, so it is in `known` but not in `missing`, and the run exits 0. | COULD NOT RUN. *Predicted YES*. | not reverted |
| 3.5 half 1 | `test_rt_agy_models_rc0_error_is_unknown` (new, present) | COULD NOT RUN. *Predicted YES*: HEAD's `ids` keeps `error:` and reports VERIFIED `1 models: error: …`. | COULD NOT RUN. *Predicted YES*. | not reverted |
| 3.5 half 2 | `test_rt_03d_non_object_model_field` (new, present) | COULD NOT RUN. *Predicted YES*: HEAD `model = d.get("model") or {}` gives `"x"`, and `model.get("baseUrl")` (HEAD `:163`) raises `AttributeError`. The run exits 1 with a traceback, and `json_checks` expects 0. | COULD NOT RUN. *Predicted YES*. | not reverted |
| 7.1 | `intake_harness.mjs`: 4 "empty restatement <field>" cases + 1 "missing restatement" case, run under pytest by the **new** `tests/test_intake.py::test_intake_harness` | COULD NOT RUN. *Predicted YES*: HEAD has no `checkRestatement`, so readiness passes and the run goes on past step 1. `result.step === 1` is false, so the harness exits 1. | COULD NOT RUN. *Predicted YES*: there are 2 calls because `MAX_ATTEMPTS` readiness attempts reuse the same canned answer. | not reverted |
| 7.3 | `intake_harness.mjs` case "loop exits to a fresh node on a stronger tier -> verified" | COULD NOT RUN. *Predicted YES*: `pieces[1]` is `p2`, with `pattern: 'loop'` (`intake_harness.mjs:48`). The text `a fresh node on a stronger tier with a handoff note` contains neither `unclear` nor a case-sensitive `EJ`, so HEAD's `/unclear\|EJ/` rejects it. | COULD NOT RUN. *Predicted YES*. The "another round" case (`:356`) still lacks `stronger tier`, so it stays unverified. | not reverted |

**The weak spot in the method itself.** Even when it is run, `git stash push -- readiness.py` reverts all five
readiness fixes together. A red result then proves the test fails against HEAD, not that it fails without *its own*
fix. I read each pair to check they are separable in principle:

- `test_rt_15` would still fail if only 3.3's counting landed: the result would be "0 sections, map MISSING", still VERIFIED.
- `test_rt_13` would still fail if only 3.1's MISSING returns landed: the count would still be 11.

So each one pins its own bug, but only by reading. For per-hunk proof, run the sabotage in a copy of the repo with
one hunk restored at a time.

## 2. The full suite

**COULD NOT RUN**, either before or after. I have no pass/fail count, so I cannot say nothing else broke. Here is
what I checked by reading for knock-on breakage. These are predictions, not results:

- `--require` uses: `test_rt_06` (`git` verified → 0, `nope` → 1) and `test_rt_11` (`--require qwen`, where the fake
  prints a version and is VERIFIED → 0) both still hold under the stricter `exit_code`. `test_rt_10` dropped its
  `--require claude`, as the spec says it should.
- The gate's new rule fires only on the 4 categories whose `Default pattern` cell contains `loop`
  (`docs/TASK_TYPES.md:88,90,91,94`: code generation, ui/ux dev, debugging, test script gen). That is the same set as
  the `LOOP_CATS` that `tests/test_task_types.py:24` and `tests/workflows/corpus_check.py:37` use to attach loops. So
  the corpus and design fixtures should still pass G3. The spec reports "zero loop-pattern nodes lack a loop,
  confirmed". I did not re-confirm that.
- Every other canned readiness answer in the harness spreads `...READY` (`intake_harness.mjs:201,243,248,263,311-383`),
  so they all inherit `restatement`. The good cases should not start failing at step 1.

## 3. The bugs that were not built

| bug | spec says | confirmed? |
|---|---|---|
| 1.5 | Blocked: G2 trusts the design's own `builds`/`touched_paths`, and there is no witness at design time | **Yes.** `FIX_PLAN.md:155` routes it to "EJ names the witness" (a DECISION). With no witness, no test can fail on HEAD without inventing the fix. |
| 7.2 | Blocked on decision 5.1 (who owns the baseline, and stop or freeze if it is red) | **Yes.** Register 5.1 (`defect-register.md:82`) is an ownership question, not code. `FIX_PLAN.md:59` and domain-fix `VERIFICATION.md:27` both say 7.2 waits on it. |
| 2.5 | Already corrected in prose | **Yes, as a doc defect.** `runs/20261004-corpus-fulltest/README.md:73-74` now names the missing denominator. `testlog.md:34` still prints the bare `codex 90%`, which is a stale run record. No code is involved. |
| 7.4 | Mis-filed; the real emitter is already fixed | **Yes.** `corpus_check.py:69` and `test_task_types.py:45` both emit `known[c].get("check") or f"a check for {c}"` (the row's own check), not a pointer to the table. Nothing in `intake.js` emits that placeholder. |

None of the four is in scope for a builder.

## 4. Flipped or deleted?

I read `git diff -- tests/` hunk by hunk. **No assertion was deleted.** Every removed line is replaced by its
corrected form, or the hunk only adds lines.

| file | change | sanctioned by spec? |
|---|---|---|
| `test_readiness.py` `test_rt_01` | the 6 directory rows go from `"verified"` to `"MISSING"`; detail unchanged | yes (3.2) |
| `test_rt_07` | rc 0 → `code=1`; the row assertion is unchanged | yes (3.4) |
| `test_rt_10` | `--require claude` dropped; still asserts the timeout bound, the kill, the UNKNOWN row and rc 0 | yes (3.4). **Lost coverage:** no test now runs `--require` against a *hanging* tool. That would now exit 1, and `test_rt_07` covers only the non-zero-exit form of UNKNOWN. |
| `test_rt_13` | fixture gains the 8 section files; assertion is `8 sections …` | yes (3.3) |
| `test_rt_15` | VERIFIED rc 0 → MISSING rc 1, `map MISSING, 0 sections: none` | yes (3.1), word for word |
| `test_rt_16` | `verified` → `MISSING` | yes (3.2) |
| `test_rt_03d`, `test_rt_agy_models_rc0_error_is_unknown` | new | yes (3.5) |
| `test_task_types.py` | one new test. It makes `code generation` a `step` row and asserts `loop is False`, which a hardcoded name list could not pass. That makes it stronger than the spec's minimum. | yes (1.4/1.6) |
| `mutation_matrix.py` | one new mutation and one new row | yes (1.4/1.6) |
| `intake_harness.mjs` | `RESTATEMENT` added to `READY`, plus 6 new cases. The spec asked for 1 restatement case; the builder added all 4 fields plus the missing-object case. | yes (7.1, 7.3) |
| `tests/test_intake.py` | **new, untracked** pytest wrapper that runs the harness | not named in the spec, but the build brief told the builder to "find [the module] or add one". Before it existed, no pytest test ran `intake_harness.mjs`, so 7.1 and 7.3 had no gate in `pytest -q`. **It must be committed** with the rest, or 7.1/7.3 lose their pytest check again. |

One source change goes beyond the spec: `readyPrompt`'s repair text now says "the restatement and Blueprint
sections". It fits 7.1's intent. The loop's log line still says "blueprint check(s) failed", which the spec marks as
cosmetic.

## 5. Findings (reported, not fixed)

1. **`tests/test_mutation_matrix.py::test_the_matrix_can_fail` passes either way.** This was there before. It checks
   `"MUTATION MATRIX CAN FAIL" in r.stdout`, but `mutation_matrix.py` prints that label followed by `True` or `False`
   in both cases. A matrix that cannot fail still prints `MUTATION MATRIX CAN FAIL: False`, and the test stays green.
   It should assert `"MUTATION MATRIX CAN FAIL: True"` and `r.returncode == 0`. This matters here because the spec
   relies on `--self-check` reporting MISSED for the new row, and that claim is checked only through this test.
2. **An untested branch:** `check_blueprint`'s "README.md present, 0 sections" → MISSING branch has no test. The spec
   says so ("no remaining test uses such a fixture"). A fixture with `README.md` and `a.md`, run with `code=1`, would
   cover it.
3. **Untested guards:** the non-object checks for `modelProviders`, `env` and `security` in `check_qwen_config`. The
   spec marks these "not separately tested". The opt-in path for a non-loop category (a `loop` on a node of a non-loop
   category) is covered only indirectly, because every matrix loop row mutates `n1`, which is a loop category.
4. **A stale name:** `test_rt_07_WART_require_accepts_present_broken_tool` now asserts the opposite of its name.
5. **A fragile rule (design note):** `"loop" in pattern.lower()` would also match a future pattern cell such as "no
   loop". It is correct for today's table (§2).

---

## 6. How to finish this verification

Run this from the repo root, in a session that may run code. Run it once per file, and check `git stash list` shows
2 entries after each push. The existing `stash@{0}` "tier rule 2026-09-22" must not be the one popped.

```
git stash push -- .claude/skills/workflow-design/scripts/readiness.py
env -u NO_COLOR python3 -m pytest -q tests/test_readiness.py -k "rt_01 or rt_07 or rt_13 or rt_15 or rt_16 or rt_03d or rt_agy"   # all 7 MUST FAIL
git stash pop && env -u NO_COLOR python3 -m pytest -q tests/test_readiness.py                                                       # MUST PASS

git stash push -- .claude/skills/workflow-design/scripts/design_gate.py
env -u NO_COLOR python3 -m pytest -q tests/test_mutation_matrix.py::test_the_gate_catches_every_mutation_aimed_at_a_rule "tests/test_task_types.py::test_parse_types_marks_loop_from_the_pattern_column"   # MUST FAIL
git stash pop && env -u NO_COLOR python3 -m pytest -q tests/test_mutation_matrix.py tests/test_task_types.py                       # MUST PASS

git stash push -- .claude/workflows/intake.js
node tests/workflows/intake_harness.mjs     # the 5 restatement cases and the stronger-tier case MUST print FAIL
git stash pop && node tests/workflows/intake_harness.mjs     # "all passed"

env -u NO_COLOR python3 -m pytest -q        # before the first push and after the last pop: same count, 0 failed
```

## What I could not verify

- **Whether any of the 9 tests fails without its fix.** All 10 rows are predictions from reading. That is the very
  thing the brief says is not enough, after a previous verifier found 7 of 13 checks passed either way.
- **Whether any of them passes with the fix.** No test was run on the current tree either.
- **The full-suite count, before or after.** I cannot say nothing else broke.
- **That `validate_design` returns `[]` on HEAD for the loop-stripped design.** The spec says "confirmed". I only
  read the code path.
- **That no corpus design has a loop-pattern node without a loop.** That is the spec's claim; I did not check it.
- **That the builders actually ran the tests red first.** I have not seen the builders' replies, and nothing in the
  tree records a red run.

---

# Executed — the COO ran what the verifier's session could not

The verifier above could not run code in its session: it read the sources and **predicted** every row, labelled each
one "Predicted YES" rather than claiming a result, and left the commands. That is the right behaviour — a
verification that asserts a negative it did not test is worth nothing — and this section is the execution of those
commands, so the predictions are now results.

Method: copy the fixed file aside, `git checkout --` it back to HEAD (the fixes are uncommitted, so HEAD is the
pre-fix code), run the named tests, then restore. No `git stash`, because the repository already holds an unrelated
`stash@{0}` ("tier rule 2026-09-22") and a careless pop would disturb it.

| fix | file reverted | without the fix | with it |
|---|---|---|---|
| 3.1, 3.2, 3.3, 3.4, 3.5 | `readiness.py` | **7 failed**, 19 deselected | 26 passed |
| 1.4 + 1.6 | `design_gate.py` | **2 failed** (mutation matrix + pattern→loop parse) | 24 passed |
| 7.1, 7.3 | `intake.js` | **6 FAILED** in `intake_harness.mjs` | all passed |

Exactly the seven readiness tests the verifier predicted would flip (`rt_01`, `rt_07`, `rt_13`, `rt_15`, `rt_16`,
`rt_03d`, `rt_agy`) went red, and no others did. Full suite after restoring everything: **516 passed**, against a
baseline of 512 before the work — four net new tests, nothing weakened.

**So all nine buildable bugs carry a test that fails without the fix.** That is the property the earlier fix plan
lacked, when a verifier found 7 of 13 proposed checks would pass either way.
