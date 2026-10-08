# Should the skills link to the WHOLE Ancient Games, not just the workflow-design method?

The Ancient Games is ONE framework (read `CLAUDE.md`): the workflow-design method (designs a workflow), the referee
(`ancient_games/`: Gate → Guard → Corroborate → Filter → Prove — clears the plan), and the shared knowledge
(`docs/`, templates). One system.

The skills are the packaged, trigger-based instructions. Today:
- `workflow-design` (`.claude/skills/workflow-design/`, symlinked into `~/.agents/skills` and `~/.claude/skills`)
  links to the METHOD (`references/method.md`).
- `requirement-check` and `meaningful-names` are global skills in `~/skills/` (symlinked into both roots).
- `coding-discipline`, `agent-experience`, `cordis-*` are harness skills.

The author's claim, to check: **the skills should link to the WHOLE Ancient Games framework, not only the
workflow-design method.**

Read the actual files (the skills, `CLAUDE.md`, the method, the referee). Do not reason from memory. Answer:

1. **Divergence** — is there anything in any skill that contradicts or drifts from the Ancient Games (a rule stated
   differently, a concept renamed, a stale reference)? Cite file:line for each.
2. **The linking claim** — is the author right that the skills should link to the whole framework (method + referee +
   knowledge)? Or is `workflow-design` correctly the only one tied to it, with the others standalone?
3. **The right structure** — how should a skill point at a framework's parts? (e.g. every skill opens with "this is
   part of the Ancient Games: method / referee / knowledge", or only workflow-design does.)

Blind, concise. Cite paths for any divergence.
