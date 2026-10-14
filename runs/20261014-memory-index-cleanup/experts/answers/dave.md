# Dave: the experiments behind the design's unclear spots

## Answer
None of the seven listed spots (Q1, Q2, D1–D5) is of kind *unknown*. All seven are decisions, so they need EJ's word, not an experiment. I raise six unknowns, N1–N6. Two of them (N1, N5) I settled with cheap read-only checks today. N2 is already covered by the design's canary but has no exit if the canary fails. N3 is the one that matters most: once the id-form check exists, 13 existing rejection tests can pass for the wrong reason. It needs one deterministic lint added to N1's check. It also needs a decision on where N3's mutant count starts.

| Spot | Kind | Verdict |
|---|---|---|
| Q1, Q2 | decision | EJ's. No experiment. N1 below gives Q1 a fact. |
| D1–D5 | decision (default) | EJ's. No experiment. D5 gets a fact (N5). D3 gets a cost (N4). |
| **N1** Does `d990dab` merge cleanly into master? | unknown, **settled** | `git merge-tree --write-tree master d990dab` reports **clean**. I ran it today: n=1, on today's master. |
| **N2** Is Codex past its usage limit? | unknown | The design's N0 canary is already the smallest experiment. I predict it succeeds (reset reported for 2026-10-13 23:27). Stop: one call. **Missing:** what N1 does if the canary fails. That goes to EJ. |
| **N3** Rejection tests masked by the new id check | unknown, **new, highest priority** | Add a fixture-id lint to N1's check. Prediction and stop below. |
| **N4** Real entries that quote a marker line | unknown, little data | No experiment possible yet. The cost is noted. Proposed B2.7 already decides the fenced-code case. |
| **N5** Is the evaluator on master (D5)? | unknown, **settled for today** | `git ls-tree master tools/` lists only `export_skills.py` and `memory_index.py`. Under D5 the evaluator is skipped unless `build/evaluator` merges before N5. |
| **N6** Edge cases of the id pattern | unknown | Two hidden mutants in N3 test it. One sub-question goes to EJ. |

