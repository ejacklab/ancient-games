# Do agents use memory well on their own? — research report

Version line: **v0** — researcher (Claude Opus 5.5), 2026-10-13. Web sources plus this repo's own memory research; 25
sources (list at the end). Later versions add a line each here.

**How to read the labels.**
- ***verified***: I read the source text myself and the quote is copied from it. The raw text is saved under `sources/`,
  or it is a repo file read directly.
- ***reported***: the quote or number came to me second-hand. That covers a WebFetch answer (a small model's summary
  of the page), a search-result summary, or a row from this repo's earlier research that I did not re-read at source.
- ***unproven***: the source asserts the claim and shows no evidence. This tag comes from `docs/RESEARCH_TAGS.md`.
- ***my reading***: an inference of mine.
- ***not measured***: nobody measured it; no source was found.

Experts and later versions should keep these labels and never upgrade one in place. Ids: **T** = tool behaviour (§1),
**E** = measured evidence (§2), **M** = failure mode (§3), **O** = option (§5), **S** = source.

## Short answer (as of this version)

1. **Reading: partly.** Each tool loads a fixed set of files by itself (T1–T8). Anything else is read only if the model
   decides to read it, and in measured runs it often does not. A docs skill was "never invoked" in 56% of cases (E1).
   58% of trials with a code-graph tool made zero calls to it (E2). *Quoted, reported.*
2. **Writing: the agents now write memory unasked, and no study has measured how good that memory is.** Claude Code
   and Codex both write their own memory (T2, T6). Nobody has published a measurement of Claude Code's auto memory or
   Codex memories — *not measured*. The closest measurements are poor:
   - skills that the agent wrote for itself scored below having no skills, in Claude Code, Codex and Gemini CLI (E3);
   - "add-all" memory made agents worse (E5);
   - repeated rewriting collapsed a memory from 18,282 to 122 tokens (E6).

   *Quoted, reported.*
3. **What does get loaded is followed, and it costs.** Agents used a tool 1.6 times per task when the context file
   named it, against under 0.01 times when it did not. Repository overviews did not help, and inference cost rose over
   20% (E4). Performance "consistently degrades with increasing input length" (E7). *Quoted, reported.*
4. **The vendors do not leave the timing to the model.** Three examples:
   - The memory tool adds "ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE" to the system prompt (T4,
     *verified*).
   - Claude Code says steps that must happen belong in hooks, because CLAUDE.md is "not a hard enforcement layer" (T1,
     *verified*).
   - Codex says rules that must always apply stay out of memories (T6, *reported*).
5. **For the method** (*my reading*, built on items 1–4): the method already puts what a node must read and write into
   files named in its brief and the state file (§4). That is the form the evidence favours. Two things it does not say
   (§5):
   - how a node's own built-in memory (Claude auto memory, Codex memories) is set;
   - how memory an agent writes is checked before it is kept.

## 1. What the agents do by themselves

The same split holds in every tool. Some reads are made by the **harness**, which loads the file whatever the model
decides. Others are made by the **model**, only if it decides to, or only when the user asks.

