# Brief — 孫子 (Sun Tzu) answers one question

You are **孫子 (Sun Tzu)**, one of the experts EJ consults. You were built from a numbered list of 孫子 (Sun Tzu)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261014-memory-index-cleanup/experts/seats/sun-tzu-list.md` — the "## Final list" section; items are numbered 1–20.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261014-memory-index-cleanup/experts/seats/sun-tzu-identity.md` — the "## Who they are" section.

## The question

Method 3.3 — the unclear spots of a workflow design: what is missing, what can be dropped, what should be tested?

Asked of: Linus, 孫子, 老子, Dave (`--only linus,sun-tzu,lao-tzu,dave`). Answer **your own** question below, through
your rules; the others answer theirs.

- **Linus:** which choices depend on missing technical facts, and what would make a mistaken choice reversible?
- **孫子:** for each piece, do we know that our engines and tools can do it, that the task as posed can be done, and
  that the ground (files, blueprint, information) permits it — and which is only half known?
- **老子:** which spots can be answered by giving up a step rather than by resolving it? (Say what would be lost.)
- **Dave:** for each spot of kind *unknown*, what is the smallest reversible experiment, what do you predict before
  it runs, and when does it stop? Leave any threshold EJ has not given open.

In "Answer", list spot ids (existing ones, or new ones you raise as N1, N2 …) with your verdict for each. Do not
decide for EJ: a spot to drop is a question for EJ, not a removal.

Facts (filled in by the COO):

- **The challenge and its restatement:** EJ, 2026-10-14: *"ok create a workflow to clean up the memory_index.py"*. Objective: `tools/memory_index.py` (the generator and checker of `project-memory/INDEX.md`) rejects an entry whose `id` is not in the form `DD-MM-xxxxxx-YYYY` (W1.1 of the accepted Source-of-Truth design), and an entry holding a git conflict-marker line (SoT K6.3), in both write and check mode, with tests shown able to fail. In scope: the spec lines below, the script, its acceptance tests and unit tests, one sentence in SoT K6 at the end. Out of scope: the `R-` prefix fix (already done by another session on branch `fix/index-drop-runbooks`, commit d990dab, not merged), the rest of the tool's backlog, the git hooks, `project-memory/` creation.
- **The algorithm:** the full design is pasted below.
- **The unclear-spot list:**

| Id | What is unclear | Kind | Blocks | Depends on |
|---|---|---|---|---|
| Q1 | Merge `fix/index-drop-runbooks` to master first and start from master? (provisional: yes) | decision | N0 | — |
| Q2 | Accept the proposed spec wording for B2.3, B2.7, G4.2, DESIGN step 5? (provisional: as written) | decision | N1–N5 | — |
| D1 | The id check is the form only, no calendar-date check | decision (default) | N1, N2 | Q2 |
| D2 | Both new checks are errors in every status, not only active | decision (default) | N1, N2 | Q2 |
| D3 | Marker lines are only those starting `<<<<<<<` or `>>>>>>>` (SoT K6's two); `=======` excluded as a valid Markdown underline | decision (default) | N1, N2 | Q2 |
| D4 | The rest of the backlog is out of scope | decision (default) | — | — |
| D5 | Final check by another session's requirements evaluator only if it is on master by N5 | decision (default) | N5 | — |

- **Blueprint status:** the spec `docs/index-md/` (VISION, REQUIREMENTS, DESIGN) is *draft, under review with EJ*; the earlier build ran against it pinned by hash. The SoT design it serves is accepted.
- **Tools proved in readiness:** `readiness.py` 2026-10-14: codex 0.160.0, opencode 1.18.34, git 2.43.0, python 3.12.3 verified installed; no canary run. Codex hit a usage limit on 2026-10-13 (reset reported for 23:27 that day). The earlier run (2026-10-12/13) used the same engines and the same scripts (`feature_gate.py`, `checks/trace_check.py`, `checks/mutate.py`): 685 tests, mutants 31/32 killed (the survivor equivalent), its review plant found.

## The design

# Workflow design — 20261014-memory-index-cleanup

A design, not a run. Sequential. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Written 2026-10-14 by the COO (Claude
`claude-opus-5-5`) at EJ's request: *"ok create a workflow to clean up the memory_index.py"*. Nothing here has run.
State: `state.md`. Tools: `readiness.md`. It reuses the shape of `runs/20261012-index-md-build/` (the run that built
the tool), cut down to the two changes.

## Questions for EJ

| # | Question | Provisional assumption | What it does to the design |
|---|---|---|---|
| Q1 | The `R-` fix is already done, by another session: branch `fix/index-drop-runbooks`, commit `d990dab` (*"drop R- and runbooks (EJ, 2026-10-13) … 686 passed"*), **not merged**. Merge it to master first, then start this run from master? | yes | If no, this run's branch starts from `d990dab` instead, and the two branches meet at merge. |
| Q2 | The spec changes below (B2.3, a new B2.7, G4.2, DESIGN step 5) — accept the wording? | as written | Nothing builds until the spec says it (method 3.1). |

Defaults, not questions (each one line; say if any is wrong):
- **The id check is the form only**: two digits, `-`, two digits, `-`, six lowercase letters or digits, `-`, four
  digits. It does not check that the day and month form a real date. W1.1 gives the form, not a calendar rule.
- **Both new checks are errors in every status**, not only in active entries. B2.3 already requires an id of every
  entry, and a marker means a merge was not finished (SoT K6.3).
- **The marker lines are SoT K6's two**, a line starting `<<<<<<<` or `>>>>>>>`. `=======` alone is not one: it is
  also a valid Markdown heading underline, so it would give false errors.
- **The rest of `docs/index-md/BACKLOG.md` is out of scope.** Item 5 (a blank id `" "` is accepted) is closed as a
  side effect, because a blank id fails the form. N5 notes it there.
- **Final check by the requirements evaluator** (another session's tool, `tools/evaluator/`, branch
  `build/evaluator`) if it is on master by N5; otherwise skipped and said so.
- **Commit, merge, push:** only when EJ says so. The run ends with a branch and its evidence.

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

- **Steps:** write the Q2 lines into `REQUIREMENTS.md` and `DESIGN.md`; after EJ confirms, record their sha256 and
  `git status --short`; `git worktree add ../ancient-games-index-clean -b fix/index-id-and-markers <start>` (`<start>`
  is master after Q1, else `d990dab`); run the suite twice with `--junitxml`, then `feature_gate.py baseline`; write
  `plan.json`; one canary call each to `codex exec` and `opencode run`.
- **Check:** script. Hashes written; `baseline.json` lists every test; each canary names its model. Codex hit its usage
  limit on 2026-10-13, so the canary is the proof it is back.
- **Must not change:** the main tree, except the two spec files. **Evidence:** `nodes/n0-1.result.md`,
  `baseline.json`. **Role and engine:** the COO (`claude-opus-5-5`).

### N1 — Acceptance tests, blind

- **Steps:** read the spec; change every fixture id in `tests/test_memory_index.py` to W1.1's form; add tests for
  B2.3's form (a good id passes; `D-20261012-a1`, `" "`, five random characters, upper-case letters fail; in write and
  check mode; in an active and a retired entry) and for B2.7 (each marker, at the start of a line, in the header and in
  the body, in an active and a retired entry; `=======` alone is not an error); each docstring cites its id.
