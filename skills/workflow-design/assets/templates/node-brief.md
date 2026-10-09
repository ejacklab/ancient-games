# Node brief — what the COO hands a worker

The COO is the stronger model; the worker is a tool, often a cheaper one. The brief is where the COO's skill goes
in: it gives the worker the **template** to fill, a worked **example**, and the **standard** the result will be
judged by, so a small model needs no guesswork and the COO never rewrites a result. One task per brief. Method:
`docs/WORKFLOW_DESIGN_METHOD.md` §3.8 and `docs/EXECUTOR_KINDS.md`, the COO.

Fill every part. A part that cannot be filled is an unclear spot, not a blank.

```
# Brief — <node id>, attempt <n>

## Task (one deliverable)
<what to produce, in one or two sentences; what it is for; what it is not>

## Context (only what this task needs)
<paths to read, with the lines or ids that matter; facts the worker must not re-derive; what is withheld on purpose>

## Template (fill this exactly)
<path to the result template, usually docs/workflow-templates/result-file.md, or research-file.md for research;
the body shape if it is not the default: headings, fields, order>

## Example (one good result, small and real)
<a short filled-in example of the same task kind, or of a smaller instance of this one. Show the shape and the
level of detail; say which parts to copy and which are only illustrative>

## Standard (how it will be judged)
<the check, as the worker can run it: the command and the result that counts as pass; what a failing result looks
like; the sabotage the check is known to catch. For a judged check: the fixed checklist, item by item>

## Limits
<may change: paths. must not change: paths or things. timers: inner <tool limit>, outer <timeout>. attempts left: n>

## Write the result to
<runs/<id>/nodes/<node>-<attempt>.result.md — written to a temp name, then renamed. Full detail and proof go in the
evidence file named in the header; return only what the template asks for.>
```

## Example (a filled brief, shortened)

```
# Brief — n3, attempt 1

## Task (one deliverable)
List every place readiness.py prints the word "unknown" and say which ones are intentional. Not a fix.

## Context
.claude/skills/workflow-design/scripts/readiness.py only. Do not read the tests.

## Template
docs/workflow-templates/result-file.md; body = a table: line number | context | intentional (yes/no) | why.

## Example
| 243 | open_unknowns, subagent concurrency | yes | cannot be proved from outside |

## Standard
Pass: every line from `grep -n unknown readiness.py` appears in the table once; no line invented.
Run that grep and compare counts. Fail looks like: a row whose line number has no "unknown" in it.

## Limits
may change: runs/20261002-x/nodes/ only. must not change: everything else. timers: outer 300 s. attempts left: 2

## Write the result to
runs/20261002-x/nodes/n3-1.result.md
```
