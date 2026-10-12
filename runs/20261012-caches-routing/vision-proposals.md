# Proposed changes to the caches vision, for EJ

The vision is `docs/memory-system/vision-statements/caches-memory-vision-statements.md`. It is EJ's, so it has not been
edited. Below are three proposals that come from the measurements in `bench/results.md` (ids `BM-*` in `CACHES.md`).
Each says what the vision says now, what the measurements show, and the wording that would follow. Accept, change or
reject each one.

## P1: who it is for

- **Now:** "An agent retrieving an entry on demand."
- **Measured:** the questions that cost tokens during development and testing are about code and docs: where X is
  defined, what calls X, which tests to run, why we decided X. On those, full-text search and the graph print far
  less before naming a right file (BM-1, BM-3, BM-4, BM-6; a proxy for tokens, not a token count).
- **Proposed:** "An agent developing or testing this project, retrieving memory entries, code or docs on demand."

## P2: "None of them is needed today"

- **Now:** "None of them is needed today."
- **Measured:** for memory entries this still holds: `project-memory/` does not exist. For code and docs (490 files
  here), full-text prints about a sixth of grep's characters before naming a right file (BM-6; a proxy, not tokens), and the graph names
  callers and test reach in tens of characters (BM-1, BM-3, BM-7).
- **Proposed:** "For memory entries, none is needed until its trigger fires. For code and docs, full-text and the
  code graph are worth having now. The vector index is not, on this evidence (BM-1, BM-7)."

## P3: what an empty answer means

- **Now:** not stated.
- **Measured:** the graph returned nothing for tests that run the code as a separate process (BM-8). Read as "no
  tests", that would skip tests that exist.
- **Proposed**, as a new never-rule: "It never treats an empty answer as proof of absence: an empty answer means *not
  seen*, and the agent falls back to the files."

## What stays as written

The never-rules, unchanged:
- never the source of truth;
- never patched;
- never read at session start;
- never a second thing to keep in sync.

The "How we know it works" test is also unchanged; this run's determinism check is that test (0 differences in 180).

## Limits on this evidence

- The numbers come from one repo and 40 questions, with n = 6 to 10 per category.
- Token cost is measured as characters read, a proxy, not as tokens.
- The harness repair was not re-audited.
