# Six experts — five open points in the memory design's requirements (A–E)

Question: `research/experts.question.md`. Answers: `experts/<id>/answers/<id>.md`. All six answered; none is missing.
Labels: *quoted* (from an answer), *my reading* (the comparer's), *not measured*. This file compares; it decides
nothing. The main agent decides.

| | Linus | 范蠡 Fan Li | 孫子 Sun Tzu | 老子 Laozi | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| A: merge and a removed path | keep the removal | keep the removal | keep the removal; `covers` merges "by change, not by union" | keep the removal | keep the removal; change "wrote" to "added" | keep the removal; apply both sides to the common ancestor |
| B: kit | carry tool + `docs/index-md/` | carry `tools/memory_index.py` (the file, not `tools/`) + `docs/index-md/` | carry tool + the whole `docs/index-md/` | **kit stays as it is**; tool installed; reviewer checks until it is | carry tool, its two test files, `docs/index-md/` | carry tool + `docs/index-md/`; without the tool: "not checked", never passed |
| C: where limits live | `docs/memory-system/reader-limits.yaml`, in the kit | `project-memory/start-limits.json` (*proposed*) | `project-memory/limits.json` | `docs/memory-system/start-limits.yaml` | `project-memory/start-limits.yaml` (*proposed*) | a small YAML file "next to the index"; the owner picks name and place |
| C: file absent | **an error** | the example applies | the example, marked interim | the example applies | the example, printed | the example, "says so" |
| D: which agents | those that load `INDEX.md` at session start | those that read it at session start, by load path | those whose session start loads it | **all that work on the project** | by how `INDEX.md` reaches each one at start | those that load it at session start |
| E: build the tool change | in its own run (no timing stated) | after the first measured limit is recorded | in its own run; "the change is small" | after the file has been filled in by hand once | after the measurement | now, in its own run |
| E: measure | **now**, every engine the owner declares | only agy, only on a trigger; possibly never | later, before the first project's real `INDEX.md` relies on it | later, agy first | **now**, before the tool change, Claude Code first | later, on a trigger, agy first |
| Main items used | #2 #4–#13 #16 #18 #19 | #1 #3 #4 #5 #7 #9 #10 #12 #14 #18 | #1–#4 #6 #8 #9 #12 #16 #17 #19 | #1 #2 #4 #6–#8 #10–#15 #17–#19 | #1–#10 | — |
| Insights cited | — | — | — | — | `runs/20261016-integrate-r11-r13/insight.md#F-d8a49e5a`, `#F-682702da`; `runs/20261017-experts-speed-trial/insight.md#F-1ed514ad`; `runs/20261016-four-experts-what-counts-as-change/insight.md#F-e69dfb66`; `runs/20261015-ts-hybrid/insight.md#F-3b8bdcec` | — |

The table rows are *my reading*, condensed from each answer's "Answer" section; the items and insights are *quoted*.

## Where they agree

- **A, all six: a path one side removed or replaced, and the other did not touch, stays removed.** *quoted*: Linus
  "an explicit committed removal or replacement … is not resurrected"; Fan Li "a path one side removed with a
  `changed:` line stays removed"; Sun Tzu "a path one side removed or replaced stays removed when the other side did
  not change it"; Laozi "the merge does not bring it back"; Dave "A path that one side removed with a `changed:` line
  stays removed (K4.3)"; Dario "every `covers` path either side removed or replaced that the other side did not
  touch". Each also adds a `fails_if` clause for a restored path (*my reading* of all six).
- **A, five of six tie the removal to its `changed:` line** (Linus, Fan Li, Laozi, Dave and, through K4.3, Dario);
  Sun Tzu keeps the `changed:` line but frames the rule as a three-way merge (*my reading*).
- **C, all six: one file the tool reads, not `AGENTS.md` and not the tool's constants.** Four give the reason for
  `AGENTS.md`: it is loaded at every start and would spend the budget it describes (*quoted*, in Fan Li, Laozi,
  Dave, Dario; Linus and Sun Tzu do not discuss `AGENTS.md` — *my reading*).
- **C, all six: the numbers leave Rd3.1a**, and the example lives once (Rd3.1b) with the tool's constants as its
  fallback (*my reading*; Linus moves the example into an `interim` record in his file instead).
- **C, five of six give each row a unit and a basis** (measured / documented / example or interim): Linus, Fan Li,
  Sun Tzu, Dave, Dario; Laozi gives `measured: false|true` and "where that limit is written" (*my reading*).
- **C/E, a present but malformed file fails loudly**: stated by Linus, Sun Tzu, Laozi, Dario; Fan Li and Dave do not
  address it (*my reading*).
- **E, all six: the tool change runs in its own run**, which keeps the 23:47 default "a tool build is its own later
  run" (*quoted* from `state.md` by Fan Li, Sun Tzu and Dave).
- **E, all six: a documented figure is not a measurement of the installed engine** (*my reading*; Linus: "do not treat
  documented figures or code inspection as engine measurements", *quoted*).
- **D, five of six: count the agents whose session start loads `INDEX.md`**, aligning Rd3.1a with the Rd3 title and
  `SOURCE_OF_TRUTH.md:157` (Linus, Fan Li, Sun Tzu, Dave, Dario). Laozi disagrees (below).
- **B, five of six: the kit carries the tool and `docs/index-md/`.** Laozi disagrees (below).

## Where they disagree (side by side, quoted; never averaged)

**B — carry the tool, or install it separately**
- Five (Linus, Fan Li, Sun Tzu, Dave, Dario), e.g. Sun Tzu: *"do not rely on each project installing the right tool;
  rely on the kit having it."*
- Laozi: *"The kit stays as it is; the tool is installed, and its absence is visible … until it does, the records with
  `check: tool` are checked by the reviewer, as the secret scanner is."* Reason: *"two copies drift."*
- Within the five: Dave says the answer *"flips"* if projects share one installed copy rather than copying the kit;
  Dario: *"Where the tool is not installed, that record is reported as not checked, never as passed."*; Linus: *"a
  missing checker must fail the check rather than silently skip"*.

**C — whose file: the kit's or the project's**
- In the design's folder (travels with the kit): Linus `docs/memory-system/reader-limits.yaml`; Laozi
  `docs/memory-system/start-limits.yaml`.
- In the project's own `project-memory/`: Fan Li *"the record is the project's own, not part of the kit"*; Sun Tzu;
  Dave *"the record belongs to the project, not to the kit and not to the tool"*.
- Dario: *"The owner picks its name and location."*

**C — format: JSON or YAML**
- JSON: Fan Li *"JSON is the one data format the standard library reads"* (marked *recall* by him); Sun Tzu *"YAML would
  need PyYAML or a hand-written parser"* (*my reading of the imports*, his label).
- YAML: Linus, Laozi, Dave, Dario (*"The requirements are already YAML."*). None of the four says how a
  standard-library-only tool reads it (*my reading*).

**C — a missing file**
- Linus: *"make missing or malformed configuration an error."*
- The other five: absent means the Rd3.1b example applies (e.g. Laozi: *"Absence falls back to Rd3.1b's example; a file
  it cannot read fails"*).

**C — when the interim example stops applying**
- Laozi: *"the interim example stops applying the moment a record is there."*
- Dario: *"The interim example applies while any entry's source is `example` or an agent has no entry."*
- Sun Tzu: per row — *"a row with no measurement holds the example in Rd3.1b and is marked `interim`."*

**D — which set**
- Five: the agents that load it at session start. Fan Li: *"A limit only applies where an agent and its load path
  meet."*
- Laozi: *"'The agents that work on the project.'"* Reason: *"Rd2.1 has every agent reading `INDEX.md` at session start,
  whichever route the engine takes, so 'the agents that read it' is emptied by a tool's behaviour rather than by a
  fact."*
- Dario raises Laozi's case as a question: if no agent loads it at start, *"'agents that work on the project' is the
  only set left."*

**E — measure now or later**
- Now: Linus *"Measure now on every owner-declared installed engine"*; Dave *"Measure now, before the tool change"*,
  Claude Code first, *"the load path Rd2.1 names"*.
- Later: Sun Tzu *"before the first project's real INDEX relies on the limit"*; Laozi *"later, agy first"*; Dario
  *"measure an engine when `INDEX.md` outgrows the lowest figure for that engine that is only reported"*.
- Fan Li: only agy, only when agy is a named reader **and** an `INDEX.md` passes 12,000 characters; *"If neither
  condition ever holds, never measure."*

**E — which engine first**
- agy (the only reported figure under the example): Fan Li, Laozi, Dario.
- Claude Code (the path Rd2.1 names): Dave.
- Every declared engine: Linus. That first project's readers: Sun Tzu.

**E — build before or after a measurement**
- Independent of it: Dario *"Change the tool now"*; Sun Tzu *"Without it, C is another file nobody reads."*
- After: Fan Li *"once the first measured limit is recorded"*; Dave *"build the reader once there is a real row"*.
- After a hand-filled use: Laozi *"when C's file exists and has been filled by hand once"*.
- Linus: own run, timing not stated; measurement *"before retiring the interim value"*.

**A — two sides change the same path** (only three address it)
- Sun Tzu: *"the merge reports the clash in the task's `state.md` and the project owner decides."*
- Dario: *"the merger keeps the path that exists in the repository and says so in a `changed:` line."*
- Linus: asks it as an open question.

## What each added that the others did not

- **Linus** — *quoted*: an agent with no published limit stays *"`unknown`, not unlimited"*; asks for the full merge
  grammar (both sides remove, replace or re-add the same path); proposed pattern: an outcome criterion that every
  declared engine/version/load path *"demonstrably loads the intended portion"*.
- **Fan Li** — *quoted*: name `tools/memory_index.py`, not `tools/`, because `tools/` also holds other tools; Rd3.1b's
  basis is wrong — *"two of the three agents behind Rd3.1b's example … give figures for a path `INDEX.md` does not
  use"* (Dave reaches the same point under D); proposed pattern: research on a limit asks per **load path**, not per
  agent; `docs/index-md/` brings its `BACKLOG.md` along.
- **Sun Tzu** — *quoted*: a second, older copy of the requirements sits at
  `memory_check/guidelines/SOURCE_OF_TRUTH_REQUIREMENTS.yaml` (its W3.6 is the older text); the `kit` text is
  generated by `runs/20261014-sot-yaml-review/build_requirements.py:62`, so change it there; `--check <rev>` should read
  the limits file from that rev; a CJK test case shows bytes and UTF-16 code units diverge; proposed pattern: a value a
  check reads gets one machine-readable record. *Comparer checked*: `diff -q` shows the two YAML files differ; that
  W3.6 is the difference is *not measured*.
- **Laozi** — *quoted*: the secret-scanner precedent (reviewer as the check until a tool exists); the record holds a
  `route` (`@` import, tool loading, start hook); proposed pattern: *"an interim value carries an ending — who ends it,
  and what ending it"*. *Comparer checked*: the YAML's `checks` key says of `secret scanner` *"None exists yet; until
  one does, the reviewer is the check"* — the precedent exists.
- **Dave** — *quoted*: W6.3a's text says *"wrote"* but its `fails_if` says *"added"*, and the two split on exactly this
  case (insight F-d8a49e5a); the kit also carries `tests/test_memory_index.py` and `tests/test_memory_index_unit.py`;
  a kit check that every path the YAML names exists (insight F-682702da); predictions written before measuring;
  Rd3 may also mean *"keep the start load small"*, which D would lift for Claude-only projects; his merge experiment
  could not run (*"the write to `/tmp` was refused"*), so his A step 2 is *recall*. He counts nine `check: tool`
  records; *comparer checked*: `grep -c "check: tool"` on the YAML gives 9 (the question says "about a dozen").
- **Dario** — *quoted*: the tool *"cannot count tokens (agy's 20,000-token budget) or combined budgets (Codex,
  dsh)"*, so those rows are reported *"not checked by the tool"*; an agent with no mark on whether it loads the index
  *"counts as loading it"*; asks whether the tool already checks that `covers` paths exist.

## What they need to know (merged; each with its options)

1. **Does a documented limit (with source and engine version) end the interim example, or only a measured one?**
   (Fan Li, Dave; Linus's answer assumes measured only.) Options: (a) documented counts — rows labelled documented or
   measured, the file can be written now from the research; (b) only measured counts — E's measurement comes first.
2. **Which agents load `INDEX.md` at session start, by which path, in the projects that will use the kit — and which
   project adopts it first?** (Linus, Fan Li, Sun Tzu, Dave, Dario.) Options: (a) Ancient Games is next — its readers
   are measured before its first real `INDEX.md`; (b) another or unknown project — the example stays interim; (c) no
   agent loads it at start — D's set is empty and Laozi's "agents that work on the project" is the only set left
   (Dario).
3. **Is the kit copied into each project, or used from one shared install / by reference?** (Dave, Dario.) Options:
   (a) copied — B carries the tool; (b) shared install — B flips and the design needs a rule for a project without the
   tool (Laozi's answer).
4. **Must the kit run where there is no `python3`?** (Fan Li, Sun Tzu.) Options: (a) no — the kit states `python3` once
   as a requirement; (b) yes — `check: tool` needs a named fallback, a design change (Fan Li: K6.1a/K6.2 cannot fall
   back to the reviewer).
5. **When both sides change the same `covers` path, what happens, and who merges?** (Linus, Sun Tzu, Dario.) Options for
   the rule: (a) report the clash in `state.md`, the project owner decides (Sun Tzu); (b) keep the path that exists in
   the repository and say so in a `changed:` line (Dario); (c) leave it unwritten for now. Options for who: (a) a
   person; (b) a git merge driver, which needs code and tests (Sun Tzu).
6. **Does any project already have a `project-memory/INDEX.md`, and how big is it against the reported 12,000
   characters?** (Fan Li, Dario.) Options: (a) yes and over — agy is measured now; (b) none or under — the trigger has
   not fired. *Comparer checked*: this repo has no `project-memory/`.
7. **Does Rd3 mean only "`INDEX.md` is not cut off", or also "keep the start load small"?** (Dave.) Options: (a) only
   not cut off — D as five answered; (b) also keep it small — a separate requirement with its own basis.
8. **Who may add an agent to the limits file?** (Laozi.) Options: (a) the project owner alone (Rd3.1a's `who_decides`
   now); (b) any agent adds its own row — then `checks` needs a line on how a self-added row is reviewed.
9. **Should the kit ship the limits file pre-filled with the six engines from `CACHES.md`, each `measured: false`?**
   (Laozi.) Options: (a) yes — a project only narrows it; (b) no — the file starts absent and the fallback applies.
10. **Can agy's 12,000-character figure be settled from the installed package rather than a load test?** (Laozi.)
    Options: (a) yes — one grep; (b) no — a load test with a marker line (Dario's E test).
11. **Does the tool already check that `covers` paths exist?** (Dario.) Options: (a) yes — Dario's A rule "keep the path
    that exists" is checkable; (b) no — the merger checks it by hand. *Not measured* by the comparer.

## Check

- *quoted from the workflow's check results*: linus pass; fan-li pass; sun-tzu pass; dario pass; dave pass; lao-tzu
  **fail** — *"Chinese not found in its list: 以深為根 (nearest in the list: 以深爲根, 1 character(s) differ)"* and
  *"以約為紀 (nearest in the list: 以約爲紀, 1 character(s) differ)"*. Both are in Laozi's item 13 (his #19, which he
  marks `attributed`). *My reading*: 為/爲 are variant forms of one character, so the citation is likely right in
  meaning and wrong in glyph; the check is right to fail it as written. Laozi's answer file also begins with a stray
  line, *"I'll read the brief first."* (*quoted*).
- Engines (*quoted* from each `status.json`): Linus — **mcode** `minimax/MiniMax-M3.1-Flash-Preview`, fallback from
  codex (*"codex has 1% left (20% or less)"*); Fan Li — **claude** `claude-opus-5-5`, fallback from agy (*"task needs
  web"*); Sun Tzu — dsh `deepseek-flash (dsh headless profile)`; Laozi — opencode
  `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`; Dave — claude `claude-opus-5-5`; Dario — claude
  `claude-sonnet-5-5`. All exit 0, `ok: true`.
- *My reading*: with the fallbacks, Linus and Laozi both ran on MiniMax M3.1 Flash, and Fan Li, Dave and Dario all ran on
  Claude, so this run has three model families, not six. All six also answered one brief with one research section;
  agreement among them is not independent evidence.
- **The check script was written by Claude** and checks that each cited item number and Chinese line exists in the
  expert's own list. It does not establish that a rule was applied correctly, that a quoted fact about the repository
  is true, or that an answer is right. The comparer's own spot checks above (`grep -c "check: tool"` = 9; the
  secret-scanner text in the YAML's `checks`; `diff -q` of the two YAML copies; no `project-memory/` here) were run by
  the comparer and cover only those claims.
