# Brief — P2: build the code-map evaluator

You are building the **evaluator** for a tool that does not exist yet. Another engine will build the tool later and
must pass your evaluator. You never see that tool, and it never writes your files.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements. Every **Fails if** line is a check.
- `runs/20261014-code-map-build/spec.md`: the tool's command line, its JSON output shapes, and the evaluator's
  contract (section "Evaluator", with the case file format).
- `code_map/package.json` and `code_map/tsconfig.json`: the package is set up; `bun install` has been run.

Read nothing else outside `code_map/` and those two files.

## Write

All of your files go under `code_map/eval/` and `code_map/test/eval/`:

1. **`code_map/eval/run.ts`**: the evaluator CLI, as the spec's "Evaluator" section describes:
   `bun code_map/eval/run.ts --tool "<command>" [--cases <file>]... --out <dir>`. It runs the tool as a black box
   (a shell command plus the arguments, reading `--json` output). It writes `report.json` and `report.md`: MET,
   NOT MET or NOT CHECKED per requirement and per Fails-if line, with totals, and for every NOT MET the case id,
   the arguments, and what was expected against what came back.
2. **`code_map/eval/fixtures/`**: small TypeScript projects, each with its own `tsconfig.json`, written so that a
   specific Fails-if line can fire. Cover every Fails-if line of R1, R2, R3, A1, A2, A3, A5 and L1 that a fixture
   can exercise. These must be included:
   - an Effect-like injected service (`yield* X.Service`, then `x.method(...)`) whose real implementation sits in a
     layer, plus a test file that defines a fake implementation of the same interface (R2: the fake is labelled
     `testFake` and the target is still `implementation`);
   - two real implementations of one interface (R2: `ambiguous`), and one with none (R2: `unresolved`);
   - a top-level marker write (R1);
   - a recursive call or a function reached twice (A2: `seen`, shown once);
   - a test that reaches a function only through a fake (A3: `undecided` with no `--fake-rule`);
   - two sibling files under one folder (A1 siblings, given by `--siblings`).
   Write no dependency imports in fixtures; define any Effect-like types inside the fixture.
3. **`code_map/eval/cases/fixtures.json`**: the case file over your fixtures, in the spec's format. Each case names
   its requirement and the exact Fails-if line it checks.
4. **`code_map/eval/stub/`**: a **stub tool** that answers exactly the commands in `cases/fixtures.json` from canned
   JSON files (one file per case, the canned answer a correct tool would give), and prints
   `{"command":..., "limits":[], "empty":"none found by static analysis"}` for anything else. The stub must pass
   every fixture case: running the evaluator with `--tool "bun code_map/eval/stub/stub.ts"` must report every
   fixture-checkable line MET. Keep the canned answers in plain JSON files, so that someone else can break one on
   purpose and check that the evaluator catches it.
5. **`code_map/test/eval/*.test.ts`**: `bun test` tests of the evaluator itself: the case matcher (`includes`,
   `excludes`, `equals`, `ambiguous`, `limitReasons`, the `[]` and `children` path rules), the MET / NOT MET /
   NOT CHECKED logic (a line no case exercises is NOT CHECKED, never MET), and a run against the stub.

R1 and R3 run the tool for real:
- **R1:** after running the tool on the marker fixture, check the marker does not exist; remove it if it does.
- **R3:** run the tool under `unshare -rn` (exit status and output kept); also compare a listing of the files
  under `--root` and the working directory before and after each run. If `unshare -rn` is unavailable, R3 is
  NOT CHECKED with that reason, never MET.

## Must not

- Do not write anything outside `code_map/eval/` and `code_map/test/eval/`. Do not write `code_map/src/`.
- Do not change `code_map/package.json`, `code_map/tsconfig.json`, the spec, or the requirements. If the spec is
  wrong or unclear, write the problem in `code_map/eval/SPEC_QUESTIONS.md` and choose the narrowest reading.
- Do not install packages. Use Bun and Node built-ins and `typescript` only.
- Do not read any other folder of this repository or of your home directory.

## Done when

In `code_map/`:
- `bun test` passes;
- `bunx tsgo --noEmit` exits 0;
- `bun eval/run.ts --tool "bun eval/stub/stub.ts" --cases eval/cases/fixtures.json --out /tmp/cm-eval` reports
  every line your fixtures exercise as MET, and NOT CHECKED for the rest.

Run all three and fix until they hold. Return the last lines of each output, the list of Fails-if lines your
fixtures cover, and the lines you marked NOT CHECKED with the reason.
