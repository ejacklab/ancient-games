# Insight — run 20261017-agent-lessons

## Lessons used up by subagents — the main agent got none

Found by: the main agent, reading `.harness-guard/lessons-shown.json` after a `python3` call of its own got no hold:
seven lessons were already marked shown for session 1159cce6…, matching the commands the crossed-check workflow's
agents ran (`opencode`, `codex`, `node`, `cat`/`grep`). Cause by reading, not yet verified in the docs.

Whys:
1. Why did the main agent get no lesson? Each lesson was already marked shown for this session.
2. Why? The installed PreToolUse hook for Bash runs this repo's `cli.ts`, so the new code went live for Bash when it
   was saved; the workflow's agents' Bash calls reached it with the same `session_id` (my reading), took the holds and
   the marks.
3. Why was that not handled? The once-per-session key is the session only (`lessons.ts`, `takeUnshown`); the experts
   raised "do subagents' calls fire this hook under the same session" (delivery-q compare.md) and I went on without
   an answer.
4. Why go on? I treated the Bash path as not yet live because the Write/Edit matcher still needs the owner's settings
   change — but the Bash matcher was already installed.
Source: instruction — the build did not check which parts of a hook change are live the moment the file is saved.
Root cause: a once-per-session mark keyed by session, while one session runs many agents.
Options:
1. [tool] Key the shown marks by session and agent (the payload's subagent id when there is one), so each agent gets
   each lesson once. evidence: the seven marks above.
2. [tool] Give lessons only to the main agent (skip calls that carry a subagent id); subagents get theirs in briefs.
   evidence: the same; briefs already carry lessons (six_experts.py, node-brief).
3. [rule] Before saving a change to a hook's code, list which of its matchers are installed and treat those paths as
   live: test them before the save. evidence: why 4.

## F-0969936e — 范蠡's agy call answered nothing: a file read was auto-denied

Found by: the guard (R12.1-wrapped-fail, from the six-experts status entry "fan-li-agy"); the runner fell back to
Claude Opus as designed (`delivery-q/fan-li/status.json`).

Whys:
1. Why no answer? agy exited 0 with no output: "a tool required the "read_file" permission that headless mode cannot
   prompt for, so it was auto-denied" (`delivery-q/fan-li/logs/fan-li.agy-failed.log`).
2. Why a read it could not do? The question named a source outside the repo, `~/.claude/plans/agent-lessons-version-b.md`
   (`delivery-question.md`, Facts); agy headless may read only inside its workspace (my reading — the log does not
   name the file).
3. Why did the question name it? The new facts rule asks each fact to carry its source, and I cited the plan file where
   it lives, without copying it into the run folder.
4. Why did nothing stop that? The agy lesson (soft-denied tools) covers shell and web, not reads outside the repo, and
   no check looks at the paths a question names.
Source: instruction — an expert question may cite a file outside the repo, which some engines cannot read headless.
Root cause: a source path outside the repo in a brief for engines that read only inside it.
Options:
1. [rule] A file an expert question or brief cites lives inside the repo: copy an outside source into the run folder
   and cite the copy. evidence: the opencode lesson already says so for opencode; agy failed the same way here.
2. [check] six_experts.py refuses a question that names a path outside the repo (an absolute or `~` path that does
   not resolve inside it), naming the path. evidence: `delivery-question.md` names `~/.claude/plans/…`.
3. [tool] Widen the agy lesson to "reads outside the workspace are auto-denied too" and keep the Claude fallback.
   evidence: the log line above.

## F-c64c0bbb — criterion C4 not met: it named the mechanism ("context, never a deny"), and the design changed

Whys:
1. Why not met? C4 said the hook "adds the matching lessons as context, never a deny"; the build holds the call once
   (a deny with the lessons as the reason).
2. Why the change? Piece 1's docs answer: context arrives "alongside the tool result", too late for the call; five of
   six experts chose the hold (delivery-q).
3. Why did C4 fix the mechanism? I wrote the criteria at the start from the plan's first wording, before piece 1 —
   which existed to settle that very point — had answered.
Source: instruction — criteria may name a mechanism an unclear spot of the same run is still to decide.
Root cause: a criterion written against an undecided mechanism instead of the outcome it serves.
Options:
1. [rule] A criterion names the outcome (here: "the matching lessons reach the agent before the call runs"), never a
   mechanism an open question of the run still decides. evidence: C4's text; piece 1 in state.md.
2. [rule] When a provisional decision changes what a criterion names, the criterion is rewritten at once with the
   decision's id, and the old text kept in state.md. evidence: the same.

## Log times written from reckoning, not read from a clock

Found by: the main agent, when `date +%H:%M` printed 15:29 after `state.md` already held entries at 15:45, 16:10 and
16:22; the commits say 15:18, 15:22, 15:23 (`git log`). Corrected in `state.md` (its 15:30 line).

Whys:
1. Why wrong times? I wrote each log line's time myself, from the minutes the guard's clock line showed, added to the
   start time in my head.
2. Why from my head? The clock line gives minutes used, not the time of day, and I did not run `date` in the call that
   wrote the line.
3. Why no check? Nothing compares a state line's time with a clock; F-a03fa5b3 (a deadline epoch typed from memory,
   run 20261016-time-monitor) had the same cause and its fix was never chosen.
