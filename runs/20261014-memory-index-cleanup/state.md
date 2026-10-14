# State — 20261014-memory-index-cleanup

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning; put notes in your own output file. Never delete a log line.

## Challenge (verbatim)

EJ, 2026-10-14: *"ok create a workflow to clean up the memory_index.py"*, after the COO listed: *"the build session's
`memory_index.py` still accepts `R-` ids, lets merge-conflict markers through, and doesn't check the id form"*.

## Restatement (method 3.0)

`tools/memory_index.py` rejects an id not in W1.1's form and an entry with a conflict-marker line, in both modes, with
tests shown able to fail. The `R-` fix is out of scope: done on `fix/index-drop-runbooks` (`d990dab`), not merged.
Category (*inferred*): code generation + test cases gen + code review. Full text: `workflow-design.md`.

## Steps

| # | Step | Status | Output file |
|---|---|---|---|
| D | Design | done | workflow-design.md, readiness.md |
| X | Experts on the unclear spots (method 3.3) | done | experts/, experts/compare.md |
| N0 | Prep: spec lines, pin, worktree, baseline, canaries | done | baseline.json, plan.json, checks/, sabotage/control-n0.md, raw/canary-*.log |
| N1 | Acceptance tests, blind (Codex) | done, attempt 1 | nodes/n1-1.result.md, nodes/n1-1.diff; frozen at `930d603` |
| N2 | Script and unit tests, loop (opencode) | done, attempt 1 | nodes/n2-1.result.md, nodes/n2-1.diff, gate-1.txt; `3eb41cb` |
| N3 | Sabotage: mutants | done (one repair round; rerun after N4 fixes) | sabotage/ |
| N4 | Blind review, planted defect (Claude Sonnet 5.5) | done, attempt 1; plant found | nodes/n4-1.result.md |
| N5 | Close | done; merged `6415a1c` and pushed | report.md, traceability.md |

## Size decision

design — steps: 6, unclear spots: 2 questions (Q1, Q2) plus 5 stated defaults, risk: low to medium.

## Questions for EJ (one batch)

| # | Question | Provisional assumption if unanswered | Must be answered before building |
|---|---|---|---|
| Q1 | Merge `fix/index-drop-runbooks` (`d990dab`) to master first, and start from master? | yes | answered: yes (merged, `ca8e043`) |
| Q2 | Accept the spec wording for B2.3, B2.7, G4.2 and DESIGN step 5? | as written | answered: accepted as written |

## Log (append only)

- 2026-10-14 D done: design written; `readiness.py --require codex --require opencode --require git` exit 0 (versions
  only, no canary). Found during design: worktree `../ancient-games-index-r` on `fix/index-drop-runbooks` already
  holds the `R-` fix (`d990dab`, another session) → Q1. The requirements evaluator's run `20261013-eval-k1e` reports
  B1 and B2 PASS on that code (its `verdict.md`, *reported*).
