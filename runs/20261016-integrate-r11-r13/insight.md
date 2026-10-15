# Insight — run 20261016-integrate-r11-r13 (the main agent's session)

## F-8392b4ce — criteria marked late in a session that ran several tasks

Whys:
1. Why was a failure logged? The Stop hook's late-criteria check found this session's first `touched` record for `criteria.yaml` (2026-10-15T17:13Z) later than the session's first success or failure record.
2. Why was there an earlier record? This session has run several tasks since 2026-10-15 (rounds 4–6, the score run); their success lines and failures carry the same session id.
3. Why does that make this task's criteria late? The check compares against the session's first record, not the first record of this task — it treats one session as one task.
4. Why does it do that? SPEC Round 6 K2 ("late criteria") names the session as the unit; a task boundary is not recorded anywhere the guard can read.
Source: check — SPEC Round 6 K2 and its code in `guard/src/hooks.ts` (late criteria).
Root cause: the late-criteria check uses the session as the task boundary, so every criteria file after a session's first task reads as late — a false failure.
Options:
1. [check] Compare against the first success or failure record after this session's last `UserPromptSubmit` before the criteria file was touched (the hook already sees every prompt; record its time), so the boundary is the request, not the session. evidence: the criteria file was written before any checked result of this request (state.md log; the first worker started after commit 57ca583).
2. [check] Compare only records whose time is after the previous criteria file of the same session was scored (all items marked), so each scored task closes a boundary. evidence: `runs/20261015-score/criteria.yaml` was scored 7/7 before this run began.
3. [rule] One task per session: the agent starts a fresh session for each request. evidence: this session spans 2026-10-15 to 2026-10-16 and seven requests; cheaper to fix in the check than to restart sessions.

## F-4cbb2f4b — an ambiguous line in my spec made the coder's output wrong

Whys:
1. Why was a failure logged? Four harness-health item names came out as `(12) withdrawal conditions (R12.6)` instead of `withdrawal conditions (R12.6)`.
2. Why? The coder copied the spec's list items exactly as written, `(12) …`, which is what the spec said.
3. Why did the spec say that? I wrote the requirement number as a `(req)` prefix inside the list item, without saying so — in the line above I had defined the other fields in words, so the prefix read as part of the name.
4. Why did nothing catch it before the coder ran? The spec had no example row for H4, unlike H3's table, and no check reads a spec for fields that mix two values.
Source: instruction — the spec's H4 list (`runs/20261016-integrate-r11-r13/spec-harness-health.md`), written by the main agent.
Root cause: a spec list that put two values (requirement number and item name) in one field with no table or example.
Options:
1. [rule] Every spec item that defines several fields of a record is written as a table with one column per field, as H3 was (method 3.8, the brief's template, example and standard). evidence: H3 (a table) came out right; H4 (a list) came out wrong, same coder, same run.
2. [check] Before sending a spec, run each literal value in it through the test writer's reading: the test brief already makes a second engine read the spec — have it list every literal it will assert, and compare with the coder's before code starts. evidence: the two Codex test writers read the same spec in parallel.
3. [tool] The brief template gains an "Example output" line for every new record shape. evidence: `docs/workflow-templates/` brief template asks for an example; this spec had none for H4.

## F-05a1b440 — the spec mixed instructions into literal values a second time

Whys:
1. Why was a failure logged? Two tests (HH-18, HH-25) failed: the docstring's opening line did not name R11/R12, and the open-failure detail ended in "(ids not printed)".
2. Why? The coder followed the spec's words: "first paragraph" (read as the second paragraph) and a literal followed by an instruction in parentheses.
3. Why did the spec read two ways? The same habit as F-4cbb2f4b: I wrote literal output text and instructions about it on one line, with no example output.
4. Why was it not caught before code? The test writer read it the other way — the crossing caught it, but only after both engines had run.
Source: instruction — `runs/20261016-integrate-r11-r13/spec-harness-health.md` H1 and H5, written by the main agent.
Root cause: one cause with F-4cbb2f4b — spec lines that put literal output and instructions in one sentence with no example.
Options:
1. [rule] A spec quotes every literal output in backticks on its own, with instructions in a separate sentence, and gives one example line per new record. evidence: the two specs' "Corrections" section lists four such lines, all from this pattern.
2. [check] Before workers start, grep the spec for a backticked literal followed by a parenthesis in the same item and rewrite it. evidence: both H4 and H5 mistakes had that shape.
3. [tool] The brief template gains an "Example output" block that the test writer and the coder both copy. evidence: H3, written as a table, came out right in both engines.

## F-90389583 — the health script wrote under HOME through bun's cache

Whys:
1. Why was a failure logged? HH-28 ran the real guard with an isolated HOME and found new files under `HOME/.bun/install/cache`.
2. Why? bun writes its runtime transpiler cache under HOME on every run unless `BUN_RUNTIME_TRANSPILER_CACHE_PATH=0` is set (checked: two runs, with and without the variable).
3. Why did the code not set it? The spec said "writes no file" but nothing about the runtime it calls; the coder passed the caller's environment as it was.
4. Why did the spec not say it? The main agent did not know bun writes a cache on a plain run; the guard's earlier tests ran in the real HOME, where the cache already exists, so no test had shown it.
Source: instruction — the spec's H5 (the guard call's environment), written by the main agent.
Root cause: a "writes no file" promise checked only in a HOME where the runtime's cache already existed.
Options:
1. [check] HH-28, a real-runtime run in an empty HOME with a tree hash before and after — added in this run, and it kills mutant M1 (`mutants.txt`). evidence: `runs/20261016-integrate-r11-r13/mutants.txt`.
2. [rule] Every script that promises to write nothing and starts a runtime (bun, node, python) gets one test in an empty HOME. evidence: this failure appeared only in the empty HOME.
3. [tool] A guard trap entry noting bun's cache variable for read-only callers. evidence: the variable's effect, verified here; the trap file is `guard/data/traps.yaml`.

