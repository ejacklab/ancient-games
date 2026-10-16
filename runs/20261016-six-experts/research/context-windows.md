# Research — engine context windows and prices (researcher subagent, claude-opus-5-5, 2026-10-16; returned as text, saved by the COO)

Digest: every engine holds the current ≈25k-token insight file easily. All list a window of about 1M tokens, except
gpt-6.1-sol, whose input caps at 922,000 (R6, R11, R12, R13, R15). Claude 5.5 needs no beta header for 1M; Opus and
Sonnet charge the same rate across the whole window; Haiku 5.5 charges 5x on prompts over 100k (R2, R3). Approximate
input cost of one 25k-token call (researcher's arithmetic, not measured): Opus $0.10, Sonnet $0.05, gpt-6.1-sol $0.05,
Gemini 3.8 Flash $0.019, Haiku $0.0025, deepseek-flash $0.0075 at peak. Caution: Anthropic states accuracy degrades as
context grows (R5); a 1M-token file in a 1M window leaves no room for output. Quotes came through the fetch tool's
summariser. Gaps: MiniMax M3.1 price; Gemini 3.1 Pro window; long-context quality statements from Google, DeepSeek,
OpenAI.

| id | model | context window | 1M? (condition) | price in/out per M | long-context note | label | URL | quote |
|---|---|---|---|---|---|---|---|---|
| R1 | Claude Opus 5.5 / Sonnet 5.5 / Haiku 5.5 | 1M each; max output 128K | yes | Opus $4/$20; Sonnet $2/$10; Haiku from $0.10/$0.50 | cache reads 5% of input (Opus, Sonnet) | verified | https://platform.claude.com/docs/en/about-claude/models/overview | "Context window ... 1M tokens"; "$4 / input MTok, $20 / output MTok" |
| R2 | Claude 5.5 | 1M | yes, no beta header; standard price except Haiku | — | — | verified | https://platform.claude.com/docs/en/build-with-claude/context-windows | "1M is the default: you don't need a beta header … except on Claude Haiku 5.5, where prompts over 100,000 tokens cost more." |
| R3 | Claude Haiku 5.5 | 1M | price step above 100k | ≤100k $0.10/$0.50; >100k $0.50/$2.50 | whole request at the higher price | verified | https://platform.claude.com/docs/en/about-claude/pricing | "Claude Haiku 5.5 (for prompts over 100,000 tokens) \| $0.50 / MTok ... \| $2.50 / MTok" |
| R4 | Claude Opus 5.5 / Sonnet 5.5 | 1M | same rate across the window | Opus $4/$20 (cache hit $0.20); Sonnet $2/$10 (cache hit $0.10); Batch half | no step above 200k | verified | same | "A 900k-token request is billed at the same per-token rate as a 9k-token request." |
| R5 | Claude (all) | — | — | — | quality degrades with length | verified | context-windows page | "As token count grows, accuracy and recall degrade, a phenomenon known as context rot." |
| R6 | gemini-3.8-flash | input 1,048,576; output 65,536 | yes | — | none on the page | verified | https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash | "Input token limit" "1,048,576" |
| R7 | Gemini 3.8 Flash | — | — | $0.75/$3.75 to 2026-12-31; $1.50/$7.50 from 2027-01-01 | no size step | verified | https://ai.google.dev/gemini-api/docs/pricing | "$0.75 through December 31, 2026." |
| R8 | Gemini 3.1 Pro Preview | not found | not found | $2/$12 (≤200k); $4/$18 (>200k) | step at 200k | verified (price) | same | "$2.00, prompts <= 200k tokens" |
| R9 | deepseek-flash (V4.1-Flash) | 1M; max output 384K | yes | cache-miss input $0.15 off-peak / $0.30 peak; output $0.60/$1.20; cache hit $0.003/$0.006 | no step shown | verified | https://api-docs.deepseek.com/quick_start/pricing | "CONTEXT LENGTH: 1M" |
| R10 | DeepSeek off-peak | — | — | half price off-peak | — | verified | same | "Off-peak rates are half of the peak rates." |
| R11 | MiniMax-M3.1-Flash-Preview | 1M | yes | not found | only via M Plan / MiniMax Code | verified | https://platform.minimax.io/docs/guides/models-intro | "Frontier multimodal coding model with 1M context window" |
| R12 | MiniMax-M3.1-Flash-Preview | up to 1M | MiniMax suggests 512K | — | similar quality at 512K and 1M, ~20% cheaper at 512K (MiniMax's own test) | verified (statement) | https://platform.minimax.io/docs/m-plan/codex | "average model performance was similar with 512K and 1M context windows" |
| R13 | MiniMax-M3 (earlier) | not stated | — | $0.30/$1.20 (≤512k); $0.60/$2.40 (>512k) | step at 512k | verified (M3 only) | https://platform.minimax.io/docs/guides/pricing | tiers as relayed |
| R14 | MiniMax M3.1 price | — | — | aggregators show $0.00 placeholders | — | unproven | opencode.ai (not fetched) | do not use |
| R15 | gpt-6.1-sol | window 1,050,000; max input 922,000; max output 128,000 | no: input caps at 922k | $2/$10 | above 272K input: 2x input/cache, 1.5x output | verified | https://developers.openai.com/api/docs/models/gpt-6.1-sol | "Maximum input tokens: 922,000" |
| R16 | gpt-6.1-sol in Codex | 500,000 default (raised 2026-10-11) | — | — | — | unproven | cryptobriefing.com (not fetched) | — |

Which can hold a 1M-token insight file (researcher's reading): Gemini 3.8 Flash comes closest (input 1,048,576);
Claude 5.5 has a 1M window but output counts inside it; DeepSeek and MiniMax list "1M" (whether output is inside it:
not found); gpt-6.1-sol cannot (922k input). Which hold today's 25k easily: all.
