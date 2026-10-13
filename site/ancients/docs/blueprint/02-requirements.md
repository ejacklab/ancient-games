Status: settled (accepted by EJ on 2026-10-13)
Drawn from: 01-vision.md. Every requirement here is a proposal by Claude from EJ's words; none is settled until EJ
accepts this file. Ids are cited by tests and nodes — never renumber.

### R1 — Four people on one page
The page shows the four seats, one panel each.
Acceptance criteria:
- R1.1 Loading `/` shows exactly four person panels, in this order: 范蠡, 孫子, 老子, Linus Torvalds.
- R1.2 Each panel shows the person's name, a "who they are" text, and every item of that person's final list; each
  item shows its kind, rule, their words, source and label. The test compares the count and the text of every item
  with `content/ancients.json`.
- R1.3 Each person's items are their own **mindsets, decision rules and algorithms** (EJ, 2026-10-13: "also include
  their own mindsets, decision making rules and algorithms"). Every item shows its kind — mindset, decision rule or
  algorithm — as a visible tag, and the top of each panel shows how many of each kind that person has (for example
  "3 mindsets · 15 decision rules"). Items stay in their list's order, which is ranked by importance.

### R2 — Left and right change the person
Acceptance criteria:
- R2.1 A horizontal touch swipe across the middle of a panel (test: from 80% to 20% of the width, at half the height)
  moves to the next person and the panel snaps fully into view; the reverse swipe moves back. A swipe on the first
  person to the right, or on the last to the left, stays put.
- R2.2 The current person's name and "n / 4" are visible at the top at all times.
- R2.3 Tapping a person's dot at the top jumps to that person.

### R3 — Up and down read the person
Acceptance criteria:
- R3.1 Scrolling vertically inside a panel moves the text and never changes the person.
- R3.2 Each person keeps its scroll place: scroll person 1 down, swipe to person 2 and back — person 1 is where it was.

### R4 — The Kindle look
Acceptance criteria:
- R4.1 An "Aa" button opens a menu with the `kindle-page` choices: font (Literata, Georgia, Sans, Hyperlegible), size,
  spacing (compact, normal, loose), margins (narrow, normal, wide), alignment (justify, left), page colour (white,
  sepia, green, black). Each choice changes the page at once.
- R4.2 After a reload, the chosen settings, the current person and each person's scroll place are restored.
- R4.3 No panel scrolls sideways inside itself: for every panel, its content is no wider than the panel (tables and
  code wrap or scroll inside their own box).
- R4.4 Each panel has a Kindle-style footer showing the % of that person read.

### R5 — Exact quotes
Acceptance criteria:
- R5.1 Every "their words" text on the page equals its field in `content/ancients.json` (after HTML rendering of the
  same Markdown).
- R5.2 `tools/check_content.py` passes: every field of `ancients.json` is copied verbatim from its source list, and
  every Chinese quote is found in `runs/20261013-four-seats/sources/`.

### R6 — Rebuild with one command
Acceptance criteria:
- R6.1 `make -C site/ancients` rebuilds `content/ancients.json` checks, `dist/index.html`, and runs the mobile tests;
  it exits 0 only if all pass.
