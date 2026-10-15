# Hook points in the installed agent harnesses (this machine, 2026-10-15)

Question: on this machine, at which fixed points can external code (ideally TypeScript run with bun) run
automatically and **block** or **annotate** the agent, per harness?

Method: installed version only — `--version`, `--help`, shipped docs/types/schemas, and `strings`/grep over each
installed binary or JS bundle. Web docs used only to confirm two gaps (Codex config paths/trust, opencode TS + throw).
No model session was started; no config was edited; config files were read for key names only.

Status labels: **verified** = seen in the installed version's own help/schema/bundle (source given);
**reported** = web docs only (URL given); **unknown** = not established. Counts are what I found, not a guarantee
the list is complete.

bun on PATH: `bun --version` → `1.4.3` (verified). Node: `v22.22.1`.

## Summary table

| harness | version | hook points (count) | can block? | TS handler possible? | status |
|---|---|---|---|---|---|
| Claude Code `claude` | 2.1.300 | 33 settings-hook events (+ in-process "mods": ~100 `on(event)` names, incl. `tool.call`, `prompt.submit`, `turn.complete`, `classic.*`) | Yes — exit 2 / JSON on 14+ events incl. PreToolUse, Stop, SubagentStop, UserPromptSubmit; PostToolUse annotates only | Yes, two ways: command hook `bun x.ts` (the CLI's own plugin scaffold writes exactly this); or a mod's `hooks/register.ts` run in-process | verified |
| Codex CLI `codex` | codex-cli 0.160.0 | 12 hook events + legacy `notify` (1) | Yes — PreToolUse, PermissionRequest, UserPromptSubmit block; Stop/SubagentStop force continue; Pre/PostCompact `continue:false` | Yes via command hook (`bun x.ts`); no in-process plugin API found | events, schemas, exit-2 texts verified; config file paths + trust flow partly reported |
| Antigravity `agy` | 1.3.5 | 6 (SessionStart, PreToolUse, PostToolUse, PreInvocation, PostInvocation, Stop) | Yes — PreToolUse `decision: deny/ask/force_ask`; Stop `decision: continue`; PostInvocation `terminationBehavior` | Yes via command hook (`sh -c "bun x.ts"`); JSON on stdin/stdout, camelCase | verified (docs embedded in the binary) |
| Qwen Code `qwen` | 0.24.7 | 22 events | Yes — exit 2 on PreToolUse, UserPromptSubmit, UserPromptExpansion, Stop, SubagentStop, PreCompact, TodoCreated, TodoCompleted; PermissionRequest by JSON | Yes via command hook; also `http`, `prompt`, `agent`, `function` hook types exist in code | verified |
| DeepSeek Harness `dsh` | 0.2.0-rc.2 | Bridges: 7 Claude-style events (`dsh-hooks-claude-code`), 5 Codex-style (`dsh-hooks-codex`); native Cordis events ~15 relevant (`tools/pre-execute`, `agent/pre-step`, `agent/turn-stopping`, …) | Yes — bridge PreToolUse/UserPromptSubmit deny, Stop forces another step; native waterfalls can deny | Yes via bridged command hook; native plugin = npm package (JS) in a profile — TS source directly: unknown | verified (package READMEs + .d.ts); bridges NOT mounted in the default profile |
| opencode `opencode` | 1.18.34 | 15 plugin hook names triggered in the binary + `event` (all bus events) | Yes — `tool.execute.before` blocks by throwing (reported; code consistent); `event` hook is observe-only | Yes, natively: `.opencode/plugins/*.ts` loaded in-process by Bun | hook names verified; "throw blocks" reported |

---

## 1. Claude Code (`claude`)

- Version: `claude --version` → `2.1.300 (Claude Code)` (verified). Binary: `~/.local/share/claude/versions/2.1.300`
  (ELF, Bun-compiled, not stripped).

### 1a. Settings ("command") hooks — 33 events

Event list, verified: the binary holds the array
`["PreToolUse","PostToolUse","PostToolUseFailure","PostToolBatch","Notification","UserPromptSubmit","UserPromptExpansion","SessionStart","SessionEnd","Stop","StopFailure","SubagentStart","SubagentStop","PreCompact","PostCompact","PreModelSwitch","PostModelSwitch","PermissionRequest","PermissionDenied","Setup","TeammateIdle","TaskCreated","TaskCompleted","Elicitation","ElicitationResult","ConfigChange","WorktreeCreate","WorktreeRemove","InstructionsLoaded","CwdChanged","FileChanged","DirectoryAdded","MessageDisplay"]`
(found with `strings -n 6 <binary> | grep -o '\["PreToolUse"…\]'`).

Handler types, verified (zod schema strings): `type:"command"` ("Shell command hook type", with optional `args`
exec form, `shell`, `timeout`, `onFailure`, `statusMessage`, `async`/`asyncRewake`), `"http"` (POSTs the input JSON
to `url`), `"mcp_tool"` (calls a tool on a configured MCP server), `"prompt"`, `"agent"`.

`onFailure` (verified text): *"'block': the failure counts as exit code 2, so the action the event guards (a tool
call, a permission request, a prompt) is blocked."* — so a crashing TS guard can be made fail-closed.

