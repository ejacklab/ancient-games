# Report — run 20261016-six-experts (plan B; time-boxed: 4 hours or 6 rounds, whichever first)

**All 6 rounds done in about 55 minutes; nothing asked of the owner during the run.** Branch `feat/six-experts`
(worktree `../ancient-games-six`); the merge waits for the plan A session, which asked me to hold it until its
uncommitted mcode change to the old `four_experts.py` is committed.

## What was built
- **six-experts** (was four-experts): Linus, 范蠡, 孫子, 老子, **Dave** and **Dario**.
  - **Dave** keeps his ten rules and now **loads the project's insights**. The runner copies the guard's insight
    index and the sections of the categories the main agent names (`--insights spec,tool`) into the run's `seats/`.
    Dave cites each insight he used as `<file>#<id>`, or writes "No insight applies", and `check` enforces it.
  - **Dario**, the plain control, runs on the same model and tools as Dave, with no rules, no identity and no
    insights. It's the baseline the record never had.
  - Both run on **Claude Sonnet 5.5** (D2). The runner never starts two opencode experts at once.
- **Guard Round 11, `insight index` / `insight show`** (plan A's Part C step 9, built here):
  - The index gives one line per insight with its ids, check, source, option kinds and category, and never the
    author's text. `show` prints whole sections for an expert who loads them.
  - **Six categories** live as data (`guard/data/insight-categories.yaml`): config · tool · test · guard-check · spec ·
    own-work. A section's own `Category:` line overrides the rules.
  - The index reads `runs/<run>/insight*.md` and `.harness-guard/insights/` only. In the main checkout that is 37
    sections; the trial showed that 27 more came from experiment fixtures nested in run folders.

## How it was checked
- **Research before deciding** (`research/context-windows.md`, R1–R16). Every engine holds today's ≈25k-token
  insight load easily, and all but gpt-6.1-sol list about 1M tokens. Insights grow by ≈40–50 KB per working day.
- **The four experts decided** the categories, how related insights are picked, and the engine
  (`experts-q1q2*/compare.md`). Linus's and 老子's dissents are kept in state.md D1.
- **Tests:**
  - opencode/MiniMax wrote 14 tests for the index and 23 for the runner, from the spec.
  - I added 1 after a surviving mutant, 5 after the review and 1 after the trial. Each failed on the code it guards
    before passing.
  - 7/7 planted mutants on the index were killed, and MiniMax's 6 on the runner were too.
  - Guard 1283/1283, tsgo clean, Python 1116.
- **Independent review** by dsh/DeepSeek, which wrote none of the code or tests: 8 findings, all fixed
  (`review-answers.md`).
- **The trial** (`trial/compare.md`, n=1):
  - All six answered the same real question, and `check` passed all six.
  - Dave cited 15+ insight ids, said one named category (`tool`) was half wrong, and added sections from one not
    named (`own-work`). Dario gave a broader, general list.
  - Dave took 216 s, against Dario's 70 s on the same model.
  - **Which is better was not judged:** no blind judge has scored them.

## The path against its parent
`success-path.yaml`: parent `runs/20261016-integrate-r11-r13/success-path.yaml`, measure failures, 3 against 15
(80% fewer). *My reading:* a weak comparison, because the tasks differ; the one change tried was sending open choices to the
experts instead of the owner, and no question went to the owner.

## Provisional decisions — yours to accept or decline (state.md)
- **D1** The 6 categories (config, tool, test, guard-check, spec, own-work). The main agent names them in the question,
  and Dave picks from the index too. Linus: "six is EJ's number … not something today's corpus supports". 老子 would
  sort by the moment a fix belongs.
- **D2** Dave and Dario on Claude Sonnet 5.5 (3 of 4 experts; 范蠡 said Opus). Revisit when one question's load passes
  100k tokens.
- **D3** No Workflow script for these rounds. Every node was an outside CLI already orchestrated by the runner.
- **P0** "4 hours, 6 rounds" read as whichever comes first.

## Conflict named
Dario goes against your 2026-10-13 removal of the plain control ("don't want the control with no persona"). Your
request today is newer, so it wins; my memory is updated.

## Waiting for you or the other session
- **The merge** waits for the plan A session's mcode commit, which I then carry into `six_experts.py`.
- **The skill links:** `~/.claude/skills/four-experts` and `~/.agents/skills/four-experts` move to `six-experts` at
  merge.
- **Push:** not done.

## Failures and insights (`.harness-guard/insights/20261016-six-experts.md`, moving into this folder at merge)
- **F-5c21dd69:** my type error, caught by the type check.
- **F-7f938bdf:** my question sent opencode experts to a file outside the repo.
- **F-b696193d:** I changed `start()`'s signature and broke the other session's quota tests.

Each has 2–3 fix options for you.
