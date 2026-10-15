# Harness health — 2026-10-15 — wangIsHere0000001

Configured is not enforced: each line reads what a config file says; none proves the harness enforces it. Nothing was changed; no quota spent.

## Ten requirements

| # | Requirement | present | absent | unknown | measured | covered |
|---|---|---|---|---|---|---|
| R1 | Clear context delivery | 1 | 0 | 0 | 2 | 0 |
| R2 | Well-designed tools | 0 | 0 | 0 | 0 | 2 |
| R3 | Planning and task structure | 0 | 0 | 0 | 0 | 1 |
| R4 | State and memory across sessions | 0 | 0 | 0 | 1 | 1 |
| R5 | Independent verification | 1 | 0 | 0 | 0 | 1 |
| R6 | Guardrails and permissions | 0 | 3 | 4 | 0 | 0 |
| R7 | Recovery and retries | 0 | 0 | 0 | 0 | 1 |
| R8 | Human-in-the-loop gates | 1 | 2 | 0 | 0 | 0 |
| R9 | Observability | 0 | 0 | 0 | 3 | 2 |
| R10 | Feedback loop that improves the harness | 1 | 0 | 0 | 0 | 0 |

## Lines

| # | Harness | Item | Status | Finding | Detail | Proof |
|---|---|---|---|---|---|---|
| — | claude | installed | verified | - | on PATH | `command -v claude` |
| — | codex | installed | verified | - | on PATH | `command -v codex` |
| — | agy | installed | verified | - | on PATH | `command -v agy` |
| — | qwen | installed | verified | - | on PATH | `command -v qwen` |
| — | dsh | installed | verified | - | on PATH | `command -v dsh` |
| — | opencode | installed | verified | - | on PATH | `command -v opencode` |
| R1 | - | project instruction file | verified | present | CLAUDE.md, AGENTS.md | . |
| R1 | - | ./CLAUDE.md | verified | measured | 127 lines, 9205 bytes | ./CLAUDE.md |
| R1 | - | ./AGENTS.md | verified | measured | 4 lines, 257 bytes | ./AGENTS.md |
| R2 | - | engine adapters with pinned flags | verified | covered | per run, by engines.py | engines.py |
| R2 | - | dispatcher | verified | covered | per run, by dispatch.py | dispatch.py |
| R3 | - | design gate | verified | covered | per run, by design_gate.py | design_gate.py |
| R4 | - | run state template | verified | covered | per run, by state.md | state.md |
| R4 | claude | project memory | reported | measured | 45 memory files | ~/.claude/projects/-home-smoke01-dev-ancient-games/memory |
| R5 | - | build gate (tests, scope, tamper) | verified | covered | per run, by feature_gate.py | feature_gate.py |
| R5 | - | engine kinds on PATH | verified | present | 6: agy, claude, codex, dsh, opencode, qwen (installed, not canary-proved) | `command -v` |
| R6 | claude | deny rules | reported | absent | no deny rule in any scope; key names from the 2.1.299 binary; installed 2.1.299 | ~/.claude/settings.json, ./.claude/settings.json, ./.claude/settings.local.json |
| R6 | claude | sandbox | reported | absent | sandbox.enabled not set; key names from the 2.1.299 binary; installed 2.1.299 | ~/.claude/settings.json, ./.claude/settings.json, ./.claude/settings.local.json |
| R6 | codex | sandbox_mode | verified | absent | not set: Codex's built-in default applies (not checked); key names verified on 0.160.0 | ~/.codex/config.toml |
| R6 | agy | permissions and sandbox | unknown | unknown | config format not verified for this harness; prove key names on the installed version first | harness_health.py docstring |
| R6 | qwen | permissions and sandbox | unknown | unknown | config format not verified for this harness; prove key names on the installed version first | harness_health.py docstring |
| R6 | dsh | permissions and sandbox | unknown | unknown | config format not verified for this harness; prove key names on the installed version first | harness_health.py docstring |
| R6 | opencode | permissions and sandbox | unknown | unknown | config format not verified for this harness; prove key names on the installed version first | harness_health.py docstring |
| R7 | - | timers and bounded repair | verified | covered | per run, by dispatch.py | dispatch.py |
| R8 | claude | permission mode | reported | present | defaultMode not set (default: a person is asked); key names from the 2.1.299 binary; installed 2.1.299 | ~/.claude/settings.json, ./.claude/settings.json, ./.claude/settings.local.json |
| R8 | claude | bypass-mode prompt | reported | absent | skipDangerousModePermissionPrompt true (user); key names from the 2.1.299 binary; installed 2.1.299 | ~/.claude/settings.json, ./.claude/settings.json, ./.claude/settings.local.json |
| R8 | codex | approval_policy | verified | absent | not set: Codex's built-in default applies (not checked); key names verified on 0.160.0 | ~/.codex/config.toml |
| R9 | - | run event log | verified | covered | per run, by runlog.py | runlog.py |
| R9 | - | token harvest | verified | covered | per run, by harvest_run.py | harvest_run.py |
| R9 | claude | session transcripts | reported | measured | 72 session logs for this project | ~/.claude/projects/-home-smoke01-dev-ancient-games |
| R9 | codex | session rollouts | verified | measured | folder present | ~/.codex/sessions |
| R9 | dsh | sessions | verified | measured | folder present | ~/.dsh/sessions |
| R10 | claude | hooks | reported | present | events: UserPromptSubmit; key names from the 2.1.299 binary; installed 2.1.299 | ~/.claude/settings.json, ./.claude/settings.json, ./.claude/settings.local.json |

## Help

### R6 · claude · deny rules

- File: `./.claude/settings.json`
- What it changes: blocks the listed tools/paths outright, whatever is allowed elsewhere. The two rules are examples from Claude Code's settings docs — replace them with what this project must never touch
- How: merge into the file: keep its other keys, and add list items to a list that is already there

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./secrets/**)"
    ]
  }
}
```

### R6 · claude · sandbox

- File: `./.claude/settings.json`
- What it changes: runs Bash commands inside Claude Code's OS sandbox (filesystem and network limits)
- How: merge into the file: keep its other keys, and add list items to a list that is already there

```json
{
  "sandbox": {
    "enabled": true
  }
}
```

### R6 · codex · sandbox_mode

- File: `~/.codex/config.toml`
- What it changes: commands run in Codex's sandbox: writes limited to the workspace
- How: a top-level line in ~/.codex/config.toml, above the first [table]; replace the line if the key is already set

```toml
sandbox_mode = "workspace-write"
```

### R8 · claude · bypass-mode prompt

- File: `~/.claude/settings.json`
- What it changes: asks the person before a session enters bypass-permissions mode
- How: merge into the file: keep its other keys, and add list items to a list that is already there

```json
{
  "skipDangerousModePermissionPrompt": false
}
```

### R8 · codex · approval_policy

- File: `~/.codex/config.toml`
- What it changes: Codex asks the person before commands it may not run on its own
- How: a top-level line in ~/.codex/config.toml, above the first [table]; replace the line if the key is already set

```toml
approval_policy = "on-request"
```

You apply any change; this script changed nothing.
