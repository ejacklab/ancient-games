I'll read the brief first.
# 老子 (Laozi) — Approve or change the COO's memory requirements

## Answer

**CHANGE** — four records. (I did not open the YAML; the brief gives each record's words as read from it.)

**W5.2** (`fails_if`)
- current: *"a task ends with what it learned unwritten, with no written reason."*
- new: *"a task ends with no end-of-task entry, with no written reason."*
- cost: it no longer catches the task that writes an entry and learns nothing; the reviewer catches that, not the fails_if.

**K5.1** (`fails_if`)
- current: *"a journal file is edited after it is written, or raw notes are kept elsewhere, with no written reason."*
- new: *"a line already written in a journal file is changed or removed, or raw notes are kept elsewhere, with no written reason."*
- cost: none. The record's own text — one file per session, appended to, never edited — already says this; only the fails_if was inverted.

**Rd5.2** (`check`; the text stands)
- current: `check: reviewer`
- new: `check: reviewer, on audit only`
- cost: the gate then passes every ordinary run unexamined; the guarantee is real only if audits actually happen.

**K1.1** (`who_decides`)
- current: *"the project's workflow: when work goes the other way"*
- new: *"the project owner, through the project's workflow: when work goes the other way"*
- cost: if the owner is away and has named no stand-in, the decision is unmade rather than wrongly made.

**APPROVE as they stand:** W6.1a, K5.1's shape, Rd1.1, W1.2a, W1.2b, K5.2.

## Why

- Four records ask a check to know what no check can know; a rule gripping what it cannot hold loses it (my #4), and the honest form is one that says when it is looked at (my #8).
- K5.1's fails_if fires on the very behaviour its own text requires, which is the reversal the Way moves by (my #4, my #11).
- The raw journal is where things settle: notes rest there, and the taking away happens later, at the entry (my #15, my #1).
- K1.1 gives deciding to a document, and a document that decides must act on the decision (my #4, my #19).
- W6.1a, Rd1.1, W1.2a, W1.2b and K5.2 are already the small, decided thing — done while it is easy, closed once (my #6, my #2, my #3).

## What I need to know

- Who reviews when EJ is away — if no stand-in is named, K1.1's new words leave a decision unmade; the answer would change back if the run already names one.
- Whether the `check` field has a closed vocabulary: if an "audit only" qualifier cannot be written, Rd5.2 needs a new value, not a qualifier.
- What marks the moment W5.2's new fails_if fires (task closed in `state.md`?) — with no trigger, an absent entry is never noticed.
- Whether a header field may hold a line exactly `---` in W1.2a; if yes, that record needs the escape named, if no it stands.
