# Brief — n2-design (claude opus, design)

## Task (one deliverable)
Turn the research digest into a buildable spec for `code_graph.py`. Print the spec to stdout. Do not write any file.

## Context (only what this task needs)
You get the research digest and the provisional decisions (location `.claude/skills/workflow-design/scripts/code_graph.py`, output JSON, coverage in scope, granularity functions + modules). Do not read the raw research. The tool must be **stdlib only** (no new dependency), parse with `ast`, and output a JSON object.
Coverage is **transitive** (decided 2026-10-05): a function is `tested` if any test reaches it directly or transitively through calls. `tested_by` holds the test ids.
Tests that run a script via `subprocess` (not by importing it) create no call edge, so those functions show as untested. **Accepted as a v1 blind spot** (decided 2026-10-05): document it under 'what it cannot see', and note a future `runs` edge kind (test -> module when the test's source names the script's path in a string literal).
From now on, do NOT block on a limitation: list it under 'what it cannot see' and proceed. Block (UNCLEAR:) only on a decision that changes the tool's interface.or transitively through calls. `tested_by` holds the test ids.

## Template (fill this exactly)
```
# Spec: code_graph.py
## Nodes
<what a node is, its fields>
## Edges
<what an edge is, its fields, direction>
## CLI
<usage line, the flags>
## Output
<the JSON schema>
## Coverage
<how coverage is computed — which nodes have a test>
```

## Example (one good result, short)
```
## Output
{"nodes": [{"id": "a.b", "kind": "function", "file": "x.py", "line": 12}],
 "edges": [{"from": "a", "to": "b", "kind": "call"}],
 "coverage": {"tested": 3, "total": 10}}
```

## Standard (how it is judged)
The spec names node types, edge types, the output schema, and the coverage query. Missing any of the four is a failure.
