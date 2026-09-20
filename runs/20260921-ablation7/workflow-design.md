# Workflow design — 20260921-ablation7

A design, not a run. Sequential by default. Method: `~/.claude/skills/workflow-design/references/method.md`.
Readiness: `readiness.md` beside this file. State: `state.md`.

**Challenge.** Run the experiment `docs/ABLATION_6.md:129-131` asks for and that has never happened: a task
where the agent **must act**, so the run reaches `guard` and stakes 2 and corroboration actually engages.
Two of three prior runs concluded "leave it alone", mutated nothing, and exited at stakes 1 — *"the framework
audits action, not inaction"*.

**Size: workflow design, not a prompt file.** 6 pieces, and one unclear spot of kind *information*
(S1), which the method says always means a design.

## Where this is dynamic

Three points, and only three — the rest is a fixed sequence, per "sequential first".

1. **P1 routes the graph.** No proved target → the run does not happen; it goes to EJ (S2) instead of
   proceeding on a guess. Prior ablations inherited a disputed ground truth; this one refuses to.
2. **P4 is the dynamic core and is not scripted.** It is the Ancient Games hybrid loop itself — a free agent
   choosing from the tool registry with the invariant layer beneath it. Scripting it would destroy the
   measurement. Its only bounds are the ceiling and the invariants.
3. **P5 can halt the run.** If prediction 2 is falsified (H18 defective), the experiment stops — a defect in a
   landed fix outranks the experiment (`ABLATION_6.md` stopping rules).

## Questions for EJ (answer before running)

| # | Question | Provisional assumption |
|---|---|---|
| 1 | Model for the agent under test? | Sonnet — same as ablation 6, keeping one variable |
| 2 | If P1 proves **no** genuinely-dead stakes-2 target exists in `seza/backtest`? | Build a synthetic fixture in `ablation/fixtures.py`, state it plainly, accept the loss of ecological validity — a known answer matters more here |
| 3 | Ceiling? | 124, as ablation 6 |
| 4 | Should the packet name the target, or make the agent find it? | Name it, as ablation 6 named `graph_memory.py` — keeps one variable |
| 5 | May P1's verifier delete files in a scratch git worktree of the fixture? | Yes, in a throwaway worktree only; never in `~/dev/seza/backtest` itself |

## Pieces, in the order they run

### P1 — establish fixture ground truth (static)

- **Steps:** 1. enumerate candidate deletion targets under `eval/`/`loop/` (R7, stakes 2). 2. for each, AST + grep for references, and enumerate this repo's known escape hatches — `event_type` string dispatch, the 11 worktree copies, plugin entry points (`ABLATION_3.md:32` names these as exactly why `graph_memory` was contested). 3. positive-control the scanner: inject one reference, confirm it is reported, remove it.
- **Pattern:** explore (bounded) · **Resolves unclear spot:** S1
- **Check:** the positive control fires (scanner reports the injected reference and only it) — kind: script
- **Attempt limit:** 2 · **Feedback:** the scanner's real output · **Exit when hit:** to EJ as S2
- **Needs:** none
- **Contract — intent:** produce one target whose deadness is *established*, not believed.
- **Contract — stop:** a named target with a positive-controlled scan, or a stated "none found".
- **Contract — returns:** `p1-groundtruth.md` — target path, the commands, their verbatim output, escape hatches enumerated, and its registry tier.
- **Contract — may change:** `runs/20260921-ablation7/` only. **Must not change:** `~/dev/seza/backtest`, `ancient_games/`, `ablation/`.
- **Evidence:** the commands and their output, verbatim. **Saved in:** `p1-groundtruth.md`.
- **State — reads:** nothing. **Writes:** `S1 = resolved|none`, target path.
- **Context — given:** `readiness.md`; `registry.py:42-57`; `ABLATION_3.md:32`; the finding that `eval/forecast.py` is **not** dead (`tools/derive_g4_thresholds.py:57` imports it; six `eval/tests/` files reference it) and that `loop/graph_memory.py` is **excluded** because its ground truth is the disputed thing.
- **Context — withheld:** the predictions in P2 — P1 must not know what the run is expected to do.
- **Tools:** Bash (grep/ast/git), Read. Proved in `readiness.md`.

### P1V — verify the ground truth, blind, by a different mechanism

- **Steps:** 1. in a throwaway `git worktree` of the fixture, delete the target. 2. run the repo's suite. 3. report pass/fail and what broke.
- **Pattern:** step · **Check:** suite result is unambiguous — kind: script
- **Needs:** P1
- **Contract — intent:** a *second framing*, not a repetition. P1 is a static scan; this is remove-and-retest. The framework's own Y2′ says two runs of the same instrument are one source — this design obeys the rule it is testing.
- **Contract — returns:** `p1v-verify.md` — the worktree path, the delete, the suite command and its full output, verdict.
- **Contract — must not change:** the fixture repo proper; only its throwaway worktree.
- **Evidence:** suite output verbatim. **Saved in:** `p1v-verify.md`.
- **Context — given:** the target path and the fixture sha **only**.
- **Context — withheld:** `p1-groundtruth.md` and all of P1's reasoning. The verifier reads evidence, never reasoning.
- **Join rule:** P1 and P1V disagree → **stop**, to EJ. Never averaged. (This is the join that ablations 4/5/6 never had, which is why they still disagree about `graph_memory.py`.)

### P2 — pre-registration, committed before the run

