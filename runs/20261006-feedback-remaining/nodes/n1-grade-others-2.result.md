---
node: n1-grade-others
attempt: 2
engine: claude
model: claude-opus-5-5
status: ok
started: 2026-10-08T00:59:20.219Z
ended: 2026-10-08T01:00:09.734Z
evidence: none
---

## grade a run
- Run (worker): <the run directory it graded, `runs/<run-id>/`, copied from the brief and not re-derived>
- Against (worker): <the rubric's path or id and its version, copied from the brief>
- Rubric (worker): <one line per rubric dimension: `<dimension> — PASS | FAIL — <proof: path:line inside the run directory>`, or `<dimension> — UNKNOWN — looked for <what> at <path>: absent`. Each dimension's verdict stays separate. No total and no score.>
- Result (worker): <`INVALID_RUN — UNKNOWN on: <dimension, dimension>` if any dimension has no run-directory proof; otherwise `VALID — all N dimensions have proof`. This says whether the proof is complete. It does not add up the verdicts. An empty run directory gives UNKNOWN on every line and INVALID_RUN here, never PASS.>
- Unclear (worker): <each dimension whose wording could not be applied to this run as written, and the reading used; or "none">

## others
- Done (worker): <what was done, one line per deliverable, with where it is (a path, or "inline below")>
- Evidence (worker): <the proof for each line in Done: a re-runnable check and what it showed, or a file under `runs/<run-id>/`; or "none — unchecked", written out>
- Findings (worker): <what the work found, one line each; or "none">
- Effort (worker): <tokens + rounds>. Only when the design runs this node as a loop.
- Source (worker): <what the work was taken from; when the source is code, this names the code graph used>. Only when there is a source.

## Whys

**grade a run / Run (kept)**
1. Why name the run? The verdicts mean something only for one specific directory.
2. Why not let the proof paths show it? An empty run has no proof paths, and the empty run is the sabotage case.
3. Why does that matter? Without Run, "INVALID_RUN on an empty directory" and "graded the wrong directory" look the same.
4. Why copy it from the brief? This is the classification `T` lesson: the worker repeats its input instead of re-deriving it, so a mismatch shows.

**grade a run / Against (kept)**
1. Why name the rubric? A verdict counts only against a standard. Code review has `Against` for the same reason.
2. Why give the version? If the rubric changes between runs, two PASS results cannot be compared.
3. Why does the worker write it? Only the worker knows which rubric it actually applied.
4. Why keep it apart from Run? The run and the rubric are two facts, and each can be wrong on its own.

**grade a run / Rubric (kept, changed: per-dimension value is now PASS | FAIL | UNKNOWN)**
1. Why one line per dimension? The type's check is "verdicts kept separate per dimension".
2. Why no total? A total lets one FAIL hide under three PASS results.
3. Why is the proof on the same line as the verdict? Without the pairing, you cannot tell which proof backs which verdict. This is the web-search claim-plus-source lesson.
4. Why UNKNOWN and not INVALID_RUN on a dimension? Decided on 2026-10-08: INVALID_RUN is a verdict on the whole run. TASK_TYPES' "UNKNOWN/INVALID_RUN" names two things, so the dimension gets UNKNOWN and the run gets INVALID_RUN.
5. Why write out "looked for X at Y: absent"? A blank would read as PASS. Written out, it is a claim that can be checked and can fail.
6. Can it fail? Yes: a missing dimension, a PASS with no path, or a path outside `runs/<run-id>/`.

**grade a run / Result (added)**
1. Why add it? Decided on 2026-10-08: if any dimension lacks run-directory proof, the run-level result is INVALID_RUN.
2. Why does the worker write it, when "a verdict lives elsewhere"? It follows mechanically from the worker's own Rubric lines. Any UNKNOWN means INVALID_RUN. It contains no judgment, and only the worker produced those lines.
3. Why is it not an overall PASS? It reports whether the proof is complete, not whether the run passed. The per-dimension verdicts still stay separate.
4. Why list which dimensions are UNKNOWN? The reader can check Result against Rubric line by line, so a contradiction between them shows.
5. Why does the empty-run case appear here? It is the type's sabotage check: an empty run must give INVALID_RUN, never PASS.

**grade a run / Unclear (kept)**
1. Why keep it? A fixed rubric can still have a dimension that does not fit this run.
2. Why not grade it silently? A silent reading becomes a hidden verdict on the rubric itself.
3. Why here? `code review` (11) settled `Unclear` as the home for the `UNCLEAR:` escape in review-shaped, no-loop types.

**grade a run / removed: Accepted, Agreement, overall score**
1. Why remove them? Whether to accept the grade is the human's or the verifier's decision.
2. Why can't the worker hold them? The worker writes before anyone has looked, so a field someone else fills later breaks the one-writer rule.
3. Where do they go? To the loop's exit and the state file.

**grade a run / removed: Effort, Source**
1. Why no Effort? `grade a run` has loop = no, and Effort is for loop types only.
2. Why no Source or code graph? Its source is a run directory, not code. Run already names it.
3. Why not add them anyway? A field that is never filled becomes a blank that looks like data.

**others / Done (kept, from the decided skeleton)**
1. Why? Every task returns something, and the reader must be able to find it.
2. Why not `Changed` or `Created`? Those words already have fixed meanings (files touched, tests made), and an `others` task may be neither.
3. Why "where it is"? The deliverable and its proof can be different files.

**others / Evidence (kept, from the decided skeleton)**
1. Why? `others` has check = "—", so no verifier is defined.
2. Why does the worker's evidence matter more here? It is the only check there is.
3. Why write out "none — unchecked"? Fail Loud: silence would be read as checked.
4. Why point into `runs/<run-id>/`? The 2026-10-06 rule (SHOULD, n=1): proof in `/tmp` was deleted and the fix became unverifiable.
5. How does it differ from the header's `evidence:`? The header points to one path. This field pairs each Done line with its proof.

**others / Findings (kept, from the decided skeleton)**
1. Why? An `others` task can learn something that is not a deliverable, such as a blocker, a surprise, or a fact.
2. Why separate from Done? Two things: what was made, and what was learned.
3. Why write out "none"? Then an empty field is a claim, not an omission.

**others / Effort (conditional)**
1. Why conditional? `others` has no default pattern. The method may make it a loop or a single node.
2. Why only for loops? This is the settled rule, with unit tokens + rounds.
3. Who knows if it is a loop? The design states it in the brief, and the worker reads it there. No one fills the field later.

**others / Source (conditional)**
1. Why conditional? Decided on 2026-10-08: Source appears only when there is a source.
2. Why name the graph when the source is code? This is the settled rule for types whose source is code.
3. Why not always include it? Many `others` tasks have no source, and a forced field gets made-up content.

**others / removed: Unclear, Closest type**
1. Why remove Unclear? The decided skeleton is three fields, and the pass-back's `UNCLEAR:` line already covers the escape for every node.
2. Why remove Closest type? It serves the `TASK_TYPES` ledger, not the reader of this return. It is a different artifact with a different maker.
3. Where does it go? The designer records it in `TASK_TYPES_LEDGER.md`.