## F-b7c8635f — a malformed doctor row reached the report

Whys:
1. Why was a failure logged? HH-26 planted `guard: 7` and a secret in a doctor row's note; the note reached the report.
2. Why? The code checked that `harnesses` was a list, then used each row's fields without checking their types.
3. Why? The spec said "output that is not the JSON shape of Round 7 → unknown" but did not list the row's field types; the coder checked the top-level key only.
4. Why did the spec leave that out? Round 7 names the fields but not their types; the main agent assumed "shape" covered both.
Source: instruction — spec H5 and guard SPEC Round 7 J1 (field types not stated).
Root cause: an external payload's field types were not written into the spec, so its validation stopped at the top level.
Options:
1. [check] HH-26 with planted wrong types — exists, kills mutant M3. evidence: `mutants.txt`.
2. [rule] A spec that reads another tool's JSON lists each field with its type and the allowed values. evidence: the correction now lists harness/note as strings and guard as installed/absent/unknown.
3. [tool] The guard publishes its JSON shapes as a small schema file that `harness_health.py` checks against. evidence: three commands, three shapes, today described only in prose.

## F-76013d09 — the guard's pipe tests failed inside the Codex sandbox only

Whys:
1. Why was a failure logged? Three round-7 tests saw empty stdout from `spawnSync(bun cli.ts … --json)` when Codex ran them.
2. Why only there? The same tests pass 19/19, five runs in a row, outside the Codex sandbox; Codex runs commands under its bundled bubblewrap (its log warns that bubblewrap is not installed on PATH).
3. Why does the sandbox change it? Not established; the cause sits inside Codex's sandbox and bun's pipe handling, which this run did not open.
4. Why did it matter? A test writer cannot tell a sandbox artefact from a code defect, so it reported a contract failure that was not one.
Source: config — Codex's `workspace-write` sandbox with the bundled bubblewrap.
Root cause: tests that spawn a child process ran inside a sandbox whose pipe behaviour differs from the machine's, and the brief did not say how to tell the two apart.
Options:
1. [config-advice] Install the system bubblewrap package, as Codex's own warning asks, then rerun the three tests under Codex to see whether the bundled one is the cause. evidence: `nodes/tests-json.log` line 15.
2. [rule] A worker's test failure is reported with a rerun outside its sandbox before it counts as a code defect; the COO reruns it. evidence: 19/19 outside, 16/19 inside.
3. [check] The test-writer brief asks for a canary spawn (`bun -e 'console.log(1)'` through a pipe) before any spawn test, so a sandbox that loses pipe output is named first. evidence: the three failures were all spawn-through-pipe.

## F-c60edad6 — the harness refused the researcher's findings file

