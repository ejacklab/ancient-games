# Evaluator

From `code_map/`:

```sh
bun eval/run.ts --tool "bun eval/stub/stub.ts" --cases eval/cases/fixtures.json --out /tmp/cm-eval2
```

From the repository root, the bundled case paths work unchanged:

```sh
bun code_map/eval/run.ts --tool "bun code_map/eval/stub/stub.ts" --out /tmp/cm-eval2
```

Additional `--cases` files follow the spec's format. The shell tool command is trusted; appended case arguments are shell quoted. Paths in external case files are relative to the invoking working directory. The evaluator reads JSON stdout (or sampled default text output for a case with `format: "text"`) and preserves the full command, exit status, stdout, stderr, changed-file list and expectation mismatches in `report.json`. `report.md` presents the requirement/line statuses and failures. Runs are sequential so snapshots belong to one invocation.

The 60 fixture cases exercise the 18 fixture-checkable Fails-if lines, with runtime marker checks and R3 observations on every invocation. A6 and L2 are NOT CHECKED without the external evaluation work. The report also states the agent/privacy parts it cannot establish. See [SPEC_QUESTIONS.md](SPEC_QUESTIONS.md).

`stub/answers/<case-id>.json` contains each editable canned answer. Change a location, resolution, count, limit, or fake label and rerun: the evaluator should report NOT MET. Identical commands have identical canned files; the stub rejects disagreement among them, so changing any one is observable. Unknown commands print the empty static-analysis answer required by the brief.

These checks were written by P2 Codex independently of the future builder. Passing the stub validates evaluator plumbing and its known answers. It does not establish correctness of a future tool on other source projects.


The repair keeps R1's marker/exit observations and R3's isolation/snapshot observations separate from answer correctness. R1 runs across all eight command-table forms, including `tests --file`, and includes a source whose top level writes the marker and throws. Wrong JSON cannot fail an R1 or R3 case; safety faults cannot fail an answer requirement. `observedChanges` preserves raw filesystem evidence; `changedFiles` excludes the deliberate R1 marker and its parent-directory timestamp change. Reports show R3, A2, A3 and A5 as `MET (tool part)` with their unchecked portions beside the verdict, in JSON and Markdown.

Optional fixture-case extensions are `tests: string[]` (overrides the suite's patterns, including `[]` for no `--tests`), `format: "text"` (omits `--json`), and `expect.textIncludes: string[]` (source names and locations required in the sampled text answer). JSON is otherwise the default. Text presentation is not prescribed beyond those evidence strings. Source comparisons parse the fixture files and compare complete syntax-node text at the stated lines, normalizing only trailing whitespace; chain and test paths are also checked for connected endpoints and source call sites.

Generate a held-out copy from `code_map/`:

```sh
bun eval/holdout.ts --seed 42 --out /tmp/cm-heldout
bun eval/run.ts --tool "bun src/cli.ts" --cases /tmp/cm-heldout/fixtures.json --out /tmp/cm-heldout-report
```

The generator leaves filenames stable, inserts seed-chosen blank/comment lines in every source file and blank lines in every tsconfig, and renames declared identifiers and their references, including contextual identifier names such as `assert`. Each name uses a seed-specific suffix; same-spelled members stay same-spelled so the type-versus-name fixture remains adversarial. Source literals, titles, import paths and external built-in names stay intact. Property accesses are checked against TypeScript declaration files so a local parameter named `value` does not rename the iterator result’s built-in `.value` member. Root and project paths in the generated case file are absolute. Location expectations, queries, names and source text expectations are rewritten from the original source's line/name maps. The generator never reads canned answers; tests transform canned witnesses to validate the resulting cases against the written source. The bundled stub's exact argument lookup intentionally fails on a held-out root.

R1's runtime marker check stays on the bundled fixtures only. Held-out R1 cases remain NOT CHECKED for the marker observation. See the ambient test-API naming question in [SPEC_QUESTIONS.md](SPEC_QUESTIONS.md).

The `const-held` fixture chains an exported constant arrow through an `Effect.fn` generator, a constant function expression, a shorthand `Service.of({ get })` binding and an object property arrow to a constant leaf. Its entry is called from outside the mapped folder; a user-pattern test reaches the leaf. Eight cases check both chain directions, callers, callees, test evidence, ordered entry decisions, and description matches found only in a comment or string. Mutation checks reject missing bodies, lost holder names, missing/reordered entry steps, and treating the shorthand binding as a call.
