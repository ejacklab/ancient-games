# Six experts — at which level does an insight belong?

Question: `runs/20261017-insight-level/question.md`. Answers: `level-q/<expert>/answers/<expert>.md`.
Labels: *quoted* (an answer's own words), *my reading* (the comparer's), *not measured*. Nobody wins here; the main agent decides.

| | Linus | 范蠡 Fan Li | 孫子 Sun Tzu | 老子 Laozi | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line, *quoted*) | "partly right … the data also contains project-specific implementation lessons beyond requirement issues" | "EJ is incorrect … the data shows genuine project-level insights rooted in repository tooling and shared test harnesses" | "Not as stated … 28 project / 22 agent-type / 6 task" | "the hypothesis is half right, and the half that is wrong is the half the owner values" | "mostly right, but not completely … 5 are project-level without being requirement issues … Another 16 carry lessons at two levels at once" | "partly right … 35 of the 56 … fit … but 21 are project-level" |
| Can a program sort it? (*quoted*) | "reliable inference from the current records is **not measured**" | "cannot sort existing insights quickly and reliably from current fields" | "can sort the written `Source:` quickly … but it cannot sort the level reliably" | "quickly but not reliably from the fields as they stand" | "quickly but not reliably from today's `Source:` and `Root cause:` text" | "can't sort the insights reliably from today's fields" |
| What the writer would add (*quoted*, shortened) | lesson, "conditions under which it applies", "who needs it: workers, callers, reviewers, or maintainers", supporting ids | `Target-level: project \| agent-type \| task` + `Target-entity:` | `Level: task \| project \| agent-type` + `Stops if:` | `fix at: <path>` + `read by: task\|agent-type\|project` | per fix option: `Learns:` + `Fires when:` | `Level:` from two yes/no questions + `Failed agent:` + `Cause owner:` |
| Main items used | #9, #10, #7, #13, #2, #18, #5 | #14, #2, #18, #3 | #1, #19, #6, #4, #11, #2, #12, #16, #5, #3, #10 | #4, #17, #6, #1, #7, #12, #8, #2, #3, #16 | #1, #5, #4, #6, #7, #2, #10, #8, #3, #9 | — |
| Insights cited (count of distinct F-ids, my count) | 12 | 10 | 38 | 33 | 57 (10 named as having changed the answer, e.g. `runs/20261016-four-experts-what-counts-as-change/insight.md#F-5182be9b`) | 36 |

## Where they agree

- **The hypothesis does not hold as stated: project-level insights exist outside requirement issues.** All six (*quoted* answer lines in the table). The ids most often given as breakers (*my count* from the answers):
  - F-682702da (export copies a multi-file skill as one file): Linus, Fan Li, Sun Tzu, Laozi, Dave, Dario (Dario: "plain tool bugs").
  - F-86553997 (journal.ts lists writable kinds twice): Linus, Fan Li, Sun Tzu, Laozi, Dave.
  - F-d8221199 (committed-export test reads uncommitted state): Linus, Sun Tzu, Laozi, Dave.
  - F-8712e9fc (export test cannot tell sessions apart): Fan Li, Sun Tzu, Dave, Dario.
  - F-5182be9b/F-1d185ee3 (export-commit-suite order written only in a memory note): Dave ("The clean break"), Dario; Sun Tzu lists F-5182be9b/F-1d185ee3 as project too.
- **The ids most often given as support** (*my count*): F-1e90a8e1 (the pipe habit): Linus, Sun Tzu, Laozi, Dave, Dario. F-0f2fa841 (a plant never shown to fail): all six put it outside project level, but at different levels (see disagreements).
- **The answer to question 1 turns on what "project requirement issues" covers.** Linus: "If *project requirement issues* includes every implementation defect … the hypothesis becomes true by definition." Sun Tzu: the wide reading "makes 'project level' mean 'anything in this repo', which empties the word." Dario: "If the former, the hypothesis holds." Dave and Laozi ask the same (*quoted*). Fan Li does not raise it (*my reading*).
- **Neither the journal's `engine` nor `Source:` says who learns.** All six cite F-7f938bdf for this (*quoted*, e.g. Fan Li: "the engine was logged as opencode, but the failure was the main agent sending a path outside the repo"). Sun Tzu, Dave and Dario add that the same `Source:` value covers several levels (*quoted*).
- **The fix is for the person writing the insight to record the level when filing it; a program then reads that field and does not guess it.** All six (row 3 of the table). Laozi and Dave say this has to happen while the facts are still known (Laozi: "A level added at filing time is written by someone who no longer knows" is the case it avoids; *quoted*).
- **One insight can carry two levels.** Linus (F-969500fa: "One exclusive label would conceal part of the lesson"), Sun Tzu ("One label per insight, or one per lesson?"), Laozi (F-b696193d: "One record holding two levels loses half of itself"), Dave (16 two-level sections), Dario ("9 Source lines name two causes"). Fan Li proposes one enum per insight and does not raise it (*my reading*).
- **Filing a lesson is not learning it** (F-4981093a): Laozi, Dave, Dario (*quoted*). Dave: "The level decides which file holds the lesson. A check at the trigger, such as the guard, is what does the recognising."
- **The check is a blind comparison of labels.** Linus, Sun Tzu, Laozi, Dave and Dario each propose comparing labels against EJ or a second labeller who has not seen the others (*quoted* "How we would know" sections). Fan Li's test is instead "100% of new insights are classified … without manual disambiguation" (*quoted*).

