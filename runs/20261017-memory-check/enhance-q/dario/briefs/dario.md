# Brief — answer one question

## The question

# Question — what should memory-check v1 improve next?

The owner (EJ) asked for the tool to be researched, implemented, reviewed, tested and enhanced. It is built and
tested; this is the enhance step. Your advice is ranked; the main agent applies the top of it. The owner decides.

Rules for this question:
- Every improvement you propose names the use case (U1–U6 in `memory_check/USE_CASES.md`) or the vision line
  (`memory_check/VISION.md`) it serves, and the case that shows it is needed now. An improvement that serves none is
  not proposed: the owner wants less work, not more.
- Rest each point on a fact below (each with its source) or one you check in this repository; a point from memory
  only is labelled *recall*.

## Facts
- The tool: `memory_check/src/` (12 modules; `cli.ts` is a launcher, the command is `command.ts`); its docs
  `memory_check/{AGENTS,VISION,USE_CASES,REQUIREMENTS}.md`. Source: those files.
- Tests: `memory_check/test/acceptance.test.ts` (55, written by Codex from the spec) and `memory_check/test/review.test.ts`
  (15, one per review finding); `cd memory_check && bun test` gives 70 pass, 0 fail. Source: `bun test`, run at 18:4x.
- The review's 14 findings and their fixes: `runs/20261017-memory-check/nodes/review.codex.md`,
  `runs/20261017-memory-check/nodes/fix-2.result.md`. Source: those files.
- The report on this repository (which has no `project-memory/`): `runs/20261017-memory-check/nodes/smoke-report.md`;
  `--warn` prints nothing and exits 0. Source: the smoke run.
- Not built yet: the session-start hook (needs the owner's yes to a settings diff); no real project with
  `project-memory/` has been checked — fixtures only. Source: `memory_check/REQUIREMENTS.md` R2, `design-decisions.md` 15.

## The decision
Rank at most five improvements, most valuable first. For each: what it is, the use case or vision line it serves,
the case that shows it is needed, and how to check it is done. Then name anything in the tool you would remove or
simplify, with the same reasoning. End with your top three in three lines.

## How to answer

Answer the question as well as you can. If the answer depends on something you were not given, list it under "What I
need to know" and answer conditionally. Write in plain English Markdown. Refer to EJ as they/them. Do not write files;
your final message is the answer.

## Write exactly this (no preamble)

# Answer — <the question in a few words>

## Answer
<your recommendation in one or two sentences>

## How I decided
<numbered steps>

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each risk or price>

## How we would know I was right
<a test, a measure, or an observable result>
