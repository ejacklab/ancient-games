# Round 1 — review two versions of one design (run 20261012-caches-merge)

You are one of three independent reviewers. You do not see the others' reviews in this round. Change no files, and
print your review to stdout.

## The two versions
Both versions design the same thing: three optional caches over a project's markdown memory and code (SQLite
full-text, a vector index, a code graph), and **when an agent should use which**, so that development and testing are
faster and cheaper in tokens.
- **Version A**: `runs/20261012-caches-merge/inputs/version-A.md`. Its evidence and run record are under
  `runs/20261012-caches-enhance/`, including `DECISION-RULES.md` and `nodes/`.
- **Version B**: `runs/20261012-caches-merge/inputs/version-B.md`. Its evidence and run record are under
  `runs/20261012-caches-routing/`, including `bench/results.md`, `nodes/runtime-recall.json` and
  `vision-proposals.md`.
- **The vision both must respect**: `docs/memory-system/vision-statements/caches-memory-vision-statements.md`.
- **Earlier research** both cite (ids `S-F*`, `V-F*`, `G-F*`): `runs/20261012-memory-caches/nodes/`.

The paths are relative to `/home/smoke01/dev/ancient-games`.

## Judge both versions on
1. **Correctness.** Do the claims and numbers match their cited sources? Open the sources to check.
2. **Coverage.** Which real questions does each version route? Consider both memory-entry questions and
   development/testing questions about code and docs.
3. **Evidence strength.** Is each claim measured or reasoned? How large is n? Who wrote each check?
4. **Vision fit.** Are the never-rules kept, and is every conflict with the vision left to EJ?
5. **Usability.** Can an agent pick the right store for its question in one lookup?

## Print exactly these sections
### Strengths of A
### Strengths of B
### Errors and weaknesses
Give each one as `A:<line>` or `B:<line>`, then what is wrong, the source line that shows it, and a severity (high,
medium or low).
### Conflicts between A and B
For each: what A says, what B says, which is better supported and why, with sources.
### Proposed merged outline
List the sections of the best version in order. For each, say: take from A, take from B, combine both, or new text
needed (and why).
### Not checked
