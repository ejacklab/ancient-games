# Dave: what a pre-flight check on a brief should verify

## Answer
Build the check as an extension of the guard's existing trap catalogue (`guard/data/traps.yaml`). It should read the file that the prompt names ("Read <file> and do what it says") and fail on three things, in this order:

1. **Can't write:** the call expects a result file, but the engine's mode cannot write one.
2. **Outside the repo:** the file names an existing file outside the repo, and the file is going to opencode.
3. **Too big:** the file plus the files it names is larger than anything the engine has passed before. This only matters for an engine with a recorded size failure, which today is only mcode.

Each rule starts as `proposed` and becomes `approved` only after a replay over the briefs already in `runs/`, comparing how often it fires on calls that failed against calls that worked. The check should not look at prose, placeholders, text that is the same on every call, quota, or properties of the answer. If the check can see only the file and not the engine command, rules 1 and 3 can't run. Then I would build rule 2 alone, for file paths only, after the replay.

## How I decided

1. **What would change my mind (my #1).** A rule that fires on good calls about as often as on bad ones blocks work and buys nothing. So the measure for each candidate is how often it fires on known-failed calls compared with calls whose status was `ok`. Every trap already carries a `withdraw_when` line, so this condition has somewhere to live.

2. **Use the data we already have first (my #5).** We have:
   - 396 brief files under `runs/**/briefs/`
   - 64 expert runs, each with a `status.json` and engine logs
   - the insight files
   - the guard's trap catalogue. It already has an approved `opencode-outside-repo` trap (`traps.yaml:26-35`) and engine recognition (`SPEC.md:55-62`).

   What the data does not show: `ok` only means the answer had its five sections. It does not mean the engine read every file it was pointed at.

3. **What the existing trap misses (my #5, applied to `SPEC.md:72-74`).** It checks the command line, and the command line names only the brief, which is inside the repo. The problem in runs/20261016-six-experts/insight.md#F-7f938bdf was inside the brief: `~/.claude/plans/…`. It also counts only words that start with `/`, so a `~/` path would pass even on a command line. There is a second blind spot: `six_experts.py` starts its engines itself (`six_experts.py:148`), so the guard's hook never sees those inner calls. This changed where the check lives: as part of the guard, called by the runner before each engine starts, the same way the runner already calls `bun cli.ts insight` (`six_experts.py:163`).

4. **A small test instead of an argument (my #2).** I ran read-only greps over the history. I wrote these greps myself, so they are not independent evidence.

   **Outside-repo paths (`~/`, `/tmp/`, other home folders):**
   - They appear in 51 of 396 brief files.
   - In 7 expert runs the question named such a path. In one, six-experts/experts-q1q2, both opencode seats were auto-rejected. In six, opencode answered: ts-hybrid/experts-spots, four-experts-what-counts-as-change, sot-must-should, its round2, harness-health/experts, and sot-yaml-review/experts. One more run named such a path, but its opencode failure had another cause (see the size bullet).
   - Counting only paths that name a file: 1 failed run (q1q2) against 2 that worked (harness-health/experts and ts-hybrid/experts-spots, both naming `~/.claude/settings.json`).
   - Three worker briefs also name outside-repo files. I did not check their engines or outcomes.
   - Only 1 of the 64 expert runs has an "auto-rejecting" line in its logs.

   **Other candidates:**
   - The grep proposed in runs/20261016-integrate-r11-r13/insight.md#F-05a1b440 (option 2: a backticked literal followed by a parenthesis) fires on 212 of 396 briefs, this one included.
   - 77 of 396 briefs carry the node-brief template's `## Standard` or `## Example` heading, and 37 carry `## Write the result to`.
   - 10 briefs are over 43 KB:
     - the mcode trial's pasted brief, which failed;
     - four in ts-hybrid/experts-spots, where opencode answered;
     - five in sot-final-review/experts, where opencode's Laozi failed with missing sections. Its log has no auto-reject line, and I could not find the cause, so I count it neither for nor against a size rule.

5. **Why "can't write" ranks first, although it has only one incident (my #10).** The incident is runs/20261016-integrate-r11-r13/insight.md#F-c60edad6: the researcher's report file was refused.
   - The engine behaviour behind it is verified in `docs/EXECUTOR_KINDS.md`, once per engine:
     - qwen headless exits 0 with no file (line 366);
     - opencode `--agent plan` refuses to write (line 282);
     - agy soft-denies tools and exits 0 (line 365).
   - Both signals are exact, which is why it ranks first:
     - first signal: the call expects a result file (a `## Write the result to` heading, or the dispatcher's expected result path);
     - second signal: the engine and mode in the command, which the guard already recognises.
   - Failure prevented: an exit-0 call with no result, found only after the call has used its full time.

6. **Rule 2 second, narrowed by the replay (my #2).** Its source is runs/20261016-six-experts/insight.md#F-7f938bdf, option 1. A version that fails on any path would block 6 good runs for each bad one. I narrowed it to existing files, sent to opencode, with `~` expanded. Even so, on the history it blocks about 2 good runs for each bad one.

7. **Rule 3 only under a condition (my #10).** runs/20261016-four-experts-what-counts-as-change/insight.md#F-e69dfb66: mcode passed 9 KB and failed every input of 44 KB or more, while opencode answered a 67 KB brief. That is one engine on one day, and "n=1 is a hint, not a law." (`EJ's rule`). The comparison is against the engine's own record, not against a number I chose. runs/20261016-four-experts-what-counts-as-change/insight.md#F-485505f6 holds mcode back until it passes a canary at full brief size. So this rule only pays if mcode is routed.

8. **Compare against doing nothing (my #4).** The current way has no pre-flight. It relies on the post-run checks: `answer_ok`, the result traps in `checkResult`, and "an empty or missing result file counts as a failure" (`EXECUTOR_KINDS.md:368`). The q1q2 seats lost only 35 s and 15 s of engine time. The real cost was diagnosing the failure and running it again, and in runs/20261014-code-map-build/insight.md#F-60cad515 the status file hid the real cause behind "empty answer". So a pre-flight check adds two things: the call is not wasted, and the cause is named. That is why few false alarms matter more than wide coverage.

9. **Why a script and not a memory rule (my reading, based on an insight).** In runs/20261016-four-experts-what-counts-as-change/insight.md#F-4981093a, a rule kept in memory was broken within an hour because nothing checked at the moment it applied. F-7f938bdf says the same about the "copy inputs in" note.

10. **What not to verify (my #2, my #5).**
    - **Literal followed by a parenthesis** (F-05a1b440, runs/20261016-integrate-r11-r13/insight.md#F-4cbb2f4b): it fires on 212 of 396 briefs because it matches this project's citation style. The real problem is wording that can be read two ways, which a script cannot see. The test-writer cross-check already caught it.
    - **Template parts present:** only 77 of 396 briefs carry those headings, so this would be adopting a new rule, which is EJ's call. A present heading also doesn't show that the example covers each record; F-4cbb2f4b's miss was a missing example for one record, not a missing section.
    - **Unfilled placeholders:** the template's own progress line (`<ISO time> · <piece id>`, `node-brief.md:34`) is meant for the worker to fill, so the regex would fire on briefs that follow the template. No insight records a placeholder failure.
    - **Existence of every repo path named:** outside a declared list of inputs, output paths and historical mentions look the same as inputs.
    - **Text that is the same on every call:** the answer sections, the "copy Chinese exactly" sentence, and the command shape (runs/20261016-time-monitor/insight.md#F-173e0190). Test these once in the test suite, not on every call.
    - **Quota and readiness** (runs/20261016-four-experts-what-counts-as-change/insight.md#F-2cc835e3, runs/20261015-ts-hybrid/insight.md#F-3b8bdcec): these are properties of the engine, not the file, and the canary step owns them.
    - **Answer-side checks:** variant characters (runs/20261016-time-monitor/insight.md#F-84636a96) are already checked by `six_experts.py check` after the run.
    - **The language of the brief:** no failure has been recorded from it.

11. **How nature solves it (my #6).** This is recall of standard immunology, so it shapes the method but does not decide anything. T cells must react to invaders and never to the body's own cells. Two mechanisms do this:
    - **Negative selection:** T cells that react to the body's own molecules are deleted in the thymus before they are released. The borrowed version: a rule is approved only after a replay against calls that worked.
    - **Co-stimulation:** a T cell needs a second signal before it acts. The borrowed version: each rule fails a call only when the file's content and the engine's known weakness both hold, which is why rules 1–3 are tied to specific engines.

12. **Does the analogy fit (my #7)?**
    - Same: the rules are fixed patterns, there is a library of "own" cases (calls that worked), and a false alarm is the main cost.
    - Different: the body's set of its own molecules is complete and clean. Our "worked" label only means the answer had its sections, and we have only a handful of labelled failures.
    - Verdict: the key condition holds partly, so I keep the analogy only as the way rules are admitted, not as evidence that the rules are right.

    The trap catalogue already shows why admission matters. The `proposed` trap `agy-plan-mode` (`traps.yaml:63-71`) matches every 范蠡 call, because the runner passes `--mode plan` (`six_experts.py:125`). Yet agy answered `ok` in q1q2, sot-must-should, harness-health/experts and sot-yaml-review/experts. A replay would have rejected that trap.

13. **Small and reversible (my #8).** Turn the check on in `six_experts.py run` first, because it writes `status.json` and logs, so its effect can be read. Then turn it on for worker-brief calls.

14. **Report what failed (my #9).** Two recorded failures would not have been caught by any brief check:
    - The 20261013-ancients-page opencode build was "blocked by external_directory, exit 0 no work" (`docs/TASK_TYPES_LEDGER.md:30`). Its brief names no outside path; the engine picked the location itself.
    - runs/20261015-ts-hybrid/insight.md#F-cf7d58f7: opencode stopped without a result, cause not found.

    The post-run checks stay.

15. ***Proposed change to the pattern*.** Before a new pre-flight trap goes from `proposed` to `approved`, it is replayed over the briefs in `runs/` together with their outcomes. Its hits on failed calls and on calls that worked are written into the run folder. This changes "each piece has its own check" into "each check is itself checked before it can block work". Today's catalogue line ("added as `proposed` until the owner approves it") gains this evidence step.

The named categories (spec, tool) missed runs/20261016-integrate-r11-r13/insight.md#F-c60edad6, filed as own-work. It is the only recorded incident for the top rule.

## What I need to know
1. **Does the check get the engine command and the expected result path, or only the file?**
   - Only the file: rules 1 and 3 cannot run, and rule 2 applies to every engine, which raises its false alarms.
   - Command too: the three rules as ranked.
2. **Will mcode, or any engine with a recorded size failure, be routed?** If not, skip rule 3 until one is.
3. **Does EJ want the node-brief template to be mandatory for every worker brief?** If yes, a check that its parts are present becomes cheap and exact, and ranks fourth. If not, it stays out.

## Costs and risks
- **Rule 1 (my #10):** the engine-mode table rests on one verification per engine. A CLI update can make it stale, and then the check blocks a working call or lets a broken one through. Price: keep the table in the guard's engine catalogue and re-check it with the canary.
- **Rule 2 (my #2):** on the history it blocks about 2 good runs for each bad one. The writer clears a block by rewording or copying the file in, which I expect to take minutes (my reading). Risk: writers learn to drop backticks from paths, and the check stops seeing them (my reading).
- **Rule 3 (my #10):** it rests on one engine and one day of data, and providers change their limits.
- **The check as a whole (my #4):** each incident it prevents is small; q1q2 lost 35 s and 15 s of engine time. With 1 auto-reject run in 64, a live before/after comparison will be slow to show anything. The replay is the test that decides.
- **Runtime (my #10):** a regex and a few file checks per call should take milliseconds. I did not measure this, because the timing script needed approval here.
- **False confidence (my #9):** a pass may be read as "the brief is fine". It checks only three mechanical faults. Wording that can be read two ways, as in F-4cbb2f4b, still passes.
- **Replay step (my #2):** minutes per new rule (my reading). This is the cost I recommend paying.

## How we would know I was right
Predictions, written before any result (my #3). The stop date is EJ's time box.

1. **Replay** over the 396 briefs and 64 expert runs:
   - Rule 1 fires on the F-c60edad6 researcher call and on no call that wrote its result file. If it fires on any call that wrote its file, its signals are wrong and I withdraw it (my #1).
   - Rule 2 fires on both q1q2 opencode seats, and on the opencode seats of harness-health/experts and ts-hybrid/experts-spots. This is already measured, so the replay only confirms the script matches my grep.
   - Rule 3, scoped to mcode, fires on the mcode trial's briefs and nothing else.
   - The `proposed` trap `agy-plan-mode` fires on the agy runs that were `ok`, which shows why admission is needed.
2. **Live,** with the check on in `six_experts.py` only (my #8), compared with the 64 runs before it (my #4):
   - no seat ends with an "auto-rejecting" log line;
   - count the blocks the main agent clears where the run then works. That is the price of false alarms. If, over EJ's window, it is larger than the incidents prevented, rule 2 goes, and that is reported as a result (my #9).
3. **Sabotage control:** plant one brief that names an outside-repo file `~/…` for an opencode seat, and one with `## Write the result to` for an opencode `--agent plan` call. The check must fail both before any engine starts.