Configured in (verified for user file; others reported/standard): `hooks` key in `~/.claude/settings.json`,
`<repo>/.claude/settings.json`, `<repo>/.claude/settings.local.json`, managed settings, `--settings <file-or-json>`,
and a plugin's `hooks/hooks.json` (the `claude plugin init` scaffold string in the binary names
`hooks.json`, `hooks-handlers/on-session-start.ts`). On this machine `~/.claude/settings.json` already has one
`UserPromptSubmit` command hook; the repo has no `.claude/settings*.json`. `--bare` skips settings and plugin hooks
(verified, `claude --help`). `--include-hook-events` puts hook lifecycle events in stream-json output (verified, help).

Exit-code semantics per event (verified — the `/hooks` UI text compiled into the binary, quoted):

| Event | Exit 2 means | Blocks? | Notes |
|---|---|---|---|
| PreToolUse | "show stderr to model and block tool call" | **Block** | JSON `hookSpecificOutput.permissionDecision` ∈ `allow/deny/ask/defer`, `permissionDecisionReason`, `updatedInput`, `additionalContext` |
| PostToolUse | "show stderr to model immediately" | annotate (tool already ran) | JSON `decision:"block"` + `reason`; `additionalContext`; `updatedMCPToolOutput` |
| PostToolUseFailure | "show stderr to model immediately" | annotate | |
| PostToolBatch | "stop the agentic loop (stderr shown to user only)" | **Stop loop** | `additionalContext` once per batch |
| UserPromptSubmit | "block processing, erase original prompt, and show stderr to user only" | **Block** | exit 0 stdout → shown to Claude; JSON `additionalContext`, `sessionTitle`, `suppressOriginalPrompt` |
| UserPromptExpansion | "block expansion and show stderr to user only" | **Block** | |
| Stop | "show stderr to model and continue conversation" | **Block stop (forces continue)** | cap: "set CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"; check `stop_hook_active` |
| SubagentStop | "show stderr to subagent and continue having it run" | **Block stop** | |
| StopFailure | "Fire-and-forget — hook output and exit codes are ignored" | no | fires instead of Stop on API error |
| SubagentStart | "show stderr to user only"; exit 0 "JSON additionalContext shown to subagent" | annotate | |
| SessionStart | "show stderr to user only"; exit 0 "stdout shown to Claude" | annotate | JSON `additionalContext`, `initialUserMessage`, `watchPaths`, `reloadSkills` |
| SessionEnd | — | no | |
| PreCompact | "block compaction" | **Block** | exit 0 stdout = custom compact instructions |
| PostCompact | — | no | |
| PreModelSwitch | "block the switch and show stderr to user" | **Block** | JSON permissionDecision as PreToolUse |
| PostModelSwitch | — | annotate | stdout shown to Claude next request |
| PermissionRequest | (no exit-2 line) "Output JSON with hookSpecificOutput containing decision to allow or deny" | **Block (JSON)** | `decision.behavior` allow (+`updatedInput`) / deny (+`message`, `interrupt`) |
| PermissionDenied | — | annotate | JSON `retry:true` tells model it may retry |
| Notification | — | no | |
| Setup | "show stderr to user only" | annotate | trigger init/maintenance |
| TeammateIdle | "show stderr to teammate and prevent idle" | **Block** | |
| TaskCreated | "show stderr to model and prevent task creation" | **Block** | |
| TaskCompleted | "show stderr to model and prevent task completion" | **Block** | |
| Elicitation | "deny the elicitation" | **Block** | |
| ElicitationResult | "block the response (action becomes decline)" | **Block** | |
| ConfigChange | "block the change from being applied to the session" | **Block** | |
| InstructionsLoaded | "This hook is observability-only and does not support blocking." | no | |
| WorktreeCreate / WorktreeRemove | non-zero = creation failed | replaces behaviour | |
| CwdChanged / FileChanged | — | annotate | can write `CLAUDE_ENV_FILE`, `watchPaths` |
| DirectoryAdded | — | no | |
| MessageDisplay | "Display-only" | no | can replace on-screen text only |

