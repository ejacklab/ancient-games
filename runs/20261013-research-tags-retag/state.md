# State — 20261013-research-tags-retag

Rules: one writer at a time. Read this file before your step; update it after. Progress and results only — never
reasoning. Never delete a log line.

## Challenge (verbatim)

"design a workflow to fix these 3 open issues" — the three, as the COO listed them on 2026-10-13: (1) the blind
re-tag with a control in `docs/RESEARCH_TAGS.md` has not run; (2) `research-agent-memory.js` still carries the old
tag definitions; (3) in the exported bundle, the template points to `docs/RESEARCH_TAGS.md`, which sits at
`references/research-tags.md`.

## Restatement

See `workflow-design.md`, "Restatement".

## Baseline

`git status --short` before the run folder: `.baseline-git-status.txt` (35 lines).

## Product baseline

```
env -u NO_COLOR python3 -m pytest -q        → 684 passed, 1 failed (test_skills_export_is_current; skills/ uncommitted)
node runs/20261011-agent-memory-graph/sabotage-harness.mjs → all 14 cases behave as designed
```

## Steps

| # | Piece | Status | Output file |
|---|---|---|---|
| 1 | R1 blind sheet and key | done | blind/, key/, evidence/R1.txt |
| 2 | A research-agent-memory.js | done | evidence/A.txt |
| 3 | B bundle mapping line | done | evidence/B.txt |
| 4 | R2 count script | done | count.py, evidence/R2.txt |
| 5 | R3 prediction | done | prediction.md |
| 6 | R4 control pass | done | tags/control.jsonl |
| 7 | R5 new-rule pass | done | tags/new.jsonl |
| 8 | R6 count, read, record | done | counts.md, result.md |

## Blueprint

Kind of task: not a product change. Map: none. Needed sections not settled: none.

## Size decision

design — issue 1: 6 pieces, unknowns; issues 2 and 3: one COO piece each. Risk: low (no definition changes; all
reversible).

## Unclear spots

| Id | What is unclear | Kind | Blueprint | Blocks | Depends on | Raised by |
|---|---|---|---|---|---|---|
| U1 | Which old definitions the control uses: the template's three or the workflow's four the rows were labelled under | decision | none | R1, R4 | — | COO |
| U2 | `RESEARCH_TAGS.md` names `verify/sections/` for the rows; that copy is planted (s2-F8) | information — found | none | R1 | — | COO (readiness) |
| U3 | Run folder for the tag sheets | decision | none | R3–R6 | — | RESEARCH_TAGS.md |
| U4 | Engine for both passes | decision | none | R4, R5 | — | COO |
| U5 | The blind is by instruction: dsh can read the repo; 13 of 143 Finding texts carry a tag-like word | unknown — counted, not resolved | none | none (read the result as a comparison) | — | COO; Dave (earlier review) |
| U6 | Taggers see only the row text, not the sources: "what was inspected" is judged from what the row shows | information — accepted limit | none | none | — | COO |
| U7 | Experts before the run | decision | none | R4, R5 | — | method 3.3 / 3.5 |
| U8 | The control quote must come from git `HEAD` before piece A edits the file | ordering — designed in | none | A after R1 | U1 | COO |
| U9 | Issue 3 is a bundle-wide convention (16 other `docs/` paths), not one file | decision | none | B | — | COO (readiness) |

Experts asked (method 3.3): experts/unclear-spots/ (linus, sun-tzu, lao-tzu, dave); method 3.5: experts/loop-check/ (linus, fan-li, sun-tzu, dave).

## Questions for EJ (one batch)

Q1–Q6 in `workflow-design.md`.

## Log (append only)

- 2026-10-13 design written by the COO; nothing run except readiness checks (readiness.py, the harness, row counts).
- 2026-10-13 EJ: "go" — Q1–Q6 provisional assumptions stand.
- 2026-10-13 experts asked: experts/unclear-spots (linus, sun-tzu, lao-tzu, dave) and experts/loop-check (linus, fan-li, sun-tzu, dave).
- 2026-10-13 R1 done: 143 rows, check PASS, sabotage fails (evidence/R1.txt). U8 changed: the .js is untracked (no git HEAD), so the control quote is from the working file before piece A, sha256 fb8ea1c2…08ac.
- 2026-10-13 A done: node --check exit 0; harness 14/14; old-definition grep 0 (evidence/A.txt).
- 2026-10-13 B done: README mapping line, 6 mappings, check PASS, sabotage fails (evidence/B.txt). RESEARCH_TAGS.md: rows path and control definitions corrected (Q1, Q2).
- 2026-10-13 R2 done: count.py fixture PASS, sabotage FAIL as required (evidence/R2.txt); sheet schema check proven both ways (evidence/R4-R5-check.txt).
- 2026-10-13 order slip (raised by 孫子): R1, A, B, R2 ran while the experts were still answering; the design said experts first. None touched a tagger.
- 2026-10-13 experts → changes: 3 control rows (R058 R091 R120) reported apart (老子); split counted both ways (Dave, Linus); key moved to the scratchpad during passes; taggers run in an empty work dir with dsh --json, every tool call audited, a read outside the two files voids the pass; 3 plants with known answers in the tagger sheet (146 rows, T-ids); same worked example in both briefs (Dave); sheet check: one shape per line, split parts differ (Linus, 范蠡, Dave) — evidence/R4-R5-check-v2.txt, evidence/run_pass-sabotage.txt. dsh --json canary: tool calls visible (verified).
- 2026-10-13 R3 done: prediction.md sha256 62e27357…6183e; sent to EJ in the chat before R4.
- 2026-10-13 EJ: "ok go" — taken as yes to a second control pass (control2, after R5) and to 140 rows as the main count.
- 2026-10-13 R4 done: schema PASS, audit clean (read brief.md, rows.md only), plants right; tags/control.jsonl moved to the scratchpad during R5 (hashes in raw/control-hashes.txt).
- 2026-10-13 R5 done: schema PASS, plants right; audit 2 flags checked by hand: the tagger wrote output.jsonl in its own work dir and ran a python check reading only that file — no read outside. tags/new.jsonl moved aside during control2 (raw/new-hashes.txt).
- 2026-10-13 control2 attempt 1: schema PASS, audit clean, plant PB failed (expected reported, got unproven) → attempt 2 (fresh session), sheets and key hidden again.
- 2026-10-13 control2 attempt 2: schema FAIL (a prose line before the 146 JSON lines) → limit reached, to EJ; not patched. Main comparison rests on control and new.
- 2026-10-13 R6 done: counts-140.md / counts.md; result.md; RESEARCH_TAGS.md result paragraph added (numbers only, no definition touched). Ledger row: not written — docs/TASK_TYPES_LEDGER.md carries another session's uncommitted edits; to add at commit time.
- 2026-10-13 EJ: "run control2 once more" — attempt 3, beyond the limit of 2, by EJ's decision; sheets and key hidden again.
- 2026-10-13 control2 attempt 3: schema PASS, audit clean, plants right. Noise floor 11 rows (control vs control2); new vs controls 26 / 21. result.md and RESEARCH_TAGS.md updated; counts.md and counts-140.md regenerated with three sheets.
- 2026-10-13 EJ: "replace the plant, then commit" — PB replaced in run_pass.py for later runs; results not re-run.
