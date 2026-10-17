# Report — at which level does an insight belong? (six experts)

**Your hypothesis: partly right, not as stated.** All six say some insights are project level without being requirement
issues (quoted, each answer's first line). Whether that holds depends on what "project requirement issues" covers — a
question only you can settle.

- **Where all six agree (quoted, compare.md):**
  - F-682702da (the skill export skipped a reference file; no test checked it) is project level — all six cite it.
  - Neither the failing engine nor `Source:` says who should learn a lesson (all cite F-7f938bdf).
  - No program can sort today's insights reliably; the writer should record the level when filing, so a program reads
    a field instead of guessing.
- **Their own counts differ** (each expert's labels, by hand, not measured): Sun Tzu 28 project / 22 agent / 6 task;
  Dario 21 / 19 / 16; Dave 5 project-only, 16 two-level.
- **The main split:** "task level" means one run (Fan Li, Laozi, Sun Tzu) or a kind of work in any project (Linus,
  Dave, Dario).
- **Notable dissent:** Laozi — the level is decided by the path of the file the fix lands in; Sun Tzu — subject (code,
  testing) and level are two separate axes; Dave — "technology" lessons (git hooks, TypeScript) are a third group.

Data: `insights.md`, extracted by the main agent's own script (`extract.py`) — so the experts worked from my extraction,
not independent of it. The `six_experts.py check` passes say each answer cites its list correctly, not that its sort
is right.

Open for EJ: the nine questions at the end of `level-q/compare.md`; the two that change the most are what
"project requirement issues" covers and what "task level" means.
