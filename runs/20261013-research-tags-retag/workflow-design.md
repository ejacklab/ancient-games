# Workflow design — 20261013-research-tags-retag

A design, not a run. Sequential by default. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Written by the COO (Claude),
2026-10-13. State: `state.md`. Readiness: `readiness.md`.

## Questions for EJ (answer before running)

| # | Question | Provisional assumption | Blueprint section |
|---|---|---|---|
| Q1 | The control pass re-tags under the "old definitions". `RESEARCH_TAGS.md` quotes the template's **three** labels, but the 143 rows were labelled under `research-agent-memory.js`'s **four** (`unproven` included). Which is the control? | The four the rows were actually labelled under, quoted from git `HEAD` of the `.js` (U1) | none |
| Q2 | `RESEARCH_TAGS.md` names `runs/…-r2/verify/sections/` as the rows' home; that folder holds the verifier's **planted** copy (s2-F8 rewritten). Use `docs/research/20261011-agent-memory-graph-r2/` and correct the path in `RESEARCH_TAGS.md`? | Yes (U2) | none |
| Q3 | Tag sheets and prediction in `runs/20261013-research-tags-retag/` (the file asks for your agreement on the folder)? | Yes (U3) | none |
| Q4 | Both tagging passes on DeepSeek `deepseek-flash` via `dsh headless` (the `classification` default), each in a fresh session? | Yes (U4) | none |
| Q5 | Run the experts before the run, as method 3.3 and 3.5 ask (two calls, about 8 engine answers)? | Yes, at go-ahead (U7) | none |
| Q6 | Issue 3 is not one file: the bundle already carries 16 other `docs/…` paths the same way. Fix it with one mapping line in the bundle README (`docs/X` → `references/x`), not by rewriting paths? | Yes (U9) | none |

## Restatement (method 3.0)

**Objective.** Three open issues from the tag adoption are closed: (1) the blind re-tag with a control has run on
the accepted run's 143 rows and its counts, stuck rows and reading are recorded in `docs/RESEARCH_TAGS.md`; (2)
`.claude/workflows/research-agent-memory.js` no longer carries its own tag definitions or the old worked example;
(3) a reader of the exported bundle can find what `docs/RESEARCH_TAGS.md` means there.
**In scope:** the five r2 findings files (read only), a new run folder, `research-agent-memory.js`,
`tools/export_skills.py` (README text) and the regenerated `skills/`, the results section and the rows' path in
`RESEARCH_TAGS.md`. **Out of scope:** changing any tag definition (EJ's), old findings files, `check-findings.py`,
EJ's operator prompts, the burnt control name in the workflow, committing (only on EJ's word).

Whys: (1) the tags were adopted before anyone tried them on real rows — we do not know if the rule decides rows
without argument; (2) EJ adopted with the check owed; (3) the file prescribes this shape; a sample instead of all
143 would be cheaper but the rows are few and cheap to tag; (4) wrong if the taggers see old labels, if the two
passes differ in engine, or if my count script is wrong — each has a guard below; (5) stops at counts and a
reading; any definition change goes to EJ; (6) done when the counts come from a script shown able to fail and the
prediction predates both tag sheets. Provisional category: `classification` (issue 1), `code generation` (2),
`document and explain` (3) — *inferred*.

Size: issues 2 and 3 are each one sentence of problem, fix and check (§2: not a workflow) — one COO piece each.
Issue 1 has 6 steps and unknowns → this design.

## Blueprint

Kind of task: not a product change (a measurement plus edits to a workflow script and documentation). No sections
needed. Baseline: `env -u NO_COLOR python3 -m pytest -q` → 684 passed, 1 failed (`test_skills_export_is_current`,
fails until `skills/` is committed); and `node runs/20261011-agent-memory-graph/sabotage-harness.mjs` → "all 14
cases behave as designed". Both recorded in `state.md`.

## Pieces, in the order they run

### A — `research-agent-memory.js` points at the one copy (issue 2)

- **Steps:** 1. Replace the label definitions in `SHAPES` (lines 64–65) with "one of verified / reported / unproven /
  unknown, defined in `docs/RESEARCH_TAGS.md`". 2. Rewrite the `EXAMPLE` row (lines 82–83): a vendor blog that only
  asserts is `unproven`. 3. Run the checks.
- **Category:** code generation · **Pattern:** step · **Builds:** yes (a workflow script) · **Criteria:** none in a
  blueprint; the stop is the three-part stop below.
