# Readiness tools check — 2026-10-14 — wangIsHere0000001

Installed and logged in only; no canary was run, no quota spent.

## Tools

| Item | Status | Detail | Proof |
|---|---|---|---|
| claude | verified | 2.1.299 (Claude Code) | `claude --version` |
| codex | verified | codex-cli 0.160.0 | `codex --version` |
| agy | verified | 1.3.5 | `agy --version` |
| qwen | verified | 0.24.7 | `qwen --version` |
| node | verified | v22.22.1 | `node --version` |
| python3 | verified | Python 3.12.3 | `python3 --version` |
| git | verified | git version 2.43.0 | `git --version` |
| opencode | verified | 1.18.34 | `opencode --version` |

## Models and logins

| Item | Status | Detail | Proof |
|---|---|---|---|
| codex model cache | reported | 10 model ids, fetched_at 2026-10-14: gpt-6.1-sol, gpt-6-astra, gpt-6-sol, gpt-6-luna, gpt-reserve, gpt-5.6-sol … (cache may be stale) | /home/smoke01/.codex/models_cache.json |
| agy login (model list) | unknown | offline run: not provable without `agy models`; rerun with --net | `agy models` (network) |
| qwen config (model, provider) | reported | default qwen3.8-max, auth openai, 18 listed models, endpoint token-plan.ap-southeast-1.maas.aliyuncs.com, key set in settings env (file claim; key validity not tested) | /home/smoke01/.qwen/settings.json |

## Skills and workflows

| Item | Status | Detail | Proof |
|---|---|---|---|
| claude skills (user) | verified | 17: agent-loop → /home/smoke01/skills/agent-loop, bootstrap → /home/smoke01/dev/ancient-games/.claude/skills/bootstrap, challenge-mediation → /home/smoke01/skills/challenge-mediation, chronos-ledger → /home/smoke01/dev/Chronos/skills/chronos-ledger, e2e-probe → /home/smoke01/skills/e2e-probe, formalization → /home/smoke01/skills/formalization, four-experts → /home/smoke01/dev/ancient-games/.claude/skills/four-experts, kindle-page → /home/smoke01/skills/kindle-page … | /home/smoke01/.claude/skills |
| agents skills (cross-tool) | verified | 7: bootstrap → /home/smoke01/dev/ancient-games/.claude/skills/bootstrap, coding-discipline, four-experts → /home/smoke01/dev/ancient-games/.claude/skills/four-experts, meaningful-names → /home/smoke01/dev/ancient-games/.claude/skills/meaningful-names, requirement-check → /home/smoke01/dev/ancient-games/.claude/skills/requirement-check, state-entry → /home/smoke01/dev/ancient-games/.claude/skills/state-entry, workflow-design → /home/smoke01/dev/ancient-games/.claude/skills/workflow-design | /home/smoke01/.agents/skills |
| codex skills (user) | verified | 1: evidence-knowledge-graph | /home/smoke01/.codex/skills |
| qwen skills (user) | MISSING | empty (/home/smoke01/.qwen/skills) | /home/smoke01/.qwen/skills |
| project skills | verified | 6: bootstrap, four-experts, meaningful-names, requirement-check, state-entry, workflow-design | /home/smoke01/dev/ancient-games/.claude/skills |
| workflow scripts | verified | 3: enhance-ancient-games.js, intake.js, research-agent-memory.js | /home/smoke01/dev/ancient-games/.claude/workflows |

## Memory

| Item | Status | Detail | Proof |
|---|---|---|---|
| project instruction files | verified | present: CLAUDE.md, AGENTS.md; absent: QWEN.md, GEMINI.md | /home/smoke01/dev/ancient-games |
| qwen auto-memory (user) | verified | 5 index lines in MEMORY.md; project dirs under ~/.qwen/projects/ | /home/smoke01/.qwen/memories |
| claude session history | verified | 36 project histories | /home/smoke01/.claude/projects |

## MCP

| Item | Status | Detail | Proof |
|---|---|---|---|
| ~/.claude/settings.json | verified | no mcpServers key | /home/smoke01/.claude/settings.json |
| ~/.claude.json | verified | 3 servers: cloudflare-api, cloudflare-docs, gcloud | /home/smoke01/.claude.json |
| ~/.qwen/settings.json | verified | no mcpServers key | /home/smoke01/.qwen/settings.json |
| .mcp.json (project) | verified | file absent → no servers from it | /home/smoke01/dev/ancient-games/.mcp.json |

## Machine

| Item | Status | Detail | Proof |
|---|---|---|---|
| this machine | verified | 9 cores; 17.8 GiB RAM available; 739 G free on /home/smoke01/dev/ancient-games | `os.cpu_count`, `/proc/meminfo`, `shutil.disk_usage` |

## Open unknowns

| Item | Status | Detail | Proof |
|---|---|---|---|
| subagent concurrency limit | unknown | runtime policy, not provable from outside. Claude Code docs report 20 concurrent, nesting depth 3 (v2.1.217+, env overrides; reported, not measured here); codex/agy: no figure | docs/EXECUTOR_KINDS.md, Concurrency row |
| codex/agy/qwen execute a task | unknown | canary required (spends quota; needs the person's go-ahead) | docs/EXECUTOR_KINDS.md canary piece |
