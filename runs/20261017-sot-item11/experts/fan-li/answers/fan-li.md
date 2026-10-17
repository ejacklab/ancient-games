# 范蠡 (Fan Li) — five open points in the memory requirements (A–E)

## Answer
**A:** the merge keeps the removal. **B:** the kit carries `tools/memory_index.py` and `docs/index-md/`. **C:** the project owner writes the readers and their measured limits in one small data file of the project's own, which the tool reads, and Rd3.1a stops repeating the numbers. **D:** the agents that read `INDEX.md` at session start, each limit taken on the path that loads it. **E:** not now. Build the tool change in its own run once the first measured limit is recorded. Measure only agy's path, and only if agy is named as a reader and an `INDEX.md` grows past the reported 12,000 characters.

## How I decided

**A. A merge, and a path one side removed**
1. My #5, `quoted`: 「夫謀之廊廟，失之中原，其可乎？」. A path removed under K4.3 was decided on one branch, and that branch wrote it down in a `changed:` line. W6.3a already makes the merger keep both `changed:` lines. If the merge also brings the stale path back, the merged entry says the path was removed and still lists it. That is a plan made at court and lost on the field.
2. My #12, `quoted`: 「又觀其民之饑飽勞逸以參之」. Act only on a sign you have cross-checked. Here the cross-check is the `changed:` line. A removal counts when its `changed:` line is there. A path that is missing with no `changed:` line is not a removal: K4.3 already fails that case (*read*: YAML:532-534), so the merge keeps the path.
3. My reading, based on `SOURCE_OF_TRUTH.md:68-70` (*read*): git merges edits on different lines with no conflict. So this case only comes up when both sides edited `covers` and someone resolves it by hand. The current words "every `covers` path either side wrote" then read as "take both copies together", and the side that did not touch the path still holds it.
   **Wording, W6.3a text:** "…both `changed:` lines, both links, and every `covers` path either side added; a path one side removed with a `changed:` line stays removed." **fails_if:** "a merged entry is missing a `changed:` line, link or `covers` path that one side added, still holds a `covers` path that one side removed with a `changed:` line, or two entries superseding one go unreported."

**B. What the kit carries**
4. My #18, `quoted`: 「審備則可以戰乎？」. Check the preparations before the fight. K6.1a and K6.2 fail when `INDEX.md` "differs from what the tool builds" (*read*: YAML:578-580, 603-604). Without the tool, nobody can make that comparison. A kit without it carries MUST records that no one can check. "Installed separately" would leave a project that copied the kit unable to meet its own gates.
5. My #14, `quoted`: 「四封之內，百姓之事，蠡不如種也。」. Say who is better at what. The prose explains, the YAML states the gates, and the tool checks them, so all three travel together. The tool is cheap to carry: one 561-line file that imports only the standard library (*read*: `tools/memory_index.py:1, 17-28`; `wc -l`).
6. My reading: name the file, not the folder. `tools/` also holds `export_skills.py`, `git-hooks/`, `why-chain-hook/` and `node_modules/` (*read*: `ls tools/`), and the pre-commit hook does not call the memory tool (*read*: grep).
   **Wording, key `kit`:** "These files travel together as one kit: SOURCE_OF_TRUTH.md, this file, CACHES.md and vision-statements/, named relative to this file's folder; and `tools/memory_index.py` (the tool `check: tool` names) and `docs/index-md/` (its requirements and design), named relative to the repository root. `project-memory/`, `AGENTS.md`, `CLAUDE.md` and `runs/` are the project's own."

**C. Where the measured limit is recorded**
7. My #5, `quoted`: 「唯謀不遷」. The plan does not shift, so one place holds it, not three. Rd3.1a stops repeating "200 lines and 24,000 bytes" and points to Rd3.1b. The tool keeps the example only as its value when nothing is recorded, with a comment citing Rd3.1b.
8. My #14 again: each party has its part. The project owner decides which agents count (*read*: Rd3.1a `who_decides`, YAML:724). A measurement supplies the number, and the tool compares. So the record is the project's own, not part of the kit.
   - **Not the tool's constants.** Under B the tool travels in the kit, so one project's limits would travel with it into a project that uses other agents (my reading).
   - **Not `AGENTS.md`.** Every agent loads it at session start (*read*: Rd2.1, YAML:665-668). A limits table there would use up the start-file room Rd3 protects, for data only the tool and a reviewer need (my reading).
