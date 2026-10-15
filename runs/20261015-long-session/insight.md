# Insight — run 20261015-long-session (the main agent's session)

## F-f09b058d — the guard logged a missing output that was not missing

Whys:
1. Why was a failure logged? The PostToolUse hook checked `claude -p … > $R/answer.txt` and found no file at `$R/answer.txt`.
2. Why no file? The hook read the path from the command text, where `$R` is a shell variable it cannot expand; the real file was written.
3. Why did the hook treat an unknown path as a missing one? SPEC M5 said to check the output file of a recognised call, and said nothing about paths the text cannot resolve.
4. Why did the spec leave that out? The review and the E2 replay used literal paths; no planted input held a variable.
Source: check
Root cause: the result check took an unexpandable path as a real one — a false failure, from a gap in SPEC M5 and its tests.
Options:
1. [check] Skip the result check when the output path or a `cd` target holds `$`, a backtick or a glob (SPEC round 4, D3), with a test planting `-o $OUT/r.md`. evidence: this record; `.claude/skills/workflow-design/guard/SPEC.md` round 4.
2. [tool] Resolve simple `NAME=value` assignments earlier in the same command line before checking. evidence: the command set `R=…` on its first line.
3. [rule] Engine calls in briefs and runners use literal paths. evidence: the E4 and long-session runners all expanded variables.
