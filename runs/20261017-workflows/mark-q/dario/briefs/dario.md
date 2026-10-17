# Brief — answer one question

## The question

A decision in a time-boxed run (workflow-design method 3.8 item 14): the owner gave a time and is not asked until it
ends, so the main agent decides from your advice — provisionally; the owner accepts or declines it at the end.

Rules for this question:
- Keep the vision and the use cases in view: an option that serves no use case is wrong, however good.
- Rest each point on a measurement or a fact given below; a point you have only from memory is labelled *recall*, and
  recall alone does not decide.

Facts:
- **Vision / use case:** an agent cannot feel time pass, so the guard tells it: a one-line clock after every Bash or
  file-write call, and a time-up line after the deadline. The owner chose this over reminders at 50%, 80% and 100%,
  which "is not able to well predict, specific when exploring solutions" (2026-10-17); the reminders are removed.
- **What is left:** `bun .claude/skills/workflow-design/guard/src/cli.ts deadline wait [--mark P]` — a command the agent
  runs in the background as a timer; it sleeps until the deadline, or until P percent of it with `--mark P`, then
  prints the status line. It is not a reminder: nothing fires unless the agent starts the wait. The code is
  `.claude/skills/workflow-design/guard/src/cli.ts` (the `wait` branch of the deadline command).
- **The two readings:** (A) `--mark P` is a leftover of the removed marks and should go, leaving `deadline wait` to
  fire at the deadline only; (B) it is a separate timer the agent chooses for itself (for example to wake at 90% and
  write the report), and should stay.
- **Use in this project so far:** the time-monitor run used a plain background `sleep` as its timer, not `deadline
  wait`; no run has used `--mark` (measured: `grep -rn "deadline wait --mark" runs/` finds none).

The decision: keep `--mark P` on `deadline wait`, or remove it? Say what each choice costs and how we would know.

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
