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
