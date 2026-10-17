# Dave — what memory-check v1 should improve next

## Answer
First, close the paths where the session-start warning stays silent even though the checks did not finish: `--warn` should print a line for a MUST that could not run, and the hook should not swallow a crash or a timeout. Then ask for EJ's yes to the hook, because that is U3's only unmet acceptance. Also tell EJ that the agent-memory folder the guideline names does not exist on this machine, while Claude Code's per-project memory does. Do no more check-logic work until a real project has `project-memory/`; today, no project on this machine has one.

## How I decided

1. **What would change my mind (my #1).**
   - If `--warn` on a shallow fixture with `project-memory/` already prints a line for the MUSTs that could not run, improvement 1 is wrong and drops out.
   - If EJ says Claude Code's per-project memory is outside the guidelines on purpose, improvement 3 shrinks to a one-line note.
   - If a project will adopt `project-memory/` within this run's time, calibrating on it moves to first place.

2. **The data that already exists (my #5).** Each item names the call that checked it.
   - **No real memory anywhere.** Glob `**/project-memory/INDEX.md` under `/home/smoke01/dev` finds none. So, by C4 (`REQUIREMENTS.md:46–48`), every SoT and CACHES record is "not applicable" on every project on this machine. The only thing the warning can print today is the missing-`AGENTS.md` line.
   - **Half the repos lack AGENTS.md.** Glob `*/.git/HEAD` finds 6 full clones directly under `~/dev`. Glob `*/AGENTS.md` shows 3 of them have no `AGENTS.md`. I looked at file names only and read no contents.
   - **The named agent-memory folder is missing; Claude Code's memory exists.**
     - `SOURCE_OF_TRUTH.md:23–24` puts agent memory at `~/.claude/agent-memory/<name>/`, "the way Claude Code does it". That folder does not exist here (Glob error: "Directory does not exist").
     - `~/.claude/projects/*/memory/MEMORY.md` exists 7 times (Glob). This project's folder holds 48 `.md` files.
     - `CACHES.md:508–513` uses SEZA's `MEMORY.md` (52 lines) as its own use case.
     - The smoke report still says agent memory is "absent" (`smoke-report.md:17`).
   - **The guideline copies are current.** `sha256sum` shows `memory_check/guidelines/*` byte-identical to `docs/memory-system/*`.
   - **Not measured.** I could not run the tool: the command needed approval and this session cannot give it. I also did not re-run `bun test`; "70 pass" is the brief's fact. So the run time of `--warn` is unknown.
   - **What this shows and doesn't.** It shows where the tool has real input today: the location list (F1) and the `AGENTS.md` line. It does not show how the check logic behaves on real entries, because there are none.

3. **Improvement 1: the warning is never silent when a check did not finish.**
   - **What.**
     - In the tool: `warn.ts:46` keeps only `verdict === "fail"`. Add one line naming the MUST ids that "could not run" (ids only, never entry text).
     - In the proposed hook command (`settings-diff.md:22`, `… --warn 2>/dev/null || true`): if the tool exits non-zero with no output, print one line such as "memory-check did not finish". Run it under an inner time limit below the hook's 20 s, so a timeout also prints that line. The limit's value is the main agent's or EJ's to set, not mine.
   - **Serves.**
     - `VISION.md:11–12`: every agent starting a session "must not start work on memory that is missing, stale or broken without being told".
     - `VISION.md:23`: never "say a requirement passes without the evidence". A silent warning reads as "all pass".
   - **Why it is needed now.** These silent paths can all happen (my reading of the code, not run):
     - A MUST that could not run makes the tool exit 1 (`command.ts:123`, R3 at `REQUIREMENTS.md:73`), but it gets no warning line.
     - Could-not-run is reachable: a broken python3 or a failing `git log` (`fix-2.result.md:29`), or a shallow clone (C5, `REQUIREMENTS.md:52`).
     - An uncaught error in `runChecks` (`command.ts:106`, no try) goes to stderr, and the hook discards stderr.
     - None of the R2 tests covers could-not-run (test names in `acceptance.test.ts:123–125, 213, 245` and `review.test.ts:113`).
     - The hook diff that would ship this silence is waiting for EJ's yes (`settings-diff.md:37`).
   - **Done when.**
     - A new test, failing first: a shallow-clone fixture with `project-memory/`, run with `--warn`. My prediction for the current code (my #3): empty stdout and exit 1. After the fix: exactly one line with the ids, no entry text.
     - The existing R2 tests still pass.
     - For the hook part: a by-hand run with a stub that exits 2, and one that sleeps past the limit, each prints the line.
   - **Basis (my #10).** n=3 earlier cases in this project where a tool's empty output was read as success (insights below). That is a pattern hint, not a law.

4. **Improvement 2: EJ's yes to the session-start hook, after improvement 1.**
   - **Serves.** U3's minimum acceptance ("the session-start hook prints one line per failing MUST…", `USE_CASES.md:25–26`). It is the only use case whose acceptance is unmet.
   - **Why it is needed now.** `settings-diff.md:37` says "Yes recorded: (not yet)".
   - **What EJ will actually see today.** The `AGENTS.md` line in 3 of 6 repos, and nothing else anywhere (from step 2).
   - **Small and reversible (my #8).** It is one entry in one settings file. If EJ prefers, the same entry can go first into a single project's `.claude/settings.json`.
   - **Done when.**
     - The first session after install is the trial run (the canary). In a git repo without `AGENTS.md` it shows the line; here it shows nothing.
     - Session-start time is measured with and without the hook (my #4: the control is no hook). The time is a reported number, not a pass/fail gate.

5. **Improvement 3: report the agent-memory location mismatch to EJ (no code).**
   - **Serves.** U1's purpose: "the owner learns which memory exists… and the agent memory the guidelines place outside the repo" (`USE_CASES.md:7–8`).
   - **Why it is needed now.** U1's fails-if passes to the letter, because the named folder really is absent. But the report tells the owner "agent memory: absent" for a project with 48 memory files (step 2). That is misleading (my reading).
   - **Who fixes it.** The tool cannot list a location the guidelines don't name without "adding a rule of its own" (`VISION.md:18`). So this is a guideline problem, and `AGENTS.md:7–8` says such problems are "reported, not fixed here".
   - **My reading, from recall.** `~/.claude/agent-memory/<name>/` is Claude Code's per-subagent memory. `~/.claude/projects/<slug>/memory/` is a different kind, per-project auto-memory, which the guideline does not name.
   - **Done when.** EJ's answer is recorded. If EJ names that folder, F1 lists it and a U1 fixture test covers it, failing first.

6. **Nature (my #6, my #7).** I considered "missing-self" in the immune system: a missing signal is treated as danger (*recall*).
   - Same: an absent signal is ambiguous between healthy and broken.
   - Different: there, healthy cells send a signal, while U3 requires silence when everything is clean.
   - The key condition differs, so I dropped the analogy and borrowed nothing from it.

7. **Remove or simplify.**
   - **(a) Collapse the "not applicable" rows.** Show one line per shared reason, with its ids.
     - Serves `VISION.md:10`: the owner wants to know "without reading the guidelines".
     - Case: today every report on this machine looks like `smoke-report.md`, where 72 of 78 records repeat one reason (`:128`).
     - Cost: the acceptance suite parses one row per id, and those tests were written by another engine (T1). So this is EJ's call and ranks low.
   - **(b) Stop check-logic work until real memory exists (my #5).** That means no further CACHES checks and no more U2 hardening. All 14 review findings came from probes and fixtures, and nothing real reaches that code yet.
   - **(c) Nothing in the code to remove.** I found no module serving no use case. This is a null result, not a full audit: I read `warn.ts`, `cli.ts`, `command.ts` and parts of `gitchecks.ts` and `gitrequirements.ts` (my #9).

8. **Not proposed, because nothing needs them now.**
   - A test that guideline copies stay in sync: they match today. It becomes needed at the first edit of the YAML or `CACHES.md`, as a one-test fix.
   - Hook run time on a large memory: K4.3 makes about N × (3 + 2c) git calls for N entries, each touched by c commits (`gitrequirements.ts:217–233`, `gitchecks.ts:238–253`; my reading). No large memory exists. If it ever runs too long, improvement 1's "did not finish" line makes that visible.
   - Calibration on real memory: when a project adopts `project-memory/`, its first full report is the calibration. Treat each fail there as a suspected tool bug until it is checked (my #9).

9. ***Proposed change to the pattern*: the enhance step starts with a list of the real inputs the tool will meet, before experts rank improvements.**
   - What changes: before ranking improvements, list the real inputs the tool will meet, from file names only. Ask before running the tool on EJ's private work repos.
   - Evidence it matters: here, four Globs (under a minute) changed my ranking. Without them, I would have ranked hardening driven by fixtures.
   - Basis: n=1 (this run).

10. **Insights used.**
    - `runs/20261016-six-experts/insight.md#F-7f938bdf`: an engine exited 0 with an empty answer. Its option 2, "a rejection is visible instead of an empty answer", is the shape of improvement 1.
    - `runs/20261017-agent-lessons/insight.md#F-0969936e`: the same failure again (agy, exit 0, no output). It raised my confidence that silence-as-success recurs here.
    - `runs/20261016-four-experts-what-counts-as-change/insight.md#F-d3132a7f`: a command shape hid the failing exit from what reads it. `2>/dev/null || true` has that shape, so improvement 1 changes the hook's command.
    - `runs/20261016-time-monitor/insight.md#F-173e0190`, option 3, "canary-proved before a run depends on it": this made the first session after install improvement 2's check. Today the diff was only "tried by hand" in a shell (`settings-diff.md:30`).
    - No category was named, and none of the index's categories was wrong for this question.

11. **Not done.** I did not write the guard's criteria file or start its deadline: the brief says to write no files, and the time is set by the main agent.

## What I need to know
- Will any project adopt `project-memory/` soon, and which one? If yes, the first report there is the next step and moves to first place. If no, freezing the check logic (7b) holds.
- Is `~/.claude/projects/<slug>/memory/` agent memory, user memory, or outside the guidelines? Only EJ, as owner of the guidelines, decides. The answer settles whether U1 is met in substance.
- Does a MUST that could not run count as "failing" under U3? U3's fails-if says the warning holds nothing else (`USE_CASES.md:24`), which literally forbids improvement 1's line. U3's purpose ("missing or failing") and R3 (could not run exits 1) support it. Under the pattern, the main agent decides this for now; EJ may overrule.

## Costs and risks
- **Improvement 1** (my #4, my #10): one more kind of warning line, and a line every session wherever a shallow clone has `project-memory/`. Improvement 1 changes how U3 reads, which needs EJ's acceptance. Cost: one small code change and one test in the tool, plus an edit to the proposed hook command.
- **Improvement 2** (my #5, my #8): an unmeasured delay at every session start (two bun starts, python3 and git). There will be one line per session in the 3 repos without `AGENTS.md`. It is reversible: one entry in a settings file.
- **Improvement 3** (my #1): one question for EJ. If EJ adds the location, F1 gets a small change and a test, and it then depends on a vendor's path, which may change (*recall*).
- **Freezing check logic** (my #9): if a project adopts `project-memory/` unexpectedly, its first report may hold false fails. They should be reported as suspected tool bugs, not as memory faults.
- **The pattern change** (my #10): a minute per enhance step. Also a privacy risk if the list of inputs goes beyond file names in EJ's work repos.

## How we would know I was right
Predictions, written down first (my #3). Each stops at the event named, or is reported as not measured if the run's time ends first.
- **P1.** On the current code, `--warn` on a shallow-clone fixture with `project-memory/` gives empty stdout and exit 1. Stop: the first run of the new test. If it already prints the ids, I was wrong (my #9).
- **P2.** After improvement 1, the same run prints exactly one line with ids and no entry text. A hook stub that exits 2 or times out prints "did not finish".
- **P3.** After install, the first session in a repo without `AGENTS.md` shows the line, a session here shows nothing, and the measured delay is reported against a session without the hook.

Top three:
1. Make the warning speak when a check did not finish: a could-not-run line in `--warn`, and the hook keeps crashes and timeouts visible.
2. Then get EJ's yes to the session-start hook (U3), with the first session as its trial run.
3. Tell EJ that the guideline's agent-memory folder is absent here while Claude Code's per-project memory exists; no more check-logic work until real `project-memory/` exists.
