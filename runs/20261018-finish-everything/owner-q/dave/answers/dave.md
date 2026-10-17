# Dave — owner-only questions at once? Claude Code's memory in memory-check F1?

## Answer

**Q1: (a), adopt it, with one step first.** Before an unclear spot is called a question no trial can answer, try to reshape it so a trial can answer it (a comparison instead of a number). Send only what is left to EJ, naming whose fact or value it is. In a time-boxed run, decide it provisionally at once and list it in the state file as soon as it is decided.

**Q2: (a), list it as present or absent only, labelled "Claude Code's memory, not a location the guidelines name".** Never (b). Whether that folder is agent, user or project memory is a question for the source-of-truth design, sent there as a request, not decided inside memory-check. If EJ reads the vision's "against the two memory guidelines" as also limiting which locations are listed, then (c).

## How I decided

### Q1

1. **What would change my mind (my #1).** Two observations would settle it. First, does a trial ever settle an owner-only question? Second, does EJ answer a listed question before the run ends? If trials do settle them, (b) is right. If EJ never answers before the end, (a) changes little beyond the wording.
2. **Data we already have (my #5).**
   - The three-trial rule is method 3.8 item 14. A trial is "one provisional choice tried and checked". A question goes to the owner "only after three failed trials on it, or once the time the owner gave is used up" (`docs/WORKFLOW_DESIGN_METHOD.md:555-558`, quoted). Its Fails-if makes asking the owner earlier a failure (`:591-593`).
   - Outside a time-boxed run, 3.3 already sends a *decision* spot straight to EJ (`:243`). Every task now starts by asking for its time (`:532-534`, and Fails-if `:591`), so item 14 governs nearly every run (my reading).
   - An owner-only question has no check that a provisional choice can fail. Under (b) it can never collect three failed trials, so it waits for the time to run out and reaches EJ in the end report (my reading of `:555-558`). The rule says nothing about exactly these questions, and its Fails-if forbids raising them earlier.
   - The one run where this came up was 20261017-memory-check. It decided its owner-only questions provisionally at once: the required locations (item 2) and a real project to calibrate on (item 15). It ran no trials on them and listed them for EJ at the end (`runs/20261017-memory-check/design-decisions.md:8-9,24`, `report.md:26-31`, quoted). In practice, that run already did what (a) says for a time-boxed run.
   - What this does not show: whether EJ would have answered earlier if asked, or whether any work resting on those provisional decisions will need redoing. EJ has not accepted or declined them yet (not measured). n=1, a hint (my #10).
3. **Control (my #4).** (b) is the control. The memory-check run is its only data point, and not a clean one, because that agent already behaved as (a) says. Both rules gave the same outcome there (my reading). So the change is cheap. Its value is fixing two things (b) gets wrong:
   - a Fails-if that forbids listing an owner-only question early;
   - a pull to invent a check so that "trials" can happen.
4. **Insight used: `runs/20261017-experts-speed-trial/insight.md#F-1ed514ad` (with F-1c81bc00).** An agent wrote a size limit nobody gave into a test, and the fix was to test the structure, not a number. This changed my answer in two ways:
   - It is the failure (b) invites when an owner-only value is forced into a trial.
   - It shows that "a threshold only the owner can set" is often not needed at all. EJ said as much of a design guide: *"this is design guide, how can I give you a number?"* (`docs/memory-system/vision-statements/caches-memory-vision-statements.md:54`, quoted).

   So (a) without a reshaping step would send EJ exactly the question they asked not to be sent.
5. **Nature (my #6, #7).** The closest living system I know is the immune system, which routes a threat by its kind at once rather than after failed attempts (recall, not checked).
   - Same: classify first, then respond.
   - Different, and this is the key condition: the immune system classifies by a pattern it can test. An agent decides "no trial can answer this" by judgment, and judgment can be wrong.
   - The method already routes by kind (3.3: information, decision, unknown, `:243`), so there is no new mechanism to borrow. What the analogy does show is that the classification needs a marker someone can check, hence the "whose" line below.
6. ***Proposed change to the pattern.*** The rule "a question goes to EJ only after three failed trials on it or once the time is used up" gains this:
   - A question no trial can answer goes at once. In a time-boxed run, it is decided provisionally at once and listed in the state file.
   - Before it is listed, the agent tries to reshape it so a trial can answer it: a comparison instead of a number, a structure instead of a size.
   - The listed question names whose fact or value it is: a location a requirement names, a project only EJ knows of, a choice only EJ may make.

   What it changes: the text of item 14 and its Fails-if line (the item number stays, since method numbers are cited), plus one "whose" line in each listed question.
7. **Prediction, written before any result (my #3).** Over the next three time-boxed runs, no owner-only question is settled by a trial. That is the review count 3.3 already uses for its expert step (`:273-274`). Metric: how many listed questions EJ or a reviewer reclassifies as trial-able or reshapeable. Stop: after the third run's report.

### Q2

1. **What would change my mind (my #1).** If the source-of-truth design places the folder in one of its scopes, or rules it out, F1 follows the guidelines and the question closes either way. If a test shows memory-check cannot find the folder reliably for every project path, (a) would report a wrong "absent". That fails F1's own Fails-if, and then the answer is (c).
2. **Data we have (my #5).**
   - F1 covers "every memory location the guidelines name", with "Who decides: the guidelines" (`memory_check/REQUIREMENTS.md:9-14`, quoted). The guidelines define the agent scope as "memory belonging to one agent name" and place it at `~/.claude/agent-memory/<name>/` (`docs/memory-system/SOURCE_OF_TRUTH.md:20,23-25`, quoted).
   - Claude Code's folder is keyed by the project path, not by an agent name. This repo's folder holds facts about the user and facts about the project side by side (its `MEMORY.md` index, read this session). By the guidelines' own definitions it is not agent memory (my reading), so the answer to the question's title is no.
   - On this repo, memory-check reports `/home/smoke01/.claude/agent-memory` as absent (`runs/20261017-memory-check/nodes/smoke-report.md:17`, quoted). Meanwhile the Claude Code folder holds 48 entries (`ls … | wc -l`, today; the question says "about 50").
   - W3.5b, "User memory and agent memory live in the home folder", is listed as needing a reviewer (`SOURCE_OF_TRUTH_REQUIREMENTS.yaml:274-280`; `smoke-report.md:37`, quoted). The row in (a) is the evidence that reviewer needs.
   - The caches guideline already treats this `MEMORY.md` as an index read at session start, with Claude Code's 25 KB load limit. But that sits in its example section (`CACHES.md:489-512`), not in its Core requirements (`:310-470`), so memory-check checks nothing from it (verified by the line ranges).
   - What this does not show: whether EJ or an agent would act on the row. Not measured.
3. **Vision and use cases first (my reading).**
   - (a) serves U1's purpose, "the owner learns which memory exists". It also serves the vision's second reader: "Every agent starting a session, which must not start work on memory that is missing, stale or broken without being told" (`memory_check/USE_CASES.md`, `VISION.md`, quoted). An agent in this repo starts every session on that index.
   - (b) serves none of them. The folder does not follow the guidelines' entry format, so every entry check would fail on memory the guidelines never governed. The vision also says "The tool adds no rule of its own."
   - (c) serves F1 as written and nothing more.
4. **Control (my #4); small and reversible (my #8).** (c) is the control: today's report. (a) is one row, present or absent, with no check and no warning line, and it can be removed as easily as it is added. (b) is the scaled-up version, and it makes sense only after the guidelines give that folder a format.
5. **A small experiment beats a long argument (my #2).** One risk in (a) can be settled by a test: how the folder name is derived from the project path. The question gives that `/` becomes `-`. What happens to `.`, `_`, a worktree, or a session started in a subfolder I do not know (recall at best, not checked here). The test costs less than this debate: build fixtures with such paths and compare the path memory-check reports with the folder Claude Code creates.
6. **One design, one document (my reading of the project's rule).** Whether the folder is agent, user or project memory belongs to the source-of-truth design, not to memory-check. So the row says "not a location the guidelines name", does not call it agent memory, and a request goes to that design. If that design names the folder, F1 lists it with no change to who decides.
7. **Insights:** none applies to Q2. The index has no entry on memory locations or on Claude Code's memory (I searched the insight files for "agent memory"). No category was named for me; for Q1 I chose from the index (category: instruction).
8. **Nature (my #6, #7):** I found no living-system mechanism that adds anything here, so I used no analogy.

**How sure (my #10).** Q1 rests on one run (n=1) plus the method's text, so it is a hint. For Q2 the definitions are verified in the files; the value of the row is not measured.

## What I need to know

- **Q1:** Does EJ read a run's state file while a time-boxed run is going, and answer a listed question then? If yes, (a) shortens the wait and the redo. If no, (a) in a time-boxed run only fixes the wording and the Fails-if line: still worth doing, but small.
- **Q1:** Does "listed for the owner" mean the state file at the moment of decision, or the end report? My answer assumes the state file.
- **Q1:** Will EJ accept or decline memory-check's provisional items 2 and 15? A decline that forces redo is the cost that (a)'s early listing exists to cut.
- **Q2:** Is memory-check limited to the locations the guidelines name (then (c)), or does it cover all the memory a project has (then (a))? EJ's reading of their own vision decides this.
- **Q2:** Will the source-of-truth design be asked to place the folder in a scope? If it names the folder and gives it a format, (b) follows from the guidelines, not from memory-check.
- **Q2:** How does Claude Code name the folder for paths with `.` or `_`, for worktrees, and for sessions started in a subfolder?

## Costs and risks

**Q1 (a):**
- EJ is asked earlier and more often. The earlier Dave seat named this cost (`runs/20261017-memory-check/research-q/dave/answers/dave.md:78`). If it turns out to be a burden, report it as a result (my #9).
- An agent may label a trial-able question as owner-only to skip work, or pass EJ a number they asked not to be given one for. The reshaping step and the "whose" line guard against this, but they are judgment, not a script (my #7: the key condition).
- In a time-boxed run, (a) still fills a gap only EJ can fill with a provisional value. CLAUDE.md's "Never fill a gap with my own value" warns against that. Listing it at once, and marking the work that rests on it, is what keeps it honest (my reading).
- The basis is n=1, a run in which both rules gave the same outcome (my #10).

**Q1 (b):** It keeps a Fails-if that forbids raising an owner-only question during the run, and the pull to invent a check. That pull has already produced one recorded failure (F-1ed514ad; my #9).

**Q2 (a):**
- F1's "Who decides: the guidelines" is bent for one row until the source-of-truth design rules on it. The row must say so, or readers will take it for a guideline location (my reading).
- A wrong path derivation would report "absent" for a folder that exists, which is F1's own failure case. The test in step 5 is the price (my #2).
- If Claude Code moves its memory, the row goes stale (recall).

**Q2 (b):** Every entry fails a format the guidelines never applied to it, and if any of those is a MUST, every session gets a warning (U3), all on memory the guidelines do not govern.

**Q2 (c):** The report keeps saying agent memory is absent while 48 entries load into every session here, and EJ must remember that from somewhere else.

## How we would know I was right

**Q1:** Over the next three time-boxed runs, stopping after the third report:
- The prediction holds: no owner-only question is settled by a trial.
- Each listed question names whose fact or value it is.
- Count the listed questions EJ or a reviewer sends back to trials or reshapes. Any at all means the classification is leaking, and (b) or a stricter step wins.
- Count those EJ answers before the run ends. Zero across all three runs means (a) bought only the wording; report that as a result (my #9).

**Q2:**
- On this repo, the report gains exactly one row, "present", and no other result or warning line changes (diff the report before and after).
- On a fixture home without the folder, the row says "absent".
- On fixtures with `.`, `_`, worktree and subfolder paths, the reported folder matches the one Claude Code made.
- The W3.5b reviewer cites the row. If no reviewer or agent ever uses it, it was noise and (c) was enough (my #9).
