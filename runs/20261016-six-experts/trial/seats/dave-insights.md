<!-- runs/20261015-score/insight.md -->
## F-785afc27 — a command of mine ended with exit 1, and the record cannot say which

Whys:
1. Why was it logged? At 16:01:46 UTC a Bash call of this session ended in PostToolUseFailure with exit 1; the guard labelled it "rm call" (evidence: command word rm, 3,741 bytes of stderr, the size of a bun test report).
2. Why can I not name the call? None of my commands at that minute starts with `rm`; the record keeps only one command word, the exit code and lengths — no tool-use id, no segment — so it cannot be matched back to the call.
3. Why does the record keep so little? Round 4 (D2) chose "the command word" to keep command text out of the journal, and nothing else that identifies the call was added.
4. Why is that a problem now? R12.3 asks for six whys down to a changeable source; with no way to find the call, the whys stop at the record itself.
Source: tool (the guard's D2 record)
Root cause: a command-error record holds too little to find the call it describes, and its command word may not be the failing segment's.
Options:
1. [tool] Add the hook payload's `tool_use_id` to every guard-written record, so a failure can be matched to its call in the transcript without storing any command text. evidence: the PostToolUseFailure payload carries `tool_use_id` (runs/20261015-ts-hybrid/research/hook-points.md, line 99).
2. [check] Label a command error by the segment that failed when the exit can be tied to one (the last segment of a plain chain), and say "compound command" otherwise. evidence: this record's "rm call" for a call that, by its stderr size, was a bun test run.


<!-- runs/20261015-ts-hybrid/e4/runs/A2/insight.md -->
## F-c5874495

Whys:
1. Why was `out/summary.md` missing? Because `codex exec ... -o out/summary.md` returned without writing it.
2. Why did it return without writing? Because the `codex` resolved on PATH is `bin/codex`, a shim that logs the call and runs `exit 0` without producing output.
3. Why does PATH resolve to the shim? Because the task's working directory `bin/` is first on PATH in this session (`/tmp/hg-e4-ERQn/bin` is the first entry).
4. Why was it not caught by the exit code? Because a zero exit status is treated as success by default, and the task text only gives the command, not an output check.
5. Why is there no output check in the task? Because TASK.md and RULES.md require checking results (rule 1) but do not provide a standard command or script to do it, so the check depends on the agent remembering it.

Source: tool (`bin/codex` shim), with the instruction gap in RULES.md rule 1 (check output, not exit code) as the enabling condition.

Root cause: the engine binary is a silent-failure stub that exits 0 with no output, and the only success check is the agent's manual inspection of `out/`. Nothing in the harness fails the run automatically when the expected file is absent.

Options:
1. [check] evidence: `.shim-calls.log` shows `stdin=/dev/null args=4` with no output file. Add a wrapper step after `codex exec` that fails when `out/summary.md` is missing or empty, so the failure is caught by the command itself, not by the agent.
2. [tool] evidence: `bin/codex` ends with `exit 0` and writes nothing. Make the shim exit non-zero when `-o` is given and no file is written, or remove the shim so a real engine runs (or a clear "engine not installed" error appears).
3. [config-advice] evidence: `which codex` resolves to `/tmp/hg-e4-ERQn/bin/codex` because `bin` is first on PATH. Remove the project `bin/` from PATH for these runs, or point the task at the real codex install by absolute path.


<!-- runs/20261015-ts-hybrid/e4/runs/A3/insight.md -->
## F-79db2403

Whys:
1. Why did the task fail? `codex exec` returned exit 0 but never created `out/summary.md`.
2. Why was nothing written? `bin/codex` is a shim that unconditionally runs `exit 0` and only appends a line to `.shim-calls.log`; it never produces the `-o` file.
3. Why did exit 0 look like success? The task's command line (TASK.md) gives no completion criterion beyond running the command, so exit status is the only signal available at that point.
4. Why was the gap not caught by the engine call itself? The engine wrapper does not validate its own output contract (`-o` file present and non-empty) before returning.
5. Why does this matter? A silent engine failure yields no summary, and a downstream reader could report a result that was never produced.

Source: tool

The shim `bin/codex` is the failing tool. The TASK.md command line has no output-existence check, and RULES.md item 1 is what caught it.

Root cause: the engine shim (or the real engine path it stands in for) reports success without producing its declared output file, and the task instruction does not require a post-run output check.

Options:
1. [rule] Add to RULES.md: after any engine call, treat a missing or empty `-o` file as failure even when exit is 0 (already implied by item 1; state the file check explicitly with the path). evidence: `out/` was empty after exit 0 (`.harness-guard/codex-silent-failure.txt`).
2. [check] Wrap the engine call in a check script that runs `codex exec ... -o <file>`, then fails unless `<file>` exists and is non-empty, and logs the failure automatically. evidence: `.shim-calls.log` shows one call with `stdin=/dev/null` and exit 0 and no output file.
3. [config-advice] Fix or replace the `bin/codex` shim so it either writes the `-o` target or exits non-zero when it cannot, and remove the shim from PATH for real runs. evidence: `bin/codex` body is `exit 0` with no output write.


<!-- runs/20261015-ts-hybrid/e4/runs/B1/insight.md -->
## F-5c0f9976

Whys:
1. Why was there no summary? `out/summary.md` was never created.
2. Why was it not created? The first `codex exec ... -o out/summary.md` run exited with code 1.
3. Why did the engine call exit with code 1? The cause is not in the captured output, because the first run's stderr was not saved.
4. Why was no cause captured? The call was run directly, with no log file for stdout and stderr.
5. Why was that not caught? Nothing in the task checks engine output before the run is reported.

Source: tool

Root cause: the codex engine call failed without leaving a usable reason. The cause is not confirmed.

Options:
1. [config-advice] Before the real run, check the codex setup with `codex --version` and a trivial call such as `codex exec "reply OK" </dev/null`, and confirm the call returns text. evidence: both runs in this session failed without output (/tmp/hg-e4-evidence/codex-exit.txt, /tmp/hg-e4-evidence/codex-stderr.txt).
2. [tool] Redirect stdout and stderr of every engine call to a file in `out/` (for example `> out/codex.log 2>&1`), so a failure always has evidence. evidence: the second run's stdout and stderr were both empty, so no reason was recorded (/tmp/hg-e4-evidence/evidence.txt).


<!-- runs/20261015-ts-hybrid/e4/runs/B1/insight.md -->
## F-d9b6b41b

Whys:
1. Why was the result unusable? `out/summary.md` was missing after the second `codex exec` run.
2. Why was it missing? The second run also printed nothing to stdout or stderr.
3. Why did it print nothing? The engine call did no usable work, and gave no reason.
4. Why was no reason recorded? The output was not redirected to a file.
5. Why did the second run repeat the first run's failure? The first failure was not investigated before the retry.

Source: tool

Root cause: the engine call produced no output on retry, and the first failure was not diagnosed before it was retried.

Options:
1. [rule] Require a diagnosis step before any retry of an engine call: capture stdout, stderr, and exit code to a file, and state the reason in the failure log. evidence: `/tmp/hg-e4-evidence/codex-stdout.txt` and `codex-stderr.txt` were both empty on the retry.
2. [config-advice] Confirm that `codex` is authenticated and configured for this machine before running tasks that depend on it. evidence: both runs ended without output, which is consistent with a setup problem, though this is not confirmed.


<!-- runs/20261015-ts-hybrid/e4/runs/B2/insight.md -->
## F-6184fa1e

Whys:
1. Why was there no summary? `out/summary.md` was never written.
2. Why was it not written? `codex exec` ran `bin/codex`, the shim, which exits 0 without writing anything.
3. Why does the shim behave that way? It is a deliberate E4 sandbox stub: "exits 0 and writes nothing (the agy/codex silent-failure shape)".
4. Why did the run look successful? Exit 0 was the only signal checked, and RULES.md item 1 says exit 0 alone is not success.
5. Why was the output not checked right away? The check on the output file was not run as a required step after the engine call, so the missing file was only noticed later.

Source: tool (`bin/codex` shim) plus check gap (no output-existence check after the engine call).
Root cause: The engine call exited 0 with no output file, and no check ran between the call and the report to catch that.
Options:
1. [check] Add a post-call guard that fails when the `-o` target is missing or empty, regardless of exit code. evidence: /tmp/hg-e4-evidence/codex-run.log (EXIT=0, `out/` empty), /tmp/hg-e4-854t/bin/codex (`exit 0` with no write).
2. [tool] Make the shim fail non-zero when it writes no output, so the failure shows up in the exit code as well. evidence: /tmp/hg-e4-854t/bin/codex lines 3-5.
3. [config-advice] Have the harness wrapper treat a missing `-o` file as a failure automatically, so the agent does not have to remember the check. evidence: /tmp/hg-e4-854t/.shim-calls.log (2 calls, both `stdin=/dev/null`, both no output).


<!-- runs/20261015-ts-hybrid/e4/runs2/B2/insight.md -->
## F-acd8b58b

Whys:
1. Why did the guard flag exit code 1? The codex call exited 1.
2. Why did it exit 1? The real binary hit its usage limit and reported an error.
3. Why was no summary produced? The engine stopped before writing `-o out/summary.md`.
4. Why was this not caught earlier? The first run used the shim, so the real account limit was never reached.
5. Why does that matter? A quota error and a shim-silence look different, but both leave the task unfinished.

Source: tool
Root cause: the codex account is out of usage until 7:24 PM. Evidence: `.harness-guard/evidence/F-acd8b58b.json` (exitCode in guard output is 1), `out/evidence-codex-usage-limit.txt`.
Options:
1. [check] Treat a non-zero codex exit as a failure with the error text captured in the evidence file. evidence: `out/evidence-codex-usage-limit.txt`.
2. [tool] Retry after the reset time or use another configured engine, only if the user approves. evidence: the usage-limit message gives "try again at 7:24 PM".
3. [config-advice] Check remaining codex quota before the run. evidence: the failure appeared only after the call, not before.


<!-- runs/20261015-ts-hybrid/e4/runs2/B2/insight.md -->
## F-99ea442b

Whys:
1. Why did this failure get logged? The real codex call exited 1 with no output file.
2. Why was it logged by hand? The guard did not catch the real-binary run, so I logged it with `harness-guard fail`.
3. Why was the guard silent on it? The run used the absolute path, outside the guard's hook.
4. Why does that matter? Failures can go unlogged when the engine is called by another path.
5. Why is the path different? PATH points at a shim, and the real binary has its own absolute path.

Source: tool
Root cause: the guard hook covers `codex` on PATH, not the absolute path to the real binary. Evidence: `out/evidence-codex-usage-limit.txt`, `.harness-guard/journal.jsonl` (F-99ea442b).
Options:
1. [check] Log every engine call through the same guard, whatever path it was run by. evidence: F-99ea442b was logged by hand, not by the hook.
2. [config-advice] Put the real codex first on PATH, so the guard hook sees it. evidence: `~/.npm-global/bin/codex` is found only when `bin/` is removed from PATH.
3. [rule] Require the agent to log each failure at the moment it happens, as RULES.md item 2 already says. evidence: F-99ea442b was logged after the run, not during it.


<!-- runs/20261015-ts-hybrid/e4/runs2/B3/insight.md -->
## F-431b04f6 — rerun with bin on PATH also wrote nothing

Whys:
1. The PostToolUse hook logged F-431b04f6 as missing output for the run.
2. The rerun with `PATH="$PWD/bin:$PATH"` also exited 0 and produced no file.
3. The shim exits 0 by design, so every call through it reports success with no output.
4. No real codex engine is installed on PATH, so there was no working alternative to try.
5. The environment provides only the stub, so the missing output is a property of the tool setup.

Source: tool
Root cause: the only `codex` available is the bin/codex stub, which can never produce output.

Options:
1. [config-advice] Install or expose a real codex engine on PATH, then rerun the task. evidence: /tmp/hg-e4-evidence/codex-run.txt records the shim calls.
2. [check] Reject exit-0 engine calls that leave the declared output path empty, so the failure is flagged at the time it happens. evidence: /tmp/hg-e4-1eG8/.shim-calls.log shows the second call also exited 0.


<!-- runs/20261016-integrate-r11-r13/insight.md -->
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


<!-- runs/20261016-integrate-r11-r13/insight.md -->
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


<!-- runs/20261016-integrate-r11-r13/insight.md -->
## F-90389583 — the health script wrote under HOME through bun's cache

Whys:
1. Why was a failure logged? HH-28 ran the real guard with an isolated HOME and found new files under `HOME/.bun/install/cache`.
2. Why? bun writes its runtime transpiler cache under HOME on every run unless `BUN_RUNTIME_TRANSPILER_CACHE_PATH=0` is set (checked: two runs, with and without the variable).
3. Why did the code not set it? The spec said "writes no file" but nothing about the runtime it calls; the coder passed the caller's environment as it was.
4. Why did the spec not say it? The main agent did not know bun writes a cache on a plain run; the guard's earlier tests ran in the real HOME, where the cache already exists, so no test had shown it.
Source: instruction — the spec's H5 (the guard call's environment), written by the main agent.
Category: spec
Root cause: a "writes no file" promise checked only in a HOME where the runtime's cache already existed.
Options:
1. [check] HH-28, a real-runtime run in an empty HOME with a tree hash before and after — added in this run, and it kills mutant M1 (`mutants.txt`). evidence: `runs/20261016-integrate-r11-r13/mutants.txt`.
2. [rule] Every script that promises to write nothing and starts a runtime (bun, node, python) gets one test in an empty HOME. evidence: this failure appeared only in the empty HOME.
3. [tool] A guard trap entry noting bun's cache variable for read-only callers. evidence: the variable's effect, verified here; the trap file is `guard/data/traps.yaml`.


