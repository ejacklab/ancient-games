# Claude Code capabilities — 2026-10-01

Context: installed CLI **2.1.286** (verified). Everything marked *reported* comes from official docs
(code.claude.com/docs) read by a search agent on 2026-10-01; docs version-gate several features — check the
installed version before relying on a row.

## Subagent limits (reported — answers the inventory's open unknown)

- **20 concurrent subagents** by default; the 21st spawn fails with `Concurrent subagent limit reached`
  (Claude is told not to retry); succeeds again when the count drops. Override:
  `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`. Requires v2.1.217+. Sessions with ultracode active are exempt.
- **Nesting depth: 3 layers** below the main conversation (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`); at the
  limit the Agent tool is withheld.
- No limit on total spawns per session. `/subtask` forks take a slot but are never blocked; resuming a
  finished subagent takes a fresh slot without the cap check.
- Consequence: the framework's CAP=3 and the method's concurrency bounds are **design** choices far inside
  the runtime's — the runtime is not the binding constraint.

## Five parallel mechanisms (reported, docs `en/agents`)

1. **Subagents** — foreground/background; fork mode default-on in interactive sessions (off with `-p`/SDK);
   background subagents run a smaller built-in tool set and surface permission prompts in the main session;
   `background: true` frontmatter pins one to background; `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` forces
   foreground.
2. **Agent view / background sessions** — `claude --bg` starts a full detached conversation;
   `claude agents | attach | logs | stop | rm | respawn` manage them (**verified locally** in --help);
   each uses subscription quota independently.
3. **Agent teams** — *experimental, disabled by default*: fixed **lead** + teammates sharing a task list and
   messaging **each other** (peers, not hub-only). Documented limits: one team per session, no nested teams,
   no resume/`/rewind` for in-process teammates, teammates **cannot** run background subagents, split-pane
   needs tmux/iTerm2, token cost scales linearly. Teammates get TaskCreate/Get/List/Update and
   CronCreate/Delete/List tools.
4. **Dynamic workflows** — the Workflow tool (intake.js runs on it) is a named first-class mechanism.
5. **Projects** (cloud) — plus **routines** (scheduled cloud sessions) and **/batch** (one change split into
   5–30 worktree-isolated subagents, each opening a PR).

Supporting primitives, not separate agent types: worktrees, cross-session messaging, background *bash*
(no agent), forked subagents (`/subtask`, v2.1.212+; `/fork` copies a whole session to background).

## CLI surface (verified locally, `claude --help` on 2.1.286)

| Group | Flags/commands | Design relevance |
|---|---|---|
| Contracts | `--json-schema` (structured-output validation), `--agents '<json>'` (custom agents at launch), `--tools` / `--allowedTools` / `--disallowedTools` | a node's "returns and in what shape" enforceable at the CLI boundary — parity with `codex exec --output-schema`, `agy --json-schema` |
| Budgets | `--max-budget-usd`, `--fallback-model`, `--effort low…max` | native cost bound (predictability); fallback-model ≈ executor-failure rule at model level |
| Isolation | `-w/--worktree`, `--tmux`, `--restricted`, `--safe-mode`, `--bare`, `--fork-session`, `--add-dir` | one-writer-at-a-time has native machinery |
| Cloud | `--environment <ccpool_…>`, `--from-pr`, `--teleport`, `ultrareview` (cloud multi-agent review of branch/PR) | `ultrareview` = ready-made blind review piece for the code-review category |
| Caching | `--system-prompt-snapshot on` (default: prompt recorded once, reused verbatim across resumes) | prompt-cache stability — relevant to tier-exit economics |
| Streaming | `--forward-subagent-text`, `--include-partial-messages`, `--input-format stream-json`, `--json-schema` with `--print` | machine-driven Claude nodes from a wrapper |
| Config | `import` (from other agents), `plugin`, `mcp`, `auto-mode`, `gateway`, `doctor`, `project`, `setup-token` | — |

## Hooks and skills (reported)

- Hook types: `command`, `http`, `mcp_tool`, `prompt`, and **`agent`** — spawns a tool-using subagent
  verifier, up to 50 turns, returning `{"ok": true/false}`. An evaluator-optimizer gate built into the tool
  boundary.
- Events include `SubagentStart`, `SubagentStop`, `PreToolUse`/`PostToolUse`/`PostToolBatch`, `Stop`,
  `UserPromptSubmit`, `PermissionDenied`, team events `TaskCreated`/`TaskCompleted`/`TeammateIdle`.
- Hooks can live in skill and subagent frontmatter; subagent hooks die with the subagent (Stop →
  SubagentStop); skill hooks stay registered for the session unless `once: true`.
- Skills: progressive disclosure as per the open standard; `context: fork` runs a skill as an isolated
  subagent (v2.1.218+; forked-skill edits sit outside checkpoints — `/rewind` won't undo them).

## What this means for the method

- Three things designs used to carry are now native: **cost bounds** (`--max-budget-usd`), **schema-enforced
  returns** (`--json-schema`), **worktree isolation** (`-w`).
- Agent teams is the native swarm/decentralized option — experimental, and its peer messaging conflicts with
  the source-independence rule (`READ_SCOPE.deny` logic; F1 in PROJECT_OVERVIEW). COO hub-and-spoke stays the
  right default.
- The `agent`-type hook is a candidate mechanism for "a check the worker cannot edit" at tool boundaries.

## Sources

- https://code.claude.com/docs/en/agents
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/agent-view
- https://code.claude.com/docs/en/background-agents
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/hooks
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
