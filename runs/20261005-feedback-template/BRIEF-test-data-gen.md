# Improve this feedback template — and answer 3–6 whys

We are designing **per-task-type feedback templates**: the summary shape a worker reports back at the end of a task,
so a verifier reads a known shape instead of free text.

The one rule over all of them (decided with the author, 2026-10-05): **every field has a writer, and the writer is
the worker.** A return template is the worker's output; a human's verdict, a design's decision, a COO's call — those
live elsewhere, not in the worker's summary.

`Effort` (tokens + rounds) goes on every **loop** type. Five types are drafted so far:

| type | loop? | template |
|---|---|---|
| `code generation` | yes | `Changed / Why / Proof / Effort` |
| `test script gen` | yes | `Created / Run / Effort` |
| `test cases gen` | no | `Created / Type / Coverage / Location` |
| `ui/ux dev` | yes | `Changed / Look / Why / Effort` |
| `debugging` | yes | `Bug / Fixed / Test / Effort` |

## The task

The current proposal for **`test data gen`** (single node, schema-validated; check = *schema validation + edge-case
coverage list*) is:

```
## Summary
- Created:   <the data / fixtures, one line each>
- Validated: <schema validation passed>
- Coverage:  <the edge cases covered>
```

**Improve or confirm it**, by the six whys: for each field you add or remove, answer 3–6 levels of "why" — until you
reach a fact, a value judgement, or something no one can answer.

Open question to settle if you can: **does the data need a `Location` line** (where the fixture files live), or is
that redundant because the result file already carries the evidence path?

## Rules

- Do not edit any file. Reply with your template and your whys, or write them to
  `runs/20261005-feedback-template/<your-engine>-test-data.md`.
- Work blind — other engines answer the same brief and none of you sees another until afterwards.
- Be concise. Three fields with honest whys beat five fields with none.
- Leave for the human what only the human decides; say so rather than inventing it.
