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
