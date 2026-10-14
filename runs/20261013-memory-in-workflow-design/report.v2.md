# Do agents use memory well on their own? — research report

Version line: **v0** — researcher (Claude Opus 5.5), 2026-10-13. Web sources plus this repo's own memory research; 25
sources (list at the end). Later versions add a line each here.
**v1** — researcher (Claude Opus 5.5), 2026-10-13. Folds in expert 1, Linus (codex), in §6.1. Six of his claims were
checked: three are *verified*, against repo files; three are *reported*, two of them re-fetched for this version. His
answer brings two corrections, each marked "(v1, from Linus, checked: …)":
- E10: the benchmark kept only tasks where the injected experience had already helped.
- T6: the Codex memories page does not say which model decides what is stored.

His proposed §4 change is the new option O6. Also fixed: an id typo in v0 §2. Sources: 27.
**v2** — researcher (Claude Opus 5.5), 2026-10-13. Folds in expert 2, 范蠡 (Claude subagent, web allowed), in §6.2.
- Nine of his factual claims were checked against repo and home-folder files. All nine are *verified*, one with a
  qualification. His classical quotes come from his own rules list and were not checked.
- New option O7: the pointer plus O1's one sentence, smaller than O6. His O4 trigger is added to §5. New failure mode
  M14: this repo's own rule delivery to non-Claude nodes. Three of his questions are added to §7.
- He and Linus disagree on O6 versus O7; the two positions are kept side by side in §5 and §6.2.
- No corrections to earlier rows. Sources: 31.

**How to read the labels.**
- ***verified***: I read the source text myself and the quote is copied from it. The raw text is saved under `sources/`,
  or it is a repo file read directly.
- ***reported***: the quote or number came to me second-hand. That covers a WebFetch answer (a small model's summary
  of the page), a search-result summary, or a row from this repo's earlier research that I did not re-read at source.
- ***unproven***: the source asserts the claim and shows no evidence. This tag comes from `docs/RESEARCH_TAGS.md`.
- ***my reading***: an inference of mine.
- ***not measured***: nobody measured it; no source was found.

Experts and later versions should keep these labels and never upgrade one in place. Ids: **T** = tool behaviour (§1),
**E** = measured evidence (§2), **M** = failure mode (§3), **O** = option (§5), **S** = source, **L** = a claim of
Linus's checked in §6.1, **F** = a claim of 范蠡's checked in §6.2.

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

   (v1, from Linus, checked L2: the two tools write differently. Claude Code writes during the session, by its own
   judgement (T2, *verified*). Codex generates memories in the background from idle past chats, once enabled. Its page
   does not say whether the working model chooses what is stored (T6, *reported*).)
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
6. **Expert 1, Linus (v1):**
   - On the first question, "partly". Mechanisms exist, but reliable reading, writing and keeping are "not
     established".
   - On the second, "yes, one change". In §4, replace the project-memory prescription with a pointer to
     `SOURCE_OF_TRUTH.md`, plus a memory contract in each node's existing Context, Contract and State fields (O6).
   - He would add no further mechanism (O3–O5) without evidence of a problem it solves.

   *Quoted*, from §6.1.
7. **Expert 2, 范蠡 (v2):**
   - On the first question, "partly".
   - On the second, "yes, one small change", smaller than O6: a pointer to `SOURCE_OF_TRUTH.md` plus O1's one sentence,
     with no per-node contract (O7). He would wait on O3–O5 "until EJ's own runs show the harm they would fix".
   - On EJ's premise, memory's value lies in "**regulating** it", not "**filling** it".

   *Quoted*, from §6.2. He also found, and I checked (*verified*), that this repo hands its own rules to non-Claude
   nodes only through a words-only pointer, or only through Claude auto memory (M14). That is the gap O4 addresses,
   found here in the repo. It has caused no measured failure: *not measured*.

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
| T6 | **Codex — memories** | Generated memories are used in later threads when enabled (`use_memories`). | Nothing during the task. Codex builds memories "from eligible past chats in the background, skipping active or short sessions and redacting secrets".<br>**(v1, from Linus, checked L2:** the page, re-fetched, describes background generation after a chat "has been idle long enough". It "doesn't say" whether the model working on a task chooses what is stored. So v0's "Nothing during the task" was *my reading*, not the doc's wording. *Reported*.) | Off by default. Enabled with `memories = true`. Guidance: keep required team rules in `AGENTS.md`, and treat memories as a recall aid, "not the only source for rules that must always apply". | *reported*, S10 |
| T7 | **Gemini CLI (replaced by Antigravity CLI on 2026-06-18)** | Global `~/.gemini/GEMINI.md` and workspace `GEMINI.md` files. When a tool touches a directory, the CLI scans that directory and its ancestors for more GEMINI.md files ("JIT"). All found files are concatenated "with every prompt". | Saving: memory is written "with `write_file` or `replace`" into one of three tiers. The use cases listed are preferences, project decisions and aliases. | — | *reported*, S11, S12 |
| T8 | **opencode** | `AGENTS.md` (project, then global), with `CLAUDE.md` as a fallback. "The first matching file wins in each category." Files listed in the `instructions` field of `opencode.json`. | Files referenced inside `AGENTS.md`: "opencode doesn't automatically parse file references". The docs' workaround tells the agent to "use your Read tool to load it on a need-to-know basis". | No built-in memory feature is mentioned. | *reported*, S13 |
| T9 | **Antigravity / `agy`** | Third-party sources only. They say it reads `AGENTS.md` and `GEMINI.md`, and that "Knowledge Items" are generated automatically from conversations. | — | — | *not measured*: no official doc was read (see §7 and Gaps) |

