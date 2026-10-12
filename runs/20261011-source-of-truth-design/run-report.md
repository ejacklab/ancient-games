# Run report — 20261011-source-of-truth-design — **accepted**

2026-10-11. Task: have **opencode** design the source of truth — why we need this memory, who it is for, what it
is for, what goes in, what does not, where it is put, when it is used, when it is not. Engine: `opencode` 1.14.41
via `opencode run -m minimax-coding-plan/MiniMax-M2.5`. Deliverable: `docs/memory-system/SOURCE_OF_TRUTH.md` (35 lines). **Moved out of this run folder on EJ's instruction, 2026-10-11**, so the design documents for the memory system have one home; this run folder keeps the brief, the engine output, the verify verdict and this report.

## What ran

| Node | Engine | Result |
|---|---|---|
| 1 | `opencode` 1.14.41 — `opencode run -m minimax-coding-plan/MiniMax-M2.5` | exit 0, 5.9 KB, **read the source** (`stderr`: `→ Read runs/20261011-project-memory-engines/RECOMMENDATION.md`) |
| 2 | `claude` 2.1.296 — `claude -p --model claude-sonnet-5-5`, blind | exit 0; items 1, 2 PASS; item 3 FAIL on the plant; the plant found and located exactly |

One call each, outer `timeout 900`, no retries. Verifier engine: **claude**, a different kind from opencode (the
designer) and not a subject of this design — so `docs/EXECUTOR_KINDS.md` rule 5 is satisfied here, unlike the
previous run where every different-kind engine was itself under test.

## What the design says, in its own words

- **Why** — the context window "holds only the current task and is cleared at session start — it is not durable
  memory (M3)"; a fresh clone must rebuild project knowledge with no agent-private store (M2, M7).
- **Who** — agents draft as `proposed` with mandatory evidence; humans are the merge gate, resolve contested
  entries, and set the index cap and age threshold (M12, Write rules).
- **What it is for** — typed entries (decision, fact, lesson, runbook, observation, hypothesis) capturing what is
  not derivable from code, tests or git (Write rules).
- **What goes in** — id, kind, status, author, recorded/observed/verified dates plus the git revision, `covers`,
  `source`/`evidence`, `depends_on`, `supersedes`, `superseded_by` (M11); one file per writer (M23).
- **What does not** — anything derivable from code/tests/git, credentials, unlabelled speculation, bulk
  transcripts, another agent's private state; never delete, only supersede (M13).
- **Where** — `AGENTS.md` at root as the one canonical instruction file with thin adapters (M9), a `memory/` tree
  with a generated `INDEX.md`, typed `entries/`, `work/<task-id>/`, append-only `journal/`, and a gitignored
  `.cache/` for optional derived SQLite/FTS.
- **When used** — at session start: `AGENTS.md`, `INDEX.md`, the `work/` listing and the task's `state.md`; on
  demand by `covers` match, filename/text search, or `git log -S` / `git blame` for line-level "why" (Read rules).
- **When not** — never auto-load `journal/`, `superseded`/`retired` entries, the whole tree, a graph or code-map
  dump, bulk issue bodies, private transcripts, or retrieved text treated as authority (M18, M19).

**It left one gap open rather than inventing it** — the path itself: CP3 is unresolved in the source (claude
proposes `memory/`, codex `docs/memory/`, opencode `.ai/`), so the design marks it
`OPEN: … Choose based on whether the project already has human documentation in docs/`. That is the behaviour the
brief demanded and the previous run's opencode did not show.

## The blind verify, and the plant

Planted: line 35's *"The index must stay under a cap; … the recommendation gives no number, the owner sets it"*
was replaced by an invented *"must stay under **500 entries**"* — a value the source explicitly does not give
(`RECOMMENDATION.md:188-190` says "no number", and line 163 says humans set the index cap).

The verifier: item 1 PASS (eight questions in order, no extra section), item 2 PASS (spot-checked M3, M11, M12,
M13, M18, M19, CP3 and the Read/Write rules sections against the source; no mismatched citation), item 3 FAIL,
item 4 PASS — **`ALTERED: line 35 — "under 500 entries"`** and `VERDICT: REPAIR`. The named line matches the
planted line. On the real design (unplanted) all four items pass.

**This is the check the previous run's design lacked.** There, a verifier that missed its plant still answered
`planted_defect_found: true`; here the artefact named is compared to what was planted, and it matched. Two runs
now agree that the boolean is the weak part and the named location is the usable one.

## Notes and caveats

- **opencode read the source this time.** In the earlier research run it read nothing (7/7 `model knowledge`).
  Given a file to read and a task that requires it, it read it (`→ Read …` in its own stderr). That is evidence
  the earlier result was about the task, not the tool — n=1 each way.
- **The design carries no `model knowledge` labels**, i.e. opencode treats every statement as grounded. The
  verifier found no citation that does not support its sentence, which is the strongest check available here — but
  it is one pass by one engine, and it did not test every sentence.
- **The design is opencode's verbatim stdout**, saved unchanged; `nodes/opencode.stdout.md` is the same bytes, and the published copy adds only a provenance block above the body.
- The eight headings are EJ's eight questions; heading 5 is written as "What will not be put in" (his words were
  "what will not"). Nothing else was added or reordered.

## Files

- `docs/memory-system/SOURCE_OF_TRUTH.md` — the deliverable (moved out of the run folder)
- `brief.md` — the brief opencode received
- `nodes/opencode.stdout.md`, `.stderr.txt`, `.status` — the engine's raw output
- `nodes/verify.stdout.md`, `.stderr.txt`, `.status` — the blind verifier's verdict
- `verify/DESIGN-planted.md` — the planted copy
- `state.md` — the run's state

