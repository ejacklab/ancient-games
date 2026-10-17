Review one build round of the `code-map` tool, through your rules.

Facts (filled in by the COO). You may read only these paths in the repository:
- Requirements: `runs/20261014-code-map-vision-relay/result-trimmed.md`. Interface: `runs/20261014-code-map-build/spec.md`.
- The code to review (new in this round, about 1,560 lines of TypeScript): `runs/20261014-code-map-build/p3/review-r1/a/src/`.
- The round's frozen tests: `code_map/test/r1/`. The evaluator's fixtures and cases: `code_map/eval/fixtures/`, `code_map/eval/cases/fixtures.json`.
- The round was for R1 ("Reads, never runs"), but the builder wrote the whole tool. Results measured by the COO:
  `bun test` 138 pass; `tsgo` exit 0; the evaluator on its 52 bundled cases: R1, R2, R3, A1, A2, A3, A5, L1 MET
  (A6 and L2 not checked here); on a held-out copy with changed names and lines: 43 MET, 0 NOT MET, 9 NOT CHECKED.

Question: should this code be accepted as the base for the next rounds?

In "Answer", give exactly one verdict line first: **APPROVE**, or **CHANGE** followed by each change tied to one
requirement line (quote the line) and the file:line it concerns. A change not tied to a requirement line is not a
change; put it under "Costs and risks". Then your reasons.
