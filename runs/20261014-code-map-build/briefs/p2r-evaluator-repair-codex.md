# Brief — P2 repair: strengthen the code-map evaluator

You wrote `code_map/eval/` earlier. Four reviewers checked whether it can serve as the build loop's check, and found
gaps. Repair them. The requirements and spec are unchanged:
`runs/20261014-code-map-vision-relay/result-trimmed.md` and `runs/20261014-code-map-build/spec.md`.

## Gaps to close

1. **R1 and R3 are judged on their own observations only.** R1: marker absent and the tool exited 0, for every
   command in the spec's command table (`where`, `find`, `callers`, `callees`, `chain`, `tests`, `tests --file`,
   `map`), whatever the answer content. R3: the isolation and snapshot results only. A wrong answer is judged under
   its own case's requirement, never R1's. An R1 or R3 fault never marks another requirement NOT MET. Add an R1
   fixture whose top level throws.
2. **Check relationships, not only shape.** Each of these false answers is accepted today, and must be rejected:
   - a sibling cell whose `text` is not the source text at its `at` location;
   - a flow step whose `text` is not the source text at its `at` location;
   - a chain whose level-1 links do not start from the requested place, or a child link whose `from` is not its
     parent link's `to`;
   - a test path whose first link does not start in the test, whose last link does not end at the asked function,
     or whose consecutive links do not join, or whose `site` is not a call on that line;
   - an answer section that does not belong to the command (for example a `chain` on a `where` answer).
   Read the fixture source to compare text; normalise only trailing whitespace.
3. **More fixtures** (each with cases):
   - two interfaces with the same member name, one implemented in source and one only in a test file; the call
     resolves through the type, not the name (R2);
   - a test file that matches `--tests` but is under no `test/` folder (R2, A3);
   - a call through a computed member (`obj[key]()`), which must carry a `dynamic` limit or be absent with one (A2,
     L1);
   - a test that names a helper with the same name as the function but never calls the function (A3: not counted);
   - a sibling group whose rows must be `shared` and `varies`, where `unclear` fails (A1);
   - an answer where a limit must be absent (L1: no blanket limit);
   - the default text mode (no `--json`) and a run with no `--tests` (the limit the spec names) must both work.
4. **A held-out generator:** `code_map/eval/holdout.ts --seed <n> --out <dir>` writes a copy of the fixtures and of
   `cases/fixtures.json` in which every fixture file has a seed-chosen number of blank or comment lines inserted at
   seed-chosen places and every identifier the fixtures define is renamed by seed, with every expected location,
   name and text in the cases rewritten to match. The copy must type-check with each fixture's tsconfig. The
   evaluator must accept `--cases <dir>/fixtures.json` with that copy as its root. R1's marker check may stay on the
   bundled fixtures only; say so in the report.
5. **Report the unchecked part beside MET:** R3 (caught connection attempts, writes outside the observed trees,
   git and training), A2 (the agent's pick and naming), A3 (the agent asking), A5 (whether the user asked). The
   report shows each as `MET (tool part)` with the unchecked part named.

The canned stub must still pass the bundled cases (update its canned answers for the new cases). On a held-out copy,
the stub's lookup table no longer matches; that is expected.

## Must not

- Write only under `code_map/eval/` and `code_map/test/eval/`. Do not write `code_map/src/`, `package.json`,
  `tsconfig.json`, the spec or the requirements. Spec problems go in `code_map/eval/SPEC_QUESTIONS.md`.
- Do not install packages. Bun and Node built-ins and `typescript` only.
- Read nothing outside `code_map/`, the requirements and the spec.

## Done when

In `code_map/`:
- `bun test` passes, including tests that each of the five false answers in gap 2 is rejected, that an R1 fault
  leaves other requirements' status unchanged, and that `holdout.ts` output type-checks and keeps every case's
  expectations consistent with its source;
- `bunx tsgo --noEmit` exits 0;
- `bun eval/run.ts --tool "bun eval/stub/stub.ts" --cases eval/cases/fixtures.json --out /tmp/cm-eval2` reports every
  exercised line MET.

Return the last lines of each output, the new cases by requirement, and any spec questions.
