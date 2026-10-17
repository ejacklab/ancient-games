# Insight decisions — run 20261017-workflows

The owner's choice for each section of `insight.md`, recorded by the agent. One entry per section.

## F-3caba088 — I parsed a workflow's output file without checking its shape
- decision: option 1 (the agent's option) — before parsing a tool's output file, print its top-level keys, then write the parse
- owner's words: "I prefer 1, extra step is ok"
- date: 2026-10-17
- applied: a working rule in the main agent's memory (`print-keys-before-parsing`), commit c25fe29

## F-bdea5631 — a trailing `ls` in a test command line was logged as a failed test run
- decision: option 1 (the agent's option) — D1 records a test failure only when the test runner is the call's last command, or when the runner's own summary shows failures; otherwise the call is a command-error warning naming the last command word
- owner's words: "go with option 1"
- date: 2026-10-17
- applied: guard Round 17, commit 0cb4657; corrected after the crossed review, commits b6f361f and 49fe260 (run 20261017-round17-crossed)
