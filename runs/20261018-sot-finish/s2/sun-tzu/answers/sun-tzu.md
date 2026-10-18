# 孫子 (Sun Tzu) — Wording the memory requirements

## Answer

CHANGE

- **W5.2** — `text`: "Written at the end of a task: other lessons, observations and hypotheses." → "At the end of a task, the agent that did it records the task's other lessons, observations and hypotheses in the task's journal."
  `fails_if`: "a task ends with what it learned unwritten, with no written reason." → "the task's journal does not record the task's other lessons, observations or hypotheses, with no written reason."
  `check`: `reviewer` → `reviewer; the K5.2 journal-read log line`.
- **K5.1** — `text`: "Both hold raw notes, one file per agent session, appended to and never edited." → "Both hold raw notes, one file per agent session, appended to; a line already written is never changed or removed."
  `fails_if`: "a journal file is edited after it is written, or raw notes are kept elsewhere, with no written reason." → "a line already written is changed or removed, or raw notes are kept elsewhere, with no written reason."
- **Rd5.2** — `check`: `reviewer` → `reviewer; only on audit`. Text and `fails_if` unchanged.
- **K1.1** — `who_decides`: "the project's workflow: when work goes the other way" → "the project owner, through the project's workflow: when work goes the other way".

Everything else stands: **W6.1a, Rd1.1, W1.2a, W1.2b, K5.2**.

## Why

- my #1: I compared each record on whether its check can see what it claims to check — W1.2a, W1.2b, W6.1a, Rd1.1 and K5.2 pass; W5.2 and Rd5.2 did not.
- my #10: strike the empty, not the solid — Dave's read found K5.1's "never edited" contradicts "appended to"; an append is a change in the diff, so say "a line already written is changed or removed" (price: the check now reads line-level diffs, not file-level).
- my #16: an order must name actor and observable — W5.2's text names neither, so I name the agent, the journal and the K5.2 line (price: the reviewer can see the line exists, not that the lesson is complete).
- my #13: a document cannot decide — K1.1's decider becomes the project owner through the workflow (price: the owner carries a decision the workflow cannot).
- my #4: a MUST checked only from a transcript still gates, but late — Rd5.2 keeps MUST and gains "only on audit" (price: it does not stop the act); the rest stand whole (my #3).

## What I need to know

- Is "entry" in W6.1a defined to exclude journal session files? If not, W6.1a's "never append" clashes with K5.1's "appended to", and W6.1a needs "other than journal session files".
- In the target repo, does `CLAUDE.md` only import `AGENTS.md`? If it carries its own instructions, Rd1.1's parenthetical is false and I would change it to "`AGENTS.md` and `CLAUDE.md` at the repo root, one importing the other".
- Is `reviewer; only on audit` a check value the YAML accepts? If not, keep `check: reviewer` and write "only on audit" into Rd5.2's text.
