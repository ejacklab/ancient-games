# Workflow design — 20261015-sot-leftovers

A design, not a run. Sequential. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Written 2026-10-15 by the COO
(`claude-opus-5-5`) at EJ's request: *"fix the item 10 leftovers with a proper designed workflows"*. State: `state.md`.

## Questions for EJ

| # | Question | Provisional assumption | Blueprint section |
|---|---|---|---|
| U1 | K4.3 lets an entry gain only four things after its first commit, so a stale `covers` path (a file renamed) can only be fixed by superseding the whole entry. May the header fields that are not the claim — `covers`, `source`, `depends_on` — be corrected after the first commit, each with a `changed:` line? The claim, `id` and `kind` still never change. | yes | the design (K4.3) |
| U2 | Rd3.1a: who decides which agents work on the project, and so the strictest `INDEX.md` limit? | the project owner | the design (Rd3.1a) |
| U3 | The tool hard-codes the limit (200 lines, 24,000 bytes), marked in its code as "the design's example, not a measurement". Leave it so, and say in Rd3.1a that the tool holds the example until the project owner records measured limits — or build the tool to read the limits from a file? | leave it; the build goes to the backlog | the design; `docs/index-md/` B4.1 |
| U5 | The design is for any project, but `basis` and two records point to `vision-statements/…` and `CACHES.md`, which exist only in this repo. Make the paths relative to the design's own folder and say so, keeping the files as siblings? | yes | the design (YAML header) |

