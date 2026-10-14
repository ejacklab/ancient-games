# Do agents use memory well on their own? — research report

**Versions.** Each line names what was added; the details are in the sections.
- **v0** — researcher (Claude Opus 5.5), 2026-10-13. Web sources plus this repo's own memory research. 25 sources.
- **v1** — Folds in expert 1, Linus (codex), §6.1. 6 claims checked. Two corrections: E10's task selection, and the
  wording of T6. New option O6. Fixed an id typo in §2. 27 sources.
- **v2** — Folds in expert 2, 范蠡 (Claude subagent, web allowed), §6.2. 9 claims checked, all *verified*. New option O7,
  new failure mode M14, new questions Q11–Q13. 31 sources.
- **v3** — Folds in expert 3, 孫子 (dsh / DeepSeek), §6.3. 7 claims checked. One correction: the denial principle
  already exists at SKILL.md L82. New option O8, new question Q14. 32 sources.
- **v4 (final)** — Folds in expert 4, 老子 (opencode / MiniMax), §6.4. 9 claims checked, 7 *verified*. Two corrections:
  the W4.1 wording, and "two copies" of the state template. New option O9, new questions Q15–Q17. The Short answer
  now shows all four experts' final positions. §5 has one comparison table for O6–O9. Repetition is tightened; no label
  or source is dropped. 35 sources.

**How to read the labels.**
- ***verified***: I read the source text myself and the quote is copied from it. The raw text is saved under `sources/`,
  or the source is a repo or home file I read directly.
- ***reported***: the quote or number came to me second-hand. That covers a WebFetch answer (a small model's summary
  of the page), a search-result summary, or a row from this repo's earlier research that I did not re-read at source.
- ***unproven***: the source asserts the claim and shows no evidence. This tag comes from `docs/RESEARCH_TAGS.md`.
- ***my reading***: an inference of mine.
- ***not measured***: nobody measured it; no source was found.

Labels are never upgraded in place. Ids:

| Prefix | Meaning |
|---|---|
| **T** | tool behaviour (§1) |
| **E** | measured evidence (§2) |
| **M** | failure mode (§3) |
| **O** | option (§5) |
| **S** | source |
| **L** / **F** / **Z** / **LZ** | a claim by Linus / 范蠡 / 孫子 / 老子, checked in §6.1 / §6.2 / §6.3 / §6.4 |

## Short answer (final, v4)

### What the evidence says

1. **Reading: the harness does it, the model mostly does not.**
   - Each tool loads a fixed set of files by itself (T1–T8).
   - Anything else is read only if the model decides to read it, and in measured runs it often does not. A docs skill
     was "never invoked" in 56% of cases (E1). 58% of trials with a code-graph tool made zero calls to it (E2).
     *Quoted, reported.*
2. **Writing: the agents now write memory unasked, and no study has measured how good that memory is.**
   - Claude Code writes during the session, by its own judgement (T2, *verified*).
   - Codex generates memories in the background from idle past chats, once enabled. Its page does not say which model
     chooses what is stored (T6, *reported*; v1 correction L2).
   - Nobody has measured the quality of either — *not measured*.
   - The closest measurements are poor:
     - skills an agent wrote for itself scored below having no skills, in Claude Code, Codex and Gemini CLI (E3);
     - "add-all" memory made agents worse (E5);
     - rewriting collapsed a memory from 18,282 tokens to 122 (E6).

     *Reported.*
3. **What does get loaded is followed, and it costs.**
   - A tool named in the context file was used 1.6 times per instance, against under 0.01 when it was not named.
   - Repository overviews did not help, and cost rose over 20% (E4).
   - Performance "consistently degrades with increasing input length" (E7).

   *Quoted, reported.*
4. **The vendors do not leave the timing to the model.**
   - The memory tool adds "ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE" (T4, *verified*).
   - Claude Code says CLAUDE.md is "not a hard enforcement layer"; hooks are (T1, *verified*).
   - Codex says always-apply rules stay out of memories (T6, *reported*).
5. **The method today** (*my reading*):
   - It already names what each node must read and write in the brief and the state file (§4), which is the form the
     evidence favours.
   - It is silent on each engine's built-in memory.
   - It is silent on checking what an agent writes.
   - In this repo, folder rules reach non-Claude nodes only through a words-only pointer. Some rules exist only in
     Claude auto memory (M14, *verified*). No harm from this has been measured.

### Where the four experts stand (each *quoted* from §6)

| Expert (engine) | Q1: do agents use memory well on their own? | Q2: should the method change? | His one change |
|---|---|---|---|
| Linus (codex) | "partly". Reliability is "not established". | "Yes" | **O6**: a pointer to SoT, plus a memory contract in each node's fields |
| 范蠡 (Claude) | "partly" | "yes, one small change" | **O7**: a pointer, plus one sentence on delivery |
| 孫子 (dsh) | "**No** — not by the model's own judgement". The report's "partly" is "the harness working, not the agent knowing". | "**Partly**", and not by "adding details of how agents use memory" | **O8**: O7 plus a denial clause (what a node must **not** receive) |
| 老子 (opencode) | "**No** — not by its own judgement". "The timing is given from outside, and the keeping is unchecked from within." | "**Partly**", and "it is not details of how agents use memory" | **O9**: a pointer, plus delivery, plus "what a node writes is kept only when the run's end, or a later reader, names it". It conflicts with SoT W4.1 and K5.2. |

**Q1 is split two against two, and the report keeps both answers.** v0 to v3 said "partly"; 孫子 and 老子 say "No".
*My reading*: the evidence is the same. "Partly" answers *whether the reads happen*. "No" answers *who knows to make
them*.

**All four agree on three things** (*my reading* of §6, each point *quoted* there):
- Replace method §4's three-file paragraph (L494–510) with a pointer to `SOURCE_OF_TRUTH.md`. 范蠡's interim applies
  while SoT is not built (F1).
- The designer, not the model, controls delivery:
  - 范蠡, 孫子 and 老子 all say "never as a request to read it";
  - Linus has each node state its "delivery mechanism and timing".
- Nothing from O3–O5 now. They wait for evidence, a visible harm, or "one run watched".

**They differ on what goes with the pointer:**
- a per-node contract (Linus only);
- a denial clause (孫子; whether 老子 keeps it is not stated, §6.4);
- a keep-when-named clause on writes (老子 only).

None of these has been measured (§5).

**On EJ's premise** ("memory and information are the two most important factors"): no expert disputes that memory
matters, and none ranks it, because nobody has measured the ranking. All four reject "more memory" as the lever:
- Linus: "does not depend on that ranking";
- 范蠡: "regulating", not "filling";
- 孫子: "narrow, never widen";
- 老子: "subtraction".

## 1. What the agents do by themselves

The same split holds in every tool. Some reads are made by the **harness**, which loads the file whatever the model
decides. Others are made by the **model**, only if it decides to, or only when the user asks.

