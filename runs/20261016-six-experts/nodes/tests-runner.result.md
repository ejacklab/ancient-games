# Result — tests-runner

status: done

Wrote the 23 acceptance tests for the six-experts runner from SKILL.md §1–2 and decisions D1/D2, every engine
mocked (`fe.start` and `fe.guard_text` replaced, so no claude, codex, agy, dsh, opencode or bun process is ever
started), and proved each one bites by running six planted mutants of the script in a scratch copy: all six were
caught by the tests written for them, and the unmutated copy passes 23/23.

## Files

- `tests/test_six_experts.py` (new, 23 tests)
- `runs/20261016-six-experts/nodes/tests-runner.progress.md` (pieces P1–P6, planned → start → done)
- `runs/20261016-six-experts/nodes/tests-runner.result.md` (this file)

Nothing else changed. `six_experts.py` was not edited (the mutants were copies under `/tmp/opencode/mut2/`, each
with `assets/` and `runs/20261013-four-seats` symlinked so `HERE`/`SEATS_ROOT` resolve). No commit.

## Commands and last lines

```
env -u NO_COLOR python3 -m pytest -q tests/test_six_experts.py
 23 passed in 0.06s

# six mutants of the script, each in /tmp/opencode/mut2/<name>/, tests run against the mutant
 M0-unmutated            23 passed
 M1-bare-allowedTools     2 failed, 21 passed   (the two --allowedTools tests)
 M2-dario-other-model     2 failed, 21 passed   (both same-model tests)
 M3-dario-gets-rules      7 failed, 16 passed   (PLAIN cleared → Dario gets rules and a list)
 M4-no-insight-load       4 failed, 19 passed   (Dave's brief loses "Load first" and both files)
 M5-no-index-check        2 failed, 21 passed   (both Dave citation checks)
 M6-no-opencode-wait      2 failed, 21 passed   (both opencode-serial tests)

env -u NO_COLOR python3 -m pytest -q          # whole suite, for the record
 5 failed, 1109 passed in 68.67s
```

All 5 whole-suite failures are outside this file and are not from it:

- `tests/test_six_experts_codex_quota.py` (4) — `run_linus.<locals>.fake_start() takes 8 positional arguments but
  9 were given`: the script's `start()` grew the `model` argument (D2), and that test's fake was not widened. It
  fails the same way with my file removed (`pytest -q tests/test_six_experts_codex_quota.py` alone: 4 failed,
  4 passed).
- `tests/test_skills_export.py::test_skills_export_is_current` (1) — `skills/` has drifted: the unexported
  workflow-design guard and SPEC changes of this run (round 2 and tests-index) are not in `skills/` yet. Nothing
  to do with six-experts.

## Coverage against the brief's promises

| Promise | tests |
|---|---|
| the Claude command keeps the prompt last, tools as one `--allowedTools=` argument | `test_claude_keeps_the_prompt_as_its_last_argument`, `…_passes_the_tools_as_one_allowed_tools_argument` (also pins that web/shell add `WebSearch,WebFetch,Bash`), `…_without_web_or_shell_asks_for_no_web_and_no_shell`, `…_without_a_model_falls_back_to_the_default` |
| Dave and Dario on the same model `claude-sonnet-5-5` | `test_dave_and_dario_are_assigned_the_same_model`, `test_dave_and_dario_both_run_on_claude_sonnet` (the `model` passed to `start`, plus `status.json`) |
| Dario's brief holds the question and the five sections, and no list, identity, "Load first" or insight path | `test_darios_brief_holds_the_question_and_the_five_sections`, `…_has_no_rules_identity_or_insights` (no `dario-list.md`/`-identity.md`/`-insight-index.md` written), `…_prompt_names_only_his_own_brief` |
| Dave's brief has "Load first: what was learned", the index path and the categories named with `--insights`; with none named he chooses from the index; the files land in the run's `seats/` | `test_daves_brief_says_load_first_and_names_the_index_and_categories`, `test_daves_insight_files_are_written_into_the_runs_seats_folder` (also pins the guard call `["show","--category","spec","--category","own-work"]`), `test_with_no_category_named_dave_is_told_to_choose_from_the_index` (no `show` call without a category), `test_an_empty_index_from_the_guard_is_recorded_not_left_out` |
| `check`: Dario passes on the sections alone; Dave fails on an id not in his index and on none without "No insight applies"; passes on an id from the index | `test_dario_passes_on_the_five_sections_alone`, `test_darios_plain_answer_is_not_judged_on_citations_or_chinese`, `test_daves_own_insight_id_passes`, `test_dave_fails_when_he_cites_an_id_not_in_his_index`, `test_dave_fails_when_he_cites_none_and_does_not_say_none_applies`, `test_dave_passes_with_no_citation_when_he_says_no_insight_applies`, `test_check_reports_dave_and_dario_together` (end-to-end `check`, all six answers) |
| two experts on opencode never run at the same time | `test_two_opencode_experts_never_run_at_the_same_time`, `test_the_waiting_expert_starts_only_after_the_first_opencode_expert_exits`, `test_one_opencode_expert_is_not_queued_when_the_other_is_on_codex` |

## How the mocking works

`run_seats` replaces `fe.start` with a fake that writes a valid answer file, so `fe.run` drives its real start /
wait / status / fallback logic; each fake process reports which experts were still running when it was launched,
which is what proves no overlap (no wall clock, so it does not depend on timing). `guard_text` is replaced, so
`bun` is never started. `fe.codex_left` is replaced, so the real `~/.codex` logs are not read. `check` is driven
through `check_one` (the same function `check` calls per answer) plus one end-to-end `check` over a run folder
with all six answers.

## CONTRADICTS

none.

Two things worth the runner author's eye, both read as mine rather than as SKILL.md's words:

- The brief in this task ("Two experts on opencode are never running at the same time") is tested through the
  *fallback path* too: the overlap only happens when Linus is on codex at the start and drops to opencode mid-run
  (`jobs["linus"]["engine"] == "opencode"` after a usage-limit failure). SKILL.md line 47 states the rule without
  saying which paths produce the collision; the test covers the codex-limit path (`codex_left` high) as well as
  the pre-run path (`codex_left` 20.0), because those are the two places `opencode_busy()` is consulted.
- `--only dave,dario` (the comparison the skill recommends in §1) needs `runs/20261013-four-seats` only for the
  four persona seats; `dave`/`dario` alone do not read it. Tests that need `linus` do read it, so those two tests
  depend on that folder existing in the tree.