# Brief, stage 2 — read all three reviews, propose one algorithm

Stage 1 is done. Three researchers (claude, codex, opencode) each wrote an independent literature review on how
to generate `INDEX.md` for the design in `/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md`.
One of them is yours.

## Read, in full

- `/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md` (the design; see K6, Rd1–Rd3, W6)
- `/home/smoke01/dev/ancient-games/runs/20261012-index-md-algorithm/lit-review/claude.md`
- `/home/smoke01/dev/ancient-games/runs/20261012-index-md-algorithm/lit-review/codex.md`
- `/home/smoke01/dev/ancient-games/runs/20261012-index-md-algorithm/lit-review/opencode.md`

A review that is empty or missing is noted as such; work from the others.

## Your task

Write **one** proposal: a single algorithm for generating `INDEX.md`. Not a menu of options.

- **The algorithm** as numbered steps, precise enough that someone could write the script from it: what it reads,
  what it writes, in what order, when it runs and what runs it, what happens in git, what happens when the index is
  too big, and how anyone checks it is in step.
- **Exactly 3 supporting reasons.** Each cites finding ids from any of the three reviews (e.g. `X4`, `C2`).
- **Exactly 6 must-not-dos.** Each is a thing the script or its users must not do, with the finding id that shows why.
- **Design changes:** if your algorithm needs any requirement in `SOURCE_OF_TRUTH.md` to change (for example Rd1.2 or
  K6), name the requirement and the change. If none, say "none".
- **Where you disagree with the other reviews**, in one short list.

Keep the design simple: the owner's rule is that memory is simple, and a mechanism that is not needed is removed.
Read only; do not change any file in the repo.

## Output — one markdown report

```
# INDEX.md — proposal (<your engine name>)

## The algorithm
1. …

## Three supporting reasons
1. … (findings: …)
2. …
3. …

## Six must-not-dos
1. … (finding: …)
…
6. …

## Design changes

## Where I disagree with the other reviews
```

The launcher tells you your engine name and where the report goes.
