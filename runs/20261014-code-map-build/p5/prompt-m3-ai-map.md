You are answering ten questions about the opencode repository, module packages/ai. Your working directory is the repository root (/home/smoke01/dev/ancient-games/runs/20261014-opencode-code-map/src/opencode), at commit 6dc4d4e. Do not change any file.

Use the code-map tool first. It answers one question per command from the code's types:

    bun /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p4/tool-a5-src/cli.ts <where|find|callers|callees|chain|tests|map> <query> --project packages/ai/tsconfig.json --root packages/ai --tests 'test/**'

<query> is a name (for example `Permission.assert`), a place `file:line` relative to --root, or a description for `find`. Add `--json` for JSON. Every answer carries its evidence (file:line) and its limits. You may also read and grep files when the tool's answer is not enough, or to check it.

For each question, give the answer in a few lines, each claim with its file:line (paths relative to the repository root). Say plainly what you could not establish. Put all ten answers in your final message, headed Q1 to Q10.

The questions:

Q1 (where defined). Where is the LLMClient service defined, and where is its live layer?
Q2 (where defined). Where are the Anthropic provider's ID, default base URL and API-key auth defined?
Q3 (what calls X, through injected services). What uses the LLMClient service?
Q4 (what calls X). What calls `prepareRequest` in route/client.ts?
Q5 (what X calls). What does `prepareRequest` call?
Q6 (call chain, down, three or more levels). From the LLMClient layer's `stream` down to protocol parsing
Q7 (call chain, up, three or more levels). From `requireTerminalEvent` up to the session step
Q8 (which tests reach X). Which tests reach the request compiler (`compileRequest`)?
Q9 (steps and decisions of one flow). How does `generateObject` produce a typed object?
Q10 (difference between siblings). How do the Anthropic and OpenAI providers differ in routes and auth?
