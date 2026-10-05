# Join — step 4 ("Size") review, 2026-10-04

Four engines reviewed step 4 read-only, blind to each other, against one fixed checklist (`BRIEF.md`). This file
de-duplicates their findings, records what the COO re-ran, and separates what survived the join from what did not.

Raw outputs, verbatim: `codex.md`, `claude.md`, `agy.md`, `opencode.md`.

## Verdicts

| Engine | Model | Mode | Verdict | Its headline |
|---|---|---|---|---|
| codex | `gpt-6.1-sol`, effort medium | `-s read-only` | UNSOUND | the gate accepts a challenger with higher monetary cost and less blindness |
| claude | `claude-sonnet-5-5` | `--permission-mode plan` | SOUND WITH FIXES | G5 compares designer-declared sets and never compares blindness |
| agy | `gemini-3.1-pro-high` | `--mode plan`, tools unavailable (see Executor findings) | UNSOUND | the >3-step unsplittable task has no route |
| opencode | `MiniMax-M3.1-Flash-Preview` | `--agent plan` | UNSOUND | the >3-step branch has no terminal route; the gate compares numbers the challenger wrote |

## Agreement map

Counts are out of 4. "Verified" means the COO re-ran or re-read the cited evidence.

| # | Finding | Raised by | Verified by COO | Severity |
|---|---|---|---|---|
| A | The `>3 steps that should not be split` case has no stated route, and the diagram's `SPLIT --> S5` skips both the prompt-file/workflow decision and default-first | codex F3/F4, claude F2, agy F1, opencode F2 | yes — method `:221` vs `:226-227`; diagram `:39,41,42` | BLOCKER |
| B | "Projected run cost" has no unit: §3.4 names none, `TASK_TYPES.md:32` names three (tokens/agents/wall time), G5 reads tokens only | codex F1, claude F6, agy F2, opencode F5 | yes — `design_gate.py:175-184` | BLOCKER |
| C | The gate reads `default_estimate`/`default_coverage` from the same challenger-authored JSON, so it proves self-consistency, not "cheaper than the default" | codex F1, claude F1, opencode F1 | yes — `design_gate.py:166-188`; no code derives the default side | BLOCKER |
| D | "Same blindness" is part of equal coverage in prose, but G5 compares only the `criteria` and `checks` sets — there is no blindness field | codex F2, claude F1, opencode F6 | yes — `design_gate.py:185-188` | BLOCKER |
| E | "Provisional assumption" (method) vs "a default" (SKILL.md:93, diagram:37) — and "default" is reused in the same paragraph for the TASK_TYPES row | codex F6, claude F7, agy C1, opencode F7 | yes — three copies compared | MAJOR |
| F | The SKILL and diagram drop "or EJ flagged high risk" from the reviewer rule; SKILL also drops the model name and the whole anchors paragraph | codex F6, claude F8, opencode C9 | yes — `SKILL.md:98`, diagram `:42` vs method `:236-237` | MAJOR |
| G | "The ledger is how the defaults earn their n" does not hold: 8 rows, 0 challengers, 1 reconciled and even that one has an unmeasurable engine | codex F9/F10, claude F5, agy F4, opencode F9 | yes — counted 8/0/1; 7 say "no — token cost not measured" | MAJOR |
| H | The three code anchors justify agent-count and dispatch limits, not a three-*step* sizing threshold | codex F7, claude F4, opencode C3 | yes — `stages.py:107-114`, `registry.py:24` | MAJOR |
| I | The ledger validator is blind to 7 of its 8 rows | codex F8 | **yes — reproduced: `parse_ledger` returns 1 row from an 8-row file** | MAJOR |
| J | The 2026-10-03 CAP correction is itself wrong: `CAP=3` is also a live-concurrency cap in the hybrid path | opencode F3 | **yes — `hybrid/tools/_shared.py:141-146` counts live dispatches; `invariants.py:151` refuses at `live >= CAP`** | MAJOR |
| K | A combination pipeline cannot supply "engine and sabotage" — its table has only order, loop position and join check | opencode F8 | yes — `TASK_TYPES.md:157-158` | MAJOR |
| L | "Tiny but risky gets one independent check" mandates a hand-off that §3.2 says must pay for itself, and never mentions the script-check escape | opencode F4, claude C4 | yes — §3.2 `:193-195` vs §3.4 `:229` | MAJOR |
| M | The step-counting rule that trial 1 produced ("count only the steps the challenge needs") lives in the tiny test, not in step 4 | opencode F6 | yes — `SKILL.md:35-36` | MAJOR |
| N | Ordering: ≤3 steps → prompt file is decided before step 2's labels are consulted, so a 3-step build task skips the build default, its sabotage and the reviewer rule | claude §4/§6 | yes — §3.4 `:221` precedes the label lookup in `:231-232` | MAJOR |
| O | No precedence rule between §2's tiny test ("one sentence each") and step 4's threshold ("up to 3 steps") | opencode §6 | yes — method `:25` vs `:221` | MINOR |
| P | G6's `builds` flag is designer-set, so a `mixed` category can avoid the stricter different-kind reviewer | claude F10 | yes — `design_gate.py:189-195` | MINOR |
| Q | G5 fails a conservative claim: claim `0.20` with a recomputed `0.215` is rejected by `abs(claim - recomputed) > 0.01` | agy §6 | yes — `design_gate.py:181-182` | MINOR |

