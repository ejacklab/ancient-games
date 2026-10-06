# Brief — n5-review (claude sonnet, code review)

## Task (one deliverable)
Review the tool against the spec, and run the generated cases against it. Print the checklist and findings to stdout. Do not write any file.

## Context (only what this task needs)
You get the tool, the spec, and the cases — never the builders' reasoning.
Concrete paths (decided 2026-10-05): the spec is the LATEST n2-design result — `runs/20261005-code-graph-tool/nodes/n2-design-4.result.md` (earlier attempts are superseded); the tool is `.claude/skills/workflow-design/scripts/code_graph.py`; the cases are the latest `n4-test-cases` result. Read the code and run the cases. Your job is a fixed checklist, not an open-ended hunt.

## Template (fill this exactly)
```
## Checklist
- [ ] every generated case passes, or is an explained failure — <answer, cite file:line>
- [ ] the tool's output matches the spec's schema — <answer>
- [ ] the coverage computation is honest (no self-grading) — <answer>
## Findings
<each finding, with file:line, or "clean pass">
```

## Example (one good result, short)
```
- [x] every case passes or is explained — 4 pass, 1 explained (lambda edge absent, spec says absent is ok)
```

## Standard (how it is judged)
Every checklist item is answered with a finding or a clean pass, and each finding cites file:line. An unanswered item is a failure. Review only — change nothing.
