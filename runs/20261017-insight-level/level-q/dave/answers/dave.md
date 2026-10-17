# Dave: which level does an insight belong to, and can a program sort it?

## Answer
The owner is mostly right, but not completely. In my sort of the 56 (I am the only rater), 33 fit their split: 10 are requirement issues of the guard, and 23 are agent-type or task-type lessons. But 5 are project-level without being requirement issues; the clearest is F-5182be9b/F-1d185ee3. Another 16 carry lessons at two levels at once. A program can sort them quickly but not reliably from today's `Source:` and `Root cause:` text. It becomes reliable only if each fix option records who must learn it and the moment the lesson must be in front of them.

## How I decided
1. **What would change my mind (my #1).**
   - **Question 1:** any insight whose lesson applies only inside this repo, and is not a gap in a requirement, breaks the hypothesis. If EJ labels the 56 without seeing my sort and puts every such case under "requirement" or "agent type", I am wrong.
   - **Question 2:** a program counts as reliable if it agrees with a human about as well as two humans agree with each other. That is the control (my #4): a comparison, not a threshold I made up.

2. **What the data already shows, and what it does not (my #5).**
   - `Source:` says where the fix goes. The journal's `engine` field says who failed. Neither says who learns.
   - The recorded name is not always the learner:
     - F-7f938bdf: the brief's own example.
     - F-a03fa5b3 and F-1b6f6a0f: the text names the guard, which only caught a slip by the main agent.
   - Seven sections from 2026-10-15 have a bare Source word with no text: F-1b6f6a0f, F-f09b058d, F-8712e9fc, F-08cf4cc3, F-f44538b2, F-cf7d58f7, F-3b8bdcec.
   - "Review finding 1" in `runs/20261017-round17-crossed/insight.md` has no F- id. It is missing from my insight index, which has 55 rows from insight.md files for 56 sections. A program that works by id would miss it.
   - The journal's 37 of 52 "none" records (taken from the brief; I did not check them) lean towards the main agent. But that field counts who failed, not who learns.

3. **What "task level" means (my reading).** It means a kind of work that any agent may do in any project: writing a fail-first test, writing a spec or criteria for another agent, calling an engine headless, changing a shared function. It does not mean one task instance, because these lessons repeat across tasks:
   - F-98c2c4c9 is "its first repeat" of F-15cf1278.
   - F-05a1b440 repeats its cause "a second time".
   - F-8243a18f and F-96578c5b failed "twice the same day".
   - F-4981093a happened "an hour after the rule against it".

   If "task" meant one instance, the hypothesis would fail at once, because these lessons outlive their task. The repeats also back the owner's reason for asking: filing in the run folder did not stop them. That is about 5 repeats over two days in one project; `EJ's rule` (my #10): "n=1 is a hint, not a law".

4. **The sort (my reading; one rater; every id from insights.md).**

   | Group | Count | Fits the hypothesis? | Insights |
   |---|---|---|---|
   | Requirement issues of this project's product, the guard | 10 | Yes (the owner's exception) | F-f09b058d, F-785afc27, F-15cf1278, F-98c2c4c9, F-d3132a7f, F-cc665076, F-2116eae0, F-8392b4ce, F-3e11ce16, F-bdea5631 |
   | Main agent's habits | 10 | Yes | F-1e90a8e1, F-1b6f6a0f, F-f44538b2, F-e82a6f58, F-4981093a, F-b696193d, F-8ac06aae, F-a03fa5b3, F-3caba088, F-c055f734 |
   | Task type: testing | 5 | Yes | F-0f2fa841, F-21e1586c, F-a2551f81, F-8243a18f, Review finding 1 |
   | Task type: specs and criteria | 4 | Yes | F-cf3f3a6e, F-4cbb2f4b, F-05a1b440, F-336edcb0 |
   | Task type: engine calls | 1 | Yes | F-08cf4cc3 |
   | Engine type | 3 | Yes | F-76013d09 (Codex sandbox); F-e69dfb66, F-485505f6 (mcode) |
   | Project level, not a requirement | 5 | **No** | F-5182be9b/F-1d185ee3, F-8712e9fc, F-d8221199, F-682702da, F-86553997 |
   | Technology, outside both levels | 2 | Only if "task" includes the tool | F-749688a0 (git hooks), F-5c21dd69 (TypeScript) |
   | Two levels in one insight | 16 | Partly | F-60cad515, F-cf7d58f7, F-3b8bdcec, F-2cc835e3, F-d1444d01, F-59498b2a, F-90389583, F-b7c8635f, F-c60edad6, F-969500fa, F-2cdebf3b, F-0a1f3ca1, F-d8a49e5a, F-7f938bdf, F-173e0190, F-84636a96 |

   - Eight of the 16 two-level insights have a project part: F-60cad515, F-2cc835e3, F-59498b2a, F-c60edad6, F-d8a49e5a, F-7f938bdf, F-173e0190, F-84636a96.
   - Clean support for the hypothesis: F-1e90a8e1 (the habit of piping a command whose exit gates the next step) and F-0f2fa841 (a planted break that was never shown to fail alone).
   - The clean break is F-5182be9b. Its lesson, "the order 'export, commit, then run the Python suite' is not written where an edit to the workflow-design skill happens", applies only in this repo. Any agent editing that skill here hits it, and it is not a requirement gap.

5. **How nature solves it (my #6; this is recall about immunology, not run data).** The body keeps two kinds of memory cells for one infection:
   - circulating cells that patrol everywhere;
   - tissue-resident cells that stay where the infection came in, because it is likely to come back there.

   The mechanism to borrow: file a lesson where the situation that triggers it comes back.
   - The trigger occurs only in this repo (editing the workflow-design skill, F-5182be9b): project level.
   - The trigger goes wherever the agent goes (piping a command whose exit gates the next step, F-1e90a8e1): agent type.
   - The trigger comes wherever the kind of work is done (planting a break, F-0f2fa841): task type.

6. **Does the analogy fit (my #7).**
   - Same: the place is chosen by where the trigger comes back, and both kinds of memory exist side by side for one infection, as in the 16 two-level insights.
   - Different: a memory cell recognises its target automatically. A written lesson is used only if something puts it in front of the agent at the trigger. The data shows this difference matters:
     - F-4981093a: a rule held in memory was broken an hour later, with "no check where the read happens".
     - F-5182be9b: the lesson sat "in a memory about the six-experts skill, not where the guard is edited".
   - So I keep "file it where the trigger comes back" and drop "filed means learned". The level decides which file holds the lesson. A check at the trigger, such as the guard, is what does the recognising.

7. **Where these lessons sit today (my #5; I checked the files).** The chosen fixes for F-a2551f81, F-21e1586c, F-3caba088 and Review finding 1 are four memory files: `assert-like-existing-tests.md`, `plant-replaces-a-line.md`, `print-keys-before-parsing.md` and `test-exemptions-on-reroute.md`. All four are code or testing lessons, which my sort puts at task level.
   - They live in `~/.claude/projects/-home-smoke01-dev-ancient-games/memory/`, a folder tied to this project and read by the main Claude agent. That it is not loaded in other projects is my recall.
   - The engines that write tests in crossed-build-check do not read it. Commit b6f361f records "opencode's 15 tests".
   - So the owner's most valued kind of lesson is filed today at project level, for one agent only.

8. **Can a program sort them (my #2).** A small test is cheaper than arguing about it. I applied this rule by hand to the `Source:` and `Root cause:` lines; I did not run it as a program. Rules are tried in order:
   - (a) names the guard, a SPEC round or `hooks.ts`: requirement;
   - (b) names a repo file (`four_experts.py`, `export_skills.py`, `journal.ts`, a spec file, the export test): project;
   - (c) names an engine: agent type;
   - (d) says "habit" or "the main agent's": agent type;
   - anything else: unsorted.

   Against my labels from step 4:

   | Result | Count | Insights |
   |---|---|---|
   | Agree | 23 | (the rest) |
   | Two-level insights given one of their two levels | 11 | (the rest of the two-level group) |
   | Wrong | 7 | see below |
   | Unsorted | 15 | see below |

   The 7 it gets wrong:
   - F-1b6f6a0f, F-a03fa5b3: they name the guard that caught a slip, so they land under requirement.
   - F-5182be9b: it says "where the guard is edited", so it lands under requirement, which hides the clearest break.
   - F-4cbb2f4b, F-05a1b440: they name a spec file, so they land under project; they are lessons about writing specs.
   - F-90389583: it says "the guard call's environment"; it is really a bun lesson plus a spec-writing lesson.
   - F-cf3f3a6e: "round-5 spec" lands under requirement; arguable.

   The 15 it leaves unsorted: F-08cf4cc3, F-cf7d58f7, F-3b8bdcec, F-2116eae0, F-e82a6f58, F-f44538b2, F-0f2fa841, F-8243a18f, F-21e1586c, F-336edcb0, F-59498b2a, F-749688a0, F-5c21dd69, F-d8a49e5a, Review finding 1.
   - Six of these are testing or criteria lessons written in the first person ("my test's planted input", "my criteria writing"). The owner's most valued kind is the kind this text sorts worst.
   - Even among the 23 that agree, no field tells agent type from task type. "My habit" in F-a2551f81 is a testing lesson that opencode needs too.

   How sure I am (my #10): I wrote both the rule and the labels. This shows the text is ambiguous; it does not show how a program would score against EJ.

9. **What would make it programmable.** My reading; a *proposed change to the R12.3 insight format*, not to the run pattern. For each fix option, the insight writer (who already writes the options, so there is still one author) adds two lines:
   - `Learns:` one of:
     - this project;
     - an agent type: main Claude, opencode, Codex, agy or mcode;
     - a named task type: testing, spec writing, engine calls, and so on.
   - `Fires when:` the moment the lesson must be in front of the learner, for example "before piping a command whose exit gates the next", or "before editing `.claude/skills/workflow-design`".

   The owner's choice of fix decides which level is used, and a two-level insight keeps two lessons. The program then reads a field instead of guessing. Its real job becomes checking:
   - flag a `Learns: task type` lesson whose applied fix sits only in this project's Claude memory;
   - flag any section without an id.

   The "where applied" line in `insight-decisions.md` is not a substitute. It records where a lesson was put, not where it belongs, so it would only repeat what step 7 found.

10. **Insights that changed the answer:**
   - `runs/20261016-four-experts-what-counts-as-change/insight.md#F-5182be9b`: the clean break; it turned my "yes" into "mostly".
   - `runs/20261016-four-experts-what-counts-as-change/insight.md#F-4981093a`: filing a lesson is not the same as learning it (step 6).
   - `runs/20261016-four-experts-what-counts-as-change/insight.md#F-98c2c4c9` and `runs/20261016-integrate-r11-r13/insight.md#F-05a1b440`: lessons repeat across tasks, so "task" means a kind of work (step 3).
   - `runs/20261016-six-experts/insight.md#F-7f938bdf` and `runs/20261016-time-monitor/insight.md#F-a03fa5b3`: the name recorded is who failed or who caught it, not who learns (steps 2 and 8).
   - `runs/20261016-four-experts-what-counts-as-change/insight.md#F-0f2fa841`: the testing lessons are the ones the text cannot sort (step 8).

   No category was named in my brief; I read all four Source kinds, because the question covers all 56.

## What I need to know
1. **Do "project requirement issues" include defects in this project's own tools and tests?** These are four_experts.py, export_skills.py, journal.ts and the export test.
   - If yes, the clean breaks shrink to two conventions about how work is done in this repo: F-5182be9b/F-1d185ee3 and F-8712e9fc.
   - If no, F-682702da, F-86553997, F-d8221199 and the project parts of 8 two-level insights also break the hypothesis.
2. **Does EJ mean "task" as a kind of work (my reading), or as one task instance?** If one instance, the hypothesis fails much more broadly, because these lessons repeat (step 3).
3. **Where should agent-type and task-type lessons live, and does any shared file get read by opencode, Codex, agy and mcode?** I don't know the second part. If these lessons stay in this project's Claude memory folder, filing them by level changes nothing outside this project.
4. **Does the guard's hook run in other projects?** I don't know. If it does, fixing a guard requirement is also an agent-type change, and in this repo those two levels overlap.

## Costs and risks
- **Writing the two new lines (my #10).** They cost the insight writer two lines per fix option, and `Learns:` is still a judgment. The guess moves to the writer; it does not go away. The owner sees it when choosing the fix.
- **Lessons leaving the repo (my #5).** Agent-type and task-type files outside the repo drop out of its git history and review. One way round it is to keep them in the repo and link them out, as the workflow-design skill already is (CLAUDE.md); the cost is keeping the links working.
- **More noise (my #8).** A project-only lesson promoted to agent type follows the agent into every project and becomes the noise the owner wants to cut. Promote one kind at a time.
- **More to read.** Splitting the 16 two-level insights into two lessons each adds entries.
- **My sort is shaky (my #10).** One rater: the counts in any group could move by several.
- **One unusual project (my #10).** All 56 come from a project whose product is agent tooling, so the split may not hold in an application repo.
- **The analogy is recall (my #6, #7).** The decision rests on F-5182be9b and F-4981093a, not on immunology.

## How we would know I was right
- **A test of both questions (my #3, #4).** The prediction is written here, before any result.
  - The metric is agreement on each insight's level between:
    - (a) EJ and a second labeller on a different engine, each blind to the other and to my sort;
    - (b) the step-8 rule, run as a program, and each of them.
  - What I expect:
    - The program agrees with each human less than the humans agree with each other.
    - Its misses fall mostly on the testing and spec lessons and on the two-level ones.
    - Both humans put F-5182be9b/F-1d185ee3 and F-8712e9fc outside both "requirement" and "agent type".
  - The test stops when the time EJ sets runs out.
  - If the humans put those under requirement or agent type, my answer to question 1 becomes "yes" and I was wrong.
- **Then a small trial (my #8, #9).**
  - Move the testing lessons first (F-0f2fa841, F-21e1586c, F-a2551f81, F-8243a18f, Review finding 1) into one task-type file. Both the main agent and the test-writing engine in crossed-build-check must read it.
  - The control is today's arrangement, where they live only in this project's Claude memory.
  - Compare how often fail-first and planted-break failures repeat in the journal before and after the move. A result of no change gets reported too.
