# Apply the 10 optimization cuts to the method (surgery, not rewrite)

Read the three reviews in `runs/20261008-optimize/` — `claude-opus-5-5.md`, `minimax-m3.1-flash.md`,
`deepseek-v4-pro.md`. They agree on the same cuts. Apply them to `docs/WORKFLOW_DESIGN_METHOD.md` and
`.claude/skills/workflow-design/SKILL.md`.

## The rules for the surgery (all mandatory)

1. **Never delete history — archive it.** Create `docs/METHOD_CHANGELOG.md` and move there: the deleted-rules
   tombstones (the "Caps — deleted" story, the removed-fallback note), the "decision C was revisited" traversal
   story (keep only the 4-line asymmetric-compare rule in 3.6), the git-status bug narrative, and the inline
   "(Added … at EJ's request; n=0)" provenance tags. One line per archived item, with the date.

2. **Move reference detail to an appendix, not out of the repo.** Add a `## Appendix` section at the END of the
   method doc and move there: the "one word, one job" glossary (currently before §1), the §4 memory-kinds table, and
   the 3.7 concurrency "name the unit" table. The main flow keeps a one-line pointer.

3. **§3.8's executor operating contract** (timers, no-polling, pass-back, the 12 items) → replace with a short
   pointer: "how a node runs — executors, timers, pass-back, no polling — is in `docs/DISPATCHER_DESIGN.md`". First
   VERIFY that doc actually holds that content; if it does not, say so and keep the 12 items but compressed to one
   line each.

4. **Baseline**: 3.1 keeps the full definition; 3.6 shortens to "the baseline recorded in 3.1 still passes".

5. **Blueprint "not answered by silence"**: keep ONE copy, reference it from the others.

6. **§5 "three qualities"**: collapse to a three-line pointer list (predictability / debuggability / quality
   control), each pointing at the step that defines it.

7. **SKILL.md**: it is a second full copy that has drifted. Replace duplicated rules (the loop's five conditions,
   the tiny test, the blueprint rules) with links to the method's section. Keep the skill's own packaging — the
   frontmatter description, the trigger, and the eight-step summary — but make the detail a link, not a copy.

8. **Do NOT touch the core**: the nine steps, the "five things every node carries", the state file, the three
   qualities (as a pointer), the acceptance criteria. Every step stays; only duplicated *definitions* merge.

Print a line-by-line summary of what you moved, cut, and linked — and any place you had to stop (e.g. the
dispatcher doc not holding §3.8's content).
