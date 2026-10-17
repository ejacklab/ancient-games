Check the five faults the COO planted to test round A5's checks. Answer through your own rules.

Facts (filled in by the COO). You may read only these paths in the repository:
- Requirements: `runs/20261014-code-map-vision-relay/result-trimmed.md` (A5: "One question, one answer"; Fails if:
  "an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked.").
  Interface: `runs/20261014-code-map-build/spec.md`.
- The code the plants were made in (round A5, attempt 1, accepted by two reviewers): `runs/20261014-code-map-build/p3/review-a5/a1/src/`.
- The round's frozen tests: `code_map/test/a5/` (13 tests, written by Codex). The evaluator: `code_map/eval/`
  (its A5 cases: `A5-specific-answer`, `A5-default-text` in `code_map/eval/cases/fixtures.json`; its notes:
  `code_map/eval/COVERAGE.md`).
- The plants and their results: `runs/20261014-code-map-build/evidence/p3-a5-src-plants.txt`. Each plant is one
  change in a copy of `src/`; each copy ran the frozen tests, the evaluator on its bundled cases, on a held-out copy
  with renamed identifiers and shifted lines (never seen by the builder), and on a private set of 8 cases from the
  real opencode code base.
- How the round's checks are used: the builder (opencode) may read the frozen tests and the bundled cases but never
  the held-out copy or the private set. A round passes when the tests pass, `tsgo` exits 0, the round's requirement
  is MET on the bundled cases, no earlier round's requirement turns NOT MET, and the round's requirement is not NOT
  MET on any held-out or private set. The COO plants and two reviewers follow.

Question: do these five plants show that round A5's checks would catch an A5 failure? Through your rules, answer:
- **Linus:** is each plant a real A5 failure a user would see, and is it caught for the right reason? Name a
  concrete A5 failure that would pass every check.
- **范蠡:** does this result justify closing round A5 now, or must something be done first?
- **孫子:** which plants are caught only by checks the builder can read? What is left to the builder's good character?
- **老子:** are the plants too heavy-handed to tell us anything? What small, quiet fault would show more?

In "Answer", give one line per plant (enough / not enough, and why), then one verdict line: **CLOSE A5**, or
**STRENGTHEN** with each change to a check, tied to A5's Fails-if line.
