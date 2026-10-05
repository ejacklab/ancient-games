# Dispatcher layer — design (2026-10-03; n=0)

**Status: steps 1–4 built** as `.claude/skills/workflow-design/scripts/dispatch.py` (tests: `tests/test_dispatch.py`,
fake engines only, no quota). Live canary passed for Codex and agy on 2026-10-03, with sabotage failing as required
(`runs/20261003-dispatch-canary/README.md`); `qwen` passed the same day with its model verified from its own output, after a timeout fix (the whole process
group is killed). Not yet done: step 5,
the first real run.

The layer that spawns and supervises agents, so the method's rules about running a node (method 3.7–3.8) are code
that cannot be skipped, and the COO keeps planning, algorithm design, decisions, monitoring and quick fixes
(`docs/EXECUTOR_KINDS.md`, the COO). EJ adopted the direction from a friend's practice (`TODO.md`). This document
is a design for EJ's review; nothing here is built yet. Design decisions cite their evidence (method 3.8 item 12):
finding ids from `docs/research/`, a file:line, or *model knowledge* where there is none.

## 1. Restatement (method 3.0)

**Objective.** One command, `dispatch.py`, runs a designed workflow's nodes from a plan file: it starts each node's
engine with its brief, enforces timers and caps, validates what comes back, retries executor failures once on the
runs the script gate, logs every event, and writes the state file — and returns to the COO only a digest
and the decisions that are hers.

**In scope.** Engine calls through Codex, `qwen` and `agy`; the pass-back contract;
the caps; the feedback log.

**Out of scope.** Choosing the design (the COO does); judging quality (the verifier and the script gate do);
changing `ancient_games/` (its `SPEC.md` and `DECISIONS.md` are EJ's — the dispatcher lives beside it, in the
skill's `scripts/`, and is engine- and project-neutral); Workflow-tool subagents (the Workflow tool already
schedules those, and Claude nodes stay with it — EJ, 2026-10-03; the dispatcher covers only the external engines);
deciding at run time who acts
next — that is fixed in the plan (§5).

**Six whys, short.** Why: rules in prose get skipped, and the COO's context fills with orchestration (EJ's
experience, method 3.2). Why now: the pieces exist — `runlog.py`, `validate_result.py`, `harvest_run.py`,
`feature_gate.py`, `quote_check.py`. Why this shape: a deterministic script, because the checks must be free and
repeatable (method §1). Why it would fail: it becomes a second brain that makes design choices — so it decides
nothing a design did not fix in advance. Why it stops here: one plan in, one digest out. Why we would believe it:
its own tests with sabotage, then one real build-a-feature run whose feedback lands in the ledger.

## 2. What already exists (readiness, method 3.1)

| Piece | What it gives the dispatcher | Source |
|---|---|---|
| `runlog.py exec` | outer timer, start/end events, raw output to the gitignored `runs/<id>/raw/` | method 3.8 item 11 |
| `validate_result.py` | the pass-back check: header, status, node, attempt, model, evidence path | method 3.8 item 4 |
| `feature_gate.py` | the build-a-feature script gate: tests, per-test baseline, scope, must-not, tamper | TASK_TYPES step 4 |
| `quote_check.py` | explorer findings checked against file:line | method 3.8 item 10 |
| `harvest_run.py` | the engines' own records into `feedback.jsonl`; the ledger's Actual cost | feedback research option A |
| Engine facts | inner timers (`qwen --max-wall-time`, `agy --print-timeout`), exit codes (qwen 1/52/55), traps (qwen exit 0 with no file; a wrong `-m` silently runs another model) | `docs/EXECUTOR_KINDS.md`, verified 2026-10-02 |

Missing: the loop that joins them, a plan format and the state-file writer.

## 3. The algorithm (method 3.2)

```
read plan.json and state.md                         # resume: nodes already `done` are skipped
check caps: roles ≤ 5, parallel group ≤ 3            # a plan over the cap is refused, not trimmed (method 3.7)
for each ready node (needs satisfied), in plan order; a parallel group only if the plan marks it:
    engine  — exactly the one the plan names; the dispatcher makes no routing choice (§5)
    brief   — refuse to start if the brief lacks a template, an example or a standard (method 3.8 item 8)
    run     — runlog.py exec with the inner timer flag and the outer timeout from the plan
    check   — validate_result.py on the result file (model must equal the plan's)
    on executor failure (no file, empty, malformed, wrong model, timeout, exit 0 with no file):
              block the node and report it to the COO; there is no fallback (removed 2026-10-05);
              a second failure → node `blocked`, stop, report to the COO       (EXECUTOR_KINDS, mid-run rule)
    on a node's own check:
              script check (gate, tests, quote_check) → pass: `done`; fail: back to the plan's repair node,
              round counter +1; past the plan's limit (default 2) → `blocked`, report
    write   — one Log line and the node row in state.md; runlog verdict
after the last node: harvest_run.py → feedback.jsonl; print the digest (≤ 20 lines) and exit
```

The dispatcher never polls the COO and the COO never polls it: it runs as one blocking command or as a background
run that notifies her on exit (method 3.8 item 3). It stops early only for a decision that is hers: a blocked
node, a small-issue fix (build-a-feature step 6), a budget ceiling, or `UNCLEAR:` from a worker.

## 4. The plan file (what the COO writes)

