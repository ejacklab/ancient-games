# Brief — dispatcher canary

Do not use any tools. Do not read or write any file. Answer from this prompt alone.

## Task (one deliverable)
Return the canary result: a result file whose body is exactly the line `CANARY OK`.

## Context
None needed. This checks that the dispatcher can start you, read your final answer and validate it.

## Template
The pass-back header (given below by the dispatcher), then a body of one line.

## Example
```
---
node: example
attempt: 1
engine: codex
model: gpt-6.1-sol
status: ok
started: 2026-10-03T00:00:00Z
ended: 2026-10-03T00:00:05Z
evidence: none
---
CANARY OK
```

## Standard
Pass: the header has every key with your real node, attempt, engine and model, `status: ok`, `evidence: none`, and
the body is exactly `CANARY OK`. Your final answer is only the result file, with no text before or after it.

## Limits
No tools, no files. Answer within one minute.
