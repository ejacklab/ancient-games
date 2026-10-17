# code-map — spec v0 (P2, written by the COO, 2026-10-14)

Requirements: `runs/20261014-code-map-vision-relay/result-trimmed.md` (draft; P3 waits for EJ's acceptance). This
spec fixes the interface so the evaluator and the build agree. It does not prescribe internals beyond what the probe
showed (`evidence/p1-callhierarchy-summary.md`).

## Package

- **Location:** `code_map/`, a TypeScript package named `code-map`.
- **Runs with:** `node code_map/dist/cli.js` after `npm run build`, or with `npx tsx code_map/src/cli.ts`.
- **Runtime dependency:** `typescript` only. ts-morph is allowed if the research shows it is needed. No other runtime
  dependency.
- **The project's compiler:** the tool loads the target project's own `typescript` from the target's
  `node_modules` when present, and falls back to its own copy otherwise.

## Command line

```
code-map <command> --project <tsconfig.json> [--json] [options]
```

| Command | Answers | Requirement |
|---|---|---|
| `where <name>` | where a function, method or service member is defined: every match, flagged if ambiguous | A1, A5 |
| `find "<code or words>"` | the places that match a piece of code (exact text) or a description (ranked words over names, comments and strings): file:line, flagged if ambiguous | A2 |
| `callers <file:line \| name>` | one level up, with each call site | A1, A2 |
| `callees <file:line \| name>` | one level down, with each call site | A1, A2 |
| `chain <file:line> [--up N] [--down N]` | the chain up and down (default 6 and 6, counted from the place as level 0) | A2 |
| `tests <file:line \| name>` | the count and list of tests that reach the function through static links, with each path | A3 |
| `tests --file <path> [--per-function]` | the tests that reach any function in the file; the per-function report only with `--per-function` | A3 |
| `map <folder>` | the module map: definitions, calls, entry flows as steps, and the sibling table when siblings exist | A1 |

- **Text output** by default, compact, for an agent. `--json` gives the same content as JSON.
- **One question per run** (A5). There is no command that prints the whole repository.

## What every answer carries

- **evidence:** `file:line` for every claim (A1).
- **resolution** for every call link:
  - `implementation`: found by the type checker's implementation lookup;
  - `declaration`: only the declaration is known;
  - `unresolved`: the target is unknown, with a reason (R2).
- **limits:** each branch or answer that stops early carries `stop: {reason}`, one of `dynamic`, `outside-repo`,
  `other-process`, `not-found`, `depth`, `seen` (a pointer back), or `other: <text>` (L1).
- **empty:** an empty result says "none found by static analysis", never "none" (L1).
- **tests:** labelled `static-call-path`, never coverage (A3).

## Call links (R2)

A call link joins a calling function to a called function. It is found as follows:

| Kind | How it is found |
|---|---|
| Direct call or `new` | the type checker's definition, then its implementation |
| Call on an injected service (Effect `yield* X.Service`, then `x.method(...)`) | the type checker's implementation lookup on the member (the probe showed `edit.ts:275` → `permission.ts:231`) |
| Callers of a function | references to its declaration and to its interface member, each mapped to the enclosing function |
| The enclosing function of a call site | the nearest function, method, arrow function, or `const x = Effect.fn(...)(...)` / `Effect.gen` body |
| The call target is not known | the link is kept with `resolution: "unresolved"` and a reason |

## Module map (A1)

- **definitions:** id, name, kind, file, line, end line.
- **calls:** in-module and out-of-module, with their resolution.
- **flows:**
  - for each entry function (one that nothing in the module calls, or one that is exported and used from outside),
    an ordered list of steps: `call`, `if`, `else`, `loop`, `try`, `catch`, `return` and `yield*`, each with its line
    and its text, never truncated;
  - a step whose text is longer than the output width is wrapped, not cut.
- **siblings:**
  - for files in one folder that export the same shape (for example the tool plugins, or the providers), a table of
    concerns, each `shared` or `varies`, with each member's text and line;
  - when the tool cannot settle a row, it says "unclear".

## Never

- **R1 Executes nothing.** It never imports, requires or runs a file of the target project. It reads files and builds
  a TypeScript program only.
- **R3 Stays offline.** It opens no network connection.
- **Stores nothing in the target.** Every run is rebuilt from the files. A cache is allowed only outside the target,
  and only if P5 shows it pays.

## Evaluator (`code_map/eval/`, built by Codex, not by the builder)

- **One check per Fails if** in the requirements, on two kinds of input:
  - small fixture projects in `code_map/eval/fixtures/`, each written so that one Fails if can fire (for example, a
    service injected with a fake Effect-like `yield*`, or a top-level marker write for R1);
  - fixed questions on opencode at `6dc4d4e`, compared with keys kept away from builders.
- **Reports** MET, NOT MET or NOT CHECKED per requirement, with totals, as JSON and Markdown.
- **R3** is checked by running the tool in a separate network namespace (`unshare -n`), or with a Node preload that
  makes every socket call throw. Either way, a connection attempt is a failure.
- **R1** is checked with a fixture whose top level writes a marker file: after `map`, `chain` and `tests`, no marker
  may exist.
- **L2** is not checked by the evaluator. It is the P5 measurement.