Common JSON output fields (verified schema): `continue`, `suppressOutput`, `stopReason`, `decision` (`approve`/`block`),
`systemMessage`, `reason`, `hookSpecificOutput`.

Payload (stdin JSON) field names, verified from the zod input schemas in the binary:

- Base, every event: `session_id`, `transcript_path`, `cwd`, `prompt_id?`, `permission_mode?`, `agent_id?`,
  `agent_type?`, `hook_event_name`.
- PreToolUse: `tool_name`, `tool_input`, `tool_use_id`, `mcp_server?`.
- PostToolUse: `tool_name`, `tool_input`, `tool_response`, `tool_use_id`, `duration_ms`, `mcp_server?`.
- PostToolUseFailure: `tool_name`, `tool_input`, `tool_use_id`, `error`, `is_interrupt`, `duration_ms`.
- UserPromptSubmit: `prompt`, `source?` ∈ `user/sdk/system/loop_wakeup/schedule_wakeup/poll_event`.
- Stop: `stop_hook_active`, `last_assistant_message?`, `background_tasks?`, `session_crons?`.
- SubagentStop: `stop_hook_active`, `agent_id`, `agent_transcript_path`, `agent_type`, `last_assistant_message?`,
  `background_tasks?`, `session_crons?`.
- SubagentStart: `agent_id`, `agent_type`. SessionStart: `source` ∈ `startup/resume/clear/compact/fork`, `model?`, ….
- PermissionRequest: `tool_name`, `tool_input`, `permission_suggestions`, `mcp_server?`.

TypeScript: yes (verified) — a command hook runs any shell command. The binary's own plugin scaffold contains
`bun "${CLAUDE_PLUGIN_ROOT}/hooks-handlers/on-session-start.ts"` and a template beginning `#!/usr/bin/env bun …
const input = await new Response(Bun.stdin.stream()).text()`. The `args` exec form avoids a shell.

### 1b. In-process "mods" (function hooks) — TypeScript, run inside Claude Code

Verified from the bundled `plugin-authoring` skill files of this build
(`/tmp/claude-1000/bundled-skills/2.1.300/…/plugin-authoring/reference.md`, `types/claude-code.d.ts`, 22,230 lines):

- A plugin folder with `.claude-plugin/plugin.json` and `hooks/hooks.json` = `{ "modules": ["./register.ts"] }`;
  the module exports `register(on, options)`; files may be `.ts/.tsx/.js/…`; "The module runs in an environment of
  its own, with no DOM and no Node" — it is not a separate `bun` process.
- `on(event, matcher?, ($, e, next) => …)`; return `{ deny }` without calling `next` to refuse. Example shipped:
  `on('tool.call', { tool: 'Edit' }, ($, e, next) => … ? { deny: '…' } : next(e))`.
- Gating sites named in reference.md: `tool.call`, `tool.check`, `prompt.submit`, `prompt.mention`, `config.set`,
  `plugin.register`, `command.run`. Also `turn.start`, `turn.step` (streaming), `turn.complete`
  (input `reason` ∈ `answer/aborted/refusal/error`), `session.start`, `session.end`, `prompt.compose`
  (system prompt sections), `session.append`, and every settings-hook event as `classic.<Event>`
  (`classic.Stop` result type includes `block`).
- Caveat (verified string): *"hooks modules are turned off in this process … installed mods are turned off
  remotely"* — a remote switch can disable mods; settings command hooks do not depend on it. API is "early access
  and moves between releases" (reference.md).

## 2. Codex CLI (`codex`)

- Version: `codex --version` → `codex-cli 0.160.0` (verified). Native binary:
  `…/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/bin/codex` (Rust).
