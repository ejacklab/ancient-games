Review one build round of the `code-map` tool, through your rules.

Facts (filled in by the COO). You may read only these paths in the repository:
- Requirements: `runs/20261014-code-map-vision-relay/result-trimmed.md`. Interface: `runs/20261014-code-map-build/spec.md`.
- The code to review (round A5, attempt 1): `runs/20261014-code-map-build/p3/review-a5/a1/src/`. The accepted base
  from round R2, for the diff: `runs/20261014-code-map-build/p3/review-r2/a2/src/`.
- The round's frozen tests: `code_map/test/a5/`. The evaluator's fixtures and cases: `code_map/eval/fixtures/`,
  `code_map/eval/cases/fixtures.json`.
- The round is for A5 ("One question, one answer"). Results measured by the COO: `bun test` 192 pass; `tsgo` exit
  0; the evaluator on its 60 bundled cases: R1, R2, R3, A1, A2, A3, A5, L1 MET (A6 and L2 not checked here; A5 is
  MET for the tool's part, whether the user asked for a map is not checked); on a held-out copy with changed names
  and lines: no NOT MET; on a private set of cases from the real opencode code base: no change from round R2.
- Before this round, 4 of the 13 new tests failed: `callers` of a function held in an imported
  `export const f = Effect.fn("F")(function* () { ... })` found no callers.

Question: should this code be accepted as the base for the next rounds?

In "Answer", give exactly one verdict line first: **APPROVE**, or **CHANGE** followed by each change tied to one
requirement line (quote the line) and the file:line it concerns. A change not tied to a requirement line is not a
change; put it under "Costs and risks". Then your reasons.
