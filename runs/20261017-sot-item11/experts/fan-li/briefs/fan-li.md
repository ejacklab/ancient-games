# Brief — 范蠡 (Fan Li) answers one question

You are **范蠡 (Fan Li)**, one of the experts EJ consults. You were built from a numbered list of 范蠡 (Fan Li)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261017-sot-item11/experts/fan-li/seats/fan-li-list.md` — the "## Final list" section; items are numbered 1–18.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261017-sot-item11/experts/fan-li/seats/fan-li-identity.md` — the "## Who they are" section.

## The question

# Five open points in the memory design's requirements: decide each

The source-of-truth memory design is three files in `docs/memory-system/`: the prose `SOURCE_OF_TRUTH.md`, the
requirements `SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, and release notes. A review left five open points. For **each** of
A–E, give your choice and one or two sentences of wording if it changes the design. Do not invent numbers: a limit is
a comparison or a measured value with its source (the owner's rule, *recall*: house memory "comparisons, not
numbers").

## A. A merge, and a path one side removed

**Fact** (*read*: the YAML, record W6.3a, level MUST): *"Whoever does the merge keeps both sides: both `changed:`
lines, both links, and every `covers` path either side wrote."* Its `fails_if`: *"a merged entry is missing a
`changed:` line, link or `covers` path that one side added"*. **Fact** (*read*: record K4.3): after its first commit
an entry's `covers` *"may also be corrected, for example after a file is renamed, with a `changed:` line"*.
**Question:** if one branch removed or replaced a stale path and the other did not touch it, does the merge keep the
removal, or bring the stale path back? Which wording?

## B. What the kit carries

**Fact** (*read*: the YAML, key `kit`): *"These files travel together as one kit: SOURCE_OF_TRUTH.md, this file,
CACHES.md and vision-statements/ … `tools/` and `docs/index-md/` are relative to the repository root."* **Fact**
(*read*: the YAML, key `checks`): `tool` means *"tools/memory_index.py, in write mode or with --check, fails it"*;
about a dozen records use `check: tool`, and K6.2 names the tool and `docs/index-md/` (its requirements and design).
**Question:** should the kit include the tool and `docs/index-md/`, or should the design say the tool is installed
separately (and what a project without it does)?

## C. Where the measured limit is recorded

**Fact** (*read*: record Rd3.1a, MUST, `check: tool`): *"`INDEX.md` fits the strictest start-file limit among the
agents that work on the project. … Until the project owner records measured limits, the tool's limit is the example in
Rd3.1b: 200 lines and 24,000 bytes."* `who_decides`: the project owner (which agents work on the project). **Fact**
(*read*: `tools/memory_index.py:35-36`): `MAX_LINES = 200`, `MAX_BYTES = 24_000`, commented as "the design's example,
not a measurement". **Fact** (*read*: `docs/index-md/REQUIREMENTS.md` B4.1): the values "come from measuring the
readers' load paths. Until then they hold the design's example". So the numbers sit in three places: Rd3.1a, Rd3.1b
and the tool. **Question:** where, and in what form, does the project owner record the agents and their limits so the
tool can read them and a reviewer can see when the interim example stops applying? (For example a section of
`AGENTS.md`, a small config file, or the tool's constants — say which and why.)

## D. Which agents count

**Fact** (*read*: the YAML, group Rd3 title): *"`INDEX.md` fits every agent that reads it"*; the prose
(`SOURCE_OF_TRUTH.md:157`): *"the strictest start-file limit of the agents that read it"*. Record Rd3.1a: *"among the
agents that work on the project"*. **Question:** which set is right — agents that read `INDEX.md` at session start, or
all agents that work on the project — and which wording?

## E. Build the tool change, and measure the limits?

**Fact** (*read*: `docs/memory-system/CACHES.md`, table "The index read at session start", lines 489–497): documented
start-file limits per engine — Claude Code `MEMORY.md` "first 200 lines … or the first 25KB" (W-1); Codex `AGENTS.md`
up to 32 KiB (`project_doc_max_bytes`, W-2); agy 24,000 bytes per rule file and a 20,000-token budget, or 12,000
characters in other reports (W-4, a conflict); opencode no limit stated; dsh a 65,536-byte budget; Qwen Code 200 lines
or 25,000 bytes. The research below re-checks these. **Question:** should the tool be changed to read the limits from
where C records them (a code change with tests, in its own run), and should the limits be measured on the engines
(not only read from docs) — now, later, or not at all?

The research for this question is added below by the workflow before you are asked.

## Research findings

Research step, 2026-10-17 (`research/experts.md`). **Labels:** *verified* = the researcher opened the source and it
says so (URL or local path given); *reported* = a source says it and it could not be confirmed. Web pages were read
through WebFetch, whose quotes are model-made extracts, not byte-checked; the dsh and Qwen Code local checks are
byte-exact greps of the installed packages. Installed versions: Claude Code 2.1.302, codex-cli 0.160.0, agy 1.4.0,
opencode 1.18.34, Qwen Code 0.21.8, dsh 0.2.0-rc.2. Whether each docs page describes the installed version is **not
measured**.

### By agent

| Agent | File(s) loaded at start | Documented limit | Over the limit | Label |
|---|---|---|---|---|
| Claude Code — auto memory | `MEMORY.md` | "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation." | "Content beyond that threshold is not loaded at session start"; a write over the limit succeeds but returns an error telling Claude to rewrite the index | verified — https://code.claude.com/docs/en/memory |
| Claude Code — instructions | `CLAUDE.md` (and its `@imports`) | "This limit applies only to `MEMORY.md`. Claude Code loads a CLAUDE.md file of up to 4 MiB in full and skips a larger file." Advice, not a limit: "target under 200 lines per CLAUDE.md file" | file over 4 MiB is skipped | verified — same page |
| OpenAI Codex CLI | `AGENTS.md` chain (global + root-to-cwd) | Codex "stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)" — combined across files, not per file | truncation: "Raise `project_doc_max_bytes` or split large files across nested directories" | verified — https://learn.chatgpt.com/docs/agent-configuration/agents-md (redirect from developers.openai.com/codex/guides/agents-md); config reference: "Maximum bytes read from `AGENTS.md`", no default shown — https://learn.chatgpt.com/docs/config-file/config-reference |
| Antigravity (agy) | `AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md` (workspace); `~/.gemini/…AGENTS.md / GEMINI.md`, `~/.gemini/config/rules/*.md` (global) | "24 KB (`24,000` bytes) per-file limit"; "All active global and `always_on` rules share a 20,000-token budget", separate from the skills/MCP budget | a file over 24,000 bytes is truncated; over 20,000 tokens "Antigravity automatically demotes the largest rule files from inline text to lightweight pointers" | verified — https://antigravity.google/docs/rules |
| Antigravity (agy), older figure | rule files | "Google documents a 12,000-character limit per rule file" | — | reported — https://agentpedia.codes/blog/antigravity-agents-md-not-working-fix (updated 2026-07-21); not confirmed on an official page (the old `/docs/rules-workflows` now redirects to `/docs/rules`; the web archive was not reachable) |
| Google Gemini CLI | `GEMINI.md` (name set by `context.fileName`), global + ancestors + subdirectories | **none stated**; the only number is the subdirectory scan, "limited to 200 directories by default" (`context.discoveryMaxDirs`) | — | verified (absence) — https://geminicli.com/docs/cli/gemini-md/ and https://geminicli.com/docs/reference/configuration/ |
| opencode | first `AGENTS.md` (or `CLAUDE.md`) walking up; `~/.config/opencode/AGENTS.md` (or `~/.claude/CLAUDE.md`); files in `instructions` of `opencode.json` | **none stated**; only "Remote instructions are fetched with a 5 second timeout" | — | verified (absence) — https://opencode.ai/docs/rules/ |
| Qwen Code — auto memory | `MEMORY.md` index | the index body and the prompt-loaded portion "share a limit of 200 lines and 25,000 UTF-16 code units" | truncated, with a notice; short entries (≤150 code units) kept before long ones | verified — https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/ ; installed 0.21.8 code: `MAX_MANAGED_AUTO_MEMORY_INDEX_LINES = 200`, `MAX_MANAGED_AUTO_MEMORY_INDEX_BYTES = 25e3`, compared against `trimmed.length` (UTF-16 code units), cut at the last newline |
| Qwen Code — instructions | `~/.qwen/QWEN.md`, project `QWEN.md`, `.qwen/QWEN.local.md`, `AGENTS.md`, `@path` imports | **none stated**; only "the longer it gets, the less reliably Qwen follows it" | — | verified (absence) — same Qwen page |
| Qwen Code — 15% warning | always-loaded context | a warning when it passes 15% of the window (earlier run, CX in `CACHES.md`) | advisory | reported — not found on the Qwen page, by web search, or by a grep of the installed bundle |
| DeepSeek Harness (dsh) | `$DSH_HOME/AGENTS.md`, then `AGENTS.md`/`CLAUDE.md` (+ `.local.md` overlays) from project root to cwd | `maxBytes` caps "the complete rendered baseline message, in bytes"; required, no built-in default — "`dsh-base` already includes it with a 65,536-byte budget"; `maxSourceBytes` 1,048,576 per source file | broader files dropped whole before the most specific file is truncated, with a visible `Workspace instruction budget ...` notice | verified, local not web — installed `dsh-agent-instructions/README.md` lines 28–75; `maxBytes: 65536` in the `standard`, `ptc` and `cordis` presets. No official web page found |
| Other DeepSeek-based CLIs | — | none found | — | not found |

### Where sources conflict, or `CACHES.md` is off

1. **agy: 24,000 bytes + 20,000 tokens, or 12,000 characters.** Official page now: 24,000 bytes per file and a
   20,000-token budget (verified). 12,000 characters: a third-party page dated 2026-07-21 citing Google (reported). A
   third-party write-up dated 2026-09-26 says the 20,000-token rules budget came in release 2.17.0 (reported —
   https://antigravitylab.net/articles/antigravity/antigravity-rules-token-budget-measure-before-demotion).
   *Researcher's reading:* 12,000 characters was the earlier limit and 24,000 bytes replaced it; not confirmed. The
   installed `agy` reports 1.4.0; which version the page's limits apply to is **not measured**.
2. **Qwen Code: bytes or code units.** `CACHES.md` says "25,000 bytes"; docs and code measure **UTF-16 code units**
   (the constant is named `_BYTES` but compares string length). Equal for ASCII; for non-ASCII text the bytes are more.
3. **Claude Code `CLAUDE.md`.** `CACHES.md` gives only "target under 200 lines" (advice). The docs also state a hard
   limit: up to 4 MiB loaded in full, larger skipped. "25KB" for `MEMORY.md`: 25,000 or 25,600 bytes is **not stated**.
4. **Codex.** The guide gives the 32 KiB combined default; the config reference omits the default. No value conflict.
5. **dsh.** 65,536 bytes is the base profile's and presets' value; the loader requires each deployment to choose
   `maxBytes`, so a profile can change it (active-profile override not checked).

### What this means for Rd3.1 (*researcher's reading*, not a decision)

The documented per-file limits that could bind a start file: Claude Code `MEMORY.md` 200 lines / 25KB; Qwen Code
`MEMORY.md` index 200 lines / 25,000 code units; agy 24,000 bytes per rule file (or 12,000 characters if the older
figure applies). Codex (32 KiB) and dsh (64 KiB) are combined budgets shared with every other instruction file. Gemini
CLI and opencode state none. The tool's interim example (200 lines, 24,000 bytes) is at or under every verified
per-file figure, and not under the reported 12,000-character agy figure. None of these numbers was measured on an
engine in this step.

## How we work — the pattern you adapt and improve

EJ's runs follow one pattern. Your advice must fit it, and it may improve it: label such a point *proposed change to
the pattern* and say what it would change.

- **The time is set at the start.** EJ gives a time or a number of rounds; within it, questions go to you, the experts,
  and the main agent decides provisionally from your advice. A question goes to EJ only after three failed trials on
  it or once the time is used up.
- **Small pieces, timestamped.** Work is divided into small pieces, each with its own check, and every worker writes a
  timestamped progress line per piece, so progress and time are seen while the work runs, not only at the end.
- **Vision and use cases first.** An option that serves no use case or vision line is wrong, however good.
- **Research and data, not recall.** Points rest on findings or measurements from the run, cited by id; a point from
  memory alone is *recall* and does not decide.
- **Workflows when possible.** Work with more than one step runs as a workflow — a script that orchestrates the
  agents in phases, with its progress visible — rather than as one long prompt.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 范蠡 (Fan Li)'s mouth that your list does not contain. Copy Chinese character by character, in the
   script your list uses (simplified or traditional); do not convert between them or swap a variant form (赵 / 趙,
   爲 / 為) — the check compares exactly, and a converted quote fails it.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 范蠡 (Fan Li) — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>


## Lessons (from earlier agents' failures; apply each that fits)

- Every file a question or brief for another engine cites lives inside the repo it runs in: copy an outside source into the run folder and cite the copy. Headless engines (agy, opencode) auto-deny reads outside it and answer nothing. (cite-files-inside-the-repo)
- A criterion names the outcome ("the matching lessons reach the agent before the call runs"), never a mechanism that an open question of the same run is still to decide; otherwise the decision fails the criterion it should have served. (criteria-name-outcomes)
- Each fact in a question or brief for another agent carries its own label and the file:line or command that checked it; a fact with neither is marked recall. One "verified" label over a block of facts hides a recalled one. (facts-carry-their-source)
- A Claude Code subagent's Write of a report file can be refused ("Subagents should return findings as text"): ask a researcher subagent for its digest first and its full findings as text after it, and save them yourself. For a read-only caller of bun, set `BUN_RUNTIME_TRANSPILER_CACHE_PATH=0`, or bun writes a cache under HOME. (subagent-returns-text)
- After EnterWorktree, the isolation guard also refuses the subagents' shell heredoc writes, `HOME=…` prefixes and writes to the main checkout — and an agent may not notice and report success. Briefs for those agents say "write files with the Write tool", inside the worktree. (worktree-isolation-reaches-subagents)
