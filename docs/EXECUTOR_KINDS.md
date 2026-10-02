# Executor kinds — who can run a node

Written 2026-09-29 from one research session (three Sonnet 5.5 agents for Codex, three for `agy`) plus local
read-only checks. Nothing here has been run in a real workflow (n=0). What the research agents read from docs or
GitHub is marked *reported*; what was checked on this machine is marked *verified*.

A node in a workflow design (method 3.6) has a **role** (planner, coder, reviewer, classifier, …: what it does) and
an **engine** (who does the work) with an exact **model** and **effort**. Role and engine are chosen separately, and
the engine is named in the node, never left to a default. This file says what each engine is, what it is assigned
to, how it is called, how its failure shows, and the rules that keep mixed runs predictable. The method's
readiness step (3.1) proves each tool works; the canary below is that proof for these three.

## The four kinds (qwen added 2026-10-02; its canary has not run)

| | Claude subagent | Codex (GPT-6.1-sol) | Antigravity `agy` (Gemini) | Qwen Code `qwen` (OpenAI-compatible provider) |
|---|---|---|---| --- |
| Assigned to (EJ's view 2026-09-29, unmeasured) | orchestration, cheap research fan-out, glue | research and reports, coding and code generation, code review, finance, data extraction, workflow planning and design, web search | classification (Gemini 3.1 Pro) | nothing yet: EJ has not assigned it a role (no entry in the role map below) |
| Called by | the Agent or Workflow tool | plugin `codex@openai-codex` v1.0.6: `/codex:rescue`, `/codex:review`, `/codex:adversarial-review`; or `codex exec` from Bash | `agy -p "<prompt>"` from Bash | `qwen "<prompt>"` from Bash: the positional prompt is a one-shot run (`-p` is deprecated). **Any bare word is a prompt, not a subcommand**: `qwen models` sent a prompt (2026-10-02). Real subcommands: `auth` (removed), `batch`, `board`, `channel`, `extensions`, `hooks`, `mcp`, `review`, `sandbox`, `serve`, `sessions`, `update` (*verified* in `--help`) |
| Installed here | yes | yes, `codex` logged in with ChatGPT (*verified*; the canary records the version, it is not pinned here) | yes, `agy` at `~/.local/bin/agy` (*verified*); `agy models` returned a list, which suggests a working login (*inferred*) | yes, 0.24.7 at `~/.npm-global/bin/qwen` (*verified*). `~/.qwen/settings.json`: provider `openai` on an Alibaba token-plan endpoint, default `qwen3.8-max`, a key set (*reported*; validity and quota untested) |
| Default write access | per agent type | the plugin defaults to approvals "never" and sandbox read-only (`scripts/lib/codex.mjs:67-68`); rescue writes only because its agent adds `--write` (`agents/codex-rescue.md:34`) (*verified*) | workspace writes auto-allowed, shell soft-denied (*reported*) | approval mode `default`: file edits and shell need approval; headless, a tool needing approval fails (*reported*, docs) |
| Read-only form | read-only agent types | `codex exec -s read-only` (*verified* in `--help`). `-a/--ask-for-approval` exists only on top-level `codex`, not on `exec`, so put it before `exec` or omit it; untested | `--mode plan`; `--sandbox` for OS isolation (*reported*, flags *verified* in `--help`) | `--approval-mode plan`, "analyze only" (flag *verified* in `--help`; that it blocks writes is untested); `--sandbox` (*verified* flag) |
| Structured result | report returned to the caller | `--output-schema <file>`, `-o/--output-last-message <file>`, `--json` (*verified* in `--help`) | `--output-format json`, `--json-schema` (flags *verified*) | `--output-format json\|stream-json`; `--json-schema <json\|@file>` (headless; ends on the first valid `structured_output` call) (flags *verified* in `--help`; output shape untested) |
| Resume | SendMessage to the agent | `--resume-last` in rescue; `codex exec resume --last` (*verified* in `--help`) | `-c` or `--conversation <id>` (*verified* in `--help`) | `-c`, `-r <id>`, `--session-id`, `--fork-session` (*verified* in `--help`) |
| Reads which instruction file | `CLAUDE.md` | `AGENTS.md` (and `~/.codex/config.toml`) | `AGENTS.md` and `GEMINI.md`, third-party source only; `CLAUDE.md` not found (*uncertain*) | `QWEN.md` and `AGENTS.md` (constants in the installed 0.24.7 source; behaviour untested). `CLAUDE.md` is not among the filenames I found |
| Model source | the agent's `model` setting | `--model`/`--effort` (rescue, `exec -m`); `~/.codex/config.toml` when none is passed: `gpt-6.1-sol`, effort medium, plan-mode effort high (*verified* 2026-09-30). Do not rely on it; see "Model and effort" | `--model`; `agy models` lists what the plan offers, and it includes Claude models as well as Gemini, so "agy = Gemini" is a choice | `-m/--model`; otherwise `model.name` in `~/.qwen/settings.json` (`qwen3.8-max`, `reasoningEffort` xhigh, *reported*). `--fallback-model` for 429/503/529. A per-call effort flag was not found in `--help` (*unknown*), so effort comes from settings |
| Concurrency and native machinery | 20 concurrent subagents, nesting depth 3 (*reported* in Claude Code docs, v2.1.217+, env overrides exist; not measured here). Native: `--json-schema` (contract), `--max-budget-usd` (budget), `-w` (worktree isolation) (*reported*) | not recorded (*unknown*) | not recorded (*unknown*) | not recorded (*unknown*). Budgets: `--max-wall-time`, `--max-tool-calls`, `--max-session-turns` (exit 55 when exceeded), `--max-subagent-depth` default 5, `--worktree` (*verified* in `--help`) |

The assignment column is EJ's stated preference, recorded as such. The research found no head-to-head evidence for
or against it. The design treats it as a default that a node can override with a reason, and the first runs are
where it gets tested.

## Roles, engines, model and effort

Provisional map from EJ's assignments (unmeasured, n=0; a node may override with a reason). EJ, 2026-09-30:
**Codex defaults to `gpt-6.1-sol`; high thinking uses `gpt-6-astra`. `agy` defaults to Gemini 3.8 Flash; high
thinking uses Gemini 3.1 Pro.** Both names *verified* to exist here: `gpt-6-astra` in `~/.codex/models_cache.json`,
and the `agy models` ids below. Thinking level is chosen by picking the model, so the coder's "medium" effort is
what `gpt-6.1-sol` runs at when no other effort is passed.

| Role | Engine | Model, effort |
|---|---|---|
| Planner, and any node whose contract asks for high thinking | Codex | `gpt-6-astra` (the high-thinking model) |
| Coder | Codex | `gpt-6.1-sol`, default effort |
| Reviewer, verifier | Codex, fresh session, never the coder's | `gpt-6.1-sol`, default effort; `gpt-6-astra` when the review is a high-thinking one |
| Researcher | Codex (web search: see Open) | `gpt-6.1-sol`, default effort |
| Any other `agy` node | `agy` | `gemini-3.8-flash-medium` |
| Classifier | `agy` | `gemini-3.1-pro-high` (EJ's earlier assignment of classification to 3.1 Pro kept; see below) |
| Small task | the COO herself | her own model |

**Model and effort.**

- For `agy` the thinking level is part of the model id (`gemini-3.8-flash-low|medium|high`,
  `gemini-3.1-pro-low|high`; `agy models`). "Gemini 3.8 Flash" means `-medium` here, my choice, since EJ named no level.
  "Codex default effort" is what `~/.codex/config.toml` sets (medium); still pass it, so a config edit cannot change a run.
- Every Codex or `agy` call passes the model and the effort explicitly (`codex exec -m <model> -c
  model_reasoning_effort=<e>`, rescue `--model/--effort`, `agy --model`). The design names them in the node; the
  wrapper does not choose. Effort follows the role, not one global setting.
- The Codex plugin's own docs and rescue prompt use `gpt-5.4-mini`, `gpt-5.3-codex-spark` and a `gpt-5-4-prompting`
  skill as examples. Never copy a model name from them. A workflow that shows 5.4 or an unrequested high is traced to a
  call that left the model or effort out, or copied an example.
- The node's result records the model the tool reports. The COO fails the node if it is not the one the contract
  named. How `codex exec` and `agy` report the model in their output is not yet checked; the canary settles it
  (*unknown*).
- The names go stale (`gpt-6-sol` in this file already had; the list changes, so check `~/.codex/models_cache.json` and `agy models`). They live in the design's node blocks and the canary
  log, so a change is one edit and the canary shows what actually ran.

## The COO

The COO is the main Claude session, and the one fixed node in every design. Three jobs:

1. **Distribution.** Reads the state file, takes the next node the graph allows, writes its brief (role, engine,
   model, effort, contract, context) and dispatches it to a role subagent. The order comes from the design's edges,
   not from her preference. A departure from the design is a Log line with the reason.
2. **Monitoring.** Reads the state file: status, evidence paths, the reported model. She does not read the raw
   Codex or `agy` output; that would fill her context.
3. **Main review.** Accepts, sends back for repair, or escalates. She reviews the verdict and the evidence of an
   independent verifier (a fresh session, a different engine where possible, rule 5), not every diff. For a risky
   node she may spot-check the evidence.

She holds the stop conditions: attempt limits, tier exit, the executor-failure rule below, the model check. Role
subagents only report status. Her picture of the run lives in the state file, so a fresh session can take over.

**When she does a node herself.** All four must hold:

- the problem, the fix and the check are each one sentence (the test for skipping a workflow, method 2);
- it fits in a few files and a few tool calls without bloating her context;
- it is reversible and touches no live system, running agent or shared state (Rule 6 applies whoever does it);
- the check is a command whose output she records, not "it looks right".

Otherwise she dispatches it. It is recorded in the state file as a node with engine "COO", like any other.

**The cap.** If she passes **8 tool calls** on one node, she stops and dispatches it. The 8 is my provisional number,
not measured; EJ sets it. The guard exists because doing everything herself feels faster and turns the design back
into one large session.

## How a failure shows

The rule for every kind: a node is done only when its **result file exists and passes its check**. An exit code is
never the check on its own.

| Kind | Signals | Trap |
|---|---|---|
| Claude subagent | error or no report | quota behaviour not seen yet (*unknown*) |
| Codex | exit code and stderr from `codex exec`; `/codex:status` for jobs | the rescue subagent returns nothing if Codex fails to start; a missing turn id can hang a job forever (plugin issue #781); quota-exhausted behaviour not seen (*unknown*) |
| `agy` | exit 0 ok, 1 error, 2 cancelled; json `status` | a tool needing approval is soft-denied and the run still exits 0 (stderr notice only); `-p` can hang with no TTY (issue #318); it stops on quota, spend cap or credits with no known code (*unknown*) |
| `qwen` | exit code (55 = a `--max-*` budget hit); json result under `--output-format json` | a bare word is a one-shot prompt that spends quota; headless, a tool needing approval fails; other exit codes, quota-exhausted behaviour and hang-without-TTY not seen (*unknown*) |

So every external call gets an outside timeout (for `agy` also `--print-timeout`, default 0 = wait forever), and an empty or missing result file counts as a failure.

## The canary piece

A preparation piece at the front of any run that uses Codex, `agy` or `qwen` (readiness, method 3.1). One tiny task per
kind, with an answer that can be checked:

1. Ask for a fixed thing: write `OK` to `runs/<runId>/canary/<kind>.txt`, or return `{"ok": true}` with the schema
   flag.
2. Run it under a 60–90 second timeout.
3. Record the tool's version in the state file. Pass only if the exit code is right, the file exists with exactly that content, stderr has no approval-denied
   or quota notice, and for `agy` the json `status` is success.
4. The canary node returns `pass`, `fail` or `timeout` with the reason to the script, and the state file records it.
   The scheduler (the script or the COO), not the state file, decides which kinds the graph may use.
   Format, one Log line per kind: `canary <kind> <version> pass|fail|timeout: <reason>`.
5. Sabotage check (house rule): once, run an impossible task and confirm the canary reports `fail`. Until that has
   been done, the canary is not known to be able to fail.

**`qwen` form (written 2026-10-02, not run).** `qwen --approval-mode plan --max-tool-calls 0 --max-wall-time 90s
--json-schema '{"type":"object","required":["ok"],"properties":{"ok":{"const":true}}}' --output-format json -m <model>
"Return ok true."` Pass: exit 0, a valid structured result with `ok: true`, no tool call made, stderr without an
approval or quota notice, and the model the tool reports equals `<model>`. Sabotage: the same call with
`--max-wall-time 1s` must end exit 55 and the canary must report `fail` or `timeout`. Never probe qwen with a bare word.

It does not prove quota left, output quality, or that the tool stays inside its workspace. Each canary spends a
little usage, so it runs once per run, and the person's go-ahead for the run covers it. Open: whether to re-check
before long jobs.

## When a kind fails mid-run (n=0, this file only)

A timeout, an empty result or a quota stop is a failure of the executor, not a failed attempt, so it does not count
against the node's attempt limit. The node reruns once as a fresh node on the fallback kind named in its design,
with a short handoff note. With no fallback, or on a second failure, the node is blocked and goes to EJ. Write a
Log line for each: `<node> executor-fail <kind>: <reason>`.

## Rules for mixed runs

1. **One writer at a time.** Two kinds never write to the same tree at once. A writing node of another kind gets its
   own `git worktree` and branch, and its result comes back as a diff that a verifier checks. Reviews and
   classification nodes are read-only.
2. **Read-only unless the contract says write.** Codex rescue and `agy` both can write by default; the node's
   contract names read-only or write, and the call is made with the matching flags.
3. **Never `--dangerously-skip-permissions` on `agy`.** Reported to defeat `--sandbox` and write outside the
   workspace (issue #36). Add specific allow rules instead.
4. **Handoff between kinds is the tier exit of method 3.5.** A piece that one kind could not finish goes to a fresh
   node of another kind with a short note (piece, check, last feedback), never a switch inside a running session.
   Which kind counts as "cheaper" is not measured; EJ decides the order per task.
5. **The independent verifier is a different kind from the worker when it can be.** The reason is different blind
   spots, which is *claimed* across many blogs and measured nowhere. It is a cheap way to get blindness, not a
   proven one.
6. **The stop-time review gate stays off.** Reported problems: re-blocks the same finding with no deferral (#790),
   cannot pin model or effort (#769), spends Codex usage on every stop.
7. **Instruction files.** `agy` is not known to read `CLAUDE.md`. A node run by `agy` gets its rules in the prompt
   or in `AGENTS.md`, never assumed from `CLAUDE.md`.
8. **External kinds are called through a Claude wrapper.** The COO (or a Workflow script) schedules nodes
   (method 3.6); a Codex or `agy` node runs as a role subagent that builds the prompt, makes one Bash call with the
   model and effort the brief names, and writes the result file. That costs Claude tokens on every such node, and
   the wrapper sees the worker's output, so the wrapper is never that node's verifier.

## Open before relying on this

- Google's terms may bar calling `agy` headless from another tool on an individual account (§6 of the Antigravity
  Additional Terms, asked on the Google AI developer forum, unanswered). Resolve before automating on it.
- Web search is assigned to Codex, but `--search` is listed only on top-level `codex`, not on `codex exec`. How to
  enable it non-interactively is unknown.
- Remaining usage cannot be read by the workflow for any of the four kinds; only failure is visible. Design for
  clean stops, not for percentages. Unchecked: Codex `/status` in the TUI, `agy` `/credits`.
- `qwen`: the canary above is written, not run. Open: whether `--json-schema` returns valid output on this token plan,
  whether `plan` mode blocks writes, whether `AGENTS.md` is read, what it costs per call, and whether the key is valid.
- `agy` headless behaviour on quota exhaustion, and whether `agy` logs in non-interactively here, are untested.
- Pricing for `agy` comes only from SEO pages that disagree; model lists conflict between blogs (trust `agy
  models`).
- `codex mcp-server` was removed per OpenAI's docs; community pages that use it are out of date. The plugin and
  `codex exec` are the supported routes.
- The Codex plugin has many open issues (leaked brokers, hooks growing `CLAUDE_ENV_FILE`, hangs). Treat it as
  fragile and run the canary first.
- Sources: `github.com/openai/codex-plugin-cc`, `learn.chatgpt.com/docs/*` (was developers.openai.com/codex),
  `antigravity.google/docs/cli/*`, `github.com/google-antigravity/antigravity-cli` issues #36, #318, #1095.
