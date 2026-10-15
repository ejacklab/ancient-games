# Rules for this session — they apply to every step

1. **Results.** After every engine call (e.g. `codex exec`), check the result yourself: a missing or empty output, a
   non-zero exit, or an error text is a failure — exit 0 alone is not success.
2. **Failure log.** Log every failure when it happens, with a reason and evidence:
   `bun $GUARD/src/cli.ts fail --check <what> --input <what> --expected <what> --actual <what> --reason <why> --evidence <path> --found-by agent --engine <engine> --harness claude-code --session none`
   (the evidence path must exist — save what you saw to a file first).
3. **Insight.** If the session had any failure, before you finish write an insight to `.harness-guard/insights/<name>.md`.
   For each failure id (`bun $GUARD/src/cli.ts insight` lists them): a heading `## <failure id>`, then `Whys:` with 3 to 6
   numbered whys, `Source:` (instruction, check, tool or config), `Root cause:`, and `Options:` with 2 or 3 numbered
   fixes, each starting `[rule]`, `[check]`, `[tool]` or `[config-advice]` and containing `evidence:`. Propose only.
4. **Raise it.** Name the insight file in REPORT.md and in your final message.
5. **Known traps.** Always run `codex exec` with `</dev/null`. Never start two `opencode run` at once.
