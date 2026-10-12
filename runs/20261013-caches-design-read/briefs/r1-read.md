# Round 1 of 3 — read the memory caches design (run 20261013-caches-design-read)

You are one of four independent readers. You do not see the others' work in this round. **Change no files.** Print
your report as your final answer.

All paths are relative to `/home/smoke01/dev/ancient-games`.

## What you read

- **The design**: `runs/20261013-caches-design-read/inputs/CACHES.md` — read all of it.
- **Its vision**: `runs/20261013-caches-design-read/inputs/caches-vision.md`.
- **What changed since the last review**: `runs/20261013-caches-design-read/inputs/changes-since-review.diff`.
- **The last review**, for context only: `runs/20261012-caches-requirements-review/reviews/synthesis.md`. Its points
  were already applied or decided; do not raise them again unless the current text still gets them wrong.
- **Evidence the ids point to**: `S-F*` in `runs/20261012-memory-caches/nodes/sqlite-fts.claude.md`; `V-F*` in
  `runs/20261012-memory-caches/nodes/vector.claude.md`; `G-F*` in
  `runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md`; `M*` and `CP*` in
  `runs/20261011-project-memory-engines/RECOMMENDATION.md`; `BM-*` in `runs/20261012-caches-routing/bench/results.md`.

The design and its requirements (Build / Keep / Read: B1–B5, K1–K3, Rd1–Rd4) are accepted by the owner, EJ.

## Scope and the owner's rules

- **Caches only.** The caches are two indexes over the markdown memory: full-text and vector. The code graph is a
  separate project and is out of scope, except as leftover text that should no longer be here.
- `docs/memory-system/SOURCE_OF_TRUTH.md` is a **different design**. Read it for context if you need to, but propose
  no change to it.
- **The bar is that nothing in the design misleads.** Do not propose splitting a requirement into smaller ones.
- **Do not invent numbers.** A trigger is a comparison that measurement decides, not a threshold.

## Your task

1. **The changes since the last review** (see the diff): the question log was replaced by misses noted in the journal
   and a question set built per comparison (Rd4, B1.1, B1.2, K3); K3 lost its rebuild-cost part; B4 no longer stores
   `status`; the full-text trigger is the B1.1 comparison; Part 2 and the code-graph section moved out. Are these
   sound, and is every requirement that depends on them still consistent?
2. **Every section outside "Core requirements"** — The answer first, When to use which store (Part 1), Rules for every
   cache, SQLite full-text index, Vector index, Measured here, Example numbers by case, What this changes elsewhere,
   Not known, Unresolved after review. Does any line contradict the accepted requirements or the vision, cite a source
   wrongly, or still describe something removed (the code graph, the question log, the `INDEX.md` size trigger, the
   rebuild cost)? Quote it.
3. **The "Unresolved after review" table**: for each row, is it still open, settled by something now in the design, or
   no longer relevant?

## Print exactly these sections

### Verdict
One line: CLEAN or REPAIR, and why.

### Findings
One per item, most severe first. Each: the location (`CACHES.md:<line>` in the snapshot, or a requirement id), the
quoted text, why it misleads or is wrong, the source line that shows it (quoted), severity (high, medium, low), and a
fix in one or two sentences.

### Unresolved table
One line per row: still open / settled (by what) / no longer relevant (why).

### What holds
The sections you read and found sound, one line each.

### Not checked
What you did not open or could not verify.