U4 (measuring each engine's real start-file limit) is out of scope by default: it is research, and `CACHES.md` already
records a conflict on agy's limit (W-4). It goes to the TODO.

## Restatement (method 3.0)

**Objective.** The five leftovers of the 2026-10-15 review (state TODO item 10) are fixed in the design's three files,
or each is settled as a decision and recorded, with the YAML still passing its build checks and a blind review
finding no contradiction the fixes left behind.

**In scope:** `docs/memory-system/SOURCE_OF_TRUTH.md`, `SOURCE_OF_TRUTH_REQUIREMENTS.yaml` (through
`runs/20261014-sot-yaml-review/build_requirements.py`), `SOURCE_OF_TRUTH_RELEASE_NOTES.md`, and the state file.
**Out of scope:** `tools/memory_index.py` and `docs/index-md/` (unless EJ picks the build in U3, which becomes its own
run), measuring engine limits (U4), `CACHES.md`, the vision file, every other TODO item.

**Whys.** (1) Problem: the review found five places where the design is inconsistent or leaves a choice unowned.
(2) Now: the design was just finished and is about to be used. (3) Shape: small text edits plus three decisions.
(4) Failure: an agent supersedes a whole entry to fix a path, or follows a link that does not exist in its project;
low risk, nothing is live. (5) Stop: at the five. (6) Done: the build checks pass, the review finds no new
contradiction, EJ accepts.

**Provisional category** (*inferred*): documentation edit with decisions — `others` in `docs/TASK_TYPES.md`.

## Blueprint

- Kind of task: fix, to the design document (a product EJ owns). No code.
- Acceptance criteria: the five leftovers, each fixed or recorded as decided:
  L1 W6.3b's `check` agrees with K6.3b; L2 K4.3 per U1; L3 paths per U5; L4 the prose typo; L5 Rd3.1a per U2/U3.
- Baseline: `python3 runs/20261014-sot-yaml-review/build_requirements.py docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml`
  passes (loads, one shape, unique ids, all 46 covered, links resolve), and `env -u NO_COLOR python3 -m pytest -q`
  gives the same result as before (993 passed, 1 failing from another session's skill edits).

## The algorithm (method 3.2)

| # | Step | Check |
|---|---|---|
| 1 | Experts on the unclear spots; EJ answers U1, U2, U3, U5 | answers recorded in `state.md` |
| 2 | L1 and L4: W6.3b's check to `reviewer`; fix the typo | build script passes; diff shows only those lines |
| 3 | L3: paths relative to the design folder, said once in the YAML header | build script passes; every path named resolves from `docs/memory-system/` (a script) |
| 4 | L2: K4.3's text and `fails_if`, and the prose sentence that repeats it, per U1 | build script passes; the prose and K4.3 say the same (review) |
| 5 | L5: Rd3.1a's `who_decides` and text per U2/U3 | build script passes |
| 6 | Blind review of the diff against L1–L5, with one planted contradiction | the plant is found; findings carry file:line |
| 7 | Close: release note, state and TODO, commit on EJ's word | baseline unchanged |

## Pieces, in the order they run

### P1 — Decisions (EJ)
- **Steps:** experts on the unclear spots (`four-experts --only linus,sun-tzu,lao-tzu,dave`, unclear-spots question);
  EJ answers U1, U2, U3, U5 in one batch.
- **Check:** EJ. **Builds:** no. **Role:** EJ decides; the COO records the full rule in `state.md`.

### P2 — Edits (COO)
- **Steps:** 1. L1, L4, L3 (no decision for L1/L4; L3 per U5). 2. L2 per U1. 3. L5 per U2/U3.
- **Pattern:** step; one attempt, repaired only on a failed check.
- **Check:** script — the build script after each step; a path check (every repo path the YAML names resolves from
  `docs/memory-system/`). *Who wrote it:* the COO. *Does not establish:* that the text is right; P3 judges that.
- **Contract — may change:** the three design files, `build_requirements.py`. **Must not change:** `tools/`,
  `docs/index-md/`, `CACHES.md`, the vision file, any other doc.
- **Evidence:** the build script's output and `git diff --stat`, in `nodes/p2.result.md`.
- **Role and engine:** the COO (`claude-opus-5-5`), in the main tree. Text edits to one document set, under the cap.

### P3 — Blind review (Claude subagent)
- **Steps:** read L1–L5 as written here, the diff, and both files; judge each leftover fixed or not, and look for any
  contradiction between the prose, the YAML and the release note.
- **Check:** one planted contradiction (chosen by the COO after P2, kept outside the repo until the verdict) must be
  found; a miss voids the review, which runs once more with a different plant, then EJ.
- **Context — withheld:** the COO's reasoning, this design's questions table, the plant.
- **Role and engine:** reviewer, Claude Code subagent `claude-sonnet-5-5`, effort high, read-only by brief.
- **Evidence:** `nodes/p3-1.result.md`.

### P4 — Close (COO)
- **Steps:** fix in-scope findings (then the build script again); release-note entry; state Log and TODO (item 10
  closed, U4 and any U3 build added); commit and push on EJ's word.
- **Check:** baseline unchanged; EJ accepts.

## Joins

P3 judges P2's text against P1's decisions; a finding that a decision was applied wrongly goes back to P2 once, then
EJ.

## Parallel candidates

None: every piece needs the one before it.

## Predictability

- Agents: the four experts and Dave at P1 (5 engine calls), one reviewer at P3 (at most 2 with the rerun). The COO
  does P2 and P4.
- Cost (*not measured*): experts about the last two rounds (5 calls, about 10–15 minutes); reviewer 40–80k tokens;
  COO 10–15 turns. Wall time about 30–45 minutes after EJ answers.
- Success criteria, written before the run: L1–L5 fixed or recorded as decided; the baseline unchanged; the plant
  found.

## Debuggability

Labels p1-decisions, p2-edits, p3-review, p4-close. Files: `experts/`, `nodes/`, `state.md`. Resume point: the last
done row in `state.md`. The edits are in git, one commit at the end; any step is undone with `git diff`.

## Quality control

- Script: the build script (already shown able to fail: it asserts on a missing id, a dangling link, a second shape);
  the path check (shown able to fail on a path made wrong on purpose before P2 starts).
- Judged: P3, tested by its plant. EJ's: P1 and the final acceptance.
- **The three qualities:** predictability — the edges and bounds above; debuggability — one file per step and git;
  quality control — every check has a named way to fail.
