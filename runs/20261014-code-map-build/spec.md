# code-map — spec v1 (P2, written by the COO)

Requirements: `runs/20261014-code-map-vision-relay/result-trimmed.md` (accepted). This spec fixes the interface so
that the evaluator and the build agree. It prescribes internals only where the probe showed what works
(`evidence/p1-callhierarchy-summary.md`, `evidence/p1-experiments-summary.md`).

## Package

- **Location:** `code_map/` in this repo, a TypeScript package named `code-map`.
- **Runs with:** `bun code_map/src/cli.ts`. Tests use `bun test`, and type checking uses `bunx tsgo --noEmit`.
- **Runtime dependency:** `typescript` 5.8.2 only. P0 showed that it compiles opencode core. No other runtime
  dependency.

## Command line

```
code-map <command> --project <tsconfig.json> [--root <dir>] [--tests <glob>]... [--json] [options]
```

- `--project` takes a tsconfig. It may be repeated, and the tool then builds one program from all of them.
- `--root` is the directory that every output path is relative to. The default is the current directory.
- `--tests <glob>` names the test files, relative to `--root`, and may be repeated. **Which files are test files is
  set by the user.** The tool has no default. With no `--tests`, no file is a test file, and every answer whose
  content would change carries the limit `{reason: "other", text: "no test-file pattern given"}`.

| Command | Answers | Requirement |
|---|---|---|
| `where <name>` | every definition matching the name (`Permission.assert` or `assert`), with `ambiguous` | A1, A5 |
| `find "<code or words>"` | the places that match exact code text, or ranked matches for a description over names, comments and strings, with `ambiguous` | A2 |
| `callers <file:line \| name>` | one level up, with each call site | A1, A2 |
| `callees <file:line \| name>` | one level down, with each call site | A1, A2 |
| `chain <file:line> [--up N] [--down N]` | the caller and callee chains. The default depth is 6 each way, and the place itself is level 0 | A2 |
| `tests <file:line \| name> [--fake-rule count\|exclude]` | the tests that reach the function through static links | A3 |
| `tests --file <path> --per-function` | the per-function report for a whole file. It runs only with `--per-function` | A3 |
| `map <path>... [--siblings <glob>]...` | the module map of one or more folders or files | A1 |

- **Text output** is the default and is compact, for an agent. `--json` gives the same content as JSON (shapes
  below).
- **One question per run** (A5). No command prints the whole repository. `map` prints a module only because the
  user asked for it.
- When `where`, `callers`, `callees`, `chain` or `tests` is given a name that matches more than one definition,
  the tool answers nothing and returns the candidates with `ambiguous: true`, exactly as `where` does.

## JSON shapes

```ts
type Loc = { file: string; line: number; endLine?: number }      // file relative to --root, lines 1-based
type Node = Loc & { name: string; kind: "function" | "method" | "arrow" | "effect-fn" | "property" | "class"
                    | "variable" | "interface-member" | "other" }
type Limit = { at?: Loc; reason: "depth" | "dynamic" | "outside-repo" | "other-process" | "not-found" | "seen"
               | "other"; text?: string; ref?: Loc }               // "seen": ref points to where it is shown
type Candidate = Node & { testFake: boolean }                     // testFake: the file matches --tests
type Link = {
  from: Node; site: Loc; kind: "call" | "new" | "service-call"
  declaration?: Loc                                               // what the type checker says the callee is
  resolution: "implementation" | "ambiguous" | "unresolved"
  to?: Node                                                       // only when resolution is "implementation"
  candidates: Candidate[]                                         // every implementation the lookup found
  via: "definition" | "implementation-lookup"
  reason?: string                                                 // required when "unresolved"
}
type Answer = {
  command: string; query: string[]
  ambiguous?: boolean; matches?: Node[]                           // where, find, and any ambiguous name
  links?: Link[]                                                  // callers, callees
  chain?: { up: ChainStep[]; down: ChainStep[] }                  // chain
  tests?: TestsAnswer                                             // tests
  map?: ModuleMap                                                 // map
  limits: Limit[]
  empty?: "none found by static analysis"                         // present exactly when the result is empty
}
type ChainStep = { level: number; link: Link; children: ChainStep[]; stop?: Limit }
type TestCase = { file: string; line: number; name: string; path: Link[]; throughFake: boolean }
type TestsAnswer = { label: "static-call-path"; count: number; tests: TestCase[]; undecided: TestCase[] }
type ModuleMap = {
  definitions: Node[]; links: Link[]
  entries: { fn: Node; steps: Step[] }[]
  siblings?: { members: string[]; rows: { concern: string; status: "shared" | "varies" | "unclear";
               cells: { member: string; text: string; at: Loc }[] }[] }
}
type Step = { kind: "call" | "if" | "else" | "loop" | "try" | "catch" | "return" | "yield*"; at: Loc;
              text: string; children?: Step[] }
```

## Call links (R2)

| Kind | How it is found |
|---|---|
| Direct call or `new` | the type checker's definition, then its implementation (`via: "definition"`) |
| Call on an injected service (Effect `yield* X.Service`, then `x.method(...)`) | the type checker's implementation lookup on the member (`via: "implementation-lookup"`). The probe showed `edit.ts:275` → `permission.ts:231` |
| Callers of a function | references to its declaration and to its interface member. Only a reference that is called is a caller (E1: a `Service.of` shorthand is not) |
| The enclosing function of a call site | the nearest function, method or arrow, named by the `const x = Effect.fn(...)` or the property that holds it. E1 found 17 of 18 calls in anonymous bodies |

