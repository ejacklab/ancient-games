# Brief — P3 round A2: write the failing tests

You write the tests for one requirement of the `code-map` tool. Another engine builds the tool afterwards and must
pass your tests without changing them.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: requirement **A2** and its **Fails if** lines.
- `runs/20261014-code-map-build/spec.md`: the command line and JSON shapes; the section "Call chain (A2)".
- `code_map/eval/fixtures/` (you may use these projects as test inputs) and `code_map/src/` (read only).
- Tests from earlier rounds: `code_map/test/` (do not change them).

## How to read A2 in this round

These are the owner's provisional decisions. Test against them:
- **A link marked dynamic is not missing** when the link carries a limit at its site naming why. A2's line reads:
  "a known link within the depth is missing with no limit at its site naming why, or a shown link or a limit
  contradicts the code". So a call the type checker resolves, marked `dynamic` instead of linked, fails.
- **"Known":** a place is known when the code or the description points to it. A link is known when it is
  established from the repository's source or type information.
- **Depth is the shortest route** from the place, counted in call links. The place is level 0, and each call link
  adds one level. A function first reached by a longer route must still have the links it has within the depth
  from the shorter route. A reference back never hides a link within the depth.
- **A body written straight into a call** (`Effect.fn("x")(function* () {...})`, or `Effect.gen(function* () {...})`
  passed as an argument) is its own place. A link names the body that holds the call. Going into such a body
  adds **no** level. Do not test the body's name: the spec does not fix it.
- **The tool's part of ambiguity:** list every candidate with `ambiguous: true`. The agent's part is checked
  elsewhere, not by your tests.
- **A function reached twice** is shown once, with a reference back that says where it is shown. A missing
  reference back, or one that does not say where, fails the "shown twice" line.

## Write

Only `code_map/test/a2/*.test.ts` (`a2` in lower case). `bun test` tests that run the tool **through its
command line** (`bun src/cli.ts ... --json`, from `code_map/`) and check the JSON against the spec. Cover every
**Fails if** line of A2, each in at least one test whose name quotes the line. Use your own small fixture projects
under `code_map/test/a2/fixtures/` where the evaluator's do not cover a case. Vary names and line positions from
the evaluator's fixtures, so a tool that memorises those cannot pass. Accept the spec's optional fields (`endLine`,
`declaration`), and never fix the order of candidates.

## The target's service style

The tool is for code like opencode's, where most calls go through Effect services and most functions are held in
constants written straight into a call. Model at least half of your fixtures on that style;
`code_map/test/r2/fixtures/` shows it (read only).

## Pieces and progress

Work in small pieces: one Fails-if line at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/a2-tests.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the
piece, and done or failed.

## Must not

- Write nothing outside `code_map/test/a2/` and that progress file. Do not write `code_map/src/`.
- Do not install packages. Read nothing else.

## Done when

`bun test test/a2` runs, and every test you wrote passes or fails for a reason you can state. The current tool is
known to lose a link within the depth when the shared function is reached first by the longer route, so at least
that test must fail now. Return the test names, the Fails-if line each covers, which fail on the current tool and
why, and the last lines of the run.
