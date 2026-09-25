# Prompt — <short name>

For a small task: up to 3 steps, nothing unclear except decisions that have a default answer. No workflow needed.

## Questions for EJ (leave out if there are none)

The steps below are written on the provisional assumptions. Answer only where the assumption is wrong — except
questions marked "must answer": they are blueprint questions, and no step that builds runs until EJ has answered them.

| # | Question | Provisional assumption | Must answer before building? |
|---|---|---|---|

## Task

<one or two sentences: what to do>

## Steps

1. <one action with a result that can be checked>
2. <…>
3. <…>

## What you need

<the exact files to read, tools to use, skills that apply — nothing else>

## Off limits

<paths and things this task must not change; the check confirms it, e.g. `git status --short` shows changes only in
the listed paths>

## The check

<how we know it is done. Best: a command and the result it must give.
For a product change: the acceptance criteria in scope (R1.1, …) and how each is checked, plus: the baseline (the
test command, run before the change) still passes, and nothing off limits changed. Anything else found goes to
docs/blueprint/backlog.md.>

## Independent check (only if the task is tiny but risky)

<what a second agent, who does not see your reasoning, must verify before this counts as done.
Risky means: a mistake would be noticed late, cannot be undone, or touches many things.>