Resolution, over the candidates that are **not** test fakes:
- exactly one → `implementation`, and `to` is that one;
- more than one → `ambiguous`;
- none → `unresolved`, with a reason.

Test fakes stay in `candidates` with `testFake: true` and never change the resolution. The tool has no rule for
Effect service wiring. A declaration is never `to`.

## Call chain (A2)

- The place is level 0. Up and down each stop at the depth given (default 6), with `stop: {reason: "depth"}`.
- A function reached a second time is not expanded again. Its step carries `stop: {reason: "seen", ref}`, where
  `ref` is the location where it is shown.
- When `find` returns several places, the **agent** picks the one that fits the question, runs `chain` on it, and
  names the others in its answer. The tool's part is to list every candidate with `ambiguous: true`. The agent's part
  is checked in P6, not by the evaluator.

## Tests (A3)

- **A test** is one `test(...)`, `it(...)` or `describe`-nested test call in a test file (`--tests`), named by its
  first argument. `count` counts test cases.
- A test reaches the function when a chain of links runs from the test's body to the function. `path` is that
  chain, and each link is its evidence.
- `throughFake` is true when the path passes a `service-call` link whose candidates include a test fake.
- **The fake rule is set by the user:**
  - `--fake-rule count`: tests with `throughFake` are counted and listed in `tests`;
  - `--fake-rule exclude`: they are left out of both `tests` and `undecided`;
  - with no `--fake-rule`, they go in `undecided`, are not counted, and the answer carries the limit
    `{reason: "other", text: "fake rule not set (A3)"}`.
- `count` always equals `tests.length`.

## Module map (A1)

- **definitions:** every function, method, class and `Effect.fn` constant in the paths given.
- **links:** calls made from inside the module, to anywhere.
- **entries:** an entry function is one that is exported and called from outside the paths given. Each entry has its
  steps in source order, with every step's full text (wrapped, never cut).
- **siblings:** set by the user with `--siblings <glob>`, repeatable, one glob per sibling group. With no
  `--siblings`, there is no sibling table, and the answer carries the limit
  `{reason: "other", text: "no sibling rule given (A1)"}`. Each row is a concern: `shared`, `varies`, or `unclear`
  when the tool cannot settle it.
- **Every claim has a location.**

## Never

- **R1 Executes nothing.** The tool never imports, requires or runs a file of the target project. It reads files and
  builds a TypeScript program only.
- **R3 Stays offline, writes only its output.** It opens no network connection and writes no file except to stdout
  and, when `--out` is given, that one file.
- **Stores nothing in the target.** Every run is rebuilt from the files.

## Evaluator (`code_map/eval/`, built by Codex, not by the builder)

- **Command:** `bun code_map/eval/run.ts --tool "<command that runs code-map>" [--cases <file>]... --out <dir>`.
  It runs the tool as a black box through its `--json` output, so a broken copy of the tool can be checked the same
  way.
- **One check per Fails-if line** of R1, R2, R3, A1, A2, A3, A5, A6 and L1, on two kinds of input:
  - fixture projects in `code_map/eval/fixtures/`, each written so that one Fails-if line can fire;
  - case files (`--cases`, JSON, format below) that hold questions about a real project and their expected answers.
    The evaluator ships the format and one small example case file over its own fixtures. Case files for opencode
    are written by the COO and kept away from builders.
- **Reports** MET, NOT MET or NOT CHECKED per requirement and per Fails-if line, with totals, as `report.json` and
  `report.md`. A requirement is MET only when every one of its lines is MET. A line that no input exercises is
  NOT CHECKED, never MET.
- **R1:** a fixture whose top level writes a marker file. After `map`, `chain`, `tests` and `callers` run, no marker
  may exist.
- **R3:** the tool runs under `unshare -rn` (E5), and a connection attempt is a failure. The evaluator also lists
  the files changed under `--root` and in the working directory before and after each run. Any change is a failure.
- **A2's naming of the other candidates** and **A5's "unasked whole map"** are agent behaviour. The evaluator
  checks the tool's part (every candidate listed; no command dumps more than asked) and marks the agent's part
  NOT CHECKED, pointing to P6.
- **A6:** the opencode case files for the three modules. A6 is MET when `map` on each module passes A1's checks.
- **L2** is not the evaluator's. It is the P5 measurement.

### Case file format

```json
{
  "project": ["packages/core/tsconfig.json"], "root": ".", "tests": ["packages/core/test/**"],
  "cases": [
    { "id": "X1", "requirement": "R2", "line": "an implementation the lookup finds has no link",
      "args": ["callees", "src/a.ts:10"],
      "expect": { "includes": [{ "path": "links[].to", "file": "src/b.ts", "line": 4 }],
                  "excludes": [], "equals": [], "ambiguous": null, "limitReasons": [] } }
  ]
}
```

- `includes`: objects with `file` and `line` that must be found at `path` (a simple dotted path; `[]` means any
  element; `children` is searched at any depth).
- `excludes`: the same form, for objects that must not be found there.
- `equals`: `{path, value}` pairs.
- `ambiguous`: `true`, `false`, or `null` (not checked).
- `limitReasons`: reasons that must appear in `limits` or in a `stop`.

The `tests` value in a case file is the test-file pattern the case runs with. What counts as a test file is open
for EJ (R2), so the opencode case files use opencode's own `test/` folders until EJ sets the rule.