Whys:
1. Why was a failure logged? The researcher's Write to `research/findings.md` was refused: "Subagents should return findings as text, not write report files."
2. Why did it try? Its definition (`.claude/agents/researcher.md`: "Writes full findings to a file and returns only a short digest and the path") and my brief both told it to.
3. Why do those say so? Method 3.8 item 9 keeps the researcher's full findings out of the main agent's context by putting them in a file.
4. Why does that now fail? The harness refuses report files from subagents; the definition and the method were written before that refusal was seen here.
Source: instruction — `.claude/agents/researcher.md` and method 3.8 item 9, against the harness's current refusal.
Root cause: the researcher's contract (write a file) conflicts with what the harness now allows a subagent to do.
Options:
1. [rule] The researcher returns the full findings as text and the main agent saves them to the run folder; the digest comes first so the main agent can stop reading early. evidence: this run did exactly that, at the cost of the findings entering the main context.
2. [config-advice] Find whether a Claude Code setting lets a named subagent write report files, and if so set it for the researcher only. evidence: the refusal names report files, not all writes.
3. [tool] Run the researcher through another engine (Codex with `--search`, which writes files) when the findings are long. evidence: memory `codex-exec-web-search` — `codex --search exec` verified 2026-10-13.

## F-969500fa — a failing export test hidden inside a command chain

Whys:
1. Why was a failure logged (by hand)? The export test printed "1 failed, 1 passed" inside a `;`-chain that ended in `git commit`; no record was written.
2. Why no record? The guard's PostToolUse check reads the Bash call's exit, which came from `git commit` (0).
3. Why was the test inside the chain? I put export, stage, test and commit in one call to save turns.
4. Why did the test fail at all? It requires a clean `skills/` before re-exporting, and I ran it with the export staged but not committed — a stale-state run; after the commit it passed 2/2.
5. Why did my rule not stop it? The F-1e90a8e1 lesson ("don't pipe a command whose exit gates the next step") is a note in my session, not a check, and here the test did not gate the commit — so the rule as written did not apply, while the guard still lost the result.
Source: check — the guard's test-run detection reads only the call's exit code; plus the main agent's command habit.
Root cause: a test run's result is invisible to the guard whenever it is not the last command of its Bash call.
Options:
1. [check] The guard's PostToolUse reads a test summary line ("N failed", bun's "N fail") anywhere in the output, whatever the exit code (extends round 4 D1). evidence: the output held "1 failed, 1 passed in 0.07s".
2. [rule] A test run is its own Bash call, never inside a chain or a pipe. evidence: F-1e90a8e1 and this record — two in two days.
3. [tool] A trap entry that warns when a test command is followed by `;`, `&&`, `|` in one call. evidence: `guard/data/traps.yaml` already lints commands before they run.

## F-2cdebf3b — the reviewer found the guard-JSON checks incomplete; F-d0736dc7 — the new test then caught my own shape check

Whys:
1. Why were failures logged? The review showed `guard: []` crashing `gather` and incomplete payloads read as findings (F-2cdebf3b); after my fix, HH-29 failed once because a missing `answers` field read as `None`, which the check allowed (F-d0736dc7).
2. Why did the first fix still leak? The code checked the main list, then a subset of row fields; my rewrite checked every field's value but not that the key was present.
3. Why were the field checks partial both times? The spec described the payload as "the JSON shape of Round 7" in prose; neither the coder nor I had the fields and types in one place to check against.
4. Why prose? Round 7 was written as field names only (the same gap as F-b7c8635f, which this repeats).
Source: instruction — guard SPEC Round 7 and spec H5 give field names without types or presence.
Root cause: one cause with F-b7c8635f — a payload contract written as prose names, so each reader checked a different subset.
Options:
1. [check] HH-29 plants one payload per missing or mistyped field (11 shapes) — added, kills M10–M12. evidence: `mutants.txt`.
2. [tool] One table `GUARD_SHAPE` in the reader holds every field and its check, so the contract is read in one place — done in `harness_health.py`. evidence: the second leak (presence) was found by HH-29 within one run of writing it.
3. [rule] A spec for a JSON contract lists field, type, required — a table, never prose. evidence: H3 (a table) was implemented right; Round 7 (prose) twice not.

## F-0a1f3ca1 — the reviewer saw the guard's JSON lost through a bun pipe

