I'll read the brief first.
# 老子 (Laozi) — where memory-check belongs in the workflow-design method

## Answer

Put it in **step 3.1 (readiness)**, inside the Information check that step already has (`docs/WORKFLOW_DESIGN_METHOD.md:114-116`), run once before the run beside `readiness.py` / `harness_health.py` / `doctor` (`:103-110`) — not a new step, not per node, not at the end of the run.
A **fail** stops the run only when the task's nodes will actually read that memory (my reading); **needs a reviewer** and **not applicable** carry on; **could not run** is recorded with its reason.
Nothing in the method becomes redundant — §4's per-node rule already says what an end-of-run check would say (`:610`).
If EJ says yes to the session-start hook (`runs/20261017-memory-check/settings-diff.md:37`), 3.1's line duplicates it and should be dropped, not kept.

## How I decided

1. **The question is a subtraction, not an addition — my #1.** 「損之又損，以至於無為」 (`quoted`). 3.1 already has the row for this exact case: "There, but not verified | Add a small piece that checks it against the source" (`:125`). memory-check is that check, written once and kept. Placing it as a line in 3.1 spends nothing; a new numbered step spends a step on every design forever.

2. **Inside the Information bullet, not Tools — my reading.** That bullet already asks "is the knowledge there; what structure is it in (… a memory folder …); and which agents and tools can actually use that structure" (`:114-116`). That is what the tool answers. `readiness.py` and `doctor` answer the Tools half.

3. **Before the run, not per node and not after — my #6.** 「為之於未有，治之於未亂」 (`quoted`).
   - Per node multiplies one read-only check by the node count, and on this repo 72 of 78 records are "not applicable" (`runs/20261017-memory-check/nodes/smoke-report.md:128`) — 72 lines per node, for nothing.
   - At the end of the run it repeats §4's State rule: the node that writes an entry regenerates `INDEX.md` in the same commit and its check fails if a required entry is missing (`:610`). My #3 — 「功遂身退，天之道」 (`quoted`): when the work is done, withdraw the extra run.
   - My #17 — 「三十輻共一轂，當其無，有車之用」 (`quoted`): on a repo with no `project-memory/`, the report's value is that it *names* the absence, and §4 already says what happens then (`:600-604`; C4, `memory_check/REQUIREMENTS.md:46-48`). Absence is information, not a failure.

4. **What 3.1 does with each of the five states (C2, `memory_check/REQUIREMENTS.md:35-39`):**
   - **pass** — record the report path in the state file; nothing else. My #2 — 「知足不辱，知止不殆」 (`quoted`): §5 requires skipped or unrun checks reported (`:632`), not passed ones explained.
   - **fail** (exit 1, R3 `REQUIREMENTS.md:73`) — **stop and ask EJ**, the shape the method already uses for a wrong premise: a wrong task kind (`:165-167`) and a label that contradicts what a piece writes (`:218-220`). Conditional, my reading: the stop is for a failing MUST whose memory the task's nodes receive through Context; §4 already has a node report an entry that no longer matches the code to EJ rather than settle it (`:609`), so a break nobody reads is a note.
   - **needs a reviewer** — carry on with a note. My #8 — 「知不知上，不知知病」 (`quoted`): a reviewer record is the owner's judgement (`memory_check/VISION.md:18`), so it must not be promoted into a gate, or a run stops on the owner forever. My #2 again: 「知止不殆」.
   - **not applicable** — say nothing. My #2 — 「禍莫大於不知足」 (`quoted`): nothing to judge, nothing to do.
   - **could not run** — record the reason and carry on (§5, `:632`).

5. **Two things the method must not do — my #14.** 「不自見故明」 (`quoted`). It must not restate a memory requirement as a check of its own: §4 already says the method does not repeat the guidelines' rules (`:596-598`), and the tool "adds no rule of its own" (`VISION.md:18`). And it must not treat a pass as a design decision — the tool checks *its own* copies of the guidelines and prints their versions (`smoke-report.md:3`; C1, `REQUIREMENTS.md:32`), so that version belongs in the state file, or the pass is a pass against a rule set nobody read. My #8: the check's own limit is part of its result.

