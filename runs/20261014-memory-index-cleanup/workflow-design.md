# Workflow design — 20261014-memory-index-cleanup

A design, not a run. Sequential. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Written 2026-10-14 by the COO (Claude
`claude-opus-5-5`) at EJ's request: *"ok create a workflow to clean up the memory_index.py"*. Nothing here has run.
State: `state.md`. Tools: `readiness.md`. It reuses the shape of `runs/20261012-index-md-build/` (the run that built
the tool), cut down to the two changes.

## Questions for EJ

| # | Question | Provisional assumption | What it does to the design |
|---|---|---|---|
| Q1 | The `R-` fix is already done, by another session: branch `fix/index-drop-runbooks`, commit `d990dab` (*"drop R- and runbooks (EJ, 2026-10-13) … 686 passed"*), **not merged**. Merge it to master first, then start this run from master? | yes | If no, this run's branch starts from `d990dab` instead, and the two branches meet at merge. |
| Q2 | The spec changes below (B2.3, a new B2.7, G4.2, DESIGN step 5) — accept the wording? | as written | Nothing builds until the spec says it (method 3.1). N0's worktree, baseline and canaries may run while Q2 is open; N1 does not start until it is answered (老子). |

On Q1, 老子's alternative: branch from `d990dab` without merging, and the question goes away; the price is a review diff
taken against `d990dab`. *Ran* (Dave, 2026-10-14): `git merge-tree --write-tree master d990dab` is clean. That shows no
text conflict, not that the merged tree passes; N0 runs the suite on whichever start is chosen.

Defaults, not questions (each one line; say if any is wrong):
- **The id check is the form only**: two digits, `-`, two digits, `-`, six lowercase letters or digits, `-`, four
  digits. It does not check that the day and month form a real date. W1.1 gives the form, not a calendar rule; a test
  shows `31-02-a1b2c3-2026` is accepted, so the choice is visible (Linus).
- **The form is matched against the whole parsed value** (after B2.1 strips spaces and quotes), with ASCII digits and
  letters only: Python's `\d` also matches non-ASCII digits, and the id is part of a file name. Raised by Dave and
  Linus; say if Unicode digits should pass.
- **Both new checks are errors in every status**, not only in active entries. B2.3 already requires an id of every
  entry, and a marker means a merge was not finished (SoT K6.3).
- **The marker lines are SoT K6's two**, a line starting `<<<<<<<` or `>>>>>>>`. `=======` alone is not one: it is
  also a valid Markdown heading underline, so it would give false errors.
- **The rest of `docs/index-md/BACKLOG.md` is out of scope.** Item 5 (a blank id `" "` is accepted) is closed as a
  side effect, because a blank id fails the form. N5 notes it there.
- **Final check by the requirements evaluator** (another session's tool, `tools/evaluator/` on branch
  `build/evaluator`) if it is on master by N5; otherwise skipped and said so. It is not on master today (Dave, 孫子).
  If it runs, N5 first says which spec it read (Linus). 老子 would drop it: `traceability.md` already shows the
  coverage; what it adds is an independent machine reading.
- **Commits:** on the build branch only, as the earlier run did: the spec commit (N0), N1's frozen tests, and one
  per green gate, so any step can be undone in the worktree. **Merge to master and push:** only when EJ says so. The
  main tree is never edited by a worker (Linus asked who may commit; this is the answer).
- **No engine switch inside a node** (method 3.8 item 5). If a canary fails, its node waits and EJ is told; Codex is
  not replaced by another engine for N1 (Dave).

## Restatement (method 3.0)

**Objective.** `tools/memory_index.py` rejects an entry whose id is not in W1.1's form `DD-MM-xxxxxx-YYYY`, and an entry
holding a git conflict-marker line, in both write and check mode. Each new **Fails if** has a test that is shown to
fail on a broken script, and the suite still passes.
**In scope:** the spec lines in Q2, `tools/memory_index.py`, `tests/test_memory_index.py`,
`tests/test_memory_index_unit.py`, and, at the end, the one sentence in SoT K6 that says the tool does not check for
markers. **Out of scope:** the `R-` fix (Q1, done), the rest of the backlog, the hooks, `CLAUDE.md`, `AGENTS.md`,
`git config core.hooksPath`, creating `project-memory/`.