Whys:
1. Why was a failure logged? The reviewer reproduced empty stdout from `process.stdout.write` then `process.exit` in a bun parent/child pair, and 41 guard tests failed in its run.
2. Why not fixed? Outside the Codex sandbox, 0 of 80 child runs lost output (5 bytes to 300 KB), and the guard suite passes 1187/1187; 38 of the reviewer's 41 failures are old CLI tests that pass here.
3. Why does the sandbox differ? Not established — the same open cause as F-76013d09 (Codex's bundled bubblewrap).
4. Why did it reach the review as a defect? The review brief did not ask the reviewer to separate sandbox effects from code effects.
Source: config — Codex's sandbox (as F-76013d09); and instruction — the review brief.
Root cause: an engine's sandbox changes pipe behaviour, and neither the test brief nor the review brief asks for a check outside it.
Options:
1. [config-advice] Install the system bubblewrap that Codex asks for, then rerun the reviewer's two-file reproduction under Codex. evidence: `nodes/tests-json.log` line 15; 0/80 outside.
2. [rule] A reviewer's or test writer's failure in a spawned process is rerun by the COO outside the engine's sandbox before it is fixed. evidence: this run did that twice, both times not reproduced.
3. [tool] Write `out()` with a synchronous write so the question cannot arise, if the reproduction under a fixed sandbox still loses output. evidence: the reviewer's own suggestion; not applied because not reproduced (Rule 2, nothing speculative).

## F-682702da — the exported skill bundle lacked R13's reference file

Whys:
1. Why was a failure logged? The reviewer found `skills/requirement-check/references/use-cases-and-requirements.md` missing from the bundle while the bundled SKILL.md names it.
2. Why missing? `tools/export_skills.py` copied only `SKILL.md` for single-file skills.
3. Why did the export test not catch it? It checked that the bundle matches a fresh export and that design_gate runs — not that a skill's named files are present.
4. Why was the export script not updated with the move? The main agent moved R13 into a new `references/` folder without checking how that skill is exported.
Source: tool — `tools/export_skills.py` (single-file skills copy one file) and its test.
Root cause: the export treated requirement-check as one file, and no test checked that a bundled skill's named references exist.
Options:
1. [tool] Export a single-file skill's `references/` too — done. evidence: `skills/requirement-check/references/use-cases-and-requirements.md` now in the bundle.
2. [check] The export test resolves every `references/<file>` a bundled SKILL.md names — added, shown failing on the old export for this file. evidence: `tests/test_skills_export.py`.
3. [rule] Moving text into a skill's new file checks the skill's export path in the same change. evidence: this miss.

## F-c055f734, F-e1161864 — my export test was too broad at first

Whys:
1. Why were failures logged? The new export check failed twice: once on purpose against the old export (F-c055f734), and once on the committed tree (F-e1161864) — on bootstrap's `references/executor-kinds.md`, not on R13.
2. Why on bootstrap? bootstrap names workflow-design's reference files; my check required every named reference to sit in the naming skill's own folder.
3. Why did the first run not show that? I read its failure with `grep "named but not exported"`, which matched the assertion's source line, not the message — I did not see which skill failed, and claimed "test failed first" in the commit message.
4. Why grep that way? To keep the output short; the same habit as F-969500fa — reading a test's result through a filter that can hide what it says.
Source: instruction — the main agent's way of reading test output (a filter that matched the source line), and the check's too-narrow rule.
Root cause: a fail-first run read through a filter that did not show the failing case, so a wrong check was taken as right.
Options:
1. [rule] A fail-first run is read in full (or by the `E ` message line), and the failing case is named in the log before the fix is applied. evidence: the second fail-first run, read by `^E `, named requirement-check correctly.
2. [check] The check accepts a reference found in any bundled skill — done, f64bd49. evidence: export test 2/2.
3. [tool] The guard's test-run record keeps the first failing assertion message, so the agent reads it from the record. evidence: `.harness-guard/evidence/F-e1161864.json` holds counts only.

## F-d8a49e5a — my R13 section added structure R13 does not have, and Limits cited a reported source

Whys:
1. Why was a failure logged? The reviewer found three things in text I wrote: "each requirement binds only once accepted" (R13.5 says suggested ones), "in this order" (R13 gives no order), and an older-summary sentence in Limits resting on a *reported* finding.
2. Why did I write them? I paraphrased R13 into a checklist instead of pointing at its lines, and summarised the research without re-reading each finding's label.
3. Why paraphrase? To make the section read as steps; the skill's own rule says "never add structure that was not given", and I did not run the section through the eight questions before committing.
4. Why not? The section was text in a skill, and I treated the check as one for requirements documents only.
Source: instruction — the requirement-check skill's "never add structure" rule was not applied to the skill's own new text.
Root cause: a paraphrase of a requirement written without running the skill's own check on it.
Options:
1. [rule] Text that restates a requirement quotes its id and its operative words, or points at the line; it never paraphrases. evidence: the three findings were all in paraphrased or summarised lines; the pointer lines had none.
2. [check] Before committing a restatement, diff its nouns and modal words against the source lines (suggested / every; order words). evidence: "suggested" → "each" was the change that widened the gate.
3. [rule] Criteria C9's "verified only" is checked by re-reading each cited finding's label at the time of writing. evidence: F4 was labelled reported in the findings table.
