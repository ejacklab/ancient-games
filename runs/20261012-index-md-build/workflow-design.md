# Workflow design — 20261012-index-md-build

A design, not a run. Sequential by default. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Written 2026-10-12 by the COO
(Claude `claude-opus-5-5`) at EJ's request: *"design a workflow to complete teh whole SDLC of this index dev and
test"*. Nothing here has run. State: `state.md`. Tools proved: `readiness.md`. Gate input: `design.json`.

## Questions for EJ — answered 2026-10-12

| # | Question | EJ's answer | What it does to the design |
|---|---|---|---|
| Q1 | The three files in `docs/index-md/` say *"draft, not accepted by EJ"*. Do we build against them as they are now? | *"as you suggest"* | We build against the drafts. N0 records their sha256. Open items stay as the files handle them: B4's limits stay example constants, G4.1 is not built, and the B/C/G names do not matter to the code. If another session changes a file mid-run, the run stops and only the nodes that file touches are planned again. |
| Q2 | `workload.py` has opencode write both the script and its tests (*ran*: `script opencode/opencode NO (self-tested)`). Override it? | *"we can have another diff test"* | *My reading:* keep `workload.py`'s split and add a second, different test set. opencode writes the code **and its unit tests** (N2, `tests/test_memory_index_unit.py`). Codex writes the **acceptance tests** blind, before any code (N1, `tests/test_memory_index.py`, the file C2 names). opencode does 2 of the 3 build nodes; the script still gets independent tests. *Not read:* "diff" as differential testing (two implementations compared); if that was meant, N1 changes. |
| Q3 | Where do findings outside the requirements go? | *"follow what you suggest"* | `docs/index-md/BACKLOG.md`, created when the first finding comes in. |

Defaults, not questions, each a one-line decision:
- **MAX_BYTES = 24,000.** This quotes the source: *"24,000 bytes per rule file"* (`docs/memory-system/CACHES.md:519`,
  the agy row). MAX_LINES = 200 (Rd3.1). Both are marked as examples in the code, as B4.1 requires.
- **Write mode with no `project-memory/` folder:** it exits 0 with "nothing to index" and creates nothing. This mirrors
  C1.3 and keeps DESIGN's rule *"do not create `project-memory/` in this repo"* safe if someone runs it here.
- **Any behaviour the requirements do not state** (for example a header with the same key twice) is neither tested nor
  decided. It goes to the backlog list.
- **Commit, merge, push:** only when EJ says so. The run ends with a branch and its evidence.

## Restatement (method 3.0)

**Objective.** `tools/memory_index.py`, `tests/test_memory_index.py`, `.githooks/pre-commit` and
`.githooks/pre-merge-commit` exist on a build branch, with the coder's own `tests/test_memory_index_unit.py` beside them (Q2). Every **Fails if** in `REQUIREMENTS.md` that is in scope has a
test, and each of those tests is shown to fail on a broken script. The repo's own suite still passes.
**In scope:** the four files that DESIGN's "For the builder" lists, plus the unit test file (Q2). **Out of scope:** DESIGN's *"Do not, without EJ's
go"* list (`SOURCE_OF_TRUTH.md`, `CLAUDE.md`, `AGENTS.md`, `git config core.hooksPath`, creating `project-memory/`);
G1.2 (the instruction line), the open G4.1 and B4 decisions, and editing the spec files.

**Whys.**
1. Problem: a hand-kept index drifts, and one shared file conflicts across branches (VISION).
2. Now: the algorithm run ended ACCEPT WITH FIXES, and EJ split the build into this session.
3. Shape: the design is already written, so this is build plus test, not research.
4. Failure: a wrong index silently hides memory from every session, and a nondeterministic one churns on every
   machine. Risk is **medium**. Nothing is live (the hook stays off, `project-memory/` does not exist), so every step
   can be undone, but a defect would show up late, in other sessions.
5. Stop: at DESIGN's builder list. Turning the hook on and editing the instruction files are EJ's next step.
6. Done: the three-part stop. Each criterion's test passes and is proved able to fail, the baseline passes, and "must
   not change" holds.

**Provisional category** (*inferred*): code generation + test cases gen + code review, the "codegen → tests → review"
pipeline and the candidate "build a feature", **case C** (an existing repo gets a feature).

## Blueprint

- Kind of task: **feature** (a new tool in an existing repo). Map: none. The spec lives in `docs/index-md/`:
  `VISION.md` = vision, `REQUIREMENTS.md` = requirements, `DESIGN.md` = architecture and business logic. All three are
  **draft** → Q1.
