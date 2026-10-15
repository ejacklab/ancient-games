# Dave — a harness-health check for the readiness step

## Answer
Build a separate `harness_health.py` beside `readiness.py`. It should start with one harness (Claude Code) and one requirement (6, guardrails), and before it is built further it should be tested against the harness failures we have already recorded. My prediction, written down now: probes that only read config files will catch at most 2 of the 7 recorded harness traps. If that holds, the "help" worth building is a memory of known traps with a fix tested for each one, not a growing list of config keys. If the opt-in canary in N1 is not allowed, behaviour traps stay `unknown` at readiness time and the per-run checks in dispatch remain the only defence. *(my reading, n=0)*

## How I decided

1. **What would change my mind (my #1).** The question that settles it is: on a setup that reproduces each recorded trap, does the check flag it before dispatch? If config probes catch most of the recorded traps, I drop my "trap memory first" ordering and build config probes for every harness.

2. **Use the data we have first (my #5).** Three sources already exist:
   - **The baseline.** `runs/20261015-harness-health/readiness-before.json` has 26 lines: 20 verified, 3 unknown, 2 reported, 1 MISSING.
   - **History.** 14 earlier `readiness*` outputs sit under `runs/*/`, so we have a history to compare against for drift.
   - **Seven harness traps** recorded in this project's memory notes:
     1. `codex exec` hangs when stdin is not `</dev/null` (n=1).
     2. Parallel opencode starts give "database is locked" (n=1).
     3. opencode auto-rejects reading a file outside its allowed paths and exits 0 having done nothing (n=1).
     4. agy soft-denies shell or `read_url`: exit 0, empty stdout (3 of 4 runs in one run folder).
     5. agy `--mode plan` stops at a plan.
     6. agy returned a transient 502 at login.
     7. Worktree isolation refused subagents' heredoc writes.

   What this shows: of the seven, only #3 (the allowed paths in `~/.config/opencode/opencode.jsonc`) and #4 (agy allow-rules) depend on a config file. The other five are behaviour that shows up at dispatch. What it does not show: whether those config keys can be read reliably on the installed versions (U6). Also, today's readiness probes no permissions at all, so the control catches 0 of 7. *(my reading of the probe list in the brief, not run as a test)*

3. **Write the prediction down first (my #3).** Before any probe code exists, write `runs/<run-id>/prediction.md` with three things:
   - **Metric:** how many of the 7 traps the check flags on fixtures that reproduce them.
   - **Expected result:** ≤2 of 7.
   - **Stop condition:** the backtest must finish before build step 5 starts.

   I give no date; the date is EJ's to set.

4. **Always run a control (my #4).** Compare against the current `readiness.py` on the same machine and the same fixtures (it catches 0 of 7 harness traps), and against the previous run's output (drift). A health line means "worse than", "changed since" or "absent", never a number judged on its own. This also answers U3 without inventing thresholds.

5. **Ask how nature solves it (my #6): immune memory and negative selection.**
   - After an infection the body keeps a detector specific to that pathogen, so the next exposure is caught fast. Borrowed mechanism: every recorded harness trap becomes a stored detector, carrying the incident it came from and its fix as the help. That is requirement 10 ("every agent mistake becomes a permanent fix") built into the check.
   - Negative selection: a detector that fires on the body's own healthy tissue is removed. Borrowed mechanism: a probe is kept only if it stays silent on a known-good fixture and fires on a planted-bad one. That is the house sabotage rule plus a control.

6. **Check the analogy fits (my #7).**
   - **Same:** the same threats recur (agy soft-deny hit 3 of 4 runs), and each detector is specific to one threat.
   - **Different:** the immune system acts on its own and kills the threat. Here the house rule is help, never auto-edit, so I drop that acting part. The body also generates detectors at random in huge numbers; here each detector costs a human-verified fixture, so I drop random generation too.
   - **Key condition:** traps must recur across runs, or a memory of them is worthless. Evidence for recurrence is thin (n=1 for most), so the analogy is kept on probation. If the backtest and the next runs show no repeats, drop it.

7. **Small and reversible, then scale (my #8).** One new script, not edits inside `readiness.py`, so it can be deleted without touching the inventory. Then one harness, then one requirement, then measure, and only then add the next harness.

8. **A small experiment beats a long argument (my #2).** U2 (what counts as help) and U6 (the key names) can both be settled by tests that cost less than debating them:
   - Help counts only if applying its snippet to a copy of the bad fixture's isolated HOME turns the probe from fail to pass.
   - A key name counts as verified only if a planted wrong value changes what the probe reports on the installed version.

9. **Report what failed (my #9).** `unknown` and "not caught" are results. The backtest reports the traps it misses with the same weight as the ones it catches.

10. **Say how sure I am (my #10).** The requirement-to-method mapping in the brief was done by the main agent and checked by no one, and every trap is n=1 or one run's worth. Any "Found → effect on the design" text (U5) is n=0 until the check has run on real runs.

**Verdicts on the unclear spots**

- **U1 (which harnesses): agree.** List every harness found. `--harness` narrows the verdict to the ones the design uses. Cost: longer output.
- **U2 (what help is): agree, with a test added (my #2).** Advice plus a ready-to-apply snippet; the script never edits harness config. A snippet ships only after it passes the flip test in step 8 above. Help for a known trap is that trap's own "how to apply" line, with its source run.
- **U3 (good enough without thresholds): agree, with comparisons added (my #4).** Pass/fail only where a concrete named thing is present or absent. Everything else is a comparison: changed since the last run, or worse than the control. No numbers. Whether "no `deny` list" fails requirement 6 is EJ's call, because requirement 6 names "hard policies", not a deny list *(my reading)*.
- **U4 (where it lives): agree, a separate script (my #8).** It reuses the same `Probe` dataclass and statuses.
- **U5 (how the result changes the design): defer (my #10).** Write the effects table only after real runs; until then mark it n=0 and leave the decision to EJ.
- **U6 (config formats unverified): agree.** Add the planted-value test for each key name (my #2). Anything not verified is `unknown` with the reason.
- **U7 (requirements judged per run): agree.** But a line "covered by <gate>" appears only if that gate file is found to exist. Otherwise it is an unchecked claim (my #10).

**New unclear spots**

- **N1 (decision for EJ).** Five of the seven traps are behaviour, and the current rule "never spends quota" leaves them `unknown` at readiness time. Should there be an opt-in `--canary` that spends a tiny amount of quota?
- **N2.** `dsh` and `opencode` are not probed at all. This is a measured gap, the cheapest fix, and inventory work, so it belongs in `readiness.py`.
- **N3.** The trap memory is specific to this project and the skill is generic. The trap catalogue must come in as a file through a flag, never hardcoded.
- **N4.** Some judgements need values, not just key names (for example `autoMode`, `skipDangerousModePermissionPrompt`, `sandbox_mode`). An allowlist of non-secret keys whose values may be read is needed, plus a test that a planted fake secret never appears in the output.
- **N5.** Drift needs a stored previous health output. Where it lives (`runs/<run-id>/harness-health.json`, then the most recent one found) needs EJ's agreement, per the evidence rule.

**Design**

- **Where it lives:** `.claude/skills/workflow-design/scripts/harness_health.py`, with tests in `tests/test_harness_health.py`. Both follow the existing pattern: isolated HOME and fake executables.
- **Per requirement:**
  - 1: instruction-file line counts measured, and changes since the last run, with no verdict.
  - 6 and 8: permissions, deny and allow, sandbox, approval keys, where verified.
  - 9: the hook list, and whether a run log exists.
  - 10: harness version changed since the last run, and known traps that match this setup.
  - 2, 3, 5, 7: "covered by <gate>" if the gate file exists.
  - 4: run `state.md` and the state-entry skill present.
- **Output:** the same table form as readiness, with one extra column, "help". Help is the setting, the file, a snippet, and the incident or source it came from.
- **Exit codes:** 1 only for a failed check on a harness named in `--harness`.

**Build order, each step with a check that can fail**

0. **Write `prediction.md` (my #3).** Fails if its timestamp is later than the first probe code.
1. **Add `dsh` and `opencode` to the readiness binaries (N2).** Fails: with the fake binary removed, the line must say MISSING.
2. **Fixtures: isolated HOMEs per harness, a good and a bad config each, with a fake secret planted.** Fails: the secret string appears in the output.
3. **Claude Code, requirement 6 only.** Fails: the bad fixture does not fire or the good fixture fires, or readiness output differs from `readiness-before.json` on the inventory lines.
4. **Backtest on the 7 traps against the control (my #4, #9).** Fails: the result is compared with the prediction, and a miss or a null result is reported as a result. Decision point for EJ: scale the config probes, or build the trap memory first.
5. **Help with the flip test (U2).** Fails: applying a snippet does not turn the probe to pass.
6. **Drift against the previous output.** Fails: a planted version change is not reported as "changed since".
7. **The other harnesses, one at a time, each after the planted-value test on its keys (U6).** Fails: an unverified key shows `pass` instead of `unknown`.
8. **Method 3.1 effects text (U5), marked n=0.** Only after real runs, and EJ decides.

## What I need to know
- Is an opt-in `--canary` that spends quota allowed (N1)? If not, 5 of 7 traps stay out of reach at readiness, and the per-run dispatch checks remain the only defence.
- For each requirement, what concrete thing counts as "absent means not good enough"? Requirement 6 in particular: is "no deny list" a fail?
- Which non-secret config values may the probe read (N4)?
- Where should the trap catalogue and the previous health output live (N3, N5)?
- Do the harnesses have a command that prints their effective config? (unknown) If yes, U6 gets cheaper and more reliable than reading files.
- The stop date for the prediction (my #3) is EJ's to set.

## Costs and risks
- **Fixtures for every harness and every key are the main build cost** (my #2, #8). They go stale when a harness version changes. The drift check flags the change, but someone must update the fixture.
- **The backtest may come back null** (my #9): config probes catch ≤2 of 7. If so, much of the "health" EJ asked for cannot be checked without spending quota. That is an honest but disappointing answer.
- **The analogy may not fit** (my #7): it rests on traps recurring, which is n=1 for most of them. If they do not recur, the trap memory is a list nobody hits.
- **Reading config files risks leaking a secret** (N4). The planted-secret test reduces the risk but covers only the patterns it plants.
- **Two scripts and two tables** (U4) cost the reader more than one, in exchange for being reversible (my #8).
- **Evidence is thin** (my #10). Each trap is n=1, or one run of four calls, and the main agent's mapping is unverified. Nothing here should be written into method text as a rule yet.

## How we would know I was right
- **The backtest in step 4 against the written prediction.** I am right if config probes flag ≤2 of the 7 recorded traps while the control flags 0. I am wrong if they flag 3 or more, and then config probes should be scaled first.
- **The flip test:** every shipped help snippet turns its probe from fail to pass in an isolated HOME. Any snippet that does not flip is counted as a failure.
- **Over the next real runs:** count the harness-caused failures seen at dispatch. For each, record whether `harness_health.py` flagged it before dispatch, compared with the same runs' plain readiness output. The check earns its place only if it flags failures the control did not. The number of runs is EJ's to set.
