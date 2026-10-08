# Brief — merge the three proposals into the settled record

## Task (one deliverable)
Read the three proposals (n1, n2, n3 result files) and merge them into `docs/FEEDBACK_TEMPLATES.md`, adding the five
remaining types. Print a summary of what you added and any rule-break you had to flag.

## Context (only what this task needs)
The three proposals are the latest result files in `runs/20261006-feedback-remaining/nodes/`. The settled rules:
every field has one writer (the worker); Effort is loop types only; code-graph where source is code. The 11 settled
templates are already in `docs/FEEDBACK_TEMPLATES.md` — do not change them. The file's table and each type's section
are the shape.

## Template (fill this exactly)
```
## Added
<each type, its fields>
## Flags
<anything that breaks the rules, or "none">
```

## Example (one good result, short)
```
## Added
grade a run: Rubric / Evidence
## Flags
none
```

## Standard (how it is judged)
All five types are present in the doc with field lists; the 11 settled ones are unchanged; any rule-break is named
rather than silently fixed.
