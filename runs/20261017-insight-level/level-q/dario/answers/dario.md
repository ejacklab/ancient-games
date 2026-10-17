# Answer — at which level does an insight belong?

## Answer
EJ is partly right. Going by my own labels, 35 of the 56 insights fit "agent-type or task level" (19 agent-type, 16 task), but 21 are project-level. Most of those 21 are bugs in this repo's own guard, runner or export code, and whether they count as "project requirement issues" is EJ's call. A program can't sort the insights reliably from today's fields, so the writer should record a `Level:` line, derived from two yes/no questions, and EJ should check it.

## How I decided
1. **Reading of the terms.**
   - *Task level* means a kind of work that any agent meets in any project, such as writing a spec for a coder, writing a test with a planted failure, or changing a shared function. The lesson names an action, not a repo file or an engine.
   - *Project level* means the root cause sits in this repo's code, tools or conventions.
   - *Agent-type level* means a fact about a kind of agent (an engine's sandbox, its connection, or the main agent's habit).
   - The labels below are my reading of `insights.md`, not a measurement. I wrote them, so they are not independent evidence.
2. **Tally by my reading (56 sections):**
   - 21 project: 18 of them have Source check or tool, 3 have instruction.
   - 19 agent-type: 9 about engines, 10 main-agent habits.
   - 16 task.
3. **Agent-type support.**
   - Codex sandbox: F-76013d09, F-0a1f3ca1.
   - mcode stalls on brief-sized input: F-e69dfb66, F-485505f6.
   - opencode rejects paths outside the repo: F-7f938bdf.
   - Main-agent habits: F-1e90a8e1 (a pipe hid a failed merge), F-a03fa5b3 (typed an epoch from memory).
4. **Task support.**
   - Test with a planted failure: F-0f2fa841, F-21e1586c.
   - Writing test expectations: F-a2551f81.
   - Spec lines that mix instructions and values: F-4cbb2f4b, F-05a1b440, F-b7c8635f.
   - Rerouting calls into an existing path: "Review finding 1".
5. **What breaks "no other project level".**
   - F-5182be9b/F-1d185ee3: the order "export, commit, then run the suite" is written only in a memory note. That is a repo procedure, not a requirement, not an agent habit, and not general to the task.
   - F-8712e9fc: the export test can't tell this session's changes from another session's, in a shared working tree.
   - F-1b6f6a0f: the guard's location rule.
   - F-d8a49e5a: a project skill's own rule.
   - Another 15 or so are false failures or gaps in the guard's rounds. F-f09b058d, F-8392b4ce, F-cc665076, F-3e11ce16 and F-bdea5631 cite SPEC rounds, so they fit "requirement issues". F-682702da, F-173e0190 and F-60cad515 are plain tool bugs.
   - If "project requirement issues" means any defect in project code or spec, the hypothesis holds. If it means only written-requirement gaps, it breaks on the non-requirement ones above. The data can't settle that.
6. **Task versus agent-type can't be separated here.** The brief's journal counts say 37 of 52 failures are the main agent's own. Whether another engine would repeat F-a2551f81 or F-4cbb2f4b, I don't know. The `engine` field also names who failed, not who should learn (F-7f938bdf).
7. **Can a program sort them?**
   - *Rule tried:* Source check or tool means project; instruction or config means agent-type or task.
     - By my labels it is wrong on about 13 of 56.
     - Ten check/tool insights are not project-level: F-3b8bdcec, F-08cf4cc3, F-0f2fa841, F-21e1586c, F-7f938bdf, F-e69dfb66, F-485505f6, F-749688a0, F-59498b2a, F-5c21dd69.
     - Three instruction insights are project-level: F-1b6f6a0f, F-5182be9b/F-1d185ee3, F-d8a49e5a.
     - It can't split agent-type from task at all.
     - Nine Source lines name two causes (for example F-0a1f3ca1: config plus instruction; F-86553997: tool plus check).
   - *Keyword rule:* an engine name means agent-type.
     - It catches the Codex, mcode and opencode ones.
     - It misses F-84636a96, which says only "an engine".
     - "my habit" and "the main agent's" mark who wrote the insight, not the level; "habit" appears in 7 lines.
8. **What the insight must record.** The writer answers two questions, and a program reads the answers:
   - (a) Would a different kind of agent in this repo hit it?
   - (b) Would the same kind of agent in another project hit it?

   | (a) | (b) | Level |
   |---|---|---|
   | yes | yes | task |
   | yes | no | project |
   | no | yes | agent-type, with the name |
   | no | no | one-off, file nowhere |

   Add `Failed agent:` and `Cause owner:` as separate fields, because F-7f938bdf has opencode failing from the main agent's brief.

## What I need to know
- Does "project requirement issues" cover any defect in the guard, runner or export code, or only gaps in written requirements? If the former, the hypothesis holds. If the latter, it breaks on about 9 insights.
- Will a project-level insight whose fix is a code change still be read after the fix? I did not see whether those fixes landed (*recall*: the owner's choices go in `insight-decisions.md`, which I did not read). If not, they need no level.
- Do you want one level per insight, or a primary and a secondary? 9 Source lines name two causes.
- Do any causes repeat across runs? The repeats I could see (F-98c2c4c9, F-05a1b440, F-2cdebf3b, F-0a1f3ca1, F-485505f6) are all inside one run. I don't know whether any filing level would have stopped a later-run repeat.

## Costs and risks
- **Same-writer bias.** The agent that failed would write the `Level:` line, so its label is not independent. My own labels have the same problem.
- **Counterfactual answers.** Questions (a) and (b) ask the writer to guess about other agents or projects, and nothing verifies the guess.
- **Overloaded bucket.** If most insights land under "main Claude agent" (71% of failures, from the brief's counts), that file grows large and noisy. That works against EJ's aim of reducing noise.
- **Filing is not learning.** F-4981093a shows a rule that existed in memory was broken an hour later. A level says where to file, not that the next agent reads it.
- **Two-cause insights.** A single level hides the second cause.
- **Moving files.** Insights are now cited by `runs/<run>/insight.md` path. I don't know what cites them, but the F-ids are stable and the paths are not.

## How we would know I was right
- EJ labels all 56 blind, or a random sample, with project/task/agent-type. Compare against the writer's `Level:` field, against my labels above, and against a program that applies the two-question table. Report the count of disagreements and list them by id. I give no pass threshold; that is EJ's to set.
- After filing by level, watch whether the same root cause shows up again in a later run. In the data, "Review finding 1" and F-a2551f81 are the kind of insight a task-level file should stop. If the same cause repeats while its insight sits at the chosen level, that level did not help.