## Where they disagree (side by side, quoted; never averaged)

**What "task level" means.**

| Expert | *quoted* |
|---|---|
| Fan Li | "a failure whose cause, assertion, or fix is confined strictly to a single run's transient setup, planted test, or ephemeral criteria" |
| Laozi | "the thing that caused it exists only inside that run … a task-level record is not a level of learning, it is a work item, and the honest label for it is 'done, nothing to file'" |
| Sun Tzu | "the lesson is tied to this one task's own brief, spec, criterion or command … its home is the run folder" (and he asks whether EJ means a kind of task) |
| Linus | "a lesson applicable to a recurring operation—writing tests, changing shared interfaces, invoking commands—regardless of project or agent engine" |
| Dave | "a kind of work that any agent may do in any project … It does not mean one task instance, because these lessons repeat across tasks" |
| Dario | "a kind of work that any agent meets in any project … The lesson names an action, not a repo file or an engine" |

*My reading:* three of them read "task" as one run (Fan Li, Laozi, Sun Tzu) and three as a kind of work (Linus, Dave, Dario). So their counts are not counting the same thing.

**What level F-0f2fa841 (planted break never shown to fail) is at.** Fan Li: task-level (one run). Sun Tzu: "a testing insight and agent-type". Linus: a testing lesson that does not "depend on Claude, Codex, or this repository". Dave: "Task type: testing". Dario: "Task support" (*quoted*).

**Whether the guard's own defects are requirement issues or project-level breakers.**

| Expert | *quoted* |
|---|---|
| Dave | F-3e11ce16, F-2116eae0, F-8392b4ce, F-bdea5631 among "Requirement issues of this project's product, the guard" (10) |
| Dario | "F-f09b058d, F-8392b4ce, F-cc665076, F-3e11ce16 and F-bdea5631 cite SPEC rounds, so they fit 'requirement issues'" |
| Sun Tzu | F-3e11ce16, F-2116eae0, F-969500fa among "The clearest breakers … none is a gap in a requirement document"; F-8392b4ce "project" |
| Fan Li | F-3e11ce16 "the repo's check did not know its own tool's exit contract" — listed as project-level |
| Laozi | F-3e11ce16 project-level, then: "If F-3e11ce16 and F-bdea5631 are in that set, my clean counter-examples drop to four" |

