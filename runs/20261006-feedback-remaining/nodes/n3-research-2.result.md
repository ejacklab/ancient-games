---
node: n3-research
attempt: 2
engine: dsh
model: 
status: ok
started: 2026-10-08T01:08:09.420Z
ended: 2026-10-08T01:09:16.387Z
evidence: none
---

## research and reports
- Answer (worker): <what is true in answer to the question asked, in the report's own words, naming the finding ids it rests on (`F1`, `F3`, …); a part of the question no finding settles is written here as unresolved, never as if answered>
- Findings (worker): <one row per finding — `<id> <claim> — CONFIRMED | INFERRED | GAP — <citation>`. `CONFIRMED` = a named source was read and says it; `INFERRED` = it follows from the `CONFIRMED` rows and names them; `GAP` = the question asked for it and it was not found or not settled, with the query run and where it was searched. Citation = both sides on the row: `both sides: <A> | <B>`, each a `file:line` with a verbatim quote (≥8 chars) or a `URL` with its published date (`undated` allowed); `— none` when no source opposes. An id is used once per section; the join stops when the same id carries a different claim>
- Gaps (worker): <the question-level residue — what the question presupposed that no finding settles, each with where it was looked for and why it stays open; or "none">

## Whys

**research and reports / Answer (kept)**
1. Why is the answer a field at all? The type's check is literally "answers the question" (`TASK_TYPES.md:100`); a return that lists findings and never states the answer leaves the reader to synthesize it, so the check cannot be run on the return.
2. Why not let the findings list be the answer? A synthesis can be wrong while every finding is right. The field is where that failure is visible, and it is what a join compares across sections — the same separation `web search` made by keeping its query log distinct from `Found`.
3. Why does the worker write it? Only the worker read every source and can say what they jointly support; the join or the human re-synthesizing would be a second writer of a fact already written (`FEEDBACK_TEMPLATES.md:7`).
4. Why must it name the finding ids it rests on? It makes the answer auditable in one pass against `Findings`; an answer resting on an id `Findings` does not contain fails without re-searching anything, and quoted ids make the field falsifiable.
5. How does it fail? Empty, or answering a different question than the brief's, or asserting more than the named findings support — including writing a `GAP` part as if answered, which is the failure "missing proof never reads as PASS" names.

**research and reports / Findings (kept)**
1. Why this field? It is the other half of the check: every finding carries both-side citations and a `CONFIRMED/INFERRED/GAP` marker (`TASK_TYPES.md:100`). A claim with no marker or no citation is an assertion the check cannot test.
2. Why is the marker on the same row as the claim? A status is only meaningful next to the claim it labels; a separate certainty list decouples and drifts, and `web search` set the precedent by folding `FACT/INFERRED/GAP` into each `Found` line.
3. Why these three labels? `web search` already borrowed this type's vocabulary as `FACT / INFERRED / GAP` (`TASK_TYPES.md:100`), so the mapping is one-to-one — `CONFIRMED` pairs with `FACT`, `GAP` with `GAP` — and a reader who knows one template reads the other without a key. The row's fourth term, `UNPROVEN`, is not a separate label here: a claim whose proof is missing is written `GAP` with the missing proof and where it was sought, so the label set stays exactly the three the two templates share.
4. Why both-side citations on each row? One side is an assertion; the opposing or alternate source named on the same row is what makes the claim checkable without repeating the search. The type's own sabotage seeds a known divergence, and the proof is that it "appears as a row with both citations" (`TASK_TYPES.md:100`) — the row is the unit, not a second section.
5. Why must the citation quote or date the source? A `file:line` with a verbatim quote (≥8 chars) or a URL with its published date is what a second reader can re-fetch and re-read; a bare URL or a paraphrase is unfalsifiable, the same defect as bare `Validated: passed` in `test data gen`.
6. How does it fail? A missing marker, a missing citation, an `INFERRED` that names no `CONFIRMED` row, or a citation that does not contain the claim — the seeded divergence catches the last; `GAP` must name the searched query so "not found" is not read as "does not exist".

**research and reports / Gaps (kept)**
1. Why keep it when `Findings` already has a `GAP` row? They are different levels: a `GAP` finding is the claim-level "this asked fact was searched for and not found"; `Gaps` is the question-level residue — what the question presupposed and no finding settles. Missing proof must never read as PASS, and this is the question's own not-found.
2. Why is it the worker's field? Only the worker knows what it searched and what the question assumed; a gap written at the join or by the verifier would be a claim about work they never saw (`FEEDBACK_TEMPLATES.md:7`).
3. Why separate from `Answer`? An answer and the list of what it does not settle are two facts; merged, every gap inherits the answer's confidence and the reader cannot tell which part is open.
4. Why "or none"? An absent field cannot be told apart from a worker that never looked, so the not-found half is written even when it is empty — the same negative `Look` and `Coverage` write (`FEEDBACK_TEMPLATES.md:33`).
5. How does it fail? A question the report could not answer and never states, or a gap left implicit so the section reads as complete. The type's second sabotage — seed conflicting sources, the join must stop — is detectable only if the conflicting row is present, and the join reads the sections' returns.

**removed: Effort**
1. Why no `Effort`? The settled rule puts `Effort` (tokens + rounds) on loop types only (`FEEDBACK_TEMPLATES.md:21`), and this type's pattern is "single node, or sectioning + join" (`TASK_TYPES.md:100`) — there is no loop.
2. Why is a re-run not a round? A round is thrash inside one loop with a feedback path; a re-run or a new section is a new call whose cost belongs to the design, not to the worker's return.

**removed: Source and the code-graph tool**
1. Why no `Source`? The code-sourced types carry `Source` naming the graph; this type's source can be code, web or documents, so naming one graph would be wrong when the report draws on several and blank when it does not.
2. Why not carry the code-graph tool anyway? A report is not necessarily code-sourced; when the read is code, that read is its own deliverable and its own label (`repo scanning`), which labelling rule 1 forbids as a passenger (`TASK_TYPES.md`). The `file:line` citation on each finding carries the graph where it applies.

**removed: Disputed, Verdict and Agreement**
1. Why no `Disputed`, when `web search` has one? The both-side citation is already on each `Findings` row, and this type's sabotage is written as "appear as a row with both citations" — a separate section could only duplicate that row or move the disagreement out of the row where the marker sits.
2. Why no `Verdict`, `Accepted` or `Agreement`? Whether the answer is good enough is the human's or the verifier's judgment and happens after the worker writes; a field the worker guesses at breaks the one-writer rule, and the worker's `Gaps` row is the open question, not its own grade (`FEEDBACK_TEMPLATES.md:7`).
