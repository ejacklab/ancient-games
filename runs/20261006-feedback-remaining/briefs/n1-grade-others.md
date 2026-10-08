# Brief — design feedback templates for `grade a run` and `others`

## Task (one deliverable)
Design the feedback templates for `grade a run` and `others`. Print both, with a 3–6 whys for each field.

## Context (only what this task needs)
`grade a run`: single node, fixed rubric; check = rubric verdicts kept separate per dimension; run-directory
evidence only; missing proof = INVALID_RUN.
`others`: no default — the full method from first principles; check = — (none).
Two decisions, already made (2026-10-08): **INVALID_RUN is a whole-run verdict** — each dimension's verdict stays separate, but if any dimension lacks its run-directory proof, the run-level result is INVALID_RUN. And **`others` fields are conditional**: Effort appears only when the design is a loop, Source only when there is a source; otherwise a minimal skeleton (what was done, evidence, findings). Do not block on these again.
Follow the settled rules: every field has one writer and the writer is the WORKER; Effort (tokens+rounds) is loop types only; types whose source is code carry the code-graph tool and `Source` names the graph; a verdict/agreement the human or verifier makes lives elsewhere, never in the worker's return. Print your answer to stdout — do not write any file.

## Template (fill this exactly)
```
## grade a run
- <field>: <what it holds>
## others
- <field>: <what it holds>
## Whys
<3-6 levels per field you added, removed or kept>
```

## Example (one good result, short)
```
## grade a run
- Rubric: <verdict per dimension, kept separate>
```

## Standard (how it is judged)
Both types have a field list; every field names its writer (the worker); the whys are present. A field a human
fills later is a failure.
