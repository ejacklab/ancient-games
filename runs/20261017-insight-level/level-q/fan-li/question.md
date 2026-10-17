# Question — at which level does an insight belong?

The owner (EJ) is asking you for advice; the owner decides.

Rules for this question:
- Rest each point on the data below: cite insight ids or headings from `runs/20261017-insight-level/insights.md`.
  A point you have only from memory is labelled *recall*, and recall alone does not decide.
- Say "I don't know" where the data does not answer; do not invent facts.

## Background
In this project every failure an agent makes gets an insight: six whys down to a source that can be changed (an
instruction, a check, a tool, a config), the root cause, and two or three fix options; the owner chooses the fix
(`docs/HARNESS_REQUIREMENTS.md`, R12.3). Today each insight is filed in the run folder where the failure happened
(`runs/<run>/insight.md`). The owner wants insights filed where they will be learned from, and said the most important
ones are code insights and testing insights, which "can improve an ai agent quality a lot and reduce noise".

Two levels were discussed: **project level** (about this project's code, tools or conventions; any agent working here
could hit it) and **agent-type level** (about a kind of agent — the main Claude agent, opencode, Codex, agy, mcode —
which follows it into any project).

## The owner's hypothesis, verbatim
> "are we able to fast eval using programming it is a AI Agent programming issue or a project level one. when I typing
> this i feel , is there even a project level insight, except those project requirement issues, else should be task
> or agent type level"

## Data
- `runs/20261017-insight-level/insights.md`: all 56 insight sections in the repo, each with its own `Source:` and
  `Root cause:` lines, extracted verbatim by a script the main agent wrote (`extract.py`, same folder).
- The guard's journal holds 52 failure records. Each has an `engine` field: opencode 7, claude 4, claude-subagent 1,
  codex 2, "pytest" 1 (a mislabel: a test runner, not an agent), and "none" 37 — the main agent's own failures, run in
  Claude Code (`harness: claude-code`). The field names who failed, not who should learn: in F-7f938bdf opencode failed
  because the main agent's brief sent it to a file outside the repo.
- Each insight's `Source:` is one of instruction, check, tool, config: where the fix goes, not who learns it.

## The decision
1. Is the owner correct: apart from project requirement issues, is every insight task level or agent-type level, with
   no other project-level insight? Say what "task level" means in your reading, and give the insight ids that support
   or break the hypothesis — at least one each way if the data has them.
2. Can a program sort an insight into its level quickly and reliably? If yes: from which fields, by what rule, and
   which of the 56 it would get wrong. If no: what the insight would have to record so that it could.