- **Check (script):** `node --check` on the file; the harness still prints "all 14 cases behave as designed";
  `grep -c "the primary document was read; reported = a secondary source"` → 0. Sabotage: the harness is known to
  fail (it has planted cases); the grep was 1 before the edit.
- **Must not change:** `LABELS` (the same four words), `CONTROL`, the check functions, the section questions.
  Note: the workflow already records not-found in a separate `control_answer` field, so the new "a gap is prose,
  not a row" rule needs no code change.
- **Role and engine:** COO herself (Claude Opus 5.5, session effort) — two string edits, a check she cannot edit.
- **Evidence:** the three commands and outputs → `evidence/A.txt`. **State:** writes A done.
- **Order:** runs **after** R1 has quoted the old definitions from git `HEAD` (Q1), so the control quote is the text
  the rows were labelled under, not the edited one.

### B — the bundle tells its reader where `docs/` files went (issue 3)

- **Steps:** 1. In `tools/export_skills.py`'s README text, under "What travels", add one line: the bundled copies of
  `docs/WORKFLOW_DESIGN_METHOD.md`, `docs/TASK_TYPES.md`, `docs/EXECUTOR_KINDS.md`, `docs/FEEDBACK_TEMPLATES.md`,
  `docs/RESEARCH_TAGS.md` and `docs/workflow-templates/` are `references/method.md`, `references/task-types.md`,
  `references/executor-kinds.md`, `references/feedback-templates.md`, `references/research-tags.md` and
  `assets/templates/`. 2. Regenerate with `python3 tools/export_skills.py`. 3. Check.
