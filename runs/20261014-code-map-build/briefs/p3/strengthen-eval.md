# Brief — strengthen the evaluator's checks for requirements A5 and A2

You change the `code-map` tool's **evaluator** (`code_map/eval/`), not the tool. Another engine builds the tool
and is judged by these checks, so a check that passes a wrong answer is the fault you are here to remove.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: requirements **A5** and **A2** and their **Fails if**
  lines. Their wording does not change.
- `runs/20261014-code-map-build/spec.md`: the command line and JSON shapes.
- `code_map/eval/README.md`, then `eval/matcher.ts`, `eval/contract.ts`, `eval/run.ts`, `eval/holdout.ts`,
  `eval/cases/fixtures.json`, `eval/stub/`, and the evaluator's own tests in `code_map/test/eval/`.
- `code_map/src/` (read only) to see what the current tool answers.

## Today's gaps

1. A5's link-command answers are never pinned whole: no A5 case checks a `callers`/`callees` answer's `from`, `to`
   and `site` together with the absence of sections the command did not ask for, or of extra links.
2. No A5 case checks a limit exactly: `limitReasons` passes when the expected reason is present among others.
3. On a `format: "text"` case, `includes` and `excludes` select nothing from a string, so `excludes` always passes
   and `includes` cannot be used. `A5-default-text` therefore cannot fail on unasked content.
4. No case checks that `chain` with `--up 0 --down 1` stops at that depth and says so.
5. A2: no fixture has a body written straight into a call with no holder, e.g.
   `Effect.gen(function* () { … })` passed as an argument. Calls inside it may be counted as calls by the
   surrounding named function. The spec's rule for the enclosing function of a call (the nearest function, method or
   arrow) decides the expected answer.
6. A2: no case checks that a same-named helper or fake is **not** shown as a real link.
7. A2: no case has two same-named `Effect.fn` steps; the answer must be `ambiguous` and list every candidate with
   its location.
8. A2: `A2-computed-member` passes an answer that adds a made-up link (for example from `obj[key]()` to an
   unrelated function) as long as the `dynamic` limit is present. `includes` checks also accept a caller, a site and
   a target found on different links.
9. A2: no case has a shared function reached first by a longer route and then by a shorter one, e.g. at depth 3
   `root → a → shared → leaf` and `root → shared → leaf → tail`, with `a` visited first. `tail` is within the depth
   through the shorter route and must still appear; the `seen` reference must not drop it.

## Write

- **Cases** in `eval/cases/fixtures.json`, labelled with their requirement and the exact Fails-if line they test:
  - A5: one `callers` or `callees` case that pins the whole answer (`from`, `to`, `site`, the full list of links,
    no unasked section); one `where <missing name>` case with an exact `equals` on `limits[].reason` being
    `["not-found"]`; one `chain … --up 0 --down 1` case with exact `equals` on the depth stop.
  - A2: one case per gap 5, 6 and 7, each in Effect service style, with `excludes` where a wrong link is the risk.
  - A2, gap 8: give `A2-computed-member` an exact check that its answer has no links, and make the link cases above
    check `from`, `site` and `to` on the **same** link (an exact `equals` on the whole link list is one way).
  - A2, gap 9: the case down and an upward counterpart, each also with the sibling order reversed in the source.
- **Fixtures** for those cases under `eval/fixtures/` (new folders; do not change existing fixture files, because
  existing cases name their lines).
- **Matcher:** on a `format: "text"` case, `includes`/`excludes` check the text for the `file:line` place
  (`chain/logic.ts:3` style). Give `A5-default-text` one `excludes` of a known definition unrelated to `leaf`.
- **Stub:** a canned answer in `eval/stub/answers/` for each new case, correct to the source.
- **Tests** in `code_map/test/eval/`: for each new case, a test that the stub passes it and that one changed canned
  answer (the wrong thing that case exists to catch) makes it NOT MET; a matcher test for the text rule, both ways.
- Keep `eval/README.md` and `eval/COVERAGE.md` true to what you changed.

## Must not

- Change nothing in `code_map/src/` or in `code_map/test/` outside `test/eval/`.
- Do not change any existing case's expectations, except to add checks: the `excludes` on `A5-default-text` and the
  exact no-links check on `A2-computed-member`.
- Do not write a held-out copy anywhere in the repository; the held-out copy is made by someone else.
- Do not install packages. Write nothing outside `code_map/eval/` and `code_map/test/eval/`.

## Done when

From `code_map/`: `bun test test/eval` passes; `bun eval/run.ts --tool "bun eval/stub/stub.ts" --out <scratch dir>`
reports every case MET; `test/eval/holdout.test.ts` covers the new fixtures (the generator rewrites their lines and
names). Return: each new case id, its requirement and Fails-if line, the wrong answer it catches;
the files changed; the last lines of each command.
