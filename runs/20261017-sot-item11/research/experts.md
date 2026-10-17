# Research: start-file limits by agent (for question E, and C/D)

Research step of the experts-decide workflow, 2026-10-17. Question: *"For each of these AI coding agents, what is the
documented limit on the instruction or memory files loaded automatically at session start …? Give the official source
for each, and say where sources conflict."*

**Labels.** *verified* = I opened the source in this step and it says so (URL or local path given). *reported* = a
source says it and I could not confirm it. Web pages were read through WebFetch, whose quotes are model-made extracts,
not byte-checked; the two local checks (dsh, Qwen Code) are byte-exact greps of the installed packages.

Installed versions on this machine (`--version`, 2026-10-17): Claude Code 2.1.302, codex-cli 0.160.0, agy 1.4.0,
opencode 1.18.34, Qwen Code 0.21.8 (package.json), dsh 0.2.0-rc.2 (package.json). The docs pages carry no version, so
whether each page describes the installed version is **not measured**.

## Findings

| Agent | File(s) loaded at start | Documented limit | Over the limit | Label |
|---|---|---|---|---|
| Claude Code — auto memory | `MEMORY.md` | "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation." | "Content beyond that threshold is not loaded at session start"; a write over the limit succeeds but returns an error telling Claude to rewrite the index | verified — https://code.claude.com/docs/en/memory |
| Claude Code — instructions | `CLAUDE.md` (and its `@imports`) | "This limit applies only to `MEMORY.md`. Claude Code loads a CLAUDE.md file of up to 4 MiB in full and skips a larger file." Advice, not a limit: "target under 200 lines per CLAUDE.md file" | file over 4 MiB is skipped | verified — same page |
| OpenAI Codex CLI | `AGENTS.md` chain (global + root-to-cwd) | Codex "stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)" — combined across files, not per file | truncation: "Raise `project_doc_max_bytes` or split large files across nested directories" | verified — https://learn.chatgpt.com/docs/agent-configuration/agents-md (redirect from developers.openai.com/codex/guides/agents-md); config reference: "Maximum bytes read from `AGENTS.md`", no default shown — https://learn.chatgpt.com/docs/config-file/config-reference |
| Antigravity (agy) | `AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md` (workspace); `~/.gemini/…AGENTS.md / GEMINI.md`, `~/.gemini/config/rules/*.md` (global) | "24 KB (`24,000` bytes) per-file limit"; "All active global and `always_on` rules share a 20,000-token budget", separate from the skills/MCP budget | a file over 24,000 bytes is truncated; over 20,000 tokens "Antigravity automatically demotes the largest rule files from inline text to lightweight pointers" | verified — https://antigravity.google/docs/rules |
| Antigravity (agy), older figure | rule files | "Google documents a 12,000-character limit per rule file" | — | reported — https://agentpedia.codes/blog/antigravity-agents-md-not-working-fix (updated 2026-07-21); a search summary said older official docs stated it, but `/docs/rules-workflows` now redirects to `/docs/rules` and the web archive was not reachable, so not confirmed |
| Google Gemini CLI | `GEMINI.md` (name set by `context.fileName`), global + ancestors + subdirectories | **none stated**; the only number is the subdirectory scan, "limited to 200 directories by default" (`context.discoveryMaxDirs`) | — | verified (absence) — https://geminicli.com/docs/cli/gemini-md/ and https://geminicli.com/docs/reference/configuration/ |
| opencode | first `AGENTS.md` (or `CLAUDE.md`) walking up; `~/.config/opencode/AGENTS.md` (or `~/.claude/CLAUDE.md`); files in `instructions` of `opencode.json` | **none stated**; only "Remote instructions are fetched with a 5 second timeout" | — | verified (absence) — https://opencode.ai/docs/rules/ |
| Qwen Code — auto memory | `MEMORY.md` index | the index body and the prompt-loaded portion "share a limit of 200 lines and 25,000 UTF-16 code units" | truncated, with a notice; short entries (≤150 code units) kept before long ones | verified — https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/ ; and in the installed 0.21.8 code: `MAX_MANAGED_AUTO_MEMORY_INDEX_LINES = 200`, `MAX_MANAGED_AUTO_MEMORY_INDEX_BYTES = 25e3`, compared against `trimmed.length` (JS string length = UTF-16 code units), cut at the last newline (`chunks/chunk-GXSNGY5M.js`) |
| Qwen Code — instructions | `~/.qwen/QWEN.md`, project `QWEN.md`, `.qwen/QWEN.local.md`, `AGENTS.md`, `@path` imports | **none stated**; only "the longer it gets, the less reliably Qwen follows it" | — | verified (absence) — same Qwen page |
| Qwen Code — 15% warning | always-loaded context | a warning when it passes 15% of the window (earlier run, CX in `docs/memory-system/CACHES.md`) | advisory | reported — not found on the Qwen page or by web search, and not found by a grep of the installed bundle |
| DeepSeek Harness (dsh) | `$DSH_HOME/AGENTS.md`, then `AGENTS.md`/`CLAUDE.md` (+ `.local.md` overlays) from project root to cwd | `maxBytes` caps "the complete rendered baseline message, in bytes"; it is required and has no built-in default — "`dsh-base` already includes it with a 65,536-byte budget"; also `maxSourceBytes` 1,048,576 per source file | broader files dropped whole before the most specific file is truncated, with a visible `Workspace instruction budget ...` notice | verified, local not web — installed `@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-agent-instructions/README.md` lines 28–75; `maxBytes: 65536` in the `standard`, `ptc` and `cordis` presets of `dsh-web-app`. No official web page found |
| Other DeepSeek-based CLIs | — | none found; a search for a DeepSeek CLI instruction-file limit returned only API upload and context-window limits | — | not found |

