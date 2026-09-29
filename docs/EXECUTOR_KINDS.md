# Executor kinds — who can run a node

Written 2026-09-29 from one research session (three Sonnet 5.5 agents for Codex, three for `agy`) plus local
read-only checks. Nothing here has been run in a real workflow (n=0). What the research agents read from docs or
GitHub is marked *reported*; what was checked on this machine is marked *verified*.

A node in a workflow design (method 3.6) is run by one executor kind. This file says what each kind is, what it is
assigned to, how it is called, how its failure shows, and the rules that keep mixed runs predictable. The method's
readiness step (3.1) proves each tool works; the canary below is that proof for these three.

## The three kinds

| | Claude subagent | Codex (GPT-6-sol) | Antigravity `agy` (Gemini) |
|---|---|---|---|
| Assigned to (EJ's view 2026-09-29, unmeasured) | orchestration, cheap research fan-out, glue | research and reports, coding and code generation, code review, finance, data extraction, workflow planning and design, web search | classification (Gemini 3.1 Pro) |
| Called by | the Agent or Workflow tool | plugin `codex@openai-codex` v1.0.6: `/codex:rescue`, `/codex:review`, `/codex:adversarial-review`; or `codex exec` from Bash | `agy -p "<prompt>"` from Bash |
| Installed here | yes | yes, `codex` logged in with ChatGPT (*verified*; the canary records the version, it is not pinned here) | yes, `agy` at `~/.local/bin/agy` (*verified*); `agy models` returned a list, which suggests a working login (*inferred*) |
| Default write access | per agent type | the plugin defaults to approvals "never" and sandbox read-only (`scripts/lib/codex.mjs:67-68`); rescue writes only because its agent adds `--write` (`agents/codex-rescue.md:34`) (*verified*) | workspace writes auto-allowed, shell soft-denied (*reported*) |
| Read-only form | read-only agent types | `codex exec -s read-only` (*verified* in `--help`). `-a/--ask-for-approval` exists only on top-level `codex`, not on `exec`, so put it before `exec` or omit it; untested | `--mode plan`; `--sandbox` for OS isolation (*reported*, flags *verified* in `--help`) |
| Structured result | report returned to the caller | `--output-schema <file>`, `-o/--output-last-message <file>`, `--json` (*verified* in `--help`) | `--output-format json`, `--json-schema` (flags *verified*) |
| Resume | SendMessage to the agent | `--resume-last` in rescue; `codex exec resume --last` (*verified* in `--help`) | `-c` or `--conversation <id>` (*verified* in `--help`) |
| Reads which instruction file | `CLAUDE.md` | `AGENTS.md` (and `~/.codex/config.toml`) | `AGENTS.md` and `GEMINI.md`, third-party source only; `CLAUDE.md` not found (*uncertain*) |
| Model source | the agent's `model` setting | `--model`/`--effort` (rescue, `exec -m`); `~/.codex/config.toml` (`gpt-6-sol`, effort medium) when none is passed | `--model`; `agy models` lists what the plan offers, and it includes Claude models as well as Gemini, so "agy = Gemini" is a choice |

The assignment column is EJ's stated preference, recorded as such. The research found no head-to-head evidence for
or against it. The design treats it as a default that a node can override with a reason, and the first runs are
where it gets tested.

## How a failure shows

The rule for every kind: a node is done only when its **result file exists and passes its check**. An exit code is
never the check on its own.

| Kind | Signals | Trap |
|---|---|---|
| Claude subagent | error or no report | quota behaviour not seen yet (*unknown*) |
| Codex | exit code and stderr from `codex exec`; `/codex:status` for jobs | the rescue subagent returns nothing if Codex fails to start; a missing turn id can hang a job forever (plugin issue #781); quota-exhausted behaviour not seen (*unknown*) |
| `agy` | exit 0 ok, 1 error, 2 cancelled; json `status` | a tool needing approval is soft-denied and the run still exits 0 (stderr notice only); `-p` can hang with no TTY (issue #318); it stops on quota, spend cap or credits with no known code (*unknown*) |

So every external call gets an outside timeout (for `agy` also `--print-timeout`, default 0 = wait forever), and an empty or missing result file counts as a failure.

## The canary piece

A preparation piece at the front of any run that uses Codex or `agy` (readiness, method 3.1). One tiny task per
kind, with an answer that can be checked:

1. Ask for a fixed thing: write `OK` to `runs/<runId>/canary/<kind>.txt`, or return `{"ok": true}` with the schema
   flag.
2. Run it under a 60–90 second timeout.
3. Record the tool's version in the state file. Pass only if the exit code is right, the file exists with exactly that content, stderr has no approval-denied
   or quota notice, and for `agy` the json `status` is success.
4. The canary node returns `pass`, `fail` or `timeout` with the reason to the script, and the state file records it.
   The script, not the state file, decides which kinds the graph may use.
   Format, one Log line per kind: `canary <kind> <version> pass|fail|timeout: <reason>`.
5. Sabotage check (house rule): once, run an impossible task and confirm the canary reports `fail`. Until that has
   been done, the canary is not known to be able to fail.

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
8. **External kinds are called through a Claude wrapper.** The script schedules nodes (method 3.6); a Codex or
   `agy` node runs as a Claude subagent that makes one Bash call. That costs Claude tokens on every such node, and
   the wrapper sees the worker's output, so the wrapper is never that node's verifier.

## Open before relying on this

- Google's terms may bar calling `agy` headless from another tool on an individual account (§6 of the Antigravity
  Additional Terms, asked on the Google AI developer forum, unanswered). Resolve before automating on it.
- Web search is assigned to Codex, but `--search` is listed only on top-level `codex`, not on `codex exec`. How to
  enable it non-interactively is unknown.
- Remaining usage cannot be read by the workflow for any of the three kinds; only failure is visible. Design for
  clean stops, not for percentages. Unchecked: Codex `/status` in the TUI, `agy` `/credits`.
- `agy` headless behaviour on quota exhaustion, and whether `agy` logs in non-interactively here, are untested.
- Pricing for `agy` comes only from SEO pages that disagree; model lists conflict between blogs (trust `agy
  models`).
- `codex mcp-server` was removed per OpenAI's docs; community pages that use it are out of date. The plugin and
  `codex exec` are the supported routes.
- The Codex plugin has many open issues (leaked brokers, hooks growing `CLAUDE_ENV_FILE`, hangs). Treat it as
  fragile and run the canary first.
- Sources: `github.com/openai/codex-plugin-cc`, `learn.chatgpt.com/docs/*` (was developers.openai.com/codex),
  `antigravity.google/docs/cli/*`, `github.com/google-antigravity/antigravity-cli` issues #36, #318, #1095.