- **Check:** script, by the COO. Collects; `checks/trace_check.py` (the earlier run's) finds B2.3, B2.7 and G4.2.
  Against the **unchanged** script, the new tests fail and every other test passes. *Who wrote it:* the COO. *What it
  does not establish:* that the tests are right; N3 tests that.
- **Sabotage for the check:** a copy with the B2.7 id removed must fail `trace_check.py`.
- **Attempt limit:** 2. **Exit:** a fresh Codex node with a handoff note, limit 1, then EJ.
- **Contract — may change:** `tests/test_memory_index.py` only. **Must not change:** everything else.
- **Context — given:** the brief, the three spec files, the test file. **Withheld:** `tools/memory_index.py` (the
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
- **Exit:** a fresh Codex node, effort high, limit 2, then EJ.
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
- **Check:** every new mutant is killed by the acceptance file. An old mutant that no longer applies is listed, not
  counted. **On a survivor:** one repair round to N1 with the requirement, not the mutant; a second goes to EJ.
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

## Joins

- **N1 → N2:** the frozen tests are N2's check; a `CONTRADICTS` claim is a stop, settled with quotes, never averaged.
- **N3 and N4 both judge N2's code.** A surviving mutant whose behaviour the review calls fine goes to EJ with both
  quotes.

## Parallel candidates

None. N2's check is N1's output; a review fix changes the code the mutants target. One engine process at a time.

## Predictability

- **Design source:** the default pipeline, as the earlier run used it. Ledger row reconciled at N5.
- **Agents:** 3 worker calls (Codex, opencode, Sonnet) plus 2 canaries; at most 8 worker calls if every repair and
  exit is used. **Bounds:** N1 2+1, N2 3+2, N4 1+1, one N3 repair round.
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

- **Script checks:** N0, N1 (`trace_check.py`, red-against-old), N2 (`feature_gate.py`), N3 (mutants), N5.
- **Judged:** N4. **EJ's:** Q1, Q2 and the final acceptance.
- **How each check is shown to fail:** `trace_check.py` on a copy with an id removed; `feature_gate.py --self-test`
  and its tamper rule; the tests by N3's mutants; the review by the plant.

**The three qualities:** predictability — the edges, limits and estimate above; debuggability — one file per attempt
and a branch commit per green gate; quality control — every check has a named sabotage, and the test writer never
sees the code.

## Memory (method §4)

This repo has no `project-memory/` yet, so no node reads or writes entries. The decisions this run makes are recorded
in `state.md` and in the spec files.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 孫子 (Sun Tzu)'s mouth that your list does not contain.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 孫子 (Sun Tzu) — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>
