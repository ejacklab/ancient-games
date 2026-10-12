# Brief — design the source of truth

You are designing **one thing**: the source-of-truth memory for a software project, as recommended in
`runs/20261011-project-memory-engines/RECOMMENDATION.md`.

## Read first — this is your evidence

- `runs/20261011-project-memory-engines/RECOMMENDATION.md` — the merged, verified recommendation (24 support rows,
  7 contested points). Read it. It is the source of the design, not your starting opinion.
- If you need a disagreement's full positions: `runs/20261011-project-memory-engines/nodes/claude.stdout.md`,
  `codex.stdout.md`, `opencode.stdout.md`.

## The design: answer these eight questions, in this order

1. **Why we need this memory.**
2. **Who it is for.**
3. **What it is for.**
4. **What will be put in.**
5. **What will not be put in.**
6. **Where it is put.**
7. **When it will be used.**
8. **When it will not be used.**

## Rules — this project's, non-negotiable

- **Ground every statement in the recommendation.** Cite the row, contested point or section you took it from,
  inline: `(M17)`, `(CP6)`, `(Write rules)`, `(Staleness and contradiction)`. A statement you add yourself is
  labelled `model knowledge` — never present your own addition as if the evidence said it.
- **Never fill a missing value with your own.** Where the recommendation does not decide a cap, threshold, count,
  filename or owner, do not invent one. Write instead:
  `OPEN: <exactly what must be decided, and by whom>`.
  A design with a blank is correct; a design with an invented number is wrong and will be rejected.
- **One maker per artifact.** For everything you say gets put in, say who writes it — agent or human — and who
  may change it afterwards.
- **Do not add sections. Do not restructure. Do not add phases, extra questions or a summary section.** The eight
  headings above are the whole document; put any `OPEN` item inside the question it belongs to.

## Output

Print the eight headings, in order, each with its content. Nothing before the first heading except a single
one-line title. Nothing after the eighth.

## Limits

One deliverable. Print the whole design to stdout. Write no files. Do not ask questions back.