6. **Session start is where the others already put it — my #19** (「人皆取先，己獨取後」, `attributed`). U3 and R2 put the warning at session start (`memory_check/USE_CASES.md:22-26`; `REQUIREMENTS.md:66-71`), and that hook still waits for the owner's yes (`settings-diff.md:37`). The method's place is the moment no hook covers: the start of a run. If the hook is installed, 3.1's line duplicates it and my #1 says remove the line rather than keep both.

**Proposed change to the pattern.** The pattern has no line for *where a finished check goes*. Proposed: when a tool arrives, the first candidate placement is a line inside an existing step, and a new step must name what no existing line catches — the same test 3.3 already puts to 老子 ("which spots can be answered by giving up a step rather than by resolving it?", `docs/WORKFLOW_DESIGN_METHOD.md:257`). It would change: one clause in that 3.3 line ("and which step absorbs a new check"), so a placement question is answered by subtraction first.

## What I need to know

1. **Does any project of EJ's have `project-memory/` today?** On this one the tool reports 0 fail, 3 pass, 3 needs a reviewer, 72 not applicable (`smoke-report.md:128`). If no project has one, this placement is decided by reading only, and the first project that does is its test — run it there before the method changes. If one does, the answer stands on measurement instead.
2. **Does EJ say yes to the hook** (`settings-diff.md:37`)? Yes → 3.1's line is redundant and is dropped (my #1), and the method gains nothing and loses nothing. No → 3.1 runs `--warn` itself and the hook stays a proposal.
3. **Are the tool's guideline copies the repo's `docs/memory-system/` files, or its own frozen copies** (C1, `REQUIREMENTS.md:32`; printed at `smoke-report.md:3`)? Own copies → 3.1 must record the printed hash.
4. **Do this project's task nodes actually load entries** (Context, `:608`)? That is the fact that turns a fail from a note into a stop.

## Costs and risks

- **A stop on any fail can halt a run whose task never reads the broken memory — my #4.** 「為者敗之，執者失之」 (`quoted`): acting on the whole ruins it. Price: narrowing the stop to memory the task reads moves a judgement into 3.1.
- **3.1's cost guard says the step is one paragraph and six short answers, no tool calls** (`:89-90`). A fourth script cuts across that unless it is read-only and cheap: `--warn` printed nothing and exited 0 here (`settings-diff.md:30`), but the full report printed 78 records. So 3.1 gets `--warn`, and the report only when the warning is not empty. My #2: enough is enough.
- **The tool's reviewer list includes a MUST** (SoT:W3.5a, `smoke-report.md:112-116`). If 3.1 ever counts it as a gate, the method stops runs on a judgement the tool cannot make — my #8.
- **Any rule keyed on the result states will be misread on this repo:** 72 of 78 not applicable, so reading the report as a finding is wrong here by measurement — my #17.
- **Rule drift:** the tool checks its own copies and prints their versions (`smoke-report.md:3`). A stale copy turns 3.1's pass into a pass against yesterday's rule — my #8.

## How we would know I was right

1. On a project with `project-memory/`, plant one failing MUST the task reads and one it does not. Predicted: the first stops at 3.1 with EJ asked; the second is a note and the run proceeds. If both stop, my #4 is real and the narrowing is required.
2. Count `--warn`'s lines and seconds in a clean repo. Predicted 0 lines, exit 0 (`settings-diff.md:30`). Visible added time means the cost guard (`:89-90`) is broken.
3. Run the next real design through 3.1 with the line present and count the unclear spots it creates. Predicted: none. A spot would mean the tool was answering a question 3.1 already asked by another route.
4. This repo is already one data point: 0 fail, 72 not applicable (`smoke-report.md:128`) — so any placement that stops here is wrong by measurement.
