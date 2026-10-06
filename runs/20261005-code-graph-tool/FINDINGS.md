# Code-graph-tool workflow — run findings (2026-10-05/06)

The first real multi-engine run through `dispatch.py` (agy → claude → opencode → codex → claude → opencode). It built
a working tool and surfaced machinery defects a mutation never would have.

## Run state: 5/6 nodes done

| node | engine | status |
|---|---|---|
| n1 research | agy | done |
| n2 design | claude opus | done (4 attempts, two UNCLEAR questions answered) |
| n3 build | opencode | done — `code_graph.py` written (35KB, runs, emits JSON) |
| n4 test cases | codex | done |
| n5 review | claude sonnet | done — **6 real findings** against the tool |
| n6 optimize | opencode | **blocked** — see finding D |

## What the independent reviewer found (n5)

Six concrete deviations, each cited file:line: fixture edge line in the wrong file; fixture-decorated functions get
role `fixture` outside test files; a bare constructor-local call resolves to `__init__` (spec rule 1 violation);
`external_imports` counted per name not per statement; function-local imports collected via `ast.walk`; dead code.
These are exactly what n6 exists to fix.

## Machinery findings (in dispatch.py / the run)

- **A. agy headless cannot write files.** It tried `write_file`, headless mode cannot prompt, auto-denied, no output.
  Fix: read-only nodes print to stdout (the dispatcher captures it); the brief must say "print, do not write".
- **B. The pass-back parser required `---` at byte 0.** claude's one-line prelude broke it. Fixed (see commit).
- **C. No canonical result file for downstream nodes.** n2 left 4 result files; n5 had to guess which was the spec.
  Fix: the brief must pin "the latest done attempt is canonical" with the exact path.
- **D. opencode `--agent build` went interactive and aborted.** With stdin=DEVNULL, opencode asked a
  confirmation ("none if blank") during its build, got EOF, and exited with 7 lines of narration and no header. This
  blocks n6. Needs an opencode auto-accept/non-interactive invocation (investigate `--yes`/a config flag).

## Decisions made as COO during the run

1. Coverage is **transitive** — a function is tested if any test reaches it directly or transitively.
2. Tests that run a script via `subprocess` create no edge — **accepted as a v1 blind spot**; future `runs` edge kind.
3. Namespace packages (no `__init__.py`) — **out of v1 scope**; n6 may add if coverage numbers warrant.
4. Where a spec example contradicts a rule — **the rule is normative**.

## Open

n6 (fix the 6 findings, run the tool on the repo, prove complete) is blocked on finding D. Once opencode's
non-interactive build is fixed, resume: `dispatch.py run runs/20261005-code-graph-tool/plan.json --design ...`.