| id | Tool | Loaded automatically (harness) | Model decides | Only on request / off by default | Label, source |
|---|---|---|---|---|---|
| T1 | **Claude Code — CLAUDE.md** | Files above the working directory are loaded at launch. Files in subdirectories load "on demand" when Claude works there (L64). Project-root CLAUDE.md is re-read after `/compact` (L625). | Whether to follow it: "Claude treats them as context, not enforced configuration" (L24); "CLAUDE.md instructions shape Claude's behavior but are not a hard enforcement layer" (L326). A CLAUDE.md that only *tells* Claude in words to read `AGENTS.md`: "Claude sees `AGENTS.md` only if it decides to open the file" (L435). | Hooks are the documented way to make a step certain: they "apply regardless of what Claude decides to do" (L589). | *verified*, S1 |
| T2 | **Claude Code — auto memory** | At the start of every conversation, the first 200 lines or 25KB of `MEMORY.md` (L546). | **What to write and when:** "It decides what's worth remembering based on whether the information would be useful in a future conversation" (L485). It "skips anything it can derive from the codebase" (L483). **When to read topic files:** they are not loaded at startup, and "Claude reads them on demand … when it needs the information" (L552). | The harness reminds Claude to shorten `MEMORY.md` near the limit, and returns an error when it is over (L548). It is on by default in local sessions. The main session's auto memory is not loaded into subagents (L554). | *verified*, S1 |
| T3 | **Claude Code — subagent memory** | The subagent gets the first 200 lines or 25KB of its own `MEMORY.md`, and "instructions for reading and writing to the memory directory". | What to record. The docs' own tips still say to ask the agent to check its memory before work and to save what it learned after. | Only works if the agent's file has the `memory` frontmatter field. | *reported*, S3 (earlier run's WebFetch reading of the sub-agents page) |
| T4 | **Claude API — memory tool** | When the tool is present, the API adds a system-prompt block: "IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE. … ASSUME INTERRUPTION …". | What to write, and how to organise it. The docs add: "If Claude still creates cluttered memory files, you can reinforce it in your prompt". | Expiry and size caps are left to the developer: "Periodically delete memory files that haven't been accessed in a long time". | *verified*, S2 (full-text return; see the note in `sources/`) |
| T5 | **Codex — AGENTS.md** | One file per directory from the project root down to the working directory, plus the global file. They are concatenated, with later files overriding earlier ones. The chain is built once per run. Default cap is 32 KiB (`project_doc_max_bytes`). Codex stops adding files at the cap, so later guidance can be cut. | Whether to follow it. | — | *reported*, S9 |
| T6 | **Codex — memories** | Generated memories are used in later threads when enabled (`use_memories`). | Nothing during the task. Codex builds memories "from eligible past chats in the background, skipping active or short sessions and redacting secrets". | Off by default. Enabled with `memories = true`. Guidance: keep required team rules in `AGENTS.md`, and treat memories as a recall aid, "not the only source for rules that must always apply". | *reported*, S10 |
| T7 | **Gemini CLI (replaced by Antigravity CLI on 2026-06-18)** | Global `~/.gemini/GEMINI.md` and workspace `GEMINI.md` files. When a tool touches a directory, the CLI scans that directory and its ancestors for more GEMINI.md files ("JIT"). All found files are concatenated "with every prompt". | Saving: memory is written "with `write_file` or `replace`" into one of three tiers. The use cases listed are preferences, project decisions and aliases. | — | *reported*, S11, S12 |
| T8 | **opencode** | `AGENTS.md` (project, then global), with `CLAUDE.md` as a fallback. "The first matching file wins in each category." Files listed in the `instructions` field of `opencode.json`. | Files referenced inside `AGENTS.md`: "opencode doesn't automatically parse file references". The docs' workaround tells the agent to "use your Read tool to load it on a need-to-know basis". | No built-in memory feature is mentioned. | *reported*, S13 |
| T9 | **Antigravity / `agy`** | Third-party sources only. They say it reads `AGENTS.md` and `GEMINI.md`, and that "Knowledge Items" are generated automatically from conversations. | — | — | *not measured*: no official doc was read (see §7 and Gaps) |

**Across the tools** (*my reading* of T1–T9): the harness loads instruction files and memory indexes. Everything
past the index is left to the model's judgement, mid-task. The only exception is Codex memories, which are written in
the background by the harness, not by the working model. No tool lets the model choose *whether to read the index*:
every vendor forces that read.

## 2. Evidence on how well they do it

Measured results come first. Every row is second-hand (WebFetch or earlier repo research) unless marked *verified*.
"Our" models (Claude Code, Codex, Gemini CLI) appear in E1, E3, E4 and E21.

| id | Claim | Label | Source (date) | Quoted |
|---|---|---|---|---|
| E1 | A Next.js docs skill was not invoked in 56% of eval cases. Without instructions the skill scored the same as no docs (53% vs 53%). An explicit instruction raised invocation to 95%+ and the pass rate to 79%. An 8KB docs index loaded in `AGENTS.md` reached 100%. Models and eval count are not stated. | reported | S15, Vercel, 2026-01-27 | "In 56% of eval cases, the skill was never invoked." |
| E2 | Agents with a code-graph tool available did not call it in 58% of trials. Using it consistently needed explicit prompting. | reported (repo row s3-F33, 2026-10-11 tags) | S23, CodeCompass arXiv 2602.20048, 2026-02-23 | "58% of trials with graph access made zero tool calls, and agents required explicit prompt engineering to adopt the tool consistently." |
| E3 | Skills that the model wrote for itself scored below the no-skills baseline in all three configurations: −8.1 pp Claude Code + Opus 4.7, −11.3 pp Codex + GPT-5.5, −11.5 pp Gemini CLI + Gemini 3.1 Pro. Curated skills scored +18.2 to +24.8 pp. A trajectory audit blames generated packs "the solver never discovers", authoring that "displaces solver work", and "confidently wrong pack content". The authors say the deficit "mixes content quality with skill-discovery and creator/solver interference effects". | reported | S17, SkillsBench arXiv 2602.12670 v4, 2026-06-14 | "Self-generated Skills land below the no-Skills baseline on all three configurations" |
| E4 | Context files (`AGENTS.md`) did not generally improve task success and raised cost by over 20%:<br>• LLM-generated files changed success by −0.5% (SWE-bench) and −2% (their own benchmark), not significant;<br>• developer-written files changed it by +2.4% (p=21%);<br>• agents did follow the files: `uv` was used 1.6 times per instance when the file named it, against under 0.01 when it did not;<br>• the files did not shorten the time to the first relevant file.<br>Tested on Claude Code + Sonnet-4.5, Codex + GPT-5.2 and GPT-5.1 mini, and Qwen Code. | reported | S16, Gloaguen et al., arXiv 2602.11988 (v1 2026-02-12, v3 2026-09-29) | "providing context files does not generally improve task success rates"; "increasing inference cost by over 20% on average"; "repository overviews, although popular and recommended by model providers, are not helpful" |
| E5 | Storing every execution as memory ("add-all") made agents worse than a fixed memory, on all four agents tested (GPT-4o-mini backbone). For example, EHRAgent scored 13.05 with add-all and 16.75 with fixed memory. Strict, evaluator-filtered addition gained +15.5 to +25.5 points over add-all. Deletion helped on three of four agents, and depends on the evaluator being reliable. | reported | S18, Xiong et al., arXiv 2505.16067 v2, 2025-10-10 (ACL 2026 per search result) | "error propagation, where inaccuracies in past experiences compound and degrade future performance" |
| E6 | When an LLM fully rewrites its own accumulated context, details are lost ("context collapse"). In one run the context fell from 18,282 tokens (accuracy 66.7) to 122 tokens (accuracy 57.1), below the 63.7 no-adaptation baseline. Rewriting also tends toward "short, generic prompts" ("brevity bias"). | reported | S19, ACE, arXiv 2510.04618 v3 (2026-03-29), ICLR 2026 | "context collapse, where iterative rewriting erodes details over time" |
| E7 | Across 18 LLMs, performance falls as input grows, even on simple tasks. A single distractor already lowers it. | reported | S20, Chroma "Context Rot", 2025-07-14 | "Across all experiments, model performance consistently degrades with increasing input length." |
| E8 | Anthropic reports that the memory tool plus context editing scored 39% above baseline on an internal agentic-search eval, and context editing alone 29%. Context editing cut tokens by 84% in a 100-turn web-search eval. No harness is published. | reported (the numbers are *unproven*: internal eval, no data shown) | S6, Claude blog, 2025-09-29 | "combining the memory tool with context editing improved performance by 39% over baseline" |
| E9 | Models differ widely in agentic retrieval, meaning choosing and chaining file reads themselves. At launch the best model scored 74.0% (Sonnet 4.5); open-weight models scored about 55–57%. | reported | S21, Letta Context-Bench, 2025-10-30 | "Context engineering remains challenging" |
| E10 | On real repository tasks, full memory systems mostly did not help: 11 of 12 solver/system pairings did not beat the memory-off baseline. Injecting verified past experience directly raised resolution on four of five solvers, by 1.1 to 4.5 pp, and lowered steps on all five. | reported | S22, VibeMemBench arXiv 2609.23570, 2026-09-20 | "eleven of twelve solver and system pairings fail to exceed the matched memory-off baseline" |
| E11 | Agents that come close to saturating LoCoMo perform poorly in multi-session agent loops (MemoryArena). Hallucinations build up at memory extraction and updating, and carry into answers (HaluMem). | reported (repo rows s5-F6, s5-F5, 2026-10-11 tags) | S24 (MemoryArena arXiv 2602.16313; HaluMem arXiv 2511.03506) | — (not re-read) |
| E12 | Anthropic states that Opus 4 "becomes skilled at creating and maintaining 'memory files'" when given local file access. The post gives no measurement. | reported; the capability claim itself is *unproven* | S8, Anthropic "Introducing Claude 4", 2025-05-22 | "Claude Opus 4 also dramatically outperforms all previous models on memory capabilities." |

**Where the evidence is thin** (*my reading*):
- None of E1–E12 measures the thing EJ asked about most directly: whether Claude Code's auto memory, or Codex memories,
  pick the right things to keep and recall them when needed. That is *not measured* (§7).
- E1 and E2 measure the agent invoking optional *tools or skills*, not reading optional *files*. They are the closest
  measurements found.
- E1, E8 and E12 are vendor numbers with no published harness.
- Model generations differ:
  - E3 uses Opus 4.7 and GPT-5.5;
  - E4 uses Sonnet 4.5 and GPT-5.2;
  - E5 uses GPT-4o-mini;
  - E1 does not name its models.

  A newer model may skip reads less often. No source settles that.

## 3. Where they fail without instructions

Concrete failure modes, each with its source. Bug reports from users are evidence that the report was filed. The
behaviour they describe stays *unproven* until reproduced.

| id | Failure | Evidence | Label |
|---|---|---|---|
| M1 | **Optional knowledge is not read.** The agent does not open a skill, tool or file it was not made to open. | E1, E2, E3 ("generated packs the solver never discovers"). Claude Code docs: a words-only pointer to `AGENTS.md` is read "only if it decides to open the file" (S1 L435). | reported (E1–E3); verified (S1) |
| M2 | **A "read X at the start" instruction is skipped.** Users report CLAUDE.md startup instructions skipped "especially for simple prompts" (#34763, Opus 4.6, closed by bot as stale, no maintainer reply). Another report says the memory-read instruction was skipped and a stale API key was used (#40272, Sonnet 4.6); its reporter's root cause is that the injected `MEMORY.md` was treated as sufficient. | S25 issues #34763 (2026-03-15), #40272 (2026-03-28) | reported (the issues exist); the behaviour and root cause are *unproven* |
| M3 | **The agent answers before it reads.** A user reports that a stored launch command was ignored "50+ times" even though it was in CLAUDE.md, auto memory and a skill. | S25 issue #43098 (2026-04-03, Opus 4.6, closed by reporter) | reported; *unproven* |
| M4 | **The agent writes everything, and memory degrades.** Bad memories get copied and amplified. | E5 | reported |
| M5 | **Rewriting erodes memory.** Full rewrites collapse detail and drift toward the generic. | E6. The memory tool docs also expect clutter: "If Claude still creates cluttered memory files…" (S2) | reported (E6); verified (S2) |
| M6 | **Self-authored procedures are wrong or unused.** | E3 | reported |
| M7 | **Across sessions, work is left undocumented or declared done early.** Without a harness, agents "tried to do too much at once", left "a feature half-implemented and undocumented", and would "mark a feature as complete without proper testing". The fix was an initializer, a progress file, a JSON feature list and a fixed set of start-of-session reads. | S5, Anthropic, 2025-11-26 (qualitative, no numbers) | reported |
| M8 | **Subagents duplicate work when briefs are vague.** "Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information." | S7, Anthropic, 2025-06-13 | reported |
| M9 | **Context grows until quality drops.** Loaded files also add cost without gain. | E7, E4 | reported |
| M10 | **Instructions are lost after compaction** if they were given only in conversation or in a nested file not yet reloaded. | S1 L627 | verified |
| M11 | **Conflicting instructions are resolved arbitrarily.** "Claude may pick one arbitrarily." | S1 L90 | verified |
| M12 | **Silent truncation.** `AGENTS.md` past 32 KiB stops being added (Codex). `MEMORY.md` past 200 lines or 25KB is "dropped on the next load" (Claude Code). | S9; S1 L548 | reported (S9); verified (S1) |

## 4. What the method says today

Read directly (*verified*) in `docs/WORKFLOW_DESIGN_METHOD.md` and the skill:

- **§4, L482–485:** state lives in a file. Each agent reads it, does one step and writes it back, with one writer at a
  time. It holds progress and results, never reasoning.
- **§4, L487–488:** files in the repo are "the one every tool and every agent can read — use them for anything that
  must last."
- **§4, L490–492:**
  - each agent gets a brief with only what its piece needs, and writes its result to a file;
  - the main agent keeps conclusions, not details;
  - stored knowledge carries a date and is rechecked before it is relied on;
  - knowledge is kept apart from state.
- **§4, L494–510:** project memory for software work is three append-only files in `docs/blueprint/`:
  `decisions.md`, `changelog.md` and `lessons.md`.
  - Each entry is about 5 lines, with a named writer and a "when".
  - Agents read only the entries their task touches, found by `grep`.
  - A lesson past its recheck date is marked stale.
- **§4, L512–514:** no store without a listed query, and "Not verified: Codex's memory and subagent features beyond
  `AGENTS.md`."
- **App. B, L541–553:** a list of memory kinds, each with its limit:
  - context window;
  - `CLAUDE.md`/`AGENTS.md`, loaded every session;
  - Claude Code auto-memory, "Only Claude Code reads it";
  - files in the repo;
  - skills;
  - run records, which "Nobody reads … unless asked";
  - a subagent's final report.
- **Skill, `SKILL.md` L85:** each node states "what it reads from the state file before starting and what it writes
  back".

**Not in the method** (*my reading*):
- When an agent's *own* memory writes happen, what they may hold, and whether they are on or off for a workflow's
  nodes.
- Codex memories, the API memory tool, Gemini/agy and opencode do not appear in App. B.
- No check on memory an agent writes, beyond "rechecked before it is relied on".
- The "agents skip optional reads" premise lives in `SOURCE_OF_TRUTH.md` Rd2.1 (L345), not in the method. Its basis in
  this repo was CodeCompass (E2; via `runs/20261011-project-memory-engines/nodes/claude.stdout.md` C21).

**A disagreement between two repo documents.** It is surfaced here and not resolved.
- Method §4 (L494–503) puts project memory in `docs/blueprint/{decisions,changelog,lessons}.md`, as append-only
  shared files.
- `docs/memory-system/SOURCE_OF_TRUTH.md` (accepted 2026-10-12) puts it in `project-memory/entries/` instead: one file
  per entry, five kinds, a generated `INDEX.md`, "agents never append to one shared file" (L107).

Which one a workflow design follows is EJ's call.

## 5. Implications for the method

These are options, not a verdict. Each is *my reading* of §1–§3. The costs are stated, and none is measured.

| id | Option | What it would say | Evidence it rests on | Cost |
|---|---|---|---|---|
| O0 | **No change** | The state file, the brief and "files in the repo" already make every must-read and must-write explicit. | M1/M2 hurt optional reads, and the method has none of those for a node's required inputs. | None now. Built-in memory (T2, T3, T6) keeps running beside the design, unplanned. |
| O1 | **Load, don't ask** (one line in §4) | A node's must-read files reach it through its brief, an import or a start hook, never through a sentence asking it to read them. | E1 (an instruction gave 95% invocation, not 100%), M1, M2, T1 L435, T4. `SOURCE_OF_TRUTH.md` Rd2.1 already says the same for project memory. | One sentence. A start hook per engine where a brief cannot carry the file. |
| O2 | **Writes are part of the return contract** | What a node must record (state, lessons, a `done:` line) is a field of its return and is checked like any output. The agent's judgement is not left to decide it. | M7 (progress file, feature list), M4, T6 (Codex keeps must-follow rules out of memories). | Already half there (SKILL.md L85). It adds a check per node. |
| O3 | **Memory an agent writes is a claim** | A memory written by an agent is not trusted until checked: an evaluator gate on what is kept, and a recheck before use. | E5 (evaluator-filtered addition +15–25 pts; it depends on the evaluator), E6, E3, M3. `SOURCE_OF_TRUTH.md` Rd5.1 covers "check before acting" for project memory. | Verifier time per write. A weak evaluator can make deletion worse (E5). |
| O4 | **Set each engine's built-in memory per node** | For each engine (`docs/EXECUTOR_KINDS.md`), record whether its own memory is on for workflow nodes. Claude auto memory is on by default in local sessions; subagent `memory` is opt-in; Codex memories are off by default. | T2, T3, T6. #40272 suggests injected memory can crowd out a designed read (*unproven*). | One row per engine, plus a decision by EJ. Turning built-in memory off loses what it would have kept. |
| O5 | **Refresh App. B** | Add Codex memories, the API memory tool, Gemini/agy and opencode (none), each with what loads and what the model decides. | §1 | Upkeep: these features changed within the last year (Gemini CLI was replaced 2026-06-18; Codex memories are recent). |

**On EJ's premise** ("memory and information are the two most important factors"): this report did not test that
ranking. *My reading*: E4, E7 and E10 suggest that *more* memory or context is not better by itself. The measured
gains came from *what reaches the agent and when*: E1 (loaded index 100% vs skill 53%) and E10 (verified experience
injected directly). That timing is a workflow decision, not something the agent manages for itself.

## 6. Experts' views

*Empty in v0. One subsection per expert will be added, in order: Linus (codex) → 范蠡 (Claude) → 孫子 (dsh) → 老子
(opencode). Each subsection keeps the expert's own words and labels, notes which report section it answers, and keeps
any disagreement with this report beside it, not merged in.*

### 6.1 Linus
### 6.2 范蠡
### 6.3 孫子
### 6.4 老子

## 7. Open questions

1. **How good is Claude Code's auto memory, or Codex memories?** That means recall when needed, precision of what is
   kept, and staleness. *Not measured*: no study found.
2. **Does a sentence in a brief ("read X first") work as well as loading X?** E1 measured it for one skill (95%
   invocation). No measurement was found for plain files or for this repo's engines.
3. **Do newer models skip fewer reads?** The evidence spans GPT-4o-mini to Opus 4.7. No source compares generations on
   the same task.
4. **Does built-in memory interfere with designed memory?** One user report (#40272) claims so. *Unproven.*
5. **What does Antigravity/agy actually load and write?** No official doc was read.
6. **Which project-memory layout does a designed workflow use?** Method §4 or `SOURCE_OF_TRUTH.md` (§4 above). This is
   EJ's decision.
7. **Do whales need per-agent memory at all?** EJ's agents are few and long-lived. Whether per-node memory pays for
   itself, against the state file plus a brief, is *not measured*.

### Gaps

- **Not read:**
  - the official Antigravity docs (none found by two searches);
  - Mem-α (arXiv 2509.25911, search summary only, so no row);
  - "Harness Engineering" (arXiv 2609.00006): its abstract had no memory content, and the full text was not read;
  - "Bad Memory" (arXiv 2607.14611) and "Memory as Infrastructure" (arXiv 2609.05510): seen in a search, not fetched.
- **Partly read:** the last 2,435 characters of 2505.16067v2, the last 75,714 of 2602.12670v4, the last 3,165 of
  2602.11988v3 and the last 31,009 of 2510.04618v3. All were fetched through WebFetch and summarised.
- **Version disagreement, kept apart:** a search summary gave SkillsBench as "+16.2 pp" over 84/86 tasks. The v4
  abstract fetch gave "+16.6 percentage points" over "87 tasks". E3 uses the v4 per-configuration numbers.
- **Budget:** 21 searches and 31 fetches. Raw text was saved for two sources (`sources/claude-code-memory.md`,
  `sources/claude-memory-tool.md`).

## Sources

| id | Source | Date | How read |
|---|---|---|---|
| S1 | Claude Code docs, "How Claude remembers your project" — https://code.claude.com/docs/en/memory | undated; fetched 2026-10-13 | raw text saved, `sources/claude-code-memory.md` (verified) |
| S2 | Claude Platform docs, "Memory tool" — https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | undated; fetched 2026-10-13 | full-text return, excerpts in `sources/claude-memory-tool.md` (verified, with that note) |
| S3 | Claude Code docs, sub-agents — https://code.claude.com/docs/en/sub-agents, via `runs/20261012-agent-memory-claude-code/notes.md` | notes 2026-10-12 | reported (that run's WebFetch reading) |
| S4 | Anthropic, "Effective context engineering for AI agents" — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2025-09-29 | WebFetch (reported). Not used for a row: background only ("CLAUDE.md files are naively dropped into context up front"; "structured note-taking, or agentic memory") |
| S5 | Anthropic, "Effective harnesses for long-running agents" — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | 2025-11-26 | WebFetch (reported) |
| S6 | Claude blog, "Managing context on the Claude Developer Platform" — https://claude.com/blog/context-management | 2025-09-29 | WebFetch (reported) |
| S7 | Anthropic, "How we built our multi-agent research system" — https://www.anthropic.com/engineering/multi-agent-research-system | 2025-06-13 | WebFetch (reported) |
| S8 | Anthropic, "Introducing Claude 4" — https://www.anthropic.com/news/claude-4 | 2025-05-22 | WebFetch (reported) |
| S9 | OpenAI Codex docs, AGENTS.md — https://learn.chatgpt.com/docs/agent-configuration/agents-md (redirected from developers.openai.com/codex/guides/agents-md) | undated | WebFetch (reported) |
| S10 | OpenAI Codex docs, Memories — https://learn.chatgpt.com/docs/customization/memories.md?surface=app (redirected from developers.openai.com/codex/memories.md) | undated | WebFetch (reported) |
| S11 | Gemini CLI docs, Memory — https://geminicli.com/docs/tools/memory | updated 2026-05-13 | WebFetch (reported) |
| S12 | Gemini CLI docs, GEMINI.md — https://geminicli.com/docs/cli/gemini-md | updated 2026-06-18 | WebFetch (reported) |
| S13 | opencode docs, Rules — https://opencode.ai/docs/rules/ | undated | WebFetch (reported) |
| S15 | Vercel, "AGENTS.md outperforms skills in our agent evals" — https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals | 2026-01-27 | WebFetch (reported) |
| S16 | Gloaguen et al., "Evaluating AGENTS.md…" — https://arxiv.org/abs/2602.11988 , https://arxiv.org/html/2602.11988v3 | v1 2026-02-12; v3 2026-09-29 | WebFetch (reported) |
| S17 | Li et al., "SkillsBench" — https://arxiv.org/abs/2602.12670 , https://arxiv.org/html/2602.12670v4 | v4 2026-06-14 | WebFetch (reported) |
| S18 | Xiong et al., "How Memory Management Impacts LLM Agents" — https://arxiv.org/abs/2505.16067 , https://arxiv.org/html/2505.16067v2 | v2 2025-10-10 | WebFetch (reported) |
| S19 | Zhang et al., "Agentic Context Engineering" — https://arxiv.org/abs/2510.04618 , https://arxiv.org/html/2510.04618v3 | v3 2026-03-29 | WebFetch (reported) |
| S20 | Hong, Troynikov, Huber, "Context Rot" — https://www.trychroma.com/research/context-rot | 2025-07-14 | WebFetch (reported) |
| S21 | Letta, "Context-Bench" — https://www.letta.com/blog/context-bench | 2025-10-30 | WebFetch (reported) |
| S22 | Fan et al., "VibeMemBench" — https://arxiv.org/abs/2609.23570 | 2026-09-20 | WebFetch (reported) |
| S23 | CodeCompass, arXiv 2602.20048, via `docs/research/20261011-agent-memory-graph-r2/FINDINGS-s3-project-graph.md` F33 | 2026-02-23 | repo row (reported) |
| S24 | MemoryArena (arXiv 2602.16313) and HaluMem (arXiv 2511.03506), via `docs/research/20261011-agent-memory-graph-r2/INDEX.md` s5-F6, s5-F5 | 2026-09-17 / 2026-01-05 versions | repo rows (reported) |
| S25 | GitHub issues anthropics/claude-code — https://github.com/anthropics/claude-code/issues/34763 , /40272 , /43098 | 2026-03-15, 2026-03-28, 2026-04-03 | WebFetch (reported) |
| S26 | This repo: `docs/WORKFLOW_DESIGN_METHOD.md` (§4 L480–514, App. B L541–553), `.claude/skills/workflow-design/SKILL.md` L85, `docs/memory-system/SOURCE_OF_TRUTH.md` (L107, L168, L345), `docs/research/20261011-agent-memory-graph-r2/DIGEST.md`, `runs/20261012-agent-memory-claude-code/notes.md` | 2026-10-11 to 2026-10-13 | read directly (verified) |

(S14 is unused: no official Antigravity source was found.)
