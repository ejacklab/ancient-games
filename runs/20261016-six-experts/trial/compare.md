# Six experts — what a pre-flight check should verify in a brief (trial, n=1)

Run: `trial/` · question `trial-question.md` · `--insights spec,tool` · `check`: PASS, 6 answers, 0 failures
(Dave's insight ids all in his index). Times from `nodes/trial.progress.md` / `status.json`.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Engine, model | codex gpt-6.1-sol | agy gemini-3.8-flash | dsh deepseek-flash | opencode MiniMax-M3.1 | claude-sonnet-5-5 | claude-sonnet-5-5 |
| Seconds | 72 | 111 | 201 | 251 | 216 | 70 |
| Answer (one line, quoted) | "start with readable input, accessible dependencies, and unfilled template fields … provisional, n=0" | "only five deterministic structural conditions … must deliberately not verify semantic quality" | "gate the brief's ground and its contract only — never its meaning" (eight checks) | "verify the hand-over itself and nothing else" (paths inside the run, no overwrite, filled pass/fail parts, one result path, an `UNCLEAR:` escape) | "Verify only the file's shape, never its meaning … four things … only after a replay shows no false fails, the one spec-shape pattern that misled two coders" | seven checks in order: readable, nothing that must not leave, headings, no placeholders, inputs exist, output usable, fits the context window |
| Insights cited | — | — | — | — | 15+ ids (e.g. `#F-05a1b440`, `#F-4cbb2f4b`, `#F-b7c8635f`, `#F-a03fa5b3`, `#F-c60edad6`) | — |

## Where they agree (quoted from the answers)
- **Shape, never meaning:** all six (e.g. 孫子 "never its meaning"; Dave "never its meaning"; Dario "a script cannot
  judge those and a pass would mislead").
- **Named paths exist:** all six. 孫子 and 老子 add *readable by that engine* / *inside the run*, which is the lesson of
  F-7f938bdf. Dario reached it without insights.
- **Placeholders or unfilled template parts:** Linus, 范蠡, 老子, Dave, Dario.

## What each added that the others did not (my reading)
- **Dave:** one pattern check taken from two recorded failures (spec literals mixed with instructions), gated on a
  replay against past briefs so it adds no false alarms (the guard-check insights). Also feedback on his own load:
  "`spec` was right. `tool` was half right … `own-work`, which was not named, held two rows that changed the answer".
- **Dario:** secrets ("nothing in it should not reach an outside engine") and fitting the engine's context window.
- **老子:** no attempt overwrites an earlier result; the brief carries an `UNCLEAR:` escape.
- **范蠡:** engine capability compatibility; a latency bound on the check.
- **Linus:** says the ranking is n=0, unmeasured.

## Dave against Dario (the first comparison of its kind; n=1, no conclusion)
- **Same model and tools** (both through the runner, claude-sonnet-5-5).
- Dave's answer is narrower (four checks against seven) and grounded in this project's recorded failures. Dario's is
  broader and general. Dave took about 3× longer (216 s against 70 s) and wrote 10.4 KB against 7.8 KB. *Measured.*
- Which answer is better was **not judged**: no blind judge has scored them. One question, one run: n=1.

## Found by the trial
- Dave said a named category was half wrong (`tool`), and that one not named (`own-work`) held two that mattered. The
  "(c) both" picking (D1) did its job here: he added sections beyond the named ones.
- The index includes insight files from inside experiment folders (`runs/20261015-ts-hybrid/e4/runs2/B3/insight.md`),
  i.e. insights written by test agents in an effectiveness run. Dave cited two of them. Open: should the index skip
  nested run folders? *my reading: yes, or mark them*.

## Check
`six_experts.py check trial` → PASS, 6 answers, 0 failures. Engines: no fallback; Linus ran on Codex (its quota was
back). The check was written by Claude; it checks sections, item and insight-id citations, and Chinese quotes, not
whether the advice is good.
