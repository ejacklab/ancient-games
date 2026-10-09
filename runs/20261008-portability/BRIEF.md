# Plan: make the skills/ bundle truly portable

`skills/` is meant to be a drop-in bundle: another project copies a skill's folder into its own
`~/.claude/skills/` or `~/.agents/skills/` and it works. It currently is NOT portable, for these reasons (already
diagnosed):

1. **The scripts assume this repo's layout.** `skills/workflow-design/scripts/design_gate.py` finds `TASK_TYPES.md`
   via a `repo_root()` that walks up looking for a repo marker, then reads `docs/TASK_TYPES.md`. In another project
   there is no `docs/TASK_TYPES.md` — the file is at `skills/workflow-design/references/task-types.md`.
2. **The scripts read several repo files by path**: `docs/TASK_TYPES.md`, `docs/EXECUTOR_KINDS.md`,
   `docs/workflow-templates/*`, `docs/TASK_TYPES_LEDGER.md`, `docs/DISPATCHER_DESIGN.md`.
3. **The skill text references repo paths** — `.claude/skills/workflow-design/scripts/…`, `docs/…`, `code_graph/…` —
   which will not exist in another project.
4. **The scripts depend on each other** (dispatch imports engines, validate_result, etc.) — that part is fine since
   they sit in one folder.

Read the actual files first (`skills/workflow-design/scripts/*.py`, `skills/workflow-design/SKILL.md`,
`skills/workflow-design/references/*`). Then produce a **PLAN** (do not implement) that answers:

A. **Should the scripts ship in the bundle at all?** Or is the bundle meant to be "the instructions + references +
   templates" only, with the scripts staying in the Ancient Games repo (which already has them, live)? Give a
   recommendation with a reason.
B. If scripts DO ship: **how do they find their resources** in a new project? (e.g. resolve paths relative to the
   script's own folder / the skill folder, a config file, an env var, a `--root` flag already present?) Name the
   concrete change per script.
C. **How to fix the text paths** — which references in SKILL.md / references/*.md / README should become
   skill-relative, and which should stay pointing at the Ancient Games repo (because they name a repo-specific
   concept)?
D. **How to keep one copy** — the plan must not re-introduce a second divergent copy of TASK_TYPES.md etc. State
   where the single source of truth lives and how the bundle gets it (generated export? manual sync? symlink at
   install time?).

Deliver: a numbered plan, ordered, each step with the file(s) it touches and the one-line change. Flag any step you
cannot decide without the author. Blind, concise.
