# Dave — five open points in the memory design's requirements

## Answer
- **A.** Keep the removal. Change W6.3a so its text uses the same word as its `fails_if`: *"…and every `covers` path either side added. A path that one side removed with a `changed:` line stays removed (K4.3)."* Add to `fails_if`: *"…or it keeps a `covers` path that one side's `changed:` line removed."*
- **B.** The kit carries `tools/memory_index.py`, its two test files and `docs/index-md/`. There is no "installed separately" route. This holds if the kit is copied into each project. If projects share one installed copy, the answer flips (see What I need to know, item 3).
- **C.** Each project records its agents and their limits in one small file in its own `project-memory/` (*proposed* name: `start-limits.yaml`). Each row gives an agent, the engine version, the load path, the limit, its unit, and the basis (a run id for a measurement, or a source for a documented figure). The tool fails `INDEX.md` against the strictest row. If the file does not exist, the tool uses the Rd3.1b example and prints that it is doing so. Not `AGENTS.md`, and not the tool's constants.
- **D.** What counts is how `INDEX.md` gets into each session, not which agents work on the project. Wording for Rd3.1a: *"`INDEX.md` fits the strictest limit among the ways it reaches the agents that load it at session start (Rd2.1): an `@` import counts against the importing file's limit; a shared budget counts `INDEX.md` together with the other files in that budget; an agent that reads it with a file read is held to that read's limit."*
- **E.** Measure now, before the tool change. On each engine, load a test `INDEX.md` the way the design loads it, at sizes just under and just over that engine's documented limit. The tool change comes afterwards, in its own run, as already settled.

## How I decided
**A**
1. My #5. The data I have: W6.3a's text says *"every `covers` path either side **wrote**"*, but its `fails_if` says *"a `covers` path that one side **added**"* (*read*: `SOURCE_OF_TRUTH_REQUIREMENTS.yaml:450-462`). K4.3 lets `covers` be corrected with a `changed:` line (*read*: `:522-530`). The two words split on exactly this case: the stale path was in the common base, so neither side added it, but either side's file can be said to have "written" it. Insight `runs/20261016-integrate-r11-r13/insight.md#F-d8a49e5a`: a restated rule whose words drifted from its source widened a gate. This changed my answer from "the rule is fine" to "make the text match the `fails_if`".
2. My #4, with git's own merge as the control. W1.2b puts one `covers` path per line (*read*: `:125-133`). Git takes a line changed on only one side from that side, so the removal survives with no conflict (*recall*, not measured). The stale path comes back only when someone resolves a conflict by hand, for example where the removal is next to the other side's added path. The current word "wrote" tells that person to put it back.
3. My #9. I planned a scratch-repo merge test of three cases (my #2), but the write to `/tmp` was refused in this session. So step 2 is still *recall*.
4. My reading: putting the stale path back leaves the entry contradicting its own `changed:` line, which W6.3a also tells the merge to keep. So the removal wins.

**B**

5. My #5. Nine records use `check: tool` (*read*: grep count of the YAML). K6.2 is a MUST: `INDEX.md` is rebuilt by the tool, and it *"is never edited by hand"* (*read*: `:588-604`). Without the tool, a project cannot pass K6.2 at all. The `kit` key mentions `tools/` and `docs/index-md/` only as paths (*read*: `:64-67`). The tool needs only Python's standard library and git (*read*: `tools/memory_index.py:17-28`). Its tests are `tests/test_memory_index.py` and `tests/test_memory_index_unit.py`.
6. Vision: *"A fresh session with only a clone of the repo can carry on"* (*read*: vision statements `:66`, marked [proposed]). Carrying on includes writing an entry, and that needs the tool. My reading.
7. Insight `runs/20261016-integrate-r11-r13/insight.md#F-682702da`: an exported bundle was missing a file its own text named. The fix was a check that every named file exists. This is the same shape, so I add that check to "How we would know".
8. My #4, against the control "installed separately". That route needs a second rule for projects without the tool, which is new structure just to make the kit one script and one folder smaller. My reading: not worth it.

**C**

9. My #5. The numbers sit in three places (Rd3.1a, Rd3.1b, `memory_index.py:35-36`), plus the table in `CACHES.md`. The project owner decides which agents work on the project, and decides it per project (*read*: `:722-723`). So the record belongs to the project, not to the kit and not to the tool.
10. My reading on the two rejected places:
    - **`AGENTS.md`:** it is loaded at every session start (Rd2.1), so a limits table there costs every session. For Codex and dsh it would also use up the same shared budget it describes (*verified* in the research). And the tool would have to parse a section of a prose file.
    - **The tool's constants:** the tool travels in the kit (B), so the next kit copy would overwrite a project's values. The owner would also have to edit code to record a decision.
11. My #8. A small file can be undone (delete it and the example applies again). The commit that adds it is the visible moment the interim example stops applying.
12. Insight `runs/20261017-experts-speed-trial/insight.md#F-1ed514ad`: a test asserted a number nobody gave. So each row carries its basis, and the tool's later tests check behaviour ("the strictest row wins"; "no file means the example, said aloud"), never a size.

**D**

