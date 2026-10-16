# Plan B — six experts: Dave learns from insights, Dario is the plain control (session 1159cce6, 2026-10-16)

Plan A (`streamed-dancing-hinton.md`, "every task teaches") is already executing in another session; this is a
separate plan.

## Context
EJ: "what makes a person very powerful is the insight". Today an insight is written when a task fails and then left in
its run folder. Nothing reads it again, so failures repeat. The Dave review (this session) showed two things: Dave's
value is measuring and predicting, and nothing has ever compared him with a plain Claude. So:
- **Dave** keeps his ten rules and also loads the insights, sorted into **6 categories**, reading the categories
  related to each task.
- **Dario** is a new plain-Claude control: no persona, no rules, no insights. He is the baseline the record never had.
- **four-experts becomes six-experts**: Linus, 范蠡, 孫子, 老子, Dave and Dario.
- The four experts design the categories and the loading. They also research which engine has a 1M-token context.

Measured now: the insights are 21 files, about 93 KB (≈ 25k tokens), so a 1M window is not needed yet; it matters as
they grow. The `Source` field already sorts them as instruction 22, check 18, tool 14, config 8.

**Limit: 4 hours or 6 rounds, whichever comes first** (EJ: "4 hours, 6 rounds"; "whichever first" is my reading). A
round is one pass from criteria to score and path (method 3.8 item 14).

## Shared with plan A (one copy each, no blending)
- **The insight index is plan A's Part C step 9 (`insight index`).** Dave loads through that one command. If
  it isn't built when this run needs it, this run builds it to plan A's spec (ids, checks, sources and kinds out,
  the text stays in the file). It doesn't build a second collector.
- **Codex is at its usage limit** (plan A's O1 notes Linus ran on opencode). Tests and the review use the
  engines that answer, each canary-proved at the start. Linus runs on Codex only if it is back.
- **The rename touches plan A's references** ("the five experts" in D4, its run folder). Old run folders keep their
  names; live docs move to six-experts.

## Rounds
1. **Start.** Write `runs/<date>-six-experts/` with criteria and state, run `deadline start --minutes 240 --run …`, and
   canary each engine.
2. **Round 1, research and decisions.**
   - The researcher (findings returned as text, saved by me) covers each engine's context window, price and long-file
     handling: Claude Opus/Sonnet 5.5, Gemini via agy, DeepSeek via dsh, MiniMax via opencode, and Codex if back. It
     also measures the insights' growth from run dates. Each finding labelled verified or reported.
   - The four experts then decide, with the research and the vision and use cases attached (`time-boxed-decision.md`,
     `--progress`):
     - Q1: the 6 categories, seeded with the 4 Source kinds and the task types, and how "related to this task" is
       picked;
     - Q2: Dave's engine and model.
     These become provisional decisions D1–D2.
3. **Round 2, the insight index and categories.** The `insight index` (or its use) plus a `category` per section, from
   Q1.
4. **Round 3, Dave and Dario.**
   - Dave's brief loads the index and then the related categories' sections, and cites the insight ids he used.
   - Dario's seat has no list, no identity and no insights. He runs on the same engine, model and tools as Dave, which
     removes the tool confound the Dave review found.
5. **Round 4, the rename.**
   - `.claude/skills/four-experts` → `six-experts`, and `four_experts.py` → `six_experts.py`.
   - `check` handles Dario: sections only, no citations.
   - Live references move: method 3.3/3.5/3.8, the workflow-design skill, templates, memory.
   - The `~/.claude/skills` and `~/.agents/skills` links move. That's an environment change, done with this plan's
     approval.
6. **Round 5, tests and review.**
   - `tests/test_six_experts.py`, each test shown failing first:
     - the prompt is the command's last argument;
     - Dario's brief holds no rules or insights;
     - Dave's brief names its categories;
     - the index holds every section once.
   - Then planted mutants, and an independent review by an engine that wrote none of it.
7. **Round 6, the first trial (n=1).** All six answer one real question. It's the first measured Dave vs Dario, timed by
   the progress lines. Labelled n=1, no conclusion.
8. **Close.** Report, commit; the push waits for you.

## Verification
- `env -u NO_COLOR python3 -m pytest -q` and the guard suite with tsgo.
- `six_experts.py run --only dario,dave` gives both answers, and `check` passes both.
- The index count equals the `## F-` and `## great:` headings across the sources.
- `deadline status` shows the workers' pieces during the run.

## Provisional (the experts advise, I decide, you accept or decline at the end)
The 6 categories · how related insights are picked · Dave's engine and model · "whichever comes first" for the limit.
