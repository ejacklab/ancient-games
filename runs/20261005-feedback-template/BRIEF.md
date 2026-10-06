# Improve this feedback template — and answer 3–6 whys

We are designing **per-task-type feedback templates**: the summary shape a worker reports back at the end of a task,
so a verifier reads a known shape instead of free text. The design rule is *default-first* — the table carries the
default, and the LLM may propose a better one from the actual prompt.

Four types are drafted so far:

| type | template |
|---|---|
| `code generation` (loop) | `Changed / Why / Proof / Effort` |
| `test script gen` (loop) | `Created / Run / Effort` |
| `test cases gen` | `Created / Type / Coverage / Location` |
| `ui/ux dev` (loop + human checkpoint) | `Changed / Why / Proof / Accepted / Effort` |

The field names are the summary section headings; a worker fills each with one line.

## The task

Improve the **`ui/ux dev`** template — but do it by the method's own tool, the **six whys**. For each field you
propose (or remove), answer **3 to 6 levels of "why"**:

- why does this field exist?
- why that, and not the alternative?
- why does the difference matter?
- …until you reach either a fact, a value judgement, or something no one can answer.

Then give your improved template.

## Rules

- Do not edit any file. Reply with your template and your whys, or write them to
  `runs/20261005-feedback-template/<your-engine>.md`.
- Work blind — another engine answers the same brief and neither of you sees the other until afterwards.
- Be concise. A 3-line template with honest whys beats a 10-line template with none.
- Where you would leave a field for the human to decide, say so rather than inventing it.