| id | Tool | Loaded automatically (harness) | Model decides | Only on request / off by default | Label, source |
|---|---|---|---|---|---|
| T1 | **Claude Code — CLAUDE.md** | Files above the working directory are loaded at launch. Files in subdirectories load "on demand" (L64). Project-root CLAUDE.md is re-read after `/compact` (L625). | Whether to follow it: "Claude treats them as context, not enforced configuration" (L24); "not a hard enforcement layer" (L326). A words-only pointer to `AGENTS.md`: "Claude sees `AGENTS.md` only if it decides to open the file" (L435). | Hooks "apply regardless of what Claude decides to do" (L589). | *verified*, S1 |
| T2 | **Claude Code — auto memory** | The first 200 lines or 25KB of `MEMORY.md` at every start (L546). | What to write: "It decides what's worth remembering based on whether the information would be useful in a future conversation" (L485). It "skips anything it can derive from the codebase" (L483). Topic files: "Claude reads them on demand … when it needs the information" (L552). | The harness reminds Claude to shorten `MEMORY.md` near the limit and returns an error when it is over (L548). On by default in local sessions. Not loaded into subagents (L554). | *verified*, S1 |
| T3 | **Claude Code — subagent memory** | The subagent gets the first 200 lines or 25KB of its own `MEMORY.md`, plus "instructions for reading and writing to the memory directory". | What to record. The docs still advise asking the agent to check memory before work and save after. | Only with the `memory` frontmatter field. | *reported*, S3 |
| T4 | **Claude API — memory tool** | When the tool is present, the API adds a system-prompt block: "IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE. … ASSUME INTERRUPTION …" | What to write and how to organise it. "If Claude still creates cluttered memory files, you can reinforce it in your prompt". | Expiry and caps are left to the developer: "Periodically delete memory files that haven't been accessed in a long time". | *verified*, S2 (full-text return; see note in `sources/`) |
| T5 | **Codex — AGENTS.md** | One file per directory from the root down, plus the global file, concatenated, with later files overriding earlier ones. Built once per run. Default cap 32 KiB (`project_doc_max_bytes`); guidance past the cap can be cut. | Whether to follow it. | — | *reported*, S9 |
| T6 | **Codex — memories** | When enabled, generated memories are used in later threads. | v0 said "Nothing during the task". **(v1, from Linus, checked L2:** the page describes background generation after a chat is "idle long enough". It "doesn't say" whether the working model chooses what is stored. So "Nothing during the task" was *my reading*.) | Off by default (`memories = true`). Required rules go in `AGENTS.md`; memories are "not the only source for rules that must always apply". | *reported*, S10 |
| T7 | **Gemini CLI** (replaced by Antigravity CLI on 2026-06-18) | Global and workspace `GEMINI.md`. When a tool touches a directory, more GEMINI.md files are found "JIT". All are concatenated "with every prompt". | Saving: "with `write_file` or `replace`", into one of three tiers. | — | *reported*, S11, S12 |
| T8 | **opencode** | `AGENTS.md` (project, then global), with `CLAUDE.md` as fallback. "The first matching file wins in each category." Also files listed in the `instructions` field. | Files referenced inside `AGENTS.md`: "opencode doesn't automatically parse file references". The docs suggest "use your Read tool to load it on a need-to-know basis". | No built-in memory is mentioned. | *reported*, S13 |
| T9 | **Antigravity / `agy`** | Third-party sources only: it reads `AGENTS.md` and `GEMINI.md`, and "Knowledge Items" are generated automatically. | — | — | *not measured* (no official doc read) |

**Across the tools** (*my reading*):
- The harness loads instruction files and memory indexes.
- Everything past the index is left to the model's judgement, mid-task.
- No tool lets the model decide *whether to read the index*.
- Codex memories are generated in the background.

The doc does not say whether the working model chooses what Codex stores. That stays *my reading* (v1, L2). The v0
summary listed separate `extract_model` and `consolidation_model` settings; they fit the reading but do not settle it.

The experts each restate this split in their own terms (their readings):
- 范蠡: "Heaven's time" against "human affairs".
- 孫子: "We know the loading side; we do not know the choosing side".
- 老子: "the timing is given from outside".

## 2. Evidence on how well they do it