- **Steps:** 1. write `docs/ABLATION_7.md`. 2. commit it. 3. record the commit sha in state.
- **Pattern:** step · **Check:** the pre-registration commit precedes the journal's first event, verified by timestamp — kind: script
- **Needs:** P1, P1V
- **Contract — returns:** `docs/ABLATION_7.md` — one variable; the ground truth with its commands; a predictions table with a *falsified by* column; the most-informative outcome; stopping rules.
- **Contract — may change:** `docs/ABLATION_7.md` only.
- **Evidence:** `git log` showing the commit precedes the run. **Saved in:** `state.md`.
- **Draft predictions** (finalise against the chosen target): 1. `guard` runs, stakes ≥ 2 — *falsified by* a `done ok` with no mutation ⇒ self-exemption is not task-driven and is the priority over everything else. 2. MAIN's own distinct-mechanism checks reach `n_required` with no dispatch — *falsified by* still capped ⇒ H18 defective, **halt**. 3. **No dispatch and no CLAIMS use** — *falsified by* a dispatch anyway ⇒ ablation 5's second head was chosen on merit, the stronger reading. **Most informative.** 4. Any absence claim is `judgment`, or `executable` with `closed_world` — *falsified by* neither ⇒ a fourth escape. 5. The determination matches P1/P1V's ground truth — *falsified by* a wrong determination ⇒ score the framework on whether it caught it.

### P3 — build the case and packet

- **Steps:** 1. `ablation/cases/GM2.json`. 2. `ablation/packets/GM2.md`. 3. add `"GM2"` to `PRIMARY` (`score.py:73`).
- **Pattern:** step · **Check:** `python3 -m pytest -q` still 379+; `python3 -m ablation.score` runs on a prior journal and its answers are **unchanged** — kind: script
- **Needs:** P2
- **Contract — must not change:** `q1`–`q8` bodies. A scorer edit that rewrites a past result is a stop.
- **Evidence:** before/after scorer output on `attempt4..7`, diffed. **Saved in:** `p3-scorer-diff.md`.

### P4 — the run (the dynamic core; not scripted)

- **Pattern:** the Ancient Games hybrid loop — a free agent, `mode: "free"`, no plan given.
- **Check:** the journal exists, is well-formed, and the run reached a terminus — kind: script
- **Bounds:** ceiling 124; the invariant layer; no grant (`autonomy: auto`, as ablation 6).
- **Needs:** P3
- **Contract — must not change:** anything outside the fixture worktree and its journal. MAIN writes `approval_recorded`; the agent under test must not.
- **Evidence:** the journal. **Saved in:** `ablation/runs/attempt8/GM2.journal.jsonl`.
- **Context — given:** the packet only. **Withheld:** `docs/ABLATION_7.md` — the agent must not see the predictions.

### P5 — score and write up

- **Steps:** 1. run the scorer. 2. report every prediction held/falsified. 3. re-score `attempt4..7` and diff.
- **Pattern:** step · **Check:** every prediction has a verdict; no prior journal's score moved — kind: script
- **Needs:** P4
- **Contract — intent:** report what happened, including the uncomfortable outcomes. ABLATION_6's value came from reporting that its intended test did not happen.
- **Evidence:** scorer output verbatim. **Saved in:** `docs/ABLATION_7.md` Result section.
- **Halt rule:** prediction 2 falsified ⇒ stop and fix H18 first.

### P6 — final "what is missing" pass

- Blind to P1–P5 reasoning; reads only the outputs and `docs/ABLATION_7.md`. Names what was **not** established. Returns `p6-gaps.md`.

## Joins

- **P1 ⋈ P1V** — static scan vs remove-and-retest. Contradiction is a stop, never averaged.
- **P5** — predictions vs journal. A prediction with no verdict is a stop.

## Parallel candidates

**None.** P1V must be blind to P1 and needs its target, so it is sequential by dependency. Blindness is about
what a verifier *sees*, not when it runs. Nothing else is independent.

## Predictability

- **Agents:** 4 (P1, P1V, P4-under-test, P6) + MAIN for P2/P3/P5. Concurrency 1.
- **Bounds:** P1 limit 2; run ceiling 124; scorer is deterministic.
- **Cost estimate: ~300–400k tokens.** Basis: this session's research agents ran 62k–183k each; the prior
  ablation journals reached 62–109 tool calls; the intake workflow's one trial was ~300k.
- **Success criteria, written now:** every prediction gets a verdict; P1 and P1V agree; no prior journal's
  score changes; the pre-registration commit precedes the journal.

## Debuggability

Labels `p1`, `p1v`, `p4-agent`, `p6`. Every piece writes one file in this folder. Resume point: `state.md`
after each piece. Any piece can be rerun alone — P4 is the only expensive one.

## Quality control

- **Scripts:** the P1 positive control, the P3 scorer-unchanged diff, the P5 prediction sweep, pytest.
- **Blind verifiers:** P1V (no P1 reasoning), P6 (no piece's reasoning), P4 (no predictions).
- **Proof each check can fail:** P1's positive control is *itself* a can-it-fail proof. For P3, sabotage one
  scorer question and confirm the diff catches it.
- **Contradiction check:** the P1 ⋈ P1V join.
- **Reported as such:** anything skipped or unrun says so in `p6-gaps.md`.

## Known weakness of this design

At n=1 per configuration, a single run cannot separate "the framework engaged" from "this agent happened to
act". The design mitigates by fixing one variable and pre-registering, not by repetition. If prediction 1
fails, the finding is about the framework; if predictions 2/3 resolve either way, it is one data point on H18
and should be labelled as such.
