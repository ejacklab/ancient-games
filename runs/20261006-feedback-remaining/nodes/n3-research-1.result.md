---
node: n3-research
attempt: 1
engine: dsh
model: 
status: ok
started: 2026-10-08T01:02:35.048Z
ended: 2026-10-08T01:03:27.838Z
evidence: none
---

## research and reports
- Answer (worker): <what is true in answer to the question asked, in the report's own words, one id per finding it rests on (`F1`, `F3`, …); a finding that rests on nothing or contradicts another is written as unresolved here, never as the answer>
- Findings (worker): <one line each — `<id> <claim> — CONFIRMED | INFERRED | GAP — <citation>`. The marker follows the claim on the same line so the finding reads as one row; `CONFIRMED` = the named source was read and says it, `INFERRED` = it follows from the `CONFIRMED` lines and names them, `GAP` = a fact the question asked for that was not found, with the query and where it was searched. Citation: the opposing or alternate source is named on the same line (`both sides: <source A> | <source B>`, each a URL with its date or a `file:line` plus a verbatim quote ≥8 chars), and `— none` when no source opposes it. An id is used once; a join that finds the same id twice with different claims is a contradiction>
- Gaps (worker): <what the question presupposed that was not settled — the residue of the answer, not the per-claim `GAP` lines, each with where it was looked for and `UNCLEAR: <question> / <best guess>` when the worker had to proceed on a reading; or "none">

## Whys

**research and reports / Answer (kept)**
1. Why is the answer a field? The type's check is "answers the question", so the return must carry the answer somewhere; a report that only lists findings makes the reader reconstruct it and hides a wrong synthesis behind right facts.
2. Why is it not the findings list itself? A synthesis can be wrong while every finding is right. The field is the witness for that failure, and it is what the join compares across sections.
3. Why does the worker write it? It is the only one who read every source; a summary written by the join or the human is a re-synthesis, i.e. a second run of the same work.
4. Why the finding ids on it? The answer can only be audited if each claim points at the line it rests on. Quoting no ids makes the answer unfalsifiable; quoting an id makes the audit one grep of `Findings`.
5. How does it fail? Empty, or it answers a different question, or it rests on an id that `Findings` does not contain — the first thing the join and the checklist read.

**research and reports / Findings (kept)**
1. Why one more field than a plain findings list? The check is "every finding carries both-side citations and a CONFIRMED/INFERRED marker", and `web search` already borrowed this type's `FACT / INFERRED / GAP` vocabulary. Same reader, same words: `CONFIRMED` pairs with `FACT`, `GAP` with `GAP`.
2. Why both-side citations? One side is an assertion. The opposing source named on the same line is what turns a claim into something a second reader can check without re-searching — and what the seeded-divergence sabotage proves (a known divergence must appear as a row carrying both citations).
3. Why the ids? The join reconciles sections without re-deriving: the same id twice with different claims is the contradiction the type's check stoppers on; without ids there is nothing to match.
4. Why `GAP` inside `Findings` when `Gaps` exists? A `GAP` finding is the claim-level not-found ("asked fact, searched query, nothing found"); `Gaps` is the question-level residue. Different levels, different reader action.
5. Why does the writer have to be the worker? Only it saw the sources in time; a verifier can mark agreement or disagreement but cannot supply a citation it never saw, and never upgrades a marker (`verified` = the primary source was read).
6. How does it fail? A missing marker, a missing citation, or a claim whose citation does not contain it — the type's own sabotage seeds a known divergence exactly to catch the first two.

**research and reports / Gaps (kept)**
1. Why keep the not-found half on the question as well as the claim? Missing proof must never read as PASS: a report whose `Findings` is all `CONFIRMED` and whose `Gaps` is silent reads as complete even when part of the question was never asked.
2. Why is this the worker's field? Only it knows what the question presupposed and what it searched; a gap stated at the join would be a claim about work the join never saw.
3. Why is it separate from `Answer`? An answer and the list of what it does not settle are two facts; merged, every gap inherits the answer's confidence.
4. How does it fail? A question the report could not answer and never states — the seeded conflicting sources make the join stop, and a missing `Gaps` row is how that stop is detected.

**removed: Effort**
1. Why no `Effort`? The settled rule puts `Effort` (tokens + rounds) on loop types only; this type is a single node or sectioning + join, and a re-run is a new node, not another round.
2. Why does a redo not count as a round? A round is thrash inside one loop with a feedback path; a new section is a new call whose cost is the design's, not the worker's return.

**removed: Source and the code-graph tool**
1. Why no `Source`? A report's source can be web, code, documents or any mix; naming one graph would be wrong when the report draws on several, and blank where a finding's source is not code.
2. Why not the code-graph tool, as `repo scanning` and the code-sourced types carry it? A report is not necessarily code-sourced. When it is, the read is its own deliverable and its own category (rule 1 forbids a passenger label); the citation in each line carries the graph there.

**removed: Disputed and Verdict**
1. Why no `Disputed` when `web search` has one? The both-side citation on each `Findings` row already carries the disagreement, and this type's own sabotage test is written as "appear as a row with both citations" — a separate `Disputed` section can only duplicate that row or move a judgment out of `Findings`, where the marker sits.
2. Why no `Verdict`, `Accepted` or `Agreement`? Whether the answer is good enough is the human's or the verifier's judgment, and it happens after the worker has written. A field the worker guesses at breaks the one-writer rule; the worker's `Gaps` row is the question, not its own grade.

UNCLEAR: does `Findings` merge into one list at the join, or stay per-section with the join only diffing ids? / best guess: stay per-section (each section owns its worker-written rows and its `Answer`), with the join diffing ids and stopping on a repeated id whose claim differs — a merged list would be a field written by the join, which is a second writer.
