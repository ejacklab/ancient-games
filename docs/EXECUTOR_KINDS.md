# Executor kinds — who can run a node

Written 2026-09-29 from one research session (three Sonnet 5.5 agents for Codex, three for `agy`) plus local
read-only checks. Nothing here has been run in a real workflow (n=0). What the research agents read from docs or
GitHub is marked *reported*; what was checked on this machine is marked *verified*.

A node in a workflow design (method 3.6) has a **role** (planner, coder, reviewer, classifier, …: what it does) and
an **engine** (who does the work) with an exact **model** and **effort**. Role and engine are chosen separately, and
the engine is named in the node, never left to a default. This file says what each engine is, what it is assigned
to, how it is called, how its failure shows, and the rules that keep mixed runs predictable. The method's
readiness step (3.1) proves each tool works; the canary below is that proof for these three.

## The four kinds (qwen added 2026-10-02; canary passed once, n=1)

| | Claude subagent | Codex (GPT-6.1-sol) | Antigravity `agy` (Gemini) | Qwen Code `qwen` (OpenAI-compatible provider) |
|---|---|---|---| --- |
| Assigned to (EJ's view 2026-09-29, unmeasured) | orchestration, cheap research fan-out, glue | research and reports, coding and code generation, code review, finance, data extraction, workflow planning and design, web search | classification (Gemini 3.1 Pro) | nothing yet: EJ has not assigned it a role (no entry in the role map below) |
| Called by | the Agent or Workflow tool | plugin `codex@openai-codex` v1.0.6: `/codex:rescue`, `/codex:review`, `/codex:adversarial-review`; or `codex exec` from Bash | `agy -p "<prompt>"` from Bash | `qwen "<prompt>"` from Bash: the positional prompt is a one-shot run (`-p` is deprecated). **Any bare word is a prompt, not a subcommand**: `qwen models` sent a prompt (2026-10-02). Real subcommands: `auth` (removed), `batch`, `board`, `channel`, `extensions`, `hooks`, `mcp`, `review`, `sandbox`, `serve`, `sessions`, `update` (*verified* in `--help`) |
| Installed here | yes | yes, `codex` logged in with ChatGPT (*verified*; the canary records the version, it is not pinned here) | yes, `agy` at `~/.local/bin/agy` (*verified*); `agy models` returned a list, which suggests a working login (*inferred*) | yes, 0.24.7 at `~/.npm-global/bin/qwen` (*verified*). `~/.qwen/settings.json`: provider `openai` on an Alibaba token-plan endpoint, default `qwen3.8-max`, a key set (*reported*; validity and quota untested) |
| Default write access | per agent type | the plugin defaults to approvals "never" and sandbox read-only (`scripts/lib/codex.mjs:67-68`); rescue writes only because its agent adds `--write` (`agents/codex-rescue.md:34`) (*verified*) | workspace writes auto-allowed, shell soft-denied (*reported*) | approval mode `default`. Headless, the write and shell tools are not offered to the model at all: it reports it cannot write and the run exits 0 with no file (*verified* 2026-10-02, one run) |
| Read-only form | read-only agent types | `codex exec -s read-only` (*verified* in `--help`). `-a/--ask-for-approval` exists only on top-level `codex`, not on `exec`, so put it before `exec` or omit it; untested | `--mode plan`; `--sandbox` for OS isolation (*reported*, flags *verified* in `--help`) | `--approval-mode plan`, "analyze only" (flag *verified*; *verified* 2026-10-02 that plan mode withholds the write and shell tools: no files appeared, with a yolo control that did write them. Blocked by absence, not by a denied attempt); `--sandbox` (*verified* flag) |
| Structured result | report returned to the caller | `--output-schema <file>`, `-o/--output-last-message <file>`, `--json` (*verified* in `--help`) | `--output-format json`, `--json-schema` (flags *verified*) | `--output-format json\|stream-json`; `--json-schema <json\|@file>` (headless; ends on the first valid `structured_output` call) (flags *verified* in `--help`; output shape untested) |
| Resume | SendMessage to the agent | `--resume-last` in rescue; `codex exec resume --last` (*verified* in `--help`) | `-c` or `--conversation <id>` (*verified* in `--help`) | `-c`, `-r <id>`, `--session-id`, `--fork-session` (*verified* in `--help`) |
| Reads which instruction file | `CLAUDE.md` | `AGENTS.md` (and `~/.codex/config.toml`) | `AGENTS.md` and `GEMINI.md`, third-party source only; `CLAUDE.md` not found (*uncertain*) | `QWEN.md` and `AGENTS.md` (*verified* 2026-10-02: each planted marker was answered with no tool call). `CLAUDE.md`: the probe got an off-task reply, so *unknown*; it is not among the filenames in the 0.24.7 source |
| Model source | the agent's `model` setting | `--model`/`--effort` (rescue, `exec -m`); `~/.codex/config.toml` when none is passed: `gpt-6.1-sol`, effort medium, plan-mode effort high (*verified* 2026-09-30; still the working default — see the correction below for the one path where it fails) | `--model`; `agy models` lists what the plan offers, and it includes Claude models as well as Gemini, so "agy = Gemini" is a choice | `-m/--model`; otherwise `model.name` in `~/.qwen/settings.json` (`qwen3.8-max`, `reasoningEffort` xhigh, *reported*). `--fallback-model` for 429/503/529. A per-call effort flag was not found in `--help` (*unknown*), so effort comes from settings |
| Concurrency and native machinery | 20 concurrent subagents, nesting depth 3 (*reported* in Claude Code docs, v2.1.217+, env overrides exist; not measured here). Native: `--json-schema` (contract), `--max-budget-usd` (budget), `-w` (worktree isolation) (*reported*) | not recorded (*unknown*) | not recorded (*unknown*) | not recorded (*unknown*). Budgets: `--max-wall-time`, `--max-tool-calls`, `--max-session-turns` (exit 55 when exceeded), `--max-subagent-depth` default 5, `--worktree` (*verified* in `--help`) |

The assignment column is EJ's stated preference, recorded as such. The research found no head-to-head evidence for
or against it. The design treats it as a default that a node can override with a reason, and the first runs are
where it gets tested.

## Roles, engines, model and effort

Provisional map from EJ's assignments (unmeasured, n=0; a node may override with a reason). EJ, 2026-09-30:
**Codex defaults to `gpt-6.1-sol`; high thinking uses `gpt-6-astra`. `agy` defaults to Gemini 3.8 Flash; high
thinking uses Gemini 3.1 Pro.** Thinking level is chosen by picking the model, so the coder's "medium" effort is
what the default runs at when no other effort is passed.

**Correction, 2026-10-03 — the DSH Codex provider bundles an old Codex, and that alone is why a model failed.** A
first reading of this section claimed `gpt-6.1-sol` was dead and had gone stale. **That was wrong.** `codex exec
-m gpt-6.1-sol -c model_reasoning_effort=high` answers normally on the CLI here (*verified* 2026-10-03,
`codex-cli 0.160.0`), and that CLI's own `codex debug models` lists ten models including `gpt-6.1-sol` at
`visibility: list`. The failure came from a *different binary*: the DeepSeek Harness's Codex subagent provider
spawns its own bundled `@openai/codex@0.153.4`, whose catalog has seven models and no `gpt-6.1-sol`. Naming it
there answers HTTP 400 *"The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account"* —
**the error blames the account when the real cause is the client version.** `~/.codex/models_cache.json` agreed
with the CLI, so it is not a lagging source either; the bundled binary was the stale thing.

Two consequences. On the **CLI and `dispatch.py`** the defaults stand unchanged: `gpt-6.1-sol`, high thinking on
`gpt-6-astra`. On the **DSH subagent provider** the model is currently pinned to `gpt-5.6-sol`, because that is
what its bundled 0.153.4 can serve — `subagent_codex` runs, and its canary reported *"GPT-5 Codex"*. The real fix
is to align the provider's bundled Codex version, after which the pin returns to the default; until then the two
paths genuinely differ and the DSH row is the exception. **Lesson: when a model 400s, check which binary asked.**

| Role | Engine | Model, effort |
|---|---|---|
| Planner, and any node whose contract asks for high thinking | Codex | `gpt-6-astra` (the high-thinking model) |
| Coder | Codex | `gpt-6.1-sol`, high effort (*verified* 2026-10-03 on the CLI) |
| Reviewer, verifier | Codex, fresh session, never the coder's | `gpt-6.1-sol`, default effort; `gpt-6-astra` when the review is a high-thinking one |
| Researcher — docs, papers, web (method 3.8 item 9) | `subagent_researcher` on the DeepSeek Harness (web search and fetch in its tool filter); `agy` by rule 2 above; a Claude subagent on Claude Code | `deepseek-flash`, low; `agy` per its own row; the session model on Claude Code |
| Explorer — existing code, read-only (method 3.8 item 10) | `subagent_explorer` on the DeepSeek Harness: read-only, `bash` allowed so a claim can be marked `ran`, no `write` or `edit`; the COO herself when the affected area is small | `deepseek-flash`, low; EJ, 2026-10-03, n=0 |
| Any other `agy` node | `agy` | `gemini-3.8-flash-medium` |
| Classifier | DeepSeek (`subagent`, kind `deepseek`) | `deepseek-flash` — EJ, 2026-10-04: "multi step planning, classification, is using Deepseek v4.1 flash". This row said `agy`/`gemini-3.1-pro-high` and contradicted the routing table below it and line 146; corrected 2026-10-05 (register 4.4) |
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
- The names go stale — `gpt-6-sol` did. But a 400 is not proof of staleness: see **"The bundled-runtime trap"**
  below before changing a name. The names live in the design's node blocks and the canary log, so a change is one
  edit and the canary shows what actually ran.

## The bundled-runtime trap

**A model that fails may be failing because of the client — not the model, the account or the permission mode. Ask
which binary made the call, and what version it is.** An engine reached through a provider may be a *bundled* copy,
older than the copy on `PATH`, and the two do not accept the same model names. The error names the model, or the
account, and never the version, so it sends you to fix the wrong thing. This has cost three diagnoses in two days:

| When | What actually ran | On `PATH` | Symptom | Cause |
|---|---|---|---|---|
| 2026-09-30 | `gpt-6-sol`, named in this file | — | the name did not exist | a stale name — the plain case |
| 2026-10-03 | the DSH Codex provider's bundled `@openai/codex@0.153.4` | `codex-cli 0.160.0` | 400 *"The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account"* | the bundled catalog has seven models and lacks it; the CLI's has ten and runs it with high effort |
| 2026-10-03 | the DSH Claude Code provider's bundled Claude Code **2.1.263** (via `@anthropic-ai/claude-agent-sdk@0.3.263`) | Claude Code **2.1.289** | 400 *"Claude Code 2.1.263 does not support this model; version 2.1.280 or later required"* | Opus 5.5 needs CC ≥ 2.1.280. Sonnet 5.5 runs on 2.1.263, so this is per-model version gating, not a blanket "too old" |

Both DSH cases first read as *"the model is dead"*. Neither model was dead. In the Codex case this file's sibling
table in `TASK_TYPES.md` was edited to a different model before the real cause was found; that edit is reverted,
and it is why this section exists.

**The checks, in order.**

1. Run the engine's own catalog command **for the binary that will make the call** — `codex debug models`,
   `agy models`, `claude --version`. Not for the engine in general: a bundled provider copy answers differently,
   and its answer is the one that matters.
2. Read the error for a *version*, not only for a model or an account. "does not support this model; version X or
   later required" is a version statement wearing a model's clothes.
3. Before concluding a model is dead, run the same id on the CLI. **If the CLI works, the bundled client is the
   problem.**
4. The fix is normally to align the bundled client — the provider's pinned dependency — not to change the model.
   Until it is aligned, the CLI route (`dispatch.py`) can use the model the provider cannot, which is how Opus 5.5
   is reachable today.

**A canary must record the version of the binary that ran**, not the version on `PATH`, or the two are
indistinguishable in the log — which is how a provider's stale client stays invisible across runs.

## Routing: which category goes to which engine

Agreed with EJ, 2026-10-03, in three sentences: **Codex** for coding, debugging, code review and unit tests;
**`agy`** for research (web and document fetch), exploring a codebase, and generating configuration files and
folder structure; **Claude Code** for complex debugging and root-cause analysis, code review, and algorithm and
solution design. This section is those sentences turned into a table — and then measured against the prompt corpus
that already exists, because three sentences do not say what happens to the work they never mention.

**What the sentences cover** (`tests/fixtures/operator_prompts_r1–r3.jsonl`, 300 labelled prompts, measured
2026-10-03; the labels are the COO's own, provisional per `TASK_TYPES.md`):

| | Prompts | Share |
|---|---|---|
| **Clean** — every category in the prompt maps to exactly one engine | 160 | 53% |
| **One true collision** — `code review`, claimed by both Codex and Claude Code | 20 | 7% |
| **Uncovered** — a category no sentence names, with no collision | 108 | 36% |
| **No category** (tiny) — correctly routed nowhere | 12 | 4% |

Every other apparent overlap was a legitimate pipeline: `agy` then Codex (×10) and Claude Code then Codex (×4)
route piece by piece, which is what a combination pipeline is for. Only a *single* category claimed by two engines
is a real collision, and there is exactly one.

**The collision is resolved by rule 5, not by picking a winner.** `code review` is claimed by both Codex and
Claude Code. Rule 5 above already says the independent verifier is a *different kind* from the worker, so the
reviewer is the other engine: Codex-built work is reviewed by Claude Code, Claude-Code-built work by Codex. That
depends on who built the thing rather than on the category, which is why it cannot collide.

**The gaps, and who takes them.** Of the 110 prompts containing at least one uncovered category (the 108 above plus
2 that also carry a collision), 78 are read-only (`builds: false`) and 32 write. Read-only prose, extraction,
classification and grading are cheap work — they go to the DeepSeek-native roles, not to a Codex or Claude Code
call.

**One row per `TASK_TYPES.md` category — the same 16, no more and no fewer.** The table is keyed by category so
an engine decision cannot be confused with a rule phrase again. Until 2026-10-04 four of its rows named things that
are **not** categories, which is exactly how EJ's instruction about `multi step planning` came to read as an override
of rule 3.

| Category | Engine | Basis |
|---|---|---|
| `classification` | `subagent_researcher` — DeepSeek `deepseek-flash`, low | EJ, 2026-10-04 |
| `code generation` | opencode **and** codex, split by `scripts/workload.py` | rule 1; the split gives opencode priority |
| `code review` | the engine that did **not** build it | rule 5; risk-tiered — Sonnet 5.5 when nothing builds |
| `debugging` | opencode **and** codex split for the fix; **Opus 5.5** when it is complex debugging or root-cause analysis | rule 1, plus rule 3's escalation. The phrase *"complex debugging and root-cause analysis"* is rule 3's wording, not a category, and it lives in **this** row |
| `document and explain` | `subagent_claude_code_sonnet` — Sonnet 5.5 | `TASK_TYPES.md` assigns it there |
| `grade a run` | `subagent_claude_code_sonnet` — Sonnet 5.5 | same |
| `information extraction` | `subagent_researcher` — `deepseek-flash`, low | EJ, 2026-10-04 |
| `multi step planning` | DeepSeek `deepseek-flash` | EJ, 2026-10-04 |
| `others` | **nothing chosen** — the catch-all names no engine in `TASK_TYPES.md` and has no routing decision | **open**; 12 claims, 3.4% of the corpus |
| `repo scanning` | `agy` **via `dispatch.py`** | rule 2, *"exploring a codebase"*; EJ, 2026-10-04 |
| `research and reports` | `agy` **via `dispatch.py`** | rule 2; EJ, 2026-10-04 |
| `test cases gen` | opencode **and** codex, split | rule 1; the split |
| `test data gen` | `subagent_claude_code_sonnet` — Sonnet 5.5 | `TASK_TYPES.md`'s own cheap-tier row |
| `test script gen` | opencode **and** codex, split | rule 1; the split |
| `ui/ux dev` | opencode **and** codex, split | rule 1; the split |
| `web search` | `agy` **via `dispatch.py`** | rule 2; EJ, 2026-10-04 |

**Phrases from the three sentences that are *not* categories.** Rule 3 and rule 2 name work that `TASK_TYPES.md` has
no row for. It is kept here rather than given a row above, because a phrase sitting in the category table is what
caused the confusion in the first place:

| Phrase (source) | What it attaches to | Engine |
|---|---|---|
| *"algorithm and solution design"* (rule 3) | **no category.** `multi step planning` is the nearest and EJ put that on `deepseek-flash` (2026-10-04), so this phrase has nowhere to land | Opus 5.5 when it is invoked — **open** |
| *"configuration files, folder structure"* (rule 2) | **no category.** It is two pieces: *design* (`multi step planning`) and *generation* (`code generation`) | `agy` by rule 2 — **open** |
| *"other more daily tasks use Sonnet 5.5"* (EJ, 2026-10-03) | a **tier rule, not work**: anything Claude does that rule 3 does not claim runs on Sonnet 5.5 | `subagent_claude_code_sonnet` |


**The split is already near even, and a run-time balance is not available anyway.** EJ asked on 2026-10-03 whether
heavy Codex use could divert about 30% of the work to Sonnet 5.5. Measured over the 300-prompt corpus, this table
with `test data gen` corrected puts **Codex at 28.5%, Claude at 29.6% and `agy` at 27.6%** of category claims — so
the mix is close to even before any balancing rule, and a rule would move little. Two things block the run-time
version: remaining usage **cannot be read** for any engine (see "Open before relying on this"), so "when Codex is
heavily used" is not a condition anything can evaluate; and `DISPATCHER_DESIGN.md` §5 records EJ's decision that
there is **no run-time routing fork** — the plan names one engine per node and the dispatcher makes no choice. A
deterministic design-time split, written into the plan, does fit those rules — and as of 2026-10-04 it is built:
see the next paragraph. The corpus is also only a proxy — billing-domain prompts skewed toward
research and scanning — so Codex's real share depends on what the work actually is, and `events.jsonl` records
every node's engine so the real mix can be reconciled per run.

**Built 2026-10-04: the design-time split is `scripts/workload.py` — opencode has priority on build work.**
Engines are assigned while the plan is written, so the plan still names one engine per node and §5's "no run-time
routing fork" is untouched. The split is by **module**, not by node count: a module's code and its tests are placed
together, and the tests go to the engine that did *not* write the code wherever the budget allows. That is
independent test authoring, which today's single-engine runs do not get at all.

**The default is the smallest lead that counts as priority, not a fixed ratio** (EJ, 2026-10-04: *"I know it is
very hard to be like 60% 40%, so give priority the opencode more will do"*). Each self-tested module moves two nodes
to the primary engine, so the minimum lead is (N+1)/2N:

| modules | opencode | self-tested |
|---|---|---|
| 3 | 67% | 1 of 3 |
| 5 | **60%** | 1 of 5 |
| 10 | 55% | 1 of 10 |
| 20 | 52.5% | 1 of 20 |

So the 60/40 first asked for is not hard to hit — **at five modules it *is* the minimum lead**, and it costs a
single module its independent tests. Demanding 60% on a 20-module plan would cost 4 of 20 rather than 1 of 20, so
the default takes the cheap end and `--share` forces the larger lead when it is wanted.

**Full independence is available at exactly 50/50 and nowhere else** — crossing every pair sends one node to each
engine, whatever pattern the primaries follow. An even split therefore has *no* priority, which is the trade the
default chooses against, and `check()` reports it rather than letting it pass silently.

`workload.py` is deterministic (sorted by module id, so a re-serialized plan does not silently move a node),
`--write` records the engines into the plan with an `engine_assigned_by` note so a reader can tell an assigned
engine from a chosen one, and `check()` requires that opencode **leads**, then judges self-testing against the lead
actually achieved — so a plan that self-tests more than its lead costs is refused, as is one whose verifier runs the
same engine as the node it verifies (rule 5).

**The basis is n=1.** One POC run of opencode scored 19/19 (`runs/20261004-opencode-poc/README.md`) — strong, but
one run, on a toy repo. This is a policy, not a measurement. The first split run's ledger row is what compares codex
and opencode on the same work.

**Where each engine lives on the DeepSeek Harness** (main environment as of 2026-10-03). **The CLI comes first and
the provider tool is the fallback** — see the rule under the table.

| Engine | Model, effort | First choice | Fallback |
|---|---|---|---|
| Codex | `gpt-6.1-sol`, high for building | `dispatch.py`, engine `codex` — the PATH `codex-cli` serves the model | `subagent_codex`, whose bundled Codex 0.153.4 cannot, so that row pins `gpt-5.6-sol` |
| Claude Code, design tier | `claude-opus-5-5` | `dispatch.py`, engine `claude` — **the only route that reaches Opus 5.5 today** | `subagent_claude_code` cannot: bundled Claude Code 2.1.263, and Opus 5.5 needs ≥ 2.1.280 |
| Claude Code, daily tier | `claude-sonnet-5-5` | `dispatch.py`, engine `claude` | `subagent_claude_code_sonnet` — works on 2.1.263 |
| DeepSeek flash tier | `deepseek-flash`, low | `subagent_researcher`, `subagent_explorer` — **the exception**: a spawn role is the only form whose `toolFilter` the harness enforces | `dispatch.py`, engine `dsh` (`dsh headless`) |
| DeepSeek strong tier | `deepseek-v4-pro`, high | `subagent_coder`, `subagent_verifier` — same reason | `dispatch.py`, engine `dsh` |
| `agy` | `gemini-3.8-flash-medium` and up | `dispatch.py`, engine `agy` | none — no provider exists, so this is CLI-only |
| `opencode` + MiniMax | `minimax-coding-plan/MiniMax-M3.1-Flash-Preview` | `dispatch.py`, engine `opencode` | `claude` / `claude-sonnet-5-5` — the engine default; no DSH provider for opencode exists |

**CLI first, provider call as the fallback (EJ, 2026-10-04).** *"AI changes fast, same as all these AI tools, so
better use the cli call."* The binary on `PATH` is the one that updates — `codex-cli 0.160.0`, Claude Code
2.1.289 — while a provider pins an older bundled copy (0.153.4, 2.1.263) and will not use `PATH` even if asked.
That is deliberate, not an oversight: the Codex provider's own docstring says *"Fixed package-local app-server
command, independent of the host `PATH`"*, and the Claude Agent SDK resolves its own native binary unless
`pathToClaudeCodeExecutable` is passed — which the provider never does, and no environment variable redirects it
(checked: the `CLAUDE_CODE_*` surface carries certs, entrypoint, OAuth and plugin paths, no executable). So the CLI
is not merely preferred; it is the route whose version tracks the tool, which is what makes it the safer default
while these tools move this fast.

**Is there anything only a provider call can do?** Nothing that cannot be shelled out at all — `bash` can always
run the CLI. But three things it does materially better, which is why it stays as the fallback rather than being
dropped:

1. **No wrapper turn.** A CLI node costs the COO a turn that re-reads her whole context (method 3.8; §8's wrapper
   cost). A provider call is a direct delegation.
2. **The child is a real harness session.** It appears in the session list, carries a session log, and its
   projection cache is what `harvest_run.py` reads for the ledger's Actual cost. A CLI call leaves only
   `dispatch.py`'s own runlog, so its cost stays invisible to the ledger unless that engine harvests it separately.
3. **Harness-enforced properties** — `toolFilter` per role, `ctx.tools.restrict` per agent, and cancellation tied
   to the turn rather than to a timer the caller owns.

**One case where this is correctness, not preference:** a node that must be **read-only or blind** — a verifier
above all — belongs in a **spawn provider call**, because its `toolFilter` is enforced by the harness. A CLI call
has no such mask: whatever `bash` can reach, that node can run. So the rule is *CLI by default, spawn tool where
blindness has to be structural*.

**`opencode` with MiniMax-M3.1-Flash-Preview: the strongest frontend and long-context results measured here so
far.** Added 2026-10-04, n=1 (one run: `runs/20261004-opencode-poc/README.md`). **19/19 objective checks** across
six POCs — a self-contained ARIA-tabbed page with an inline SVG chart, rendered in Chrome to confirm it (9/9,
29 s); three needles across a **197k-token** file with their sum, exact, in **14 s**; a bar chart read correctly
from an image; a failing pytest suite diagnosed to `calc.py:6`, fixed, and the tests passing; and `--agent plan`
refusing to write at all.

**Two traps, both silent, both verified.** The message must come before any `--file=`: `-f` is a greedy array
option that swallows the next positional, so a file-first call makes opencode read the *prompt* as the attachment
path (`File not found: <the prompt>`). And an attachment it cannot read makes it **exit 1 even when the task then
succeeds** — P4 answered correctly and still returned 1, reproducibly — which `dispatch.py` reads as an executor
failure *before* it parses stdout. The adapter therefore emits no `-f`, and a node reads its own inputs.

Video is advertised in the model catalog but the read path answers `Cannot read binary file`; the agent recovered
by running `ffprobe` then `ffmpeg -vsync 0` to extract frames and reading those. `--format json` reports real
`tokens` and `cost` per step — the best cost source wired in so far, and a candidate for the ledger's Actual cost
column, which currently says "not instrumented" for DSH runs. Not built.

Routing is **not** changed by this: the evidence argues for `ui/ux dev`, `document and explain` and long-document
`information extraction`, but moving a category is EJ's call, and one run is n=1.

**Evidence per row, and what is not evidence.** The two external rows each passed one canary on 2026-10-03 — a
two-line answer with no tools, which shows the provider authenticates and completes a turn, nothing more. The
flash/v4-pro tiers were verified from the harness's own session records (`modelSelection.lastUsed`), and the
read-only filter by asking a child what it had. **None of this table has been exercised on real work**: it is a
measured policy, not a measured outcome. Two specific unknowns: whether an external provider honours a `persona` or
a `toolFilter` is untested, so those rows carry neither; and a `toolFilter` cannot remove a *scoped* registration,
so a child still has the `subagent` tool and depth is held by `maxDepth` instead — also untested.

## The COO

The COO is the main session of whichever harness is running — the DeepSeek Harness as of 2026-10-03, Claude Code
before that — and the one fixed node in every design. Planning and monitoring stay hers: a delegated child returns
only its final result, so no engine below ever takes the lead. She is the leader: she gives
directions, holds the budget and accepts results. **Planning and algorithm design are hers, on the strongest
model** (EJ, 2026-10-03); bulk coding goes to the cheaper coder (method 3.5 tier rule), and she codes only when the
work fits her context and a hand-off would not pay. She does not do the small work, and she does not carry its
details (EJ, 2026-10-02; n=0). The vision, the requirements and every approval stay EJ's. Three jobs:

1. **Directions.** Reads the state file, takes the next node the graph allows, writes its brief (role, engine,
   model, effort, contract, context) and dispatches it. The order comes from the design's edges, not from her
   preference. A departure from the design is a Log line with the reason. The brief and contract are how knowledge
   passes to a worker: written down, not narrated step by step. This is where the stronger model's skill goes: every
   brief carries a template, a worked example and the standard the result is judged by (method 3.8;
   `docs/workflow-templates/node-brief.md`), so the worker needs no guessing and she never rewrites a result.
2. **Budget.** Enforces the ceiling EJ sets: attempt limits, timeouts, the cost ceiling, the tier exit, the
   executor-failure rule below and the model check. (The "5 roles and 3 at once" caps were deleted 2026-10-05 at
   EJ's direction — see method 3.7; they had re-labelled the spike rule's numbers as a role cap. The dispatcher
   still runs at most `MAX_WORKERS` nodes at a time — a pool size, and it takes its number from the harness's
   `@deepseek-ai/dsh-subagent` `maxActiveSubagents`, default 8, not from a preference.)
   When the next step would pass the ceiling she stops and reports;
   she never raises it herself.
3. **Acceptance.** Accepts, sends back for repair, or escalates, on the digest, the verdict and the evidence path
   of an independent verifier (a fresh session, a different engine where possible, rule 5). Reading the state
   file is part of this, and she never polls (method 3.8). She does not read raw Codex or `agy` output, research
   findings or diffs: workers write their full results to files and return a digest and a path (method 4,
   project memory; 3.8, pass-back). For a risky node she may spot-check the evidence, one finding at a time.
   She does not review code herself (EJ, 2026-10-03): the mechanical checks are a script gate and the judgment is a
   verifier's, which reviews the diff only after writing its cases blind (`docs/TASK_TYPES.md`, build a feature).

Role subagents only report status. Her picture of the run lives in the state file, so a fresh session can take
over.

**When she does a node herself.** All four must hold:

- the problem, the fix and the check are each one sentence (the test for skipping a workflow, method 2);
- it fits in a few files and a few tool calls without bloating her context;
- it is reversible and touches no live system, running agent or shared state (Rule 6 applies whoever does it);
- the check is a command whose output she records, not "it looks right".

Otherwise she dispatches it. It is recorded in the state file as a node with engine "COO", like any other.

**The cap.** If she passes **8 tool calls** on one node, she stops and dispatches it. The 8 is my provisional number,
not measured; EJ sets it, like the cost ceiling. The guard exists because doing everything herself feels faster and turns the design back
into one large session.

## How a failure shows

The rule for every kind: a node is done only when its **result file exists and passes its check**. An exit code is
never the check on its own.

| Kind | Signals | Trap |
|---|---|---|
| Claude subagent | error or no report | quota behaviour not seen yet (*unknown*) |
| Codex | exit code and stderr from `codex exec`; `/codex:status` for jobs | the rescue subagent returns nothing if Codex fails to start; a missing turn id can hang a job forever (plugin issue #781); quota-exhausted behaviour not seen (*unknown*) |
| `agy` | exit 0 ok, 1 error, 2 cancelled; json `status` | its own `--print-timeout` firing also exits 0, with stderr `[agy] print timeout after Ns with turn in progress; returning partial output` (*verified* 2026-10-03, `runs/20261003-dispatch-canary`); a tool needing approval is soft-denied and the run still exits 0 (stderr notice only); `-p` can hang with no TTY (issue #318); it stops on quota, spend cap or credits with no known code (*unknown*) |
| `qwen` | **a timeout must kill the process group**: the `qwen` wrapper's `node` child outlived a plain kill and ignored SIGTERM (*verified* 2026-10-03, `runs/20261003-dispatch-canary/README.md`); `--max-wall-time 90s` let a call run 101 s and exit 0, so the outer timer is the real limit; from a repo root it loads the project's context — a one-line answer cost about 198k tokens, against 18–27k from an empty folder. Exit code: 1 = argument validation (bad `--approval-mode`, `--output-format`, `--max-wall-time`, unknown `-r` session), 52 = `--json-schema` unreadable or invalid, 55 = a `--max-*` budget hit (*verified* 2026-10-02); json result under `--output-format json` | a bare word is a one-shot prompt that spends quota. **A wrong `-m` exits 0 and silently runs `qwen3.7-plus`**: read `init.model` in the json, never the exit code. A task that needs a write tool exits 0 with no file. Quota-exhausted behaviour and hang-without-TTY not seen (*unknown*) |

So every external call gets an outside timeout (for `agy` also `--print-timeout`, default 0 = wait forever), and an empty or missing result file counts as a failure.

## The canary piece

A preparation piece at the front of any run that uses Codex, `agy` or `qwen` (readiness, method 3.1). One tiny task per
kind, with an answer that can be checked:

1. Ask for a fixed thing: write `OK` to `runs/<runId>/canary/<kind>.txt`, or return `{"ok": true}` with the schema
   flag.
2. Run it under a 60–90 second timeout.
3. Record the version of the **binary that ran** — for a provider, its bundled copy, not the CLI on `PATH` (see
   "The bundled-runtime trap"). Pass only if the exit code is right, the file exists with exactly that content,
   stderr has no approval-denied or quota notice, and for `agy` the json `status` is success.
4. The canary node returns `pass`, `fail` or `timeout` with the reason to the script, and the state file records it.
   The scheduler (the script or the COO), not the state file, decides which kinds the graph may use.
   Format, one Log line per kind: `canary <kind> <version> pass|fail|timeout: <reason>`.
5. Sabotage check (house rule): once, run an impossible task and confirm the canary reports `fail`. Until that has
   been done, the canary is not known to be able to fail.

**`qwen` form (run 2026-10-02, qwen 0.24.7, `-m qwen3.8-flash`).** `qwen --approval-mode plan --max-wall-time 90s
--json-schema '{"type":"object","required":["ok"],"properties":{"ok":{"type":"boolean"}}}' --output-format json
-m <model> "Return ok true."` with stdin closed. Pass: exit 0, `subtype: success`, the result's `result` field is
`{"ok":true}`, and the `system` init event's `model` equals `<model>`. Result: **pass**, 1 turn, about 17.8k tokens.
Sabotage: the same call with `--max-wall-time 1s` ended exit 55 with `FatalBudgetExceededError` on stderr: **fail
proven**. Lessons: (1) `{"ok":{"const":true}}` failed 5 turns (~112k tokens): the model sent `"true"` as a string
and the tool kept rejecting it, so use `type: boolean` and check the value in the script; (2) `--max-tool-calls 0`
aborted with exit 55 even though `structured_output` is documented as exempt, so do not use it here; (3) `--bare`
skips settings, so auth is lost ("No auth type is selected"); (4) a bare run loads ~17k input tokens of
context, a run with skills and memory loaded cost far more. Never probe qwen with a bare word.

It does not prove quota left, output quality, or that the tool stays inside its workspace. Each canary spends a
little usage, so it runs once per run, and the person's go-ahead for the run covers it. Open: whether to re-check
before long jobs.

## When a kind fails mid-run — removed 2026-10-05

**There is no fallback.** A timeout, an empty result or a quota stop is a failure of the executor, not a failed
attempt, so it does not count against the node's attempt limit — but it **blocks the node and goes to EJ**. Write a
Log line: `<node> executor-fail <kind>: <reason>`.

**Why it was removed (EJ, 2026-10-05).** *"This fallback I think we make things too complex already. We already do a
checking before creating the workflow, and now opencode has higher priority than codex, so just let it — we remove
the rule, because I can see when things failed the subagents will report back, so no need to have this."*

What the mechanism cost, for the record. `DEFAULT_FALLBACKS` added a second engine, a second model and a second
`workdir` to every failure path; a node could finish on an engine nobody chose, and the log line that made it
visible was the only thing standing between a silent substitution and a reported one. It also carried a live defect:
both builder kinds fell back to **Claude**, which is the reviewer most designs give a Codex builder, so any fallback
could quietly make the reviewer the builder's own kind (register `8.2`, rule 5). Removing the fallback removes that
case rather than policing it.

The simpler rule that replaces it: **one engine per node, and a failure reports.** If a plan ever wants a second
engine, that is a node in the graph — visible, with its own check — not a hop inside the dispatcher.

**Still true, and unaffected:** the dispatcher refuses a node whose plan names an unknown engine or a model it
needs; `check_plan` validates the engine a node *names*. And the failure table above still records that
quota-exhausted behaviour has not been seen (*unknown*) — a quota stop that exits 0 with a notice is read as
*success*, so it never looks like a failure at all. Removing the fallback does not change that; it means such a
failure is reported when it is seen, not papered over.

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
- `qwen`: the canary passed and its sabotage failed as required (above); the key is valid. Cost per call, measured
  2026-10-02: about 18k to 27k tokens for a one-turn answer, 93k to 129k when it uses tools. Still open: whether
  `CLAUDE.md` is read (inconclusive), quota-exhausted exit code.
- Skill visibility (probe 2026-10-02, model self-report): Codex lists skills from `~/.agents/skills` and `~/.codex/skills`
  (the `coding-discipline` control appeared) but NOT from `~/.claude/skills` or a project `.claude/skills`, so it does
  not see `workflow-design`; `codex exec` outside a git repo needs `--skip-git-repo-check`. agy listed only its own
  built-ins, did not list `coding-discipline`, and has no working positive control: whether it reads any user skill
  dir is *unknown*. Adding a `workflow-design` link under `~/.agents/skills/` should expose it to Codex; not done.
- `agy` headless behaviour on quota exhaustion, and whether `agy` logs in non-interactively here, are untested.
- Pricing for `agy` comes only from SEO pages that disagree; model lists conflict between blogs (trust `agy
  models`).
- `codex mcp-server` was removed per OpenAI's docs; community pages that use it are out of date. The plugin and
  `codex exec` are the supported routes.
- The Codex plugin has many open issues (leaked brokers, hooks growing `CLAUDE_ENV_FILE`, hangs). Treat it as
  fragile and run the canary first.
- Sources: `github.com/openai/codex-plugin-cc`, `learn.chatgpt.com/docs/*` (was developers.openai.com/codex),
  `antigravity.google/docs/cli/*`, `github.com/google-antigravity/antigravity-cli` issues #36, #318, #1095.
