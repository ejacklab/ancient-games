# The full algorithm, one pass — four engines, 2026-10-04

Reviewing the workflow-design **algorithm overall**, not step by step. EJ's reason, and it is the right one: a human
divides because working memory forces it, but dividing *destroys exactly the defects worth finding* — the ones that
live between steps. This run tests that claim, and the claim holds.

## How it was run

All four engines, blind to each other, one brief, **the whole algorithm inlined into the prompt** (946 lines,
~21 k tokens) rather than left on disk:

- `docs/WORKFLOW_DESIGN_METHOD.md` — the method, 3.0-3.8 then 4 and 5
- `.claude/skills/workflow-design/SKILL.md` — the same algorithm packaged as a skill
- `docs/WORKFLOW_DESIGN_DIAGRAM.md` — the same algorithm as diagrams, plus its step-numbering table

| engine | model | mode | time | findings |
|---|---|---|---|---|
| agy | `gemini-3.8-flash-high` | `--mode plan` | 111 s | 5 |
| claude | `claude-opus-5-5` | `--permission-mode plan` | 81 s | 16 |
| codex | `gpt-6.1-sol` | `-s read-only` | 98 s | 5 |
| opencode | `MiniMax-M3.1-Flash-Preview` | `--agent plan` | 248 s | 9 |

**35 findings, 35 quotes verified against the real files, 0 fabricated.**

Inlining is why agy could take part at all. In the step-1 review it produced nothing — headless agy auto-denies the
`command` permission it needs to read a file, and the escape it suggests (`--dangerously-skip-permissions`) is the
flag rule 3 forbids. Given the same evidence *in the prompt* and told to use no tools, agy answered in 111 s. The
technique is another session's (`runs/20261004-step4-review/AGY_APPENDIX.md`); it is now proven twice, and it
matters because rule 2 routes `repo scanning`, `web search` and `research and reports` to agy.

Inlining has a second benefit: every engine reviews an identical evidence base, so a disagreement is about judgement
rather than about who could open which file.

## The findings, by the question asked

Corroboration is counted, not asserted. "n/4" means n engines independently cited that place for that question.

### 4/4 — the engine split exists only in the skill, and it silently added a fourth quality

Four engines, one place: `SKILL.md:175`. I added that bullet today. It requires a pre-run allocation
(`scripts/workload.py`, opencode priority) and refuses a plan where a verifier shares its node's engine — and
**neither the method nor the diagram mentions it**:

```
grep -ciE 'workload\.py|engine split|opencode' docs/WORKFLOW_DESIGN_METHOD.md     -> 0
grep -ciE 'workload\.py|engine split|opencode' docs/WORKFLOW_DESIGN_DIAGRAM.md   -> 0
grep -ciE 'workload\.py|engine split|opencode' SKILL.md                          -> 1
```

Consequence, as claude put it: the method's §5 is titled *"Three qualities every design must show"*
(`WORKFLOW_DESIGN_METHOD.md:476`) while the skill's finish checklist now has **four** items. A design made from the
skill and a design made from the method no longer have to show the same things. **Verified.**

### 3/4 — the baseline has no owner

`WORKFLOW_DESIGN_METHOD.md:295-296`, found by agy, claude and opencode. A building node's three-part stop requires
regressions against "the baseline recorded in the state file before the first piece that builds" — but **no step
captures it**. 3.1 does not require it, 3.4 does not size it, 3.6 assumes it. Nothing decides what happens when the
baseline is already red or flaky. So a required precondition of every build node's stop condition is produced by
nobody. **Verified by reading 3.1 and 3.6 against each other.**

### 2-3/4 — the final "what is missing" pass has no owner

`WORKFLOW_DESIGN_METHOD.md:306`, found by claude and opencode (claude also at `:306` from §5). Both §5 and 3.6
demand a final "what is missing" pass; no step places it in the graph, gives it an engine, an attempt limit or a
position. A design can omit it and still be complete by every other rule. **Verified.**

### 3/4 — step 5 dispatches work before steps 6 and 7 define the graph and the caps