- Feature flag: `codex features list` → `hooks  stable  true`; `plugin_hooks  removed  false` (verified).
- Help: `--dangerously-bypass-hook-trust  Run enabled hooks without requiring persisted hook trust for this
  invocation` (verified, `codex --help`).

### Hook events — 12 (verified)

The binary embeds JSON Schemas titled `<event>.command.input/output` (found with `strings` + regex on `"title":`):
`pre-tool-use`, `permission-request`, `post-tool-use`, `pre-compact`, `post-compact`, `session-start`,
`session-end` (input only), `user-prompt-submit`, `stop`, `subagent-start`, `subagent-stop`, `interrupt`.
TOML enum `HookEventsToml` lists the same names (`PreToolUse PermissionRequest PostToolUse PreCompact PostCompact
SessionStart SessionEnd SubagentStart SubagentStop Interrupt`, plus UserPromptSubmit and Stop from the schemas).

| Event | Block? | Evidence (verified unless marked) |
|---|---|---|
| PreToolUse | **Block** | output schema: `decision` ∈ `approve/block`, `hookSpecificOutput.permissionDecision` ∈ `allow/deny/ask`; strings "Tool call blocked by PreToolUse hook:", "hook returned updatedInput without string field `command`" |
| PermissionRequest | **Block** | output `behavior` ∈ `allow/deny`; "PermissionRequest hook exited with code 2 but did not write a denial reason to stderr" |
| PostToolUse | annotate / replace result | `decision: block` (reported: "doesn't undo the command. It replaces the tool result with feedback") |
| UserPromptSubmit | **Block** | `decision: block`; "UserPromptSubmit hook exited with code 2 but did not write a blocking reason to stderr" |
| Stop | **Block stop (continue)** | `decision: block`; "Stop hook exited with code 2 but did not write a continuation prompt to stderr" |
| SubagentStop | **Block stop** | same pattern, "SubagentStop hook exited with code 2 …" |
| PreCompact / PostCompact | `continue:false` stops compaction | output has `continue`, `stopReason` (behaviour reported) |
| SessionStart | annotate (`additionalContext`) | |
| SubagentStart | annotate | |
| SessionEnd | observe | input only, no output schema |
| Interrupt | observe | output only `systemMessage`; "Interrupt hook returned non-JSON stdout" |

Common output fields (verified): `continue`, `stopReason`, `suppressOutput`, `systemMessage`, `decision`, `reason`,
`hookSpecificOutput`.

Payload field names (verified, schema `required`/properties): `session_id`, `transcript_path`, `cwd`,
`hook_event_name`, `model`, `permission_mode` (`default/acceptEdits/plan/dontAsk/bypassPermissions`), `turn_id`,
`agent_id?`, `agent_type?`; tool events add `tool_name`, `tool_input`, `tool_use_id`, PostToolUse `tool_response`;
UserPromptSubmit `prompt`; Stop `stop_hook_active`, `last_assistant_message`; SubagentStop adds
`agent_transcript_path`; SessionStart `source` (`startup/resume/clear/compact/fork`); compact `trigger`
(`manual/auto`). This is the Claude Code dialect plus `turn_id`/`model`.

Handler types: `HookHandlerConfig::Command` (fields `command`, `commandWindows`, `timeout`, `async`, `statusMessage`,
`additionalContextLimit`) and `HookHandlerConfig::McpTool` (verified). Strings "prompt hooks are not supported yet",
"agent hooks are not supported yet" (verified) — so command (and MCP tool) only.

Configuration: verified that `ConfigToml` has a `hooks` key and that per layer Codex warns "loading hooks from both …
and …; prefer a single representation for this layer", plus `hooks.state."<key>".trusted_hash` and plugin
`hooks/hooks.json`. Exact paths **reported** (https://learn.chatgpt.com/docs/hooks, redirected from
developers.openai.com/codex/hooks): `~/.codex/hooks.json`, `~/.codex/config.toml` `[hooks]`,
`<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml`; project hooks load only if the project layer is trusted;
"Non-managed hooks must be reviewed and trusted before they run" via `/hooks`; trust is per hook hash, so a changed
hook is skipped until re-trusted. On this machine: `~/.codex/config.toml` has no `hooks` or `notify` key and there is
no `~/.codex/hooks.json`.

