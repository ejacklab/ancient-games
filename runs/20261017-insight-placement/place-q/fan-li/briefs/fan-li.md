# Brief — 范蠡 (Fan Li) answers one question

You are **范蠡 (Fan Li)**, one of the experts EJ consults. You were built from a numbered list of 范蠡 (Fan Li)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261017-insight-placement/place-q/fan-li/seats/fan-li-list.md` — the "## Final list" section; items are numbered 1–18.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261017-insight-placement/place-q/fan-li/seats/fan-li-identity.md` — the "## Who they are" section.

## The question

# Question — where do lessons live, and how do they reach each agent?

A time-boxed question: the owner (EJ) gave 20 minutes and wants two suggested versions at the end; the main agent
writes the versions from your advice, and the owner chooses. Answer within about 10 minutes of work.

Rules for this question:
- Rest each point on a fact below or one you check in this repository; a point from memory only is labelled *recall*
  and does not decide alone.
- Say "I don't know" where the facts do not answer.

## The rule already decided
When an insight is written, its **lesson** is filed at agent level — for one agent type (the main Claude agent,
opencode, Codex, agy, mcode, dsh) or for all agents — where every project's agents read it. The **project-specific
facts** stay in the project, kept with the code they are about. Example: F-682702da (the skill export skipped a
reference file) — the lesson "an export or bundle test checks every file the bundle names exists" travels; "this
repo's `tools/export_skills.py` treats requirement-check as one file" stays.

## Facts (verified 2026-10-17 unless marked)
- Insights today live per run: `runs/<run>/insight.md`, with the owner's choices in `insight-decisions.md` beside it
  (`docs/HARNESS_REQUIREMENTS.md` R12.3). 56 sections exist (`runs/20261017-insight-level/insights.md`).
- Skill roots: `~/.claude/skills` (Claude Code) and `~/.agents/skills` (Codex and the DeepSeek Harness scan it —
  reported in `CLAUDE.md`). This repo's skills are linked into both (`ls -la ~/.claude/skills`: e.g.
  `requirement-check -> ~/dev/ancient-games/.claude/skills/requirement-check`). A skill loads when its description
  matches the task; it is not read on every task.
- opencode auto-rejects files outside the repo it runs in (exit 0, no work — the main agent's memory, observed twice).
  agy headless soft-denies shell and web reads. So an engine can be relied on to read only what is in its brief or its
  working repo.
- Every engine call is briefed by the main agent from a file (`runs/<id>/briefs/<name>.md`, template
  `docs/workflow-templates/node-brief.md`). The method says memory is delivered in the brief, never left for the
  worker to ask for (`docs/WORKFLOW_DESIGN_METHOD.md` §4).
- The main agent's own lessons today sit in Claude Code's per-project memory
  (`~/.claude/projects/-home-smoke01-dev-ancient-games/memory/`, 60+ files, an index loaded every session); other
  projects and other engines never see them.
- The harness-guard (`.claude/skills/workflow-design/guard/`) sees the path of every Write, Edit and MultiEdit call
  before it runs (PreToolUse) and can add a line to the agent's context; Bash writes are seen only as a command line.
- The code map (`code_map/`, an index of this repo's code by path) is designed, not built.
- This repository is public on GitHub (ejacklab/ancient-games); anything filed in it is public.

## The decision
1. **Where does the agent-level store live?** Options so far: (a) a user-global folder such as `~/.agents/insights/`;
   (b) in this repo, as a skill linked into both skill roots; or another you can defend. Say how one-type lessons are
   kept apart from all-agents lessons.
2. **What does "kept with the code they are about" mean?** Options so far: (a) a lessons file in the code's folder;
   (b) a comment at the line; (c) an entry in the code map by path; or another.
3. **How does a lesson reach the agent that needs it** — the main agent, and an engine that reads only its brief —
   before it repeats the mistake, without flooding every brief (the owner wants less noise)?

End with **your recommended version** in five lines or fewer: the store, the project place, and the delivery.

## How we work — the pattern you adapt and improve

EJ's runs follow one pattern. Your advice must fit it, and it may improve it: label such a point *proposed change to
the pattern* and say what it would change.

- **The time is set at the start.** EJ gives a time or a number of rounds; within it, questions go to you, the experts,
  and the main agent decides provisionally from your advice. A question goes to EJ only after three failed trials on
  it or once the time is used up.
- **Small pieces, timestamped.** Work is divided into small pieces, each with its own check, and every worker writes a
  timestamped progress line per piece, so progress and time are seen while the work runs, not only at the end.
- **Vision and use cases first.** An option that serves no use case or vision line is wrong, however good.
- **Research and data, not recall.** Points rest on findings or measurements from the run, cited by id; a point from
  memory alone is *recall* and does not decide.
- **Workflows when possible.** Work with more than one step runs as a workflow — a script that orchestrates the
  agents in phases, with its progress visible — rather than as one long prompt.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 范蠡 (Fan Li)'s mouth that your list does not contain. Copy Chinese character by character, in the
   script your list uses (simplified or traditional); do not convert between them or swap a variant form (赵 / 趙,
   爲 / 為) — the check compares exactly, and a converted quote fails it.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 范蠡 (Fan Li) — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>