## How I decided
1. Before proposing anything, I asked what is already measured (my #5). The table holds only decisions. So I read the test file, SoT W1.1/K6.3 and the git state for unknowns the table does not list.
2. **N1.** Running a test cost less than debating Q1 (my #2). Merge base `d137f48`; one commit ahead (`d990dab`); merge-tree clean. *What it does not establish:* that the merged tree passes the suite. merge-tree checks only for text conflicts. *Who wrote the check:* me. Q1 itself stays EJ's.
3. **Old mutants (feeds N3, design step 4).** Same rule (my #5). I counted the 32 mutants in `runs/20261012-index-md-build/sabotage/mutants.json` whose `old` text occurs exactly once: **30 on master, 29 on `d990dab`**. So on the Q1 = yes path, I predict about 29 apply. The rest are "listed, not counted", per the design. Script mine, run once (my #10: a count, not a law).
4. **N3, the main finding** (my reading, from the code). In `tests/test_memory_index.py`, `INVALID_ENTRIES` (13 cases) is used by `test_malformed_entries_fail_without_writing`. Twelve of the 13 cases use `id: bad`, `id: ''` or `id: nested-only`. The test asserts only `returncode == 1` and `"D-bad.md: "` in the output. Once the id-form check exists, each of these entries fails on its id alone. So the test still passes if the status, kind, Why or header check is deleted.
   - The design's step-2 check ("against the unchanged script, every other test passes") cannot see this, because the unchanged script has no form check.
   - N3's rerun of the old mutants cannot see it either. A masked test *kills* those mutants for the wrong reason, so the count looks healthy (my #4: a control is only a control if it can come out differently).
   - The design's line "every fixture id into W1.1's form" covers this **only if** N1 actually converts these deliberately "bad"-looking ids. The file has 15 `id: bad`, 4 `id: old`, and `write_entry` defaults to `D-20261012-a1`.
   - **Experiment:** a lint in N1's check, written by the COO. Every `id:` value and every `id=` argument in the acceptance file must match W1.1's form, except in tests whose docstring cites B2.3.
   - **Prediction, written first (my #3):** if N1's brief names `INVALID_ENTRIES` and `write_entry`'s default, the lint finds 0 leftovers. If it does not, at least 1 is left. That second part is my reading, not measured.
   - **Stop:** one deterministic run. A failure uses N1's existing repair attempt. No new limit.
   - **Sabotage for the lint:** the current file must fail it. It will, so the lint is shown able to fail before it is trusted.
5. **N3 control (my #4).** Write down the old-mutant result on master before N2 runs: the old mutants run against master's script and tests. The expectation is the earlier run's 31/32, restricted to the 30 that apply today. After N2, compare that list mutant by mutant, not as a total. A mutant killed before and surviving after means a test lost power. A total alone hides swaps.
6. **N4** (my #6, #7). Nature offers one mechanism that fits: thymic negative selection, where a detector is tested against "self" so it does not attack healthy tissue.
   - Same: a checker must be tested against valid entries (a good id passes; `=======` alone passes), not only against bad ones.
   - Different, and it matters: the thymus tests against the body's real self. Here no `project-memory/` exists, so "self" is only synthetic fixtures.
   - I keep the analogy only as a reminder of that gap. The data I have: no `.md` file in the repo has a line starting `<<<<<<<` or `>>>>>>>` (grep run today). That is evidence about docs, not about entries.
   - Proposed B2.7 already settles the fenced-code case: a fenced line still "starts with" the marker, so it is an error.
7. **N6** (my #2, #3). The pattern for `DD-MM-xxxxxx-YYYY` has two cheap failure modes, each a hidden COO mutant in N3: matching only the start of the string (trailing junk passes), and checking the raw value before quotes and spaces are stripped. The file already parses `id:   'D-20261012-a1'  `.
   - Prediction: N1's tests as the design specifies them (good id; `D-20261012-a1`, `" "`, five random characters, upper case) kill the quote mutant. I predict they do **not** kill the trailing-junk mutant unless a case like `14-10-a1b2c3-2026x` is added.
   - Stop: one N3 run. A survivor goes through the design's existing repair round.
8. Reporting (my #9). If the canary, the lint or a mutant gives a null or negative result, it goes into `report.md` with the same weight as a pass.

## What I need to know
- **N2:** if the Codex canary fails at N0, what happens? Does the run wait for Codex, or does N1 move to another engine? If another engine, N1 and N2 must not end up on the same engine, or the blindness the design relies on is lost. The design gives N1 no exit before it starts.
- **N6:** W1.1 says "digits" and "lowercase letters". Are they ASCII only? Python's `\d` also matches non-ASCII digits. If EJ says ASCII, add one test case. If EJ says it does not matter, drop that case. I have not chosen a value.
- **N3 baseline:** should the mutant comparison start from master (30 apply) or from `d990dab` (29 apply)? This follows from Q1. If Q1 = yes, the merged tree is the baseline.

## Costs and risks
- The lint (N3) costs one short script and one check run. The risk is false alarms on ids built in code, such as `id={id}` or `raw.replace("id: old", ...)`. The lint must read string values, not names. If it is too crude it blocks N1 on a false failure (my #3: the prediction can be wrong both ways).
- The per-mutant control (step 5) adds one N3-sized run before N2. If skipped, the price is that a masked test passes unseen (my #4).
- My N1 and N5 results are a snapshot of today (my #10). Master or `build/evaluator` can move before the run, so N0 should run both again. Each costs a second.
- N4 cannot be tested without real entries. A false error on a legitimate quoted marker is possible later (my #7: the analogy's key condition, a real self-set, is missing).
- Two extra hidden mutants in N6 cost about a minute of N3 time. They must stay out of every worker-read file until the verdict, as the design already says for N3's mutants.

## How we would know I was right
- **N3:** after N1, the lint shows 0 non-W1.1 ids outside B2.3's tests. Run one old status- or kind-check mutant against the new script and new tests: it is killed, and the failure message names the status or kind problem, not the id. If the message names the id, the masking is real and my concern was right. If the lint finds nothing on the first try, my second prediction (at least 1 leftover without a named brief) was wrong, and I report it (my #9).
- **Per-mutant control:** the kill list on the new code matches master's on every mutant that applies to both.
- **N6:** the trailing-junk mutant survives N1's tests as specified (my prediction). If it is killed, my prediction was wrong, and that is recorded as a result.
- **N1/N5:** N0's own merge and `git ls-tree` give the same answers as mine today.
