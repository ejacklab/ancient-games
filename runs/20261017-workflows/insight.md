# Insight — run 20261017-workflows

## F-3caba088 — I parsed a workflow's output file without checking its shape

Whys:
1. Why was a failure logged? My one-off Python read of the workflow's output file failed with `KeyError: 'built'`.
2. Why? I assumed the output file held the workflow's return value at its top level; it is the task's own record, whose shape I had not looked at.
3. Why assume? The notification printed the return value, so I took the file to hold the same thing, and wrote the parse before inspecting it.
4. Why did the notification not point me right? It did: its diagnostics say to read the run's `journal.jsonl` for each agent's full return value — I read past that line.
Source: instruction — the main agent's habit of parsing a file by an assumed structure instead of printing its keys first.
Root cause: a parse written against an assumed shape, when the tool named the file that holds the data.
Options:
1. [rule] Before parsing a tool's output file, print its top-level keys (one command), then write the parse. evidence: the second try did that and worked in one step.
2. [rule] For a finished workflow, read `<transcript>/journal.jsonl` as its diagnostics say, never the task output file. evidence: the notification's diagnostics line names journal.jsonl.
