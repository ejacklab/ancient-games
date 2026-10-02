# Result file — what every node writes back

One file per call, `runs/<id>/nodes/<node>-<attempt>.result.md`, written to a temp name and renamed, so a half-written
file is never read. A script (`.claude/skills/workflow-design/scripts/validate_result.py`) checks it; the COO reads
the capped summary and the path, never more. Method §3.8.

```
---
node: <node id>
attempt: <n>
engine: <codex | agy | qwen | claude-subagent | COO>
model: <the model as the tool reports it, not as requested>
status: ok | fail | partial
started: <UTC time>
ended: <UTC time>
evidence: <path to the proof: the command and its output, or file:line — never "it works">
---
<body: exactly the shape the brief's Template asked for. First line: the answer in one sentence.>
```

- `partial`: say in the body what is done and what remains, as a new small task the COO can dispatch.
- `fail`: say what was tried and the real error text, in the evidence file; the body stays short.
- Never put reasoning or narrative in the body; notes go in the evidence file.

## Example

```
---
node: n3
attempt: 1
engine: qwen
model: qwen3.8-flash
status: ok
started: 2026-10-02T10:00:00Z
ended: 2026-10-02T10:02:40Z
evidence: runs/20261002-x/nodes/n3-1.evidence.txt
---
Four lines print "unknown"; three are intentional.
| line | context | intentional | why |
|---|---|---|---|
| 243 | open_unknowns, subagent concurrency | yes | cannot be proved from outside |
```
