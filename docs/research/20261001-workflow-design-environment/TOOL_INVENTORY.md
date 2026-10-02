# Tool inventory, this machine — 2026-10-01

All rows **verified** by read-only commands on 2026-10-01 unless marked. No canary was run; no quota spent.
This snapshot is superseded by re-running the script — do not rely on it stale:

```bash
python3 .claude/skills/workflow-design/scripts/readiness.py          # offline
python3 .claude/skills/workflow-design/scripts/readiness.py --net    # + agy models
```

The script is packed with the workflow-design skill (commit f389628), marks every line
verified/reported/unknown/MISSING with its proof, and never spends quota.

## Binaries (verified, `--version`)

| Tool | Version |
|---|---|
| claude (Claude Code) | 2.1.286 |
| codex (Codex CLI) | codex-cli 0.159.3 |
| agy (Antigravity CLI) | 1.2.14 |
| qwen (Qwen Code) | 0.24.7 |
| node | v22.22.1 |
| python3 | 3.12.3 |
| git | 2.43.0 |

## Models and logins

- **agy logged in** (verified, `agy models`): gemini-3.8/3.7/3.6-flash (low/medium/high), gemini-3.1-pro
  (high/low), claude-sonnet-4-6, claude-opus-4-6-thinking, gpt-oss-120b-medium — 14 ids; matches the
  EXECUTOR_KINDS defaults (gemini-3.8-flash-medium, gemini-3.1-pro-high).
- **Codex model cache** (reported — cache may be stale; `~/.codex/models_cache.json`, fetched_at 2026-10-01):
  10 ids incl. gpt-6.1-sol, gpt-6-astra, gpt-6-sol, gpt-6-luna, gpt-reserve, gpt-5.6-sol. EXECUTOR_KINDS
  verified gpt-6-astra on 2026-09-30.

## Skills and workflows (verified locations)

| Location | Contents |
|---|---|
| `~/.claude/skills/` | 11: agent-loop, challenge-mediation, chronos-ledger, e2e-probe, formalization, procedure-to-skill, stage2a-e2e-dev116, synced, task-decomposition-strategies, verify-extraction, workflow-design (→ this repo) |
| `~/.agents/skills/` | coding-discipline |
| `~/.codex/skills/` | evidence-knowledge-graph |
| project `.claude/skills/` | workflow-design (the source; scripts/readiness.py packed inside) |
| project `.claude/workflows/` | intake.js, enhance-ancient-games.js |
| `~/.claude/workflows/` | absent |

`task-decomposition-strategies` ships `scripts/select_strategy.py` (disqualifier-first strategy selector,
facts in → strategy out) with its own regression file; written Aug 2026, tests not re-run as of this date.

## MCP and agents config (verified)

- **No MCP servers**: `mcpServers` key absent from `~/.claude/settings.json`, `~/.claude.json`,
  `~/.qwen/settings.json`; no project `.mcp.json`.
- **No custom Claude subagents**: `~/.claude/agents/` does not exist.

## Memory locations (verified)

- Repo instruction files: `CLAUDE.md`, `AGENTS.md` (no QWEN.md/GEMINI.md in this repo).
- Qwen auto-memory: `~/.qwen/memories/` (user) + `~/.qwen/projects/<hash>/memory/` (project).
- Claude session history: `~/.claude/projects/` (15 project histories), `~/.claude/history.jsonl`.
- Repo files: `runs/`, state files, journals — the one memory every tool can read (method §4).
- chronos-ledger skill (cross-session state, via `~/.claude/skills`).

## Machine (verified)

9 cores · 25 GiB RAM (21+ GiB available) · 779 G free on `/`.

## Known at session end (reported, from official docs — see CLAUDE_CODE_CAPABILITIES.md)

- Claude Code subagent concurrency: **20 default** (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`); nesting depth 3.

## Still unknown

- Codex/agy **execute a task** here — canary required (spends quota; needs EJ's go-ahead).
- Whether Codex and agy actually **load** SKILL.md (directories exist ≠ loading; canary extension proposed).
- agy headless behaviour on quota exhaustion; where agy looks for skills.
- Concurrency limits of qwen/codex/agy runtimes.