**Across the tools** (*my reading* of T1–T9): the harness loads instruction files and memory indexes. Everything
past the index is left to the model's judgement, mid-task. The only exception is Codex memories, which are written in
the background by the harness, not by the working model. No tool lets the model choose *whether to read the index*:
every vendor forces that read.

(v1, from Linus, checked L2: the doc supports "in the background". It does not say "not by the working model".
That part stays *my reading*. The v0 summary of the page listed separate `extract_model` and `consolidation_model`
settings, which fits that reading but does not settle it.)

(v2, 范蠡 reads this paragraph through his rule #1. "Heaven's time" is what the engine forces. "Human affairs" is what
the designer delivers. The model's mid-task judgement is neither. *His reading*, §6.2.)

## 2. Evidence on how well they do it

Measured results come first. Every row is second-hand (WebFetch or earlier repo research) unless marked *verified*.
"Our" models (Claude Code, Codex, Gemini CLI) appear in E3 and E4. (v1 correction: v0 said "E1, E3, E4 and E21". There
is no E21, and E1 names no models.)

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
| E10 | On real repository tasks, full memory systems mostly did not help: 11 of 12 solver/system pairings did not beat the memory-off baseline. Injecting verified past experience directly raised resolution on four of five solvers, by 1.1 to 4.5 pp, and lowered steps on all five.<br>**(v1, from Linus, checked L1:** the benchmark kept a task only if injected experience had already improved it. Abstract: "Each target is retained only when injected history experience improves its executable outcome in a reference setting". So the direct-injection gain is measured on tasks selected because injection helps. It does not show that injecting experience helps in general. The abstract says "reference setting"; Linus's "reference solver" is not its wording. *Reported*.) | reported | S22, VibeMemBench arXiv 2609.23570, 2026-09-20 | "eleven of twelve solver and system pairings fail to exceed the matched memory-off baseline" |
| E11 | Agents that come close to saturating LoCoMo perform poorly in multi-session agent loops (MemoryArena). Hallucinations build up at memory extraction and updating, and carry into answers (HaluMem). | reported (repo rows s5-F6, s5-F5, 2026-10-11 tags) | S24 (MemoryArena arXiv 2602.16313; HaluMem arXiv 2511.03506) | — (not re-read) |
| E12 | Anthropic states that Opus 4 "becomes skilled at creating and maintaining 'memory files'" when given local file access. The post gives no measurement. | reported; the capability claim itself is *unproven* | S8, Anthropic "Introducing Claude 4", 2025-05-22 | "Claude Opus 4 also dramatically outperforms all previous models on memory capabilities." |

**Where the evidence is thin** (*my reading*):
- None of E1–E12 measures the thing EJ asked about most directly: whether Claude Code's auto memory, or Codex memories,
  pick the right things to keep and recall them when needed. That is *not measured* (§7).
- E1 and E2 measure the agent invoking optional *tools or skills*, not reading optional *files*. They are the closest
  measurements found. (v1: Linus makes the same point about E1. It "concerns discovery of a documentation skill and
  index, not every kind of memory".)
- E1, E8 and E12 are vendor numbers with no published harness.
- Model generations differ:
  - E3 uses Opus 4.7 and GPT-5.5;
  - E4 uses Sonnet 4.5 and GPT-5.2;
  - E5 uses GPT-4o-mini;
  - E1 does not name its models.

  A newer model may skip reads less often. No source settles that.
- (v1, from Linus, checked L1) E10's positive direct-injection result holds only for tasks selected because
  injection helped there (see the E10 row).
- (v2, 范蠡) E4 shows that loaded files are *followed*. Nothing measured shows that following them *improves
  outcomes*: the developer-written files' +2.4% has p=21%. This agrees with the E4 row as written.

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
| M13 | (v1, from Linus, *my reading* in his words, not checked against any measurement) **Stored notes can leak a worker's reasoning to its verifier.** If memory is selected without respecting the method's information boundaries, the verifier may see what it must not. | §6.1, Linus "Costs and risks". The boundary itself is in method §4 L484–485 and SKILL.md L82 (*verified*). | *my reading* (Linus's); *not measured* |
| M14 | (v2, from 范蠡, checked F2–F6) **In this repo, the folder rules reach a non-Claude node only if the model chooses to read them, and some rules never reach it.** Two cases:<br>• `AGENTS.md` is a words-only pointer: "The instructions for this folder are in `CLAUDE.md` … Read it first". Codex loads `AGENTS.md` (T5), and `~/.codex/config.toml` sets no fallback filename. opencode uses only `AGENTS.md` when both files exist (T8). So for these engines `CLAUDE.md` arrives only if the model decides to open it, which is the M1 / T1 L435 pattern.<br>• At least one of EJ's working rules, "Stay in own scope", exists only in the main session's Claude auto memory. Method App. B says "Only Claude Code reads it". | The facts are *verified* (F2–F6, S30–S32). That a non-Claude node gets neither by load is *my reading* on *verified* and *reported* (T5, T8) premises. That any node has failed because of it is *not measured*, as 范蠡 says himself. | verified (facts); *not measured* (harm) |

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

(v1, from Linus, checked L3: Linus resolves this disagreement toward `SOURCE_OF_TRUTH.md`. His reason is that "the
brief establishes `SOURCE_OF_TRUTH.md` as accepted". Both premises check out:
- the run's `question.md` L10 calls it "EJ's project memory design, accepted";
- its status line, L3, reads "accepted by EJ on 2026-10-12".

Both are *verified*. That the accepted design should therefore *replace* method §4's prescription is Linus's reading.
Neither document says so. The decision remains EJ's.)

(v2, from 范蠡, checked F1: `SOURCE_OF_TRUTH.md` is accepted but **not built**. A Glob for `project-memory/**` in the
repo finds no files, which is *verified*. Without a shell I could not tell an empty directory from a missing one. A
pointer to it therefore leads, for now, to rules with no store behind them. 范蠡 also resolves toward SoT, and his
reason is timing: the contradiction already exists, and S1 L90 says conflicting instructions are picked
"arbitrarily". Linus's reason is the document's status. The decision remains EJ's.)

## 5. Implications for the method

These are options, not a verdict. Each is *my reading* of §1–§3. The costs are stated, and none is measured.

| id | Option | What it would say | Evidence it rests on | Cost |
|---|---|---|---|---|
| O0 | **No change** | The state file, the brief and "files in the repo" already make every must-read and must-write explicit. | M1/M2 hurt optional reads, and the method has none of those for a node's required inputs. | None now. Built-in memory (T2, T3, T6) keeps running beside the design, unplanned. |
| O1 | **Load, don't ask** (one line in §4) | A node's must-read files reach it through its brief, an import or a start hook, never through a sentence asking it to read them. | E1 (an instruction gave 95% invocation, not 100%), M1, M2, T1 L435, T4. `SOURCE_OF_TRUTH.md` Rd2.1 already says the same for project memory. | One sentence. A start hook per engine where a brief cannot carry the file. |
| O2 | **Writes are part of the return contract** | What a node must record (state, lessons, a `done:` line) is a field of its return and is checked like any output. The agent's judgement is not left to decide it. | M7 (progress file, feature list), M4, T6 (Codex keeps must-follow rules out of memories). | Already half there (SKILL.md L85). It adds a check per node. |
| O3 | **Memory an agent writes is a claim** | A memory written by an agent is not trusted until checked: an evaluator gate on what is kept, and a recheck before use. | E5 (evaluator-filtered addition +15–25 pts; it depends on the evaluator), E6, E3, M3. `SOURCE_OF_TRUTH.md` Rd5.1 covers "check before acting" for project memory. | Verifier time per write. A weak evaluator can make deletion worse (E5). |
| O4 | **Set each engine's built-in memory per node** | For each engine (`docs/EXECUTOR_KINDS.md`), record whether its own memory is on for workflow nodes. Claude auto memory is on by default in local sessions; subagent `memory` is opt-in; Codex memories are off by default. | T2, T3, T6. #40272 suggests injected memory can crowd out a designed read (*unproven*). (v2: M14 is the same gap found inside this repo, *verified*; no harm measured.) | One row per engine, plus a decision by EJ. Turning built-in memory off loses what it would have kept. |
| O5 | **Refresh App. B** | Add Codex memories, the API memory tool, Gemini/agy and opencode (none), each with what loads and what the model decides. | §1 | Upkeep: these features changed within the last year (Gemini CLI was replaced 2026-06-18; Codex memories are recent). |
| O6 | (v1, **Linus's proposal**) **A memory contract per node, pointing at the accepted design.** This combines O1 and O2. | Linus's text, quoted: "For task and project memory, the workflow designer **SHOULD** specify each node's memory inputs, delivery mechanism and timing, required outputs and write timing, and checks in its existing Context, Contract and State fields, following the accepted Write, Keep and Read policy." It *replaces* §4's own project-memory prescription (L494–510) with a pointer to `SOURCE_OF_TRUTH.md`. | O1/O2's evidence. The fields already exist (SKILL.md L81–85, *verified*). The accepted design already has check-before-use, superseded claims kept and contradictions reported (SoT Rd5.1 L383, K4.1/K4.3 L301–307, Rd5.3 L386, *verified*). | Linus: "more brief preparation, input tokens and checking time. The amount is **not measured**." Also: "delivering memory does not establish that the agent understood or followed it". Time spent on unneeded contracts is not recovered. A §4 paragraph is reversible. |
| O7 | (v2, **范蠡's proposal**) **Pointer plus O1's one sentence, with no per-node contract.** This is O1 plus the pointer half of O6. | Replace §4 L494–510 with a pointer to `SOURCE_OF_TRUTH.md`, plus, quoted: *"a node's must-read memory reaches it through its brief, an import or a start hook, never as a request to read it."*<br>**Interim, his Q3:** if SoT is not built before the next workflow that needs project memory, "keep §4's three files, marked 'until SoT is built', and change only the one sentence". | O1's evidence. Timing and checks are already in SoT (Rd2.1 L344, Rd5.1 L383, *verified*). Node inputs and writes are already in SKILL.md L82–85 (*verified*). Reason for keeping it small: his #13/#10 and "anything the method adds about memory should **narrow** what a node gets, never widen it". | 范蠡: "the pointer depends on a design that has not been built" (F1); "the sentence may cost brief tokens and buy nothing" (*not measured*); a start hook per engine; "some nodes' memory needs go unstated", e.g. a verifier that must *not* get certain entries (M13). These must then be carried case by case, and "the method will not prompt for it". |

**O6 against O7: kept side by side, not merged.**
- **Linus (O6):** each node states its memory inputs, delivery and timing, outputs and write timing, and checks, in
  its existing fields.
- **范蠡 (O7):** "Repeating SoT's rules in every node is a second copy … Since SoT governs timing and checks, the
  contract he wants already exists, once."
- **What they share:** both point §4 at SoT, both include O1's delivery rule, and both wait on O3–O5.

*My reading* of the crux, which neither expert states this way. SoT Rd2.1 fixes the *session-start* reads of *project*
memory: `AGENTS.md`, `INDEX.md`, the `work/` listing and the task's `state.md`. It does not say which entries a given
workflow node's brief carries, or which a verifier must be denied. So under O7 the per-node part rests on the existing
Context and State fields, filled without a memory prompt. That is the gap 范蠡 names as his last cost. Which matters
more is *not measured*: the cost of a second copy in every node (his view), or the cost of unprompted omissions (what
O6 guards against). Linus's matched-task test (§6.1), narrowed as 范蠡 proposes in §6.2, would compare the two.

**Linus on O3–O5** (v1, *quoted*, §6.1): "an additional evaluator, automatic expiry or per-engine memory controls
would each need evidence of a problem they solve". He holds that the accepted design already covers checking, keeping
superseded claims and reporting contradictions.

*My reading*, kept beside his view and not merged into it: `SOURCE_OF_TRUTH.md` "covers task and project memory" (L70,
*verified*). It says nothing about an engine's own built-in memory (T2, T3, T6) beyond how another agent may read it
(Rd4.5). So the problem O4 addresses, built-in memory running beside a designed workflow, lies outside both the
accepted design and O6. O6's wording also scopes itself to "task and project memory". Whether that gap needs anything
is open: the only evidence it causes harm is an *unproven* user report (#40272).

**范蠡 on O3–O5** (v2, *quoted*, §6.2): wait "until EJ's own runs show the harm they would fix". #40272 is "a sprout,
not a visible form". He agrees with Linus "by a different rule". He also names the cost of waiting: "If the gap … is
already causing silent rule breaks, every run until it is noticed pays for it."

His **trigger for O4**, quoted: "Has a Codex, agy or opencode node ever broken a rule that existed only in Claude auto
memory or only in `CLAUDE.md`? If yes, the time has come for O4 … Add a row per engine to `docs/EXECUTOR_KINDS.md`, and
have such rules loaded into the brief. If no, keep waiting." He is wrong, by his own test, if "a run's evidence shows a
node acting on memory that a Claude-only or words-only channel failed to deliver, or on built-in memory that
contradicted the state file".

*My reading*: M14 makes that trigger checkable today. The rule "Stay in own scope" and the words-only `AGENTS.md` are
concrete things to look for in past non-Claude runs' evidence. No such check has been run.

**On EJ's premise** ("memory and information are the two most important factors"): this report did not test that
ranking. *My reading*: E4, E7 and E10 suggest that *more* memory or context is not better by itself. The measured
gains came from *what reaches the agent and when*: E1 (loaded index 100% vs skill 53%) and E10 (verified experience
injected directly). That timing is a workflow decision, not something the agent manages for itself.

(v1, from Linus, checked L1: E10's gain was measured on tasks selected because injection helped, so it supports this
reading less than v0 implied. Linus's own conclusion: "these results justify testing deliberate delivery; they do not
establish that loading more memory universally improves work". He also says his recommendation "does not depend on
that ranking".)

(v2, 范蠡: "I agree that memory matters. My rules say its value is in **regulating** it, meaning what reaches which node
and when. **Filling** it, meaning loading more, is not where the value is." He cites E4, E5, E6 and E7, all
*reported*, as "all negative" on more memory. He *agrees* with EJ that memory matters, and *disagrees* that more of it
is the lever.)

## 6. Experts' views

*One subsection per expert, in order: Linus (codex) → 范蠡 (Claude) → 孫子 (dsh) → 老子 (opencode). Each subsection keeps
the expert's own words and labels, notes which report section it answers, and keeps any disagreement with this report
beside it, not merged in.*

### 6.1 Linus

Source: `experts/answers/linus.md` (S27, read directly). His labels are kept: "my reading", "not measured", and "my #N"
for his own numbered rules.

**Answer, quoted:** "**My reading: partly**—agents have memory mechanisms, but reliable decisions about reading,
writing and keeping memory across these engines are not established. **Yes**—make one change to §4: replace its
project-memory prescription with a reference to EJ's accepted design and an explicit memory contract in each node's
existing fields."

**What he responds to, point by point:**

| Report section | His point (quoted where it matters) | Agrees / disagrees with the report |
|---|---|---|
| §1, §2, §7 | "separate capability from demonstrated reliability. Report §1 describes mechanisms; §2 and §7 leave their practical quality unmeasured." Codex memories are background-generated, "so this is not simply the working model independently deciding what to remember". | Agrees with Short answer 2. He sharpens T6: see L2, which corrected v0's T6 cell. |
| §5 / O1, §2 E1, E10 | E1 "concerns discovery of a documentation skill and index, not every kind of memory". VibeMemBench "selected tasks where injected experience had already helped a reference solver". "**My reading:** these results justify testing deliberate delivery; they do not establish that loading more memory universally improves work." | Partly disagrees: E10 was used too strongly in v0's "On EJ's premise" paragraph. Folded in as a v1 correction (L1). |
| §4 | Context, Contract, Evidence and State "already describe inputs, outputs and checks. Memory can use those fields." On the layout disagreement, he "references that policy instead of maintaining another prescription". | Settles the §4 disagreement toward SoT. The report keeps that as EJ's call (§4, v1 note). |
| §5 / O1, O2 | The proposed replacement for §4 is O6 above. | New option. |
| §5 / O3–O5 | "an additional evaluator, automatic expiry or per-engine memory controls would each need evidence of a problem they solve." "connecting that policy to node contracts is the immediate need." | Disagrees with adopting O3–O5 now. The researcher's note on what SoT does not cover is beside it in §5. |
| (EJ's premise) | "EJ's ranking of memory and information is also **not measured**; this recommendation does not depend on that ranking." | Agrees that it is untested. |

**His self-check of the proposal.** He says it passes all eight `requirement-check` items, among them "basis (a
proposal, n=0, reviewed after the test below)", and its "performance benefit remains **not measured**". This check was
written and passed by Linus himself, so it is not independent evidence. Per `CLAUDE.md`, "a check I wrote and then
passed is not independent evidence".

**His question for EJ, quoted:** "What additional token cost or elapsed time would EJ accept for fewer missed
decisions and better handoffs? That answer determines whether the proposed change earns its ongoing cost."

**Costs and risks he names, quoted:**
- "more brief preparation, input tokens and checking time. The amount is **not measured**."
- "delivering memory does not establish that the agent understood or followed it."
- "memory selection must respect the existing information boundaries; a verifier could otherwise receive the worker's
  reasoning through stored notes." (This is M13.)
- "the method paragraph is reversible, but time already spent preparing unnecessary contracts is not recovered."

**His proposed test** (his own; summarised, with key words quoted). Compare the current method against the explicit
contract "on matched repository tasks, keeping the engine, model and memory settings fixed". The tasks include a
fresh-session handoff, a relevant prior decision, and "an entry contradicted by current code". Measure task outcomes,
memory mistakes, tokens and elapsed time. "Contract completeness alone would not establish that."

**His new factual claims, checked by the researcher (v1):**

| id | Linus's claim | Check | Label |
|---|---|---|---|
| L1 | VibeMemBench "selected tasks where injected experience had already helped a reference solver". | Re-fetched abstract: "Each target is retained only when injected history experience improves its executable outcome in a reference setting". The selection is confirmed. The abstract says "reference setting", not "solver". This **corrects** how v0 used E10 (§2, §5). | reported (S22, re-fetched via WebFetch) |
| L2 | The current OpenAI docs show Codex generates memories in the background, "not simply the working model independently deciding". | Re-fetched https://learn.chatgpt.com/docs/customization/memories: background generation after a chat is "idle long enough". The page "doesn't say" whether the working model chooses what is stored. The background part is confirmed; "not the working model" is not stated. This **corrects** v0's T6 cell wording. | reported (S10, re-fetched via WebFetch) |
| L3 | "the brief establishes `SOURCE_OF_TRUTH.md` as accepted". | `question.md` L10: "EJ's project memory design, accepted". SoT L3: "accepted by EJ on 2026-10-12". | verified (S28, S26) |
| L4 | The accepted design "already specifies checking before use, preserving superseded claims, and reporting contradictions". | SoT Rd5.1 (L383), K4.1/K4.3 (L301–307), Rd5.3 (L386). Scope: task and project memory only (L70). | verified (S26) |
| L5 | The node fields Context, Contract, Evidence and State "already describe inputs, outputs and checks". | SKILL.md L82–85 holds exactly those four rows; L81 is Tools. | verified (S26) |
| L6 | E1 is about discovering a docs skill and index, not all memory. | Matches the E1 row (S15). | reported (S15, unchanged) |

### 6.2 范蠡

Source: `experts/answers/fan-li.md` (S29, read directly). His labels are kept: *quoted*, *reported*, *verified*, *my
reading*, *not measured*, and "my #N" for his own numbered rules. His classical Chinese quotes (「天道盈而不溢」,
「夫謀之廊廟，失之中原，其可乎？」, 「得時無怠」, 「究數而止」, 「越用其五而得意」, 「逆節萌生。天地未形」, 「王無蚤圖」,
「天予不取，反為之災」) come from his own rules list. The researcher did not check them against any classical text;
that is out of scope.

**Answer, quoted:**
- "**Question 1: partly.** The harness forces some reads, and those happen. Everything the model decides for itself,
  such as opening an optional file, choosing what to keep or rewriting what it kept, is unreliable or *not measured*
  (report §1, §2)."
- "**Question 2: yes, one small change.** It is smaller than Linus's O6. In method §4, replace the three-file
  project-memory paragraph (L494–510) with a pointer to `docs/memory-system/SOURCE_OF_TRUTH.md`, plus O1's one sentence
  … Wait on O3–O5 until EJ's own runs show the harm they would fix."

**What he responds to, point by point:**

| Report section | His point (quoted where it matters) | Agrees / disagrees |
|---|---|---|
| §1 "Across the tools" | Harness reads are "Heaven's time"; what the designer delivers is "human affairs"; the model's mid-task judgement is neither. "That is the vendors themselves not trusting the model's timing." (*my reading*, his) | Agrees with Short answer 1 and 4. |
| §2 E1, §1 T6 → O1 | "give timing to the harness and the brief, and leave content judgement to the model. That is O1." | Agrees with O1. |
| §5 "On EJ's premise"; E4–E7 | More memory is "keeping the full", while memory at the right time is "regulating affairs". "anything the method adds about memory should **narrow** what a node gets, never widen it." | Agrees with the report's reading and adds the consequence. Partly disagrees with EJ's premise as stated. |
| §4 disagreement; S1 L90 | "The contradiction is already here, so EJ should not wait to fix it … My reason is the timing, not the documents' status." | Same conclusion as Linus, different reason. |
| §5 O6 (Linus) | "Repeating SoT's rules in every node is a second copy. So my change is the pointer plus one sentence, not a per-node contract." | **Disagrees with Linus.** Both views are kept in §5. |
| §4 / SoT status | "SoT is accepted but not built … Pasting SoT into the method would spread an untried design further. A pointer keeps one copy." | Adds a fact (F1) and a reason to point rather than copy. |
| §5 O3–O5; M2 #40272 | Wait: #40272 "is a sprout, not a visible form". "On this I agree with Linus, by a different rule." | Agrees with Linus on waiting. |
| §3 / O4: "something the report misses" | `AGENTS.md` here is a words-only pointer; some of EJ's rules live only in Claude auto memory. "This is the O4 gap made concrete … What it does not establish: that any node has failed because of it." | Adds M14. He names the limits of his own check. |

**His three questions for EJ, quoted in substance; they are also in §7:**
1. "Has a Codex, agy or opencode node ever broken a rule that existed only in Claude auto memory or only in
   `CLAUDE.md`?" If yes, O4 is due; if no, keep waiting.
2. "Should `AGENTS.md` import `CLAUDE.md`'s content rather than ask the agent to read it?" If EJ's workflows use Codex
   or opencode nodes, the one-sentence rule covers it; if they do not, "it does not matter".
3. "Is SoT going to be built before the next designed workflow that needs project memory?" If not, keep §4's three
   files "marked 'until SoT is built'" and change only the one sentence.

**Costs and risks he names, quoted:**
- "the pointer depends on a design that has not been built".
- "the sentence may cost brief tokens and buy nothing. *Not measured.*"
- a start hook per engine is "setup and upkeep for each engine".
- "Waiting on O4 has a price too … every run until it is noticed pays for it. Watching for the sign is cheap, but
  someone has to look."
- "Being smaller than O6 means some nodes' memory needs go unstated … the method will not prompt for it."

**How he would know he was right** (summarised):
1. For the pointer: no new design file in `runs/` cites §4's three files or asks EJ which layout to use. "grep the next
   three design files."
2. For "load, don't ask": in the next non-Claude design, check that every must-read file reached the engine by brief,
   import or hook, and compare missed reads with one earlier ask-only run. This is "Linus's matched-task test …
   narrowed to one variable: delivery method".
3. For waiting: he is wrong if a run shows a node acting on memory that a Claude-only or words-only channel failed to
   deliver.

**His factual claims, checked by the researcher (v2):**

| id | 范蠡's claim | Check | Label |
|---|---|---|---|
| F1 | "`ls project-memory` in the repo returns 'No such file or directory'". SoT is not built. | Glob `project-memory/**` under `/home/smoke01/dev/ancient-games` returned no files. I had no shell to run `ls`, so an empty directory and a missing one look the same here. Either way, no entry and no `INDEX.md` exist. | verified (no files), with that qualification |
| F2 | `AGENTS.md` here is a words-only pointer: "The instructions for this folder are in `CLAUDE.md` … Read it first". | `AGENTS.md` L3: "The instructions for this folder are in `CLAUDE.md`, next to this file. Read it first; it applies to every agent and tool, not only Claude Code." The whole file is 4 lines. | verified (S30) |
| F3 | For Codex and opencode nodes, folder rules arrive only if the model opens `CLAUDE.md`. | Premises: F2 (*verified*); Codex loads `AGENTS.md` (T5, *reported*); `~/.codex/config.toml` has no `fallback`/`project_doc` setting (grep, *verified*, S32); opencode with both files present "only `AGENTS.md` is used" (T8, *reported*). The conclusion is *my reading* (and his). | *my reading* on verified and reported premises |
| F4 | Claude auto memory at `~/.claude/projects/-home-smoke01-dev-ancient-games/memory/` has "36 index lines". | `MEMORY.md` there has 36 lines, one per entry. | verified (S31) |
| F5 | Grepping `AGENTS.md`, `CLAUDE.md` and `docs/` for "Stay in own scope" finds nothing. | A case-insensitive grep of the whole repo finds the phrase only in `experts/answers/fan-li.md`. A grep for "own scope" in `AGENTS.md`, `CLAUDE.md` and `docs/**` also finds nothing. The rule lives in `memory/stay-in-own-scope.md` (type `feedback`, modified 2026-10-12). *My note:* a broader, related rule, "Touch only what you must", is in the user-level `/home/smoke01/CLAUDE.md` (Rule 3). That file is outside the repo, Claude Code loads it, and Codex does not. | verified (S31, S26) |
| F6 | Method App. B says of auto memory "Only Claude Code reads it". | Method L549. | verified (S26) |
| F7 | SoT L344 is Rd2.1 (reads at session start); L383 is Rd5.1 (check before acting). | L344: "**Rd2.1** At session start, an agent reads `AGENTS.md`, `INDEX.md`, the `work/` listing and its task's `state.md`." L383: "**Rd5.1** Before acting on something read from memory, the agent checks it against the code, test or commit it points to." | verified (S26) |
| F8 | SKILL.md L82–85 holds the node fields; State is "what it reads from the state file before starting and what it writes back". | SKILL.md L85, exact wording. | verified (S26) |
| F9 | S1 L90: given conflicting instructions, "Claude may pick one arbitrarily". | `sources/claude-code-memory.md`, L90. | verified (S1) |

### 6.3 孫子
### 6.4 老子

## 7. Open questions

1. **How good is Claude Code's auto memory, or Codex memories?** That means recall when needed, precision of what is
   kept, and staleness. *Not measured*: no study found.
2. **Does a sentence in a brief ("read X first") work as well as loading X?** E1 measured it for one skill (95%
   invocation). No measurement was found for plain files or for this repo's engines. (v2: 范蠡's narrowed test in §6.2
   would measure this on EJ's runs.)
3. **Do newer models skip fewer reads?** The evidence spans GPT-4o-mini to Opus 4.7. No source compares generations on
   the same task.
4. **Does built-in memory interfere with designed memory?** One user report (#40272) claims so. *Unproven.*
5. **What does Antigravity/agy actually load and write?** No official doc was read.
6. **Which project-memory layout does a designed workflow use?** Method §4 or `SOURCE_OF_TRUTH.md` (§4 above). This is
   EJ's decision. (v1: Linus proposes `SOURCE_OF_TRUTH.md`, O6. v2: 范蠡 agrees, O7, with an interim while SoT is
   unbuilt; F1.)
7. **Do whales need per-agent memory at all?** EJ's agents are few and long-lived. Whether per-node memory pays for
   itself, against the state file plus a brief, is *not measured*.
8. (v1, Linus) **What extra token cost or elapsed time would EJ accept** for fewer missed decisions and better
   handoffs? The answer decides whether O6 earns its cost.
9. (v1, Linus) **Does O6 beat the current method on matched tasks?** His proposed test is in §6.1. *Not run.* (v2:
   it would also settle O6 against O7, §5.)
10. (v1, *my reading*) **Is an engine's own built-in memory left out of scope on purpose?** O6 and `SOURCE_OF_TRUTH.md`
    cover task and project memory only. Is that deliberate, or a gap (O4)?
11. (v2, 范蠡) **Has a Codex, agy or opencode node ever broken a rule that existed only in Claude auto memory or only in
    `CLAUDE.md`?** This is his trigger for O4. It is checkable against past runs' evidence, using M14's concrete
    cases. *Not checked.*
12. (v2, 范蠡) **Should `AGENTS.md` carry or import `CLAUDE.md`'s content** instead of asking the agent to read it?
    Today it asks in words (F2). *My note*, on *reported* premises: neither Codex nor opencode has an `@` import in
    `AGENTS.md` (T5, T8). Codex has `project_doc_fallback_filenames`, which is not set here (S32). opencode has an
    `instructions` field.
13. (v2, 范蠡) **Will SoT be built before the next designed workflow that needs project memory?** If not, O7's interim
    applies (F1).

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
- **v1, not read:** VibeMemBench's full text. Whether its "reference setting" is a single solver is not settled; the
  abstract does not say.
- **v2, not done:**
  - No shell was available, so F1 could not separate an empty `project-memory/` directory from a missing one.
  - Past non-Claude runs were not searched for a broken "Stay in own scope" or other auto-memory-only rule (Q11).
  - 范蠡's classical quotes were not checked.
- **Budget:**
  - v0: 21 searches and 31 fetches.
  - v1: 0 searches and 2 fetches.
  - v2: 0 web calls, and these repo and home checks: 2 Globs, 3 Greps, 3 Reads (`AGENTS.md`, auto-memory `MEMORY.md`,
    `stay-in-own-scope.md`) and 1 grep of `~/.codex/config.toml`.

  Raw text was saved for two sources (`sources/claude-code-memory.md`, `sources/claude-memory-tool.md`).

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
| S10 | OpenAI Codex docs, Memories — https://learn.chatgpt.com/docs/customization/memories.md?surface=app (redirected from developers.openai.com/codex/memories.md); v1 re-fetch: https://learn.chatgpt.com/docs/customization/memories | undated | WebFetch (reported) |
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
| S22 | Fan et al., "VibeMemBench" — https://arxiv.org/abs/2609.23570 | 2026-09-20 | WebFetch (reported); abstract re-fetched in v1 for the selection rule |
| S23 | CodeCompass, arXiv 2602.20048, via `docs/research/20261011-agent-memory-graph-r2/FINDINGS-s3-project-graph.md` F33 | 2026-02-23 | repo row (reported) |
| S24 | MemoryArena (arXiv 2602.16313) and HaluMem (arXiv 2511.03506), via `docs/research/20261011-agent-memory-graph-r2/INDEX.md` s5-F6, s5-F5 | 2026-09-17 / 2026-01-05 versions | repo rows (reported) |
| S25 | GitHub issues anthropics/claude-code — https://github.com/anthropics/claude-code/issues/34763 , /40272 , /43098 | 2026-03-15, 2026-03-28, 2026-04-03 | WebFetch (reported) |
| S26 | This repo: `docs/WORKFLOW_DESIGN_METHOD.md` (§4 L480–514, App. B L541–553), `.claude/skills/workflow-design/SKILL.md` L81–85, `docs/memory-system/SOURCE_OF_TRUTH.md` (L3, L70, L107, L168, L301–307, L344, L345, L383, L386), `docs/research/20261011-agent-memory-graph-r2/DIGEST.md`, `runs/20261012-agent-memory-claude-code/notes.md`; repo-wide greps for "Stay in own scope" / "own scope" (v2) | 2026-10-11 to 2026-10-13 | read directly (verified) |
| S27 | Linus (codex), `runs/20261013-memory-in-workflow-design/experts/answers/linus.md` | 2026-10-13 | read directly (verified as to what he wrote) |
| S28 | `runs/20261013-memory-in-workflow-design/question.md` (L10) | 2026-10-13 | read directly (verified) |
| S29 | 范蠡 (Claude subagent), `runs/20261013-memory-in-workflow-design/experts/answers/fan-li.md` | 2026-10-13 | read directly (verified as to what he wrote) |
| S30 | This repo's `AGENTS.md` (4 lines; L3 quoted) | read 2026-10-13 | read directly (verified) |
| S31 | Claude auto memory for this project: `~/.claude/projects/-home-smoke01-dev-ancient-games/memory/MEMORY.md` (36 lines) and `stay-in-own-scope.md` | read 2026-10-13 | read directly (verified) |
| S32 | `~/.codex/config.toml`: grep for `fallback\|project_doc`, no match | checked 2026-10-13 | read directly (verified, absence of the setting only) |

(S14 is unused: no official Antigravity source was found.)
