# State — 20261003-node-workdir

Rules: one writer at a time (the COO; the dispatcher writes only dispatch.json and events.jsonl). Progress and
results only; never reasoning.

## Challenge (verbatim)
"yes, do the per-node working folder as first run" — EJ, 2026-10-03, picking the open item from
`docs/DISPATCHER_DESIGN.md` §9: a per-node working folder, so a `qwen` node does not load the repo's context.

## Restatement (method 3.0)
Objective: a dispatcher plan node may name a working folder (`workdir`); its engine runs there, while briefs, result
files and checks keep resolving against the repo root. In scope: `dispatch.py` and its tests. Out of scope: other
scripts, `ancient_games/`, docs (the COO updates them after). Why: a qwen node from the repo root cost about 198k
tokens for a one-line answer (explore.md X8). Done when: R1–R7 pass in the verifier's blind cases, the baseline still
passes, nothing outside scope changed. Category: code generation (case C: existing system, clear requirement).
Pipeline: build a feature (TASK_TYPES candidate), first real run.

## Acceptance criteria (each with an example)
- R1 A node with `"workdir"` runs its engine with that folder as its working folder. Example: a script node whose
  command prints `os.getcwd()`, with `"workdir": "w/q"`, records a result containing `<root>/w/q`.
- R2 A relative `workdir` resolves against `--root`, and a missing folder is created. Example: `w/new` absent before
  the run exists after it.
- R3 A node without `workdir` runs in the repo root, as before. Example: the printed folder equals `<root>`.
- R4 The Codex adapter's `-C` names the node's working folder. Example: `--dry-run` on a codex node with
  `"workdir": "w"` prints `-C <root>/w`.
- R5 The brief, the result file and check commands still resolve against the repo root. Example: a node with
  `"workdir": "w"`, brief `brief.md` at the root and a check `python3 check.py {result}` with `check.py` at the root
  runs and passes; its result file is under `runs/<run_id>/nodes/`.
- R6 A fallback without its own `workdir` keeps the node's; a fallback with one uses it. Example: node `"a"`,
  fallback `"b"` → the fallback call runs in `<root>/b`.
- R7 `dispatch.py check` refuses a `workdir` that exists as a file. Example: `"workdir": "x.txt"` with `x.txt` a file →
  a refusal naming the node and saying it is not a folder.

## Baseline
Full suite at db1fad2, recorded per test twice (`runs/20261003-node-workdir/baseline/baseline.json`): 463 tests, all
pass, none flaky. Taken with `env -u NO_COLOR`, as CLAUDE.md says.

## Projection (written before the run)
- Calls: 4 engine calls (dev, cases, review, plus at most one repair), 4 script steps.
- Tokens: dev (Codex `gpt-6.1-sol`, medium) 150k–300k; cases (agy) 30k–80k; review (agy) 30k–80k. Total 210k–460k.
- Wall time: 10–20 min. The COO's own preparation is not counted.

## Steps
| # | Step | Status | Output |
|---|---|---|---|
| 0 | Restatement, explore, baseline, projection | done | this file, explore.md, baseline/ |
| 1 | Dispatch plan.json | todo | dispatch.json, events.jsonl, nodes/ |
| 2 | COO review of findings, docs, ledger row | todo | ledger, feedback.jsonl |

## Log
- 2026-10-03 explore.md quote-checked: 8/8 after one fix (X8 cited line 31; the quote is at 25).