- Acceptance criteria in scope: **B1.1 B1.2 B1.3 · B2.1–B2.6 · B3.1–B3.4 · B4.1 B4.2 B4.3 B4.4 · C1.1–C1.4 · C2.1
  C2.2 · G1.1 · G2.1 G2.3 · G3.1 G3.2 · G4.2**.
  - Not in scope: G1.2 and G2.2 (both on EJ's do-not list), G4.1 (open), and B4's "Open" line.
  - G1.1 is in scope only through C1, the check that catches it, as its Fails if says.
- Baseline: `env -u NO_COLOR python3 -m pytest -q`. On 2026-10-12 it gave **529 passed in 31.61 s** (*ran*, in the
  main tree). N0 records it again, per test, in the worktree.
- A piece that builds stops when its criteria pass, the baseline still passes, and its "must not change" holds. A
  failure of any of the three is a failed attempt. Anything else goes to the backlog (Q3), not into this run.

## The algorithm (method 3.2)

| # | Step | Check |
|---|---|---|
| 1 | Pin the spec, open a worktree, record the per-test baseline, run the engine canaries | hashes, two JUnit runs, `feature_gate.py baseline`, canary result files |
| 2 | Write the acceptance tests from the spec alone (no code exists) | collects; every criterion id is cited by a test; every test is red with no script |
| 3 | Write the script and the hooks against the frozen tests | `feature_gate.py check`: new tests green, baseline green, scope, must-not, tamper |
| 4 | Prove the tests can fail: one hidden mutant per Fails if | each mutant turns at least one test red |
| 5 | Blind review of the diff against the spec, with one planted defect | the plant is found; findings carry file:line |
| 6 | Final pass: traceability, must-not-change, docs unchanged, feedback, ledger | a matrix with no empty cell; full suite green |

Pieces (method 3.2, "a label is not a node"):

| Piece | Steps | Deliverable | Category | Default (TASK_TYPES) | Node |
|---|---|---|---|---|---|
| prep | 1 | baseline, worktree, canaries | — (step-level shell work) | — | N0, COO |
| tests | 2 | `tests/test_memory_index.py` | test cases gen | single node + review; split by `workload.py` | N1, Codex |
| code | 3 | the script and the two hooks | code generation | evaluator–optimizer loop; split by `workload.py` | N2, opencode (loop) |
| sabotage | 4 | the mutant table | — (inside the tests piece's check) | "a seeded mutant must be caught" | N3, COO |
| review | 5 | the review result | code review | maker–checker, fresh blind session, a different kind | N4, Claude subagent |
| close | 6 | acceptance pack | — | three-part stop | N5, COO |

Each subagent hand-off earns its place: N1 and N2 are different kinds (blind test authoring), and N4 is a different
kind from both workers. The COO pieces are shell work with a script check, under her 8-call cap.

## Pieces, in the order they run

### N0 — Prep: pin, worktree, baseline, canaries

- **Steps:**
  1. Record the sha256 of the three spec files and `git status --short` in `state.md`.
  2. `git worktree add ../ancient-games-index-md -b build/index-md HEAD`.
  3. In the worktree, run the suite twice with `--junitxml`, then `feature_gate.py baseline --junit r1.xml --junit
     r2.xml --out runs/20261012-index-md-build/baseline.json`.
  4. Write `plan.json` with the gate's globs.
  5. Run one canary call each to `codex exec` and `opencode run`, and record the model each reports.
- **More than 3 steps because:** all five are shell commands with no hand-off between them, and the COO does them in one
  sitting under her 8-call cap.
- **Category:** step-level (file IO, shell). **Pattern:** step. **Builds:** no (it creates a branch; product files are
  untouched).
- **Check:** script. The hashes are written; `baseline.json` exists and lists the 529 tests; each canary writes a result
  file that names its model.
- **Contract — must not change:** the main tree. **Evidence — saved in:** `runs/20261012-index-md-build/nodes/n0-1.result.md`,
  `baseline.json`, `raw/`.
- **State — writes:** the hashes, the baseline line, the worktree path and the canary models.
- **Role and engine:** the COO herself (`claude-opus-5-5`).
- **Note:** `docs/index-md/` is untracked, so the worktree does not contain it. Every brief points at the main tree's
  absolute path, and the pinned hashes guard it.

### N1 — Acceptance tests, written blind

- **Steps:**
  1. Read the spec.
  2. Write one or more tests per in-scope **Fails if**. Each test's docstring cites its criterion id. Each test builds a
     temporary git repo, isolated with `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and author env vars, and
     runs the script as a subprocess.
  3. Run it: it must collect, and with no script every test fails.
- **Category:** test cases gen. **Pattern:** loop. **Builds:** yes (test surface, labelling rule 5).
- **Blueprint sections it depends on:** requirements and architecture (draft; held by Q1).
- **Acceptance criteria it covers:** all those listed above, as tests. C2.1 and C2.2 directly.
- **Check:** script, by the COO. `pytest --collect-only` succeeds. `runs/…/checks/trace_check.py` finds every in-scope id
  in a test docstring. `pytest tests/test_memory_index.py` in the worktree, with no script present, reports **0 passed**.
  *Who wrote the check:* the COO. *What it does not establish:* that the tests are right. N3's mutants test that.
- **Sabotage for the check:** drop one id from a copy of the test file; `trace_check.py` must fail.
- **Attempt limit:** 2. **Feedback on failure:** the check's real output (the missing ids, the passing test names).
- **Exit:** a fresh Codex `gpt-6-astra` node with a handoff note, limit 1, then EJ.
- **Needs the result of:** N0.
- **Contract:**
  - **Intent:** tests that come from the spec, not from the code.
  - **Stop:** the check passes.
  - **Returns:** the test file, and a result file with a table of criterion id → test names.
  - **May change:** `tests/test_memory_index.py` only.
  - **Must not change:** everything else. It does not create `tools/memory_index.py`, not even as a stub.
- **Evidence:** the collect output and the red run, in `nodes/n1-<attempt>.result.md`.
- **Context:**
  - **Given:** the brief, `REQUIREMENTS.md`, `DESIGN.md`, `VISION.md` (main-tree paths), `tests/test_skills_export.py`
    as the house style, and the test command.
  - **Withheld:** any code, this design file, `state.md` and the sabotage plan.
- **Role and engine:**
  - Role: test writer. Engine: Codex CLI `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high`, write mode,
    `-C <worktree>`.
  - One engine, no fallback. Wrapped in `runlog.py exec`.
  - Timers: no inner timer; outer `timeout 1200`.
- **Tools:** the brief at `briefs/n1.md`, invoked as "read <file> and do what it says".

### N2 — Script, hooks and unit tests (the build loop)

- **Steps:**
  1. Read the spec and the frozen acceptance tests.
  2. Write `tools/memory_index.py` (Python 3, standard library only, in the style of `tools/export_skills.py`), the two
     hooks, and the coder's own unit tests in `tests/test_memory_index_unit.py` (Q2).
  3. Run both test files until they are green.
- **Category:** code generation. **Pattern:** loop. **Builds:** yes.
- **Blueprint sections it depends on:** requirements and architecture (draft; held by Q1).
- **Acceptance criteria it covers:** all in scope. Its stop names them, plus "the baseline still passes" and its "must
  not change".
- **Check:** script, run by the COO, not the worker:
  `feature_gate.py check --plan plan.json --base-ref build/index-md@{N0} --baseline baseline.json --junit current.xml`.
  It covers new tests green, baseline green, scope, must-not, and **tamper**: `tests/test_memory_index.py` is protected.
- **Attempt limit:** 3 on the cheap tier.
- **Feedback on failure:** the gate's output and the failing tests' output, capped at 60 lines.
- **Contradiction path:** the worker may return `CONTRADICTS <test> <criterion id>` instead of code. The COO quotes both
  side by side. If the test is wrong, it goes back to N1 as a repair (this counts against N1's limit, not N2's).
  Otherwise she rejects the claim with the quote.
- **Exit:** a fresh Codex `gpt-6.1-sol` node, effort high, with a handoff note (the piece, the check, the last feedback),
  limit 2, then EJ.
- **Needs the result of:** N1 (its check passed).
- **Contract:**
  - **Intent:** the product.
  - **Stop:** the gate passes.
  - **Returns:** the code, and a result file listing each requirement id → file:line.
  - **May change:** `tools/memory_index.py`, `.githooks/pre-commit`, `.githooks/pre-merge-commit`,
    `tests/test_memory_index_unit.py`.
  - **Must not change:** the acceptance test file `tests/test_memory_index.py`, the spec, `CLAUDE.md`, `AGENTS.md`, `SOURCE_OF_TRUTH.md` and git config. It
    must not create `project-memory/` or commit anything.
- **Evidence:** the gate output, in `nodes/n2-<attempt>.result.md` and `gate-<attempt>.txt`.
- **State:**
  - **Reads:** N1's result path.
  - **Writes:** the attempt number, the gate verdict, the result path.
- **Context:**
  - **Given:** the brief, the spec (main-tree paths), the frozen test file, and `tools/export_skills.py` for style.
  - **Withheld:** N1's result notes, this design file, `state.md` and the sabotage plan.
- **Role and engine:**
  - Role: coder. Engine: opencode `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`, `--agent build`, write, run in the
    worktree.
  - Effort: *unknown*. I have not checked whether `opencode run` takes an effort flag for this model; N0's canary
    settles it, and the node names it before dispatch.
  - Wrapped in `runlog.py exec`. Timers: outer `timeout 1200` per attempt.

### N3 — Sabotage: the tests can fail

- **Steps:**
  1. Copy the worktree into a scratch directory.
  2. Apply each mutant to `tools/memory_index.py`, one at a time, and run the test file.
  3. Write a table: mutant id · the Fails-if it breaks · killed or survived.
- **Category:** inside the tests piece's check (TASK_TYPES: "a seeded mutant must be caught"). **Pattern:** step.
  **Builds:** no (scratch only).
- **The mutants:** one per in-scope **Fails if** line, written by the COO against N2's code. They are kept in the
  scratchpad until the verdict (memory: plants stay out of worker files). Here they are named only by the Fails-if they
  break.
- **Check:** script. Every mutant must be killed by the **acceptance** file (N1's), because that file is the
  independent one. The table also records whether the unit file kills each mutant, as information only. *Who wrote it:*
  the COO. *What it does not establish:* behaviour that no
  Fails if names.
- **On a survivor:** the criterion id goes to N1 as one repair round, with the requirement and not the mutant. N2's gate
  runs again, then N3 runs again. A second survivor goes to EJ.
- **Needs the result of:** N2 (the gate passed).
- **Must not change:** the worktree and the main tree. **Evidence:** `nodes/n3-1.result.md`, with the table; the mutants
  are copied in after the verdict.
- **Role and engine:** the COO herself, under the 8-call cap. A runner script does the loop, so the cap holds.

### N4 — Blind review

- **Steps:**
  1. Read the spec and the diff `HEAD..build/index-md`. In this copy the COO has planted **one** defect that the tests
     cannot catch. Its kind is kept in the scratchpad until the verdict.
  2. Judge the fixed checklist below.
  3. Write findings, each with file:line, split into *in criteria* and *outside criteria*.
- **Category:** code review. **Pattern:** step. **Builds:** no (read-only).
- **Checklist** (each item yes or no, with evidence):
  1. Every DESIGN step 1–12 is implemented as written: the `-z` listings, one `git cat-file --batch` call, code-point
     sort, CRLF→LF, the exact render bytes, atomic rename, no write in check mode, the size line printed on every run.
  2. Each of DESIGN's six **Must not** holds.
  3. Standard library only, and runs on a fresh clone.
  4. Errors read `<file>: <problem>`, and no input ends in a traceback.
  5. The hooks match G2.1, and `pre-merge-commit` is the one-line `exec`.
  6. The tests isolate git config and never touch the real repo except `--check HEAD`.
  7. Naming and style match `tools/export_skills.py`.
- **Check:** EJ's three-part stop judged as a checklist, plus the sabotage: **the plant must be found**. If it is
  missed, the review is void and runs again once, in a fresh session, with a different plant. A second miss goes to EJ.
- **Findings:**
  - A small finding inside the criteria: the COO fixes it (one sentence each for problem, fix and check, under 8 calls),
    then the N2 gate and N3 run again.
  - A big finding: back to N2, at most 2 rounds.
  - Outside the criteria: to the backlog (Q3).
- **Needs the result of:** N3 (all mutants killed).
- **Contract — returns:** `nodes/n4-1.result.md` (header from `result-file.md`, then the checklist table, then the
  findings).
- **Context:**
  - **Given:** the spec, the planted copy of the diff, and the gate output.
  - **Withheld:** the workers' result notes and reasoning, this design file, `state.md`, and the plant.
- **Role and engine:** reviewer. A Claude Code subagent (`general-purpose`), model Sonnet 5.5 (`claude-sonnet-5-5`),
  effort high, fresh session. It is a different kind from both opencode and Codex (EXECUTOR_KINDS rule 5). Read-only by
  brief, writing only its result file.

### N5 — Close: the "what is missing" pass

- **Steps:**
  1. Check the spec hashes against N0's. A mismatch is a stop: diff the file and plan the affected nodes again.
  2. Build `traceability.md`: criterion id → test(s) → mutant killed → review item. An empty cell is a failed stop.
  3. Run the full suite in the worktree. Check that the must-not-change list holds in the main tree:
     - `git diff --stat` on the protected paths is empty;
     - `git config --get core.hooksPath` is empty;
     - there is no `project-memory/`.

  Then run `harvest_run.py`, append the ledger row, and report to EJ.
- **Category:** the three-part stop. **Pattern:** step. **Builds:** no.
- **Check:** script, plus EJ. The matrix has no empty cell, the suite has 529 + N passed with 0 failed, and every
  must-not check comes back empty. EJ then accepts or not; the run's last judgment is his.
- **Returns:** `report.md`: a digest of about 15 lines, the matrix path, what was skipped and why, and the backlog
  entries.
- **Role and engine:** the COO herself.

## Joins

- **N1 → N2:** the frozen tests are N2's check. A `CONTRADICTS` claim is a join contradiction, and that is a stop: the
  COO picks one with quotes, and never averages.
- **N3 and N4 both judge N2's code.** If a mutant survives and the review says that behaviour is fine, it is a stop and
  goes to EJ with both quotes.

## Parallel candidates

None. N1 ∥ N2 fails condition 1, because N2's loop check is N1's output. N3 ∥ N4 fails condition 3, because a review
fix changes the code the mutants target. The whole run stays sequential.

## Predictability

- **Design source:** default, the "codegen → tests → review" pipeline with the build-a-feature roles: the dev writes
  unit tests, and the verifier writes acceptance cases blind. `workload.py`'s split stands (Q2), and opencode leads
  with 2 of the 3 build nodes. That share is *my arithmetic*; `workload.py` does not model a second test node. A ledger row in `docs/TASK_TYPES_LEDGER.md` is reconciled at N5.
- **Agents in total:** 3 worker calls (Codex, opencode, Claude subagent) plus 2 canaries; up to 9 worker calls if every
  repair and exit is used. **Bounds:** N1 2+1, N2 3+2, N4 1+1 attempts; at most 2 big review rounds; at most 1
  test-repair round from N3. Concurrency: 1 engine process alive at a time.
- **Cost estimate** (*not measured*; a range from this repo's earlier single-node runs, to be replaced by
  `harvest_run.py`):

  | Call | Tokens |
  |---|---|
  | N1, Codex | 100–250k |
  | N2, opencode, per attempt (cheap tier) | 80–200k |
  | N4, Sonnet | 60–120k |
  | COO | 15–25 turns |

  Wall time: about 1–2 hours.
- **Success criteria, written before the run:** the in-scope ids listed under Blueprint.

## Debuggability

- **Labels:** n0-prep, n1-tests, n2-code, n3-sabotage, n4-review, n5-close.
- **Every attempt's files:**
  - `briefs/<node>.md` (the input)
  - `nodes/<node>-<attempt>.result.md` (the output)
  - `raw/` (the engine output, gitignored)
  - `runlog` verdict lines
- **Resume point:** the last done row in `state.md`. The worktree branch holds the code at every accepted step: the COO
  commits on the **build branch** after each green gate, so a failed attempt is discarded by `git checkout .` in the
  worktree, never in the main tree.

## Quality control

- **Script checks:** N0, N1 (`trace_check.py` and the red run), N2 (`feature_gate.py`), N3 (mutants) and N5.
- **Judged:** N4's checklist. **EJ's:** Q1–Q3 and the final acceptance.
- **How each check is shown to fail:**
  - `trace_check.py`: a copy with an id removed.
  - `feature_gate.py`: its own `--self-test` and the tamper rule. N2 is told it cannot edit the test file, and the gate
    proves it.
  - The tests: N3's mutants.
  - The review: the plant.
- **What is missing pass:** N5, by the COO, against the three-part stop. Anything outside it goes to the backlog.

**The three qualities:**
- **Predictability:** the edges, limits and estimate above.
- **Debuggability:** one file per attempt, and a branch commit per green gate.
- **Quality control:** every check has a named sabotage. The reviewer is a third kind. The test writer never sees code
  before writing.
