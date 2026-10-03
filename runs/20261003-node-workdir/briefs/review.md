# Brief — verifier, phase 2: review the dev's change

Read `runs/20261003-node-workdir/diff.patch` (the dev's change) and `runs/20261003-node-workdir/state.md`
(criteria R1–R7). Your acceptance cases are already fixed and run by a script; this is the code review only. Read
those two files; do not change anything.

## Task (one deliverable)
A review of the diff against the criteria, the "must not change" list in state.md, and the code's own conventions.

## Template
Your body: a table `| id | where (file:line in the new code) | finding | kind |`, kind one of `bug`, `scope`,
`criterion` (a criterion not met), `risk`; or the single line `No findings.` Then one line `Verdict: accept` or
`Verdict: changes needed`.

## Example
```
| id | where | finding | kind |
|---|---|---|---|
| F1 | dispatch.py:212 | the fallback ignores its own workdir (R6) | criterion |
Verdict: changes needed
```

## Standard
Every finding cites a line of the diff and says what is wrong in one sentence; no style preferences; a finding outside
R1–R7 and the must-not list is `risk`, not `criterion`.
