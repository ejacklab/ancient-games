<!-- runs/20261014-code-map-build/insight.md -->
## F-60cad515 — read Linus's answer file after his run had failed

Whys:
1. `sed -n … experts-p3-strengthen/answers/linus.md` exited 2: the file did not exist.
2. It did not exist because Linus's run failed: Codex answered "You've hit your usage limit … try again at 3:16 AM" and exited 1 after 4 s.
3. I read the answer files without first gating on the run: `four_experts.py run` returns 1 when an asked expert is not ok (`four_experts.py:202`), but my command ended in `; tail …`, so the background task reported exit 0.
4. `status.json` records the failure as `problem: "empty answer"`, which hides the engine's own error line (the usage limit), so even the status read did not say why.
5. The four-experts skill orders run → check, but does not say to read nothing from `answers/` until `check` (or `status.json`'s `ok`) has passed for that expert.

Source: tool — `four_experts.py` reports an engine error (usage limit) as "empty answer"; and my command shape masked its exit code.
Root cause: `four_experts.py` collapses an engine's error output into "empty answer", and my `run …; tail` call discarded the run's non-zero exit.

Options:
1. [tool] In `four_experts.py`, when an engine exits non-zero with no answer, put the engine log's last `ERROR:` line in `status.json` `problem` (for example "usage limit until 3:16 AM"). evidence: experts-p3-strengthen/status.json linus `problem: "empty answer"`; experts-p3-strengthen/logs/linus.log shows "You've hit your usage limit".
2. [rule] Before reading any `answers/<id>.md`, read `status.json` and skip every expert whose `ok` is false; run the engine call with `set -o pipefail` or without a trailing `; tail` so its exit code survives. evidence: `four_experts.py:202` returns 1 when an expert fails; the task wrapper reported exit 0.
3. [check] Before a step that needs Codex, probe its quota with `codex exec -s read-only "Say OK." </dev/null` and stop on an `ERROR:` line. evidence: the probe at 2026-10-15T17:39Z returned the usage-limit error in under 5 s.


<!-- runs/20261015-learn-success/insight.md -->
## F-cf3f3a6e — the guard suite was red during the parallel build

Whys:
1. Why was the run red? 22 tests from rounds 1–4 asserted "a passing call writes no record", and one round-5 path test expected a child with no aim to fail.
2. Why did the old tests fail? Round 5 S1 makes a passing call write a `success` line, which those assertions forbid; the code worker followed the newer SPEC and was not allowed to change tests.
3. Why was that not settled before the parallel start? The COO's round-5 spec did not list which older assertions S1 contradicts, so the conflict surfaced only when the pieces met.
4. Why was the aim test red? The paths worker read "aim must name a measure" as applying only when an aim is present; the spec did not say a child must have one in so many words.
Source: instruction (the round-5 spec, the COO's)
Root cause: the spec for a parallel build named new behaviour but not the older assertions it overturns, nor one required field in plain words.
Options:
1. [rule] A spec that changes behaviour lists the older tests it contradicts, so the test writer updates them in the same round. evidence: the 22 assertions in test/hooks.test.ts, round3.test.ts, round4.test.ts, updated by the COO after the fact.
2. [check] Before a parallel start, run the old suite against a one-line stub of the new behaviour to see what it breaks. evidence: S1's stub (write a success line) would have shown the 22 at 14:51.
3. [tool] The guard's D1 should read bun's own summary ("23 fail"), which it missed — it logged "21 error" from other text. evidence: this record's actual field against the bun output of the same run.


<!-- runs/20261015-learn-success/insight.md -->
## F-1b6f6a0f — a lookup command ended with exit 2

Whys:
1. Why exit 2? The command's last part, `ls .claude/skills/workflow-design/guard/.harness-guard`, listed a folder that does not exist.
2. Why list it? The main agent checked whether the guard had written state inside its own package folder, which it never does — the journal lives at the git top-level.
3. Why that guess? The main agent did not use the guard's own `guardRoot` rule when it looked.
Source: instruction
Root cause: an exploratory check written without the guard's own location rule; harmless, but an errored call by R12.2.
Options:
1. [rule] Look for guard state at the git top-level only (`.harness-guard/` there). evidence: SPEC Common, guardRoot.
2. [tool] Add `cli.ts where` that prints the guard root and journal path for the current folder. evidence: this lookup.


<!-- runs/20261015-score/insight.md -->
## F-1e90a8e1 — a pipe hid a failed merge

Whys:
1. Why did the chain continue? `git merge … 2>&1 | tail -1 && …` — the pipeline's exit is tail's (0), so `&&` went on.
2. Why did the merge fail? An untracked copy of `runs/20261015-score/mutants.txt` in the main checkout would have been overwritten.
3. Why was there an untracked copy? The main agent writes run evidence in the main checkout and copies it into the worktree to commit, leaving the original behind.
4. Why was the pipe there? Habit: trimming long git output with `| tail` — the same "exit 0 is not success" trap the guard exists to catch, in the main agent's own commands.
Source: instruction (the main agent's command habit; no rule forbids piping a command whose exit matters)
Root cause: a command whose success gates the next step was piped, so its failure was invisible to `&&`.
Options:
1. [rule] Never pipe a command whose exit gates the next step; print its exit (`; echo "exit $?"`) or use `set -o pipefail`. evidence: this record; runs/20261015-score/merge-hidden.txt.
2. [check] A guard trap: `git merge|git push|git commit … | tail|head` followed by `&&` — the pipe hides the exit. evidence: the same shape here; E2's corpus can count how often it occurs.
3. [tool] Keep run evidence only in the worktree during a build and copy it to the main checkout after the merge, so no untracked twin can block it. evidence: the identical mutants.txt (cmp) that blocked the merge.


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


<!-- runs/20261015-ts-hybrid/insight.md -->
## F-f44538b2 — the runner was edited while it ran

Whys:
1. Why did the m5-code missing result go unseen? `run_node.sh` crashed with a bash syntax error after the engine call.
2. Why did it crash? The COO edited `run_node.sh` (adding the review branch) while a run was still executing it.
3. Why does editing break a running script? bash reads a script as it runs, so the running copy read half of the new text.
4. Why was it edited in place? The COO treated the runner as a config file, not as a program in use.
Source: instruction
Root cause: no rule against editing a script that a running process is executing.
Options:
1. [rule] Never edit a script while a background run uses it; write the new version to a new file and switch over between runs. evidence: tasks/b3jrjz8l0.output ("unexpected EOF").
2. [tool] Runner scripts copy themselves to a temp file and exec the copy, so an edit cannot reach a running instance. evidence: same.


<!-- runs/20261015-ts-hybrid/insight.md -->
## F-cf7d58f7 — opencode stopped without a result file

Whys:
1. Why was there no m5-code result? opencode's stdout ends after "Now the CLI:" — it wrote the files and stopped before running its checks or writing the result.
2. Why did it stop there? Not established: exit 0, no error text; the brief asked for the result last.
3. Why did nothing block the stop? The brief's result step was the last step, so a stop anywhere before it leaves no result.
Source: instruction
Root cause: the brief put the only progress record at the very end; a partial run left no trace of what it had checked.
Options:
1. [rule] Briefs ask for the result file to be written first as `status: partial` and updated at the end ("write it even if you stop early" was added for r3-code, which did report partial). evidence: `nodes/r3-code-1.result.md`.
2. [check] Treat "files changed but no result" as a failed node in `run_node.sh` and `dispatch.py`. evidence: this failure.


<!-- runs/20261016-four-experts-what-counts-as-change/insight.md -->
## F-e82a6f58 — I read a question.md that a research run never had

Whys:
1. Why was a failure logged? `head -60 runs/20261015-four-experts-speed/question.md` exited 1: no such file.
2. Why that path? I wanted a past experts question as a format example, picked the folder from the run list because its name has "four-experts" in it, and built the path as if every such folder held `question.md`.
3. Why would it not? Folders the four-experts runner makes are named `<date>-four-experts-<slug>` and always hold `question.md`; `20261015-four-experts-speed` is a research run (`DIGEST.md`, `research.md`) whose name has the same shape, so the name does not say which kind a folder is.
4. Why did the listing not stop the read? I put `ls <folder>` and `head <file>` in one command, so the listing that would have shown no `question.md` came back with the error, not before it.
Source: instruction — how I build a path to read: from a folder-name pattern, read in the same command that lists the folder.
Root cause: a path inferred from a naming pattern two kinds of runs share, read before the listing that would have disproved it was seen.
Options:
1. [rule] Read only a path a listing or glob has returned; when the listing and the read share one command, glob for the file itself (`ls runs/*/question.md`). evidence: `ls runs/20261015-four-experts-speed/` shows `DIGEST.md` and `research.md` only.
2. [tool] The runner's own file marks an experts run (it writes `status.json` with each expert's start and finish, per the four-experts skill), so "is this an experts run" is a file test, not a name guess. evidence: the four-experts SKILL.md, section 1, "`status.json` records each expert's start and finish time".


<!-- runs/20261016-four-experts-what-counts-as-change/insight.md -->
## F-2cc835e3 — criterion C2 not met: Linus had no quota, and the check failed

Whys:
1. Why was a failure logged? C2 ("all five answered … check passes") was marked not met: Linus has no answer, and `check.txt` reports 3 failures.
2. Why no answer from Linus? Codex exited 1 after 8 s with "You've hit your usage limit … try again at 2:37 PM" (`logs/linus.log`).
3. Why was the limit found only by the run? The runner starts all four engines at once and checks none of them first; I started it without checking either.
4. Why is there no check first? The four-experts runner has no readiness step. The option to add one, "a runner path is canary-proved (one cheap call) before a run depends on it", was raised in `runs/20261016-time-monitor/insight.md` (F-173e0190, option 3) and not applied.
5. Why the other two check failures? 孫子 wrote a quote from his list in traditional characters (趙…晉國歸焉) where the list has simplified (赵…晋国归焉, `seats/sun-tzu-list.md:301`). That is the same cause as F-84636a96 in the time-monitor run (an engine changing a character's form), whose options were not applied either, so it repeated.
Source: tool — `.claude/skills/four-experts/scripts/four_experts.py` starts every engine with no readiness check, and the experts' brief still lets an engine change a quote's script.
Root cause: an engine out of quota, found only by the run itself, because the runner has no canary step; plus a repeat of the script-variant failure whose fix was never chosen.
Options:
1. [tool] The runner makes one tiny call per engine before the run and reports any quota or login error with the time it resets, before the other experts start. evidence: `logs/linus.log` shows the error after 8 s, so a canary costs seconds; F-173e0190 option 3 proposed the same.
2. [rule] When an expert's engine is out of quota, the run says so and offers the rerun (`--only linus --out <run>` after the reset), never a silent substitute engine. evidence: the four-experts SKILL.md has a fallback only for 范蠡; `status.json` records Linus as exit 1, "empty answer".
3. [rule] The experts' brief says to copy Chinese quotes character by character, in the list's own script (simplified or traditional), and not to convert between them. evidence: this repeat, and F-84636a96 option 1 in `runs/20261016-time-monitor/insight.md`.


<!-- runs/20261016-four-experts-what-counts-as-change/insight.md -->
## F-4981093a — a read of a file that was never written, an hour after the rule against it

Whys:
1. Why was a failure logged? `grep -c "^## " linus.md` in `trial-mcode/retry/` exited 2: no such file.
2. Why was the file missing? It was the `-o` output of the repeat mcode call, and that call failed (exit 4, provider timeout), so mcode never wrote it.
3. Why read it without knowing it existed? I put `cat <task output>` and the reads of the answer file in one command. The output that said "exit 4" came back together with the error, not before it, which is F-e82a6f58's pattern exactly.
4. Why did the rule written for F-e82a6f58 not stop it? The rule is in memory ("read only a path a listing or glob has returned"), and memory is read at session start as background. Nothing checks a read at the moment it is written, so a habit in one long session outran it within an hour.
Source: instruction — the read-only-listed-paths memory rule, which has no check at the moment of the read; plus my habit of chaining a status read with the reads that depend on it.
Root cause: a rule held only in memory, with no check where the read happens; the dependent read was chained after the status that would have decided it.
Options:
1. [rule] Read a command's status first and read its outputs in a later call, only when the status says they were written; never chain the two. evidence: both failures (F-e82a6f58, F-4981093a) put the deciding read and the dependent read in one command.
2. [check] The guard's PreToolUse lint warns on a read (`head`, `cat`, `grep`, `sed -n`) of a path that does not exist when the command runs, before it runs. evidence: the guard already lints every Bash command before it runs (`src/traps.ts` `lintCommand`); both missing paths were knowable then.
3. [tool] Wrap engine calls so they always write the answer file, empty with the exit code noted when the call fails, so a follow-up read never hits a missing file. evidence: `four_experts.py` `answer_ok` already treats an empty answer as a failure.


<!-- runs/20261016-four-experts-what-counts-as-change/insight.md -->
## F-e69dfb66 — criterion C4 not met: mcode gave Linus no answer on a brief-sized input

Whys:
1. Why was a failure logged? C4 ("a real Linus answer from mcode … passes the experts' check") was marked not met: every brief-sized mcode run exited 4 with no answer.
2. Why no answer? mcode reported "LLM request timed out: no response from the provider" on the 67 KB pasted brief (twice), on the 44 KB sections-only brief, and in standard mode reading the files itself. A 9 KB brief answered in 20 s.
3. Why is it mcode and not the model? opencode answered the same brief on the same model (MiniMax-M3.1-Flash-Preview) in 181 s at the same time. What differs is mcode's connection: it signs in through `minimax_oauth`, while opencode uses the `minimax-coding-plan` provider.
4. Why was this found only in a full run? The engine was proved with a canary of a few lines, and an expert's brief is 40–70 KB. The canary proved the call shape but not the input size the run needs.
Source: tool — mcode's `minimax_oauth` connection, which does not answer brief-sized requests within its first-event limit; and my canary, which did not use a brief-sized input.
Root cause: an engine proved only with a tiny canary, used for inputs 5–7 times the size it was shown to handle.
Options:
1. [config-advice] EJ gives mcode an API key (`mcode provider set-minimax-key`) so it uses `minimax_api` instead of the OAuth login, then the try-out is rerun. evidence: `mcode provider list` shows `minimax_api` enabled with no key; the stall is on the OAuth path only (opencode answered).
2. [rule] An engine's canary uses an input the size of the real brief before a run depends on it. evidence: the 9 KB canary passed in 20 s, and every input of 44 KB or more failed.
3. [tool] Keep Linus on opencode, with the six-experts runner's wait for a busy opencode, until mcode passes a brief-sized canary. evidence: opencode answered this brief in 181 s and 220 s; the wait is `opencode_busy()` on the six-experts branch.


<!-- runs/20261016-four-experts-what-counts-as-change/insight.md -->
## F-485505f6 — criterion C5 not met: the mcode change was not committed

Whys:
1. Why was a failure logged? C5 ("… committed and pushed alone") was marked not met.
2. Why not committed? Committing a fallback that leaves Linus with no answer would make every run in which Codex is low worse than today's opencode fallback.
3. Why does that follow from C4? The change works mechanically (routing, read-only, stdin; 10 tests, 5 of 5 mutants, 1093 suite) but the engine it routes to does not answer real briefs (F-e69dfb66).
4. Why was it saved and reverted instead of left in place? Another session was about to merge a rename of the same files into this working tree, and uncommitted edits there would have blocked it. The change is kept as a patch that re-applies cleanly.
Source: tool — mcode's connection (the same cause as F-e69dfb66); not committing was the decision that cause forced.
Root cause: F-e69dfb66's — the target engine does not answer brief-sized inputs, so the change cannot land yet.
Options:
1. [tool] Re-apply `trial-mcode/linus-mcode.patch` onto the renamed six-experts runner once mcode passes a brief-sized canary (F-e69dfb66 option 1 or 2). evidence: `git apply --check` passed on the patch before the rename; the rename moves the file to `six_experts.py`, so the patch's paths need updating.
2. [rule] Drop the mcode change and record opencode with the wait as Linus's fallback. evidence: opencode answered the brief in 181 s and 220 s, and the wait already exists on the six-experts branch.


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


<!-- runs/20261016-six-experts/insight.md -->
## F-5c21dd69 — my new insight-index.ts did not typecheck

Whys:
1. Why was a failure logged? `tsgo --noEmit` exited 2: `heading.match(ID_RE) ?? []` is typed `RegExpMatchArray | never[]`, and `includes(id)` on it rejected a string.
2. Why did I write it that way? I copied the pattern from `insight.ts`, where the same expression is assigned to a variable already typed `string[]`.
3. Why did the copy lose the type? In the new code the result went into a `const` with no annotation, so TypeScript inferred the union.
4. Why was it caught only at the type check? I wrote the module in one go and ran tsgo after, as the build pattern says — the check did its job.
Source: tool — TypeScript's inference of `?? []` as `never[]`; caught by the type check, as designed.
Root cause: a copied expression lost its declared type, so the empty-array fallback was inferred as never[].
Options:
1. [rule] An empty-array fallback is always written with its type (`const ids: string[] = x ?? []`). evidence: the fix was that one annotation.
2. [check] Keep running tsgo before any test, as now; it caught this in one step. evidence: `tsgo` exit 2, then clean after the fix.


<!-- runs/20261016-six-experts/insight.md -->
## F-b696193d — I changed start()'s signature and broke the other session's quota tests

Whys:
1. Why was a failure logged? The Python suite failed 4 tests in `tests/test_six_experts_codex_quota.py`: `fake_start() takes 8 positional arguments but 9 were given`.
2. Why? I added a 9th parameter (`model`) to `start()` and passed it positionally on every call, including Linus's.
3. Why did that reach the tests? The quota tests replace `start` with an 8-argument fake; I had run them before the change (8/8) and not after.
4. Why not after? I ran only the new runner tests and the guard suite after the Dave/Dario edit, not every test that patches `start`.
Source: instruction — the main agent's habit of running only the tests it just wrote after changing a shared function's signature.
Category: own-work
Root cause: a shared function's signature changed without running every test that replaces it.
Options:
1. [rule] After changing a function's signature, grep the tests for the name (`start`, `fake_start`) and run those before anything else. evidence: one grep finds `tests/test_six_experts_codex_quota.py`.
2. [tool] Pass optional parameters by keyword and only when set (`**seat_model(...)`), so existing callers and fakes keep their shape — done. evidence: 31/31 after the change.
3. [check] The runner's tests include one that calls `start` through a strict 8-argument fake, so a widened signature fails there first. evidence: the quota tests did exactly that, by accident.


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


<!-- runs/20261016-time-monitor/insight.md -->
## F-a03fa5b3 — I typed the deadline's epoch from memory, a year off

Whys:
1. Why was a failure logged? `deadline start --minutes $left` got −525542: the end time I used, 1760584921, is 2025-10-16 11:22, not 2026.
2. Why that number? I wrote the epoch into the command from my own reckoning instead of computing it from the start time I had saved (`$CLAUDE_JOB_DIR/tmp/run-start`).
3. Why did I reckon it? Converting a wall-clock time to an epoch looked trivial, so I treated it as known rather than measured — recall standing in for data, the same thing this run's rule forbids for decisions.
4. Why did it get as far as the guard? Nothing between me and the command checks a time I type; the guard's own validation (minutes must be positive) was the first check, and it held.
Source: instruction — the main agent's way of producing a time value (typed, not computed); the guard's validation was the check that caught it.
Root cause: a time value typed from recall instead of derived from a recorded start; it was caught only because `deadline start` rejects non-positive minutes.
Options:
1. [tool] `deadline start` also takes `--until HH:MM` (local), so a deadline is given as the wall-clock time the owner said, with no arithmetic by the agent. evidence: the second call, computed from the saved start, worked.
2. [rule] A time or a number the agent did not read from a file or a command is not typed into a command; it is computed in the same command from a recorded source. evidence: `date -d @$((start+3600))` gave the right end in one step.
3. [check] Keep the guard's positive-minutes check (it caught this) and add an upper bound warning when minutes exceed a day. evidence: −525542 would also have been flagged by any magnitude check.