**Whys.**
1. Problem: the tool passes two things the accepted design says are wrong. SoT W1's Fails if names "an id not in the
   W1.1 form", and SoT K6's names a conflict-marker line, *"judged, because the tool does not check for markers"*.
2. Now: W1.1's id form was settled on 2026-10-13, after the tool was built (2026-10-12).
3. Shape: two small checks in a tool with a full acceptance suite. This is build plus test, not research.
4. Failure: a bad id or a half-merged entry is indexed silently. Nothing is live (`project-memory/` exists in no
   product, the hook is off), so the risk is **low to medium**. The cost of a defect is late discovery.
5. Stop: at the two checks. The rest of the backlog is EJ's to pick.
6. Done: the three-part stop. Each new criterion's test passes and is shown able to fail, the baseline passes, and
   "must not change" holds.

**Provisional category** (*inferred*): code generation + test cases gen + code review, the "codegen → tests → review"
pipeline, **case C** (an existing tool gets a feature).

## Blueprint

- Kind of task: feature. The spec is `docs/index-md/` (draft, under review with EJ). The changes in Q2 are written by
  N0 and confirmed by EJ before N1.
- Acceptance criteria in scope: **B2.3** (as changed), **B2.7** (new), **G4.2** (as changed). The rest of B, C and G
  is the baseline: their tests must still pass.
- Baseline: `env -u NO_COLOR python3 -m pytest -q` on the start branch. On master today: 685 passed (*ran*,
  2026-10-14). `d990dab` says 686 (*reported*, its commit message). N0 records it again in the worktree.

### The spec changes (Q2), proposed

`docs/index-md/REQUIREMENTS.md`:
- **B2.3** becomes: *"Every entry must have a readable header with an `id` in W1.1's form, `DD-MM-xxxxxx-YYYY` (two
  digits, two digits, six lowercase letters or digits, four digits), and a `status` of `active`, `superseded` or
  `retired`. No two entries share an `id`."*
- **B2.7** (new): *"No entry holds a line that starts with `<<<<<<<` or `>>>>>>>`, a git conflict marker (SoT K6.3).
  It is an error in every status."*
- **B2 Fails if** gains: *"an id not in W1.1's form passes, or an entry with a conflict-marker line passes."*
- **G4.2** becomes: *"The script rejects a duplicate id and an id not in W1.1's form (B2.3); it does not choose an
  id."*

`docs/index-md/DESIGN.md` step 5, "Errors, for every entry": add *"an `id` not in W1.1's form; a line starting
`<<<<<<<` or `>>>>>>>`"*.

Requirement check (the skill, on each line above): source — W1.1 and K6.3, both accepted, plus EJ's "clean up";
one thing — yes, one check each; unit — the form is a pattern, no number to choose; can it fail — `id: D-20261012-a1`,
`id: " "` and a `<<<<<<< HEAD` line each fail; weak words — none; level — this spec has no levels yet (the
MUST/SHOULD pass on SoT is running separately); basis — quoted from SoT; links — B2.7 cites K6.3, quoted.

## The algorithm (method 3.2)

| # | Step | Check |
|---|---|---|
| 1 | Write the spec changes; pin the spec; open a worktree; record the per-test baseline; run the engine canaries | EJ confirms Q2; hashes; two JUnit runs; canary result files |
| 2 | Update the acceptance tests from the spec alone: every fixture id into W1.1's form, and tests for B2.3's form and B2.7 | collects; the ids are cited; against the **unchanged** script exactly the new tests fail and every other passes |
| 3 | Change the script and its unit tests against the frozen tests | `feature_gate.py check`: new tests green, baseline green, scope, must-not, tamper |
| 4 | Prove the new tests can fail: one hidden mutant per new Fails-if clause, and rerun the earlier run's mutants | each mutant turns at least one acceptance test red |
| 5 | Blind review of the diff, with one planted defect | the plant is found; findings carry file:line |
| 6 | Close: SoT K6 sentence, traceability, evaluator, backlog note, ledger, report | no empty cell; full suite green |

