# Brief — design feedback templates for `multi step planning` and `repo scanning`

## Task (one deliverable)
Design the feedback templates for `multi step planning` and `repo scanning`. Print both, with 3–6 whys per field.

## Context (only what this task needs)
`multi step planning`: plan + gate (this method); check = script schema gate + checklist review.
`repo scanning`: parallel sectioning, read-only fan-out; check = coverage manifest; findings with paths. Its
deliverable IS a code graph — the tool is `code_graph/code_graph.py`.
Decision (2026-10-08): **Coverage is written per section, then reconciled by the join.** Each parallel section reports what IT read and what it skipped — only the section that read knows what it skipped — and the join merges those into one manifest. The join never re-derives a section's coverage. Do not block on this again.
Follow the settled rules: every field has one writer and the writer is the WORKER; Effort (tokens+rounds) is loop types only; types whose source is code carry the code-graph tool and `Source` names the graph; a verdict/agreement the human or verifier makes lives elsewhere, never in the worker's return. Print your answer to stdout — do not write any file.

## Template (fill this exactly)
```
## multi step planning
- <field>: <what it holds>
## repo scanning
- <field>: <what it holds>
## Whys
<3-6 levels per field>
```

## Example (one good result, short)
```
## repo scanning
- Coverage: <which nodes/edges were read, and which were NOT>
```

## Standard (how it is judged)
Both types have a field list; every field names its writer; whys present; `repo scanning` carries the graph.
