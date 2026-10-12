# Merge — write the best version from Versions A and B (run 20261012-caches-merge)

You are the merger. You did not write either version, and you did not review them. Below you have:
- Version A and Version B, both in full;
- three independent round-1 reviews of them, by agy, codex and opencode;
- the same three reviewers' round-2 discussion.

Write the **best version**: one document that keeps the strengths of both.

## Rules
1. **Follow the reviewers' agreement.** Where the round-2 reviews agree on an outline or a point, follow it. Where
   they still disagree, do not pick silently. Add the point as a row in a final section, **Unresolved after review**,
   with each reviewer's position.
2. **Reuse the versions' own text.** Copy whole sections or table rows from A or B wherever possible. Write new text
   only to join them, and keep it short.
3. **Invent nothing.** Every number, finding id (`S-F*`, `V-F*`, `G-F*`, `BM-*`, `M*`, `D*`, `R*`) and claim must
   appear in A or in B exactly as written there. Do not add a number. Do not round a number differently.
4. **Keep the labels** a source attaches to a claim: *my reading*, *not measured*, *proposed*, `GAP`, `OPEN`.
5. **Keep the vision's never-rules.** Any change to the vision stays a proposal for EJ, never a decision.
6. **Header.** Start the document with a short status block: "Status: draft, not accepted by EJ. Merged 2026-10-12
   by dsh (`deepseek-flash`) from Version A (`runs/20261012-caches-enhance/CACHES.md`) and Version B
   (`runs/20261012-caches-routing/CACHES.enhanced.md`), after reviews by agy, codex and opencode
   (`runs/20261012-caches-merge/reviews/`)."
7. **Measured and reasoned rules stay apart.** If both a memory-entry routing table (A) and a measured routing table
   for code and docs (B) survive, keep them as two tables and say which corpus each covers.

## Output, exactly
Print the merged document between the lines `BEGIN_MERGED` and `END_MERGED`. Then print a merge-notes table between
`BEGIN_NOTES` and `END_NOTES`, with the columns `section | taken from (A / B / both / new) | reviewer support | note`.
