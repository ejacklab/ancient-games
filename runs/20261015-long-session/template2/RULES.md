# Rules for this session — they apply to every step

1. **Failures.** A failure is anything that went wrong while you worked, whoever caused it: a test run that failed, a
   command or tool call that errored, an engine result that is missing or empty (exit 0 alone is not success), work you
   had to undo or redo. Your own mistakes count.
2. **Failure log.** Log every failure when it happens, with a reason and evidence:
   `bun $GUARD/src/cli.ts fail --check <what> --input <what> --expected <what> --actual <what> --reason <why> --evidence <path> --found-by agent --engine <engine> --harness claude-code --session none`
   (the evidence path must exist — save what you saw to a file first).
3. **Insight.** If the session had any failure, before you finish write an insight to `.harness-guard/insights/<name>.md`.
   For each failure id (`bun $GUARD/src/cli.ts insight` lists them): a heading `## <failure id>`, then `Whys:` with 3 to 6
   numbered whys, `Source:` (instruction, check, tool or config), `Root cause:`, and `Options:` with 2 or 3 numbered
   fixes, each starting `[rule]`, `[check]`, `[tool]` or `[config-advice]` and containing `evidence:`. Propose only.
4. **Raise it.** Name the insight file in REPORT.md and in your final message.
5. **Known traps.** Always run `codex exec` with `</dev/null`. Never start two `opencode run` at once.