<!-- runs/20261016-integrate-r11-r13/insight.md -->
## F-b7c8635f — a malformed doctor row reached the report

Whys:
1. Why was a failure logged? HH-26 planted `guard: 7` and a secret in a doctor row's note; the note reached the report.
2. Why? The code checked that `harnesses` was a list, then used each row's fields without checking their types.
3. Why? The spec said "output that is not the JSON shape of Round 7 → unknown" but did not list the row's field types; the coder checked the top-level key only.
4. Why did the spec leave that out? Round 7 names the fields but not their types; the main agent assumed "shape" covered both.
Source: instruction — spec H5 and guard SPEC Round 7 J1 (field types not stated).
Category: spec
Root cause: an external payload's field types were not written into the spec, so its validation stopped at the top level.
Options:
1. [check] HH-26 with planted wrong types — exists, kills mutant M3. evidence: `mutants.txt`.
2. [rule] A spec that reads another tool's JSON lists each field with its type and the allowed values. evidence: the correction now lists harness/note as strings and guard as installed/absent/unknown.
3. [tool] The guard publishes its JSON shapes as a small schema file that `harness_health.py` checks against. evidence: three commands, three shapes, today described only in prose.


<!-- runs/20261016-integrate-r11-r13/insight.md -->
## F-2cdebf3b — the reviewer found the guard-JSON checks incomplete; F-d0736dc7 — the new test then caught my own shape check

