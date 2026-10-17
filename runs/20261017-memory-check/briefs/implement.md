# Brief — implement memory-check v1

You work in the repository root. Change only files under `memory_check/` (except its four docs) and the result and
progress files named below. Do not commit.

## Task (one deliverable)
Build the TypeScript tool `memory-check` in `memory_check/` so that it meets `memory_check/REQUIREMENTS.md` (F1–F3,
C1–C6, R1–R3) and the use cases in `memory_check/USE_CASES.md`. Read `memory_check/AGENTS.md`, `VISION.md`,
`USE_CASES.md` and `REQUIREMENTS.md` first. Not tests beyond a smoke check: another engine writes the tests.

## Context (each fact with its source)
- The checks come from `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml` (records under `categories[].groups[]
  .requirements[]`, each with `id`, `level`, `check`, `fails_if`; 64 records, listed in
  `runs/20261017-memory-check/sot-requirements.txt`) and `docs/memory-system/CACHES.md` § "Core requirements"
  (B1–B5, K1–K3, Rd1–Rd3, bold headings `**B1 — …**`). Source: those files.
- Which records a tool can decide, and how: `runs/20261017-memory-check/research-q/compare.md` ("Where they agree")
  and the six answers in `research-q/<expert>/answers/`. The decisions taken: `runs/20261017-memory-check/design-decisions.md`.
- `tools/memory_index.py --check` already checks the index and entry format (K6.1a, K6.2, K6.3a, W1.1a/b, W1.2a,
  W1.3a, W4.1b, Rd3.1a): run it with `python3`, from the checked project's root, and parse its output; find it at
  `path.resolve(import.meta.dirname, "../../tools/memory_index.py")`. Source: `tools/memory_index.py` lines 1–15.
- This repo has no `project-memory/` (source: `ls project-memory` fails), so most of its report is "not applicable".
- Layout and config to copy: `code_map/package.json`, `code_map/tsconfig.json` (bun, `bun test`, `tsgo --noEmit`).
  YAML: `Bun.YAML.parse` (used in `.claude/skills/workflow-design/guard/src/criteria.ts:66`).

## Lessons (from `lessons for --agent opencode --kinds code-edit,brief`)
- Each fact in a question or brief for another agent carries its own label and the file:line or command that checked
  it; a fact with neither is marked recall.
- Every file a brief cites lives inside the repo; reads outside it are auto-denied.
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.

## Pieces and progress (first)
Divide the work into small pieces, e.g. scaffold · guidelines loader · locations · memory_index adapter · git checks ·
cache checks · report and warning · CLI · smoke run. Before starting, append one `planned` line per piece to
`runs/20261017-memory-check/nodes/implement.progress.md`, then one line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
- `bun src/cli.ts --project <repo root>` prints a report whose first line names the snapshot (C5); `--warn` prints the
  warning only; `--out F` writes the report; `--home D` sets the home folder for agent memory; exit codes per R3.
- Every SoT record and every CACHES Core requirement appears in the report with one of the five results (C2), its id
  prefixed `SoT:` or `CACHES:`.
- Reads only: no file is created or changed by a run except `--out`'s.
- `cd memory_check && bun install && ./node_modules/.bin/tsgo --noEmit -p .` is clean.
- Smoke run on this repo: `cd memory_check && bun src/cli.ts --project .. --out ../runs/20261017-memory-check/nodes/smoke-report.md; echo "exit $?"`.

## Limits
May change: `memory_check/` (not its four .md docs), the progress file, the smoke report and
`runs/20261017-memory-check/nodes/implement.result.md`. No other AI engine. Foreground commands only.

## Result
`runs/20261017-memory-check/nodes/implement.result.md`: `status: done|partial|fail`, one sentence; the files written;
the typecheck and smoke commands with their last lines; each requirement you could not meet and why; CONTRADICTS (a
requirement or use case line that cannot be met as written, quoted) or none.
