# Readiness — 20260930-blueprint-review

Design only: nothing below was run for this run's purposes. "Checked earlier" means checked in this session for
another reason.

## Tools

| Tool | Needed for | Command that proved it works | Result |
|---|---|---|---|
| git | P0, P1 diff | not run for this design | to prove in P0 |
| Codex CLI, `gpt-6.1-sol` and `gpt-6-astra` | P1, P3–P6, P9 | model names checked in `~/.codex/models_cache.json` (2026-09-30); no call made | names exist; canary to run in P0 |
| Claude subagent (Agent tool) | verifiers | none needed | works (in use) |
| script runner (python3) | P2, P7 | `env -u NO_COLOR python3 -m pytest -q` passed earlier this session (381) | works |
| `agy` | not used (Q7) | `agy models` listed models earlier | not needed |

## Skills that apply

| Skill | What it covers here |
|---|---|
| workflow-design | this design |
| verify-extraction | P2/P7: check what an agent says the blueprint says against the file |
| agent-loop | possible enforcement of the P8 loop |
| chronos-ledger | if the run spans sessions |

## Information

| What is needed | Where it is | Structure | Verified against the source? | Which agents can read it |
|---|---|---|---|---|
| The product's blueprint sections 1–8 | `docs/blueprint/` of the product (Q1) | md hierarchy with a map | no (product unknown) | all |
| The renewal's changes | git history of those files | git | not yet | all with the repo |
| Ids (R, N, decisions, tables, screens) | inside the blueprint files | md, only if ids are written consistently | no; P2 tests this | all |

## Blueprint

- Product and map: unknown (Q1).
- Kind of task: not a product change — it reviews blueprint documents and edits none, so no sections are needed and
  no acceptance criteria apply. The guard: any finding that needs code, schema or UI change is a new task with its
  own check.

## Missing or unverified

| Item | Effect |
|---|---|
| Which product (Q1) | ask EJ; blocks P0 |
| Whether ids are machine-readable | P2 tests it; if not, that is a finding and P2 becomes a Codex extraction node |
| How `codex exec` reports the model it ran | canary in P0 settles it; until then the model check is unverified |
| `agy` terms for headless use | excluded (Q7) |