Legacy `notify`: verified — `notify` is a `ConfigToml` key, source file `hooks/src/legacy_notify.rs`, payload keys
`agent-turn-complete`, `thread-id`, `turn-id`, `cwd`, `client`, `input-messages`, `last-assistant-message`.
Behaviour (argv program run after each turn with that JSON; observe-only) is my reading — **not** in the hooks web page.

TypeScript: yes via a command hook (`bun /abs/path/guard.ts`); no in-process plugin hook API found (plugins bundle
hooks.json, skills, MCP).

## 3. Antigravity (`agy`)

- Version: `agy --version` → `1.3.5` (verified). Binary `~/.local/bin/agy` (Go, stripped).
- `agy plugin --help` lists `list/import/install/uninstall/enable/disable/validate/link`; `import [source]` = "Import
  plugins from gemini or claude" (verified).

The binary embeds a "Lifecycle Hooks (`hooks.json`)" guide (verified, `strings | grep`, around the text "The working
directory is set to the directory containing `hooks.json`"). Quoted facts:

- "Hooks are configured in a single `hooks.json` file placed in your customization root directory (e.g.,
  `.agents/hooks.json`)." Customization roots (same embedded docs): workspace `.agents/` (or `.agent/`, `_agents/`,
  `_agent/`) walking up to the repo root; global `~/.gemini/config/`; plugins `plugins/<name>/hooks.json`.
- Format: top-level key = a named hook (`{"enabled": bool, "<Event>": [...]}`); tool events use
  `{matcher, hooks:[…]}` groups, others are flat lists.
- Handler: `type` "Only `"command"` (shell execution) is currently supported", run via `sh -c`, `timeout` default 30 s.
  (The Go symbols also show a `PromptHook` / `executePromptModeHook`, but the docs say command only.)
- "Hooks run synchronously and block the agent loop (no async execution)."
- Payload keys are **camelCase**. Common: `conversationId`, `workspacePaths`, `transcriptPath`,
  `artifactDirectoryPath`, `modelName`.

| Event | When | Block? | Input / output |
|---|---|---|---|
| SessionStart | once per new session | annotate | out `injectSteps` |
| PreToolUse | before a tool step | **Block** | in `toolCall{name,args}`, `stepIdx`; out `decision` ∈ `allow/deny/ask/force_ask` (required), `reason`, `permissionOverrides`, `overwrite` (shallow arg rewrite) |
| PostToolUse | after a tool step | no ("Expects an empty JSON object `{}`") | in `toolCall`, `stepIdx`, `error` |
| PreInvocation | before the model is called | annotate | in `invocationNum`, `initialNumSteps`; out `injectSteps` (`systemMessage` / `userMessage` / `ephemeralMessage`) |
| PostInvocation | after tool calls finish | **can force continue or terminate** | out `injectSteps`, `terminationBehavior` ∈ `force_continue/terminate` |
| Stop | when the loop terminates | **Block stop** | in `executionNum`, `terminationReason`, `error`, `fullyIdle`; out `decision: "continue"` + `reason` |

Exit-code semantics: unknown (docs specify JSON on stdout only). Local state: `~/.gemini/config/` holds only
`mcp_config.json`, `projects`; no `hooks.json` present.

TypeScript: yes via command (`"command": "bun ./hooks/guard.ts"`). Note the memory note on agy headless traps
(soft-denied shell gives exit 0, empty output) — untested whether that affects hook processes.

## 4. Qwen Code (`qwen`)

- Version: `qwen --version` → `0.24.7` (verified). Package `~/.npm-global/lib/node_modules/@qwen-code/qwen-code`
  (Node bundle, `chunks/*.js`).
- `qwen --help` lists `qwen hooks  Manage Qwen Code hooks (use /hooks in interactive mode)`, `--safe-mode` "Disable
  all customizations (… hooks …)". `qwen hooks --help` printed nothing (exit 0) — noted, not investigated.

Event enum, verified (`chunks/chunk-GM463R2B.js`, `packages/core/src/hooks/types.ts`), 22 events:
PreToolUse, PostToolUse, PostToolUseFailure, PostToolBatch, Notification, UserPromptSubmit, UserPromptExpansion,
SessionStart, Stop, MessageDisplay, SubagentStart, SubagentStop, PreCompact, PostCompact, SessionEnd, SessionDelete,
PermissionRequest, PermissionDenied, StopFailure, TodoCreated, TodoCompleted, InstructionsLoaded.

