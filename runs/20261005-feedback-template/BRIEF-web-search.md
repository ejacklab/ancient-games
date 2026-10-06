# Improve this feedback template — and answer 3–6 whys

We are designing **per-task-type feedback templates**: the summary shape a worker reports back at the end of a task,
so a verifier reads a known shape instead of free text.

The one rule over all of them (decided with the author, 2026-10-05/06): **every field has a writer, and the writer is
the worker.** A human's verdict lives elsewhere. `Effort` (tokens + rounds) goes on loop types only.

Eight types are decided; the current proposal for **`web search`** (single node, voting on contested facts; check =
*dated sources with URLs; claims traceable*) is:

```
## Summary
- Found:    <the answer/facts, one line each>
- Sources:  <dated source + URL for each claim — traceable>
- Disputed: <contested facts and the split — the voting>
```

**Improve or confirm it**, by the six whys: for each field you add or remove, answer 3–6 levels of "why" — until you
reach a fact, a value judgement, or something no one can answer.

## Rules

- Do not edit any file. Reply with your template and your whys, or write them to
  `runs/20261005-feedback-template/<your-engine>-web-search.md`.
- Work blind — other engines answer the same brief; none of you sees another until afterwards.
- Be concise. Three fields with honest whys beat five fields with none.
- Leave for the human what only the human decides; say so rather than inventing it.
