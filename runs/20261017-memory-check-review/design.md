# Workflow design — review and enhance the memory-check tools

A design, not a run. Sequential by default. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Nothing here is built.

## Questions for EJ

| # | Question | Provisional assumption |
|---|---|---|
| Q1 | The limit for a run: a time, a number of rounds, or both (method 3.8 item 14)? | none — asked when a run starts; no limit means decisions go to EJ |
| Q2 | Is `tools/memory_index.py` in scope for fixes, or reviewed only? | in scope: memory-check calls it, and a wrong answer there is a wrong answer in the report |

## Restatement (3.0)

- **Objective:** the memory-check tools give no wrong answer against their own vision, use cases and requirements,
  and the improvements worth making are made. Done when a review round finds no new accepted finding, the
  enhancements chosen are built, and every test passes.
- **In scope:** `memory_check/` (TypeScript) and `tools/memory_index.py` (Python, the check `memory_check` calls);
  their tests; `memory_check/{VISION,USE_CASES,REQUIREMENTS}.md` where a finding shows a spec line wrong.
- **Out of scope:** the guidelines themselves (`docs/memory-system/*`: a problem there is reported, never fixed
  here); new checks no use case asks for; the session-start hook (installed).
- **Whys:** the tool is new (n=1 build, fixtures only), its first review found 14 defects, so a second pass is
  likely to find more; the owner wants fewer, better steps, so every finding and enhancement must name the use case
  or requirement it serves.
- **Category:** review + repair (a fix loop), then a small feature step.

## Blueprint

- Kind of task: fix, then feature. The product's blueprint is the folder's own `VISION.md`, `USE_CASES.md`,
  `REQUIREMENTS.md`.
- **The judge is those three documents** (R12.2): a finding is accepted only if it names the use case or requirement
  it breaks and an input that shows it. One that names none is dropped, with a line in the report.
- Baseline: `cd memory_check && bun test` (74 pass today), `tsgo --noEmit`, `python3 -m pytest -q
  tests/test_memory_index.py tests/test_memory_index_unit.py`; written to `state.md` before the first piece that builds.

## Pieces, in the order they run

| # | Piece | Engine (role) | Reads | Writes | Check that closes it |
|---|---|---|---|---|---|
| P0 | Readiness | main agent | the tools, engine quotas | `readiness.md`, baseline in `state.md` | baseline commands run; quotas recorded; one opencode free |
| P1 | Review | Codex read-only, and agy read-only as the second view (dsh returned nothing today) | the two tools, their three docs | `review/<engine>.md`: findings with severity, file:line, input, the requirement or use case broken | each file has a Findings heading; a reviewer with no usable answer is rerun once, then marked absent |
| P2 | Judge | main agent | P1's files | `findings.md`: deduplicated, each accepted (with its requirement id) or dropped (with why) | every P1 finding appears once with a verdict |
| P3 | Reproduce | Claude subagent (did not write the code) | `findings.md`, the tests' helpers | `test/review-<round>.test.ts`, one test per accepted finding | each test fails on HEAD for the finding's reason (`expect-fail --run`); a test that passes is a finding not reproduced → dropped |
| P4 | Fix | opencode (wrote the code) | the failing tests, `findings.md` | `memory_check/src/**`, `tools/memory_index.py` (if Q2) | P3's tests pass, the baseline still passes, tsgo clean |
| P5 | Verify | main agent | — | `state.md` | full suite, tsgo, the smoke report on this repo, and the read-only check (no file changed outside `--out`) |
| loop | P1–P5 again | — | — | — | **stops** when a round's P2 accepts no new finding, or the limit (Q1) is reached |
| P6 | Enhance | six experts (`experts-decide`) | the tool, the last round's state | `enhance-q/compare.md` | each proposal names its use case; at most five; the main agent picks (R12.3) and writes `enhance.md` |
| P7 | Build the picks | P3 + P4 + P5 once, for the picks | `enhance.md` | tests, code | as P3–P5 |
| P8 | Report | main agent | everything | `report.md`, criteria scored | every accepted finding and pick: fixed, or open with its reason |

## Why this shape

- **Review and repair loop, closed by an objective check (3.5):** a round ends when its reproduced tests pass and the
  baseline holds; the loop ends when a review finds nothing new — not when an engine says it is done.
- **Crossed roles:** code by opencode; tests by an engine that did not write the code; review by two engines that
  wrote neither. No piece is checked by its own author.
- **Only reproduced findings get fixed:** a finding whose test does not fail on HEAD is dropped. That keeps the loop
  from spending work on findings that are not real.
- **Parallel only at P1** (two read-only reviewers, nothing shared to write); everything else in sequence (3.7).

## What today's runs taught, built in

- Every engine call has its own timeout, given per call, not one fixed 580 s (Codex's test writing hit it).
- A reviewer that returns no Findings heading is rerun once on another engine (dsh returned one line).
- opencode briefs say "relative paths only" (it stopped twice on an absolute path) and run one at a time.
- A workflow step starts only after the files it reads exist (the research ask once ran before its question file).
- Every brief carries its Lessons section from `lessons for` (crossed-build-check refuses one without).

## How it would run

As a saved workflow, `.claude/workflows/review-enhance.js`, args `{run, tool_dirs, limit_rounds?, deadline?}`,
reusing `experts-decide` for P6 and the crossed pattern for P3–P4; with an offline harness like the other two. Cost,
from today's measured runs: about 0.7–1.2M subagent tokens per experts call, about 15–30 minutes per review-and-fix
round. Not built until you say go.
