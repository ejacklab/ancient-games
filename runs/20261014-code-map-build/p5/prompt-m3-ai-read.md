You are answering ten questions about the opencode repository, module packages/ai. Your working directory is the repository root (/home/smoke01/dev/ancient-games/runs/20261014-opencode-code-map/src/opencode), at commit 6dc4d4e. Do not change any file.

Use reading and searching only (Read, Grep, Glob). No other tools.

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
