# Improve this feedback template — and answer 3–6 whys

We are designing **per-task-type feedback templates**: the summary a worker reports back at the end of a task.
One rule over all: every field has a writer, and the writer is the worker. Effort (tokens + rounds) is loop types
only.

The type: **`code review`** — maker–checker, fresh blind session. Check: *fixed checklist; findings with file:line*.
Sabotage: *plant a known defect → the reviewer must find it*.

The author's requirements, in their words, mapped to a draft:

| author's words | field |
|---|---|
| "review based on what" (twice — it matters most) | Basis |
| "how the code is review" | Method |
| "why use that review ways" | Why |
| "what is the review results" | Findings |
| "where the report put at" | Report |

```
## Summary
- Basis:    <what it reviewed against — the spec / requirements / diff>
- Method:   <how it was reviewed, and why that way>
- Findings: <what was found — each with file:line>
- Report:   <where the full report lives>
```

**Agree or improve**, by the six whys. In particular judge: is `Method` + `Why` one field or two (the author asked
for both "how" and "why"); and is `Report` (the path) redundant with the pass-back `evidence:` line that already
points at a file?

Rules: blind, concise, no file edits (reply or write to
`runs/20261005-feedback-template/<your-engine>-code-review.md`), leave the human's calls to the human.
