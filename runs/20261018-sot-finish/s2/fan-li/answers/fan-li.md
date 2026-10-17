# 范蠡 (Fan Li) — Wording written into memory requirements

## Answer
CHANGE

- **K1.1** `who_decides`:
  - Exact current words: `the project's workflow: when work goes the other way`
  - Exact new words: `the project owner, through the project's workflow: when work goes the other way`

- **K5.1** `fails_if`:
  - Exact current words: `a journal file is edited after it is written, or raw notes are kept elsewhere, with no written reason.`
  - Exact new words: `a line already written is changed or removed, or raw notes are kept elsewhere, with no written reason.`

## Why
- K1.1 must assign the choice to the project owner rather than the workflow, because authority belongs to a person and not an inanimate document (my #14); the price is that exceptions must wait for owner intervention (my reading).
- K5.1 must penalize changing or removing written lines rather than any edit, because git marks appends as edits and regulating affairs requires mechanisms that match reality on the ground (my #2, my #18); the price is more detailed diff verification (my reading).
- Rd5.2 stands unchanged because instructions established at court must never be overthrown by memory read on the spot (my #5); the price is that agents cannot unilaterally route around stale instructions (my reading).
- The remaining records stand because distinct files, standard layouts, and reader extraction regulate affairs cleanly (my #2, my #14); the price is managing multiple files and trusting reader judgment (my reading).

## What I need to know
Whether EJ intends the project workflow to decide automatically when work goes the other way: if so, K1.1 should name an automated tool check instead of the project owner.
