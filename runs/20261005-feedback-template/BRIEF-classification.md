# Improve this feedback template — and answer 3–6 whys

We are designing **per-task-type feedback templates**: the summary shape a worker reports back at the end of a task,
so a verifier reads a known shape instead of free text. One rule over all of them: **every field has a writer, and
the writer is the worker.** A human's verdict lives elsewhere. `Effort` (tokens + rounds) is loop types only.

The type, in plain words: **`classification`** is a routing node — the worker reads something and puts it into one
of a fixed set of buckets. The result is a label. Check: *schema-valid label + agreement on a labeled sample* (the
worker must agree with the human on a few pre-labeled examples).

A first, deliberately simple proposal:

```
## Summary
- Item:   <the thing classified, one line>
- Label:  <the label, from the allowed list>
- Agreed: <N of M labeled samples matched — the calibration>
```

**Improve or confirm it**, by the six whys: for each field you add or remove, answer 3–6 levels of "why" — until you
reach a fact, a value judgement, or something no one can answer. Keep it simple: this is a one-line-output type, so
a five-field template would be wrong even if every field could be defended.

## Rules

- Do not edit any file. Reply with your template and your whys, or write them to
  `runs/20261005-feedback-template/<your-engine>-classification.md`.
- Work blind — other engines answer the same brief; none of you sees another until afterwards.
- Be concise. Simpler is better here.
- Leave for the human what only the human decides.
