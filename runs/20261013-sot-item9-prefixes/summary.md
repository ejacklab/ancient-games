# Summary — readers on item 9, the O-/H- prefixes

COO (Claude `claude-opus-5-5`), 2026-10-13. Three reports: `reviews/claude.md`, `reviews/opencode.md`, `reviews/agy.md`.
**codex produced nothing:** *"You've hit your usage limit … try again at 2:00 AM"* (`reviews/codex.stderr.txt`).

## All three recommend the same

**Confirm `O-` observation and `H-` hypothesis.** Each of the five kinds then has one letter, its initial (D, F, L, O,
H, with no clash), and the prefix must match the entry's `kind`. Dropping prefixes was considered and rejected by
claude and opencode: it is a bigger change, and the prefix is the only place that shows an entry's kind without opening
the file.

**Their reasons (quoted):**
1. The kinds are already settled. The vision has *"lessons, observations and hypotheses"* and W2.2 defines all three,
   so one rule for all five needs no exception.
2. `H-` keeps a guess labelled wherever the file name shows: listings, `git log`, links. The design leans on that
   label: *"Guesses not labelled as a hypothesis"* are kept out, and W2 fails *"a guess recorded under any kind but
   hypothesis"*. opencode adds, honestly, that the case for `O-` is weaker: it is cheap rather than important.
3. Nothing to build. The `INDEX.md` draft already reads `^[DFLOH]-`, and the script already maps O and H.

**The edits:**
- W1.1 lists five prefixes and adds *"the prefix matches the entry's `kind`"*.
- W1's check adds *"a file whose prefix is outside the five or doesn't match its `kind`"*.
- The layout's `entries/` line lists all five, and the "proposed in W1.1" sentence goes.
- `docs/index-md/REQUIREMENTS.md` B1.1 drops its "proposed" hedge.

## One question (claude and opencode, the same)

When an entry's kind changes (a hypothesis is confirmed, or an observation turns out to be a fact), is it **a new
entry that supersedes the old one**, or **the old file renamed**? Both recommend the new entry. Renaming breaks links
and meets merges badly, and K4.1 already provides "superseded". This would be one sentence in W1.1: *an entry's kind,
and so its prefix, never changes; a change of kind is a new entry that supersedes the old one.*

## Outside this item

- **The built script still accepts runbooks.** `tools/memory_index.py` (built by the other session) still maps
  `R` → runbook, and opencode confirmed that an `R-` file passes `--check`. This is a leftover from item 8, in the
  build session's files, and not the COO's to edit.
- **agy:** should unconfirmed hypotheses be left out of `INDEX.md` to save space? That is a new question about the
  index, not about prefixes.
