# Challenge — harness health in the readiness step

## The request (EJ, 2026-10-15, quoted)

> "design and execute a workflow that enhance the readiness step to also validate a harness health conditions, if not
> good enough can we provide some help, get the 4 experts to plan and design these."

Earlier in the same session: *"I am thinking we can extend that review to more, so when we start design we can make
sure the harness 'health'"*, with a pasted ten-requirement list (outside source, author unknown) — copied in
`harness-ten.md`.

## Method 3.0 — understand the challenge

**Objective.** When a workflow design starts, the readiness step (method 3.1, `scripts/readiness.py`) also reports
whether the agent harness is in good health against the ten requirements, and where it is not, says what would help.

**In scope.**
- The readiness step's script layer in `.claude/skills/workflow-design/scripts/` and its tests `tests/test_readiness.py`.
- The `dsh` and `opencode` gap (installed, have dispatcher adapters, not probed).
- "Help" when a condition is not good enough — its form is an open spot (U2).
- The method text that tells the designer what to do with the result (method 3.1), if the experts' design needs it.

**Out of scope.**
- Changing any harness configuration on this machine (`~/.claude/settings.json`, `~/.codex/config.toml`, …).
- The referee code (`ancient_games/`), `SPEC.md`, `DECISIONS.md`.
- Running canaries (spends quota; separate go-ahead).
- The skills bundle export (`tools/export_skills.py`) — regenerated only if EJ asks.

**Six whys** (stopped at the answer that no longer changes the design):
1. Why health? Readiness proves tools exist; it says nothing on whether the harness around them is safe and
   verifiable, and the design rests on that (e.g. a build node with no sandbox, or a single engine kind so no
   different-kind reviewer).
2. Why at design start? The design is where a weak harness can still be compensated (higher Guard stakes, a script
   check instead of an agent reviewer); after dispatch it is too late.
3. Why help? A bare FAIL line sends the person to research the fix; the fix is usually one known setting.
4. Why the experts? EJ asked; the shape of "good enough" and of help are design choices with no default here.

**Provisional category.** Code generation on an existing script, with code review — a feature to a tool
(`docs/TASK_TYPES.md`). Relabelled per piece after the design.

**Tiny?** No: ten requirements × several harnesses, an open form of "help", and a checked build.
