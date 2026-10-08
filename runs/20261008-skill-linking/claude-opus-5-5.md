I could read `workflow-design`, `requirement-check`, `meaningful-names` and the Ancient Games docs. I could not read `coding-discipline`, `agent-experience` or `cordis-*`: their files are outside the folder this session can read, and none of them could be loaded as a skill. So there is no verdict on those three.

## 1. Divergence

**Inside `workflow-design` (`.claude/skills/workflow-design/SKILL.md`)**
- **`SKILL.md:9`** says "the five templates", but `docs/workflow-templates/` holds nine (blueprint, explorer-file, node-brief, prompt-file, readiness, research-file, result-file, state, workflow-design). That count is out of date.
- **The engine count differs from file to file:**
  - `CLAUDE.md` describes `EXECUTOR_KINDS.md` as "the three engines (Claude subagent, Codex, Antigravity `agy`)".
  - `docs/EXECUTOR_KINDS.md:11` says "these three", while its heading at `:13` says "The four kinds" (qwen was added).
  - A fifth engine, opencode, is used in routing at `:163` and `:248`.
  - `SKILL.md:39` names only "Codex or `agy`", yet `SKILL.md:94` gives opencode priority.

  The skill matches `EXECUTOR_KINDS.md`. It is `CLAUDE.md` and `EXECUTOR_KINDS.md:11` that are out of date.
- **`docs/WORKFLOW_DESIGN_DIAGRAM.md:213`** points at `SKILL.md` "line 123 / 127 / 132". The skill is now 129 lines long (shortened in commit 97c171f), so those pointers are broken.

**The eight-question checklist exists in four copies, and they already differ**
- The four copies:
  - `docs/research/20261005-requirement-statements/FINDINGS.md:85-109` (§2, which `CLAUDE.md` names as the source)
  - `CLAUDE.md`'s "The eight, short"
  - the `requirement-check` skill
  - a summary at `SKILL.md:98-102`
- **What to do on a fail:** `FINDINGS.md:87` says "Any 'no' stops you". `CLAUDE.md` and `requirement-check` say report pass/fail, then ask the person. These are different actions.
- **Source:** in `FINDINGS.md:90`, "mine" means the agent's own inference, which must be labelled or left out. In `requirement-check` and `CLAUDE.md`, "'Mine' is a valid answer" means the person's own rule.
- **Weak words:** `FINDINGS.md:100` lists *if possible, etc.* but not *logical*. `requirement-check` adds *logical, reasonable* and drops *if possible, etc.*
- **Level:** `FINDINGS.md:103-104` also asks "*what* must be true, or *how*?". `requirement-check` drops that question and adds "a method does not earn MUST" instead, which does match the checked RFC 2119 §6 quote at `FINDINGS.md:321-332`.

**No drift found**
- `meaningful-names`: its rename table matches the code (`dispatch.py:69,113,310`, `readiness.py:83`) and the method's Appendix A (`WORKFLOW_DESIGN_METHOD.md:468-477`).
- The "four failures / three failures" figures (`SKILL.md:100-101`) match `FINDINGS.md:380-406`.
- The "five conditions" in method 3.5 and 3.7 and the three-part stop in 3.6 all check out (`METHOD.md:255, 341-347, 300-304`).

## 2. The linking claim

**Mostly not right.** The docs themselves say why. `WORKFLOW_DESIGN_DIAGRAM.md:157-158`: "There is no code path between them … the skill never names its five algorithms." Lines `:171-176` add that the referee works while a task runs, and the method works earlier, at design time. The method takes names and one number from the referee code (`:160-169`), not its stages.

So:
- `workflow-design` is already tied to the method and the knowledge files: the method, task types, executor kinds and templates are all symlinked from `docs/`. It does not mention the referee. The only gap is that it never says where the referee comes in later. `CLAUDE.md` says the referee's findings feed back into the method, but that hand-off isn't written down anywhere I can point to.
- `requirement-check` and `meaningful-names` are general standards (RFC 2119, *Clean Code*), installed for every project. They already carry a one-line origin pointing back here. Opening them with "part of the Ancient Games: method / referee / knowledge" would pull this project's context into unrelated projects without helping either skill do its job.

What actually goes wrong today is not missing links. It is **copies**: the checklist exists in four places and has drifted in four ways.

## 3. The right structure

- **Links run from the framework to the skills, not from every skill to the framework.** One entry point maps the parts: `CLAUDE.md`, or `workflow-design`'s "Related skills" section. Standalone skills keep only their one-line origin.
- **One copy per rule.** `SKILL.md:98-102` and `CLAUDE.md` should point to `requirement-check` instead of restating the checklist. Then one copy has to be named the owner: `FINDINGS.md` §2 or the skill. That is a decision for EJ, because the two disagree on stop versus ask.
- **`workflow-design` gets one line about the referee** only once there is a real hand-off ("a finished plan is cleared by the referee's Prove stage") with a source. Until then, the diagram's "no code path" is the accurate statement.

**One question for the author:** what does "link" mean here — a symlink to a shared file, a pointer line, or a common opening paragraph? The answer decides which of these fixes applies.
