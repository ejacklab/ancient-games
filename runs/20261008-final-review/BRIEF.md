# Review the current state of the Ancient Games repo for consistency

A day of changes just landed: the method was slimmed (history moved to `docs/METHOD_CHANGELOG.md`, reference detail to a
`## Appendix`), the eight-question checklist was collapsed to one copy (the `requirement-check` skill), stale refs were
fixed (engine count, template count, a dead `workflow-authoring` link, line pointers), and a portable `skills/` bundle
was created (self-contained, symlinks dereferenced).

Review the CURRENT state for anything still wrong, stale, or inconsistent. Check specifically:

1. **`skills/` bundle** — is it self-contained? Do `skills/workflow-design/references/*` resolve (no dangling paths)?
   Are the scripts and templates all present? Does the README's install instructions hold?
2. **Stale references** — any remaining line-number pointers, hard-coded counts, or dead links across `docs/`,
   `CLAUDE.md`, `.claude/skills/workflow-design/SKILL.md`?
3. **The checklist** — is it truly one copy now? Do `CLAUDE.md` and `SKILL.md` point at `requirement-check` without
   restating the definitions?
4. **The method doc** — does the main flow + changelog + appendix read coherently after the cuts? Any dangling
   reference to something that was moved?
5. **Cross-file drift** — does anything in `CLAUDE.md`, the skill, or the docs still disagree with the others?

Report a list of findings with file:line, ordered by importance. If it's clean, say so and name the one thing you'd
still check. Read the actual files — do not reason from memory. Blind, concise.