## Where sources conflict or the repo's table is off

1. **agy: 24,000 bytes + 20,000 tokens, or 12,000 characters.** The current official page says 24,000 bytes per file
   and a 20,000-token budget (verified). The 12,000-character figure is a third-party page dated 2026-07-21 citing
   Google (reported). A third-party write-up dated 2026-09-26 says the 20,000-token rules budget arrived in release
   2.17.0 and that before it rules shared one budget with skills and MCP (reported —
   https://antigravitylab.net/articles/antigravity/antigravity-rules-token-budget-measure-before-demotion).
   *My reading:* 12,000 characters was the earlier documented limit and 24,000 bytes replaced it; not confirmed. The
   installed `agy` reports 1.4.0, and which release numbering the page's limits apply to is **not measured**; a grep
   of the agy binary found none of these numbers.
2. **Qwen Code: bytes or code units.** `CACHES.md` says "200 lines or 25,000 bytes". The docs and the code both measure
   **UTF-16 code units** (the constant is named `_BYTES` but compares string length). The same for ASCII; for
   non-ASCII text the byte count is larger than the counted length.
3. **Claude Code `CLAUDE.md`.** `CACHES.md` gives only the advice "target under 200 lines". The docs also state a hard
   rule: up to 4 MiB loaded in full, larger skipped. The 25KB for `MEMORY.md` is written "25KB"; whether that is 25,000
   or 25,600 bytes is **not stated** on the page.
4. **Codex.** The AGENTS.md guide gives the 32 KiB default, combined; the config reference names
   `project_doc_max_bytes` without a default. No conflict in value, only in completeness.
5. **dsh.** `CACHES.md` calls 65,536 bytes dsh's budget. It is the value in the base profile and presets; the loader
   itself requires the deployment to choose `maxBytes`. A profile that sets another value changes it (active-profile
   override not checked here).

## What this means for Rd3.1 (*my reading*, not a decision)

The documented per-file limits that could bind a start file are: Claude Code `MEMORY.md` 200 lines / 25KB; Qwen Code
`MEMORY.md` index 200 lines / 25,000 code units; agy 24,000 bytes per rule file (or 12,000 characters, if the older
figure applies to the installed version). Codex (32 KiB) and dsh (64 KiB) are combined budgets shared with all other
instruction files, so what fits depends on the rest of the chain. Gemini CLI and opencode state no limit. The tool's
interim example (200 lines, 24,000 bytes) is at or under every verified per-file figure; it is not under the reported
12,000-character agy figure. None of these numbers was measured on an engine in this step.
