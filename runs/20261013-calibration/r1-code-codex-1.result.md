node: r1-code-codex

Changed only the four permitted files. No commit. Frozen acceptance still fails.

- F1 — [verdict.py:227](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/verdict.py:227): empty scope prevents MEETS; parser portion outside scope.
- F2 — [model_io.py:255](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/model_io.py:255): judge folder separated; plant identity kept in coordinator metadata.
- F3 — [probe_matrix.py:29](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/probe_matrix.py:29): unchanged; edits forbidden.
- F4 — [verdict.py:145](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/verdict.py:145): integrity guard added; matrix producer unchanged.
- F5 — [verdict.py:132](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/verdict.py:132): mutant health guard added; matrix producer unchanged.
- F6 — [evaluate-requirements.js:114](/home/smoke01/dev/ancient-games-evaluator/.claude/workflows/evaluate-requirements.js:114): one repair round wired; required repair brief is missing.
- F7 — [evaluate-requirements.js:124](/home/smoke01/dev/ancient-games-evaluator/.claude/workflows/evaluate-requirements.js:124): one judge retry using the next valid plant.
- F8 — [workspace.py:25](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/workspace.py:25): exclusions apply at every depth; custom globs add.
- F9 — [model_io.py:412](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/model_io.py:412): mutant view and collection added; workflow supplies scratch HOME/TMPDIR.
- F10 — [workspace.py:50](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/workspace.py:50): stale evidence refused.
- F11 — [verdict.py:43](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/verdict.py:43): malformed entries skipped and reported; model I/O also hardened.
- F12 — [workspace.py:128](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/workspace.py:128): resolved run containment enforced; workflow validates runId upfront.
- F13 — [verdict.py:79](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/verdict.py:79): shell quoting retained.
- F14 — [verdict.py:233](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/verdict.py:233): unparsed ids block MEETS; parser portion outside scope.
- F15 — [verdict.py:177](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/verdict.py:177): duplicate classifications become human.
- F16 — [verdict.py:212](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/verdict.py:212): out-of-scope ids carry reasons.
- F17 — [model_io.py:381](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/model_io.py:381): output validation added; unfinished models block.
- F18 — [model_io.py:399](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/model_io.py:399): UTC stamps, agent count, and unreported tokens recorded.
- F19 — [evaluate-requirements.js:131](/home/smoke01/dev/ancient-games-evaluator/.claude/workflows/evaluate-requirements.js:131): matching run provenance required; authoritative JSON returned.
- F20 — [verdict.py:219](/home/smoke01/dev/ancient-games-evaluator/tools/evaluator/verdict.py:219): orphan probes reported in JSON and Markdown.

**Choices not in the spec**

Zero-based entry positions; models recorded in `cost.json`; repair metadata uses `round` and `cases`; scratch folder is `probe-scratch`. Mutant prompts resolve the brief through `$PWD`; judge prompts override the older brief’s paths.

CONTRADICTS `test_meets_is_false_when_there_is_no_in_scope_requirement_at_all` E10 counts: asserts two out-of-scope ids after evaluating the empty spec.

CONTRADICTS `test_a_matrix_with_no_runs_key_is_an_older_matrix_and_still_proves` R1-F5(c): expects PASS from one failed result. Other PASS assertions reuse this unhealthy fixture.

CONTRADICTS `test_a_judge_answer_whose_root_is_not_an_object_is_dropped_rather_than_crashing` R1-F2: writes call 1 in the run folder instead of the judge folder.

CONTRADICTS `test_an_exclude_glob_replaces_the_default_tests_glob` R1-F8: expects custom exclusions to restore excluded tests.

CONTRADICTS `test_confirm_check_keeps_a_probe_whose_both_quotes_are_there` R1-F6: expects the old two-column stdout; three other confirmation tests do likewise.

CONTRADICTS `test_judge_input_names_the_first_judged_case_with_a_valid_plant` R1-F2: expects exposed plant metadata and old stdout. Other older judge tests use the removed locations.

CONTRADICTS `test_an_open_id_gets_no_verdict_and_is_listed_out_of_scope` R1-F16: expects strings instead of objects.

CONTRADICTS `test_a_product_copy_that_was_not_restored_makes_every_case_unknown` R1-F4: requires “restored” in the new mandated reason.

CONTRADICTS `evaluate_harness.mjs::repairRound` R1-F6: conditional fixtures omit responses for required repair calls.

CONTRADICTS `evaluate_harness.mjs::judgeRerun` R1-F7: retry responses are missing; its “no other plant” order also excludes the required input call.

CONTRADICTS `evaluate_harness.mjs::excludeGlobs` R1-F8: rejects correctly shell-quoted glob arguments.

**Command summaries**

- Full pytest: **804 passed, 57 failed**, exit 1. Includes 24 failures in forbidden-to-edit parser/matrix modules.
- Workflow harness: **13 PASS, 7 FAIL**, exit 1.
- Feature gate: scope, protection, and new-test checks pass; **25 baseline failures**, exit 1.
- `git diff --check`: pass.
- Codex-authored supplemental checks: **87 passed**; these do not establish independent acceptance.