13. My #5. Two documented facts from the research (*verified*):
    - Claude Code's 200 lines / 25KB *"applies only to `MEMORY.md`"*. `CLAUDE.md` and its `@imports` load up to 4 MiB.
    - Qwen Code's 200 lines / 25,000 code units applies to its own auto-memory `MEMORY.md` index. Its `QWEN.md`/`AGENTS.md` imports have no stated limit.

    The design loads `INDEX.md` into Claude Code through an `@` import in `CLAUDE.md` (*read*: Rd2.1, `:661-668`).

    My reading: on the design's own load path, neither source of Rd3.1b's "200 lines" applies to `INDEX.md`. agy's 24,000 bytes per file applies only if agy loads `INDEX.md` as one of its own files. Whether agy follows imports is not in the research (*not measured*). `CACHES.md:494` already says Codex's limit applies to the index "if the index is loaded through `AGENTS.md`", and `CACHES.md:497` says the same for dsh's instruction files.
14. My #6 and #7. Liebig's law of the minimum: a plant's growth is held back by the scarcest nutrient it actually takes up.
    - **What is the same:** the strictest limit is the one that binds (`CACHES.md`: *"the binding limit is the smallest one among them"*).
    - **What is different:** a nutrient the plant does not take up does not limit it, and here a limit counts only if `INDEX.md` passes through it. That key condition matches.

    I use the analogy to state D. It is not evidence.
15. So "all agents that work on the project" counts too many agents. Picking a limit by agent name alone also picks the wrong one (Claude's `MEMORY.md` limit).

**E**

16. My #1. What would change my mind on D: a Claude Code session that loses the end of an `@`-imported `INDEX.md` just over 25 KB. One call settles it.
17. My #2. The test costs one headless call per engine and size. The argument already spans three documents and five open points.
18. My #3, with these predictions written before any result:
    - **Claude Code:** an `@`-imported `INDEX.md` loads in full above 200 lines and 25 KB.
    - **agy:** cuts the file at 24,000 bytes, but only if it loads `INDEX.md` at all.
    - **Codex:** counts `INDEX.md` only if it is in the `AGENTS.md` chain.

    Metric: the agent returns the marker on the file's last line without reading the file.
19. My #8 and #10. Measure one engine first: Claude Code, the load path Rd2.1 names. Then the others. Each result is n=1 per engine and size, so it is a hint. Loading is done by code, not by sampling, so a clean pair (found just under, missing just over) is enough for this use.
20. Insight `runs/20261016-four-experts-what-counts-as-change/insight.md#F-e69dfb66`: an engine passed on a tiny test input and then failed at real size. So the test files sit either side of each documented limit, not a few lines long.
21. Already settled: the 23:47 log line in `runs/20261017-sot-item11/state.md` says *"a tool build is its own later run"*. I do not reopen it. My #8 supports the order: build the reader once there is a real row for it to read.

*Proposed change to the pattern:* every measuring step writes its prediction line into the run's `state.md` before its first call (my #3). That makes a later "as expected" checkable instead of remembered.

## What I need to know
1. Does a documented limit (with its source and engine version) end the interim example, or only a measured one? Rd3.1a says "measured".
   - If a documented limit counts, the C file can be written today from the research table, and E checks it.
   - If only a measured one counts, E has to come first.
2. Does Rd3 mean only "`INDEX.md` is not cut off on the way in", or also "keep the start load small" (`CACHES.md`, *"Why the start load should stay small, whatever the window"*)?
   - If it also means the second, that is a separate requirement with its own basis.
   - Under D alone, a project using only Claude Code would have its limit rise from 200 lines to whatever its load path allows.
3. Is the kit copied into each project's repo, or run from one shared install? If it is one shared install, B flips: the design then needs a rule for what a project without the tool does.
4. Which agents work on the first project to use the kit? The project owner decides, and the answer sets the order of E's measurements.

## Costs and risks
- **A (my #4):** a merger now has to read the `changed:` lines before resolving a conflict. If the other side deliberately wanted the path kept, that is lost unless it adds the path again with its own `changed:` line.
- **B (my #8):** each project holds its own copy of the tool, and the copies can drift apart between kit versions. The kit also grows by one script, two test files and one folder.
- **C (my #8):** one more file in `project-memory/`, so Rd1.1's layout list (`:635-645`) has to name it. Rows go stale when an engine is updated, which is why each row carries the engine version.
- **D (my #5, #7):** if the owner meant "keep the start load small", this wording lifts the bound for Claude-only projects. That is what question 2 above is for. The analogy is only a way to state the rule; if it were mistaken for evidence it would add nothing.
- **E (my #2, #10):** engine quota (Codex hit its usage limit mid-run before, `runs/20261015-ts-hybrid/insight.md#F-3b8bdcec`), and n=1 per engine and size. A missed marker at a large size could be the model not recalling it rather than the file being cut. The first-line marker, and a control run with the import line removed, separate the two.
- **Not tested (my #9):** the merge behaviour in A is *recall*. The experiment could not run in this session because the write to `/tmp` was refused.

## How we would know I was right
- **A:** a scratch repository with three merges (one-path-per-line removal; removal next to the other side's added path; a one-line list). After the reworded W6.3a, every merged entry has no path its `changed:` lines removed, and has every path either side added.
- **B:** on a fresh project with only the kit copied in, `python3 tools/memory_index.py --check` runs. A kit check (from F-682702da) finds that every path the YAML names, under `check: tool` and K6.2, exists in the kit.
- **C:** a reviewer can answer "is the interim example still in force?" from whether the file exists and the tool's printed size line, without reading code.
- **D and E:** the marker test with the predictions in step 18. I am wrong on D if Claude Code's last-line marker is missing just over 25 KB while the first-line marker is found. The `start-limits` file and the reworded Rd3.1a then go back to the `MEMORY.md`-sized limit.
