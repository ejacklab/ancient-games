# 孫子 (Sun Tzu) — keep or remove `deadline wait --mark`

## Answer

Keep `--mark P`: the removed marks were automatic reminders at fixed percentages, while `--mark` is a timer the agent starts and sets itself, and the only recorded timer in this project was aimed five minutes before the deadline — that is this flag's job. If the owner meant to forbid every percentage trigger, even one the agent starts, then remove it; on the reason as given, keep it.

## How I decided

1. **Laid the choice out before choosing (my #1).** The facts to count are the vision, the owner's reason, the code, the use so far, and the two readings. 「多算勝，少算不勝，而況於無算乎？」 (quoted). The count turns on one question: **who fixes the moment?** The removed reminders fixed 50/80/100 themselves and fired from the hooks after a tool call. Read in `cli.ts`, nothing of `deadline wait` fires unless the agent runs it, and the agent names the point. That is a different act, not a smaller version of the same one.

2. **Told the two defects apart (my reading).** The owner's reason as given is about prediction: fixed percentages cannot well predict the specific moment when exploring solutions. The defect is the **fixed** percentage, not the percentage. A number the agent chooses at the moment it starts the wait is the agent's own prediction, made with the work in front of it. Reading A needs the stronger claim — that any percentage is a leftover — and the facts given do not carry it.

3. **Tested the "leftover" claim against the record (my #17).** 「角之而知有餘不足之處。」 (quoted). Three facts from the repository:
   - The `wait` branch reads only the deadline's start and minutes; it never reads the marks field that the reminders used (read in `deadline.ts` and `cli.ts`).
   - The commit that removed the reminders rewrote the final usage-error line, deleting `deadline start ... [--marks 50,80,100]` and leaving `wait [--mark P]` (read in `07b67a9`). That does not prove it was kept on purpose, but it is not code the removal forgot to sweep.
   - No run's record shows `deadline wait` being run at all. The one timer in the runs tree was set for 11:17 against an 11:22 deadline (read in `runs/20261016-time-monitor/state.md`), and it was a plain `sleep` (given). That is a pre-deadline wake aimed five minutes early — B's use case, done without the flag. The run finished early, so the record shows the intent, not that the wake helped.
   
   So the measured zero — `grep -rn "deadline wait --mark" runs/` finds none — measures the **whole timer path**, not the flag. It cannot decide between A and B.

4. **Put the harm beside the benefit on both sides (my #6).** 「是故智者之慮，必雜於利害，雜於利而務可信也，雜於害而患可解也。」 (quoted). The harm column is in the next section. The decisive entry is that keeping costs a small unused surface, while removing loses the only wall-clock wake that can return **before** the deadline without a tool call. The after-call clock cannot cover that case: it is written after a call, so a long call leaves the agent blind until it ends.

5. **Applied the gate: move only with advantage (my #5).** 「非利不動，非得不用，非危不戰。」 and 「合於利而動，不合於利而止。」 (quoted). A removal is also a move and needs a use case. Its only gain is tidiness; no vision line or use case in view asks for the deletion, while keeping serves the pre-deadline wake. The option that serves no use case here is removal.

6. **Refused the fixed form the owner objected to (my #10).** 「故兵無成勢，無恒形，能因敵變化而取勝者，謂之神。」 (quoted). Deleting `--mark` does not remove the prediction from the system; it moves it to a plain `sleep` interval the agent computes, where the guard cannot see it and no status line is printed. Keeping the flag keeps the prediction where the deadline is known.

7. **Decided provisionally and bounded the test (my #8, my #17).** 「故兵貴勝，不貴久。」 (quoted). Keep now; do not argue it longer than the trial needs. **Proposed change to the pattern:** set the timer at the start with `deadline wait --mark`, and record the command and the chosen mark in the state's start line, as the time-monitor run recorded "background timer fires 11:17". It changes "the time is set at the start" by adding that the timer is set there too, and it makes the next decision on the flag a measure instead of a grep over runs that never invoked the command.

## What I need to know

- **Did the owner's decision cover every percentage trigger, or only the automatic reminders?** If it meant "no percentage trigger at all, even one the agent starts", remove the flag; my answer is conditional on the narrower reading.
- **Is `deadline wait` itself staying?** If way 2 is being retired and timers are to be plain `sleep`, `--mark` goes with the branch — a larger decision than this one, which I was not given.
- **Does a background timer's output reach the agent when it fires, without the agent making a call?** If it does not, a pre-deadline wake buys nothing until the next call and the case for keeping weakens. The time-monitor run did not test this, because it finished early.

## Costs and risks

- **Keep — an untested branch (my #6).** No test exercises `--mark`; the one `wait` test runs the default 100% (read in the test tree). Risk: the mark offset can regress silently. Cheap fix: plant a two-minute deadline, run `--mark 50`, and require a return at about one minute with `used 1 of 2 min` and exit 0.
- **Keep — the word (my reading).** T5 says "no marks" while T3 documents `wait [--mark P]`. Risk: the next reader repeats reading A and deletes the flag. Fix the wording: scope T5 to automatic marks, and call `--mark` the agent's own wake point.
- **Keep — the unit (my reading).** The recorded intent was "five minutes before"; a percent makes the agent convert (11:17 on an 11:22 deadline is about 92%). Risk of a mis-set mark. Not decisive: a coarse 90 still leaves time to write the report.
- **Remove — the capability leaves the guard (my #5, my #10).** The next pre-deadline wake is a `sleep` and the agent's arithmetic, invisible to the guard, with no status line. The guard cannot then see or measure what replaced the flag.
- **Remove — the record (my #6).** SPEC T3 and the usage text must be rewritten, and the reason has to be written down, or the next reader cannot tell whether a leftover or a capability was removed.
- **Remove — the less reversible choice (my reading).** Keeping can be removed later on evidence; removing cannot be tested. With one anticipated timer and zero invocations of the path, that asymmetry matters.
- **Common risk (my reading).** The evidence is thin in both directions. Either choice is provisional, and the trial below is what makes it more than a preference.

## How we would know I was right

Run one time-boxed task with the timer set at the start:

```
bun .claude/skills/workflow-design/guard/src/cli.ts deadline wait --mark 90
```

with the same command and the chosen mark recorded in the state's start line. I am right if the timer fires before the deadline, the agent sees it, the report is written before the time-up line, and the record shows which mark was chosen and why.

I am wrong if a run needs a pre-deadline wake but reaches for `sleep` while `--mark` exists — then the flag is not discoverable, and the fix is the docs, not the flag. I am also wrong if two consecutive time-boxed runs need no pre-deadline timer at all — then the need is not recurring, and `--mark` should go, with `deadline wait` itself re-examined in the same decision.