9. My reading: use a small data file in `project-memory/`. The name is *proposed*: `project-memory/start-limits.json`. It has one row per reader:
   - the agent;
   - the path that loads `INDEX.md` (see D);
   - the limit, in the unit its source uses (lines, bytes, UTF-16 code units, characters or tokens — the research shows all of these);
   - the evidence path under `runs/<run-id>/`;
   - the date.

   I chose JSON because the tool uses only the standard library, and JSON is the one data format the standard library reads on every Python 3 (*recall*). A reviewer can see that the interim example has stopped applying when this file exists. The tool's run should also print which of the two applies; B4.2 already prints the size against both limits (*read*: `docs/index-md/REQUIREMENTS.md:67`). Rd1.1's list of what `project-memory/` holds would gain this file.
   **Wording, Rd3.1a, last sentence:** "The project owner records the agents, their load paths and their measured limits in `project-memory/start-limits.json`; while it does not exist, the tool's limit is the example in Rd3.1b."

**D. Which agents count**
10. My #1, `quoted`: 「夫人事必將與天地相參，然後乃可以成功。」. A limit only applies where an agent and its load path meet. Take an agent that works on the project but does not load `INDEX.md` at start, such as an engine that is handed a brief. It has no start-file limit for `INDEX.md`, and counting it would tighten the limit for nothing. The Rd3 title (*read*: YAML:710) and the prose (`SOURCE_OF_TRUTH.md:157`) already say "the agents that read it". Rd3.1a is the odd one out, so Rd3.1a is the one to change.
11. My #9, `quoted`: 「天地未形，而先為之征，其事是以不成」. Do not act before the shape is visible, and the research shows the shape belongs to the load path, not the agent:
   - Claude Code's 200 lines / 25KB "applies only to `MEMORY.md`"; a `CLAUDE.md` is loaded in full up to 4 MiB (verified).
   - Qwen's 200 lines / 25,000 code units is the cap on its auto-memory `MEMORY.md` index. No limit is stated for `QWEN.md` or `AGENTS.md` (verified).
   - Under Rd1.1 and Rd2.1 (*read*: YAML:639, 665-668), `INDEX.md` reaches Claude Code through an `@` import in `CLAUDE.md`, not through `MEMORY.md`.

   My reading: so two of the three agents behind Rd3.1b's example ("Claude Code, Qwen and agy") give figures for a path `INDEX.md` does not use. The example is still at or under every verified per-file figure, so it is safe, but the reason it gives for itself is wrong. Whether an imported file counts toward the 4 MiB alone or together with `CLAUDE.md` is not stated.
   **Wording, Rd3.1a, first sentence:** "`INDEX.md` fits the strictest start-file limit among the agents that read it at session start, each limit taken on the path that loads it there (Rd2.1)." **`who_decides`:** "project owner: which agents read `INDEX.md` at session start and by which path, and so the strictest limit."

**E. Build the tool change, and measure?**
12. My #5 again: the default EJ accepted for Q3 stands — "a tool build is its own later run" (*read*: `runs/20261017-sot-item11/state.md`, log line 2026-10-17 23:47). I do not reopen it.
13. My #3, `quoted`: 「時不至，不可彊生；事不究，不可彊成。」 and my #7, `quoted`: 「王無蚤圖」.
   - This repo has no `project-memory/` (*read*: `ls`), so no `INDEX.md` here can come near any limit.
   - While C's file does not exist, Rd3.1a says the tool uses the example, and it already does (*read*: `tools/memory_index.py:35-36`). The code is right today.
   - Building now would mean a reader for a file nobody has written.
