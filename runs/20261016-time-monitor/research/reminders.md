# Research — when to tell an agent its remaining time (researcher subagent, Claude Opus 5.5, 2026-10-16; returned as text, saved by the COO)

Digest: three independent sources found that showing the remaining budget changes behaviour — BATS (per-step budget
display: Gemini-2.5-Pro at budget 10 matched ReAct at 100), a negotiation study (a remaining-time update every turn
raised GPT-5.1 deal closure from 4% to 32%), "On the Clock" (a budget stated only in the prompt failed; harness timing
feedback improved adherence). s1: a token budget in the prompt alone gave 40% control vs 100% with external forcing.
Anthropic's context awareness and task budgets update after each tool call / continuously. No source compares
fixed-fraction marks or end-only notices with per-step updates (not measured).

| id | finding | label | URL | quote |
|---|---|---|---|---|
| F1 | BATS Budget Tracker adds a budget block after every tool response, not at thresholds | verified | https://arxiv.org/html/2511.17006v1 | "At each subsequent iteration" … "immediately after each tool response" |
| F2 | With the tracker, Gemini-2.5-Pro at budget 10 reached 12.8% vs ReAct 12.6% at budget 100, 40.4% fewer search calls, 31.3% lower cost | verified | same | "the standard ReAct baseline saturates at a budget of 100" |
| F2b | Appendix prompt strategy tiers by remaining budget (HIGH ≥70% … CRITICAL <10%) — how to act, not when to show | reported | same | "HIGH Budget (>=70% remaining)" |
| F3 | Anthropic context awareness: total in the system prompt, an update after each tool call | verified | https://platform.claude.com/docs/en/build-with-claude/context-windows | "After each tool call, the API gives Claude an update on its remaining capacity" |
| F4 | Anthropic task budgets (beta): a continuously updated countdown the model uses to pace itself; too small a budget causes refusal or early stop | verified (vendor claim) | https://platform.claude.com/docs/en/build-with-claude/task-budgets | "it may decline to attempt the task at all, scope it down aggressively, or stop early" |
| F5 | s1: prompt-stated token budget 40% control vs 100% with budget forcing | verified | https://arxiv.org/html/2501.19393 | "our model cannot reliably count tokens" |
| F6 | Negotiation agents: per-turn remaining-time update vs limit given once: closure 32% vs 4% (GPT-5.1) | verified | https://arxiv.org/html/2601.13206v1 | "LLMs struggle to internally track elapsed time" |
| F7 | That study's only other condition: a qualitative urgency note every turn; no fraction-based or end-only condition | verified (tool's reading) | same | "(Deadline approaching--act with urgency.)" |
| F8 | "On the Clock": budget in the prompt alone fails; timing feedback improves adherence | verified (abstract) | https://neurips.cc/virtual/2026/170689 | "substantially improves budget adherence" |

Reminder marks at 50/80/100% only: not addressed — per-step updates are supported (F1–F4, F6), a once-only budget fails
(F5, F6, F8). All quotes came through the fetch tool's model, not raw page text.