**How many of the 56 are at each level** (each expert's own labels; *quoted*; none of them measured against a second labeller).

| Expert | Count |
|---|---|
| Sun Tzu | 28 project / 22 agent-type / 6 task |
| Dario | 21 project / 19 agent-type / 16 task |
| Dave | 10 requirement · 23 agent or task type · 5 project (not requirement) · 2 technology · 16 two-level |
| Laozi | by file named in `Source:`: about 12 inside the repo / 6 third party / 38 "I don't know" |
| Linus | none: "I therefore cannot give an honest error count" |
| Fan Li | none |

**How a simple program scores** (each applied by hand; none run as a program; *quoted*).
- Sun Tzu: Source rule "gets **13 of 56 wrong** (43/56, 77%)".
- Dario: a similar Source rule is "wrong on about 13 of 56". *My reading:* the two lists of 13 are not the same. Sun Tzu calls F-0f2fa841, F-21e1586c, F-e69dfb66, F-485505f6, F-08cf4cc3, F-3b8bdcec and F-c055f734/F-e1161864 misfiled as project. Dario's ten include F-7f938bdf, F-749688a0, F-59498b2a and F-5c21dd69, which Sun Tzu does not list.
- Dave: a keyword rule gives 23 agree, 11 partial, "7 wrong", "15 unsorted"; and "I wrote both the rule and the labels".
- Laozi: a rule keyed on the file path "must abstain" on 38.
- Linus and Fan Li ran no rule.

**Which ids land where.** F-7f938bdf: Sun Tzu project ("nothing checks that a question's paths are inside the repo"); Dario agent-type ("opencode rejects paths outside the repo"); Dave two-level. F-1b6f6a0f: Sun Tzu task ("one command"); Dave main agent habit; Dario project ("the guard's location rule"). F-173e0190: Linus "matters to callers of that CLI, including callers using another engine"; Sun Tzu, Laozi and Dario project; Dave two-level (*quoted*).

**What the writer records and how much.**
- Laozi: "One new field is enough: the path, with `none` allowed. Not three fields." He then proposes two words on the `Source:` line.
- Fan Li: two header fields, made "a required header before the fix options are accepted".
- Sun Tzu: two lines, worked out from two counterfactual questions.
- Dave: two lines for each fix option, not for each insight.
- Dario: `Level:` plus two more fields, `Failed agent:` and `Cause owner:`.
- Linus: four items, with "Multiple applicable audiences remain possible."

(*quoted*)

**The two questions behind the level.** Sun Tzu and Dario both propose two yes/no questions. The questions differ and so do their outcomes (*quoted*):
- Sun Tzu: "(1) Would the same failure happen in a different task in this repo? No → task. (2) Would it happen in a different repo with the same agent kind? No → project; yes → agent-type."
- Dario: "(a) Would a different kind of agent in this repo hit it? (b) Would the same kind of agent in another project hit it?", giving yes/yes task, yes/no project, no/yes agent-type, no/no "one-off, file nowhere".

**Thresholds for the check.**
- Sun Tzu: "At least 16 of 20 agreeing".
- Laozi: "more than about six" disagreements.
- Fan Li: "100% of new insights".
- Dave: "agrees with a human about as well as two humans agree with each other … a comparison, not a threshold I made up".
- Dario: "I give no pass threshold; that is EJ's to set".
- Linus asks EJ for the limits.

(*quoted*)

**What to do with the 56 existing insights.**
- Sun Tzu: "do not move the 56 files … backfill one when it is loaded".
- Laozi: "should be left there".
- Fan Li asks EJ whether to backfill.
- Dave: a trial that moves "the testing lessons first … into one task-type file".

(*quoted*)

## What each added that the others did not

- **Linus.** A lesson has several possible audiences ("workers, callers, reviewers, or maintainers"). "The concrete repair and the transferable lesson can have different audiences." He keeps an unresolved cause unresolved (F-8ac06aae). He ran his own rule through requirement-check: it fails weak words, level and basis. He asks whether the labels stay advice or control delivery (*quoted*).
- **Fan Li.** A `Target-entity:` naming the component or learner (e.g. `repo:tools/export_skills.py`). He would make the field required before fix options are accepted, and he names the risk: "validation friction … risking failed runs" (*quoted*).
- **Sun Tzu.** Subject (code/testing) and scope (project/agent-type) are two separate axes that cross, so "you need both". He cites the existing `insight index` decision, where `Source` kinds did as well as guessed categories (`data/insight-categories.yaml`). He proposes a `Stops if:` line, a `level` column in the index, EJ's override in `insight-decisions.md`, and the index as "the filing cabinet, not a new folder tree" (*quoted*).
- **Laozi.** What decides the level is the path of the file the fix lands in. He adds a third-party group (mcode, git hooks, Codex sandbox, TypeScript). His cheapest next step is to grep the fix options, because they are "the likeliest place a path is already written down" (*quoted*). He asks whether other engines read any file outside their project: "If they read nothing outside the project, then 'agent-type level' is not a place at all". He also notes the census does not line up (56 sections vs 52 records + 1 review finding) (*quoted*).
- **Dave.**
  - A `Fires when:` line: the moment the lesson must be in front of the learner.
  - A "Technology, outside both levels" group (F-749688a0, F-5c21dd69).
  - Four testing lessons already live in this project's Claude memory folder, which "The engines that write tests in crossed-build-check do not read".
  - "Review finding 1" has no F-id and is missing from the insight index.
  - Seven 2026-10-15 sections have a bare Source word.
  - An analogy from immunology, labelled recall.
  - All 56 come from an agent-tooling project, "so the split may not hold in an application repo".

  (*quoted*)
- **Dario.** A fourth cell, "one-off, file nowhere". `Failed agent:` and `Cause owner:` as separate fields. A question: "Will a project-level insight whose fix is a code change still be read after the fix?" And "Same-writer bias": the agent that failed would be the one writing the level (*quoted*).

## What they need to know (merged, for EJ)

1. **What "project requirement issues" covers** (Linus, Sun Tzu, Laozi, Dave, Dario).
   - (a) Only gaps in written requirements (SPEC, HARNESS_REQUIREMENTS). The guard, tool and test defects then break the hypothesis: 5 to 28 sections, depending on the expert.
   - (b) Any defect in this repo's code, tools and tests. The hypothesis then nearly holds, but "project" comes to mean "anything in this repo".
   - (c) Defects in the guard (this project's product) count as requirement issues; defects in other repo tools and tests do not. This is Dave's split.
2. **What "task level" means** (Sun Tzu, Dave).
   - (a) One task or run instance. Its home is the run folder, or "nothing to file" (Fan Li, Laozi, Sun Tzu).
   - (b) A kind of work done in any project, such as writing a fail-first test, writing a spec or calling an engine (Linus, Dave, Dario).
   - (c) Both, as two separate levels. Sun Tzu: "that is a fourth level".
3. **One level per insight, or per lesson** (Sun Tzu, Dario, Laozi, Linus).
   - (a) One label per insight.
   - (b) A primary and a secondary label.
   - (c) One label per lesson or fix option, so a two-level insight carries two (Dave, Linus).
4. **Who fills the level** (Sun Tzu; Linus "EJ retains the decision"; Dario "Same-writer bias").
   - (a) The insight's writer, as a claim, with EJ's override in `insight-decisions.md`.
   - (b) EJ, as a decision, the way the fix is chosen.
5. **Where agent-type and task-type lessons live, and who reads them** (Fan Li, Dave, Laozi).
   - (a) A shared global directory, such as `~/.agents/`, or harness system prompts.
   - (b) Kept in this repo and linked out, the way the workflow-design skill is.
   - (c) They stay in this project, which Dave says "changes nothing outside this project". Laozi and Dave also ask a factual question: do opencode, Codex, agy and mcode read any shared file outside their project? Neither knows.
6. **Do the labels stay advice, or do they route lessons automatically** (Linus)?
   - (a) Advice: uncertain labels get reviewed.
   - (b) Automatic delivery: missed and irrelevant deliveries then need measuring.
7. **The existing 56** (Fan Li, Sun Tzu, Laozi, Dave).
   - (a) Backfill all 56 by manual review.
   - (b) Leave them in their run folders; label new insights only.
   - (c) Label an old one when it is next loaded (Sun Tzu).
   - (d) A trial that moves the testing lessons into one task-type file first (Dave).
8. **What counts as reliable** (Linus asks for limits).
   - (a) A number EJ sets (Sun Tzu proposes 16 of 20; Laozi about 6 disagreements; Fan Li 100%).
   - (b) A comparison: the program agrees with a human about as well as two humans agree with each other (Dave).
   - (c) Report the disagreement count by id, with no pass line (Dario).
9. **Does a project-level insight whose code fix has landed still need a level** (Dario)?
   - (a) Yes: it is still read by whoever edits that code.
   - (b) No: once the fix lands, it needs no filing.

**Factual checks the main agent can do without EJ** (raised by the experts; not EJ's choices):
- Laozi: do the fix options already name a path? His test is a grep over the 38 sections whose `Source:` names no file.
- Laozi: which file is the census, given 56 sections against 52 journal records plus 1 review finding.
- Dave: does the guard hook run in other projects?
- Dave: "Review finding 1" has no F-id, so the insight index misses it.

## Check

- **The workflow's check.** The harness reports all six as usable with check pass. Each `level-q/<expert>/check.txt` holds 5 FAIL lines, all "no answer file", one for each of the *other* five experts, and ends "FAIL: 1 answers, 5 failure(s)". None of those lines names the expert whose folder it is. The workflow counts only that expert's lines, and so do the progress-log notes (e.g. "linus check passed (no linus FAIL lines; other experts not in this folder)"). *quoted* from check.txt and `nodes/level-q.progress.md`.
- **Who wrote the check, and what it does not establish.** The check (`six_experts.py check`) was written by Claude. It shows that an answer file exists and has its sections. It does not establish that any expert applied its rules correctly, labelled any insight correctly, or counted correctly.
- **Engines** (from each status.json): Linus codex `gpt-6.1-sol`; Fan Li agy `gemini-3.8-flash-medium`; Sun Tzu dsh `deepseek-flash (dsh headless profile)`; Laozi opencode `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`; Dave claude `claude-opus-5-5`; Dario claude `claude-sonnet-5-5`. All exit 0, ok true, problem empty. No reruns. No fallback is recorded: Linus ran on Codex, not mcode, and Fan Li on agy, not Claude.
- **Shared engine** (*my reading*): Dave, Dario and this comparer all run on Claude, so these three are not independent of each other.
- **Laozi's answer file** starts with a stray line, "I'll read that brief first.", before its heading (*quoted*). It does not change the content.
- **My checks (the comparer's), measured:**
  - Every F-id cited in the six answers appears in `insights.md`. This shows only that each id exists; it does not show the id says what the expert claims.
  - `insights.md` has 56 sections. The first word of their `Source:` lines counts instruction 26, check 15, tool 13, config 2.
  - Sun Tzu's "19 check, 9 tool" does not match that first-word count. The difference may come from Source lines that name two kinds; *not measured*.
- **Not measured:** every level count and every program error count above (13/56, 7 wrong, 15 unsorted, 12/6/38). Each is one expert's labels applied by hand, and no second labeller has checked them. Dave and Dario say so themselves.
