---
node: n4-merge
attempt: 1
engine: claude
model: claude-sonnet-5-5
status: ok
started: 2026-10-08T01:09:16.402Z
ended: 2026-10-08T01:09:52.551Z
evidence: none
---

## Added
I used attempt 2 of each node (n1, n2, n3) as the latest result files. I replaced the "12–16 not yet walked" row in `docs/FEEDBACK_TEMPLATES.md` with five table rows and added a section for each type. All five are marked proposed, n=0, and not yet walked with EJ. I did not edit the 11 settled rows or sections. The only change near them is an inserted block before the "`Effort` goes on every loop type" line.
- 12 `multi step planning` (no loop): Objective / Nodes / Coverage / Method / Unclear
- 13 `repo scanning` (no loop): Scope / Coverage / Findings / Source (code graph) / Unclear
- 14 `research and reports` (no loop): Answer / Findings (CONFIRMED / INFERRED / GAP) / Gaps
- 15 `grade a run` (no loop): Run / Against / Rubric / Result / Unclear
- 16 `others` (loop "—"): Done / Evidence / Findings. `Effort` is added only if the brief runs the node as a loop. `Source` is added only if there is a source.

## Flags
- **`grade a run` Result:** `Result` is not in the type's decided shape. It is derived mechanically from the worker's own Rubric lines. It sits close to a verdict, but it reports whether the proof is complete, not whether the run passed. EJ should confirm it is the worker's field.
- **`repo scanning` Coverage:** the sections write the rows and the join concatenates them. This is still one writer per row, but the join touches the field. I recorded it as "join does not re-derive".
- **`research and reports` labels:** n3 dropped `UNPROVEN`, which `TASK_TYPES.md:100` lists as a fourth label, and writes a missing proof as `GAP`. n3 also uses `CONFIRMED` where `web search` uses `FACT`. I kept n3's three labels. The table and template disagree until EJ rules.
- **`others` Effort and Source:** conditional fields are a new pattern. The settled rule says `Effort` is for loop types only, and `others` has no default loop status. I kept n1's "only when the brief says loop".
- **`others` Unclear:** I dropped it. n1 removed it because the pass-back `UNCLEAR:` line already covers the escape, which differs from `code review`.
- **Stale prose in the settled part:** line 28 still says `repo scanning`, `code review` and `debugging` are "to come". I left it unchanged under the "11 unchanged" rule.
- **Whys not carried over:** the "Whys" blocks in the result files are not merged into the doc. Only the field shapes and one-line notes are.
- **Pass-back header:** n3's `model:` is empty, which is allowed for a no-model engine (commit bde3f92).
