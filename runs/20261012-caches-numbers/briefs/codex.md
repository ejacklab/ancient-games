# Your slice: the SEZA project as a use case, by agent type

Look at `/home/smoke01/dev/seza`, read-only. Several kinds of agent work in it (check `AGENTS.md`, `CLAUDE.md`,
`orchestration.mdc`, `docs/` and `runs/`): Claude Code, Codex, agy and others.

1. **What each agent type loads at session start in SEZA.** Measure the bytes, and the tokens at 4 characters per
   token (labelled as an estimate), of the instruction and memory files each one reads. Include Claude Code's
   memory folders under `~/.claude/projects/-home-smoke01-dev-seza*/memory/`, and `AGENTS.md` for Codex.
2. **SEZA's memory stores:** `backtest/project_memory/`, `factstore/`, `seza-factstore/`, `knowledge/` and
   `.ctxgraph/`. For each: the entry count, the total bytes and the median entry size. Also whether anything queries
   `.ctxgraph`.
3. **Two or three concrete use cases from SEZA's history** (its `runs/` and docs) where finding a memory entry was
   slow, missed, or cost many tokens; or evidence that it never was. Quote file:line.
4. **For each agent type:** given its context window (cite official docs, or GAP) and its start-of-session load, how
   much room is left, and at what memory size an index read at start would stop fitting comfortably. Give the
   arithmetic, and label it as your arithmetic.

Give the command and its output for every measurement.