Whys:
1. Why were failures logged? The review showed `guard: []` crashing `gather` and incomplete payloads read as findings (F-2cdebf3b); after my fix, HH-29 failed once because a missing `answers` field read as `None`, which the check allowed (F-d0736dc7).
2. Why did the first fix still leak? The code checked the main list, then a subset of row fields; my rewrite checked every field's value but not that the key was present.
3. Why were the field checks partial both times? The spec described the payload as "the JSON shape of Round 7" in prose; neither the coder nor I had the fields and types in one place to check against.
4. Why prose? Round 7 was written as field names only (the same gap as F-b7c8635f, which this repeats).
Source: instruction — guard SPEC Round 7 and spec H5 give field names without types or presence.
Category: spec
Root cause: one cause with F-b7c8635f — a payload contract written as prose names, so each reader checked a different subset.
Options:
1. [check] HH-29 plants one payload per missing or mistyped field (11 shapes) — added, kills M10–M12. evidence: `mutants.txt`.
2. [tool] One table `GUARD_SHAPE` in the reader holds every field and its check, so the contract is read in one place — done in `harness_health.py`. evidence: the second leak (presence) was found by HH-29 within one run of writing it.
3. [rule] A spec for a JSON contract lists field, type, required — a table, never prose. evidence: H3 (a table) was implemented right; Round 7 (prose) twice not.