| Piece | Steps | Deliverable | Category | Node |
|---|---|---|---|---|
| prep | 1 | spec lines, worktree, baseline, canaries | step-level | N0, COO |
| tests | 2 | `tests/test_memory_index.py` | test cases gen | N1, Codex |
| code | 3 | the script and its unit tests | code generation | N2, opencode (loop) |
| sabotage | 4 | the mutant table | inside the tests' check | N3, COO |
| review | 5 | the review result | code review | N4, Claude subagent |
| close | 6 | acceptance pack | three-part stop | N5, COO |

Each hand-off earns its place as in the earlier run: N1 is blind to the code, N2 is a different engine from N1, and
N4 is a third kind. The diff is small, so N4 could be the COO's own reading; it stays a node because the plant is the
only check on the review, and a reviewer who wrote the plant cannot be tested by it.

## Pieces, in the order they run

### N0 — Prep

- **Steps:**
  1. `git worktree add ../ancient-games-index-clean -b fix/index-id-and-markers <start>` (`<start>` is master after
     Q1, else `d990dab`). If the path outside the repo is refused, use one inside it (孫子).
  2. After EJ confirms Q2, write the Q2 lines into the worktree's `docs/index-md/REQUIREMENTS.md` and `DESIGN.md` and
     commit them on the build branch, so every worker reads the new spec where it works. Record their sha256. (孫子:
     edits left in the main tree never reach the worktree.)
  3. Copy `runs/20261012-index-md-build/checks/trace_check.py` into this run's `checks/` and add B2.7 to its id list;
     its own sabotage then can fire (孫子: the old copy hard-codes its ids and has no B2.7).
  4. Write `checks/fixture_ids.py`: every literal id value in the acceptance file is in W1.1's form, except in tests
     whose docstring cites B2.3 or G4.2. Its sabotage: the current test file must fail it (Dave).
  5. Run the suite twice with `--junitxml`, then
     `.claude/skills/workflow-design/scripts/feature_gate.py baseline --junit r1.xml --junit r2.xml --out baseline.json`;
     write `plan.json`.
  6. **Mutant control (Dave):** run the earlier run's 32 mutants with `checks/mutate.py` against the start tree's script
     and tests; save the per-mutant kill list. Dave counted 30 that apply on master and 29 on `d990dab`.
  7. One canary each: `codex exec`, `opencode run --variant high`, and a read-only Claude Sonnet 5.5 subagent, each
     naming its model.
- **Check:** script. Hashes written; `baseline.json` lists every test; `fixture_ids.py` fails on the current file;
  `trace_check.py` fails on a copy with B2.7 removed; the control kill list is saved; each canary names its model.
  Codex hit its usage limit on 2026-10-13, so its canary is the proof it is back.
- **Must not change:** the main tree, except the two spec files. **Evidence:** `nodes/n0-1.result.md`,
  `baseline.json`. **Role and engine:** the COO (`claude-opus-5-5`).

### N1 — Acceptance tests, blind

- **Steps:**
  1. Read the spec.
  2. Change every fixture id in `tests/test_memory_index.py` to W1.1's form, so that each existing test fails for its
     own reason and not for its id. The brief names the places Dave found: `write_entry`'s default `D-20261012-a1`,
     the `INVALID_ENTRIES` cases (12 of 13 use `id: bad`, `id: ''` or `id: nested-only`; their test asserts only the
     exit code and the file name, so after the change they would pass on the id alone), and the `id: bad` / `id: old`
     fixtures. An id that a test means to be bad stays only in a test that cites B2.3.
  3. Add tests for B2.3's form: a good id passes; `D-20261012-a1`, `" "`, five characters, upper case, trailing junk
     (`14-10-a1b2c3-2026x`) and a non-ASCII digit fail; `31-02-a1b2c3-2026` passes; in write and check mode; in an
     active, a superseded and a retired entry.
  4. Add tests for B2.7: each marker at the start of a line, in the header and in the body, in all three statuses;
     `=======` alone is not an error (老子: the one fixture that must not be given up).
  5. Each docstring cites its id.
