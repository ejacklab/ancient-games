# Workflow design — harness health in the readiness step

Run `20261015-harness-health`. Inputs: `challenge.md`, `experts/compare.md`, evidence under `evidence/`.
Everything below marked **proposed** is the main agent's choice where the experts split or EJ has not answered; each
names the expert line it follows, and EJ can overturn it at the merge.

## Decisions taken for this build

| Spot | Taken | Basis |
|---|---|---|
| U1 harnesses | All installed harnesses listed; `--harness NAME` (repeatable) narrows the lines and help; exit 1 if a named harness is not installed | all five |
| U2 help | File + key + snippet + one line on what it changes; the script writes nothing; every snippet passes a flip test in a fixture | all five; flip test: Dave, Linus, 孫子 |
| U3 good enough | A finding is `present` / `absent` / `measured` / `covered` / `unknown`. Help only where a thing the requirement names is absent. Numbers are reported with no verdict. A config line says *configured*, never *enforced* (header says so) | 孫子, 老子, 范蠡; Linus's enforcement point as the header line and the status rule below — **proposed** |
| Status rule | A line reading a key whose name was proved against the installed version (the harness rejected a bad value) is `verified`; key names known only from binary strings or another version are `reported`; an unverified format is `unknown` | 孫子 #4/#11, 老子 #8; downgrade-not-flip on version change is **proposed** (孫子/老子 asked for `unknown`; that would turn every Claude Code update into unknowns) |
| U4 location | New `scripts/harness_health.py`, reuses `readiness.Probe`-style fields; `readiness.py` only gains `dsh`, `opencode` | all five |
| U5 effects table | Not written into method 3.1 yet; proposed effects below, n=0 | Dave (defer) over 范蠡/孫子/老子 — **proposed**: no run has used it |
| U6 key names | Codex `sandbox_mode`, `approval_policy` verified on 0.160.0 (`evidence/u6-codex-keys.txt`); Claude Code keys reported from 2.1.299 binary strings (`evidence/u6-claude-keys.txt`); qwen, agy, dsh, opencode → `unknown` | all five |
| U7 per-run requirements | R2, R3, R7 (and parts of R4, R5, R9) → `covered by <script>` only if that script exists beside it | Dave, 孫子, 老子 |
| Block vs inform | Inform: findings never change the exit code | open for EJ (Q1) — **proposed** |
| Canary, drift, trap catalogue | Not in this build | open for EJ (Q2, Q5, Q6) |
| Output size | Ten summary rows, then detail lines, then help; no overall grade | 老子 |

## Proposed effects on a design (n=0 — not in method text)

| Found | Effect on the design |
|---|---|
| R6 sandbox absent for an engine a building node uses | that node's Guard stakes go one level up, or it runs read-only |
| R5 fewer than two verified engine kinds | a building node's reviewer is a script check (G6 cannot be met by an agent) |
| R8 approval set to never / dangerous-mode prompt skipped | high-stakes actions need an explicit checkpoint in the design |
| unknown for an engine the design dispatches to | the canary piece is required before that engine's first node |

## Algorithm (each step with its check)

1. **Prediction first** (Dave #3) — `prediction.md` before any probe code. *Check:* file timestamp earlier than the first commit touching `harness_health.py`.
2. **readiness: add `dsh`, `opencode`** — *Check:* test with the fake binary absent → `MISSING`; existing 26 tests still pass.
3. **`harness_health.py`** — ten requirements, Claude Code + Codex probes, unknown lines for the rest, help with snippets. *Checks:* tests in `tests/test_harness_health.py`, isolated HOME:
   - each probe: good fixture → `present`, bad fixture → `absent` (sabotage per check);
   - planted fake secret in Claude `env` and Codex `[model_providers]` never appears in markdown or JSON;
   - flip test: each snippet applied to its bad fixture (as the help text says) turns the finding to `present`;
   - config files byte-identical after a run;
   - `covered by` line goes `MISSING` when its script is removed;
   - `--harness` unknown name → exit 1; `--self-test` passes.
4. **Wire in** — one sentence in method 3.1 Tools and in SKILL.md step 1; regenerate `skills/` (`tools/export_skills.py`, required by `tests/test_skills_export.py`). *Check:* full suite passes against the recorded baseline.
5. **Run on this machine** — save output to `evidence/harness-health-this-machine.md`. *Check:* reproduces the observed facts (Claude: no deny list; Codex: no top-level `sandbox_mode`/`approval_policy`; dsh/opencode listed).
6. **Backtest on paper** (Dave #4) — the 7 recorded traps vs the built probes and vs plain readiness. *Check:* compared with `prediction.md`, misses reported.
7. **Independent review** — Codex read-only, different kind from the builder (G6), given the diff, the acceptance criteria and the evidence, not the builder's notes. *Check:* its findings are answered or fixed; the suite still passes.

## Acceptance criteria

- **AC1** readiness lists `dsh` and `opencode`; all prior readiness tests pass.
- **AC2** `harness_health.py` prints ten requirement rows on any machine, with no project path hardcoded.
- **AC3** every check that can say `absent` has a test that makes it say so (sabotage), and one that makes it say `present`.
- **AC4** no planted secret value appears in any output.
- **AC5** every help snippet passes its flip test; the script modifies no file.
- **AC6** the full suite (`env -u NO_COLOR python3 -m pytest -q`) passes, compared with the baseline taken in the worktree before the change.
- **AC7** the run on this machine matches the observed facts in `expert-question.md`.

## Engine and nodes — a deviation, stated

The skill says build work goes through `workload.py` with opencode priority. This build is one module (~300 lines +
tests); splitting it costs more than it buys (memory: "agents are whales"). **Proposed:** the main agent (Claude Opus
5.5) builds; the reviewer is Codex (gpt-6.1-sol, read-only), a different kind, so G6's intent holds. Isolation: a git
worktree on branch `feat/harness-health`; the live skill (linked into `~/.claude/skills`) is untouched until EJ merges.

## Predictability · debuggability · quality control

Predictable: one sequential path, each step's check named above. Debuggable: every line carries its proof; evidence
under `runs/20261015-harness-health/evidence/`. Quality control: sabotage per check, flip test, secret test, a
different-kind reviewer, the full baseline.
