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

Chosen (EJ, 2026-10-17): option 1 — "I prefer 1, extra step is ok". Applied as a working rule in the main agent's memory (print-keys-before-parsing).

## F-bdea5631 — a trailing `ls` in a test command line was logged as a failed test run

(Corrected after the workflow's own report: the first version of this section blamed the planned fail-first run; the
step's report shows the exit came from a trailing `ls`.)

Whys:
1. Why was a failure logged? A Bash call in crossed-build-check's fail-first step exited 2 at 09:52:55, and the guard recorded it as a failed `bun test` run.
2. Why exit 2? The command line ran the base tests and then `ls` on the temporary worktree to show it had been removed; `ls` exits 2 when the path is gone — the expected answer (the step's report: "a trailing `ls` that checked the worktree was gone; exit 2 there was the expected result").
3. Why was it read as a test failure? The guard's D1 sees a test runner (`bun test`) in the command and takes the call's exit as the test run's, though the exit came from a later command in the chain.
4. Why does D1 do that? It reads the whole call's exit; it attributes it to the test runner whenever one appears, without checking that the runner was the last command — the same family as F-969500fa (a test result hidden by a chain) and F-86553997 (the guard naming the wrong command of a chain).
Source: check — the guard's D1 test-run detection attributes a chain's final exit to a test runner that is not its last command.
Root cause: a failed call is labelled a failed test run because a test runner appears anywhere in its command, not because the runner produced the exit.
Options:
1. [check] D1 records a test failure only when the test runner is the call's last command, or when the runner's own summary in the output shows failures; otherwise the call is a command-error warning naming the last command word. evidence: this call's output summary showed "7 pass, 10 fail" for the planned run, and the exit 2 was the `ls`.
2. [rule] A planned red test run is its own Bash call, never chained with lookups; with `expect-fail --run` when it is planned (Round 12). evidence: `cli.ts` usage: "expect-fail --run COMMAND --out FILE … run a planned red run".
3. [tool] crossed-build-check's fail-first step runs the base tests through `expect-fail --run` and checks the worktree in a separate call. evidence: the step's report names both commands.