- **Category:** document and explain · **Pattern:** step · **Builds:** yes (the export's text)
- **Check (script):** a check script reads the mapping line and asserts every named bundle path exists under
  `skills/workflow-design/`; sabotage: misspell one path in a copy → it fails. `pytest` unchanged except the export
  test, which passes once `skills/` is committed.
- **Must not change:** `skills/` by hand; any other bundle file.
- **Role and engine:** COO herself. **Evidence:** `evidence/B.txt`.

### R1 — blind sheet and key

- **Steps:** 1. `make_blind.py` reads the five `docs/research/20261011-agent-memory-graph-r2/FINDINGS-s*.md`
  files, takes id, Finding, Label and the rest as Source (7 rows carry `|` inside the Source; cells after the third
  are joined), renumbers rows R001–R143 in an order shuffled with a fixed seed, and writes `blind/rows.md` (id ·
  Finding · Source — no Label) and `key/old-labels.json` (R-id → section id, original id, old label). 2. It quotes
  the old definitions from `git show HEAD:.claude/workflows/research-agent-memory.js` into `blind/control-defs.md`.
  3. It counts rows whose Finding text carries a tag-like word (13 found in readiness) → `blind/leaks.txt`.
- **Category:** information extraction (a script) · **Pattern:** step
- **Check (script):** 143 rows; ids unique; every R-id in the key; old-label counts 94 / 44 / 3 / 2; no row in
  `rows.md` contains a Label cell. Sabotage: drop one row from a copy → the check fails.
- **Must not change:** the r2 findings files. **Role:** COO. **Evidence:** `evidence/R1.txt`.

### R2 — count script, written before any tag sheet exists

- **Steps:** 1. `count.py` reads the key and one tag sheet and gives, per row, *same* / *moved* (old → new) /
  *split* (old → tag of each part) / *stuck* (between which two); per pass the four totals, a movement matrix, and
  every stuck row by R-id and original id. 2. A fixture sheet with known answers (written by hand: 2 same, 2 moved,
  1 split, 1 stuck) → the script must report exactly those. 3. Sabotage: one fixture row changed → it reports the
  change.
- **Category:** code generation · **Pattern:** loop (attempt limit 3, feedback = the fixture diff; exit → EJ)
- **Check (script):** the fixture test above. Who wrote it: the COO — so the counts are not independent evidence;
  the sheets and the key are saved so EJ can recount any row by hand.
- **Role:** COO. **Evidence:** `evidence/R2.txt`.

### R3 — prediction, before either tagger starts

- **Steps:** 1. The COO writes `prediction.md`: the metric (R2's four totals for both passes), the expected result,
  a stop date, and the UTC time. 2. Its `sha256sum` and time go into the `state.md` Log.
- **Check:** the Log line's time is earlier than both tag sheets' first line time (script, at R6).
- **Role:** COO. Not delegated: the prediction is the COO's own claim.

### R4 — control pass

- **Steps:** one tagging call, then the schema check.
- **Category:** classification · **Pattern:** loop · **Attempt limit:** 2 · **Exit:** to EJ — not a stronger tier,
  because a different engine for one pass breaks the comparison; an escalation re-runs both passes on the new tier.
- **Check (script):** `tags/control.jsonl` has 143 lines, every R-id once, each tag one of the four old labels.
  Sabotage: a fixture with a missing id and a fifth label → 2 failures.
- **Feedback:** the check's real output.
- **Context — given:** the brief (`briefs/R4.md`: the old definitions quoted verbatim, the output format, one
  worked example row that is not from the 143), `blind/rows.md`. **Withheld:** `key/`, the original findings
  files, `RESEARCH_TAGS.md`, `prediction.md`, the other pass. The brief names only its two files; dsh can read the
  repository, so the blind is by instruction plus renumbering — not enforced (U5).
- **Returns:** `tags/control.jsonl` — `{"id": "R001", "tag": "verified"}`.
- **Role and engine:** classifier — `dsh headless`, DeepSeek `deepseek-flash`, effort low, fresh session; prompt in
  the file, stdin from `/dev/null`, a timeout (memory notes). **Evidence:** the raw output → `raw/R4-<n>.txt`.

### R5 — new-rule pass

- Same as R4 except: the brief quotes `docs/RESEARCH_TAGS.md`, section "The tags", verbatim; each line is
  `{"id", "tag"}` or `{"id", "split": [{"part", "tag"}, …]}` or `{"id", "stuck": [tag, tag], "why"}`. Check: 143
  ids, tags from the four, a split has ≥ 2 parts, a stuck names two different tags and a reason. Same engine, model
  and effort as R4, a different fresh session. **Withheld** additionally: `tags/control.jsonl`.

### R6 — count, read, record

- **Steps:** 1. Run `count.py` on both sheets → `counts.md`; run the R3 time check. 2. Write `result.md`: both
  passes side by side, the stuck rows with weight equal to the totals, the reading by the file's step 6 (any stuck
  row → definitions to EJ; new-rule movement no larger than control → no measurable difference), the leak count
  from R1, who tagged each pass. 3. Replace "The check still owed" heading's status in `docs/RESEARCH_TAGS.md`
  with the result and a link — numbers only; no definition is touched.
- **Check:** `counts.md` regenerates byte-identical from the saved sheets (script); the result's numbers are the
  script's (a grep of each number in `counts.md`).
- **Role:** COO.

## Joins

R6 joins R4 and R5 through the key. A contradiction between the passes is the result, not a stop. A stop is: a sheet
that fails its schema twice (to EJ), or the R3 time check failing (the prediction is void; reported, not repaired).

## Parallel candidates

R4 and R5 meet all five conditions (neither needs the other, separate output files, one would not change the other,
each has its own check, the join is R6 anyway). **Not taken**: the saving is a few minutes, and sequential is the
default (EJ). A and B are independent of R1–R6 apart from A's ordering after R1.

## Predictability

- Design source: default — `classification` row (single routing node, `deepseek-flash`, schema check + agreement on a
  labelled sample; the agreement here is the comparison with the control). No challenger claim; a ledger row at the end.
- Agents: 2 engine calls (R4, R5), up to 4 with retries; the rest is the COO. Expert calls (Q5): 2 runs, 8 answers.
- Cost estimate: each pass reads ~15k tokens of rows plus a ~3k brief and writes ~6k → about 25–40k tokens per
  pass on a cheap tier; COO work about 60–100k. Unmeasured (n=0).
- Success criteria, written before the run: the objective's three clauses, each with its script check above.

## Debuggability

Labels: `A`, `B`, `R1`…`R6`. Every input and output is a file in this folder (`blind/`, `key/`, `briefs/`, `raw/`,
`tags/`, `evidence/`). Resume point: the first piece not marked done in `state.md`; a failed pass re-runs alone.

## Quality control

- Scripts: A's three checks, B's path check, R1's sheet check, R2's fixture test, R4/R5's schema checks, R6's
  regeneration and time checks. Each is shown able to fail by its sabotage above.
- Judged: nothing. EJ's: what a stuck row means for the definitions.
- What is missing, at the end: the COO compares `git status --short` with `.baseline-git-status.txt`; the run may
  add files only in this folder and change only `research-agent-memory.js`, `tools/export_skills.py`, `skills/` and
  `docs/RESEARCH_TAGS.md`. Anything else found goes to EJ as a note, not into this run.
