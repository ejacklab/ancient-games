# Linus Torvalds — Memory requirement wording

## Answer
CHANGE. Unlisted wording stands.

- **W5.2 — text**

  Current: “Written at the end of a task: other lessons, observations and hypotheses.”

  New: “At the end of a task, record other lessons, observations and hypotheses, if any.”

  **W5.2 — `fails_if`**

  Current: “a task ends with what it learned unwritten, with no written reason.”

  New: “a completed task has neither a written record of other lessons, observations and hypotheses, a statement that there are none to add, nor a written reason in the task's state.md for omitting the record.”

- **K5.1 — `fails_if`**

  Current: “a journal file is edited after it is written, or raw notes are kept elsewhere, with no written reason.”

  New: “a line already written in a journal is changed or removed, or raw notes are kept elsewhere, with no written reason in the task's state.md.”

- **Rd5.2 — `check`**

  Current: “reviewer”

  New: “reviewer; only on transcript audit”

- **W1.2a — `fails_if`**

  Current: “a header is not between two `---` lines.”

  New: “the file's first line is not exactly `---`, or the header does not end at the next line that is exactly `---`.”

- **K1.1 — `who_decides`**

  Current: “the project's workflow: when work goes the other way”

  New: “the project owner, through the project's workflow: when work goes the other way”

## Why
- **My #18:** W5.2 becomes reviewable from written evidence. Price: a task with nothing to add needs a short statement; this still cannot prove that every lesson was recorded.
- **My #10:** K5.1 permits the append operation its text requires, resolving the contradiction identified in the supplied Dave Q2 finding. Price: checking it requires comparing existing lines.
- **My #7:** Rd5.2 names the evidence its check needs, following the supplied Dave Q2 finding. Price: without a transcript audit, compliance remains unverified.
- **My #18:** W1.2a's failure condition now covers the first-line requirement. Price: the tool must check placement as well as delimiters.
- **My #4:** K1.1 assigns the decision to an accountable person, following the supplied Dave Q2 finding. Price: the owner must establish the workflow's direction.

## What I need to know
None for these wording corrections.