Rows are second-hand unless marked *verified*. Our engines (Claude Code, Codex, Gemini CLI) appear in E3 and E4. (A v1
correction removed v0's non-existent "E21".)

| id | Claim | Label | Source (date) | Quoted |
|---|---|---|---|---|
| E1 | A Next.js docs skill was not invoked in 56% of eval cases. Without instructions it scored the same as no docs (53% vs 53%). An explicit instruction raised invocation to 95%+ and the pass rate to 79%. An 8KB docs index in `AGENTS.md` reached 100%. Models and eval count are not stated. | reported | S15, Vercel, 2026-01-27 | "In 56% of eval cases, the skill was never invoked." |
| E2 | With a code-graph tool available, 58% of trials made zero calls to it. Consistent use needed explicit prompting. | reported (repo row s3-F33, 2026-10-11 tags) | S23, CodeCompass arXiv 2602.20048, 2026-02-23 | "58% of trials with graph access made zero tool calls, and agents required explicit prompt engineering to adopt the tool consistently." |
| E3 | Skills that the model wrote for itself scored below the no-skills baseline in all three configurations: −8.1 pp Claude Code + Opus 4.7, −11.3 pp Codex + GPT-5.5, −11.5 pp Gemini CLI + Gemini 3.1 Pro. Curated skills scored +18.2 to +24.8 pp. The authors' audit blames packs "the solver never discovers", authoring that "displaces solver work", and "confidently wrong pack content". The deficit "mixes content quality with skill-discovery and creator/solver interference effects". | reported | S17, SkillsBench arXiv 2602.12670 v4, 2026-06-14 | "Self-generated Skills land below the no-Skills baseline on all three configurations" |
| E4 | Context files did not generally improve success, and raised cost by over 20%:<br>• LLM-generated files: −0.5% (SWE-bench) and −2%, not significant;<br>• developer-written files: +2.4% (p=21%);<br>• agents followed the files: `uv` was used 1.6 times per instance when named, against under 0.01 when not;<br>• the files did not shorten the time to the first relevant file.<br>Tested on Claude Code + Sonnet-4.5, Codex + GPT-5.2 and GPT-5.1 mini, and Qwen Code. | reported | S16, Gloaguen et al., arXiv 2602.11988 (v1 2026-02-12, v3 2026-09-29) | "providing context files does not generally improve task success rates"; "increasing inference cost by over 20% on average"; "repository overviews, although popular and recommended by model providers, are not helpful" |
| E5 | "Add-all" memory scored worse than a fixed memory on all four agents (GPT-4o-mini). For example, EHRAgent scored 13.05 with add-all against 16.75 with fixed memory. Strict evaluator-filtered addition scored +15.5 to +25.5 points over add-all. Deletion helped on 3 of 4 agents, and it depends on the evaluator. | reported | S18, Xiong et al., arXiv 2505.16067 v2, 2025-10-10 | "error propagation, where inaccuracies in past experiences compound and degrade future performance" |
| E6 | When an LLM fully rewrites its own context, details are lost. In one run the context fell from 18,282 tokens (accuracy 66.7) to 122 tokens (57.1), below the 63.7 no-adaptation baseline. There is also "brevity bias" toward "short, generic prompts". | reported | S19, ACE, arXiv 2510.04618 v3 (2026-03-29), ICLR 2026 | "context collapse, where iterative rewriting erodes details over time" |
| E7 | Across 18 LLMs, performance falls as input grows, even on simple tasks. One distractor already lowers it. | reported | S20, Chroma "Context Rot", 2025-07-14 | "Across all experiments, model performance consistently degrades with increasing input length." |
| E8 | Memory tool plus context editing: +39% on an internal agentic-search eval. Context editing alone: +29%. Tokens fell 84% in a 100-turn eval. No harness is published. | reported (the numbers are *unproven*) | S6, Claude blog, 2025-09-29 | "combining the memory tool with context editing improved performance by 39% over baseline" |
| E9 | Models differ widely in agentic retrieval. The best scored 74.0% (Sonnet 4.5) at launch; open-weight models scored about 55–57%. | reported | S21, Letta Context-Bench, 2025-10-30 | "Context engineering remains challenging" |
| E10 | Full memory systems mostly did not help on repository tasks: 11 of 12 pairings did not beat memory-off. Direct injection of verified experience raised resolution on 4 of 5 solvers by 1.1–4.5 pp, and lowered steps on all 5.<br>**(v1, from Linus, checked L1:** "Each target is retained only when injected history experience improves its executable outcome in a reference setting". So the injection gain is measured on tasks selected because injection helps, and does not show that it helps in general. The abstract says "setting", not Linus's "solver".) | reported | S22, VibeMemBench arXiv 2609.23570, 2026-09-20 | "eleven of twelve solver and system pairings fail to exceed the matched memory-off baseline" |
| E11 | Agents near saturation on LoCoMo do poorly in multi-session loops (MemoryArena). Hallucinations build up at extraction and update (HaluMem). | reported (repo rows s5-F6, s5-F5) | S24 | — (not re-read) |
| E12 | Anthropic says Opus 4 "becomes skilled at creating and maintaining 'memory files'". No measurement is given. | reported; the claim is *unproven* | S8, 2025-05-22 | "Claude Opus 4 also dramatically outperforms all previous models on memory capabilities." |

**Where the evidence is thin** (*my reading*, with the experts' agreement noted):
- Nothing measures the exact question: do Claude auto memory or Codex memories keep the right things and recall them
  when needed? *Not measured* (§7 Q1).
- E1 and E2 are about invoking *tools or skills*, not reading *files*. Linus agrees: E1 is "not every kind of memory".
- E1, E8 and E12 are vendor numbers with no published harness. Model generations also differ: E3 used Opus 4.7 and
  GPT-5.5, E4 used Sonnet 4.5 and GPT-5.2, E5 used GPT-4o-mini, and E1 names no models.
- E10's injection gain is conditional on task selection (v1, L1).
- E4 shows that loaded files are *followed*, not that following them *helps*: the +2.4% has p=21% (范蠡, 孫子).
- 孫子: the count "must come from the engines' own records and from our own runs".
- 老子 reads E3, E5 and E6 as "one disease under three names", meaning no limit on what is kept. His conclusion: "the
  'what to keep' half of Q1 is answered by *counting what leaves*, not by scoring the model". That is his reading;
  nothing in §2 measures what leaves.

## 3. Where they fail without instructions

User bug reports are evidence that a report was filed. The behaviour they describe stays *unproven* until reproduced.

| id | Failure | Evidence | Label |
|---|---|---|---|
| M1 | **Optional knowledge is not read.** | E1, E2, E3 ("the solver never discovers"). S1 L435: a words-only pointer is read "only if it decides to open the file". | reported (E1–E3); verified (S1) |
| M2 | **A "read X at start" instruction is skipped.** #34763 (Opus 4.6; closed as stale, no maintainer reply): "especially for simple prompts". #40272 (Sonnet 4.6): a skipped memory read led to a stale API key. The reporter's root cause is that the injected `MEMORY.md` was treated as sufficient. | S25 (2026-03-15, 2026-03-28) | reported (the issues exist); behaviour and root cause *unproven* |
| M3 | **The agent answers before it reads.** A stored command was ignored "50+ times" (#43098, Opus 4.6). | S25 (2026-04-03) | reported; *unproven* |
| M4 | **It writes everything, and memory degrades.** | E5 | reported |
| M5 | **Rewriting erodes memory.** | E6. S2: "If Claude still creates cluttered memory files…" | reported (E6); verified (S2) |
| M6 | **Self-authored procedures are wrong or unused.** | E3 | reported |
| M7 | **Across sessions, work is left undocumented or declared done early.** Agents "tried to do too much at once", left "a feature half-implemented and undocumented", and would "mark a feature as complete without proper testing". The fix was an initializer, a progress file, a JSON feature list and fixed start-of-session reads. | S5, 2025-11-26 (qualitative) | reported |
| M8 | **Subagents duplicate work when briefs are vague.** "Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information." | S7, 2025-06-13 | reported |
| M9 | **Context grows until quality drops,** and loaded files add cost. | E7, E4 | reported |
| M10 | **Instructions are lost after compaction** if they were given only in conversation or in a nested file not yet reloaded. | S1 L627 | verified |
| M11 | **Conflicting instructions are resolved arbitrarily:** "Claude may pick one arbitrarily." | S1 L90 | verified |
| M12 | **Silent truncation:** `AGENTS.md` past 32 KiB (Codex); `MEMORY.md` past 200 lines or 25KB is "dropped on the next load". | S9; S1 L548 | reported (S9); verified (S1) |
| M13 | (v1, Linus) **Stored notes leak a worker's reasoning to its verifier** when memory selection ignores the information boundaries. O8's denial clause is built on this. | §6.1. The boundary is in method §4 L484–485 and SKILL.md L82 (*verified*). | *my reading* (Linus's); *not measured* |
| M14 | (v2, 范蠡) **In this repo, folder rules reach non-Claude nodes only if the model reads them, and some never reach them.**<br>• `AGENTS.md` is a words-only pointer: "The instructions for this folder are in `CLAUDE.md` … Read it first". Codex loads `AGENTS.md` (T5) with no fallback set (S32). opencode uses only `AGENTS.md` when both files exist (T8).<br>• "Stay in own scope" exists only in Claude auto memory, which App. B says "Only Claude Code reads". | F2–F6, S30–S32 | verified (facts); *my reading* (delivery); *not measured* (harm) |
| M15 | (v4, 老子) **Nothing ever leaves the store, and nobody counts it.** If no step names what to keep, everything written stays: "if nothing ever leaves the store, the store is already in the illness". "Today that count does not exist, so a run that promotes zero is invisible." | §6.4. SoT K5.2 (the writer chooses) and K4.2 ("Age alone never expires an entry"), both *verified*. | *my reading* (老子's); *not measured* |

## 4. What the method says today

Read directly (*verified*) in `docs/WORKFLOW_DESIGN_METHOD.md` and the skill:

- **§4 L482–485.** The state lives in one file (`docs/workflow-templates/state.md`), with one writer at a time. It holds
  progress and results, never reasoning. A worker's notes go in its own file, "so a verifier can be kept blind to
  them".
- **§4 L487–492.** Files in the repo are "the one every tool and every agent can read". Each agent gets a brief with
  only what its piece needs. The main agent keeps conclusions. Stored knowledge is dated and rechecked. Knowledge is
  kept apart from state.
- **§4 L494–510.** Project memory is three append-only files in `docs/blueprint/`: `decisions.md`, `changelog.md` and
  `lessons.md`.
  - Each entry is about 5 lines.
  - Each file has a named writer and a time to write. For `lessons.md`, "any node proposes, the COO appends" (L503).
  - Agents read only the entries their task touches, found by `grep`.
  - Stale lessons are marked.
- **§4 L512–514.** No store without a listed query. "Not verified: Codex's memory and subagent features beyond
  `AGENTS.md`."
- **App. B L541–553.** The kinds of memory, each with its limit:
  - context window;
  - `CLAUDE.md`/`AGENTS.md`;
  - auto memory, "Only Claude Code reads it";
  - files in the repo;
  - skills;
  - run records, which "Nobody reads … unless asked";
  - a subagent's final report.
- **SKILL.md.**
  - L82, Context: "exactly what it is given, and what is withheld (a verifier never sees the worker's reasoning)".
  - L85, State: "what it reads from the state file before starting and what it writes back".
  - L91: the state template is `assets/templates/state.md`.

**Not in the method** (*my reading*):
- the agents' own built-in memory: when it writes, what it may hold, and whether it is on;
- Codex memories, the memory tool, agy and opencode, in App. B;
- any check on what an agent writes;
- any rule on when kept memory stops being kept. 老子 notes that the same is missing from SoT (§6.4).

**A disagreement between two repo documents.** It is not resolved here; it is EJ's call.
- Method §4 L494–503 says `docs/blueprint/{decisions,changelog,lessons}.md`, as shared append-only files.
- `docs/memory-system/SOURCE_OF_TRUTH.md` (accepted 2026-10-12) says `project-memory/entries/`, one file per entry:
  "agents never append to one shared file" (L107).

All four experts resolve it to SoT, each for his own reason:

| Expert | His reason for SoT |
|---|---|
| Linus | its status: `question.md` L10 and SoT L3 both call it "accepted" (L3, *verified*) |
| 范蠡 | the timing: the conflict exists now, and S1 L90 says such conflicts are resolved "arbitrarily" |
| 孫子 | "one whole copy" |
| 老子 | 「功成而弗居」, the work done and not dwelt in. "Keeping both is the hoarding" (his reading) |

Neither document says SoT *replaces* §4.

**SoT is accepted but not built** (v2, F1). A Glob of `project-memory/**` finds no files (*verified*). Without a shell I
could not tell an empty directory from a missing one. Until it is built, a pointer leads to rules with no store.

## 5. Implications for the method

These are options, not a verdict. Each is *my reading* of §1–§3, plus the experts' proposals. None is measured.

| id | Option | What it would say | Rests on | Cost |
|---|---|---|---|---|
| O0 | **No change** | The brief, the state file and repo files already make each must-read and must-write explicit. | M1 and M2 hit optional reads, and required inputs are not optional. | Nothing now. Built-in memory (T2, T3, T6) keeps running beside the design, unplanned. |
| O1 | **Load, don't ask** | A node's must-read files reach it through its brief, an import or a hook, never through a request to read them. | E1 (an instruction raised invocation to 95%, not 100%), M1, M2, T1 L435, T4. SoT Rd2.1 already says this for project memory. | One sentence. A start hook per engine where a brief cannot carry the file. |
| O2 | **Writes are part of the return contract** | What a node must record is a field of its return, and is checked. | M7, M4, T6. | Half there already (SKILL.md L85). Adds a check per node. |
| O3 | **Agent-written memory is a claim** | An evaluator gate on what is kept, and a recheck before use. | E5 (+15–25 pts, but evaluator-dependent), E6, E3, M3. SoT Rd5.1 covers checking before use. | Verifier time per write. A weak evaluator makes deletion worse (E5). |
| O4 | **Set built-in memory per engine** | One row per engine in `docs/EXECUTOR_KINDS.md`: on or off for workflow nodes. | T2, T3, T6. #40272 (*unproven*). M14 (*verified*, no harm measured). | One row per engine, plus EJ's decision. Turning it off loses what it would have kept. |
| O5 | **Refresh App. B** | Add Codex memories, the memory tool, agy and opencode. | §1 | Upkeep: these features changed within the last year. |
| O6 | **Linus.** A pointer plus a per-node memory contract. | "For task and project memory, the workflow designer **SHOULD** specify each node's memory inputs, delivery mechanism and timing, required outputs and write timing, and checks in its existing Context, Contract and State fields, following the accepted Write, Keep and Read policy." It replaces §4 L494–510 with a pointer to SoT. | O1 and O2's evidence. The fields exist (SKILL.md L81–85). SoT already has the checks (Rd5.1, K4, Rd5.3). All *verified*. | "more brief preparation, input tokens and checking time … **not measured**". "delivering memory does not establish that the agent understood or followed it". |
| O7 | **范蠡.** A pointer plus O1's one sentence, and no contract. | "a node's must-read memory reaches it through its brief, an import or a start hook, never as a request to read it." **Interim:** while SoT is unbuilt, "keep §4's three files, marked 'until SoT is built', and change only the one sentence". | O1's evidence. Timing and checks are already in SoT (Rd2.1 L344, Rd5.1 L383). Inputs and writes are already in SKILL.md L82–85. All *verified*. "narrow … never widen". | "the pointer depends on a design that has not been built". "the sentence may cost brief tokens and buy nothing". "some nodes' memory needs go unstated … the method will not prompt for it". |
| O8 | **孫子.** O7 plus a denial clause. | "a node's memory arrives by brief, import or hook and never as a request to read it; the brief names what the node must not receive, and no verifier gets a worker's reasoning or an entry that carries it." Same interim as O7.<br>**(v3, checked Z5:** the denial principle already exists in SKILL.md L82 and method L484–485 and §5 L522. What O8 adds is naming *memory entries*. SoT Rd2.3 bars "another agent's transcripts", but has no rule per verifier.) | M13. "a sentence about loading without the denial clause is half an order." | "carried by the designer, not enforced by the method … unless it becomes a line in the node's fields". "Narrowing can omit a needed entry". |
| O9 | **老子.** A pointer, plus delivery, plus keep-when-named. | One sentence, two halves. The first is "a node's memory arrives by brief, import or start hook, never as a request to read it". The second: "**what a node writes is kept only when the run's end, or a later reader, names it; until then it stays in that task's journal.**" It uses the pattern of §4's `lessons.md` ("any node proposes, the COO appends", L503).<br>**Whether O9 keeps O8's denial clause is not stated.** His sentence quotes only the delivery half. His fallback is "孫子's O8 plus the pointer". He says his write half is "sized by what the node needs, not by what is dangerous". | M15, E3, E5, E6 as "one disease". SoT has no rule on when keeping stops: K5.2 "the writer chooses", K4.2 "Age alone never expires" (*verified*). | **Conflicts with SoT W4.1 and K5.2** (below). "A promotion step sits after the last check passed. If nobody is at the end to name anything, the store keeps growing silently". "If the first three workflows promote zero entries and nothing was ever wrong … the sentence … should be deleted." |

**O6–O9 compared.** Each claim in this table is *quoted* in §6; the costs come from the experts and none is measured.

| | O6 | O7 | O8 | O9 |
|---|---|---|---|---|
| Backed by | Linus | 范蠡 | 孫子 | 老子 |
| Pointer to SoT | yes | yes | yes | yes |
| Delivery rule | inside each node's contract | one sentence | first half of the sentence | first half of the sentence |
| Per-node memory contract | **yes** | no ("a second copy") | no ("a second, broken copy") | no ("one sentence and not a section") |
| Denial: what a node must not get | no | no (he lists it as a cost) | **yes** | not stated; his fallback is O8 |
| What a node's writes keep | via each node's "write timing" | SoT as is | SoT as is | **kept only when named**; until then in the task journal |
| Conflicts with accepted SoT | none found | none found | none found | **yes: W4.1, K5.2** |
| Main cost | brief preparation and tokens on every node | omissions nobody is prompted to catch | the designer must carry the denial | a promotion step at the end, which may never happen; a change to SoT |
| Reversible | a §4 paragraph | one sentence | one sentence | one sentence, plus a change to SoT that EJ must make |

**O9's conflict with the accepted design. It is kept explicit and not resolved here.**
- SoT W4.1 (L253–255): "Anyone, agent or person, may create or change any entry … There is no owner and no approval."
- SoT K5.2 (L315–316): the agent "writes what is worth keeping as entries".
- O9 makes keeping depend on someone other than the writer naming the entry.
- 老子: his clause "narrows who *promotes*, not who may write — that distinction is my reading, and a reviewer may well
  reject it as approval in disguise. If it is rejected, drop the second half; do not rewrite it into something larger."
  His Q1 asks EJ to decide: "This is EJ's call on an accepted requirement, not mine."
- *My reading*: per `CLAUDE.md`, "Only EJ changes" SPEC and DECISIONS. SoT was accepted by EJ, so the same applies to
  W4.1 and K5.2. O9 cannot be adopted by the method alone.

**The crux of O6 against O7, O8 and O9** (*my reading*): SoT Rd2.1 fixes the reads of *project* memory at *session
start*. It does not say which entries a given node's brief carries, or which ones a verifier must not get. Each option
fills that gap differently:
- O6 prompts the designer at every node.
- O7 relies on the existing fields.
- O8 adds the denial.
- O9 adds a gate on what is kept.

None has been measured. Linus's matched-task test (§6.1) would compare them. 范蠡 narrows it to the delivery method;
孫子 adds a denial check; 老子 adds a count of what is promoted.

**The experts on O3–O5** (*quoted*):

| Expert | Position |
|---|---|
| Linus | "an additional evaluator, automatic expiry or per-engine memory controls would each need evidence of a problem they solve" |
| 范蠡 | wait "until EJ's own runs show the harm they would fix". #40272 is "a sprout, not a visible form". Waiting has a price: "every run until it is noticed pays for it" |
| 孫子 | his change "does not touch" built-in memory. "an unknown left on the board, not a settled front" |
| 老子 | "a named unknown needs no new sentence; it needs one run watched". Method L514 already names it |

*My reading*: SoT "covers task and project memory" (L70, *verified*). It does not cover an engine's built-in memory
(T2, T3, T6), and neither does any of O6–O9. So O4's gap remains: M14 shows it exists here, but no harm has been
measured.

**范蠡's trigger for O4**: "Has a Codex, agy or opencode node ever broken a rule that existed only in Claude auto
memory or only in `CLAUDE.md`? If yes, the time has come for O4". 孫子 and 老子 accept watching for it. M14 gives the
concrete cases to look for. That check has not been run (§7 Q11).

**On EJ's premise**: see the Short answer. The detail is in the expert subsections.
- E10 supports "deliberate delivery" less than v0 implied (v1, L1).
- 老子 adds "subtraction … which is also EJ's own standing rule that a mechanism which is not needed is removed". That
  rule is in `question.md` L11 (*verified*: "a mechanism that is not needed is removed").

## 6. Experts' views

*One subsection per expert, in order. Each subsection keeps the expert's own words and labels, names the report section
it answers, and keeps disagreements beside the report rather than merged into it. The classical Chinese quotes come
from each expert's own rules list. The researcher did not check them against classical texts.*

The COO ran `four_experts.py check` against the experts' rules lists (state.md, 14:56:37Z). It failed 6 items, all in
老子's file:
- 5 are script variants (為/爲, 敗/败);
- 1 normalises a bracketed transcription (list L80).

The COO notes "None invented". That check was written by Claude, and it "does not establish rules were applied
correctly".

### 6.1 Linus (codex)

Source: S27. His labels are "my reading" and "not measured", plus "my #N" for his rules.

**Answer:** "**My reading: partly**—agents have memory mechanisms, but reliable decisions about reading, writing and
keeping memory across these engines are not established. **Yes**—make one change to §4: replace its project-memory
prescription with a reference to EJ's accepted design and an explicit memory contract in each node's existing
fields."

| Report section | His point | Against the report |
|---|---|---|
| §1, §2, §7 | "separate capability from demonstrated reliability". Codex memories are background-generated, "so this is not simply the working model independently deciding". | Agrees. Sharpens T6 (L2). |
| E1, E10 → O1 | E1 "concerns discovery of a documentation skill and index, not every kind of memory". VibeMemBench "selected tasks where injected experience had already helped". "these results justify testing deliberate delivery; they do not establish that loading more memory universally improves work." | Corrects how E10 was used (L1). |
| §4 | Context, Contract, Evidence and State "already describe inputs, outputs and checks. Memory can use those fields." | Resolves toward SoT. |
| O3–O5 | They "would each need evidence of a problem they solve." | Disagrees with adopting them now. |
| Premise | "this recommendation does not depend on that ranking." | Agrees it is untested. |

He self-checked his proposal against all eight `requirement-check` items, with "basis (a proposal, n=0 …)". He wrote
that check himself, so it is not independent evidence.

**His question:** "What additional token cost or elapsed time would EJ accept for fewer missed decisions and better
handoffs?" (Q8)

**His test:** compare the current method with O6 "on matched repository tasks, keeping the engine, model and memory
settings fixed". The tasks include a fresh-session handoff, a relevant prior decision, and "an entry contradicted by
current code". Measure outcomes, memory mistakes, tokens and time. "Contract completeness alone would not establish
that."

**His costs:** brief preparation, tokens and checking time, *not measured*. Delivery does not mean the agent followed
it. The verifier boundary (M13). Time spent on unneeded contracts is not recovered.

| id | Claim | Check | Label |
|---|---|---|---|
| L1 | VibeMemBench selected tasks "where injected experience had already helped a reference solver". | Abstract: "retained only when injected history experience improves its executable outcome in a reference setting". It says "setting", not "solver". **Corrects E10.** | reported (S22, re-fetched) |
| L2 | Codex memories are generated in the background, not by the working model deciding. | The page confirms background generation. It "doesn't say" which model chooses. **Corrects T6's wording.** | reported (S10, re-fetched) |
| L3 | SoT is accepted. | `question.md` L10; SoT L3. | verified (S28, S26) |
| L4 | SoT already checks before use, keeps superseded claims and reports contradictions. | Rd5.1 L383; K4.1/K4.3 L301–307; Rd5.3 L386. Scope: task and project only (L70). | verified (S26) |
| L5 | The node fields already describe inputs, outputs and checks. | SKILL.md L82–85. | verified (S26) |
| L6 | E1 is about skill discovery, not all memory. | Matches E1. | reported (S15) |

### 6.2 范蠡 (Claude)

Source: S29. His labels are *quoted*, *reported*, *verified*, *my reading* and *not measured*, plus "my #N".

**Answer:**
- "**Question 1: partly.** The harness forces some reads, and those happen. Everything the model decides for itself …
  is unreliable or *not measured*."
- "**Question 2: yes, one small change.** It is smaller than Linus's O6 … a pointer to
  `docs/memory-system/SOURCE_OF_TRUTH.md`, plus O1's one sentence … Wait on O3–O5 until EJ's own runs show the harm
  they would fix."

| Report section | His point | Against the report |
|---|---|---|
| §1 | Harness reads are "Heaven's time"; designed delivery is "human affairs". "That is the vendors themselves not trusting the model's timing." | Agrees. |
| E1, T6 → O1 | "give timing to the harness and the brief, and leave content judgement to the model." | Agrees with O1. |
| Premise; E4–E7 | "anything the method adds about memory should **narrow** what a node gets, never widen it." | Agrees, and adds this consequence. |
| §4 | "The contradiction is already here … My reason is the timing, not the documents' status." | Resolves toward SoT, for a different reason than Linus. |
| O6 | "Repeating SoT's rules in every node is a second copy." | **Disagrees with Linus.** |
| SoT status | "accepted but not built … A pointer keeps one copy." | Adds F1. |
| O3–O5 | #40272 is "a sprout, not a visible form". | Agrees with Linus that they should wait, by a different rule. |
| O4 | `AGENTS.md` is a words-only pointer, and some rules are only in auto memory. "What it does not establish: that any node has failed because of it." | Adds M14. |

**His questions:** a rule broken only through Claude auto memory (Q11); whether `AGENTS.md` should import `CLAUDE.md`
(Q12); whether SoT will be built before the next workflow (Q13).

**His costs:** the pointer leads to an unbuilt design. The sentence "may cost brief tokens and buy nothing". A hook per
engine. Waiting on O4 "has a price too". Being smaller than O6 means "some nodes' memory needs go unstated".

**His tests:**
1. Grep the next three design files for §4's three files.
2. Compare delivered reads against ask-only reads on the next non-Claude design. This is "Linus's matched-task test …
   narrowed to one variable: delivery method".
3. He is wrong if a run shows a node acting on memory that a Claude-only or words-only channel failed to deliver.

| id | Claim | Check | Label |
|---|---|---|---|
| F1 | `project-memory/` does not exist, so SoT is not built. | Glob `project-memory/**` finds no files. With no shell, an empty directory and a missing one look the same. | verified (no files), qualified |
| F2 | `AGENTS.md` is a words-only pointer. | L3: "The instructions for this folder are in `CLAUDE.md`, next to this file. Read it first; it applies to every agent and tool, not only Claude Code." | verified (S30) |
| F3 | Codex and opencode get the folder rules only if the model opens `CLAUDE.md`. | Premises: F2; T5, T8 (*reported*); no fallback setting in `~/.codex/config.toml` (S32). | *my reading* on verified and reported premises |
| F4 | Auto memory has 36 index lines. | `MEMORY.md` has 36 lines. | verified (S31) |
| F5 | "Stay in own scope" is not in `AGENTS.md`, `CLAUDE.md` or `docs/`. | A repo-wide grep finds it only in `fan-li.md`; "own scope" is also absent. The rule lives in `memory/stay-in-own-scope.md`. *My note:* a broader rule, "Touch only what you must", is in user-level `/home/smoke01/CLAUDE.md`, which is loaded by Claude Code and not by Codex. | verified (S31, S26) |
| F6 | App. B: auto memory, "Only Claude Code reads it". | Method L549. | verified (S26) |
| F7 | SoT L344 is Rd2.1 and L383 is Rd5.1. | Both match. | verified (S26) |
| F8 | SKILL.md L82–85 holds the node fields. | L85, exact wording. | verified (S26) |
| F9 | S1 L90: "Claude may pick one arbitrarily". | Matches. | verified (S1) |

### 6.3 孫子 (dsh)

Source: S33. His labels are `quoted` for his rules list, *not measured* and *unproven*, plus "my #N".

**Answer:**
- "**Q1: No — not by the model's own judgement.** … The report's 'partly' is the harness working, not the agent
  knowing."
- "**Q2: Partly — yes, one change to §4, but not by adding details of how agents use memory.** … the node's brief
  names what it must **not** receive; no verifier gets a worker's reasoning or an entry that carries it." He uses
  范蠡's interim while SoT is unbuilt.

| Report section | His point | Against the report |
|---|---|---|
| Short answer 1, §1, §2 | "We know the loading side; we do not know the choosing side … it is not the model that is doing the knowing." | **Disagrees with "partly".** |
| Q2 framing | "'How agents use memory' is 責於人 … The method's lever is 勢 … §4 should set the position, not describe the agent's mind." | Disagrees with EJ's framing. |
| O6, O7; M13 | "Neither says what it **must not be given** … it is what I add." | Adds O8 (Z5 qualifies it). |
| O6 vs O7 | "A per-node copy of SoT's rules is a second, broken copy … one whole copy, not his 'timing'." | **Disagrees with Linus.** Partly corrects O7: loading without denial "is half an order". |
| E4, E10, Q1; thin evidence | The count "must come from the engines' own records and from our own runs". | Agrees. |
| O4 | "an unknown left on the board". | Leaves it open. |

**His questions:** whether SoT will be built (→ Q13); whether workflows use non-Claude nodes (→ Q12); whether the
matched test may run before the change is written (→ Q9); whose memory each node needs (→ Q14, new in v3).

**His costs:** brief preparation. The denial clause is "carried by the designer". The pointer leads nowhere until SoT
is built. Removing §4 "may strip the only concrete instruction an existing run uses". Narrowing may omit an entry.
Built-in memory keeps running.

**His tests:**
1. In the next design, delivery is by brief, import or hook, and "no verifier brief names a worker's reasoning file
   or a reasoning-bearing entry".
2. The matched test.
3. A fresh-session handoff (SoT Rd6.1).
4. He is wrong if designs still cite §4's three files, if a verifier receives reasoning, or if a needed entry is
   missed while the brief said nothing.

| id | Claim | Check | Label |
|---|---|---|---|
| Z1 | §4 L484–485 applies the blind verifier to a worker's notes. | Exact. | verified (S26) |
| Z2 | The §4 project-memory paragraph is L494–510. | Exact. | verified (S26) |
| Z3 | E4's developer-file gain has p=21%. | Matches E4. | reported (S16) |
| Z4 | SoT Rd6.1 is a fresh-session test. | L400–404. | verified (S26) |
| Z5 | Neither O6 nor O7 says what a node must not get. | True of O6 and O7. **(v3, checked:** SKILL.md L82 already has "what is withheld (a verifier never sees the worker's reasoning)", and method §5 L522 names "a blind verifier". O8 adds the naming of memory entries.) | verified, with correction |
| Z6 | T9 and Codex memories are *not measured*. | T9 is not measured. Codex memory *quality* is not measured; its mechanism is *reported* (T6). | matches, with nuance |
| Z7 | E8 and E12 are *unproven*; E5 used GPT-4o-mini. | Matches. | reported (rows) |

### 6.4 老子 (opencode)

Source: `experts/answers/lao-tzu.md` (S34, read directly). His labels are `quoted` (his list's words), `attributed`
(words reported of Laozi by a later author: 史記 for #18, 莊子·天下 for #19), *not measured*, and "my #N". The answer
ends with an operational note after the `---`, about a stray line in his file. It is not about the question. The COO's
log records that the stray line was removed.

**Answer:**
- "**Q1: No — not by its own judgement, and with one qualification that decides the whole thing.** … for 'what to keep,
  what to leave out' the answer needs no measurement of the model at all, because the failure has a name you can check
  without asking the agent … So: the timing is given from outside, and the keeping is unchecked from within."
- "**Q2: Partly — one change to §4, and it is not details of how agents use memory.** … The first half is not mine and
  I do not improve it: *a node's memory arrives by brief, import or start hook, never as a request to read it* … The
  second half is mine … **what a node writes is kept only when the run's end, or a later reader, names it; until then
  it stays in that task's journal.** All three proposals add what *reaches* a node. None says what *leaves*."
- Conditional: "if EJ will not touch SoT's W4.1 … my change reduces to the pointer plus the first half".

**What he responds to:**

| Report section | His point | Against the report / the others |
|---|---|---|
| Short answer 1; §1 | "The words do not say the timing is the agent's own. That the harness sets it is my reading of §1's own sentence." | **Disagrees with "partly"** (with 孫子). |
| §2 E3, E5, E6 | They are "one disease under three names". 「禍莫大於不知足」. "the 'what to keep' half of Q1 is answered by *counting what leaves*, not by scoring the model." | A new reading of §2 (M15). |
| Premise; E4, E7, E10 | 「為道日損」. "the store's job is to get *smaller* until what is left still does the work … also EJ's own standing rule that a mechanism which is not needed is removed." | Agrees with the direction, and states it as subtraction. |
| O6, O7, O8 | "each adds what reaches a node; O8 adds what a node must not receive". 「無之以為用」, read by him as: "the empty half must be sized by what the node needs, not by what is dangerous — which is why my sentence says a *named* write, not a *refused* one." | Adds O9. **Differs from 孫子** on how the "empty half" is framed. Whether O9 also keeps O8's denial clause is not stated (§5). |
| §4 layout | 「功成而弗居」 … 「多藏必厚亡」. "That the *copies* are the problem is my reading." | Resolves toward SoT (all four agree). |
| SoT (§4, §5) | "nothing in SoT says when the *keeping* stops, and the choice sits with whoever wants to keep it". This rests on When to write (L113–119), K5.2, K4.1–K4.2 and W4.1. | A new gap in SoT (his reading; LZ1–LZ4). |
| O3–O5, O6 | "What I do **not** touch … a named unknown needs no new sentence; it needs one run watched." | Agrees: nothing now. |
| Premise | "I do not dispute that memory matters, and I do not rank it … What I will not do is treat the ranking as a reason to add." | Agrees it is untested. |
| The method's own files | §4 L482 and SKILL.md L91–93 "both point at one file". "the skill's own copy under `assets/templates/` is byte-identical today (same md5) and nothing checks it." He proposes no check. | Partly contradicted by CLAUDE.md L45 (LZ7). |

**His questions:**
1. "Will EJ change SoT's W4.1 and K5.2?" → Q15, new.
2. "Which point is 'the run's end'?" SoT has three write times: W5.1, W5.3 and W5.2. "I was not told which one names
   memory, and I will not fill it." → Q16, new.
3. "Has anything ever been removed from EJ's own memory — an entry retired, a store pruned?" → Q17, new.
4. Whether SoT will be built → merged into Q13.
5. Whether non-Claude nodes are used → merged into Q12.

**His costs** (*quoted* in substance):
- narrowing may omit a needed entry;
- the promotion step "sits after the last check passed. If nobody is at the end to name anything, the store keeps
  growing silently and the rule looks satisfied";
- "It collides with an accepted requirement … If it is rejected, drop the second half; do not rewrite it into
  something larger";
- "A rule that names nothing is hoarding in a new form";
- removing §4 costs what was already spent learning it;
- "The paragraph must stop growing";
- the template note (LZ7).

**His tests:**
1. In the next workflow, every entry kept was named by someone other than its writer, or the design names the point
   where that happens. The run records how many entries were promoted and how many were left. "Today that count does
   not exist, so a run that promotes zero is invisible."
2. Grep the next three designs, as 范蠡 proposed.
3. "no new sentence about memory in §4 or App. B without an id in the report or a run showing the harm it fixes".
   Countable in git.
4. He is wrong if:
   - a promoted entry "had to be argued for";
   - a needed entry was never promoted and is missing from the journal;
   - nothing was ever promoted and nothing was ever wrong.

**His factual claims, checked by the researcher (v4):**

| id | 老子's claim | Check | Label |
|---|---|---|---|
| LZ1 | SoT's "When to write" (L113–119; W5.1–W5.3) says *when* to write. | L113 "**When to write.**", with the table at L115–119. W5.1–W5.3 are at L261–270. | verified (S26) |
| LZ2 | K5.2: the agent "writes what is worth keeping as entries", so the writer chooses. | L315–316: "an agent reads its task's journal … writes what is worth keeping as entries". "The writer chooses" is his reading of that wording. | verified (wording); his reading (inference) |
| LZ3 | K4.1–K4.2 retire an entry only when a reader finds a mismatch (Rd5). | K4.1 L301–302: an entry is never deleted; it is marked `superseded` or `retired`. K4.2 L303–304: "Age alone never expires an entry. An entry is found out of date only when someone reads it and checks it against the code (Rd5)." K4.1 does not limit when an entry may be retired. "Only when" goes beyond K4.1's wording; it is his reading. | verified (wording); his reading (inference) |
| LZ4 | W4.1 says "no owners and no approval gate", and he quotes "no owners and no human approval gate". | **(v4, from 老子, checked:** W4.1 L253–254 reads "There is no owner and no approval". The exact phrase "no owners and no human approval gate" is in SoT's status header, L44 ("Where this differs … no owners and no human approval gate"), not in W4.1. The substance is the same; the quoted words are L44's.) | verified, with correction |
| LZ5 | Rd2.1 governs session-start loads, and Rd4.1 the reads before an edit. | L344; L371 ("Before editing a file, an agent reads the entries whose `covers` include it"). | verified (S26) |
| LZ6 | Method §4 L482 names the state template. L503: `lessons.md` is "any node proposes, the COO appends". L514: "Not verified: Codex's memory and subagent features beyond `AGENTS.md`". | All three match. | verified (S26) |
| LZ7 | SKILL.md L91–93 and §4 L482 point at one file. The skill's "copy" under `assets/templates/` is "byte-identical today (same md5) and nothing checks it". Two copies, no check. | SKILL.md L91 names `assets/templates/state.md` (*verified*). I could not check the md5: no shell. **(v4, from 老子, checked:** `CLAUDE.md` L45 says the skill's "method and templates are links into `docs/`, so there is one copy of each" (*verified*). A Glob of the skill folder did not list `assets/`, but `assets/templates/state.md` reads as the state template. That pattern is consistent with a symlink (*my reading*). So "two copies" is contradicted by the repo's own statement, though not checked on the filesystem. If it is a link, identical md5 is expected and there is nothing to keep in step.) | *unknown*: md5 not checked; "two copies" contradicted by CLAUDE.md L45 |
| LZ8 | E3, E5, E6: self-authored skills below baseline; add-all worse; 18,282 → 122 tokens. | Matches those rows. | reported (rows) |
| LZ9 | §1: "no tool lets the model choose *whether to read the index*". | Matches §1's "Across the tools", which is *my reading*. | matches (*my reading*) |

## 7. Open questions

Merges in v4 are noted. Ids are stable from v0.

1. **How good is Claude Code's auto memory, or Codex memories?** That means recall, precision and staleness. *Not
   measured.*
2. **Does "read X first" in a brief work as well as loading X?** E1 measured one skill (95%). It was not measured for
   files or for this repo's engines. 范蠡's narrowed test would measure it.
3. **Do newer models skip fewer reads?** No source compares model generations.
4. **Does built-in memory interfere with designed memory?** Only #40272 says so, and it is *unproven*.
5. **What does agy load and write?** No official doc was read.
6. **Which project-memory layout?** All four experts say SoT, with the interim while it is unbuilt. The decision is
   EJ's.
7. **Do whales need per-agent memory at all?** *Not measured.*
8. (Linus) **What extra tokens or time would EJ accept** for fewer missed decisions? This decides whether any of O6–O9
   earns its cost.
9. (Linus; 孫子's Q3 merged) **Does the change beat the current method on matched tasks?** Not run. The test would
   compare O6 to O9, with 范蠡's narrowing, 孫子's denial check and 老子's promotion count. 孫子 also asks whether it may
   run before the change is written.
10. (*my reading*) **Is built-in engine memory out of scope on purpose?** O6–O9 and SoT cover task and project memory
    only (O4).
11. (范蠡) **Has a Codex, agy or opencode node ever broken a rule held only in Claude auto memory or `CLAUDE.md`?** This
    is the O4 trigger, and it is checkable against past runs (M14). Not checked.
12. (范蠡; 孫子's Q2 and 老子's Q5 merged) **Do EJ's workflows use non-Claude nodes, and should `AGENTS.md` carry or
    import `CLAUDE.md`'s content?** Today `AGENTS.md` asks in words (F2). Neither Codex nor opencode parses an `@`
    import in `AGENTS.md` (T5, T8, *reported*). Codex `project_doc_fallback_filenames` is not set (S32). opencode has
    `instructions`. 老子: if only Claude nodes are used, "the first half is nearly free".
13. (范蠡; 孫子's Q1 and 老子's Q4 merged) **Will SoT be built before the next workflow that needs project memory?** If
    not, the interim applies (F1).
14. (孫子) **Whose memory does each node need: task, project, agent or user?** SoT covers task and project; agent and
    user memory sit in the home folder (SoT L64–72).
15. (老子, new) **Will EJ change SoT W4.1 and K5.2** to allow keep-when-named? If not, O9's second half is dropped, and
    by 老子's own fallback his change becomes O8 plus the pointer.
16. (老子, new) **Which write time is "the run's end" that names what is kept?** It could be W5.1 (immediately), W5.3
    (when the work is complete) or W5.2 (end of task). It is not given, and 老子 will not fill it.
17. (老子, new) **Has anything ever been removed from EJ's memory, such as an entry retired or a store pruned?** Not
    checked. If nothing has been, O9 addresses "a disease no run has met".

### Gaps

- **Not read:**
  - the official Antigravity docs;
  - Mem-α (2509.25911, search only);
  - Harness Engineering (2609.00006): its abstract had no memory content;
  - Bad Memory (2607.14611) and Memory as Infrastructure (2609.05510);
  - VibeMemBench in full, so whether its "reference setting" is a single solver is not known.
- **Partly read (WebFetch summaries):** the tails of 2505.16067v2 (2,435 characters), 2602.12670v4 (75,714),
  2602.11988v3 (3,165) and 2510.04618v3 (31,009).
- **Kept apart:** SkillsBench "+16.2 pp" in a search summary, against "+16.6" over "87 tasks" in the v4 abstract. E3
  uses the v4 numbers.
- **No shell, so not done:**
  - F1 cannot tell an empty `project-memory/` from a missing one;
  - LZ7: md5 not computed, and the symlink not confirmed on the filesystem.
- **Not checked:**
  - past non-Claude runs, for a broken auto-memory-only rule (Q11);
  - whether anything was ever removed from EJ's memory (Q17);
  - every expert's classical quotes against classical texts. The COO's `four_experts.py check` compared them with the
    rules lists (§6 head).
- **Budget:**
  - v0: 21 searches and 31 fetches;
  - v1: 2 fetches;
  - v2: 2 Globs, 3 Greps, 3 Reads and 1 config grep;
  - v3: 1 Read and 1 Grep;
  - v4: 0 web calls; 1 Glob and 1 Grep of the skill folder, 1 Grep of `CLAUDE.md`, and 1 Read of
    `assets/templates/state.md`.

  Raw text was saved for S1 and S2 under `sources/`.

## Sources

| id | Source | Date | How read |
|---|---|---|---|
| S1 | Claude Code docs, "How Claude remembers your project" — https://code.claude.com/docs/en/memory | undated; fetched 2026-10-13 | raw text saved, `sources/claude-code-memory.md` (verified) |
| S2 | Claude Platform docs, "Memory tool" — https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | undated; fetched 2026-10-13 | full-text return, excerpts in `sources/claude-memory-tool.md` (verified, with that note) |
| S3 | Claude Code docs, sub-agents — https://code.claude.com/docs/en/sub-agents, via `runs/20261012-agent-memory-claude-code/notes.md` | notes 2026-10-12 | reported |
| S4 | Anthropic, "Effective context engineering for AI agents" — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2025-09-29 | WebFetch (reported); background only |
| S5 | Anthropic, "Effective harnesses for long-running agents" — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | 2025-11-26 | WebFetch (reported) |
| S6 | Claude blog, "Managing context on the Claude Developer Platform" — https://claude.com/blog/context-management | 2025-09-29 | WebFetch (reported) |
| S7 | Anthropic, "How we built our multi-agent research system" — https://www.anthropic.com/engineering/multi-agent-research-system | 2025-06-13 | WebFetch (reported) |
| S8 | Anthropic, "Introducing Claude 4" — https://www.anthropic.com/news/claude-4 | 2025-05-22 | WebFetch (reported) |
| S9 | OpenAI Codex docs, AGENTS.md — https://learn.chatgpt.com/docs/agent-configuration/agents-md | undated | WebFetch (reported) |
| S10 | OpenAI Codex docs, Memories — https://learn.chatgpt.com/docs/customization/memories.md?surface=app ; v1 re-fetch https://learn.chatgpt.com/docs/customization/memories | undated | WebFetch (reported) |
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
| S22 | Fan et al., "VibeMemBench" — https://arxiv.org/abs/2609.23570 | 2026-09-20 | WebFetch (reported); abstract re-fetched in v1 |
| S23 | CodeCompass, arXiv 2602.20048, via `docs/research/20261011-agent-memory-graph-r2/FINDINGS-s3-project-graph.md` F33 | 2026-02-23 | repo row (reported) |
| S24 | MemoryArena (arXiv 2602.16313), HaluMem (arXiv 2511.03506), via `docs/research/20261011-agent-memory-graph-r2/INDEX.md` s5-F6, s5-F5 | 2026-09-17 / 2026-01-05 versions | repo rows (reported) |
| S25 | GitHub issues anthropics/claude-code — https://github.com/anthropics/claude-code/issues/34763 , /40272 , /43098 | 2026-03-15, 2026-03-28, 2026-04-03 | WebFetch (reported) |
| S26 | This repo: `docs/WORKFLOW_DESIGN_METHOD.md` (§4 L480–514, §5 L522, App. B L541–553); `.claude/skills/workflow-design/SKILL.md` L81–85, L91–93; `docs/memory-system/SOURCE_OF_TRUTH.md` (L3, L44, L64–72, L107, L113–119, L168, L253–254, L261–270, L301–307, L315–316, L344, L345, L371, L383, L386, L400–404); `docs/research/20261011-agent-memory-graph-r2/DIGEST.md`; `runs/20261012-agent-memory-claude-code/notes.md`; repo greps (v2) | 2026-10-11 to 2026-10-13 | read directly (verified) |
| S27 | Linus (codex), `experts/answers/linus.md` | 2026-10-13 | read directly (verified as to what he wrote) |
| S28 | `runs/20261013-memory-in-workflow-design/question.md` (L10, L11) | 2026-10-13 | read directly (verified) |
| S29 | 范蠡 (Claude subagent), `experts/answers/fan-li.md` | 2026-10-13 | read directly (verified as to what he wrote) |
| S30 | This repo's `AGENTS.md` (4 lines; L3) | read 2026-10-13 | read directly (verified) |
| S31 | Claude auto memory: `~/.claude/projects/-home-smoke01-dev-ancient-games/memory/MEMORY.md` (36 lines), `stay-in-own-scope.md` | read 2026-10-13 | read directly (verified) |
| S32 | `~/.codex/config.toml`: no `fallback`/`project_doc` setting | checked 2026-10-13 | grep (verified, absence only) |
| S33 | 孫子 (dsh / DeepSeek), `experts/answers/sun-tzu.md` | 2026-10-13 | read directly (verified as to what he wrote) |
| S34 | 老子 (opencode / MiniMax), `experts/answers/lao-tzu.md` | 2026-10-13 | read directly (verified as to what he wrote) |
| S35 | This repo's `CLAUDE.md` L45 ("links into `docs/`, so there is one copy of each"), and `.claude/skills/workflow-design/assets/templates/state.md` (first 4 lines read) | read 2026-10-13 | read directly (verified as to the text; link status not checked on the filesystem) |

(S14 is unused: no official Antigravity source was found.)
