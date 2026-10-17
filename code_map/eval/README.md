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

The 70 fixture cases exercise the 18 fixture-checkable Fails-if lines, with runtime marker checks and R3 observations on every invocation. A6 and L2 are NOT CHECKED without the external evaluation work. The report also states the agent/privacy parts it cannot establish. See [SPEC_QUESTIONS.md](SPEC_QUESTIONS.md).

`stub/answers/<case-id>.json` contains each editable canned answer. Change a location, resolution, count, limit, or fake label and rerun: the evaluator should report NOT MET. Identical commands have identical canned files; the stub rejects disagreement among them, so changing any one is observable. Unknown commands print the empty static-analysis answer required by the brief.

These checks were written by P2 Codex independently of the future builder. Passing the stub validates evaluator plumbing and its known answers. It does not establish correctness of a future tool on other source projects.


The repair keeps R1's marker/exit observations and R3's isolation/snapshot observations separate from answer correctness. R1 runs across all eight command-table forms, including `tests --file`, and includes a source whose top level writes the marker and throws. Wrong JSON cannot fail an R1 or R3 case; safety faults cannot fail an answer requirement. `observedChanges` preserves raw filesystem evidence; `changedFiles` excludes the deliberate R1 marker and its parent-directory timestamp change. Reports show R3, A2, A3 and A5 as `MET (tool part)` with their unchecked portions beside the verdict, in JSON and Markdown.

Optional fixture-case extensions are `tests: string[]` (overrides the suite's patterns, including `[]` for no `--tests`), `format: "text"` (omits `--json`), and `expect.textIncludes: string[]` (source names and locations required in the sampled text answer). JSON is otherwise the default. On text cases, location `includes` and `excludes` search stdout for the complete `file:line` place; their JSON `path` is ignored. Matching a line does not match a longer line number or a suffix of another path. Text presentation is not prescribed beyond those evidence strings. Source comparisons parse the fixture files and compare complete syntax-node text at the stated lines, normalizing only trailing whitespace; chain and test paths are also checked for connected endpoints and source call sites.

`expect.shapes: [{path, value}]` uses the same path selection as `equals`. Scalars match exactly; objects require the written fields and allow additional fields; arrays require exactly the written items, each matched once, in any order, recursively. This keeps a link's caller, site and target together and rejects extra or missing links and candidates while accepting optional `endLine`/`declaration` fields and extra node metadata. Omit a field from the shape when the spec leaves its value open. `equals` retains exact, ordered deep equality. `expect.exactLimitReasons: string[]` requires exactly that set of reasons across `limits` and branch `stop`s; repeating a branch reason in the summary does not add a reason. It does not replace checking each required branch stop.

Generate a held-out copy from `code_map/`:

```sh
bun eval/holdout.ts --seed 42 --out /tmp/cm-heldout
bun eval/run.ts --tool "bun src/cli.ts" --cases /tmp/cm-heldout/fixtures.json --out /tmp/cm-heldout-report
```

The generator leaves filenames stable, inserts seed-chosen blank/comment lines in every source file and blank lines in every tsconfig, and renames declared identifiers and their references, including contextual identifier names such as `assert`. Each name uses a seed-specific suffix; same-spelled members stay same-spelled so the type-versus-name fixture remains adversarial. Source literals, titles, import paths and external built-in names stay intact. Property accesses are checked against TypeScript declaration files so a local parameter named `value` does not rename the iterator result’s built-in `.value` member. Root and project paths in the generated case file are absolute. Location expectations, queries, names and source text expectations are rewritten from the original source's line/name maps. The generator never reads canned answers; tests transform canned witnesses to validate the resulting cases against the written source. The bundled stub's exact argument lookup intentionally fails on a held-out root.

R1's runtime marker check stays on the bundled fixtures only. Held-out R1 cases remain NOT CHECKED for the marker observation. See the ambient test-API naming question in [SPEC_QUESTIONS.md](SPEC_QUESTIONS.md).

The `const-held` fixture chains an exported constant arrow through an `Effect.fn` generator, a constant function expression, a shorthand `Service.of({ get })` binding and an object property arrow to a constant leaf. Its entry is called from outside the mapped folder; a user-pattern test reaches the leaf. Eight cases check both chain directions, callers, callees, test evidence, ordered entry decisions, and description matches found only in a comment or string. Mutation checks reject missing bodies, lost holder names, missing/reordered entry steps, and treating the shorthand binding as a call.

The A5/A2 strengthening adds ten cases in five new fixture projects. A5 pins a complete callee link list, rejects unasked sections through the contract, checks exactly `["not-found"]` for a missing definition, and pins the one-level chain and its depth stop. The depth case permits a top-level depth summary or just the required branch stop, rejecting other reasons. Its default text case excludes the unrelated `recursive` definition. Resolved link/chain/test answers cannot carry a separate `matches` candidate section. A2 checks ownership of a service call inside an unheld `Effect.gen` generator, excludes a same-named helper and test fake as real targets, and lists both same-named `Effect.fn` steps as ambiguous. The inline generator's `<anonymous>` canned name is a fixture label; only its source location and kind are pinned, because the spec leaves an unheld body's name open. The existing computed-member case requires an empty link list even when a dynamic limit is present.

Four chain cases exercise a shared function reachable by a long route and a short route, downward and upward, with both source sibling orders. Their witnesses expand the shared function on the shorter route and reference it on the longer route, keeping the tail inside depth three. The depth-three link is checked as one shape, independent of sibling order and optional fields. The contract checks that each `seen` reference identifies a function shown exactly once, including when its full expansion is serialized later. Integration mutation tests require each new case to be MET with the stub and a spec-allowed variant, and NOT MET with its targeted wrong answer. Variants add optional fields, reorder candidates and siblings, and change the unheld body's name. See [COVERAGE.md](COVERAGE.md) for case IDs, exact Fails-if lines, files and verification. Holdout tests create their temporary copies outside the repository and rewrite link-shape locations, exclusions, duplicate step names and exact query expectations.