`WORKFLOW_DESIGN_METHOD.md:245` (opencode, codex) and `SKILL.md:102` (codex). Step 5 "runs clear pieces as loops"
while the unclear spots are still being resolved — but nodes, edges, the 5-role cap and the 3-at-once cap are all
defined in 3.6 and 3.7, after it. So the work that runs concurrently is unbounded at the moment it runs.
**Verified by reading the step order.**

### 2/4 — the algorithm's central promise is broken for one whole class of task

`WORKFLOW_DESIGN_METHOD.md:131`, found by agy and opencode. The algorithm promises a run "ends at the acceptance
criteria", and separately says non-product-change tasks carry none. Those two sentences cannot both hold, and no
step defines the stop condition for that class. **Verified by reading both.**

### Confirmed singles worth acting on

- `WORKFLOW_DESIGN_DIAGRAM.md:19` and `WORKFLOW_DESIGN_METHOD.md:24` (codex, claude) — **the tiny-task exit skips
  readiness**, so a small *product* change builds without the blueprint acceptance criteria or the baseline. Both
  reviewers flagged this as high, from two different files.
- `WORKFLOW_DESIGN_METHOD.md:333` (claude) — the caps (5 subagent roles per run, 3 at once) appear only in the
  method; neither the skill's step 7 nor the diagram carries them.
- `WORKFLOW_DESIGN_METHOD.md:426` (opencode) — item 12's gate ("a design decision with no finding id may not drive a
  node that builds") exists only in the method.
- `WORKFLOW_DESIGN_METHOD.md:382` (claude) — nothing decides a node's fallback engine, stronger-tier model or
  attempt-limit value, though both the executor-failure rerun and the tier exit depend on them.
- `WORKFLOW_DESIGN_METHOD.md:314` (codex) — no run-wide replan limit, so returning exhausted nodes to planning can
  renew their local budgets indefinitely.
- `SKILL.md:172` (claude) — the skill weakens "proof the check can fail" to *script* checks only, exempting
  checklist and EJ-judged checks, which 3.5 item 5 does not.
- `WORKFLOW_DESIGN_METHOD.md:358` (opencode) — the five-things promise says a node can be run "without asking
  anyone", but 3.8 requires timers that the five things do not include.

### My error, found by the review

`WORKFLOW_DESIGN_DIAGRAM.md:213` (claude) — **the mapping row I added hours ago is wrong.** I wrote that method 3.8
has "**no step**" in the skill. It has no *dedicated* step, but its content is inline in skill step 7:

```
tools (method 3.8): one small bounded task per call, an inner and an outer timer named in the node, no polling
```

So the skill does carry 3.8 — inside step 7 — and my row overstated the gap. That is the second thing I wrote today
that a reviewer corrected, and the second time the correction came from reading two artifacts against each other.

## What this proves about reviewing overall vs step by step

The findings that matter most are the ones **no single-step review can produce**:

- the baseline is required by 3.6 and produced by no step — that is a *relationship between two steps*;
- the "what is missing" pass is demanded by §5 and owned by no step — the same shape;
- step 5 runs before steps 6-7 bound it — an *ordering* property of the whole;
- the engine split is in one of three renderings — a *cross-artifact* property;
- the tiny-exit bypasses readiness — a *branch interacting with a later step*.

The step-1 review, bounded and careful, produced 24 findings and not one of these. It could not: every one of them
is invisible from inside a single step. **EJ's instinct was right and my earlier advice was wrong** — the overall
pass is not a convenience for a large context window, it is the only pass that can see composition at all. The two
reviews are complementary, not alternatives: step-level gave the check-that-cannot-fail and the status vocabulary,
overall gave the ownership and ordering defects.

## Files

- `build_brief.py` — assembles the inlined brief; reusable for any whole-algorithm review
- `brief-overall.txt` — exactly what all four engines were given (946 lines)
- `run.sh` — the four calls with each engine's read-only mode and model
- `verify.py` — quote verification, and grouping by question letter with counted corroboration
- `agy.out`, `claude.out`, `codex.md`, `opencode.out` — raw, unedited
- `canary.out` — the agy canary that proved the inlined format works

## Not done

Nothing was fixed, including my own two errors. The algorithm review has produced a defect list that spans four
files and at least three renderings; which of them to change, and in what order, is a decision rather than a
cleanup, and several (the ordering of steps 5-7, the ownership of the baseline) change the algorithm rather than
correct a mistake in it.
