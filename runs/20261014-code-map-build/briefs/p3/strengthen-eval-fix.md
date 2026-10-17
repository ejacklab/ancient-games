# Brief — fix the new evaluator checks: they reject answers the spec allows

You wrote ten new cases in `code_map/eval/` (brief `runs/20261014-code-map-build/briefs/p3/strengthen-eval.md`).
Run against the real tool (`bun src/cli.ts`), several fail on answers that are correct under
`runs/20261014-code-map-build/spec.md`. A check that fails a correct answer is as wrong as one that passes a wrong
answer. The run's report: `runs/20261014-code-map-build/p3/A5-a1-strengthened/eval/report.json` (each case keeps
the tool's `answer`).

## The faults, by shape

1. Exact `equals` on a whole link or chain fails when the answer carries a field the spec types allow and the case
   does not test: optional fields (`endLine`, `declaration`), or a field on a node that adds nothing the spec forbids.
2. Exact `equals` on candidate lists fails when the order differs; the spec does not fix their order.
3. A case pins a name the spec does not define: the spec names an enclosing function by the const or property that
   holds it, and says nothing about the name of a body with no holder.

## Do

- Change the new cases (and only the matcher support they need) so each still fails on the wrong answer it exists
  to catch — wrong or extra links, a caller, site and target on different links, unasked sections, a missing or
  extra limit reason, a missing link within the depth, a made-up link — and passes every answer the spec allows.
  Pin a field only where the spec fixes it.
- For each changed case, a test in `code_map/test/eval/` that a spec-allowed variant passes (extra optional fields,
  reordered candidates, a different name for a body with no holder) and the wrong answer still fails.
- Keep `eval/README.md` and `eval/COVERAGE.md` true.

## Must not

- Same as the first brief: write only in `code_map/eval/` and `code_map/test/eval/`; no changes to `src/`, to
  other tests, or to existing cases' expectations; no held-out copy; no packages.
- Do not loosen a check until it passes the tool's answer: the report shows the tool's answers, and some of them
  are wrong. A check that now passes must pass because the spec allows the answer.

## Done when

From `code_map/`: `bun test test/eval` passes; the stub run reports every case MET. Then run the evaluator with
`--tool "bun src/cli.ts"` into a scratch folder and return, per new case: MET or NOT MET, and for each NOT MET the
mismatch and why the spec makes that answer wrong.
