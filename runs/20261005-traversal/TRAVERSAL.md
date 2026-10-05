# Traversal — one challenge, end to end, 2026-10-05

Run to answer two questions: *is the machinery duplicated, and is it working?* Answer to both: **the tail works, the
chain does not exist.** The crossing between the design and the plan is manual, lossy, and nothing checks it.

Run dir: `runs/20261005-traversal/`. The challenge (`challenge.txt`) is real work that is still outstanding: make the
gate's challenger rule (G5) and ledger rule (G7) actually execute against the corpus. 98 words, builds code.

## What was run, in order

| step | how | result |
|---|---|---|
| 1. intake's "before" records | the real commands | baseline = `514 passed`, recorded in `baseline.txt`; pre-run git state clean |
| 2. the design | written per the method | `design.json` — **`design_gate.py` PASS** |
| 3. the plan | **written by hand** — nothing automates this | `plan.json` — **`check_plan` "plan ok"** |
| 4. dry run | `dispatch.py run --dry-run` | walked all 3 nodes; writes nothing by design |
| 5. **real run** | `dispatch.py run`, script engines so no quota | **ran to completion: 2 done, 1 blocked, 6 calls** |

## The tail works — proven, not assumed

```
s1-no-check              done     calls 3 rounds 0
s2-checked-ok            done     calls 1 rounds 0
s3-fails-then-repairs    blocked  calls 2 rounds 2
dispatch …: STOPPED — 2/3 nodes done, 6 call(s)
needs the COO: s3-fails-then-repairs blocked: check failed 2 round(s)
```

`dispatch.json` and `events.jsonl` were written. So: the dispatcher loads a plan, validates it, schedules it, **counts
retries per node**, blocks a node that exhausts `max_rounds`, stops the run, and reports to the COO. **The retry
counter is real and observable** — `rounds: 2` in the state file is exactly the number the requirement we were
arguing about would bound.

## The chain does not exist — and this is now measured, not theorised

**a. `intake.js` has no runtime here.** It is a Workflow-tool module (`export const meta`, hooks `agent`/`phase`/`log`),
and this harness's workflow tool takes an *inline* script, not a file. So its steps were enacted by hand. **A runnable
form that cannot be run in the harness it was written for.**

**b. The design→plan crossing is manual and lossy.** I wrote the plan by hand and had to supply, from outside the
design: the engine split (kind → bare name + exact model id), the model ids (prose in `EXECUTOR_KINDS` only), role
names, a brief per node with **three hardcoded sections**, timers, the budget, and repair targets.

And the crossing **silently dropped things the design had promised**:

| | design | plan |
|---|---|---|
| `n1`'s check | yes | yes |
| **`n2`'s check** | yes | **DROPPED** |
| **`n3`'s check** | yes | **DROPPED** |
| `touched_paths` | present | **absent** |
| `baseline` | present | **absent** |
| `categories` | present | **absent** |
| `estimate` | present | **absent** |

`check_plan` said **"plan ok"**. Nothing compares the two — decision C, and this is the first measurement of what C
costs.

**c. A node with no check reports `done`.** `s1-no-check` finished `status=done, rounds=0` having run no check at all.
So **"done" does not mean "checked"** — and in a real run, not a mutation.

**d. `{node}` is not a placeholder.** `build_script` substitutes only `{prompt_file}`, `{out}` and `{attempt}`. A plan
author writing `{node}` gets `node '{node}' != contract 's1-no-check'` — a pass-back error that names the symptom,
not the cause.

**e. Two state files.** The method's state is `state.md`; the dispatcher's is `dispatch.json`. Same word, different
artefact, different format.

**f. The number 2 lives in six places.** `intake.js` `MAX_ATTEMPTS = 2`, `DEFAULT_BUDGET.max_rounds = 2`, the design's
`loop.limit: 2`, `node-brief.md`'s `attempts left: 2`, `TASK_TYPES.md:44` *"Two repair attempts"*, `:192` *"at most
**2 rounds**"*. **Nothing keeps them in sync**, and the design's limit and the plan's budget are unconnected — the two
2s agreed only because I typed the same digit twice.

## What this answers

* **"Duplicate efforts?"** Yes, and specifically: the same *facts* are copied into places that must agree, with
  nothing checking that they do — the retry number (×6), the brief's sections (dispatch's hardcoded list vs the
  template), the engines (10 files), the design vs the plan (two copies of one graph).
* **"Not sure the efforts working?"** **The parts work. The assembly has never run — until now, and when it ran, it
  dropped two of three checks and reported success.**

## What it suggests

**Decision C should be revisited, and this is the evidence.** The cost of the hand-crossing is not theoretical: a real
traversal lost 2 of 3 checks, the touched paths, the baseline and the categories, and every validator said OK.

The smallest fix that would have caught all of it: **a check that takes both files and compares them** — every design
node present, its check carried, the reviewer present, the engines of the right kind. That is option A from the C
decision, and the traversal is the measurement that was missing when C was chosen.