Exit-code table, verified (`chunks/chunk-YHJFF7KH.js`, `getHookExitCodes`):
- **Exit 2 blocks**: PreToolUse "show stderr to model and block tool call"; UserPromptSubmit "block processing, erase
  original prompt…"; UserPromptExpansion "block expanded prompt submission…"; Stop "show stderr to model and continue
  conversation"; SubagentStop "…continue having it run"; PreCompact "block compaction"; TodoCreated / TodoCompleted
  "block … and show reason to model".
- PermissionRequest: "use hook decision if provided" (JSON).
- Annotate: PostToolUse / PostToolUseFailure / PostToolBatch "show stderr to model immediately"; SessionStart,
  SubagentStart stdout shown to Qwen/subagent ("blocking errors ignored").
- Fire-and-forget: MessageDisplay, SessionDelete, StopFailure. Observe: Notification, InstructionsLoaded, SessionEnd,
  PostCompact, PermissionDenied.
- Runner (verified, `chunk-GXSNGY5M.js`): `const isBlockingError = exitCode === 2;` stderr parsed as JSON when exit 2.

Hook types, verified (`getHookKey`): `command`, `http`, `function`, `prompt` (and `agent` in the enum).
Config, verified (settings schema in `chunk-OHKJVAKG.js`): `hooks` object in settings.json with one array per event
(`mergeStrategy: concat`), plus `disableAllHooks`, `stopHookBlockingCap` (env `QWEN_CODE_STOP_HOOK_BLOCK_CAP`).
Settings file locations `~/.qwen/settings.json` / `<repo>/.qwen/settings.json`: standard, not separately verified.
Local: `~/.qwen/settings.json` has no `hooks` key.
Payload names (verified present in bundle): `hook_event_name`, `transcript_path`, `tool_input`, `tool_response`,
`stop_hook_active`, `last_assistant_message`, `permissionDecision`, `updatedInput`, `additionalContext` — the
Claude Code dialect.

TypeScript: yes via command hook. `function` hooks are in-process JS but how to register one from outside (SDK only?)
is unknown.

## 5. DeepSeek Harness (`dsh`)

- Version: `dsh --version` → `0.2.0-rc.2` (verified). Package `@deepseek-ai/dsh` (Node); profiles under `~/.dsh/profiles/`
  (`headless`, `web`), each a `package.json` + `cordis.yml` + `cordis.patch.yml`.
- `dsh plugin --profile <name> <pnpm args>` installs plugins into a profile (verified, help).

Two kinds of hook point:

**(a) Hook bridges (command hooks), verified from installed READMEs:**
- `@deepseek-ai/dsh-hooks-claude-code`: mount in a profile with `configPath` (a Claude Code `hooks.json` or a settings
  file whose `hooks` key holds it), `pluginRoot`, `projectDir`, `defaultTimeoutMs` (600,000). Events and power, quoted:
  SessionStart "attach context"; UserPromptSubmit "block the prompt, or attach extra context"; PreToolUse "block the
  tool, or ask for approval"; PostToolUse "block the result with feedback, or attach extra context"; Stop "force
  another step with a reason"; SubagentStart "attach context … (in-process only)"; SubagentStop "observe only".
  Payload base `session_id`, `transcript_path` (always `''`), `cwd`, `hook_event_name`. "A hook that fails to run …
  is logged, and the agent continues" (fail-open).
- `@deepseek-ai/dsh-hooks-codex`: `configPath: ./.codex/hooks.json`; SessionStart, UserPromptSubmit, PreToolUse
  ("block the tool"), PostToolUse, Stop.
- **Not mounted** in the default `headless` profile: `dsh --profile headless --dump-default-config` lists ~90 plugins,
  none with "hook" in the name (verified). Using them needs a `cordis.patch.yml` entry (a config edit — not done).

**(b) Native Cordis extension points (in-process plugins), verified from `.d.ts`:**
- `tools/pre-execute` — "Allow, deny, cancel, or ask before dispatch" (`@mode waterfall`, `dsh-tools`).
- `tools/execute` — around-dispatch waterfall; `tools/post-execute` — "Accept, replace, enrich, or block a normalized
  dispatch result".