## Refuted at the join (reported, then disproved)

These are the reason the join re-checks every citation.

1. **agy F5 — "SKILL.md points to a non-existent path `references/task-types.md`."** False.
   `.claude/skills/workflow-design/references/task-types.md` is a symlink to `docs/TASK_TYPES.md`. agy had no
   tools and could not see it. Dismissed.

2. **opencode F2 evidence — "`SPLIT` has no outgoing edge."** False. `WORKFLOW_DESIGN_DIAGRAM.md:41` is
   `SPLIT --> S5`. The substantive finding (A) survives and is better stated by codex: the edge exists but leads
   to S5, skipping the default-first node `DF`. opencode's proposed fix (`SPLIT --> PF2`) is the wrong repair;
   codex's (`SPLIT --> DESIGN`) is the right one. Evidence corrected, finding kept.

3. **agy F4/C8 — "the text claims n=0 but one row is reconciled, so change it to n=1."** Misread. The `n=0`
   tags the *challenger-replacement* mechanism, and there are zero challenger rows. The one reconciled row is a
   **default**. The better correction is opencode's: state the ledger's real counts instead of a bare `n=0`.

4. **agy C3 — "the three anchors all PASS."** Too generous, and contradicted by the other three engines and by
   reading `stages.py:309`, which is a docstring, not a use site. The anchors support their narrow code
   descriptions (C3 passes on that reading) but not the step threshold (H fails).

## Executor findings (about the tooling docs, not step 4)

These came out of running the review and are worth their own line.

1. **`EXECUTOR_KINDS.md` overstates agy's read-only form.** It lists `agy --mode plan` as the read-only call
   (*reported*). Verified here: `agy --mode plan -p` **auto-denies `read_file`** in headless mode, exits **0**,
   and prints **nothing**. The log says: *"a tool required the 'read_file' permission that headless mode cannot
   prompt for, so it was auto-denied."* So any agy read-only node that must read a file fails silently unless an
   allow-rule is added under `permissions.allow`. `engines.py` already maps `"auto-denied"` to `denied`, so the
   dispatcher would catch it — but the doc's read-only row needs the caveat. This is the exact failure mode the
   same file warns about two sections later. agy was re-run with all evidence inlined and made zero tool calls;
   its evidence base was therefore *provided*, not self-fetched, unlike the other three.
2. **opencode writes non-answer text to stdout.** `opencode.md` begins `I'll read the brief first.` before the
   report. `engines.py`'s note says "Answer on stdout, banner on stderr"; a preamble also lands on stdout. The
   dispatcher reads the whole stdout as the result, so this is tolerable but pollutes the artifact.
3. **`claude -p --permission-mode plan` worked for a read-only analysis task** and did not return a plan instead
   of the answer. The doc's read-only form holds here.

## The five fixes that would remove the blockers

Ordered by what they buy. None applied — this was a review.

1. **Give the >3-step branch a terminal route.** End §3.4's second bullet: *"a task that stays one piece after
   the split test is a workflow design — the step count is a prompt to look for a split, not a gate."* Then make
   the diagram route `SPLIT` into `DESIGN`, so both >3-step outcomes hit default-first.
2. **Name the cost unit in §3.4 and make the gate agree.** Method and SKILL: *"≥20% lower projected run cost in
   tokens — the unit `design_gate.py` reads"*. Optionally extend G5 later to accept a declared metric, but do not
   leave prose with three units and a gate with one.
3. **Stop letting the challenger author the baseline.** Derive `default_estimate` and `default_coverage` from the
   named default pipeline and the labelled pieces, as G2 already derives categories from `TASK_TYPES.md`, and
   fail G5 when the default side is supplied by hand.
4. **Make coverage equality include blindness.** Add a `blind` set to both coverage records and compare it in G5;
   add a blindness row to the 4-item checklist in `TASK_TYPES.md:41-43`.
5. **Unify the wording across the three copies.** "Provisional assumption" in SKILL.md and the diagram; restore
   "Sonnet 5.5; a different kind when the design builds or EJ flagged high risk" in the SKILL; and replace the
   bare `n=0` with the ledger's real counts: *8 runs, 0 challengers, 1 reconciled, 7 with no token measurement.*

Two mechanical bugs also deserve a line each, independent of step 4's prose:

6. **`parse_ledger` must survive the comment block** in `TASK_TYPES_LEDGER.md`. It currently validates 1 of 8
   rows; `--ledger` PASSes a file that is 7/8 unchecked. Reproduce:
   `python3 -c "import sys; sys.path.insert(0,'.claude/skills/workflow-design/scripts'); import design_gate as g; from pathlib import Path; print(len(g.parse_ledger(Path('docs/TASK_TYPES_LEDGER.md'))))"`
   → `1`.
7. **Correct the 2026-10-03 CAP parenthetical.** `CAP=3` caps a plan-wide dispatch count in the Gate path *and*
   live concurrency in the hybrid path (`invariants.py:151`). So §3.7's "3 running at once" is not "our own
   number" after all — which also means the `>3 steps` anchor and the concurrency cap are the same 3, which is
   worth knowing before the threshold is defended with either.

## Cost

Four engine calls. codex ~230 KB of streamed log; opencode ~29 KB; claude and agy small. Token cost not
instrumented by the CLIs here except opencode (`--format json` reports cost per step, not used this run). Design
and review time: about 12 minutes wall clock, four calls in parallel.