- **Check:** script, by the COO. Collects; this run's `checks/trace_check.py` finds B2.3, B2.7 and G4.2;
  `checks/fixture_ids.py` passes. Against the **unchanged** script (restored beside the frozen tests in a scratch
  copy), the new tests fail and every other test passes. *Who wrote it:* the COO. *What it
  does not establish:* that the tests are right; N3 tests that.
- **Sabotage for the check:** a copy with the B2.7 id removed must fail `trace_check.py`.
- **Attempt limit:** 2. **Exit:** a fresh Codex node with a handoff note, limit 1, then EJ.
- **Contract — may change:** `tests/test_memory_index.py` only. **Must not change:** everything else.
- **Context — given:** the brief, the three spec files (committed on the branch in N0), the test file. **Withheld:** `tools/memory_index.py` (the
  worktree it works in has the script removed, as in the earlier run's repair round), this design, `state.md`, the
  sabotage plan.
- **Role and engine:** test writer. Codex CLI `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high`, write mode,
  `-C <code-free worktree>`, stdin `</dev/null`, outer `timeout 1200`. Brief in `briefs/n1.md`.

### N2 — Script and unit tests (the loop)

- **Steps:** read the spec and the frozen tests; change `tools/memory_index.py` and `tests/test_memory_index_unit.py`;
  run both test files until green.
- **Check:** `feature_gate.py check --plan plan.json --base-ref <N1's frozen commit> --baseline baseline.json --junit
  current.xml`, run by the COO: new tests green, baseline green, scope, must-not, tamper (the acceptance file is
  protected).
- **Attempt limit:** 3. **Feedback:** the gate's output and the failing tests, capped at 60 lines.
  **Contradiction path:** `CONTRADICTS <test> <id>` goes back to N1 as a repair, quoted side by side.
- **Exit:** a fresh Claude subagent (`claude-opus-5-5`, effort high) with a handoff note, limit 2, then EJ. Not Codex:
  Codex wrote the tests, and the coder must not be the test writer's engine (老子, Dave).
- **Contract — may change:** `tools/memory_index.py`, `tests/test_memory_index_unit.py`. **Must not change:** the
  acceptance file, the spec, the hooks, `CLAUDE.md`, `AGENTS.md`, SoT, git config; it creates no `project-memory/` and
  commits nothing.
- **Context — given:** the brief, the spec, the frozen tests. **Withheld:** N1's notes, this design, `state.md`, the
  sabotage plan.
- **Role and engine:** coder. opencode `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`, `--agent build`,
  `--variant high` (accepted by the earlier run's canary), in the worktree, stdin `</dev/null`, outer `timeout 1200`.

### N3 — Sabotage

- **Steps:** with `checks/mutate.py` (the earlier run's), apply each new mutant to the script in a scratch copy and run
  the acceptance file; then rerun the earlier run's 32 mutants (`runs/20261012-index-md-build/sabotage/mutants.json`)
  where their `old` text still occurs once.
- **The new mutants:** one per new Fails-if clause, written by the COO against N2's code and kept in the scratchpad
  until the verdict.
- **The new mutants include** a start-only match (trailing junk passes) and a check on the raw value before quotes are
  stripped (Dave), and one that applies a check to active entries only (老子's D2 risk).
- **Check:** every new mutant is killed by the acceptance file, and the old mutants' kill list matches N0's control
  **mutant by mutant**: one killed before and surviving now means a test lost power, which a total would hide (Dave).
  For one old status or kind mutant, the failing test's output names the status or kind, not the id. An old mutant
  that no longer applies is listed, not counted. (老子 would run only the old mutants inside N2's diff; they all run,
  because the run is a script and the control is what catches masking.) **On a survivor:** one repair round to N1 with the requirement, not the mutant; a second goes to EJ.
- **Role and engine:** the COO. **Evidence:** `nodes/n3-1.result.md`; mutants copied in after the verdict.

### N4 — Blind review

- **Steps:** read the spec and the diff (with one planted defect the tests cannot catch, kept in the scratchpad until
  the verdict); judge: both checks in both modes, errors read `<file>: <problem>`, no traceback on any input, standard
  library only, the earlier run's naming and style; findings with file:line, in or outside the criteria.
- **Check:** the plant must be found; a miss voids the review, which runs once more with a different plant, then EJ.
  Small in-criteria findings: the COO fixes them, then the gate and N3 run again. Outside the criteria:
  `docs/index-md/BACKLOG.md`.
- **Context — withheld:** the workers' notes and reasoning, this design, `state.md`, the plant.
- **Role and engine:** reviewer. Claude Code subagent, `claude-sonnet-5-5`, effort high, fresh session, read-only by
  brief.

### N5 — Close

- **Steps:** spec hashes against N0's; `traceability.md` (id → tests → mutant → review item); full suite in the
  worktree; must-not checks (protected paths unchanged, `core.hooksPath` empty, no `project-memory/`); the requirements
  evaluator on the branch if it is on master (default above); SoT K6's Fails if changed from *"that part is judged,
  because the tool does not check for markers"* to *"in an entry, the tool's check catches it (`docs/index-md/`
  B2.7); in `INDEX.md`, the comparison in K6.2 does"* (*proposed*; EJ approves it with the merge); BACKLOG item 5 noted
  as closed by B2.3; ledger row; `report.md`.
- **Check:** no empty cell; suite green; must-not empty; then EJ accepts or not.
- **Role and engine:** the COO.

## Expert review of the unclear spots (method 3.3)

`experts/` — Linus, 孫子, 老子 and Dave (`--only linus,sun-tzu,lao-tzu,dave`), 2026-10-14; comparison in
`experts/compare.md`. Every finding is folded in above and marked with who raised it. One claim was wrong:
孫子 said `tools/evaluator/` does not exist; it does, on branch `build/evaluator` (`git ls-tree`, *ran*), and not on
master. Spots that stay with EJ: Q1, Q2, and whether Unicode digits should pass the id check.

## Joins

- **N1 → N2:** the frozen tests are N2's check; a `CONTRADICTS` claim is a stop, settled with quotes, never averaged.
- **N3 and N4 both judge N2's code.** A surviving mutant whose behaviour the review calls fine goes to EJ with both
  quotes.

## Parallel candidates

None. N2's check is N1's output; a review fix changes the code the mutants target. One engine process at a time.

## Predictability

- **Design source:** the default pipeline, as the earlier run used it. Ledger row reconciled at N5.
- **Agents:** 3 worker calls (Codex, opencode, Sonnet) plus 3 canaries. **Bounds:** N1 2 attempts + 1 exit, N2 3 + 2
  exit, N4 1 + 1, plus one N3 repair round, which is an N1 call: at most **11 worker calls** if every repair and exit is
  used. A `CONTRADICTS` return sent back to N1 counts against N1's limit. (Linus: the earlier "8" was wrong.)
- **Cost** (*not measured*; ranges from the earlier run, which built the whole tool):

  | Call | Tokens |
  |---|---|
  | N1, Codex | 60–150k |
  | N2, opencode, per attempt | 50–150k |
  | N4, Sonnet | 40–80k |
  | COO | 12–20 turns |

  Wall time: about 45–90 minutes.
- **Success criteria, written before the run:** B2.3 (form), B2.7, G4.2, and the baseline.

## Debuggability

Labels n0-prep … n5-close; per attempt `briefs/<node>.md`, `nodes/<node>-<attempt>.result.md`, `raw/` (gitignored),
the gate files. Resume point: the last done row in `state.md`. The COO commits on the build branch after each green
gate; a failed attempt is discarded in the worktree only.

## Quality control

- **Script checks:** N0, N1 (`trace_check.py`, `fixture_ids.py`, red-against-old), N2 (`feature_gate.py`), N3
  (mutants against N0's control), N5.
- **Judged:** N4. **EJ's:** Q1, Q2 and the final acceptance.
- **How each check is shown to fail:** `trace_check.py` on a copy with an id removed; `fixture_ids.py` on the current
  test file; `feature_gate.py --self-test`
  and its tamper rule; the tests by N3's mutants; the review by the plant.

**The three qualities:** predictability — the edges, limits and estimate above; debuggability — one file per attempt
and a branch commit per green gate; quality control — every check has a named sabotage, and the test writer never
sees the code.

## Memory (method §4)

This repo has no `project-memory/` yet, so no node reads or writes entries. The decisions this run makes are recorded
in `state.md` and in the spec files.