- `agent/pre-step` (waterfall, can reject), `agent/request`, `agent/request-error` (waterfall),
  `agent/turn-stopping` (serial; "a listener that objects steers (`agent.steer(...)`)" → forces another step),
  `agent/created` (serial), `agent/status`, `agent/assistant-stream`, `agent/error`, `agent/disposed` (emit = observe).
- `subagent/start`, `subagent/end`; `session/created`, `session/event`, `session/flush`, `session/disposed`.

TypeScript: via bridge command (`bun x.ts`) yes. A native plugin is an npm package loaded by Node 22 in the profile;
whether a `.ts` source loads directly is **unknown** (Node 22.22 needs a flag to strip types; not tested).

## 6. opencode (`opencode`)

- Version: `opencode --version` → `1.18.34` (verified). Binary `~/.opencode/bin/opencode` (Bun-compiled ELF).
- `--pure  run without external plugins` and `opencode plugin <module>  install plugin and update config`
  (verified, help).

Plugin loading, verified in the binary: glob `"{plugin,plugins}/*.{ts,js}"` over each config directory, plus the
config `plugin` array (npm specs, `./` paths, `file://`). Reported (https://opencode.ai/docs/plugins/):
`.opencode/plugins/` (project), `~/.config/opencode/plugins/` (global); "JavaScript or TypeScript files".
Plugins run **in-process** under Bun — TypeScript is native here.

Hook names actually triggered in 1.18.34 (verified, regex `\.trigger\("…"` over `strings`):
`chat.headers`, `chat.message`, `chat.params`, `command.execute.before`, `experimental.chat.messages.transform`,
`experimental.chat.system.transform`, `experimental.compaction.autocontinue`, `experimental.session.compacting`,
`experimental.text.complete`, `file.open`, `shell.env`, `tab.new`, `tool.definition`, `tool.execute.after`,
`tool.execute.before` (15). Plus `event` (every bus event, e.g. `session.idle`, `permission.asked`) and `config`.

Signatures, verified from `~/.config/opencode/node_modules/@opencode-ai/plugin/dist/index.d.ts` (package **1.14.24**,
older than the binary): `"tool.execute.before"(input:{tool,sessionID,callID}, output:{args})`;
`"tool.execute.after"(input:{tool,sessionID,callID,args}, output:{title,output,metadata})`;
`"chat.message"(input:{sessionID,agent?,model?,messageID?,variant?}, output:{message,parts})`;
`"experimental.compaction.autocontinue"` output `{enabled}`; `"permission.ask"(input, output:{status})`.

Blocking:
- `tool.execute.before`: block by throwing — **reported** (docs example `throw new Error("Do not read .env files")`).
  Code is consistent: `Plugin.trigger` awaits each hook in turn (`yield* v.promise(async()=>M(K,U))`), so a
  rejection propagates — my reading, not run. It can also rewrite `output.args`.
- `tool.execute.after`: can rewrite the output the model sees (annotate/replace).
- `event`: fire-and-forget (`v.sync(()=>{… V.event?.(…)})`, not awaited) → observe-only. So there is no blocking
  "Stop" hook; `session.idle` is observable only.
- `permission.ask` is declared in the 1.14.24 types but **no trigger for it exists in the 1.18.34 binary** (verified
  absence) — do not rely on it.

Local: `~/.config/opencode/opencode.jsonc` keys `$schema`, `permission`; no `plugin` key; no plugin directory.

## 7. Wrapper / stream points (observe, or kill the process)

Every harness can be wrapped by an outer bun process that reads a structured event stream (verified from help):
`claude -p --output-format stream-json --include-hook-events`; `codex exec --json` / `codex app-server`;
`agy -p --output-format stream-json` (+ `--input-format stream-json`); `qwen --json-fd/--json-file` (+ `--input-file`
for injected commands, `--max-tool-calls`, `--max-wall-time` exit 55); `opencode serve` (HTTP server, SSE events);
`dsh` SDK/ACP profiles. A wrapper sees events after the fact and can only stop the run, not veto one tool call — the
in-harness hooks above are the blocking points.

## What this does not establish

- No hook was installed or fired; every "can block" claim is from shipped text/schemas/code, not a run.
- Claude mod event list beyond the ones quoted was not enumerated per-event for block power.
- Codex config paths and trust flow are web-reported; agy exit-code semantics, dsh native-TS loading, and qwen
  `function`-hook registration are unknown.
- Hook-point counts are what I found; "~" counts are approximate.