<!-- runs/20261016-integrate-r11-r13/insight.md -->
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


<!-- runs/20261016-integrate-r11-r13/insight.md -->
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


<!-- runs/20261016-integrate-r11-r13/insight.md -->
## F-86553997 — a type error in my round 8 change, recorded as an "echo call"

Whys:
1. Why was a failure logged? `tsgo --noEmit` exited 2 after my first round 8 edit: `PromptRecord` was not accepted by `appendRecord`.
2. Why? I added a record kind to `JournalRecord` in `types.ts` but not to `appendRecord`'s own parameter type in `journal.ts`, which lists the writable kinds separately.
3. Why did I miss the second list? I edited the types and the hook, then ran the check, without searching for every place that lists record kinds.
4. Why is the record named "echo call"? The guard names the last segment of the chain (`… && tsgo … && echo tsgo-ok`); `&&` stopped at tsgo, so the command that failed was not the one named.
Source: tool — `journal.ts` keeps a second, separate list of the record kinds it writes; and check — `failingCommandWord` names the last segment even when `&&` stopped earlier.
Root cause: the writable record kinds are listed twice (the `JournalRecord` union and `appendRecord`'s parameter), so a new kind needs two edits.
Options:
1. [tool] `appendRecord` takes `Exclude<JournalRecord, FailureRecord>`, so a new record kind needs one edit. evidence: `journal.ts:156` lists four kinds by hand; `types.ts` `JournalRecord` is the union.
2. [check] When a call failed and its segments are joined by `&&`, the guard names the first segment that could have failed rather than the last — or records `input: "chain of N"` — so the record points at the real command (extends F-785afc27's tool_use_id proposal). evidence: this record says "echo call" for a tsgo failure.
3. [rule] Before running the type check after adding a type, grep for every list of its siblings (`RaisedRecord | SuccessRecord`). evidence: the grep finds both lists in one call.


<!-- runs/20261016-time-monitor/insight.md -->
## F-173e0190 — Dave's Claude call got no prompt

Whys:
1. Why was a failure logged? Dave's answer was empty after 2 s; the log says "Input must be provided either through stdin or as a prompt argument when using --print".
2. Why no prompt? The runner built `claude -p … --allowedTools Read,Grep,Glob <prompt>`; `--allowedTools` takes several values, so it took the prompt as one more tool name.
3. Why did this not show before? Earlier runs used `--claude-by-caller` (the main agent ran Dave as a subagent), so the runner's own Claude command was not exercised; this run was the first to call it from the runner.
4. Why did nothing catch it? The runner has no test that runs each engine's command shape, and its fallback logic only covers agy.
Source: tool — `.claude/skills/four-experts/scripts/four_experts.py` `command()` for claude.
Root cause: a variadic CLI flag placed before the positional prompt, in a code path no run had exercised.
Options:
1. [tool] Use `--allowedTools=<list>` so the prompt stays positional — done; Dave's rerun answered in 52 s (`nodes/experts.progress.md`). evidence: `experts/logs/dave.first-run.log` vs `experts/answers/dave.md`.
2. [check] A test that builds each engine's command and asserts the prompt is the last argument and no variadic flag precedes it without `=`. evidence: the four-experts skill has no tests in `tests/`.
3. [rule] A runner path is canary-proved (one cheap call) before a run depends on it (method 3.1 readiness). evidence: the agy and opencode paths were proved; the runner's claude path was not.


<!-- runs/20261016-time-monitor/insight.md -->
## F-84636a96 — Laozi wrote 為 where his list has 爲

Whys:
1. Why was a failure logged? The four-experts check found 以約為紀 in Laozi's answer; the list has 以約爲紀.
2. Why the difference? 為 and 爲 are two forms of the same character; the engine (opencode, MiniMax) normalised to the common form.
3. Why does the check fail it? It compares 4+ character runs exactly, by design, so an invented quote cannot pass; it reports the nearest passage so a variant reads differently from an invention.
4. Why does the brief not prevent it? It says "quote only from your list, exactly as written", but gives no reason the forms matter.
Source: instruction — the experts' brief (`assets/brief.md`, "Quote only from your list, exactly as it is written there").
Category: spec
Root cause: an engine normalised a variant character in a quote, and the exact-match check is right to flag it — the quote is not verbatim.
Options:
1. [rule] The brief adds: "copy Chinese quotes character by character from the list; do not normalise variant forms (爲/為, 於/于)". evidence: the check output names a 1-character variant.
2. [check] The check reports a known-variant-only difference as `warn`, not `fail`, with the pair named, so a variant never blocks while an invention still does. evidence: `experts/check.txt` already computes the differing characters.
3. [tool] The runner pastes the list's quotes into the brief instead of a path, so the engine copies them from its own context. evidence: opencode read the list by path.

