You are answering ten questions about the opencode repository, module packages/core/src/session. Your working directory is the repository root (/home/smoke01/dev/ancient-games/runs/20261014-opencode-code-map/src/opencode), at commit 6dc4d4e. Do not change any file.

Use the code-map tool first. It answers one question per command from the code's types:

    bun /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p4/tool-a5-src/cli.ts <where|find|callers|callees|chain|tests|map> <query> --project packages/core/tsconfig.json --root packages/core --tests 'test/**'

<query> is a name (for example `Permission.assert`), a place `file:line` relative to --root, or a description for `find`. Add `--json` for JSON. Every answer carries its evidence (file:line) and its limits. You may also read and grep files when the tool's answer is not enough, or to check it.

For each question, give the answer in a few lines, each claim with its file:line (paths relative to the repository root). Say plainly what you could not establish. Put all ten answers in your final message, headed Q1 to Q10.

The questions:

Q1 (where defined). Where is the SessionRunner service defined, and where is its `drain` implemented?
Q2 (where defined). Where is the maximum-steps prompt defined, and where is it applied?
Q3 (what calls X, through injected services). What calls `SessionRunner.drain`?
Q4 (what calls X). What calls `SessionStep.attempt`?
Q5 (what X calls). What does `SessionStep.attempt` call?
Q6 (call chain, down, three or more levels). From SessionExecution down to a tool's own execute function
Q7 (call chain, up, three or more levels). From `SessionRunnerRetry.policy` up to the session runner
Q8 (which tests reach X). Which tests reach `SessionRunnerRetry.policy`?
Q9 (steps and decisions of one flow). How does `SessionStep.attempt` decide its outcome after the stream ends?
Q10 (difference between siblings). How do the Retry and Continue step outcomes differ?
