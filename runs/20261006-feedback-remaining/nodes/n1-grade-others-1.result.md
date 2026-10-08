---
node: n1-grade-others
attempt: 1
engine: claude
model: claude-opus-5-5
status: ok
started: 2026-10-08T00:57:32.623Z
ended: 2026-10-08T00:59:01.620Z
evidence: none
---

## grade a run
- Run (worker): <the run directory it graded, `runs/<run-id>/`, copied from the brief>
- Against (worker): <the rubric's id or path, and its version, copied from the brief and not re-derived>
- Rubric (worker): <one line per rubric dimension: `<dimension> — PASS | FAIL | INVALID_RUN — <proof: path:line inside the run directory>`, or for INVALID_RUN `looked for <what> at <path>: absent`. No total, no overall score. An empty run directory gives INVALID_RUN on every line, never PASS.>
- Unclear (worker): <each dimension whose wording could not be applied as written, and the reading used; or "none">

## others
- Delivered (worker): <each deliverable, one line: what it is and where it is (a path, or "inline below")>
- Checked (worker): <the check the worker ran, re-runnable, and what it showed; or "none ran — unchecked">
- Unclear (worker): <each point the brief left open, and the reading used; or "none">
- Effort (worker): <tokens + rounds>. Only when the brief runs this node as a loop.
- Source (worker): <the code graph used>. Only when the task's source is code.

The brief may add task-specific fields on top of these. A replacement template the worker proposes must cover at least these (the default-first rule).

UNCLEAR: Is INVALID_RUN a verdict for one dimension or for the whole run? TASK_TYPES says "missing proof = UNKNOWN/INVALID_RUN" and the brief says only INVALID_RUN. / Best guess: one value set, `PASS | FAIL | INVALID_RUN`. A dimension with no proof gets INVALID_RUN. An empty run gets INVALID_RUN on every line. UNKNOWN is dropped.
UNCLEAR: `others` has "loop? —". Should Effort and Source be conditional fields, or left out entirely? / Best guess: conditional, as written above. The settled rules attach them to what the node is, not to its category.

## Whys

**grade a run / Run (kept)**
1. Why name the run? The verifier must know which directory the verdicts are about.
2. Why not rely on the proof paths? An empty run has no proof paths, and that is the sabotage case.
3. Why does that matter? Without Run, "INVALID_RUN on an empty directory" and "graded the wrong directory" look the same.
4. Why copy it from the brief? This is the classification `T` lesson: the worker repeats the input it was given and does not re-derive it, so a mismatch shows.

**grade a run / Against (kept)**
1. Why name the rubric? A verdict counts only against a standard. This is the same reason code review has `Against`.
2. Why the version? A rubric that changes between runs makes two PASS results incomparable.
3. Why does the worker write it? Only the worker knows which rubric it actually applied.
4. Why separate from Run? "One thing": the run and the rubric are two facts and can each be wrong on their own.

**grade a run / Rubric (kept, from the example)**
1. Why one line per dimension? The type's check is "verdicts kept separate per dimension".
2. Why no total? A total lets one FAIL hide under three PASS results.
3. Why does the proof go on the same line as the verdict? This is the web-search lesson, a claim paired with its source. A separate evidence list loses track of which proof backs which verdict.
4. Why must the proof be inside the run directory? Evidence from the run directory only. A cited path outside it is a check that fails on sight.
5. Why spell out INVALID_RUN with "looked for X at Y"? If missing proof is left blank, it reads as PASS. Written out, it can fail.
6. Can it fail? Yes: a dimension missing from the list, a PASS with no path, or a path outside `runs/<run-id>/`.

**grade a run / Unclear (kept)**
1. Why? A fixed rubric can still have a dimension that does not fit this run.
2. Why not just grade it anyway? A silent reading becomes a hidden verdict on the rubric itself.
3. Why here? `code review` already settled `Unclear` as the home for the `UNCLEAR:` escape (conventions).

**grade a run / removed: Overall verdict, Accepted, agreement**
1. Why remove them? Whether to accept the grade is the human's or verifier's decision.
2. Why not record it in the return? The worker writes before anyone looks, so the rule is broken (one writer, the worker).
3. Where does it go? To the loop's exit and the state file.

**grade a run / removed: Effort, Source**
1. Why no Effort? `grade a run` has loop = no, and Effort is for loop types only.
2. Why no Source or code graph? Its source is a run directory, not code.
3. Why not add them anyway? An unfilled field becomes a blank that looks like data.

**others / Delivered (kept)**
1. Why? Every task returns something, and the reader must find it.
2. Why not `Changed` or `Created`? Those words already have fixed meanings (files touched, tests made), and an `others` task may be neither.
3. Why "where it is"? The pass-back `evidence:` points to proof, not to the deliverable. They can be different files.

**others / Checked (kept)**
1. Why? The type's check is "—": no verifier is defined.
2. Why does that make the worker's own check matter? It is the only check there is.
3. Why "none ran — unchecked" written out? Fail Loud: silence would be read as checked.
4. Why re-runnable? A later reader can then turn the worker's claim into a verified one.

**others / Unclear (kept)**
1. Why? `others` is the least-defined type, so it has the most open points.
2. Why record the reading used? Whoever reviews it can see which guess the work rests on.
3. Why the same name as in code review? It is shared vocabulary, so the merger does not need a new word.

**others / Effort and Source (conditional)**
1. Why conditional? `others` has no fixed pattern. The method may make it a loop or a single node, and its source may or may not be code.
2. Why not always? Effort is for loops only. Source + graph is only for when the source is code.
3. Why not never? That would drop a settled rule just because the category name is vague.
4. Who decides? The brief states the shape. The worker fills the field only when the brief's shape calls for it (see the UNCLEAR line above).

**others / removed: Closest type**
1. Why was it considered? It would help add new `TASK_TYPES` rows.
2. Why removed? It serves the ledger, not the reader of this return. It is a different artifact ("who is this for").
3. Where does it go? The designer records it in `TASK_TYPES_LEDGER.md`.