- 2026-10-14 X done: four_experts `--only linus,sun-tzu,lao-tzu,dave` → `experts/`; check: 2 failures (fan-li not asked, by design; 老子 為/爲 script variant). Folded into the design, each marked with who raised it: spec committed on the build branch in N0 (孫子); trace_check copied and B2.7 added (孫子); fixture-id lint and a per-mutant control against masked tests (Dave); superseded status, trailing-junk, non-ASCII-digit and impossible-date cases (Linus, Dave); N2's exit moved from Codex to a Claude Opus subagent (老子, Dave); bound corrected to 11 worker calls (Linus); commit authority stated (Linus). 孫子's "tools/evaluator/ does not exist" was wrong: it is on build/evaluator.
- 2026-10-14 Q1 answered: EJ, *"yes please merge fix/index-drop-runbooks into main"* → merged into master as `ca8e043` (no conflicts); `pytest -q` 686 passed. Not pushed. N0 branches from master. Still waiting: Q2, and the id-form level (all four experts rate W1.1's form SHOULD — `runs/20261014-sot-must-should/round2/compare.md`), which decides error versus warning.
- 2026-10-14 Q2 answered: EJ, *"MUST, accept Q2 wording, go ahead and push"*. The id form is MUST, so an id not in W1.1's form is an error (design as written, no warning mode); the spec wording for B2.3, B2.7, G4.2 and DESIGN step 5 is accepted as written. master pushed to origin (`5c68878..ca8e043`). All questions answered; the run waits for EJ's go.
- 2026-10-14 EJ: *"run it, go ahead to start the cleanup"* → run started.
- 2026-10-14 N0: worktree `../ancient-games-index-clean`, branch `fix/index-id-and-markers` from master `ca8e043`; spec lines committed `662603b` (sha256 REQUIREMENTS.md 8c1521c8…, DESIGN.md 31dad122…); `checks/trace_check.py` (B2.7 added; self-test PASS; fails on the current test file: "missing criterion ids: B2.7"); `checks/fixture_ids.py` (new; self-test PASS; fails on the current test file: 30 literal ids — first run flagged 4 `pytest.param` case names, fixed); baseline 686/686 pass in two runs (`baseline.json`); canaries: codex `gpt-6.1-sol` (log header), opencode `MiniMax-M3.1-Flash-Preview`, Sonnet subagent `claude-sonnet-5-5`, each "CANARY OK". Addition by the COO, not in the design: a reference patch (form + marker check on the old script), kept outside the repo until N2 is done, to check that N1's tests all pass on a correct script — it catches tests masked by a computed id, which the lint cannot see.
- 2026-10-14 N1 attempt 1 started: Codex in a code-free workspace (a fresh git repo holding only the spec, the test file, the hooks and the two checks; no history of the script).
- 2026-10-14 N0 control: the earlier run's 32 mutants on the start tree → `sabotage/control-n0.md`: 30 killed; M03 no longer applies (the `R-` fix changed its text); M27 (C1.2 bad rev) survives, as it did in all three of the earlier run's tables — a known gap, out of scope, not caused by this run. N0 done.
- 2026-10-14 N1 attempt 1 done (codex gpt-6.1-sol, 68,175 tokens, exit 0): 5 new tests, 41 fixture-id sources converted, 300 tests collect. COO's checks: `trace_check.py` "all 30 in-scope ids cited"; `fixture_ids.py` pass; against the unchanged script 108 failed, 192 passed — every failure is in the two new negative tests (`test_invalid_id_forms_fail_in_every_status` 54, `test_conflict_markers_fail_in_every_status` 54), no other test fails; against the COO's reference patch 300 passed. N1 raised three CONTRADICTS: (1) SoT K6.3 says the tool does not check markers — expected, N5 changes that sentence; (2) B2.5 "a problem in an inactive entry beyond B2.3 is a warning" against B2.7 "an error in every status", and (3) B2's Fails if "a broken retired entry stops the build" — real wording clashes with what EJ accepted. Fixed by the COO on the build branch, `9acec67`: B2.5 and the Fails if now say "beyond B2.3 and B2.7" (*the COO's wording, for EJ at the merge*). Tests frozen at `930d603` (sha256 bdf31f35…); REQUIREMENTS.md now 6798cbc7….
- 2026-10-14 N2 attempt 1 started: opencode MiniMax-M3.1-Flash-Preview, --agent build --variant high, in `../ancient-games-index-clean`.
- 2026-10-14 N2 attempt 1 done (opencode MiniMax-M3.1-Flash-Preview, exit 0, no CONTRADICTS): script +19 lines (`ID_FORM` with ASCII classes and `fullmatch`; `flag_conflict_markers` over every line before the header is parsed), unit tests updated and extended. Full suite 885 passed. Gate (`gate-1.txt`): tests, scope, must-not, tamper ok; baseline FAIL on 57 "missing" — all are parametrized cases of `test_malformed_entries_fail_without_writing` (39) and `test_inactive_content_problems_warn_without_blocking` (18) whose names held the old fixture ids N1 replaced; under the new names all pass (30 + 18, and the 3 moved cases as 27 in `test_entries_require_top_level_nonempty_id`). Gate accepted by the COO with that reason. Committed `3eb41cb`.
- 2026-10-14 N3: 13 new mutants (COO, kept outside the repo until N4's verdict): 12 killed, 1 survived — the B2.7 "starts with" part had no test. Repair round to N1 with the requirement, not the mutant (`briefs/n1-repair.md`; codex, 37,310 tokens): one new test, 408 acceptance tests, both checks pass; committed `0f3faf3`. Rerun: 13/13 killed. Old 32 mutants on the new code: identical to N0's control mutant by mutant (30 killed, M03 not applicable, M27 the known survivor) — no test lost power.
- 2026-10-14 N4 attempt 1 started: Claude subagent `claude-sonnet-5-5`, review packet outside the repo.
- 2026-10-14 N4 attempt 1 done (claude-sonnet-5-5, 111k tokens): the plant was found (F1, high), verified with the reviewer's own probes, so the review stands. Plant logged after the verdict: `sabotage/plant-review-1.txt`. COO fixed F3–F6 (`48162f0`); F7 not changed (unit tests pin the script's own messages, as before); F2, F8, O1, O3 to the backlog; O2 noted (408 acceptance tests run in about 21 s). Gate-2 (base `0f3faf3`): tests, scope, must-not, tamper ok; the same 57 renamed cases. N3 rerun with mutants updated to the new code text plus N14: 13/14 killed by the acceptance file, N14 (first marker only) killed by the unit file only — backlog. Old mutants identical to the control.
- 2026-10-14 N5 done: 994 passed (full suite, `6126804`); core.hooksPath empty; no `project-memory/`; SoT K6.3 sentence changed on the branch (*proposed*, for EJ at the merge); BACKLOG item 5 closed, five new items; evaluator skipped (not on master); ledger row waits for the merge (the main tree's ledger has another session's uncommitted edits). `report.md`, `traceability.md`. Branch `fix/index-id-and-markers` not merged, not pushed.
- 2026-10-14 Merged: EJ, *"merge into master and push"* → `6415a1c` (no conflicts; merged tree identical to the branch tip, which passed 994/994 in its worktree), pushed `ca8e043..6415a1c`. On the main tree 993 passed, 1 failed: `test_skills_export_is_current`, from another session's uncommitted edits to `.claude/skills/requirement-check/SKILL.md` and `skills/requirement-check/SKILL.md`, not from this merge. Ledger row still pending (the main-tree ledger has another session's uncommitted edits).