14. My #1, `quoted`: 「人事至矣，天應未也，王姑待之。」. Wait until both sides have arrived. Build when the project owner has named the readers and their paths (D) **and** has recorded the first measured limit, so C's file exists.
15. My #12, and my #10, `quoted`: 「無過天極，究數而止」. Measure only where the sources disagree, and stop once that is settled. The example is at or under every verified per-file figure. The one figure it is not under is agy's 12,000 characters, which is *reported*, not verified. So:
   - Measure agy's load path once, when both of these hold: agy is named as a reader through a path its rule-file limit covers, and an `INDEX.md` grows past 12,000 characters.
   - The other paths need no measurement while the example is stricter than their verified figures.
   - If neither condition ever holds, never measure.
16. My #4, `quoted`: 「得時無怠，時不再來，天予不取，反為之災。」. When the trigger comes, one run does the whole job: the code, its tests, the Rd3.1a wording that points to the file, and the tool's comment.

*Proposed change to the pattern:* research on a limit should ask about each **load path**, not each agent. This run's table and `CACHES.md`'s are both organised by agent, and that is how a `MEMORY.md` cap ended up behind the `INDEX.md` example. The change is one line in how research questions about limits are written.

## What I need to know
- **May a documented limit stand in for a measured one?** If the project owner accepts a documented limit with its URL and date, each row of C's file carries a label, *measured* or *documented*, and this run's research can be recorded now. If not, the file waits for E's measurement.
- **Which agents read `INDEX.md` at session start, by which path, in the projects that will use the kit?** If agy is not among them, E's one measurement is not needed.
- **Does any project already have a `project-memory/INDEX.md`, and how big is it?** I checked only this repo. If one is past 12,000 characters and agy reads it, E's trigger has already fired.
- **Must the kit run where there is no Python 3?** If so, B needs a fallback. `reviewer` cannot take the tool's place for K6.1a and K6.2, because their `fails_if` is defined by the tool's output. That would be a change to the design, not a change of wording.

## Costs and risks
- **A** (my #5, #12): the merger has to read the `changed:` lines instead of just taking both lists. If a removal was a mistake, the path stays out until someone corrects `covers` again. Nothing is lost, because git and the `changed:` line keep it.
- **B** (my #18, #14): every project that adopts the kit needs Python 3. The tool and the YAML can drift apart if they are copied at different times. `docs/index-md/` also brings its `BACKLOG.md`, which is the tool's own work list.
- **C** (my #5, #14): a new file and a new format, and Rd1.1's list changes. Readers count in different units (code units, bytes, characters, tokens), so the tool must compare each row in its own unit, or the row must say how it was converted. The JSON choice rests on *recall*.
- **D** (my #1, #9): an agent that reads `INDEX.md` later rather than at start is not covered; if its read limit is smaller than the index, nothing checks it. This change also exposes that Rd3.1b's stated basis is wrong, which means one more edit.
- **E** (my #3, #7, #12): while we wait, agy may cut off an index past 12,000 characters if that figure is real. The tool prints the size on every run (B4.2) but does not compare it to 12,000, so a person has to notice. That is the price of not building yet. The example also stays stricter than needed on paths like Claude Code's 4 MiB: an index can fail the check at 201 lines even though no reader would cut it. Nothing is lost (B4.3), but the commit stops.

## How we would know I was right
- **A:** a test merge. The base `covers` holds `old/x.py`. Branch 1 replaces it with `new/x.py` and adds a `changed:` line. Branch 2 adds a link in the same header block. Resolved under the new wording, the entry holds `new/x.py`, both `changed:` lines and the link, and not `old/x.py`. Resolved under the old wording, taking both lists, `old/x.py` comes back.
- **B:** copy only the kit into an empty repo, add one entry, and run `python3 tools/memory_index.py` and then `--check`. Both run, and every `check: tool` record has something that can fail it. Without the tool, the same copy cannot judge K6.2 at all.
- **C:** `grep -n "24,000\|24_000\|200 lines"` across the YAML and the tool finds the numbers only in Rd3.1b and in the tool's fallback. With the file present, the tool prints that the recorded limit applies; with the file removed, it prints that the example applies.
- **D:** the Rd3 title, `SOURCE_OF_TRUTH.md:157` and Rd3.1a all name the same set of agents.
- **E:** if the trigger fires and the agy measurement shows text cut off below 24,000 bytes, waiting cost something and the example was too loose. If it shows 24,000 bytes, waiting cost nothing. If the trigger never fires, nothing was spent.
