# Run 20261012-index-md-algorithm — state

**Asked by EJ, 2026-10-12:** *"prepare a workflow prompt for research and discuss, fork your subagents, codex,
opencode and agy to research about this INDEX.md algrithm, all put 1 research lit review report at a folder, then
when everyone don research, all of them reac all the lit review and gen a report with single algo proposal, and 3
supporting reasons and 6 must not do, and you review all of the report and give a sum"*

**Why:** review finding 5 on `docs/memory-system/SOURCE_OF_TRUTH.md` — every branch regenerates the one shared
`INDEX.md`, so parallel branches conflict on it; and K6 leaves open which tool generates it and what runs it.

## Shape (EJ's)

1. Stage 1, parallel, blind: claude (Claude Code subagent), codex, opencode, agy each write one literature review →
   `lit-review/<engine>.md`. Brief: `briefs/1-lit-review.md`. Finding prefixes: C, X, O, A.
2. Stage 2, parallel, after all four exist: each reads all four reviews and writes one proposal (one algorithm,
   3 reasons, 6 must-nots) → `proposals/<engine>.md`. Brief: `briefs/2-proposal.md`.
3. The COO reviews the four proposals and writes `summary.md` for EJ.

## Engines

- claude: Claude Code general-purpose subagent, fresh context (not a fork: a fork would carry the COO's own
  recommendation from the session and would not be blind).
- codex: `gpt-6.1-sol`, effort high, `--sandbox read-only`.
- opencode: `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`, `--agent plan`.
- agy: `gemini-3.1-pro-high`, `--mode plan`; no shell (headless denies it, seen in run 20261012-caches-merge).

Exact command lines: `run.sh`. Prompts are given as "read <brief> and do what it says".

## Log
- 2026-10-12T14:36:56Z STAGE 1 done: codex exit=0 22247B; opencode exit=0 36716B; agy exit=0 0B; 
- 2026-10-12T14:41:21Z STAGE 1 claude (subagent) done: 36006B, 58 findings (C1–C58). agy empty: headless auto-denied read_url; allow-rule attempt (bare names) did not match; read_url(*) edit blocked by Claude Code auto-mode; waiting on EJ.
- 2026-10-12T14:41:36Z EJ: "ok stop the agy one". agy dropped from both stages; stage 2 runs claude, codex, opencode. agy settings.json restored from backup (my allow-rule edit undone).
- 2026-10-12T14:45:53Z STAGE 2 done: codex exit=0 14361B; opencode exit=0 16024B; 
- 2026-10-12T14:47:15Z STAGE 2 claude (subagent) done: proposals/claude.md 17706B. COO summary written: summary.md.
- 2026-10-12T14:50:56Z EJ: "try to ask codex, agy and opencode to review the claude's version algorithm". Stage 3: three blind reviews of proposals/claude.md, brief briefs/3-review.md, out reviews/<engine>.md. agy back in for this stage: local files only, no web needed.
- 2026-10-12T14:58:32Z STAGE 3 done: codex exit=0 14360B; opencode exit=0 16679B; agy exit=0 14097B; 
- 2026-10-12T14:59:27Z STAGE 3 read: all three ACCEPT WITH FIXES; COO summary reviews/summary.md.
- 2026-10-12T15:06:36Z EJ asked for the design, vision and requirements in a folder for a separate build session. Written: docs/index-md/{VISION,REQUIREMENTS,DESIGN}.md (drafts; requirements review continues in this session).
