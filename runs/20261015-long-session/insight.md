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

## F-8712e9fc — the full Python suite had one failing test

Whys:
1. Why did the suite fail? `tests/test_skills_export.py::test_skills_export_is_current` found `skills/requirement-check/SKILL.md` modified before export.
2. Why was it modified? Another session's uncommitted edit to `.claude/skills/requirement-check/SKILL.md` and its exported copy is in the working tree.
3. Why does that fail this session's run? The export test checks the whole `skills/` tree, so any uncommitted change there fails it, whoever made it.
4. Why was it run anyway? The full suite is the baseline check after a merge; the failure was known (seen after the first merge) and not resolved because the edit is not this session's.
Source: check
Root cause: shared working tree — the export test cannot tell this session's changes from another session's uncommitted ones.
Options:
1. [rule] Run the suite in a clean worktree after a merge, so other sessions' uncommitted edits cannot fail it. evidence: the guard-r4 worktree run passed 922/922 and 1030 + this one.
2. [check] The export test names the files that drifted and whether they were committed by this branch. evidence: its message already lists the file.
3. [config-advice] Ask the owner whether the requirement-check edit should be committed or dropped. evidence: `git status` shows it modified since the session started.