## Node 3 — codex review: **REPAIR**

`codex-cli` 0.160.0, `-m gpt-6.1-sol -c model_reasoning_effort=medium`, exit 0, 27,972 tokens. A fixed six-item
checklist in one pass, on a copy of the design carrying **one planted control** — the never-delete sentence's
citation changed from `(M13)` to `(M16)`.

**Control: CAUGHT.** *"SOURCE_OF_TRUTH-reviewcopy.md:31: M16 concerns deterministic staleness checks; the
no-deletion rule is M13."* Line and correct row both named, so this review is a check that can fail.

**Verdict: REPAIR**, on ownership. Findings, each re-verified by the COO against the files rather than relayed:

- **OWNERSHIP — FAIL.** Who may revise an entry's body, evidence and verification metadata *after* acceptance is
  unspecified (lines 19, 27); no writer is named for `AGENTS.md`, `CLAUDE.md`, task state, events, journal notes or
  the derived caches, and `INDEX.md` is "generated" with no generator (line 35).
- **CONSISTENCY — FAIL**, three findings, all confirmed:
  1. the design writes `memory/INDEX.md` and a `memory/` tree (lines 35, 41, 45) while declaring the path `OPEN`
     (line 37) — a builder would implement `memory/` while being told it is undecided;
  2. "every entry carries" the full metadata list (line 27) against the source's *"use applicable fields"*
     (`RECOMMENDATION.md:140`) — stricter than what it cites;
  3. line 45's *"Never load the whole memory tree, the full session history…"* drops M18's **auto-**, turning a
     prohibition on auto-loading into an unconditional one (`M18`, `RECOMMENDATION.md:47`).
- **GROUNDING — FAIL**, three beyond the control: line 15's "all project knowledge" against M2/M7; line 23's six
  entry kinds cited to *Write rules* when they come from *Layout*; line 45's M18 over-reach (above).
- **COVERAGE — PASS. NO INVENTED VALUES — PASS.** The OPEN discipline held.
- **GAPS** — five questions a builder still has: who may change each artifact and each mutable field; which
  location replaces OPEN; the index cap and what unit it counts; the age threshold; how code drift and unresolved
  contradictions are caught before an entry determines an action.

What the review does **not** overturn: coverage passes, no value is invented, and the control shows the reviewer
read the source. What it does overturn: the design is **not finished** — the earlier "accepted" in this report and
in the ledger was on four checklist items (coverage, grounding, no invented values, one planted defect); codex ran
a *different* checklist and found a class (ownership) that the first one never asked about.

## Node 4 — Claude Code reviews both tools: **REPAIR**, headline agreed

`claude` 2.1.296, `--model claude-sonnet-5-5`, exit 0, 9.8 KB. It reviewed opencode's design **and** codex's review
of it, adjudicating every codex finding, listing what codex missed, and reconciling its own earlier PASS.

**The control worked.** I had falsified one of codex's findings in the copy it was given (item 3 changed to FAIL,
accusing line 45 of stating a "500 entries" cap). Claude rejected it: *"S:45 says 'the recommendation gives no
number, the owner sets it'. Grep for '500' in S finds nothing."*

**And I must correct its conclusion.** Claude speculated *"Either codex read a copy that is no longer on disk, or it
invented the finding."* Neither is true: **the false finding was planted by the COO as the control; codex never made
it.** Codex's own run passed item 3 (`nodes/codex-review.stdout.md:3`). Left uncorrected, the record would carry a
false accusation against codex, so it is corrected here rather than in a footnote.

**A leak, recorded.** Claude also confirmed codex's third grounding finding (the M16/M13 citation) — but it read
`state.md`, whose log entry calls that row "the planted control". That catch is therefore **not blind**, and it is
weaker evidence than the item-3 catch, which it reached from the files alone.

**What claude found that codex missed** (all re-verified by the COO):

1. **Contested rows are cited as settled.** The design cites M23, M24, M17 and M6 as plain fact, while the source
   marks all four `CONTESTED` (CP4, CP7, CP6, CP1). Only CP3 is flagged in the design. Verified: M17/M23/M24 all
   carry verdict `CONTESTED` in `RECOMMENDATION.md`.
2. **No `model knowledge` label appears anywhere in the design** — the brief required one for every addition.
   Verified: `grep -c "model knowledge"` returns 0.
3. **Staleness is dropped.** The design has humans set an "age threshold" and never says staleness is computed from
   code drift, not age — a builder reading it would implement age-based expiry.
4. **The layout lacks what the design requires** (`work/<task-id>/evidence/`, claim files; `INDEX.md`'s
   "never hand-edited" rule).
5. **`OPEN:` is not in the required form** — the brief asked for what *and by whom*; line 37 omits the "by whom".

**Where claude corrected codex** — and it is right on both, verified:

- codex charged the design with leaving placement OPEN, citing `S:9-10` — but `S:9-10` is the **COO's provenance
  block**, not opencode's text.
- codex charged the design with the "every field" conflict, but **the source contradicts itself**: `M11` says "every
  durable entry carries", `R:140` says "use applicable fields". The design picked the M11 side.
- It also flagged codex's double-counting (the "auto-" slip reported as both a GROUNDING and a CONSISTENCY finding).

**Claude's own reconciliation, quoted:** *"My check matched citation ids to rows. It did not test whether the cited
row supports the sentence… I wrote that check and then passed it, so it is not independent evidence."*

**Verdict: REPAIR**, and `HEADLINE: AGREE` — ownership is the right headline, with the addition that the unlabelled
additions and the silently-settled contested rows belong in it.