```json
{
  "run_id": "20261004-feature-x",
  "budget": {"max_rounds": 2, "token_ceiling": 2000000},
  "nodes": [
    {"id": "classify", "role": "classifier", "engine": "agy", "model": "gemini-3.1-pro-high",
     "brief": "runs/<id>/briefs/explore.md", "result": "runs/<id>/nodes/explore-{attempt}.result.md",
     "inner_timer": "120s", "outer_timeout_s": 150,
     "check": {"name": "schema", "cmd": ["python3", "validate_result.py", "{result}"]}, "needs": []},
    {"id": "dev", "role": "coder", "engine": "codex", "model": "gpt-6.1-sol", "needs": ["classify"],
     "parallel_group": "build", "check": {"kind": "gate", "plan": "runs/<id>/gate-plan.json"},
     "repair": "dev", "...": "..."},
    {"id": "verify-cases", "role": "verifier", "engine": "agy", "model": "gemini-3.8-flash-medium",
     "needs": ["classify"], "parallel_group": "build", "...": "..."}
  ]
}
```

`design_gate.py` already checks a design's nodes, edges, loops and reviewer kind; the plan adds only what running
needs (engine command, timers, result path). A G-check for plans (caps, timers present,
present, brief has its three parts) belongs in `design_gate.py`, not in the dispatcher.

## 5. Who acts next is decided before the run, not during it

Forks, splits and who does what are decided at design time by the COO on the strongest model, with the method and
Ancient Games (the Gate decides how many agents and splits a list above three, `ancient_games/stages.py:109`, and
journals each decision). The plan carries the result; the dispatcher only executes it. There is no run-time routing
fork and no decision model (EJ, 2026-10-03). A decision model such as Jev pays off for high-volume, per-turn routing
(J11); a run of ours has at most five roles, a strong model decides them once, and a Gate rule is auditable where a
model's probability is not (J9, J10). The research is kept in `docs/research/20261003-jev/` and is not adopted.

## 6. Failure handling, per method

| Event | Dispatcher action | Counts against the attempt limit? |
|---|---|---|
| timeout, empty or missing file, bad header, wrong model, exit 0 with no file | block the node and report it to the COO; handoff note; second → `blocked` | no (executor failure) |
| result valid, check failed | repair node, round + 1; past the limit → `blocked` | yes |
| `UNCLEAR:` in the result | stop the node; the question goes to the COO | no |
| plan over a cap, brief missing a part | refuse to start | — |
| budget ceiling reached | stop before the next call; report | — |

## 7. Pieces to build, in order (each with its own check)

1. **Plan check** — built as `dispatch.py check PLAN` rather than in `design_gate.py`, so the runner refuses a bad
   plan itself: caps, timers, brief parts. Check: self-test with sabotage.
2. **Engine adapters**: one small function per engine that turns a node into the command line with its inner timer
   and model flag (Codex `exec -m … -c model_reasoning_effort=…`, `qwen --max-wall-time … -m …`,
   `agy --print-timeout … --model …`). Check: a dry-run mode that prints commands; a test
   per adapter. One live canary per engine, which spends quota — EJ's go-ahead (EXECUTOR_KINDS canary).
3. **The loop** (§3) with the state-file writer and resume. Check: fake engines (scripts that sleep, crash, write
   a bad header, write the wrong model) — every row of §6 has a test that fails without its handling.
4. **Gate and feedback hooks**: `feature_gate.py` as a node check; `harvest_run.py` at the end. Check: an
   end-to-end run on fake engines produces `feedback.jsonl` and the digest.
5. **First real run**: one small build-a-feature (case C) with a projection written before it; the ledger gets its
   first row (feedback research, first measurement).

Steps 1–4 need no quota; 2's canaries and 5 need EJ's go-ahead.

## 8. Decisions for EJ (decided: no run-time routing fork, no decision model — §5; it lives in the skill's
`scripts/`; Claude nodes stay with the Workflow tool — EJ, 2026-10-03)

1. The default inner and outer timers per role (method 3.8 item 2 gives provisional sizes).

## 9. What the build settled, and what is still unverified

- Each node's result is the engine's final answer, so read-only engines need not write files: Codex via `-o`,
  `qwen` from the `result` event of `--output-format json`, `agy` from stdout.
- The model check uses what the *tool* reports (`qwen`'s `system` event), never the worker's own header line; Codex and `agy` report none here, so their nodes are logged
  "model unverified" and `harvest_run.py` reads the Codex model from its rollout afterwards.
- Timers have no hidden defaults: a plan without `inner_timer` and `outer_timeout_s` is refused (decision 1 stays
  EJ's).
- A run that mixes Claude and external nodes is split by engine: the COO runs the Claude nodes with the Workflow
  tool and the external ones with `dispatch.py`, in the design's order; both write results to `runs/<id>/nodes/`,
  so the next node reads a file either way.
- The Codex and `agy` command lines are verified by the live canary (n=1 each). The canary also changed the
  dispatcher: it fills `started`/`ended` itself, gives engines `stdin=DEVNULL`, keeps output printed before a
  timeout, treats `agy`'s exit-0 print-timeout notice as a timeout, and kills the whole process group on a timeout
  (qwen's child process survived a plain kill). A per-node `workdir` now exists (built in the first real run,
  `runs/20261003-node-workdir`): give a `qwen` node an empty working folder so it does not load the repo's context. `--dry-run` prints them for review.
- The dispatcher writes `runs/<id>/dispatch.json` and `events.jsonl` and never edits the COO's `state.md` (one writer
  at a time, method 4).
