# Review — the memory caches requirements (run 20261012-caches-requirements-review)

You are one of three independent reviewers. You do not see the others' reviews. **Change no files.** Print your
review to stdout.

All paths are relative to `/home/smoke01/dev/ancient-games`.

## What to review

Today the core requirements of the memory caches design were rewritten, and its vision was edited.

- **The design**: `runs/20261012-caches-requirements-review/inputs/CACHES.md` (a snapshot). The section under review is
  `## Core requirements`: Build (B1–B5), Keep (K1–K3), Read (Rd1–Rd4). Each requirement names its source — (v) the
  vision, (d) this document's text, *proposed* for wording the owner has not decided — and has a **Fails if** check.
- **The vision** it must serve: `runs/20261012-caches-requirements-review/inputs/caches-vision.md`.
- **What changed today**: `runs/20261012-caches-requirements-review/inputs/changes-since-HEAD.diff` (against the last
  commit, where the requirements were a flat list R1–R9 that the owner had accepted).
- **Evidence the ids point to**: `S-F*` in `runs/20261012-memory-caches/nodes/sqlite-fts.claude.md`; `V-F*` in
  `runs/20261012-memory-caches/nodes/vector.claude.md`; `G-F*` in
  `runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md`; `M*` in
  `runs/20261011-project-memory-engines/RECOMMENDATION.md`; `BM-*` in `runs/20261012-caches-routing/bench/results.md`.
- **The sibling design** the caches sit inside: `docs/memory-system/SOURCE_OF_TRUTH.md`.

Scope decided by the owner today: the caches are **two** indexes over the markdown memory (full-text and vector). The
code graph was moved to its own project (`docs/code-graph/`); it is **not** in scope, except as leftover text that
should no longer be in the requirements.

## Judge each requirement on

1. **Checkable.** Can its *Fails if* actually fail? Name one concrete case that breaks it, or say it cannot fail.
2. **One thing.** Does it describe one event, or two that should be split?
3. **Units and weak words.** Does every comparison say what it counts? Any vague word (enough, about, period, once)?
4. **Source.** Is the label (v / d / proposed) right? Open the cited id: does the source say what is claimed?
5. **Consistency.** Does it contradict the vision, another requirement, or other text in `CACHES.md` (the rules, the
   5W1H tables, the routing tables, the example numbers)? Quote both lines.
6. **Gaps.** What must be true for the caches to work that no requirement says? Do not invent numbers; say what is
   missing.

## Print exactly these sections

### Verdict
One line: ACCEPT, REPAIR or REJECT, and why.

### Findings
One per item, most severe first. For each: the requirement id (or `CACHES.md:<line>`), what is wrong, the line or
source that shows it (quoted), severity (high, medium, low), and a proposed fix in one or two sentences.

### Gaps
Requirements that are missing, each with why it is needed.

### What holds
The requirements you checked and found sound, one line each.

### Not checked
What you did not open or could not verify.
