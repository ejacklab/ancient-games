# 范蠡 (Fan Li) — at which level an insight belongs

## Answer
EJ is incorrect that every insight outside project requirement issues is only task-level or agent-type level: the data shows genuine project-level insights rooted in repository tooling and shared test harnesses (broken by F-682702da, F-8712e9fc, and F-86553997). A program cannot sort existing insights quickly and reliably from current fields, and can only do so if future insights explicitly record a standardized target level enum at filing time.

## How I decided
1. Applying my #14, I separate what belongs inside the borders from what belongs outside the borders:
   > 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 (`quoted`)
   > "Inside the four borders, the people's affairs: I am not as good as 種. Outside the four borders, dealing with enemy states, matters decided on the spot: 種 is not as good as I."

   In my reading, "inside the borders" corresponds to the project level—the repository's internal tools, common scripts, data structures, and shared test harnesses that remain constant regardless of which external engine runs. "Outside the borders" corresponds to the agent-type level—the engines (Codex, opencode, Claude, mcode) and their cross-project characteristics, sandboxes, and behavioral habits that follow them across repositories.
2. In my reading, "task level" means a failure whose cause, assertion, or fix is confined strictly to a single run's transient setup, planted test, or ephemeral criteria, without outliving the task or applying to other runs. The data supports the existence of task-level insights with F-336edcb0 ("criterion C3 not met: it asked for an event after the task") and F-0f2fa841 ("the failing-export test planted its break where the exporter never reaches"). It also supports agent-type insights with F-76013d09 ("the guard's pipe tests failed inside the Codex sandbox only") and F-e69dfb66 ("criterion C4 not met: mcode gave Linus no answer on a brief-sized input"), as well as project requirement issues with F-cf3f3a6e ("the guard suite was red during the parallel build", from an incomplete spec).
3. Applying my #2, affairs cannot be collapsed into only two domains:
   > 「夫國家之事，有持盈，有定傾，有節事。」/「持盈者與天，定傾者與人，節事者與地。」 (`quoted`)
   > "In the affairs of a state there is keeping the full, steadying the tilting, and regulating affairs." / "Keeping the full goes with Heaven; steadying the tilting goes with people; regulating affairs goes with Earth."

   Earth (節事者與地) governs the material ground and storehouses—the repository code, tools, and build scripts. The data breaks EJ's hypothesis because there are critical project-level insights that are not requirement issues:
   - F-682702da: `tools/export_skills.py` failed because it treated bundled skills as a single file, omitting reference files. This is a project tool defect affecting any agent running skill exports in this repo.
   - F-8712e9fc: the full Python suite failed because a shared working tree allowed an export test to confuse uncommitted session changes with clean state. This is a project test harness defect.
   - F-86553997: `journal.ts` duplicated writable record definitions across two distinct types (`JournalRecord` union and `appendRecord`), forcing duplicate edits. This is project-level codebase architecture.
   - F-3e11ce16: the guard hook logged its own exit code as a command error because the repo's check did not know its own tool's exit contract.
4. Applying my #18, one must verify that the defensive preparations exist before committing to battle:
   > 「審備則可以戰乎？」王曰：「巧。」 (`quoted`)
   > "If the preparations are examined, can we then fight?" The king: "Skilful."

   A program cannot sort the 56 insights into levels today because the preparation in the records is insufficient. `Source:` names only the repair mechanism (instruction, check, tool, config), not the scope of learning; `Root cause:` is unstructured prose; and the journal's `engine` field logs only who executed the step, not who should learn from it (for example, in F-7f938bdf the engine was logged as opencode, but the failure was the main agent sending a path outside the repo).
5. Applying my #3, one cannot force an outcome before the required structure exists:
   > 「時不至，不可彊生；事不究，不可彊成。」 (`quoted`)
   > "When the time has not come, growth cannot be forced; when the matter has not run its course, completion cannot be forced."

   To make automated sorting fast and reliable, the insight recording template (`runs/<run>/insight.md`) must record an explicit, machine-readable field at filing time: `Target-level:` with an enumerated value (`project`, `agent-type`, `task`), accompanied by `Target-entity:` naming the specific learner or component (e.g. `repo:tools/export_skills.py` or `agent:claude-code`).
6. *Proposed change to the pattern*: Update the R12.3 insight requirement in `docs/HARNESS_REQUIREMENTS.md` so that every new insight must record `Target-level: project | agent-type | task` as a required header before the fix options are accepted. Once recorded as structured metadata, a deterministic script can ingest and route insights to their target destinations without LLM inference or error-prone prose heuristics.

## What I need to know
- Whether EJ wants agent-type insights stored in a shared global directory outside this repo (such as `~/.agents/` or harness system prompts) or maintained locally within this repo's agent definitions.
- If past insights must be backfilled into the new structure or if the programmatic routing applies only to future runs; if backfilling is required, whether EJ wants the 56 existing entries classified by manual review or left archived in their respective run directories.

## Costs and risks
- Under my #14, requiring the filer to designate `Target-level` forces a decision at the boundary between internal and external concerns; if an agent mistakes the tool that failed for the actor who caused it (as occurred in F-7f938bdf), it risks misrouting an insight.
- Under my #3, refusing to build a speculative prose-matching classifier now leaves existing historical insights unfiled in their run folders until a structured schema is enforced and historical records are labeled.
- Under my #18, adding a mandatory structured field to the insight contract introduces validation friction into the harness, risking failed runs if an agent writes an insight without the new enum.

## How we would know I was right
Update the insight template to require `Target-level: [project | agent-type | task]` and run a validation script on newly filed insights. If 100% of new insights are classified into project, agent-type, or task destinations without manual disambiguation, and recurring tool failures like F-682702da cease to recur when different agents touch repo tools, the decision is proven.