Source: instruction — the main agent writes times it has not read from a clock.
Root cause: a time of day written from reckoning, where one command would read it.
Options:
1. [rule] Every time written into a state, report or record is read from `date` in the same call that writes it;
   never computed. evidence: the corrections above.
2. [tool] The guard's clock line also prints the time of day (`… 26/180 min, 15:21`), so the time is in front of the
   agent on every call. evidence: the clock line printed minutes only.

## C17 guard tests fail on any commit while other sessions' engines run

Found by: the guard suite, three C17 tests (`test/round3.test.ts`) — once during the experts' run, then three times in
a row at 15:28, and again on the last commit in a clean worktree, while another session's `opencode run` and dsh were
running (`ps`). So not this run's change.

Whys:
1. Why do they fail? They count processes from the machine's live process list.
2. Why does that change? Other sessions' engines and hooks run on the same machine (my reading, not traced to the
   assertion).
3. Why does a unit test see them? The C17 tests read the real `ps` output instead of an injected list.
Source: check — tests that depend on the machine's live process list.
Root cause: the C17 tests read the real process list, which other sessions change.
Options:
1. [check] Give C17 an injected process list (the CLI already takes one for `running`), so the tests own their input.
   evidence: the clean-worktree run on HEAD failed the same three.
2. [rule] Run the guard suite only when no other session's engine runs, and report a C17-only failure as
   environmental. evidence: the same.

## F-e0b622aa — the Python suite failed 8 while another session was editing six_experts.py and its tests

Found by: the guard (R12.2-test-failed) on my `pytest` run at 15:30: "8 failed, 1139 passed" (1136 at my last commit).
The run right after printed no FAILED line. `git diff --stat` showed `six_experts.py` +84 and `test_six_experts.py`
+97 lines I did not write, plus changes to the guard's `traps.ts` and `SPEC.md`.

Whys:
1. Why 8 failures? The working tree held another session's unfinished edits to `six_experts.py` and its tests (my
   reading: the tests outran the code for a moment; the next run passed).
2. Why did my run see them? Both sessions work in place in one checkout, so my suite ran their half-made change.
3. Why did I run it then? I ran the full suite as the last check before a commit, without first looking at what
   changed in the tree that was not mine.
Source: instruction — I run the full suite in a shared working tree without checking for other sessions' edits first.
Root cause: a suite run over another session's unfinished work, counted as my failure.
Options:
1. [rule] Before a suite run that gates a commit, list the tree's changed files (`git status`); if files I did not
   change are modified, run the suite on my staged state in a temporary worktree instead. evidence: the C17 check on
   HEAD in a worktree gave a clean answer the same afternoon.
2. [tool] The pre-commit hook runs the suite on the index in a temporary worktree, the way it already builds the
   export from the index. evidence: `tools/git-hooks/pre-commit` lines 5–6.
