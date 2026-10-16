# Brief — tests-index

You work in a git worktree; the current folder is the repository root. Work only inside it.

## Task
Write acceptance tests for guard **Round 11** (`insight index`, `insight show`, the categories) in
`.claude/skills/workflow-design/guard/test/round11-insight-index.test.ts`, from
`.claude/skills/workflow-design/guard/SPEC.md` section "Round 11" and the categories file
`.claude/skills/workflow-design/guard/data/insight-categories.yaml`. You may import from `src/insight-index.ts`
(`insightIndex(root, rules)`, `categorize(entry, rules, title, own)`, `loadCategories(guardDir)`,
`showSections(root, entries, {categories, refs})`, `indexMarkdown(entries)`) and run the CLI
(`bun src/cli.ts insight index|show` with `cwd` set to a temporary git root). Do not change any `src/` file.

## Pieces and progress (first)
Divide the task into small pieces (one per Fails-if line is fine). Before starting, append one `planned` line per piece
to `runs/20261016-six-experts/nodes/tests-index.progress.md`, then one line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece id> · <planned|start|done|fail> · <short note>`

## Standard
- Every Round 11 Fails-if line has a test with a planted temporary root (insight files under `runs/x/insight.md` and
  `.harness-guard/insights/`, and a journal `.harness-guard/journal.jsonl` with failure records for the checks).
- Include: a section whose own `Category: spec` line overrides the rules; a planted secret in a why or an option that
  must never appear in `insight index` output; `show --category` returning only matching sections.
- `cd .claude/skills/workflow-design/guard && bun test test/round11-insight-index.test.ts` and
  `./node_modules/.bin/tsgo --noEmit -p .` — report the counts.

## Limits
May change: the test file, the progress file and your result file only. Do not commit. No other AI engine.
Stop by 15:30 +0800.

## Result
`runs/20261016-six-experts/nodes/tests-index.result.md`: `status: done|partial|fail`, one sentence; files; commands and
last lines; CONTRADICTS (with the SPEC line) or none.
