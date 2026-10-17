# Answer — keep or remove `--mark P` on `deadline wait`

## Answer
Remove `--mark P` (reading A), provisionally. No run has used it, no test covers it, and a percent point the agent picks is the same kind of point the owner declined. If EJ wants agents to wake before the deadline, the plain `sleep` the time-monitor run used already does that.

## How I decided
1. **Vision and use case.** The use case is that the agent cannot feel time, so the guard tells it. The clock line after every Bash or file-write call and the time-up line after the deadline serve that. Plain `deadline wait` (wake at the deadline) fits it too. The owner declined the 50/80/100% reminders because percent points are "not able to well predict, specific when exploring solutions". My reading is that this objection is about picking a percent of the deadline, not about who picks it. EJ did not say that, so it is *my reading*.
2. **Use.** The brief says no run has used `--mark`. I ran a wider search: `--mark` appears only in `cli.ts`, the guard `SPEC.md` (T3), the time-monitor run's report, state and review files, and this question's files. The one run that needed a timer used plain `sleep`. That is *measured*, but only for this repository.
3. **Tests.** No file in `guard/test/` contains `--mark`, so the flag is untested (*measured*). The time-monitor review (`nodes/review.result.md`, item 10) asked for a test with an explicit earlier `--mark`, and none exists. The only `deadline wait` test, at `round10-deadline.test.ts:190`, uses the default.
4. **The documents disagree.** `method.md` (line 551), edited after the owner's decision, says `deadline wait` is "a timer that returns at the deadline", with no `--mark`. `SPEC.md` T3 and the time-monitor report still say "or until P percent". Removing the flag makes everything match the newer text.
5. **Reversibility.** The flag is about 7 lines (`cli.ts:221-227`). It is cheap to add back from git history either way, so reversibility doesn't decide. The question reduces to whether any use case needs it, and none has appeared (steps 2 and 3).
6. **Recall, which does not decide.** A pre-deadline wake is useful when the agent is idle waiting on workers, because the clock line only appears after a call. That is *recall*. It argues for being able to wake early, not for this flag specifically, since `sleep` can do it.

## What I need to know
- Does EJ want agents to schedule their own wake-ups before the deadline, for example to write the report? If yes, keep `--mark` or document the `sleep` recipe. If no, remove it.
- Has any time-boxed run overrun or lost its report because the agent was idle until the deadline? I found no such record, but I did not look at every run.
- Does anything outside this repository call `deadline wait --mark`? My search covers only this repository.

## Costs and risks
- **Removal fails silently.** `flagValue` (`cli.ts:70-76`) only looks up the flags it is asked for. I found no unknown-flag check (`grep "unknown flag|unknown option|Unknown"` in `cli.ts` returned nothing). If the `--mark` branch is deleted, `deadline wait --mark 90` would run to 100% without complaint. An agent that learned the flag from the old `SPEC.md` or the time-monitor report would sleep through its own 90% wake-up. The removal must make `--mark` a loud usage error, or it breaks the "fail loud" rule.
- **Removal loses a convenience.** The agent must work out the seconds for an early wake from `deadline status`. The arithmetic can go wrong. I have no measurement showing it did.
- **Removal edits three places.** `cli.ts` (the code and the usage string at lines 45 and 242), `SPEC.md` T3, and the time-monitor report's wording.
- **Keeping leaves a trap.** `--mark` is a "percent of the deadline" feature that looks like the removed marks. A later agent or reader may take it as a sanctioned reminder and rebuild what the owner declined.
- **Keeping leaves dead, untested code**, and a gap between `method.md` and `SPEC.md`.
- **This is provisional.** The decision rests on zero uses in one repository. If an early-wake use shows up, the cost of being wrong is one small flag to restore.

## How we would know I was right
- **After removal:** `deadline wait --mark 90` exits non-zero with a usage message, and `deadline wait` (no flag) still passes `round10-deadline.test.ts:190`. A one-line test can cover the first part.
- **Documents:** `grep -rn -e "--mark" .claude/skills skills docs` returns nothing except the usage error and its test.
- **Over the next time-boxed runs:** the report says whether any agent needed to wake before the deadline and what it used. If a plain `sleep` did the job each time, that confirms removal. If agents repeatedly work out seconds by hand, or a report is lost to an idle wait, that argues for putting `--mark` back.
